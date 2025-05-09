# app/notifications/telegram_notifier.py

import requests
from app.config import Config

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or Config.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or Config.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_telegram_message(self, message):
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(self.api_url, json=payload)

            if response.status_code == 200:
                print(f"[✓] Telegram message sent: {message}")
            else:
                print(f"[✗] Telegram message failed: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[✗] Exception occurred while sending Telegram message: {e}")
