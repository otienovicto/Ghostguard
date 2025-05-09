# app/notifications/__init__.py

from .notifier import Notifier
from .email_notifier import EmailNotifier
from .slack_notifier import SlackNotifier
from .telegram_notifier import TelegramNotifier

# Initialize global notifiers (can be configured later)
email_notifier = EmailNotifier()
slack_notifier = SlackNotifier()
telegram_notifier = TelegramNotifier()

notifier = Notifier([
    email_notifier,
    slack_notifier,
    telegram_notifier
])
