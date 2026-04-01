## Download the Starting Project

### 1. Project Overview

The starting project provides a pre-built Flask application skeleton. It includes all the necessary HTML templates, a static file (a PDF cheat sheet), and an SQLite database with a `users` table. The application renders the pages correctly, but the authentication logic (registration, login, logout) is not yet implemented. Your task in the subsequent lessons will be to add that functionality.

The project is designed to focus your efforts purely on authentication, without the distraction of building the front-end or setting up the database from scratch.

### 2. Project Structure

After downloading and extracting the zip file, you will see the following directory structure:

```
project_folder/
│
├── main.py                 # The main Flask application
├── users.db                # SQLite database file (pre-created)
├── requirements.txt        # Python package dependencies
│
├── static/                 # Static files (CSS, files, etc.)
│   ├── css/                # CSS stylesheets
│   │   └── styles.css      # Custom styles for the project
│   └── files/              # Downloadable files
│       └── cheat_sheet.pdf # Secret PDF (only for logged-in users)
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base layout template (inherited by all pages)
│   ├── index.html          # Home page
│   ├── login.html          # Login form page
│   ├── register.html       # Registration form page
│   └── secrets.html        # Protected page (visible after login)
│
└── venv/                   # Virtual environment (created after setup)
```

#### Explanation of Key Files and Folders

- **main.py**: The entry point of the Flask application. It contains route definitions and basic configuration. Initially, it renders the templates but does not handle form submissions or authentication.

- **users.db**: An SQLite database file that already contains a `users` table. The table schema includes columns for `id` (primary key), `name`, `email`, and `password`. The database is initially empty.

- **requirements.txt**: Lists all Python packages required to run the project. These include Flask, Flask-Login, Werkzeug, and others.

