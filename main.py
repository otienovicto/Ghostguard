import os
from persistence import Persistence
from file_interceptor import FileInterceptor
from cryptography.fernet import Fernet


def generate_key():
    # Define the path where the key should be saved
    key_path = 'ghostguard/ghostguard.key'

    # Ensure the 'ghostguard' directory exists
    if not os.path.exists('ghostguard'):
        os.makedirs('ghostguard')

    # Check if the key file already exists
    if not os.path.exists(key_path):
        # Generate a new key if the file doesn't exist
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        print(f"Key generated and saved to {key_path}")
    else:
        print(f"Key already exists at {key_path}")


def main():
    # Ensure the key is generated before starting the file monitoring
    generate_key()

    # Define the directory you want to monitor (monitor all directories)
    watch_directory = "C:\\"  # This will monitor the entire C: drive

    # Ensure the watch directory exists
    if not os.path.exists(watch_directory):
        print(f"Error: The directory '{watch_directory}' does not exist.")
        return

    # Initialize the file interceptor with the watch directory
    interceptor = FileInterceptor(watch_directory)
    
    # Start watching for file events
    print(f"Starting to monitor {watch_directory} for file deletions...")
    interceptor.watch()

    # Setup persistence to ensure app is always running
    persistence = Persistence()
    persistence.setup()
    persistence.monitor_self()


if __name__ == "__main__":
    main()
