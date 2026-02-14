## Step 2: Project Structure and File Descriptions

Understanding the project structure is fundamental to grasping how the application works. This step provides a detailed breakdown of every file and directory in the project, explaining their purpose, contents, and how they interact.

### Directory Layout

The project is organized as follows:

```
project_root/
│
├── .env                      # Environment configuration file (not shown in provided code, but used)
├── app.py                    # Main Flask application entry point
├── email_service.py          # Email handling logic encapsulated in a class
├── requirements.txt          # List of Python dependencies (implied)
└── templates/
    └── index.html            # Frontend HTML template with embedded CSS/JavaScript
```

**Key Points:**
- The root directory contains all Python files and the `.env` file.
- The `templates/` folder is standard in Flask for storing HTML templates.
- No static folder is present because CSS and JavaScript are embedded directly in the HTML (simplifies deployment for this small project).

### Detailed File Analysis

#### 1. `.env` – Environment Variables File

This file is not included in the code listing but is referenced in `app.py` via `python-dotenv`. It stores sensitive configuration data that should never be hard-coded. Example content:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=admin@example.com
```

**Why this matters:**
- Separates configuration from code.
- Keeps credentials out of version control (should be added to `.gitignore`).
- Allows different settings for development, testing, and production.

**Usage in code:**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables into os.environ

smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
smtp_port = int(os.getenv('SMTP_PORT', 587))
username = os.getenv('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD')
recipient = os.getenv('RECIPIENT_EMAIL')
```

The `os.getenv` function retrieves the value, with an optional default (e.g., `'smtp.gmail.com'`).

#### 2. `app.py` – Main Flask Application

This file is the heart of the backend. It creates the Flask app, defines routes, handles form submissions, and integrates the email service.

**Structure:**
- Imports necessary modules.
- Loads environment variables.
- Configures logging.
- Creates an instance of `EmailService` using credentials from `.env`.
- Defines two routes:
  - `@app.route('/')` – serves the HTML form.
  - `@app.route('/send-message', methods=['POST'])` – processes form data.

**Code highlights:**
```python
from flask import Flask, render_template, request, jsonify
from email_service import EmailService

app = Flask(__name__)

email_service = EmailService(
    smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    smtp_port=int(os.getenv('SMTP_PORT', 587)),
    username=os.getenv('EMAIL_ADDRESS'),
    password=os.getenv('EMAIL_PASSWORD'),
    recipient=os.getenv('RECIPIENT_EMAIL')
)

@app.route('/send-message', methods=['POST'])
def send_message():
    # Parse JSON or form data
    data = request.json if request.is_json else request.form
    # Extract, validate, and send email
    ...
    return jsonify({'success': True, 'message': msg})
```

**Interaction with other files:**
- Calls `render_template('index.html')` to display the form.
- Uses `EmailService` from `email_service.py` to send emails.
- Returns JSON responses that the frontend JavaScript consumes.

#### 3. `email_service.py` – Email Sending Logic

This file defines a class `EmailService` that encapsulates all SMTP operations. It is designed to be reusable and testable.

**Class definition:**
```python
class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password, recipient):
        # Store configuration

    def send_contact_email(self, name, email, phone, project_type, budget, message):
        # Construct and send email
        # Returns (bool, str)
```

**Key components:**
- **Constructor**: Initializes SMTP settings and recipient.
- **send_contact_email**: Builds a multipart email (plain text and HTML), connects to the SMTP server, sends the message, and handles errors.

**Why a separate class?**
- Separation of concerns: email logic is isolated from Flask route handling.
- Easier to unit test and modify.
- Can be extended later (e.g., to support attachments, different email templates).

**Code example of email construction:**
```python
msg = MIMEMultipart('alternative')
msg['From'] = self.username
msg['To'] = self.recipient
msg['Subject'] = f"New Contact Form: {project_type} from {name}"
msg['Reply-To'] = email

text_part = MIMEText(plain_text, 'plain')
html_part = MIMEText(html_content, 'html')
msg.attach(text_part)
msg.attach(html_part)
```

#### 4. `templates/index.html` – Frontend Form

Located in the `templates/` folder, this file contains the entire user interface. It includes:
- HTML5 structure.
- Bootstrap 5.3 CSS and JS for responsive design.
- Custom CSS for dark theme and styling.
- JavaScript using Fetch API to submit the form asynchronously.

**Structure within the file:**
- **Head**: Meta tags, Bootstrap CDN, Google Fonts, and custom styles.
- **Body**: A container with two columns:
  - Left panel: contact information (address, phone, email, hours, social links).
  - Right panel: the form with fields (name, email, project type, budget, message) and a submit button.
- **Script**: JavaScript that handles form submission, validation, AJAX call, and dynamic alerts.

**Why this matters:**
- The template is rendered by Flask when the user visits `/`.
- It communicates with the backend via the `/send-message` endpoint.
- The JavaScript makes the experience smooth (no page reloads).

**Key JavaScript snippet:**
```javascript
fetch('/send-message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        showAlert(data.message, 'success');
        form.reset();
    } else {
        showAlert(data.message, 'danger');
    }
})
```

#### 5. `requirements.txt` (Implied)

Although not provided in the code listing, a `requirements.txt` file is standard for Python projects. It lists all third-party packages needed to run the application. Based on the imports, the file would contain:

```
Flask
python-dotenv
email-validator
```

**Installation command:**
```bash
pip install -r requirements.txt
```

**Purpose:**
- Ensures anyone cloning the project can install the exact dependencies.
- Facilitates deployment and collaboration.

### How the Files Interact

1. **Startup**: When `app.py` runs, it imports `EmailService` and creates an instance using environment variables.
2. **User Request**: A user accesses `http://localhost:5000/`. Flask calls the `index()` function, which renders `index.html` using `render_template`.
3. **Form Submission**: User fills the form and clicks submit. JavaScript collects data and sends a POST request to `/send-message`.
4. **Backend Processing**: Flask's `send_message()` function receives the data, validates it, and calls `email_service.send_contact_email(...)`.
5. **Email Sending**: `EmailService` connects to SMTP, sends the email, and returns a status.
6. **Response**: Flask returns a JSON response, which the JavaScript uses to display a success or error message.
7. **Feedback**: The user sees an alert without leaving the page.

### Summary of Roles

- **.env**: Holds secrets.
- **app.py**: Orchestrates the web server and request handling.
- **email_service.py**: Handles the email delivery logic.
- **index.html**: Provides the user interface and client-side logic.
- **requirements.txt**: Manages dependencies.

This modular structure makes the project maintainable, scalable, and easy to understand for developers of all levels. Each file has a single responsibility, and the interactions are clearly defined through function calls and HTTP requests.