- **static/**: Holds static assets. The `css/styles.css` file provides basic styling for the forms and pages. The `files/cheat_sheet.pdf` is the secret file that will be downloadable only after authentication.

- **templates/**: Contains HTML files using Jinja2 templating. 
  - `base.html` defines the common layout (navigation bar, footer, etc.) and includes blocks for page-specific content.
  - `index.html` extends `base.html` and displays a welcome message with buttons to login or register.
  - `login.html` contains a form with email and password fields.
  - `register.html` contains a form with name, email, and password fields.
  - `secrets.html` is the protected page that shows a greeting and a download button for the cheat sheet.

### 3. Setup Instructions

Follow these steps to set up the project on your local machine.

#### Step 1: Download and Extract
- Download the starting `.zip` file from the course resources.
- Extract the contents to a folder of your choice (e.g., `flask_auth_project`).

#### Step 2: Open in PyCharm
- Launch PyCharm.
- Click **File** → **Open** and select the extracted project folder.
- PyCharm may automatically detect the `requirements.txt` file and prompt you to create a virtual environment and install dependencies. If prompted, click **OK** or **Create Virtual Environment** and agree to install the requirements.

#### Step 3: Manual Virtual Environment Setup (if not prompted)
If PyCharm does not automatically prompt you, set up a virtual environment manually:

1. Go to **File** → **Settings** → **Project: [project name]** → **Python Interpreter**.
2. Click the gear icon ⚙️ and select **Add**.
3. Choose **New environment** and leave the default settings (the location should be inside your project folder, e.g., `./venv`). Ensure "Inherit global site-packages" is **unchecked**.
4. Click **OK**. PyCharm will create the virtual environment.

#### Step 4: Install Dependencies via Terminal
If the dependencies are not automatically installed, open the terminal in PyCharm (bottom left corner) and run:

- On **Windows**:
  ```bash
  python -m pip install -r requirements.txt
  ```
- On **macOS / Linux**:
  ```bash
  pip3 install -r requirements.txt
  ```

This will install Flask, Flask-Login, Werkzeug, and other required packages into the virtual environment.

#### Step 5: Verify Installation
After the installation completes, ensure there are no red underlines in `main.py`. If you still see import errors, double-check that the virtual environment is selected as the project interpreter (Settings → Project → Python Interpreter should point to the `venv` folder).

### 4. Database Inspection

The project includes a pre‑created SQLite database file `users.db`. It contains a single table named `users` with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

- `id` is an auto‑incrementing primary key.
- `name` stores the user’s full name (as entered during registration).
- `email` must be unique – no two users can share the same email address.
- `password` will eventually store the hashed password. In the starting state, it is empty because no users exist.

You can inspect the database using a tool like **DB Browser for SQLite** (recommended) or via Python's `sqlite3` module. Open `users.db` in DB Browser and view the table structure. Initially, there will be no rows.

### 5. Exploring the Code

#### main.py

The `main.py` file contains the core Flask application. Let’s examine its contents:

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Create database tables (if not exist)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/secrets')
def secrets():
    return render_template('secrets.html')

@app.route('/logout')
def logout():
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**

- **Flask and SQLAlchemy** are imported. The app is configured with a secret key (used for session security) and a SQLite database URI pointing to `users.db`.
- A `User` model is defined, mapping to the `users` table. It includes `id`, `email`, `password`, and `name` columns.
- `db.create_all()` ensures the table is created. Since the database file already exists, this command will simply connect to it and verify the schema.
- Route definitions:
  - `/` → renders `index.html`
  - `/register` → renders `register.html`
  - `/login` → renders `login.html`
  - `/secrets` → renders `secrets.html`
  - `/logout` → placeholder (does nothing yet)
- The app runs in debug mode when executed directly.

Note: The routes currently only render templates; they do not handle form submissions (POST requests) or interact with the database.

#### Templates

- **base.html**:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>{% block title %}{% endblock %}</title>
      <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
  </head>
  <body>
      <nav>
          <a href="{{ url_for('home') }}">Home</a>
          {% if not current_user.is_authenticated %}
              <a href="{{ url_for('login') }}">Login</a>
              <a href="{{ url_for('register') }}">Register</a>
          {% else %}
              <a href="{{ url_for('logout') }}">Logout</a>
          {% endif %}
      </nav>
      <main>
          {% block content %}{% endblock %}
      </main>
  </body>
  </html>
  ```
  - The navigation bar uses `current_user.is_authenticated` (provided by Flask-Login) to conditionally show links. However, at this stage Flask-Login is not yet installed/configured, so `current_user` is not defined. This will cause an error when you run the app. In the starting project, you may see a placeholder comment or an alternative static navigation. The exact code may differ slightly, but the concept remains: after Flask-Login is integrated, the navigation will adapt based on login status.

- **index.html**:
  ```html
  {% extends "base.html" %}
  {% block title %}Home{% endblock %}
  {% block content %}
  <h1>Welcome to the Secret Page</h1>
  <p>This is a secret area. You need to log in to see the secrets.</p>
  <a href="{{ url_for('login') }}">Login</a> or <a href="{{ url_for('register') }}">Register</a>
  {% endblock %}
  ```

- **login.html** and **register.html** contain forms with method="POST" and appropriate fields. They currently do not have form action URLs, but they will submit to the same route.

- **secrets.html**:
  ```html
  {% extends "base.html" %}
  {% block title %}Secrets{% endblock %}
  {% block content %}
  <h1>Hello, {{ name }}!</h1>
  <p>Welcome to the secret page. Only logged-in users can see this.</p>
  <a href="{{ url_for('download') }}">Download Your File</a>
  {% endblock %}
  ```
  Note the `{{ name }}` placeholder and the link to `url_for('download')`. The `download` route does not yet exist; you will add it later.

### 6. Running the Application

To confirm that the project is set up correctly:

1. Ensure your virtual environment is active (PyCharm usually does this automatically).
2. Run `main.py` (right-click → Run 'main' or click the green triangle).
3. Open a browser and go to `http://127.0.0.1:5000`.

You should see the home page with a welcome message and links to Login and Register. Clicking these links should render the respective forms. The forms will not submit successfully because the routes do not handle POST requests yet, but the pages should display.

If you encounter errors related to `current_user`, it means the template is referencing Flask-Login variables before Flask-Login is installed. This is expected in the starting state. You will fix this when you integrate Flask-Login in a later lesson. For now, you can comment out the conditional parts in `base.html` or simply ignore the error and proceed with the setup.

### 7. Next Steps

With the project running, you are ready to begin implementing authentication. The subsequent lessons will guide you through:

- **Register New Users**: Handling the registration form, storing user data in the database.
- **Downloading Files**: Creating a `/download` route that serves the PDF file.
- **Encryption and Hashing**: Understanding why passwords must be hashed.
- **Salting Passwords**: How to add randomness to password hashes.
- **Hashing with Werkzeug**: Using `generate_password_hash` and `check_password_hash`.
- **Flask-Login Integration**: Setting up user sessions, protecting routes, and implementing login/logout.
- **Flash Messages**: Providing feedback for failed login attempts or duplicate registrations.
- **Template Authentication Status**: Conditionally showing/hiding navigation links based on login status.

Each lesson will build upon the code you have in this starting project. By the end, you will have a fully functional authentication system.

### 8. Troubleshooting

- **Red underlines in main.py**: Usually means the required packages are not installed or the interpreter is not set correctly. Double-check the Python interpreter in PyCharm settings and ensure it points to the `venv` folder where packages were installed.
- **ModuleNotFoundError**: Run `pip install -r requirements.txt` again from the terminal.
- **Database errors**: Ensure `users.db` is in the same directory as `main.py`. If missing, you can create it by running `db.create_all()` in a Python shell.
- **Template errors related to `current_user`**: Temporarily remove the conditional logic or define `current_user` as a dummy variable. This will be resolved after Flask-Login is configured.

Now you have a solid foundation. Proceed to the next lesson to start registering new users.