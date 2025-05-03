import os
import shutil
from datetime import datetime
import configparser

# Read backup directory from settings.ini
config = configparser.ConfigParser()
config.read("settings.ini")
DEFAULT_BACKUP_DIR = config.get("BackupSettings", "BACKUP_DIR", fallback="./db_backup")
source_db_path = "./instance/workshop_inventory.sqlite3"

def backup_database(source_path=source_db_path, backup_dir=DEFAULT_BACKUP_DIR):
    """
    Backs up the database file to the specified backup directory.
    If a new backup directory is provided, it will be used instead of the default.

    :param source_path: Path to the source database file.
    :param backup_dir: Path to the backup directory (optional).
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file '{source_path}' does not exist.")

    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Generate a timestamped backup file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file_name = f"workshop_inventory_backup_{timestamp}.sqlite3"
    backup_path = os.path.join(backup_dir, backup_file_name)

    # Copy the database file to the backup directory
    shutil.copy2(source_path, backup_path)
    print(f"Backup created at: {backup_path}")

# Example usage
if __name__ == "__main__":
    # Call the function with the default backup directory
    try:
        backup_database()
    except Exception as e:
        print(f"Error: {e}")