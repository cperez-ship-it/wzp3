# Bot WhatsApp Supervisión v4

Esta versión corrige la estructura del ZIP e incluye **carpeta `bot/`** además de `app/`, para que sea más fácil ubicar los archivos.

## Estructura
- `bot/` → acceso rápido para pruebas manuales
- `app/` → aplicación principal
- `data/` → contactos, puertos, materiales y charlas
- `templates/` → dashboard
- `run.py` → inicia el servidor
- `.env.example` → variables de entorno

## Instalación rápida
1. Crear `.env` desde `.env.example`
2. Instalar dependencias:
   - Mac: `python3 -m pip install -r requirements.txt`
   - Windows: `py -m pip install -r requirements.txt`
3. Ejecutar:
   - Mac: doble clic en `iniciar_mac.command`
   - Windows: doble clic en `iniciar_windows.bat`
   - o terminal: `python3 run.py`

## Prueba simple
Para ver el mensaje diario que recibiría un supervisor:
- Mac: `python3 bot/send_test.py`
- Windows: `py bot\send_test.py`

## Dashboard
Abrir en el navegador:
- `http://localhost:5000/dashboard`

## Datos a cargar
Editar estos CSV:
- `data/contacts.csv`
- `data/ports_status.csv`
- `data/materials_by_role.csv`
- `data/safety_talks.csv`

## Producción
Para que funcione con WhatsApp Cloud API real necesitas:
- Token de Meta
- Phone Number ID
- Webhook público
- Plantilla aprobada para mensajes iniciados por la empresa

## Nota
La carpeta `bot/` se agregó especialmente porque en la versión anterior la estructura quedó bajo `app/` y podía dar la impresión de que faltaban archivos.
