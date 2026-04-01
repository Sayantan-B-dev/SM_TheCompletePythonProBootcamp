# Day 61: Building Advanced Forms with Flask-WTF

## Goals

Today we move beyond basic HTML forms and learn to use **Flask-WTF**, a Flask extension that integrates the powerful **WTForms** library. By the end of the day, you will build a **"Secrets" website** – a page that hides secret content behind a login form. Only users with the correct credentials (`admin@email.com` / `12345678`) can access the secret.

You will learn:

- Why Flask-WTF is preferred over raw HTML forms.
- How to install and configure Flask-WTF.
- Creating form classes with different field types.
- Adding built‑in validators (required, email format, length).
- Handling form submission and validation in Flask routes.
- Using Jinja2 template inheritance to create a consistent layout.
- Styling your site with Bootstrap‑Flask.
- The ultimate shortcut: `render_form()`.

---

## Why Flask‑WTF?

Flask‑WTF brings three major advantages:

| Benefit | Description |
|--------|-------------|
| **Easy Form Validation** | Automatically check that email addresses contain `@` and a dot, that passwords meet length requirements, etc. No need to write custom validation logic. |
| **Less Code** | Define forms once as Python classes and reuse them. Greatly reduces repetitive HTML. |
| **Built‑in CSRF Protection** | Protects against Cross‑Site Request Forgery attacks by generating a unique token per form. |

Even though you may still encounter raw HTML forms in the wild, understanding Flask‑WTF is essential for modern Flask development.

---

## Installing Flask‑WTF

Start with the provided starter files (or create a new project). Make sure you have a virtual environment activated.

Install Flask‑WTF (and its dependencies) using pip:

```bash
pip install Flask-WTF
```

If a `requirements.txt` is provided, you can install everything at once:

**Windows:**
```bash
python -m pip install -r requirements.txt
```
**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

The key packages are:
- `Flask`
- `Flask-WTF`
- `WTForms`
- `email-validator` (for email validation)

---

## Creating Forms with Flask‑WTF

Forms are defined as Python classes that inherit from `FlaskForm`. Each form field is an instance of a WTForms **Field** class (e.g., `StringField`, `PasswordField`). Fields can accept a **label** (first argument) and a list of **validators**.

### Basic Login Form

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
```

To render this form in a template, you pass an instance of the form to `render_template()`. In the HTML, you can manually create the form elements, but you need to include the CSRF token:

```html
<form method="POST" action="{{ url_for('login') }}">
    {{ form.csrf_token }}
    {{ form.email.label }} {{ form.email(size=30) }}
    {{ form.password.label }} {{ form.password(size=30) }}
    {{ form.submit() }}
</form>
```

> **Note:** The `size` attribute controls the width of the input box.

### Adding a Secret Key

CSRF protection requires a secret key. Set it in your Flask app:

```python
app.secret_key = 'any-secret-string-you-make-up'
```

For production, store the key in an environment variable or a `.env` file.

---

## Code Improvements for WTForms

The quick‑start code can be refined for better readability and functionality.

1. **Use `PasswordField`** – automatically masks input.
2. **Use `SubmitField`** – creates a submit button.
3. **Add keyword arguments for labels** – makes the code clearer.
4. **Use `url_for` in the form action** – avoids hard‑coded paths.
5. **Arrange fields with HTML** – wrap them in `<p>`, `<div>`, etc., for layout.

**Improved Form Definition:**
```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
```

**Improved Template (`login.html`):**
```html
<form method="POST" action="{{ url_for('login') }}">
    {{ form.csrf_token }}
    <p>{{ form.email.label }} {{ form.email(size=30) }}</p>
    <p>{{ form.password.label }} {{ form.password(size=30) }}</p>
    {{ form.submit() }}
</form>
```

---

## Adding Validation with Flask‑WTF

One of the biggest benefits of WTForms is the wide range of built‑in validators. You add them to the `validators` list when defining a field.

### Common Validators

| Validator | Usage |
|-----------|-------|
| `DataRequired()` | Field cannot be empty. |
| `Email()`        | Must be a valid email address (requires `email-validator` package). |
| `Length(min=8)`  | Input must be at least 8 characters. |

**Example with multiple validators:**
```python
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')
```

### Displaying Validation Errors

Each field has an `.errors` attribute – a list of error messages. In your template, you can loop through them:

```html
{% if form.email.errors %}
    <ul>
    {% for error in form.email.errors %}
        <li style="color: red;">{{ error }}</li>
    {% endfor %}
    </ul>
{% endif %}
```

### Disable Browser Validation

Browsers have their own built‑in validation (e.g., pop‑ups for required fields). To rely solely on WTForms validation, add the `novalidate` attribute to your `<form>` tag:

```html
<form method="POST" action="{{ url_for('login') }}" novalidate>
```

Now all validation messages will be consistent across browsers.

---

## Receiving Form Data with WTForms

In your route, you need to handle both **GET** (display the form) and **POST** (process submitted data). WTForms provides the `validate_on_submit()` method, which:

- Returns `True` if the request is POST **and** all validators pass.
- Returns `False` otherwise.

### Simple Login Logic

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check credentials
        if form.email.data == 'admin@email.com' and form.password.data == '12345678':
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=form)
```

