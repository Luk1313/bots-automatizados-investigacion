# SecAlertBot – Alertas de intentos de ingreso y eventos (SSH/Docker/Google/Microsoft)

Monitorea intentos de acceso a **servidores Linux (SSH)**, **eventos de contenedores Docker**, y **alertas de acceso de Google/Microsoft**, enviando notificaciones a **Slack, Telegram y WhatsApp (Twilio)**.

> ⚠️ Este proyecto es una **plantilla funcional mínima**. Ajusta rutas de logs, permisos y credenciales según tu entorno.

## Características
- Toma de eventos de **/var/log/auth.log** (fallos SSH).
- Lectura de **eventos Docker** (start/stop/exec). 
- Ingesta opcional de **alertas de inicio de sesión**:
  - **Google**: vía Gmail API buscando correos de seguridad.
  - **Microsoft**: vía Microsoft Graph (auditLogs/signIns).
- **De-duplicación** y **estado** para no alertar repetidos.
- Notificación configurable: Slack, Telegram y/o WhatsApp.

## Requisitos
- Python 3.10+
- Permisos para leer `/var/log/auth.log` y acceso al socket Docker si corresponde.
- Credenciales para APIs (opcionales según integración activada).

```bash
pip install -r requirements.txt
cp .env.example .env   # Rellena variables
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

## Variables de entorno (.env)
```
# --- Canales de alerta (opcionalmente activa uno o varios) ---
SLACK_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TWILIO_SID=
TWILIO_TOKEN=
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+569XXXXXXX

# --- Google (vía Gmail API con service account o OAuth local) ---
GOOGLE_CREDENTIALS_FILE=service_account.json
GOOGLE_GMAIL_QUERY=from:(no-reply@accounts.google.com) subject:(Alerta de seguridad OR Security alert)

# --- Microsoft Graph (aplicación Entra ID) ---
MS_TENANT_ID=
MS_CLIENT_ID=
MS_CLIENT_SECRET=

# --- General ---
STATE_FILE=.state.json
AUTH_LOG_PATH=/var/log/auth.log
DOCKER_ENABLED=true
GMAIL_ENABLED=false
MSGRAPH_ENABLED=false
```

## Endpoints
- `GET /health` → Estado del servicio.
- `POST /test` → Envía una alerta de prueba a los canales configurados.

## Seguridad
- Recomendado ejecutar con usuario dedicado (systemd) y acceso restringido al socket Docker.
- Mantener secretos fuera del repo. Usar un Secret Manager en producción.

## Despliegue (Docker Compose ejemplo)
```yaml
services:
  secalertbot:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./sec_alert_bot:/app
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/log/auth.log:/var/log/auth.log:ro
      - ./creds:/app/creds
    env_file:
      - ./.env
    command: bash -lc "pip install -r requirements.txt && uvicorn app:app --host 0.0.0.0 --port 8001"
    restart: unless-stopped
```
