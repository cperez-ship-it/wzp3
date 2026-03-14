from datetime import datetime
from app.db import get_conn


def upsert_contact_day(report_date: str, contact: dict):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO daily_reports(report_date, phone, name, role, port, center, sent_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(report_date, phone) DO UPDATE SET
            name=excluded.name,
            role=excluded.role,
            port=excluded.port,
            center=excluded.center,
            sent_at=excluded.sent_at,
            updated_at=excluded.updated_at
        """,
        (
            report_date,
            contact["phone"],
            contact.get("name"),
            contact.get("role"),
            contact.get("port"),
            contact.get("center"),
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def _update_field(report_date: str, phone: str, field_sql: str, params: tuple):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE daily_reports SET {field_sql}, updated_at=? WHERE report_date=? AND phone=?",
        params + (datetime.utcnow().isoformat(), report_date, phone),
    )
    conn.commit()
    conn.close()


def update_location(report_date: str, phone: str, lat, lng, name):
    _update_field(report_date, phone, "location_lat=?, location_lng=?, location_name=?", (lat, lng, name))


def update_photo(report_date: str, phone: str, media_id, mime_type):
    _update_field(report_date, phone, "photo_media_id=?, photo_mime_type=?", (media_id, mime_type))


def update_text(report_date: str, phone: str, text):
    _update_field(report_date, phone, "text_reply=?", (text,))


def get_reports_by_date(report_date: str):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM daily_reports WHERE report_date=? ORDER BY center, name", (report_date,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_pending_by_date(report_date: str):
    rows = get_reports_by_date(report_date)
    pending = []
    for r in rows:
        missing = []
        if not r.get("location_lat"):
            missing.append("ubicación")
        if not r.get("photo_media_id"):
            missing.append("foto")
        if (r.get("text_reply") or "").strip().upper() != "OK INICIO":
            missing.append("OK INICIO")
        if missing:
            r["missing"] = missing
            pending.append(r)
    return pending
