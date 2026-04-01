# Cafe & Wifi API – Starting Project Setup

## 1. Project Overview
The starting project for the Cafe & Wifi API provides a foundational codebase and database for building a RESTful web service. It includes:

- A pre-populated SQLite database (`cafes.db`) containing records of cafes in London, with details such as location, amenities, and coffee prices.
- A Flask application skeleton (`main.py`) with basic imports and configuration.
- A `requirements.txt` file listing all necessary Python packages.
- A folder structure that separates the database (inside `instance/`) from the application code.

This setup allows developers to focus on implementing API endpoints without worrying about database creation or initial data population. The project is designed to be run in a virtual environment to isolate dependencies.

## 2. Database Structure – cafes.db

The SQLite database `cafes.db` contains a single table named `cafe`. The table schema is defined using SQLAlchemy ORM in `main.py` (though the database was created separately and provided as a ready-to-use file). The fields are as follows:

| Column Name      | Data Type | Description |
|------------------|-----------|-------------|
| id               | Integer   | Primary key, auto-incrementing unique identifier for each cafe. |
| name             | String    | The name of the cafe. |
| map_url          | String    | URL to the cafe’s location on Google Maps (or similar service). |
| img_url          | String    | URL to an image of the cafe. |
| location         | String    | The general area or neighbourhood (e.g., "Shoreditch", "Covent Garden"). |
| has_sockets      | Boolean   | Indicates if power sockets are available. |
| has_toilet       | Boolean   | Indicates if a public toilet is present. |
| has_wifi         | Boolean   | Indicates if Wi-Fi is available. |
| can_take_calls   | Boolean   | Indicates if it is acceptable to take phone/video calls. |
| seats            | String    | Description of seating capacity (e.g., "10-20", "50+"). |
| coffee_price     | String    | Price of a single black coffee (e.g., "£2.50"). |

The database is populated with several records representing real cafes in London that are suitable for remote work. These records serve as the initial data set for the API.

## 3. Project File Structure

After downloading and unzipping the starting project, the directory structure should resemble:

```
project-folder/
│
├── instance/
│   └── cafes.db               # SQLite database file
├── main.py                     # Flask application entry point
├── requirements.txt            # Python package dependencies
└── (other files, e.g., README)
```

- `instance/` is a conventional folder for Flask to store instance-specific data like database files. It ensures that the database is not accidentally committed to version control if a `.gitignore` is properly set.
- `main.py` contains the Flask app initialization, SQLAlchemy configuration, and the `Cafe` model definition.
- `requirements.txt` lists all packages required to run the project.

## 4. Setting Up the Development Environment

### 4.1 Prerequisites
- Python 3.13 or higher (the project was tested on Python 3.13.1).
- pip (Python package installer).
- (Optional) A virtual environment tool (venv is built into Python).

### 4.2 Step-by-Step Setup Instructions

#### 4.2.1 Download and Extract
1. Download the starting `.zip` file from the provided resources.
2. Extract the contents to a directory of your choice (e.g., `cafe-api/`).

#### 4.2.2 Create a Virtual Environment (Recommended)
Open a terminal/command prompt in the project directory and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

A virtual environment ensures that the project's dependencies are isolated from other Python projects and the system Python installation.

#### 4.2.3 Install Dependencies
With the virtual environment activated, install the required packages using `pip` and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Alternatively, if you are using PyCharm, the IDE may automatically prompt you to create a virtual environment and install dependencies upon opening the project. If that prompt appears, accept it.

#### 4.2.4 Verify Installation
Check that all packages are installed correctly:

```bash
pip list
```

The output should include packages such as Flask, Flask-SQLAlchemy, SQLAlchemy, Werkzeug, etc., matching the versions in `requirements.txt`.

### 4.3 Troubleshooting Common Issues

#### 4.3.1 Red Underlines in main.py (PyCharm)
If you open `main.py` in PyCharm and see red underlines under import statements, it indicates that the interpreter is not configured correctly. Solutions:

