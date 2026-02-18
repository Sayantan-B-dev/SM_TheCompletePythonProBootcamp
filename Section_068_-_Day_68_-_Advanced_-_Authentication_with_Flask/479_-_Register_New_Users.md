## Register New Users

### 1. Overview

The first step in building an authentication system is to allow new users to create an account. In this lesson, you will take the data submitted through the registration form (`register.html`), create a new `User` object, and save it to the `users.db` database. After successful registration, the user will be automatically redirected to the `secrets.html` page, where they will be greeted by name.

At this stage, we will store the password as **plain text** to keep things simple and focus on the registration flow. In later lessons, you will replace this with secure password hashing.

### 2. Understanding the Registration Form

The `register.html` template contains a form that submits a POST request to the `/register` URL. The form includes three input fields:

- `name` – the user’s full name
- `email` – the user’s email address (must be unique)
- `password` – the user’s chosen password

Here is the relevant part of `register.html`:

```html
<form method="POST" action="{{ url_for('register') }}">
    <input type="text" name="name" placeholder="Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Register</button>
</form>
```

- `method="POST"` indicates that the form data will be sent in the body of the HTTP request, not as URL parameters.
- `action="{{ url_for('register') }}"` means the form will be submitted to the same route (`/register`) that rendered the form. This is a common pattern: the same route handles both displaying the form (GET) and processing the submission (POST).

### 3. Modifying the Register Route

Currently, the `/register` route in `main.py` only handles GET requests and renders the form. We need to extend it to also accept POST requests and process the form data.

#### Step 3.1: Import Required Modules

At the top of `main.py`, ensure you have imported the necessary modules from Flask:

```python
from flask import Flask, render_template, request, redirect, url_for
```

- `request` allows us to access the form data.
- `redirect` and `url_for` will be used to send the user to the secrets page after registration.

#### Step 3.2: Modify the Route to Handle POST

Update the `/register` route as follows:

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # TODO: Add validation (e.g., check if email already exists)
        
        # Create a new User object
        new_user = User(
            name=name,
            email=email,
            password=password  # Stored as plaintext for now
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to secrets page (we'll pass the user's name)
        return redirect(url_for('secrets', name=name))
    
    # If GET request, just render the registration form
    return render_template('register.html')
```

**Explanation:**

- The `methods` parameter now includes both `GET` and `POST`.
- Inside the `if request.method == 'POST'` block, we extract form data using `request.form.get('field_name')`. This returns the value as a string, or `None` if the field is missing.
- A new `User` instance is created with the submitted data. The `password` is stored exactly as entered (plaintext). **This is insecure and will be fixed later.**
- The user is added to the database session and committed. If the email is not unique, SQLAlchemy will raise an integrity error. For now, we ignore error handling; we'll add flash messages in a later lesson.
- After saving, we redirect to the `secrets` route, passing the user's name as a query parameter (`name=name`). This will allow the secrets page to greet the user personally.

#### Step 3.3: Pass the Name to the Secrets Page

The `secrets` route currently just renders `secrets.html`. We need to modify it to accept the `name` parameter from the URL and pass it to the template.

Update the `/secrets` route:

```python
@app.route('/secrets')
def secrets():
    name = request.args.get('name')
    return render_template('secrets.html', name=name)
```

- `request.args.get('name')` retrieves the `name` query parameter from the URL.
- We pass `name=name` to the template, where it will be available as the variable `name`.

### 4. Updating the Secrets Template

The `secrets.html` template already contains a placeholder `{{ name }}`. Ensure it looks like this:

```html
{% extends "base.html" %}
{% block title %}Secrets{% endblock %}
{% block content %}
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to the secret page. Only logged-in users can see this.</p>
    <a href="{{ url_for('download') }}">Download Your File</a>
{% endblock %}
```

When the user is redirected after registration, the `name` variable will be populated, and the greeting will display correctly (e.g., "Hello, John!").

### 5. Testing the Registration Flow

1. Run the Flask application (`main.py`).
2. Navigate to `http://127.0.0.1:5000/register`.
3. Fill in the form with a name, email, and password.
4. Click **Register**.

**Expected behavior:**

- The form submits, and you are redirected to `http://127.0.0.1:5000/secrets?name=John` (if name is "John").
- The secrets page displays "Hello, John!" and the download link.
- Open the `users.db` database with a tool like DB Browser for SQLite. You should see a new row in the `users` table with the entered name, email, and the plaintext password.

### 6. Important Considerations

#### 6.1 Plaintext Passwords (Temporary)

At this point, the password is stored exactly as the user typed it. This is a severe security risk. Do not deploy this code to a production server. We will replace it with hashed passwords using Werkzeug in a later lesson.

#### 6.2 Duplicate Email Addresses

If a user registers with an email that already exists in the database, SQLAlchemy will raise an `IntegrityError` because the `email` column has a `unique=True` constraint. The application will crash with a 500 error. In a future lesson, we will catch this error and display a friendly flash message, redirecting the user to the login page with an appropriate notification.

#### 6.3 Missing Fields

If any form field is left empty, the `request.form.get()` will return an empty string or `None`. We are not validating this, which could lead to incomplete user records. For now, the HTML `required` attribute on the input fields provides basic client-side validation, but server-side validation is always necessary for security and reliability. We will add validation later.

### 7. Code Summary

After completing this lesson, your `main.py` should include the following relevant parts:

```python
from flask import Flask, render_template, request, redirect, url_for
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

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        new_user = User(
            name=name,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('secrets', name=name))
    
    return render_template('register.html')

@app.route('/secrets')
def secrets():
    name = request.args.get('name')
    return render_template('secrets.html', name=name)

# ... other routes (login, logout, download) will be added later
```

### 8. Next Steps

You have successfully implemented user registration and database storage. In the next lesson, you will create the `/download` route to allow authenticated users to download the secret PDF file. After that, you will learn about encryption and hashing to secure passwords properly.