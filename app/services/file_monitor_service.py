# app/services/file_monitor_service.py

import os
import threading
from ghostguard.file_interceptor import FileInterceptor

class FileMonitorService:
    def __init__(self, watch_directory="C:\\"):
        self.watch_directory = watch_directory
        self.interceptor = FileInterceptor(self.watch_directory)
        self.thread = None
        self.running = False

    def start(self):
        if not os.path.exists(self.watch_directory):
            raise ValueError(f"Directory does not exist: {self.watch_directory}")

        if self.running:
            print("[!] File monitoring service is already running.")
            return

        print(f"[✓] Starting file monitor service on: {self.watch_directory}")
        self.running = True
        self.thread = threading.Thread(target=self.interceptor.watch, daemon=True)
        self.thread.start()

    def stop(self):
        # Add logic here if your FileInterceptor supports stopping
        print("[!] File monitoring cannot be cleanly stopped without enhancements.")
        self.running = False
        # If you want to implement a way to signal the thread to stop,
        # modify FileInterceptor to support a stop flag.

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

# Example for standalone testing
if __name__ == "__main__":
    monitor = FileMonitorService(watch_directory="C:\\")
    monitor.start()

    try:
        while True:
            pass  # Keep main thread alive
    except KeyboardInterrupt:
        print("[*] Stopping monitor service...")
        monitor.stop()
