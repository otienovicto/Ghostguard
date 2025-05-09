# app/notifications/notifier.py

class Notifier:
    def __init__(self, notifiers=None):
        """
        Accepts a list of notifier instances (EmailNotifier, SlackNotifier, TelegramNotifier).
        """
        if notifiers is None:
            notifiers = []
        self.notifiers = notifiers

    def add_notifier(self, notifier):
        """
        Dynamically add a new notifier (if needed).
        """
        self.notifiers.append(notifier)

    def notify(self, message, subject=None):
        """
        Sends a notification through all configured notifiers.
        :param message: The message content.
        :param subject: Optional subject line (used for email).
        """
        for notifier in self.notifiers:
            try:
                if hasattr(notifier, 'send_email') and subject:
                    notifier.send_email(subject=subject, message=message)
                elif hasattr(notifier, 'send_slack_notification'):
                    notifier.send_slack_notification(message=message)
                elif hasattr(notifier, 'send_telegram_message'):
                    notifier.send_telegram_message(message=message)
            except Exception as e:
                print(f"[!] Failed to send notification via {notifier.__class__.__name__}: {e}")
