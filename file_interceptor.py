import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from datetime import datetime

class FileArchiver:
    def __init__(self, backup_directory):
        self.backup_directory = backup_directory

    def archive(self, file_path):
        """ Archive the deleted file by moving it to the backup directory. """
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)
        
        # Check if the file exists before attempting to move it
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}. Skipping archiving.")
            return

        # Create a timestamp for unique naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.basename(file_path)
        backup_path = os.path.join(self.backup_directory, f"{timestamp}_{file_name}")
        
        try:
            shutil.move(file_path, backup_path)
            print(f"File archived: {backup_path}")
        except Exception as e:
            print(f"Error archiving file {file_path}: {e}")

class FileInterceptor(FileSystemEventHandler):
    def __init__(self, watch_directory):
        self.watch_directory = watch_directory

    def on_deleted(self, event):
        """ Handle the event when a file is deleted. """
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            # Archive the deleted file before it's fully removed
            archiver = FileArchiver("ghostguard/backups/")
            archiver.archive(event.src_path)

    def watch(self):
        """ Watch the directory for file changes and handle events. """
        event_handler = self
        observer = Observer()
        observer.schedule(event_handler, self.watch_directory, recursive=True)  # Set to True to monitor subdirectories as well
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

# Example usage
if __name__ == "__main__":
    # Monitor the entire C: drive (all files and folders)
    watch_directory = "C:\\"  # This will monitor the entire C: drive
    
    # Ensure the watch directory exists
    if not os.path.exists(watch_directory):
        print(f"Error: The directory '{watch_directory}' does not exist.")
    else:
        interceptor = FileInterceptor(watch_directory)
        print(f"Starting to monitor {watch_directory} for file deletions...")
        interceptor.watch()
