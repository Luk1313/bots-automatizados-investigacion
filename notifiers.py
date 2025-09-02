import os, requests
from twilio.rest import Client

def notify_slack(text: str):
    url = os.getenv("SLACK_WEBHOOK_URL")
    if url:
        requests.post(url, json={"text": text})

def notify_telegram(text: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage",
                     params={"chat_id": chat_id, "text": text})

def notify_whatsapp(text: str):
    sid = os.getenv("TWILIO_SID")
    tok = os.getenv("TWILIO_TOKEN")
    w_from = os.getenv("TWILIO_WHATSAPP_FROM")
    w_to = os.getenv("TWILIO_WHATSAPP_TO")
    if sid and tok and w_from and w_to:
        Client(sid, tok).messages.create(body=text, from_=w_from, to=w_to)
