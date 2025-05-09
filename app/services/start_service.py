# app/services/start_service.py

from app.services.file_monitor_service import FileMonitorService

monitor = FileMonitorService(watch_directory="C:\\")  # Or a more specific path
monitor.start()

print("[✓] File monitoring service started. Press Ctrl+C to stop.")

try:
    while True:
        pass  # Keep the script alive
except KeyboardInterrupt:
    print("\n[*] Stopping service manually...")
    monitor.stop()
