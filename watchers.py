import os, json, time, re, datetime as dt
from loguru import logger
from alerts import notify_all
from state import State
import docker
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import msal
import requests

STATE = State(os.getenv("STATE_FILE", ".state.json"))

# --- SSH auth.log ---
def check_auth_log():
    path = os.getenv("AUTH_LOG_PATH", "/var/log/auth.log")
    last_pos = STATE.get("authlog_pos", 0)
    try:
        with open(path, "rb") as f:
            f.seek(last_pos)
            new = f.read().decode("utf-8", errors="ignore").splitlines()
            STATE.set("authlog_pos", f.tell())
    except FileNotFoundError:
        logger.warning("auth.log no encontrado")
        return

    pattern = re.compile(r"Failed password for .* from (?P<ip>\d+\.\d+\.\d+\.\d+)")
    events = []
    for line in new:
        m = pattern.search(line)
        if m:
            ip = m.group("ip")
            ts = dt.datetime.utcnow().isoformat()
            events.append((ts, ip, line))

    if events:
        msg = "🚨 *Intentos SSH fallidos* encontrados:\n" + "\n".join([f"- {e[0]} IP {e[1]}" for e in events[:10]])
        notify_all(msg)

# --- Docker events ---
def check_docker_events():
    try:
        client = docker.from_env()
        last = STATE.get("docker_since", int(time.time()) - 120)
        events = client.api.events(since=last, decode=True, filters={"type":"container"})
        got = []
        now = int(time.time())
        for ev in events:
            if ev.get("Type")=="container" and ev.get("status") in {"start","die","exec_create"}:
                name = ev.get("Actor",{}).get("Attributes",{}).get("name")
                got.append(f"{ev.get('status')} → {name}")
        STATE.set("docker_since", now)
        if got:
            notify_all("🐳 *Eventos Docker*:\n" + "\n".join(f"- {g}" for g in got[:10]))
    except Exception as e:
        logger.warning(f"Docker no disponible: {e}")

# --- Gmail security alerts ---
def check_gmail_security_alerts():
    creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
    if not creds_file or not os.path.exists(creds_file):
        return
    query = os.getenv("GOOGLE_GMAIL_QUERY", "subject:Security alert")
    creds = Credentials.from_service_account_file(creds_file, scopes=[
        "https://www.googleapis.com/auth/gmail.readonly"
    ])
    svc = build("gmail", "v1", credentials=creds)
    last_ts = STATE.get("gmail_last_epoch", 0)
    res = svc.users().messages().list(userId="me", q=query).execute()
    ids = [m["id"] for m in res.get("messages", [])]
    seen = set(STATE.get("gmail_seen_ids", []))
    new_ids = [i for i in ids if i not in seen]
    if new_ids:
        notify_all(f"🔐 *Gmail/Google:* {len(new_ids)} alerta(s) de seguridad nuevas.")
        seen.update(new_ids)
        STATE.set("gmail_seen_ids", list(seen))

# --- Microsoft Graph signIns ---
def check_ms_signins():
    tenant = os.getenv("MS_TENANT_ID")
    client_id = os.getenv("MS_CLIENT_ID")
    secret = os.getenv("MS_CLIENT_SECRET")
    if not (tenant and client_id and secret):
        return
    app = msal.ConfidentialClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant}",
        client_credential=secret
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in token:
        return
    last = STATE.get("ms_last_dt", (dt.datetime.utcnow()-dt.timedelta(minutes=10)).isoformat()+"Z")
    url = f"https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=createdDateTime ge {last}"
    r = requests.get(url, headers={"Authorization": f"Bearer {token['access_token']}"})
    if r.status_code == 200:
        data = r.json().get("value", [])
        if data:
            notify_all(f"🪟 *Microsoft Entra:* {len(data)} registro(s) de inicio de sesión recientes.")
        STATE.set("ms_last_dt", dt.datetime.utcnow().isoformat()+"Z")
