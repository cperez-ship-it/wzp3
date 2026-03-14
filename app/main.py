from flask import Flask, jsonify, render_template, request, Response
import csv
import io
from app.config import settings
from app.db import init_db
from app.repository import update_location, update_photo, update_text, get_reports_by_date
from app.scheduler import start_scheduler, daily_dispatch, followup_summary
from app.services import today_str
from app.whatsapp import send_ack

app = Flask(__name__, template_folder="../templates")
app.config["APP_PORT"] = settings.APP_PORT
_bootstrapped = False


def normalize_phone(value: str) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def bootstrap():
    global _bootstrapped
    if _bootstrapped:
        return
    init_db()
    start_scheduler()
    _bootstrapped = True


@app.route("/health")
def health():
    return {"ok": True, "company": settings.COMPANY_NAME}


@app.route("/dashboard")
def dashboard():
    report_date = request.args.get("date") or today_str()
    rows = get_reports_by_date(report_date)
    totals = {
        "total": len(rows),
        "with_location": sum(1 for r in rows if r.get("location_lat")),
        "with_photo": sum(1 for r in rows if r.get("photo_media_id")),
        "with_ok": sum(1 for r in rows if (r.get("text_reply") or "").strip().upper() == "OK INICIO"),
    }
    return render_template("dashboard.html", report_date=report_date, rows=rows, totals=totals, company=settings.COMPANY_NAME)


@app.route("/export.csv")
def export_csv():
    report_date = request.args.get("date") or today_str()
    rows = get_reports_by_date(report_date)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()) if rows else ["report_date", "phone"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename=reporte_{report_date}.csv"})


@app.route("/run/daily", methods=["GET", "POST"])
def run_daily():
    daily_dispatch()
    return jsonify({"ok": True, "message": "envío diario ejecutado"})


@app.route("/run/summary", methods=["GET", "POST"])
def run_summary():
    followup_summary()
    return jsonify({"ok": True, "message": "resumen ejecutado"})


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return challenge, 200
    return "verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {}
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                phone = normalize_phone(msg.get("from", ""))
                report_date = today_str()
                msg_type = msg.get("type")
                if msg_type == "location":
                    loc = msg.get("location", {})
                    update_location(report_date, phone, loc.get("latitude"), loc.get("longitude"), loc.get("name") or loc.get("address"))
                    send_ack(phone)
                elif msg_type == "image":
                    img = msg.get("image", {})
                    update_photo(report_date, phone, img.get("id"), img.get("mime_type"))
                    send_ack(phone)
                elif msg_type == "text":
                    text = ((msg.get("text") or {}).get("body") or "").strip()
                    update_text(report_date, phone, text)
                    if text.upper() == "OK INICIO":
                        send_ack(phone)
    return jsonify({"received": True})
