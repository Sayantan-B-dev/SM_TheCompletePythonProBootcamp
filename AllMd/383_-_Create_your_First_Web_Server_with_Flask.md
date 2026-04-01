# Library vs Framework — Structural and Control Differences

## Core Conceptual Distinction

| Dimension            | Library                               | Framework                                                 |
| -------------------- | ------------------------------------- | --------------------------------------------------------- |
| Control Flow         | You control execution flow explicitly | Framework controls execution and calls your code          |
| Inversion of Control | No inversion of control occurs        | Inversion of control principle enforced                   |
| Usage Pattern        | Import and use functions selectively  | Define structure and plug logic into predefined lifecycle |
| Flexibility          | Highly flexible, minimal constraints  | Opinionated structure and architectural enforcement       |
| Example in Python    | `requests`, `numpy`                   | `Flask`, `Django`, `FastAPI`                              |

### Technical Clarification

A **library** is a collection of reusable functions or classes that you explicitly invoke when required.

A **framework** defines the application skeleton and lifecycle. You write code that fits into its architecture, and it decides when execution happens.

Example analogy:

* Using `requests.get()` is library usage because you call it.
* Using Flask route decorators is framework usage because Flask calls your function when HTTP request occurs.

---

# All Steps to Run a Successful Flask Server

## Step 1 — Install Python

Verify Python installation:

```bash
python --version
```

Expected output:

```
Python 3.x.x
```

---

## Step 2 — Create Virtual Environment

Creating isolated environment avoids dependency conflicts.

```bash
python -m venv virtual_environment_name
```

Activate environment:

**Windows**

```bash
virtual_environment_name\Scripts\activate
```

**Mac/Linux**

```bash
source virtual_environment_name/bin/activate
```

Expected output shows environment prefix in terminal.

---

## Step 3 — Install Flask

```bash
pip install flask
```

Verify installation:

```bash
pip list
```

Expected output includes:

```
Flask x.x.x
```

---

## Step 4 — Project Structure

```
project_folder/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
```

Explanation:

* `templates/` stores HTML files.
* `static/` stores CSS, JavaScript, images.
* `app.py` contains server logic.

---

# Minimal Flask Server Setup

## File: app.py

```python
# Import Flask framework
from flask import Flask, render_template

# Create Flask application instance
application = Flask(__name__)

# Define route for homepage
@application.route("/")
def homepage():
    """
    This function renders an HTML template.
    Flask automatically searches inside 'templates' folder.
    """
    return render_template("index.html")


# Entry point of program
if __name__ == "__main__":
    # debug=True enables auto-reload and error tracing
    application.run(debug=True)
```

---

## Run Server

```bash
python app.py
```

Expected console output:

```
* Running on http://127.0.0.1:5000/
```

---

# Connecting HTML Pages in Flask

## Step 1 — Create HTML File

### File: templates/index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask HTML Example</title>
    <!-- Link CSS from static folder -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

    <h1>Welcome to Flask Backend</h1>
    <p>This page is rendered from backend.</p>

</body>
</html>
```

Explanation:

`{{ url_for('static', filename='style.css') }}` dynamically generates correct static path.

---

## Step 2 — Create CSS File

### File: static/style.css

```css
body {
    background-color: #121212;
    color: white;
    font-family: Arial;
}
```

Expected behavior:

Browser loads CSS automatically from static folder.

---

# Connecting Multiple HTML Pages

## Add Another Route

Modify `app.py`:

```python
@application.route("/about")
def about_page():
    """
    Renders About page.
    """
    return render_template("about.html")
```

---

## Create About HTML

### File: templates/about.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>About Page</title>
</head>
<body>

    <h2>About This Application</h2>
    <a href="/">Go Back Home</a>

</body>
</html>
```

---

# Passing Data from Backend to HTML

Modify route:

```python
@application.route("/")
def homepage():
    """
    Pass dynamic data into template.
    """
    
    user_name = "Sayantan"
    
    return render_template("index.html", name=user_name)
```

Update HTML:

```html
<h1>Hello {{ name }}</h1>
```

Expected output:

```
Hello Sayantan
```

---

# Production-Level Flask Execution

For development:

```bash
python app.py
```

For production:

```bash
pip install gunicorn
gunicorn app:application
```

Explanation:

* `app` refers to file name without `.py`
* `application` refers to Flask instance variable

---

# Common Reasons Flask Server Fails

| Issue                    | Cause                         | Resolution                  |
| ------------------------ | ----------------------------- | --------------------------- |
| Module not found         | Virtual environment inactive  | Activate environment        |
| Port already in use      | Another server running        | Change port                 |
| Template not found       | HTML outside templates folder | Correct folder placement    |
| Static files not loading | Incorrect `url_for` usage     | Use Flask static convention |

---

# Final Conceptual Understanding

A successful Flask server requires:

* Correct environment setup
* Structured folder hierarchy
* Proper route definition
* Correct template rendering
* Static file linking via `url_for`
* Debug configuration during development
* WSGI server during production

This forms the foundational backend workflow connecting Python server logic to HTML frontend rendering.