- **Reload from Disk:** Go to `File -> Reload All from Disk`. This forces PyCharm to re-index the project and recognize the virtual environment.
- **Manually Set Interpreter:** Go to `File -> Settings -> Project -> Python Interpreter`. Click the gear icon, then `Add...`. Choose `Existing environment` and navigate to the `venv/Scripts/python.exe` (Windows) or `venv/bin/python` (macOS/Linux). Ensure the interpreter path points to the virtual environment's Python executable.
- **Install Packages via Terminal:** Open the terminal in PyCharm (bottom left) and run:
  ```bash
  pip install -r requirements.txt
  ```
  This ensures packages are installed in the currently activated environment.

#### 4.3.2 Flask Not Found
If running `python main.py` results in `ModuleNotFoundError: No module named 'flask'`, the virtual environment is either not activated or dependencies were not installed. Activate the environment and run the installation command again.

#### 4.3.3 Database Not Found or Empty
The database file `cafes.db` should be inside the `instance/` folder. If the file is missing, check that you extracted all files correctly. The database is pre-populated; you can verify its contents using a tool like **DB Browser for SQLite** (see Section 5).

### 4.4 Running the Application
After successful setup, you can run the Flask development server:

```bash
python main.py
```

By default, the server will start at `http://127.0.0.1:5000`. Visiting this URL in a browser may show a 404 error because no routes have been defined yet. This is expected; the next steps involve implementing API endpoints.

## 5. Inspecting the Database with DB Browser for SQLite

To understand the data you will be working with, it is helpful to inspect `cafes.db` using a graphical tool. **DB Browser for SQLite** is a free, open-source tool that allows you to view and query SQLite databases.

1. Download and install DB Browser for SQLite from [https://sqlitebrowser.org/](https://sqlitebrowser.org/).
2. Open the application and click `Open Database`.
3. Navigate to your project's `instance/` folder and select `cafes.db`.
4. Browse the `cafe` table under the "Browse Data" tab.

You will see the existing records with all fields populated. Familiarizing yourself with the data will help when designing API responses and understanding what information is available.

## 6. Understanding the Code – main.py

The `main.py` file contains the core Flask application setup. Below is an annotated version of what you can expect to see (the actual file may vary slightly).

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Cafe model
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Converts the Cafe object into a dictionary for JSON serialization."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

### 6.1 Key Components

- **Flask App:** The central application instance.
- **SQLAlchemy Configuration:** `SQLALCHEMY_DATABASE_URI` points to the SQLite database file located in the `instance/` folder. Flask automatically resolves `sqlite:///cafes.db` to `instance/cafes.db`.
- **Cafe Model:** Defines the table structure. The `to_dict()` method is a utility that returns a dictionary representation of the model instance, useful for JSON responses.
- **db.create_all():** Ensures the tables exist when the app starts. Since the database is already provided, this line is not strictly necessary but is harmless.

## 7. Next Steps – Building the API

With the project set up and the database in place, the next tasks involve implementing the RESTful endpoints as described in the subsequent lessons:

- **GET /random** – Retrieve a random cafe.
- **GET /all** – Retrieve all cafes.
- **GET /search?loc=...** – Search cafes by location.
- **POST /** – Add a new cafe.
- **PATCH /update-price/<cafe_id>** – Update the coffee price.
- **DELETE /report-closed/<cafe_id>** – Delete a cafe (with API key authentication).

Each endpoint will interact with the database using SQLAlchemy queries and return JSON responses using Flask's `jsonify()` or the model's `to_dict()` method.

## 8. Important Considerations

- The database file `cafes.db` is provided as part of the starting project. Any changes made via the API (POST, PATCH, DELETE) will modify this file. To reset to the original state, you can re-download the starting project or keep a backup copy.
- The project uses **Flask-SQLAlchemy**, which integrates SQLAlchemy with Flask. All database operations should be performed within an application context.
- Debug mode is enabled (`debug=True`) during development, which provides detailed error pages and auto-reloads on code changes. This should be disabled in production.

## 9. Summary

The starting project provides everything needed to begin building a RESTful API for cafe data. By following the setup instructions, you will have a fully functional development environment with a populated database. The subsequent lessons will guide you through implementing each HTTP method and building a complete, documented API service.