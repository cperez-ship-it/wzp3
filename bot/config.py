import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID", "")
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "devtoken")
    ADMIN_PHONE: str = os.getenv("ADMIN_PHONE", "")
    APP_PORT: int = int(os.getenv("APP_PORT", "8080"))
    TZ: str = os.getenv("TZ", "America/Santiago")
    DAILY_SEND_TIME: str = os.getenv("DAILY_SEND_TIME", "07:00")
    FOLLOWUP_REMINDER_TIME: str = os.getenv("FOLLOWUP_REMINDER_TIME", "09:30")
    LOCATION_REQUEST_TEMPLATE: str = os.getenv("LOCATION_REQUEST_TEMPLATE", "solicitud_ubicacion")
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Servicios Acuícolas del Sur")
    DAILY_PORT_STATUS_SOURCE: str = os.getenv("DAILY_PORT_STATUS_SOURCE", "data/ports_status.csv")
    DB_PATH: str = os.getenv("DB_PATH", "daily_reports.db")

settings = Settings()
