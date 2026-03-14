# Bot WhatsApp Supervisión Buceo — v5

Versión mejorada para pruebas locales y despliegue simple en Render.

## Qué hace
- Envía mensaje diario a supervisores y operaciones.
- Inserta estado de puerto/zona, EPP y materiales por rol.
- Inserta charla diaria de seguridad.
- Solicita ubicación y foto del centro.
- Registra respuestas en SQLite.
- Muestra dashboard web y exportación CSV.
- Incluye rutas manuales para disparar el envío y el resumen.

## Estructura importante
- `app/` → aplicación principal Flask
- `bot/` → scripts auxiliares de prueba
- `data/` → contactos, puertos, materiales y charlas
- `templates/` → dashboard
- `run.py` → punto de inicio
- `render.yaml` → despliegue rápido en Render

## 1. Configuración local
Copiar `.env.example` a `.env` y completar:

```env
WHATSAPP_TOKEN=pega_aqui_tu_token_meta
PHONE_NUMBER_ID=pega_aqui_tu_phone_number_id
VERIFY_TOKEN=crea_un_token_simple
ADMIN_PHONE=56912345678
TZ=America/Santiago
DAILY_SEND_TIME=07:00
FOLLOWUP_REMINDER_TIME=09:30
COMPANY_NAME=Servicios Acuícolas del Sur
```

## 2. Instalar
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
En Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Ejecutar localmente
```bash
python run.py
```
Abrir:
- `http://localhost:8080/health`
- `http://localhost:8080/dashboard`

## 4. Prueba manual sin esperar el horario
Con la app arriba:
- `http://localhost:8080/run/daily`
- `http://localhost:8080/run/summary`

## 5. Verificar webhook en Meta
URL del webhook:
```text
https://TU-SERVICIO.onrender.com/webhook
```
Verify token:
```text
el mismo valor de VERIFY_TOKEN
```
Suscribirse al menos a `messages`.

## 6. Despliegue simple en Render
### Opción A — con `render.yaml`
1. Subir esta carpeta a GitHub.
2. En Render elegir **New +** → **Blueprint**.
3. Seleccionar tu repositorio.
4. Crear el servicio.
5. Agregar variables de entorno que faltan:
   - `WHATSAPP_TOKEN`
   - `PHONE_NUMBER_ID`
   - `VERIFY_TOKEN`
   - `ADMIN_PHONE`

### Opción B — Web Service manual
- Build Command: `pip install -r requirements.txt`
- Start Command: `python run.py`
- Health Check Path: `/health`

## 7. Archivos a personalizar
### `data/contacts.csv`
Columnas esperadas:
- `name`
- `phone`
- `role`
- `center`
- `port`
- `active`

### `data/ports_status.csv`
- `port`
- `status`
- `window`
- `notes`

### `data/materials_by_role.csv`
- `role`
- `materials`

### `data/safety_talks.csv`
- `title`
- `talk`

## 8. Limitaciones reales
- Para mensajes iniciados por la empresa fuera de la ventana de 24 horas normalmente debes usar plantillas aprobadas en WhatsApp Business Platform.
- La recepción de imágenes y ubicación depende de que el webhook esté correctamente configurado y accesible públicamente.
- Esta versión es una base funcional y editable, no un producto certificado.

## 9. Idea de operación diaria
- 07:00 → envío al equipo
- 09:30 → resumen de pendientes a administración
- Dashboard durante la mañana para revisión

## 10. Soporte de prueba local
Si no quieres conectar Meta todavía, arranca el proyecto y revisa las rutas `/health` y `/dashboard`. Luego personaliza CSV antes de subirlo.
