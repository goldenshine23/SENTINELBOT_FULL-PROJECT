import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id")

def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram error: {e}")
