import os
import shutil
from datetime import datetime

class FileArchiver:
    def __init__(self, backup_directory):
        """ Initialize with the backup directory where files will be stored. """
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
        
        # Move the file to the backup directory
        try:
            shutil.move(file_path, backup_path)
            print(f"File archived: {backup_path}")
        except Exception as e:
            print(f"Error archiving file {file_path}: {e}")
