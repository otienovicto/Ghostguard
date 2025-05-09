import os
from datetime import datetime

class GhostLogger:
    def __init__(self, log_dir="ghostguard/logs", log_file="ghostguard.log"):
        self.log_dir = log_dir
        self.log_file = os.path.join(self.log_dir, log_file)

        # Ensure the logs directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level.upper()}] {message}\n"

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"Logging failed: {e}")

        print(entry.strip())  # Also print to console

    def log_error(self, message):
        self.log(message, level="ERROR")

    def log_warning(self, message):
        self.log(message, level="WARNING")

    def log_success(self, message):
        self.log(message, level="SUCCESS")

# Example usage
if __name__ == "__main__":
    logger = GhostLogger()
    logger.log("GhostGuard logger initialized.")
    logger.log_warning("This is a warning message.")
    logger.log_error("This is an error message.")
    logger.log_success("Action completed successfully.")
