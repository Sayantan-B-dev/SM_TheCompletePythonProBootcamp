# Dynamic HTML Templating in Python

Dynamic HTML templating is the process of **generating HTML documents programmatically**, where parts of the content are injected at runtime using variables, loops, conditions, or computed values.

This is typically done using a **template engine**, which separates presentation (HTML) from application logic (Python).

---

# 1. Conceptual Architecture

A templating workflow generally follows this execution flow:

```
Python Data  →  Template Engine  →  HTML Output
```

The template contains placeholders, and Python supplies the dynamic data context.

---

# 2. Using Jinja2 (Industry Standard Approach)

## What is Jinja2?

Jinja is a powerful, fast, and expressive template engine for Python.
It is widely used with frameworks like Flask and Django (Django has its own similar engine).

---

## Installation

```bash
pip install jinja2
```

---

## Basic Example — Injecting Variables

### Step 1: Create Template File (`template.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>Hello {{ user_name }}</h1>
    <p>Your age is {{ age }}</p>
</body>
</html>
```

---

### Step 2: Python Rendering Script

```python
# Import Jinja2 environment and file loader
from jinja2 import Environment, FileSystemLoader

# Create a template environment
# FileSystemLoader tells Jinja2 where template files are located
template_environment = Environment(
    loader=FileSystemLoader(searchpath="./")
)

# Load the template file
template_object = template_environment.get_template("template.html")

# Define dynamic content to inject
dynamic_context = {
    "page_title": "User Profile",
    "user_name": "Sayantan",
    "age": 26
}

# Render the template with dynamic data
rendered_html_output = template_object.render(dynamic_context)

# Write the final HTML to a file
with open("output.html", "w", encoding="utf-8") as output_file:
    output_file.write(rendered_html_output)

print("HTML file generated successfully.")
```

---

### Expected Output (Generated HTML)

```html
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>Hello Sayantan</h1>
    <p>Your age is 26</p>
</body>
</html>
```

---

# 3. Dynamic Lists with Loops

Templates support iteration logic.

### Template (`products.html`)

```html
<ul>
{% for product in product_list %}
    <li>{{ product.name }} - ₹{{ product.price }}</li>
{% endfor %}
</ul>
```

---

### Python

```python
from jinja2 import Environment, FileSystemLoader

template_environment = Environment(
    loader=FileSystemLoader(searchpath="./")
)

template_object = template_environment.get_template("products.html")

dynamic_context = {
    "product_list": [
        {"name": "Laptop", "price": 55000},
        {"name": "Keyboard", "price": 1500},
        {"name": "Mouse", "price": 800}
    ]
}

rendered_html_output = template_object.render(dynamic_context)

with open("products_output.html", "w", encoding="utf-8") as output_file:
    output_file.write(rendered_html_output)
```

---

### Expected Output

```html
<ul>
    <li>Laptop - ₹55000</li>
    <li>Keyboard - ₹1500</li>
    <li>Mouse - ₹800</li>
</ul>
```

---

# 4. Conditional Rendering

### Template

```html
{% if is_logged_in %}
    <p>Welcome back, {{ username }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

---

# 5. Template Inheritance (Advanced Structure)

Useful for large projects.

### Base Template (`base.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <header>Website Header</header>

    {% block content %}
    {% endblock %}

    <footer>Website Footer</footer>
</body>
</html>
```

---

### Child Template

```html
{% extends "base.html" %}

{% block title %}Home Page{% endblock %}

{% block content %}
<h1>Main Content Here</h1>
{% endblock %}
```

This architecture prevents duplication and improves maintainability.

---

# 6. Without Jinja2 (Pure Python String Formatting)

This is possible but not recommended for complex logic.

```python
user_name = "Sayantan"
age = 26

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>Hello {user_name}</h1>
    <p>Your age is {age}</p>
</body>
</html>
"""

with open("output.html", "w", encoding="utf-8") as output_file:
    output_file.write(html_template)
```

### Why This Is Not Ideal

* No separation of concerns
* Hard to scale
* No loops or conditional logic
* Security risk if rendering unescaped user input

---

# 7. Production-Level Usage

If building web applications:

| Framework | Template Engine               |
| --------- | ----------------------------- |
| Flask     | Jinja2                        |
| Django    | Django Template Engine        |
| FastAPI   | Jinja2 (optional integration) |

For static site generation, reporting systems, dashboards, or scraping pipelines that output HTML reports, Jinja2 remains the cleanest solution.

---

# 8. Best Practices

* Keep logic minimal inside templates
* Pass fully prepared data structures from Python
* Escape user input (Jinja2 auto-escapes in web mode)
* Use template inheritance for large projects
* Avoid embedding business logic in HTML

---

If you want, I can next show:

* Generating HTML reports from scraped Selenium data
* Building a mini templating engine manually
* Using FastAPI with HTML templates
* Converting dynamic HTML to PDF
* Structuring a large multi-page template system

Tell me the direction you're aiming for, and we’ll go deep into that architecture.
