from __future__ import annotations
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from app.config import settings


def now_local() -> datetime:
    return datetime.now(ZoneInfo(settings.TZ))


def today_str() -> str:
    return now_local().strftime("%Y-%m-%d")


def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path).fillna("")


def get_contacts() -> list[dict]:
    df = read_csv("data/contacts.csv")
    df["active"] = df["active"].astype(str).str.lower().isin(["1", "true", "si", "sí", "yes"])
    return df[df["active"]].to_dict(orient="records")


def get_port_status(port: str) -> dict:
    df = read_csv(settings.DAILY_PORT_STATUS_SOURCE)
    if df.empty:
        return {"status": "Sin dato", "window": "Sin dato", "notes": "Actualizar archivo de puertos"}
    row = df[df["port"].astype(str).str.lower() == str(port).lower()]
    if row.empty:
        return {"status": "Sin dato", "window": "Sin dato", "notes": "Puerto no encontrado en ports_status.csv"}
    row = row.iloc[0]
    return {
        "status": row.get("status", "Sin dato"),
        "window": row.get("window", "Sin dato"),
        "notes": row.get("notes", ""),
    }


def get_materials(role: str) -> str:
    df = read_csv("data/materials_by_role.csv")
    row = df[df["role"].astype(str).str.lower() == str(role).lower()]
    if row.empty:
        return "Revisar EPP base, equipo de comunicación, equipo de inmersión y check previo."
    return row.iloc[0].get("materials", "")


def get_talk_for_today() -> dict:
    df = read_csv("data/safety_talks.csv")
    if df.empty:
        return {"title": "Charla de seguridad", "talk": "Realizar AST y verificar condiciones antes de iniciar."}
    idx = now_local().timetuple().tm_yday % len(df)
    row = df.iloc[idx]
    return {"title": row.get("title", "Charla diaria"), "talk": row.get("talk", "")}


def compose_daily_message(contact: dict) -> str:
    port_status = get_port_status(contact.get("port", ""))
    materials = get_materials(contact.get("role", ""))
    talk = get_talk_for_today()
    return (
        f"*{settings.COMPANY_NAME}*\n"
        f"Hola {contact.get('name','equipo')}, buen día.\n\n"
        f"*Centro:* {contact.get('center','-')}\n"
        f"*Puerto/Zona:* {contact.get('port','-')}\n"
        f"*Estado puerto:* {port_status['status']}\n"
        f"*Ventana operacional:* {port_status['window']}\n"
        f"*Observación:* {port_status['notes'] or 'Sin observaciones'}\n\n"
        f"*Materiales/EPP obligatorios para {contact.get('role','tu rol')}:*\n{materials}\n\n"
        f"*Charla diaria de seguridad: {talk['title']}*\n{talk['talk']}\n\n"
        f"Antes de iniciar envía por este chat:\n"
        f"1. *Ubicación en tiempo real*\n"
        f"2. *Foto del centro / frente de trabajo*\n"
        f"3. Mensaje *OK INICIO*\n\n"
        f"Responder apenas estén en el punto de operación."
    )
