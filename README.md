![version](https://img.shields.io/badge/version-1.0.0-blue)
# AVL Inventory Manager

AVL Inventory Manager is a lightweight, user-friendly inventory management system designed for local workshops or small warehouses. It allows staff to track inventory items, log item retrievals, and maintain user histories. The system also supports exporting reports and includes automated backup features.

---

## Features

- **Inventory Management**

  - Add, edit, retrieve, and archive inventory items
  - Track quantities, models, serial numbers, stock thresholds, and more
  - Soft-delete support with restoration options

- **User Management**

  - Add and manage users who interact with inventory

- **History Tracking**

  - Logs all item edits, retrievals, and deletions with user attribution
  - Filterable and exportable activity history

- **Reporting**

  - Export inventory and history data to **PDF** or **CSV**
  - Filter and export only what you see (e.g., low stock items)

- **Low Stock Notifications**

  - Low stock items are automatically highlighted
  - A dedicated view is available for only low stock items

- **Backup System**

  - Auto-backup of database via Windows Task Scheduler
  - Configurable schedule and destination via settings page

- **Modern UI**

  - Bootstrap 5 styled, responsive design
  - DataTables for filtering, sorting, pagination, and exporting

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, DataTables, Jinja2
- **Database**: SQLite (with SQLAlchemy ORM)
- **PDF Generator**: WeasyPrint
- **Scheduler**: Windows Task Scheduler (via `schtasks`)

---

## Installation

### Requirements:

- Python 3.9+
- Windows OS (for auto-backup feature)
- GTK-for-Windows https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe

### Setup Steps:

1. Clone or copy this repository to your local machine.

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python run.py
```

4. Open `http://127.0.0.1:5000` in your browser.

---

## Settings and Auto-Backup

- Navigate to the **Settings** page to configure:

  - Backup destination folder
  - Frequency: DAILY / WEEKLY / MONTHLY
  - Time to run the backup

- A background script (`backup_setup.py`) will create a scheduled task.

---

## Notes

- This project is built for small teams and local environments.
- Tested primarily on Windows systems with local deployments.
- All data is stored in a local SQLite database file (instance/workshop_inventory.sqlite3).

---

---

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

---

## Credits

Made with ❤️ by Tharinda Lakshan PDWGA using Flask, Bootstrap, and passion for clean interfaces.

---
