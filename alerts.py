import os, json, requests
from slack_sdk.webhook import WebhookClient
from twilio.rest import Client

def _slack(msg: str):
    url = os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        return
    WebhookClient(url).send(text=msg)

def _telegram(msg: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return
    requests.get(f"https://api.telegram.org/bot{token}/sendMessage",
                 params={"chat_id": chat_id, "text": msg, "parse_mode":"Markdown"})

def _whatsapp(msg: str):
    sid = os.getenv("TWILIO_SID")
    tok = os.getenv("TWILIO_TOKEN")
    w_from = os.getenv("TWILIO_WHATSAPP_FROM")
    w_to = os.getenv("TWILIO_WHATSAPP_TO")
    if not (sid and tok and w_from and w_to):
        return
    Client(sid, tok).messages.create(body=msg, from_=w_from, to=w_to)

def notify_all(message: str):
    _slack(message)
    _telegram(message)
    _whatsapp(message)
