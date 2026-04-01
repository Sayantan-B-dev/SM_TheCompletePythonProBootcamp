# Introduction to Jinja2

Jinja is a modern templating engine for Python designed to generate dynamic text-based output, most commonly HTML. It separates presentation logic from application logic, allowing developers to keep Python code independent from markup structure.

It is widely used in web development frameworks such as Flask and Django, although Django includes its own templating system inspired by Jinja’s design philosophy.

---

## 1. Why Jinja2 Exists

When generating HTML dynamically using raw Python string formatting, code becomes tightly coupled with presentation logic. This creates:

* Poor maintainability
* Hard-to-read markup
* Unsafe rendering risks
* No structured control flow

Jinja2 solves this by introducing:

* Variable interpolation
* Control structures such as loops and conditionals
* Template inheritance
* Automatic HTML escaping
* Reusable template components

---

## 2. Installation

Install via pip:

```bash
pip install jinja2
```

---

## 3. Core Concepts

### 3.1 Template

A template is an HTML file containing placeholders and control structures.

Example template file: `profile.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Hello {{ username }}</h1>
</body>
</html>
```

The `{{ ... }}` syntax represents variable substitution.

---

### 3.2 Rendering a Template

```python
# Import the required classes from jinja2
from jinja2 import Environment, FileSystemLoader

# Create an environment object that loads templates from current directory
template_environment = Environment(
    loader=FileSystemLoader(searchpath="./")
)

# Load the template file
template_object = template_environment.get_template("profile.html")

# Define dynamic content that will be injected into the template
context_data = {
    "title": "User Dashboard",
    "username": "Sayantan"
}

# Render the template using the context dictionary
rendered_output = template_object.render(context_data)

# Save the rendered HTML to a file
with open("output.html", "w", encoding="utf-8") as file_object:
    file_object.write(rendered_output)

print("HTML generated successfully.")
```

---

### Expected Output

```html
<!DOCTYPE html>
<html>
<head>
    <title>User Dashboard</title>
</head>
<body>
    <h1>Hello Sayantan</h1>
</body>
</html>
```

---

## 4. Syntax Overview

### 4.1 Variable Expression

```html
{{ variable_name }}
```

Used to display values passed from Python.

---

### 4.2 For Loop

```html
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

The `{% ... %}` syntax is used for control statements.

---

### 4.3 Conditional Statements

```html
{% if user_is_admin %}
    <p>Access granted</p>
{% else %}
    <p>Access denied</p>
{% endif %}
```

---

## 5. Template Inheritance

Inheritance avoids duplication in multi-page systems.

Base template:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

Child template:

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
<h1>Main Page</h1>
{% endblock %}
```

This pattern is critical in large applications.

---

## 6. Autoescaping and Security

Jinja2 automatically escapes HTML-sensitive characters when configured in web environments. This prevents cross-site scripting vulnerabilities when rendering user input.

Example:

```python
Environment(
    loader=FileSystemLoader("./"),
    autoescape=True
)
```

---

## 7. When to Use Jinja2

Jinja2 is ideal for:

* Web applications
* Static site generation
* HTML report generation
* Email template rendering
* Dashboard generation
* Data visualization wrappers

---

## 8. Architectural Philosophy

Jinja2 enforces a clean separation:

* Python handles data processing
* Templates handle presentation
* Minimal logic inside templates
* Structured rendering pipeline

This separation increases scalability, readability, and maintainability in both small and large systems.

---

If you want, next we can go deeper into:

* Custom filters and macros
* Integrating Jinja2 with FastAPI
* Building a report generator system
* Structuring large multi-template projects
* Performance optimization and caching

Just specify the direction and depth you want.
