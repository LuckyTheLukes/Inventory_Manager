import os
import logging
import configparser
import subprocess
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_task(force=False):
    # Load settings from settings.ini
    config = configparser.ConfigParser()
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.ini')
    config.read(settings_path)

    backup_dir = config.get('BackupSettings', 'BACKUP_DIR', fallback='./db_backup')
    time = config.get('BackupSettings', 'TIME', fallback='00:00')
    frequency = config.get('BackupSettings', 'FREQUENCY', fallback='DAILY').upper()
    task_name = config.get('BackupSettings', 'TASK_NAME', fallback='InventoryBackupTask')

    # Construct paths
    script_path = os.path.join(os.path.dirname(__file__), 'backup_script.py')

    # Check if the task already exists
    try:
        task_exists = subprocess.run(
            ["schtasks", "/Query", "/TN", task_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode == 0
    except subprocess.SubprocessError as e:
        logging.error(f"An error occurred while checking the task: {e}")
        task_exists = False

    # Delete the task if force is True and the task exists
    if force and task_exists:
        try:
            subprocess.run(["schtasks", "/Delete", "/TN", task_name, "/F"], check=True)
            logging.info(f"Task '{task_name}' deleted successfully.")
        except subprocess.SubprocessError as e:
            logging.error(f"An error occurred while deleting the task: {e}")
        task_exists = False

    # Create the task if it doesn't exist
    if not task_exists:
        command = f'"{sys.executable}" "{script_path}" "{backup_dir}"'
        try:
            subprocess.run([
            "schtasks", "/Create",
            "/SC", frequency,
            "/TN", task_name,
            "/TR", command,
            "/ST", time
            ], check=True)
            logging.info(f"Task '{task_name}' created successfully.")
        except subprocess.SubprocessError as e:
            logging.error(f"An error occurred while creating the task: {e}")
    else:
        logging.info(f"Task '{task_name}' already exists. Use --force to recreate it.")

if __name__ == "__main__":
    create_task(force=False)