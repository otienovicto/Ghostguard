# app/notifications/slack_notifier.py

import requests
from app.config import Config

class SlackNotifier:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or Config.SLACK_WEBHOOK_URL

    def send_slack_notification(self, message):
        try:
            payload = {
                "text": message
            }
            response = requests.post(self.webhook_url, json=payload)

            if response.status_code == 200:
                print(f"[✓] Slack notification sent: {message}")
            else:
                print(f"[✗] Slack notification failed: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[✗] Exception occurred while sending Slack notification: {e}")
