import sqlite3
from app.config import settings


def get_conn():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_reports (
            report_date TEXT NOT NULL,
            phone TEXT NOT NULL,
            name TEXT,
            role TEXT,
            port TEXT,
            center TEXT,
            location_lat REAL,
            location_lng REAL,
            location_name TEXT,
            photo_media_id TEXT,
            photo_mime_type TEXT,
            text_reply TEXT,
            sent_at TEXT,
            updated_at TEXT,
            PRIMARY KEY (report_date, phone)
        )
        """
    )
    conn.commit()
    conn.close()
