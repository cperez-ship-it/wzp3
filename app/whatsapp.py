from __future__ import annotations
import requests
from app.config import settings

BASE = "https://graph.facebook.com/v23.0"


def _headers():
    return {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }


def _send(payload: dict):
    if not settings.WHATSAPP_TOKEN or not settings.PHONE_NUMBER_ID:
        return {"skipped": True, "reason": "faltan credenciales"}
    url = f"{BASE}/{settings.PHONE_NUMBER_ID}/messages"
    try:
        r = requests.post(url, headers=_headers(), json=payload, timeout=20)
        return {"status_code": r.status_code, "body": r.text}
    except Exception as e:
        return {"error": str(e)}


def send_text(to: str, body: str):
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"preview_url": False, "body": body}}
    return _send(payload)


def send_location_request(to: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "location_request_message",
            "body": {"text": "Comparte tu ubicación para validar arribo al centro."},
            "action": {"name": "send_location"},
        },
    }
    return _send(payload)


def send_ack(to: str):
    return send_text(to, "Recibido. Gracias. Seguimos monitoreando el inicio de faena.")
