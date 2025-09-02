from fastapi import FastAPI
from loguru import logger
from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler
from alerts import notify_all
from watchers import check_auth_log, check_docker_events, check_gmail_security_alerts, check_ms_signins

load_dotenv()
app = FastAPI(title="SecAlertBot")

scheduler = BackgroundScheduler()
scheduler.start()

@app.on_event("startup")
def _startup():
    logger.info("SecAlertBot iniciado")
    # Cada 60s: revisar auth.log
    scheduler.add_job(check_auth_log, "interval", seconds=60, id="authlog")
    # Cada 90s: eventos Docker
    if os.getenv("DOCKER_ENABLED", "false").lower() == "true":
        scheduler.add_job(check_docker_events, "interval", seconds=90, id="docker")
    # Cada 180s: Gmail
    if os.getenv("GMAIL_ENABLED", "false").lower() == "true":
        scheduler.add_job(check_gmail_security_alerts, "interval", seconds=180, id="gmail")
    # Cada 180s: Microsoft Graph
    if os.getenv("MSGRAPH_ENABLED", "false").lower() == "true":
        scheduler.add_job(check_ms_signins, "interval", seconds=180, id="msgraph")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/test")
def test():
    notify_all("🔔 *Prueba de alerta* – SecAlertBot está operativo.")
    return {"ok": True}
