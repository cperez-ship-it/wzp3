from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.repository import upsert_contact_day, get_pending_by_date
from app.services import get_contacts, compose_daily_message, today_str
from app.whatsapp import send_text, send_location_request

scheduler = BackgroundScheduler(timezone=settings.TZ)


def parse_hhmm(value: str):
    hh, mm = value.split(":")
    return int(hh), int(mm)


def daily_dispatch():
    report_date = today_str()
    for contact in get_contacts():
        upsert_contact_day(report_date, contact)
        send_text(contact["phone"], compose_daily_message(contact))
        send_location_request(contact["phone"])


def followup_summary():
    if not settings.ADMIN_PHONE:
        return
    pending = get_pending_by_date(today_str())
    if not pending:
        send_text(settings.ADMIN_PHONE, "Resumen diario: todo el equipo reportó ubicación, foto y OK INICIO.")
        return
    lines = ["Resumen diario de pendientes:"]
    for item in pending:
        lines.append(f"- {item['name']} | {item['center']} | falta: {', '.join(item['missing'])}")
    send_text(settings.ADMIN_PHONE, "\n".join(lines[:40]))


def start_scheduler():
    if scheduler.running:
        return
    daily_h, daily_m = parse_hhmm(settings.DAILY_SEND_TIME)
    sum_h, sum_m = parse_hhmm(settings.FOLLOWUP_REMINDER_TIME)
    scheduler.add_job(daily_dispatch, "cron", hour=daily_h, minute=daily_m, id="daily_dispatch", replace_existing=True)
    scheduler.add_job(followup_summary, "cron", hour=sum_h, minute=sum_m, id="followup_summary", replace_existing=True)
    scheduler.start()
