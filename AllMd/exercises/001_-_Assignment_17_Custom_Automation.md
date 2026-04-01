# Comprehensive Documentation: Six Python Automation Projects

This document provides an in-depth look at six different automation projects built with Python. Each project is documented with its purpose, requirements, folder structure, environment configuration, key algorithms, data flow, and a set of 10 interview questions to test understanding and provoke discussion. The projects range from email automation to network monitoring, file organization, job automation, WhatsApp messaging, and system health monitoring.

---

## Table of Contents

1. [Project 1: Raise Request Email Automation](#project-1-raise-request-email-automation)
2. [Project 2: Wi-Fi Device Monitor with Web Dashboard](#project-2-wi-fi-device-monitor-with-web-dashboard)
3. [Project 3: Downloads Folder Organizer](#project-3-downloads-folder-organizer)
4. [Project 4: Job Automation Web Dashboard](#project-4-job-automation-web-dashboard)
5. [Project 5: WhatsApp Scheduler](#project-5-whatsapp-scheduler)
6. [Project 6: System Health Monitor – Terminal UI](#project-6-system-health-monitor--terminal-ui)

---

## Project 1: Raise Request Email Automation

### Overview
This project automates sending a quarterly raise request email to a boss. It uses Python to send a professionally formatted HTML email every 90 days. The script reads configuration from environment variables for security, loads an HTML template, and schedules itself to run continuously. A test email is sent on startup to verify everything works.

### Requirements & Installation
- **Python** 3.7+
- **Dependencies**: `schedule`, `python-dotenv`
- Install with: `pip install schedule python-dotenv`

### Folder Structure
```
raise_email_automation/
│
├── main.py              # Main automation script
├── config.py            # Configuration and environment variable loader
├── email_template.txt   # HTML email template with placeholders
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── scheduler.log        # Log file (created automatically)
└── README.md            # (optional) Project documentation
```

### Environment Variables (`.env`)
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=boss.email@company.com
YOUR_EMAIL=your.email@gmail.com
YOUR_NAME=Your Full Name
BOSS_NAME=Dr. Smith
```

### Imports & Libraries
- `smtplib` – for sending emails via SMTP.
- `logging` – to record events to a file.
- `schedule` – for periodic job scheduling.
- `datetime` – to get current date/time.
- `email.mime` – to construct multipart emails.
- `dotenv` – to load environment variables.

### Configuration (`config.py`)
Loads environment variables and sets defaults. Also defines `LOG_FILE`, `TEMPLATE_FILE`, `RAISE_INTERVAL_DAYS=90`, and `SEND_TEST_ON_START=True`.

### Email Template (`email_template.txt`)
Contains HTML with placeholders: `{name}`, `{boss_name}`, `{current_date}`, `{current_year}`, `{email}`. The first line must start with `Subject:` to define the email subject.

### Function Algorithms & Flow

#### `load_template(name, boss_name, current_date, current_year, email)`
- Reads `email_template.txt`.
- Replaces all placeholders with provided values.
- Returns the template string.

#### `send_email(recipient, subject_prefix="", is_test=False)`
1. Get current date, year, name, boss name, email from config.
2. Load template with `load_template()`.
3. Extract subject from template (first line after `Subject:`). Remove that line from HTML.
4. Apply `subject_prefix` if given.
5. Create `MIMEMultipart` message with plain text fallback.
6. Connect to SMTP server using credentials from environment.
7. Send email and log success/failure.

#### `job()`
Wrapper that calls `send_email(config.RECIPIENT_EMAIL, is_test=False)`.

#### `main()`
- If `SEND_TEST_ON_START` is True, sends a test email to `YOUR_EMAIL` with prefix `[TEST]`.
- Schedules `job` to run every `RAISE_INTERVAL_DAYS` days.
- Enters infinite loop checking for scheduled jobs every minute.

### Data Flow
1. Environment variables → `config.py` → used by `send_email`.
2. Template file → read → placeholders replaced with config values.
3. Email content → SMTP server → recipient inbox.
4. Logs → `scheduler.log`.

### Running the Script
```bash
python main.py
```
The script will send a test email and then wait 90 days to send the real one. Keep it running continuously (use process manager or cron).

### 10 Interview Questions
1. Why is it important to use environment variables for sensitive data like email credentials?
2. How would you modify the script to send emails to multiple recipients?
3. Explain the purpose of `MIMEMultipart('alternative')` and why we include both plain text and HTML.
4. How does the `schedule` library work? What happens if the scheduled time passes while the script is not running?
5. What improvements would you make to handle email sending failures (e.g., retries, logging)?
6. How would you test this script without actually sending an email every 90 days?
7. Explain the logic for extracting the subject from the template. Why is that approach used?
8. What are the security implications of storing the email password in plain text in the `.env` file? How can you mitigate this?
9. How could you extend this project to include attachments (e.g., a performance review document)?
10. What would you change to make the scheduling more robust, for example using `APScheduler` instead of `schedule`?

---

## Project 2: Wi-Fi Device Monitor with Web Dashboard

### Overview
A real‑time network scanning tool that continuously monitors a local network and displays all connected devices through a web dashboard with a hacker/terminal theme. It detects devices as they connect/disconnect, shows MAC address, IP, vendor, hostname, and updates in real‑time without page refreshes.

### Requirements & Installation
- **Python** 3.7+
- **Dependencies**: `flask`, `scapy`, `python-dotenv`
- **Administrator/Root privileges** required for ARP scanning.
- Install with: `pip install flask scapy python-dotenv`

### Folder Structure
```
smart_lights_automation/
│
├── app.py                 # Flask web application
├── scanner.py             # Network scanning module
├── config.py              # Configuration (loads .env)
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── README.md
├── templates/
│   └── index.html         # Main dashboard page
└── static/
    ├── style.css          # Hacker theme CSS
    └── script.js          # Frontend JavaScript
```

### Environment Variables (`.env`)
```
NETWORK_RANGE=192.168.1.0/24
SCAN_INTERVAL=5
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

### Imports & Libraries
- **Flask** – web framework.
- **scapy** – for ARP scanning (`ARP`, `Ether`, `srp`).
- **dotenv** – load environment variables.
- **threading** – background scanning thread.
- **socket** – for hostname resolution.
- **datetime** – timestamps.

### Key Components

#### `config.py`
Loads environment variables into Python constants.

#### `scanner.py`
- **DeviceInfo class**: Represents a single device with attributes: `mac`, `ip`, `first_seen`, `last_seen`, `hostname`, `vendor`, `status`, `connection_count`, `ip_history`.
  - `_get_hostname(ip)`: performs reverse DNS lookup.
  - `_get_vendor(mac)`: looks up manufacturer from MAC prefix dictionary.
  - `update(ip)`: refreshes last_seen, increments count, records IP changes.
- **NetworkScanner class**:
  - `__init__()`: initializes devices dict, lock, scan count.
  - `scan_network()`: builds ARP request, sends via `srp()`, returns dict {mac: ip}.
  - `update_devices()`: marks all as disconnected, then updates responding ones; adds new devices.
  - `get_stats()`: returns counts of total/connected/disconnected devices and last scan time.
  - `start_scanning()`: launches background thread that runs `update_devices()` every `SCAN_INTERVAL` seconds.

#### `app.py`
- Creates Flask app, initializes `NetworkScanner`, starts scanning.
- Routes:
  - `/` – serves `index.html`.
  - `/api/devices` – returns JSON of all devices and stats.
  - `/api/connected` – returns only connected devices.
  - `/api/stats` – returns stats only.
- Uses threading lock when accessing shared devices dict.

#### `templates/index.html`
- Skeleton with stats cards, filter buttons, and a `<div id="device-grid">`.

#### `static/style.css`
- Dark background, green text, monospace font, terminal‑like effects (scan lines, brackets, blinking cursor).

#### `static/script.js`
- `fetchStats()`: polls `/api/devices` every 2 seconds.
- `renderDashboard(data)`: updates stats and dynamically creates device cards.
- Filter buttons update `currentFilter` and re‑render.
- Countdown timestamps? (Not in this project; but device cards show last seen.)

### Function Algorithms & Flow
1. **NetworkScanner.scan_network()**:
   - Create `ARP(pdst=NETWORK_RANGE)`.
   - Create `Ether(dst="ff:ff:ff:ff:ff:ff")`.
   - Combine: `packet = ether/arp`.
   - `srp(packet, timeout=3, verbose=0)` sends and receives.
   - For each answered packet, extract `hwsrc` (MAC) and `psrc` (IP).
2. **NetworkScanner.update_devices()**:
   - Acquire lock.
   - Mark all devices as disconnected.
   - For each discovered (MAC, IP), update or create DeviceInfo, mark as connected.
   - Release lock.
3. **Background thread** loops: call `update_devices()`, sleep `SCAN_INTERVAL`.
4. **API endpoints** access the shared devices dict with lock, convert to list of dicts, return JSON.
5. **Frontend** polls API, rebuilds HTML with current data.

### Data Flow
1. ARP request broadcast → device responses → `scanner.py` updates internal dictionary.
2. Flask API serves dictionary as JSON.
3. JavaScript fetches JSON, updates DOM.

### Running the Application
```bash
sudo python app.py   # Linux/macOS
# or as Administrator on Windows
```
Open browser to `http://localhost:5000`.

### 10 Interview Questions
1. Why is administrator/root privilege required for ARP scanning?
2. Explain how ARP scanning works. What is the role of the broadcast MAC address?
3. How does the application handle thread safety when accessing the devices dictionary?
4. What are the limitations of using `scapy` for network scanning on different operating systems?
5. How would you improve vendor detection beyond a hardcoded dictionary?
6. Describe the algorithm for detecting when a device disconnects.
7. What potential security risks exist in exposing device information via a web dashboard?
8. How could you extend the project to send notifications when a new unknown device joins the network?
9. Why is the hostname resolution performed in the `DeviceInfo` constructor rather than during scanning?
10. What changes would be needed to scan multiple subnets or VLANs?

---

## Project 3: Downloads Folder Organizer

### Overview
A desktop application with a Tkinter GUI that automatically sorts files in a chosen folder into subfolders based on file extensions. It offers one‑time sort and real‑time monitoring (using `watchdog`). Configuration (extension‑to‑folder mapping) is stored in `config.json`.

### Requirements & Installation
- **Python** 3.6+ (Tkinter included).
- **Dependencies**: `watchdog`
- Install with: `pip install watchdog`

### Folder Structure
```
folder_organizer/
│
├── main.py               # Core logic: file operations, monitoring
├── ui.py                 # Tkinter GUI
├── config.json           # Extension to folder mapping
├── requirements.txt
└── README.md
```
After running, a log file `folder_organizer.log` appears in the home directory.

### Configuration (`config.json`)
```json
{
    "Images": [".jpg", ".jpeg", ".png", ...],
    "Documents": [".pdf", ".docx", ...],
    "Others": []
}
```

### Imports & Libraries
- **os, shutil, json, time, pathlib** – file operations, JSON parsing.
- **logging** – logging to file and console.
- **watchdog.observers.Observer** – directory monitoring.
- **watchdog.events.FileSystemEventHandler** – event handling.
- **tkinter** – GUI.
- **threading, queue** – for background tasks and thread‑safe logging.

### Core Functions in `main.py`

#### `load_config(config_path='config.json')`
- Reads JSON, returns dict. Falls back to default mapping if file missing/invalid.

#### `build_extension_map(category_map)`
- Converts `{folder: [extensions]}` to `{extension: folder}`.

#### `ensure_folder(folder_path)`
- Creates folder if it doesn’t exist.

#### `is_file_stable(file_path, wait_seconds=60)`
- Returns True if file’s last modification time is older than `wait_seconds`.

#### `get_unique_filename(destination_folder, filename)`
- If file exists, appends `_1`, `_2`, etc., until unique.

#### `organize_file(file_path, ext_map, root_folder, skip_stability_check=False)`
- Skips if file is already in a category subfolder.
- Optionally checks stability.
- Determines target folder using extension map.
- Ensures target folder exists.
- Generates unique filename.
- Moves file with `shutil.move()`.
- Returns (success, destination).

#### `organize_folder(folder_path, category_map, skip_stability_check=False)`
- Iterates over files in folder (non‑recursive).
- Calls `organize_file` for each.
- Returns count of moved files.

#### `FolderMonitor` class
- Wraps watchdog `Observer`.
- `start()`: creates `Handler`, schedules it, starts observer.
- `stop()`: stops observer.
- `is_active()`: checks if observer is alive.

#### `Handler` class (inherits from `FileSystemEventHandler`)
- Overrides `on_created` and `on_modified`.
- In `_handle_event`: ignores directories; skips if file already in category folder; waits 1 second; calls `organize_file` with stability check.
- Calls a callback (if provided) for UI logging.

### UI (`ui.py`)

#### `App` class
- **Attributes**: `folder_path` (StringVar), `monitor_active`, `monitor`, `log_queue`, `config`.
- **create_widgets()**: builds UI: folder selection, Sort Now button, Start/Stop Monitoring button, log text area, status bar.
- **browse_folder()**: opens directory dialog.
- **log_message(msg)**: puts message into queue.
- **poll_log_queue()**: called every 100ms via `after()`; drains queue and inserts into log widget.
- **sort_now()**: validates folder, starts background thread running `_run_sort`.
- **_run_sort(folder)**: calls `organize_folder` with `skip_stability_check=True`, logs result.
- **toggle_monitor()**: starts/stops monitoring. If starting, performs initial sort, creates `FolderMonitor` with callback, starts it.
- **on_closing()**: stops monitor if active, destroys window.

### Function Flow
- **Sort Now**: background thread → `organize_folder` → `organize_file` for each file.
- **Start Monitoring**: initial sort, then background observer thread triggers `Handler` on file events → `organize_file` with stability check.
- **Logging**: background threads call `log_message` → queue → main thread displays.

### Data Flow
1. User selects folder.
2. `config.json` → loaded into `category_map`.
3. File paths read from disk → moved to subfolders.
4. Log messages → queue → UI.

### Running the Application
```bash
python ui.py
```

### 10 Interview Questions
1. Why is the stability check (`is_file_stable`) important, especially for files being downloaded?
2. How does the application prevent moving files that are already inside a category folder? Why is this necessary?
3. Explain the purpose of `get_unique_filename` and how it works.
4. What threading issues are addressed by using a queue for log messages?
5. How would you modify the program to sort files recursively (including subfolders)?
6. What happens if a file is being written to while the script tries to move it? How does the script handle such errors?
7. Why is `watchdog` used instead of repeatedly scanning the folder with `os.listdir`?
8. How could you extend the project to support custom rules (e.g., move files based on date or size)?
9. What are the limitations of the current vendor detection? How could it be improved?
10. Describe a scenario where a file might be moved multiple times and how to avoid that.

---

## Project 4: Job Automation Web Dashboard

### Overview
A Flask‑based web dashboard designed to automate repetitive work tasks. It provides a UI to manage input data (CSV), trigger automation cycles (which can include web form filling via Selenium and report generation), and view generated reports. It includes a background scheduler for periodic runs. The project is a template that can be customized for specific job requirements (e.g., filling timesheets, submitting orders).

### Requirements & Installation
- **Python** 3.8+
- **Dependencies**: `Flask`, `pandas`, `selenium`, `pyyaml`, `python-dotenv`
- Install with: `pip install -r requirements.txt`
- Chrome browser and ChromeDriver required for Selenium.

### Folder Structure
```
job-automation-dashboard/
│
├── .env                       # Environment variables
├── .env.example                # Example env file
├── app/                        # Main package
│   ├── __init__.py             # App factory
│   ├── config.py               # Loads config.yaml and env
│   ├── models/                 # Data handling
│   │   ├── __init__.py
│   │   ├── data_manager.py     # CRUD on input CSV
│   │   └── report_manager.py   # Read/write report CSV
│   ├── routes/                 # Blueprints
│   │   ├── __init__.py
│   │   ├── main.py             # Dashboard home
│   │   ├── data.py             # Data management pages
│   │   ├── reports.py          # View and send reports
│   │   └── automation.py       # Control automation
│   ├── services/                # Core automation
│   │   ├── __init__.py
│   │   ├── automation_engine.py # Web automation + report
│   │   └── scheduler.py         # Background scheduler
│   ├── static/                  # CSS, JS
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/               # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── data_list.html
│       ├── data_add.html
│       ├── data_edit.html
│       ├── data_upload.html
│       ├── reports.html
│       └── automation.html
├── config.yaml                  # Non‑sensitive config
├── data/                        # Data directory
│   ├── input_data/              # Input CSV files
│   │   └── data.csv
│   └── output_reports/           # Generated reports
│       └── report.csv
├── requirements.txt
├── run.py                        # Entry point
└── sample.gif
```

### Environment Variables (`.env`)
```
SECRET_KEY=your-secret-key
FLASK_DEBUG=True
WEB_USERNAME=your_web_username
WEB_PASSWORD=your_web_password
EMAIL_SENDER=sender@example.com
EMAIL_PASSWORD=your_email_password
```

### Configuration (`config.yaml`)
```yaml
web:
  enabled: false
  login_url: "https://example.com/login"
  username_field: "username"
  password_field: "password"
  login_button: "login-btn"
  submit_button: "submit-btn"

form_mapping:
  Name: "fullname_field"
  Email: "email_field"
  Department: "dept_field"
  Score: "score_field"

email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  subject: "Automation Report"
  body: "Please find attached the latest report."
```

### Imports & Libraries
- **Flask** – web framework.
- **pandas** – data manipulation (CSV).
- **selenium** – browser automation.
- **pyyaml** – parse YAML config.
- **python-dotenv** – load `.env`.
- **smtplib, email** – send emails.
- **threading, time** – scheduler background thread.
- **logging** – error logging.

### Key Components

#### `app/__init__.py` (App Factory)
- Creates Flask app.
- Loads config from `config.py`.
- Registers blueprints with URL prefixes.
- Initializes logging.

#### `app/config.py`
- Loads `.env` via `load_dotenv()`.
- Reads `config.yaml` into `automation_config`.
- Defines `Config` class with `SECRET_KEY`, `DEBUG`, and paths.
- Creates data directories if missing.

#### `models/data_manager.py`
- `read_data()`: reads `input_data/data.csv`, returns DataFrame. If file missing/empty, creates default DataFrame with columns.
- `write_data(df)`: saves DataFrame to CSV.
- `add_row(row_dict)`: appends a row.
- `update_row(index, row_dict)`: updates row.
- `delete_row(index)`: deletes row.
- `append_data(new_df)`: concatenates DataFrames (union of columns).

#### `models/report_manager.py`
- Similar but for `output_reports/report.csv`.
- `read_report()` returns DataFrame; handles empty/missing.
- `write_report(df)` saves CSV including index.

#### Routes (Blueprints)

- **`main_bp`** (`/`): dashboard home – shows counts and links.
- **`data_bp`** (`/data`): list, add, edit, delete, upload, clear.
- **`reports_bp`** (`/reports`): view report, send via email.
- **`automation_bp`** (`/automation`): status, start/stop scheduler, run once.

#### `services/automation_engine.py`
- `setup_driver(headless=True)`: creates Chrome WebDriver.
- `login_to_web_app(driver, config)`: navigates to login URL, waits for fields, enters credentials, clicks login.
- `fill_form(driver, row, config)`: for each column in `form_mapping`, finds element by ID, clears, sends value, then clicks submit.
- `run_automation_once()`:
  - Reads input data via `data_manager.read_data()`.
  - If web enabled: sets up driver, logs in, iterates over rows calling `fill_form`, quits driver.
  - Generates report using `df.describe()` and writes via `report_manager.write_report()`.
  - Logs completion.

#### `services/scheduler.py`
- `AutomationScheduler` class:
  - `__init__(interval_seconds)`: default 60.
  - `start()`: starts background thread running `_run_loop`.
  - `stop()`: signals stop and joins thread.
  - `_run_loop()`: while running, calls `run_automation_once()`, then sleeps `interval`, checking stop flag every second.
- Global instance `scheduler` created with default interval.

#### Templates
- `base.html`: navbar, container, flash messages.
- `index.html`: dashboard cards.
- `data_list.html`: table with Edit/Delete, buttons.
- `data_add.html`, `data_edit.html`: forms.
- `data_upload.html`: file upload or paste CSV.
- `reports.html`: statistics table, email form.
- `automation.html`: status and control buttons (AJAX).

#### Static Files
- `style.css`: dark theme, responsive cards.
- `main.js`: currently empty (can be extended).

### Function/Workflow
- **Data Management**: User adds/edits/deletes rows; changes saved to CSV via `data_manager`.
- **Upload CSV**: Reads uploaded file/pasted text → pandas DataFrame → appended or replaced.
- **Run Once**: Triggers `run_automation_once()` in background thread.
- **Start Scheduler**: Calls `scheduler.start()` – background thread runs automation periodically.
- **Send Report**: Reads report CSV, attaches to email, sends via SMTP.

### Data Flow
1. Input CSV (`data.csv`) ↔ `data_manager` (CRUD).
2. Automation reads input data → performs web actions (if enabled) → generates report → writes `report.csv`.
3. Reports page reads `report.csv` → displays table.
4. Email sends `report.csv` as attachment.

### Running the Application
```bash
python run.py
```
Open browser to `http://localhost:5000`.

### Customization Notes
- Modify `form_mapping` in `config.yaml` to match target web form.
- Adjust `fill_form()` in `automation_engine.py` for complex interactions (dropdowns, file uploads).
- Change scheduler interval in `scheduler.py` or make it configurable.

### 10 Interview Questions
1. Explain the purpose of using an application factory pattern in Flask.
2. How does the `data_manager` ensure that the input CSV always has a consistent structure?
3. What are the advantages of separating configuration into `.env` (sensitive) and `config.yaml` (non‑sensitive)?
4. Describe how the scheduler runs automation in the background without blocking Flask.
5. What improvements would you make to handle errors during Selenium automation (e.g., element not found)?
6. How could you extend the report generation to include visual charts or PDFs?
7. Why is it important to use `WebDriverWait` in Selenium instead of `time.sleep`?
8. What security considerations should be taken when storing email credentials in `.env`?
9. How would you modify the project to support multiple different automation tasks (e.g., different websites)?
10. Explain the data flow when a user uploads a CSV file and chooses to append.

---

## Project 5: WhatsApp Scheduler

### Overview
A Flask application that allows users to schedule WhatsApp messages to be sent at specific times or intervals. It uses `pywhatkit` (which automates WhatsApp Web) to send messages. The web interface supports creating, editing, viewing, and deleting scheduled messages. A background thread continuously checks for due messages and sends them.

### Requirements & Installation
- **Python** 3.7+
- **Dependencies**: `Flask`, `Flask-WTF`, `Flask-SQLAlchemy`, `pywhatkit`, `python-dotenv`
- Install with: `pip install -r requirements.txt`
- Google Chrome must be installed (for pywhatkit).

### Folder Structure
```
whatsapp-scheduler/
│
├── .env                       # Environment variables
├── app/                        # Main package
│   ├── __init__.py             # App factory, DB init
│   ├── forms.py                # WTForms for scheduling
│   ├── models.py               # SQLAlchemy models
│   ├── routes.py               # Blueprint with all routes
│   ├── scheduler.py            # Background scheduler thread
│   ├── static/                 # CSS, JS
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js         # Countdown, formatting
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html
│   │   ├── edit.html
│   │   └── index.html
│   └── utils.py                # WhatsApp sending function
├── config.py                   # Configuration class
├── instance/                   # Contains app.db (SQLite)
├── PyWhatKit_DB.txt            # pywhatkit log
├── requirements.txt
└── run.py                      # Entry point
```

### Environment Variables (`.env`)
```
SECRET_KEY=your-secret-key
# Optional: DATABASE_URL for non-SQLite
```

### Configuration (`config.py`)
- Loads `SECRET_KEY` from environment (required).
- Sets `SQLALCHEMY_DATABASE_URI` (default SQLite in `instance/`).
- `WHATSAPP_WAIT_TIME = 5` – seconds pywhatkit waits after opening WhatsApp Web.

### Database Models (`models.py`)
```python
class ScheduledMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    schedule_type = db.Column(db.String(10), nullable=False)  # 'once', 'daily', 'interval'
    time_of_day = db.Column(db.String(5), nullable=True)      # for once/daily
    interval_seconds = db.Column(db.Integer, nullable=True)   # for interval
    next_run = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Forms (`forms.py`)
- `MessageForm` with fields:
  - `to_number` (required, regex `^\+\d{1,15}$`)
  - `message` (required)
  - `schedule_type` (radio: once/daily/interval)
  - `time` (optional, regex HH:MM)
  - `interval_seconds` (optional, integer min=5 max=7200)
- Validation ensures `time` is provided for once/daily, and `interval_seconds` for interval.

### Routes (`routes.py`)

- **`/`** (GET, POST): Display form and list of messages. On POST, create new message (calculate next_run), save to DB, redirect.
- **`/send_now`** (POST): Validates form, calls `send_whatsapp_message` immediately (does not save to DB).
- **`/edit/<int:msg_id>`** (GET, POST): Pre‑fill form, update message, recalculate next_run.
- **`/delete/<int:msg_id>`** (GET): Delete message.
- **`/deactivate/<int:msg_id>`** (GET): Toggle `active` flag.

### Scheduler Thread (`scheduler.py`)
- Global `scheduler_thread` and `stop_scheduler` flag.
- `start_scheduler(app)`: starts daemon thread running `schedule_loop`.
- `schedule_loop(app)`: with app context, loops every 2 seconds:
  - Queries for active messages where `next_run <= now`.
  - For each, calls `send_whatsapp_message`.
  - Updates `next_run` based on schedule type (once → deactivate, daily → add 1 day, interval → add interval).
  - Commits changes; rolls back on error.
- `stop_scheduler_thread()`: sets flag to stop.

### Utility Functions (`utils.py`)
- `send_whatapp_message(phone, message)`:
  - Uses `pywhatkit.sendwhatmsg_instantly(phone_no, message, wait_time, tab_close=True)`.
  - Returns (success, result) tuple.
  - Logs success/failure.

### Templates & Static Files
- `base.html`: navbar, flash messages.
- `index.html`: form with formatting toolbar, schedule type toggles, list of messages with countdown timers.
- `edit.html`: similar to index form but pre‑filled.
- `main.js`: 
  - Dynamic show/hide of time/interval fields.
  - Text formatting buttons (wrap selected with *, _, ~, ```).
  - Countdown update every second using JavaScript.
- `style.css`: dark theme with green accents.

### Function/Workflow
1. User fills form → POST to `/` → new `ScheduledMessage` saved with `next_run` (UTC).
2. Background thread wakes every 2s → fetches due messages.
3. For each due message, calls `send_whatsapp_message`.
4. On success/failure, updates DB accordingly.
5. Frontend countdown shows remaining time until next run.

### Data Flow
- Form data → SQLite database.
- Scheduler reads DB → calls pywhatkit → updates DB.
- List page reads DB → displays with countdown.

### Running the Application
```bash
python run.py
```
Open `http://localhost:5000`. Ensure you are logged into WhatsApp Web in Chrome (first manual login required).

### Important Notes
- Times are stored in UTC; countdown uses browser's local time.
- Scheduler accuracy is ±2 seconds.
- pywhatkit opens Chrome each time; ensure computer doesn't sleep.

### 10 Interview Questions
1. Explain how the scheduler determines when a message is due and how it updates `next_run` after sending.
2. Why is it important to use `with app.app_context()` inside the scheduler thread?
3. What are the potential issues with using `pywhatkit` for sending messages? How would you mitigate them?
4. How does the form validation ensure that the correct fields are provided based on schedule type?
5. Describe the algorithm for calculating `next_run` for a daily message when the specified time has already passed today.
6. How does the JavaScript countdown work? What happens if the user's system clock is different from the server time?
7. What would you change to allow editing a message without losing its schedule history?
8. How could you implement a retry mechanism for failed sends?
9. Why is the scheduler implemented as a daemon thread? What are the implications?
10. What security measures would you add if deploying this application publicly?

---

## Project 6: System Health Monitor – Terminal UI

### Overview
A real‑time system monitoring dashboard with a retro terminal aesthetic. Built with Flask for the backend (using `psutil` to collect system metrics) and JavaScript (Chart.js, jQuery) for the frontend. The dashboard displays CPU, memory, disk, network, sensors, processes, and system information, updating every 2 seconds.

### Requirements & Installation
- **Python** 3.7+
- **Dependencies**: `Flask`, `Flask-CORS`, `psutil`
- Install with: `pip install -r requirements.txt`

### Folder Structure
```
system-health-monitor/
│
├── app.py                     # Main Flask app
├── requirements.txt           # Dependencies
├── static/
│   ├── script.js              # Frontend JavaScript
│   └── style.css              # Terminal-themed CSS
└── templates/
    └── index.html             # Single HTML page
```

### Imports & Libraries
- **Flask, Flask-CORS** – web server and CORS.
- **psutil** – cross‑platform system information.
- **platform** – OS details.
- **time** – uptime calculation.
- **jQuery** and **Chart.js** – loaded from CDN in HTML.

### Backend (`app.py`)

#### Helper: `get_size(bytes)`
- Converts bytes to human‑readable string (B, KB, MB, GB, TB).

#### CPU Info: `get_cpu_info()`
- `psutil.cpu_percent(interval=0.5)` – overall CPU usage.
- `psutil.cpu_percent(percpu=True)` – per‑core percentages.
- `psutil.cpu_count()` – logical cores.
- `psutil.cpu_count(logical=False)` – physical cores.
- `psutil.cpu_freq()` – current frequency.
- `psutil.getloadavg()` – load average (1,5,15 min) – converted to percentage of total cores.
- Returns dict.

#### Memory Info: `get_memory_info()`
- `psutil.virtual_memory()` – total, available, percent, used, free, etc.
- `psutil.swap_memory()` – swap stats (try/except).
- Returns dict with 'virtual' and 'swap' keys.

#### Disk Info: `get_disk_info()`
- `psutil.disk_partitions()` – list of partitions.
- For each, attempt `psutil.disk_usage(mountpoint)`. If permission denied, skip.
- `psutil.disk_io_counters()` – I/O stats (read/write bytes, time, etc.) if available.
- Returns dict with 'partitions' and 'io'.

#### Network Info: `get_network_info()`
- `psutil.net_if_addrs()` – interface addresses.
- `psutil.net_io_counters()` – bytes sent/received, packets, errors.
- `psutil.net_connections()` – number of active connections (may require root; returns -1 on error).
- Returns dict.

#### Sensors Info: `get_sensors_info()`
- `psutil.sensors_temperatures()` – hardware temperatures.
- `psutil.sensors_fans()` – fan speeds.
- `psutil.sensors_battery()` – battery status.
- Returns dict with keys 'temperatures', 'fans', 'battery' if data exists.

#### Processes Info: `get_processes_info()`
- Iterate over processes with `psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])`.
- Filter out None values.
- Sort to get top 5 CPU and top 5 memory consumers.
- Returns dict with 'cpu_top' and 'mem_top'.

#### System Info: `get_system_info()`
- `platform.node()`, `platform.system()`, `platform.release()`, `platform.version()`, `platform.machine()`, `platform.processor()`.
- `psutil.boot_time()` – boot time as timestamp, formatted.
- `psutil.users()` – list of logged‑in users.

#### Flask Routes
- `@app.route('/')` – serves `index.html`.
- `@app.route('/api/stats')` – calls all above functions and returns JSON.

### Frontend (`static/script.js`)

#### Global `charts` Object
- Stores Chart.js instances keyed by canvas ID.

#### `createOrUpdateChart(ctx, type, data, options)`
- If chart exists for ctx, update its data and call `update()`. Else create new Chart.

#### `renderDashboard(data)`
- Builds HTML string with cards for each section.
- Inserts HTML into `#dashboard`.
- For CPU per‑core chart, gets canvas context and calls `createOrUpdateChart` with bar chart data.
- Updates stats text, progress bars, tables.

#### `fetchStats()`
- Uses `$.getJSON` to call `/api/stats` and passes response to `renderDashboard`.

#### Polling
- On document ready, call `fetchStats()` and set `setInterval(fetchStats, 2000)`.

### Styling (`static/style.css`)
- Black background, green text, monospace.
- Cards with borders, progress bars, grid layout.

### HTML Template (`templates/index.html`)
- Includes Chart.js and jQuery from CDN.
- Links local CSS/JS.
- `<div id="dashboard">` placeholder.

### Function Algorithms & Flow
1. **Backend**: Each API call gathers fresh data via `psutil` functions.
2. **Frontend**: Polls every 2s, re‑renders entire dashboard.
3. **Chart updates**: Only the CPU per‑core chart is updated in‑place; other stats are recreated as HTML.

### Data Flow
- `psutil` → Python dictionaries → JSON → JavaScript → DOM.

### Error Handling
- Each data‑gathering function is wrapped in try/except to return empty/default values on error.
- Disk partitions that cannot be accessed are skipped.
- Network connections may raise `AccessDenied`; returns -1.

### Running the Application
```bash
python app.py
```
Open browser to `http://localhost:5000`.

### 10 Interview Questions
1. Why is `psutil.cpu_percent(interval=0.5)` used instead of a non‑blocking call?
2. How does the application handle cases where certain metrics are not available on the OS (e.g., swap on some systems)?
3. Explain the algorithm for converting load average to a percentage.
4. What are the tradeoffs of re‑rendering the entire dashboard every 2 seconds versus updating only changed elements?
5. How would you add historical data and graphs to show trends over time?
6. Why is `Flask-CORS` included even though the frontend and backend are served from the same origin?
7. Describe how `psutil.net_connections()` might require elevated privileges and how the code handles that.
8. How could you modify the frontend to allow users to choose which metrics to display?
9. What are the limitations of using `psutil` on different operating systems? Give examples.
10. How would you extend this project to send alerts when CPU usage exceeds a threshold?

---

*This comprehensive documentation provides a deep dive into six practical Python automation projects, covering everything from setup to advanced interview questions. Each project demonstrates different aspects of Python programming: email automation, network scanning, file organization, web automation, messaging, and system monitoring. Use this as a reference for learning, building, or preparing for technical interviews.*