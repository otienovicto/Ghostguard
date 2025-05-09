# app/notifications/email_notifier.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config


class EmailNotifier:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None, sender_email=None):
        self.smtp_server = smtp_server or Config.MAIL_SERVER
        self.smtp_port = smtp_port or Config.MAIL_PORT
        self.username = username or Config.MAIL_USERNAME
        self.password = password or Config.MAIL_PASSWORD
        self.sender_email = sender_email or Config.MAIL_DEFAULT_SENDER

    def send_email(self, subject, message, recipient=None):
        try:
            recipient = recipient or Config.MAIL_DEFAULT_RECIPIENT
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()

            print(f"[✓] Email sent to {recipient}: {subject}")
        except Exception as e:
            print(f"[✗] Failed to send email: {e}")
