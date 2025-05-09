import os
import sys
import winreg

def enable_auto_start(app_name="GhostGuard", script_path=None):
    """
    Enables auto-start for the app by adding it to Windows startup registry.
    :param app_name: Name to use in the Windows registry (e.g., GhostGuard)
    :param script_path: Path to the script to run at startup.
    """
    try:
        if script_path is None:
            script_path = os.path.abspath(sys.argv[0])

        python_path = sys.executable
        command = f'"{python_path}" "{script_path}"'

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)

        print(f"[✓] Auto-start enabled for: {app_name}")
        print(f"    Launch Command: {command}")

    except Exception as e:
        print(f"[✗] Failed to enable auto-start: {e}")

def disable_auto_start(app_name="GhostGuard"):
    """
    Removes the app from Windows startup registry.
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_ALL_ACCESS
        )
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        print(f"[✓] Auto-start disabled for: {app_name}")
    except FileNotFoundError:
        print(f"[!] No startup entry found for: {app_name}")
    except Exception as e:
        print(f"[✗] Failed to disable auto-start: {e}")

# For manual test
if __name__ == "__main__":
    enable_auto_start()
    # disable_auto_start()  # Uncomment to remove
