# Jinja2 in Flask — Loops, Data Handling, Bidirectional Data Flow, and Conditional Rendering

## 1. Data Flow Model Between Client, Flask, and Jinja

The complete lifecycle operates in the following direction:

```
Client Request → Flask Route → Python Processing → Jinja Template → HTML Response
```

Data can flow:

• From Flask to Jinja (rendering variables)
• From Client to Flask (forms, query params, JSON payloads)
• From Flask back to Client (HTML, JSON, redirects)

Jinja only renders data passed to it by Flask. It does not fetch data itself.

---

# 2. Passing Different Data Types to Templates

Jinja supports rendering of most native Python data types.

## Example Flask Route

```python
# Import necessary modules
from flask import Flask, render_template, request, jsonify

application = Flask(__name__)

@application.route("/")
def home_route():
    
    # Define multiple types of data
    user_name = "sayantan"
    user_age = 26
    is_active_user = True
    
    skills_list = ["Python", "Flask", "React"]
    
    user_dictionary = {
        "role": "developer",
        "location": "India",
        "experience": 2
    }
    
    return render_template(
        "dashboard.html",
        name=user_name,
        age=user_age,
        active=is_active_user,
        skills=skills_list,
        profile=user_dictionary
    )

if __name__ == "__main__":
    application.run(debug=True)
```

---

# 3. Jinja For Loops

## Template: `dashboard.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>

    <h2>Skill List</h2>

    <ul>
        {% for skill in skills %}
            <li>{{ loop.index }} - {{ skill }}</li>
        {% endfor %}
    </ul>

</body>
</html>
```

### Explanation

`{% for skill in skills %}` iterates over the Python list.

`loop.index` gives 1-based index.
Other loop attributes available:

| Attribute   | Meaning                     |
| ----------- | --------------------------- |
| loop.index  | Current iteration (1-based) |
| loop.index0 | Current iteration (0-based) |
| loop.first  | True if first iteration     |
| loop.last   | True if last iteration      |
| loop.length | Total items in loop         |

---

## Conditional Logic Inside Loop

```html
{% for skill in skills %}
    {% if skill == "Python" %}
        <li><strong>{{ skill }}</strong> (Primary)</li>
    {% else %}
        <li>{{ skill }}</li>
    {% endif %}
{% endfor %}
```

---

# 4. Looping Through Dictionaries

### Python Dictionary

```python
user_dictionary = {
    "role": "developer",
    "location": "India",
    "experience": 2
}
```

### Template

```html
<h3>User Profile</h3>

<ul>
    {% for key, value in profile.items() %}
        <li>{{ key }} : {{ value }}</li>
    {% endfor %}
</ul>
```

Jinja allows `.items()` similar to Python.

---

# 5. Nested Data Structures

## Python

```python
projects = [
    {"name": "Portfolio", "tech": ["Flask", "React"]},
    {"name": "API Server", "tech": ["FastAPI", "PostgreSQL"]}
]
```

## Template

```html
<h3>Projects</h3>

{% for project in projects %}
    <h4>{{ project.name }}</h4>
    
    <ul>
        {% for technology in project.tech %}
            <li>{{ technology }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

Jinja supports nested iteration without restrictions.

---

# 6. Conditional Rendering (Advanced)

## Basic Conditional

```html
{% if active %}
    <p>User is active</p>
{% else %}
    <p>User is inactive</p>
{% endif %}
```

---

## Multiple Conditions

```html
{% if age < 18 %}
    <p>Minor</p>
{% elif age >= 18 and age < 60 %}
    <p>Adult</p>
{% else %}
    <p>Senior</p>
{% endif %}
```

---

## Truthy / Falsy Checks

```html
{% if skills %}
    <p>Total skills: {{ skills|length }}</p>
{% else %}
    <p>No skills available</p>
{% endif %}
```

Empty lists evaluate as False.

---

# 7. Handling Missing Variables Safely

```html
<p>{{ name or "Guest" }}</p>
```

or using filter:

```html
<p>{{ name | default("Guest") }}</p>
```

---

# 8. Data Passing From Client to Flask

## Query Parameters

```python
@application.route("/search")
def search_route():
    
    query_value = request.args.get("query")
    
    return render_template("search.html", query=query_value)
```

URL:

```
/search?query=flask
```

---

## HTML Form (POST Example)

### Template Form

```html
<form method="POST" action="/submit">
    <input type="text" name="username">
    <input type="number" name="age">
    <button type="submit">Submit</button>
</form>
```

---

### Flask Handling

```python
@application.route("/submit", methods=["POST"])
def submit_route():
    
    username = request.form.get("username")
    age_value = request.form.get("age")
    
    return render_template("result.html", name=username, age=age_value)
```

---

# 9. Sending JSON Data (API Communication)

Flask can return structured JSON.

```python
@application.route("/api/data")
def api_data_route():
    
    response_payload = {
        "status": "success",
        "count": 3,
        "items": ["Python", "Flask", "Jinja"]
    }
    
    return jsonify(response_payload)
```

Frontend JavaScript can consume this API asynchronously.

---

# 10. Combining Conditional Rendering and Data Flow

Example template combining everything:

```html
<h2>Welcome</h2>

{% if name %}
    <p>Hello {{ name.title() }}</p>
{% endif %}

{% if gender %}
    <p>You might be a {{ gender }}</p>
{% endif %}

{% if age %}
    <p>Your age could be: {{ age }}</p>
{% endif %}

{% if skills %}
    <h3>Skills</h3>
    <ul>
        {% for skill in skills %}
            <li>{{ skill }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

This ensures:

• No empty placeholders
• Clean conditional blocks
• Dynamic list rendering
• Safe evaluation

---

# 11. Server-Side vs Client-Side Rendering

| Feature                | Jinja (Server) | JavaScript (Client) |
| ---------------------- | -------------- | ------------------- |
| Runs On                | Server         | Browser             |
| SEO Friendly           | Yes            | Depends             |
| Faster First Load      | Yes            | Sometimes slower    |
| Dynamic Without Reload | No             | Yes                 |

Jinja is ideal when:

• You want full page rendering from server
• You are building a traditional web app
• You want simple architecture

---

# 12. Security Note

Jinja auto-escapes HTML content to prevent XSS attacks.

Example:

If user submits:

```
<script>alert(1)</script>
```

It will render safely as text unless explicitly marked safe.

---

Jinja2 in Flask gives you:

• Clean separation of logic and UI
• Powerful data handling
• Full control over conditional rendering
• Structured templating architecture

If you want next, we can move into:

• Template inheritance architecture
• Authentication-based conditional UI
• Session-based rendering
• Building a production-ready folder structure
• Integrating with React frontend

Tell me the direction and we go deeper.
