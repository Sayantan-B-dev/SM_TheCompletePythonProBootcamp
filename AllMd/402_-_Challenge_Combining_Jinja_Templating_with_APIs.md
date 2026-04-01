# Introduction to Jinja2 with Flask

## What Jinja2 Actually Does

Jinja is a server-side templating engine that transforms HTML files into dynamic documents using runtime data passed from Python.

When used with Flask, Jinja2 is automatically integrated. Flask renders `.html` templates and injects variables from routes into those templates.

The rendering pipeline looks like this:

```
HTTP Request → Flask Route → Python Logic → Jinja2 Template → Final HTML Response
```

---

# Project Structure

```
project_folder/
│
├── app.py
│
└── templates/
    └── index.html
```

Flask automatically looks for templates inside the `templates/` directory.

---

# Basic Flask + Jinja2 Example

## app.py

```python
# Import required modules
from flask import Flask, render_template, request, jsonify

# Create Flask application instance
application = Flask(__name__)

# Define route for homepage
@application.route("/")
def home_route():
    # Send simple variable to template
    return render_template(
        "index.html",
        name="sayantan",
        gender="developer",
        age=26
    )

# Run application
if __name__ == "__main__":
    application.run(debug=True)
```

---

## templates/index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Jinja Example</title>
</head>
<body>

    {% if name %}
        <p>Hello {{ name.title() }}</p>
    {% endif %}

    {% if gender %}
        <p>You might be a {{ gender }}</p>
    {% endif %}

    {% if age %}
        <p>Your age could be: {{ age }}</p>
    {% endif %}

</body>
</html>
```

---

# Explanation of This Template

### 1. `{% if name %}`

This checks whether `name` exists and is truthy.

If Flask does not pass `name`, this block does not render.

### 2. `{{ name.title() }}`

Double curly braces mean:
“Evaluate this Python expression and print the result.”

`.title()` is a Python string method.
Jinja allows calling simple methods like this.

If `name = "sayantan"`, output becomes:

```
Hello Sayantan
```

### 3. Conditional Rendering Logic

The template behaves like:

```
if variable exists:
    show HTML block
else:
    show nothing
```

This prevents errors and avoids displaying empty placeholders.

---

# Passing Data from Route Parameters

Flask supports multiple types of route parameters.

---

## 1. String Parameter

```python
@application.route("/user/<username>")
def user_profile(username):
    return render_template("index.html", name=username)
```

URL:

```
/user/rahul
```

Flask automatically injects `"rahul"` into the function argument.

---

## 2. Integer Parameter

```python
@application.route("/age/<int:user_age>")
def age_route(user_age):
    return render_template("index.html", age=user_age)
```

If user enters `/age/30`, Flask ensures it is integer.

---

## 3. Float Parameter

```python
@application.route("/price/<float:amount>")
def price_route(amount):
    return f"Price received: {amount}"
```

---

## 4. Multiple Parameters

```python
@application.route("/profile/<name>/<gender>/<int:age>")
def profile_route(name, gender, age):
    return render_template(
        "index.html",
        name=name,
        gender=gender,
        age=age
    )
```

URL:

```
/profile/sayantan/male/26
```

---

# Query Parameters (From URL ?key=value)

These are accessed using `request.args`.

```python
@application.route("/info")
def info_route():
    name = request.args.get("name")
    gender = request.args.get("gender")
    age = request.args.get("age")

    return render_template(
        "index.html",
        name=name,
        gender=gender,
        age=age
    )
```

URL:

```
/info?name=alex&gender=engineer&age=25
```

---

# Handling Forms (POST Request)

```python
@application.route("/submit", methods=["POST"])
def submit_route():
    name = request.form.get("name")
    age = request.form.get("age")

    return render_template("index.html", name=name, age=age)
```

---

# Returning JSON (API Response)

Flask can also act as an API server.

```python
@application.route("/api/user/<username>")
def api_user(username):
    response_data = {
        "name": username,
        "role": "developer",
        "status": "active"
    }

    return jsonify(response_data)
```

This does not use Jinja.
It returns JSON instead of HTML.

---

# Mixing HTML and API in One App

Flask allows:

| Route Type | Returns          |
| ---------- | ---------------- |
| `/`        | HTML Template    |
| `/api/...` | JSON             |
| `/submit`  | Redirect or HTML |
| `/data`    | Raw text         |

You choose response type depending on application architecture.

---

# Advanced Jinja Concepts

## Loop Example

```html
<ul>
{% for skill in skills %}
    <li>{{ skill }}</li>
{% endfor %}
</ul>
```

If Python sends:

```python
skills = ["Python", "Flask", "React"]
```

It renders a dynamic list.

---

## Filters in Jinja

```html
<p>{{ name | upper }}</p>
<p>{{ name | lower }}</p>
<p>{{ name | capitalize }}</p>
```

Filters transform data before display.

---

## Default Value Handling

```html
<p>{{ name or "Guest" }}</p>
```

If `name` is missing, "Guest" is shown.

---

# What Happens Internally

1. Flask receives HTTP request.
2. Flask matches route.
3. Route function executes.
4. `render_template()` loads HTML.
5. Jinja replaces placeholders.
6. Final HTML returned to browser.

Jinja executes on the server, not in the browser.

---

# Why Templating Is Powerful

• Prevents hardcoding HTML
• Enables dynamic content generation
• Clean separation of logic and presentation
• Secure variable escaping
• Scalable architecture for large applications

---

If you want next, I can:

* Build a small real-world mini project structure
* Show template inheritance with layout system
* Connect Flask frontend with React backend
* Demonstrate authentication example with sessions
* Explain security issues like XSS in templates

Tell me the direction and we go deeper into architecture.