Notice that you access the submitted values via `form.field.data`.

---

## Template Inheritance Using Jinja2

To avoid repeating the same HTML structure (like headers and footers) on every page, Jinja2 offers **template inheritance**.

### Base Template (`base.html`)

Create a parent template that defines **blocks** – placeholders that child templates can fill.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    <style>
        {% block styling %}
        body { background: purple; }
        {% endblock %}
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### Child Template (`success.html`)

A child template uses `{% extends "base.html" %}` and then overrides the blocks.

```html
{% extends "base.html" %}
{% block title %}Success{% endblock %}
{% block content %}
    <div class="container">
        <h1>Top Secret</h1>
        <iframe src="https://giphy.com/embed/Ju7l5y9osyymQ" ... ></iframe>
    </div>
{% endblock %}
```

### Super Blocks

If you want to **add** to a block’s content rather than replace it, use `{{ super() }}`. For example, in `denied.html` you might keep the purple background but make the `<h1>` red:

```html
{% block styling %}
    {{ super() }}
    h1 { color: red; }
{% endblock %}
```

---

## Using Bootstrap‑Flask as an Inherited Template

To quickly give your site a modern look, use **Bootstrap‑Flask**, a Flask extension that integrates Bootstrap 5.

### Installation

```bash
pip install bootstrap-flask
```

### Initialisation

In `main.py`:

```python
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
```

### Update `base.html` to Load Bootstrap

```html
<!doctype html>
<html lang="en">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% block styles %}
        {{ bootstrap.load_css() }}   <!-- loads Bootstrap CSS -->
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <style>
            {% block styling %}{% endblock %}
        </style>
    {% endblock %}
    <title>{% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    {% block scripts %}
        {{ bootstrap.load_js() }}    <!-- loads Bootstrap JavaScript -->
    {% endblock %}
</body>
</html>
```

Now all your pages will have Bootstrap styling automatically.

---

## Bootstrap‑Flask Supports WTForms

The most powerful feature of Bootstrap‑Flask for forms is the `render_form()` macro. It takes a WTForms form object and generates the entire HTML – labels, inputs, validation messages, and CSRF token – all styled with Bootstrap.

### Using `render_form()`

1. **Import the macro** at the top of your template:
   ```html
   {% from 'bootstrap5/form.html' import render_form %}
   ```
2. **Replace your manual form code** with a single line:
   ```html
   {{ render_form(form) }}
   ```

Your `login.html` can now be as simple as:

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="container">
    <h1>Login</h1>
    {{ render_form(form) }}
</div>
{% endblock %}
```

That’s it! The macro handles everything, including error display and layout.

> **Why learn the manual way?**  
> `render_form` is a “black box” – it’s convenient, but if something goes wrong, you need to understand the underlying mechanics to debug. By first building forms manually, you gain that understanding and can then use shortcuts with confidence.

---

## Putting It All Together: The Secrets App

### Folder Structure

```
secrets_project/
├── static/
│   └── style.css          # custom global styles
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── success.html
│   └── denied.html
├── main.py
├── requirements.txt
└── .env                    # stores SECRET_KEY
```

### Key Files

**`main.py`** – full application with form definition and routes.
```python
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key')
bootstrap = Bootstrap(app)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@email.com' and form.password.data == '12345678':
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

**`templates/base.html`** – as shown in the Bootstrap‑Flask section.

**`templates/login.html`** – using `render_form`.
```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="container">
    <h1>Login</h1>
    {{ render_form(form) }}
</div>
{% endblock %}
```

**`templates/success.html`** and **`denied.html`** – simple pages extending `base.html`.

**`static/style.css`** – optional global customisations.

### Running the App

1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set a strong `SECRET_KEY` in your `.env` file.
4. Run `python main.py`.
5. Visit `http://127.0.0.1:5000`.

Try logging in with:
- Email: `admin@email.com`
- Password: `12345678`

You’ll be granted access to the secret page. Any other credentials will send you to the denied page.

---

## New Concepts Summary

| Concept | Description |
|---------|-------------|
| **Flask‑WTF** | Flask extension integrating WTForms, adds CSRF protection. |
| **WTForms** | Python library for form handling, validation, and rendering. |
| **FlaskForm** | Base class for your form classes (from Flask‑WTF). |
| **Field types** | `StringField`, `PasswordField`, `SubmitField`, etc. |
| **Validators** | Rules like `DataRequired`, `Email`, `Length`. |
| **CSRF token** | Hidden token that protects against cross‑site request forgery. |
| **`validate_on_submit()`** | Checks if request is POST and validation passed. |
| **Template inheritance** | `{% extends %}`, `{% block %}`, `{{ super() }}`. |
| **Bootstrap‑Flask** | Extension that provides Bootstrap helpers and the `render_form` macro. |
| **`render_form()`** | Macro that automatically renders a complete Bootstrap‑styled WTForm. |

---

## Final Thought

Mastering Flask‑WTF and template inheritance will dramatically speed up your Flask development. The combination of WTForms for back‑end logic and Bootstrap‑Flask for front‑end presentation gives you a professional, secure, and maintainable foundation for any web application.

Now go ahead and experiment – add more fields, try different validators, or customise the Bootstrap theme!