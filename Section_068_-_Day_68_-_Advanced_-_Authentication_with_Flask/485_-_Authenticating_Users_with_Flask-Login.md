## Authenticating Users with Flask-Login

### 1. Introduction

Currently, any user can navigate directly to `/secrets` or `/download` and access those pages, even without logging in. This defeats the purpose of having a protected area. To enforce that only authenticated (logged‑in) users can view certain pages, you need a way to track whether a user is logged in and to restrict access accordingly.

**Flask‑Login** is the most widely used extension for managing user sessions in Flask. It handles:

- Storing the user's ID in the session after login.
- Retrieving the user object from the database on each request (via a `user_loader` callback).
- Providing a `current_user` proxy that gives you access to the logged‑in user anywhere in your code or templates.
- Decorators like `@login_required` to protect routes.
- Helpers like `login_user()` and `logout_user()`.

By the end of this lesson, you will have integrated Flask‑Login, updated the registration and login flows to properly authenticate users, and secured the `/secrets` and `/download` routes so that only authenticated users can access them.

---

### 2. What Flask‑Login Does (and Doesn’t)

| Feature | What it provides |
|---------|------------------|
| **Session management** | Stores the user ID in the user's session after login. |
| **User loader** | A callback that loads a user object from the database given the user ID stored in the session. |
| **`current_user`** | A proxy that represents the logged‑in user. Available in routes and templates. |
| **`login_user()`** | Function to mark a user as authenticated for the current session. |
| **`logout_user()`** | Function to log out the user and clear the session. |
| **`@login_required`** | Decorator to protect routes – redirects unauthenticated users to the login page. |
| **`UserMixin`** | A mixin class that provides default implementations of the required methods (e.g., `is_authenticated`, `is_active`). |

Flask‑Login does **not**:

- Handle user registration or password verification.
- Provide a database or user model.
- Manage passwords (you already handle that with Werkzeug).

Your job is to integrate it with your existing user model and database.

---

### 3. Step‑by‑Step Implementation

Follow these steps in order. Each step builds on the previous one.

#### 3.1 Install Flask‑Login

Flask‑Login is already listed in your `requirements.txt`, but if not, install it:

```bash
pip install flask-login
```

#### 3.2 Configure Flask‑Login in `main.py`

Add the necessary imports and initialize the extension.

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Name of the login route – used for @login_required redirect
```

**Explanation:**

- `LoginManager` is the core class.
- `login_manager.init_app(app)` binds it to your Flask app.
- `login_manager.login_view` tells Flask‑Login which route to redirect to when a user tries to access a `@login_required` page but isn't logged in. Here we set it to `'login'` (the function name of the login route).

#### 3.3 Update the User Model with `UserMixin`

Your `User` class needs to inherit from `UserMixin`. This provides default implementations of methods like `is_authenticated`, `is_active`, etc. Flask‑Login expects these methods to exist.

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

**Note:** `UserMixin` must come **before** `db.Model` in the inheritance list. This is a standard Python multiple‑inheritance pattern.

#### 3.4 Create the `user_loader` Callback

Flask‑Login needs a way to load a user from the database given the user ID stored in the session. You provide this via a decorator.

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

This function receives a user ID as a string (from the session), converts it to an integer, and retrieves the corresponding `User` object from the database. It returns `None` if the user doesn't exist.

#### 3.5 Modify the Registration Route to Log Users In

After successfully creating a new user, you should automatically log them in using `login_user()`. This sets up the session so they are considered authenticated.

**Updated `/register` route:**

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists (we'll add flash messages later)
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))
        
        # Hash the password
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        login_user(new_user)
        
        # Redirect to secrets page (no need to pass name as query param)
        return redirect(url_for('secrets'))
    
    return render_template('register.html')
```

**Important changes:**

- Added a check for an existing email (will be enhanced with flash messages later).
- After committing the new user, we call `login_user(new_user)`.
- The redirect to `secrets` no longer needs a `name` query parameter because the secrets page can now access the user's name via `current_user`.

#### 3.6 Protect the Secrets Route with `@login_required`

Add the decorator to the `/secrets` route. Also modify the route to use `current_user` to get the user's name.

```python
@app.route('/secrets')
@login_required
def secrets():
    # current_user is set by Flask-Login and refers to the logged-in user
    return render_template('secrets.html', name=current_user.name)
```

**What happens:**

- If an unauthenticated user tries to visit `/secrets`, Flask‑Login intercepts the request and redirects them to the login page (as specified by `login_manager.login_view`).
- If the user is authenticated, the route executes normally, and we can access `current_user.name` to personalize the page.

#### 3.7 Protect the Download Route

Similarly, add `@login_required` to the `/download` route.

```python
@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')
```

Now, only logged‑in users can download the file.

#### 3.8 Implement the Login Route

The login route must:

1. Handle GET requests (render the login form).
2. Handle POST requests:
   - Retrieve email and password from the form.
   - Find the user by email.
   - Verify the password using `check_password_hash`.
   - If valid, call `login_user(user)` and redirect to the secrets page.
   - If invalid, show an error message (we'll use flash messages later).

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            # Password is correct – log the user in
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            # Invalid credentials – for now, just a simple message
            return "Invalid email or password. <a href='/login'>Try again</a>"
    
    return render_template('login.html')
```

**Explanation:**

- `user and check_password_hash(...)` ensures both that the user exists and that the password matches.
- `login_user(user)` creates the session and marks the user as authenticated.
- After login, redirect to the protected secrets page.

#### 3.9 Implement the Logout Route

The logout route simply calls `logout_user()` and redirects to the home page.

```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
```

Note: Even though this route is `@login_required`, it's fine because only logged‑in users should be able to log out. If an unauthenticated user somehow hits this route, they'll be redirected to the login page.

#### 3.10 Update the Secrets Template

Since you are now passing `name=current_user.name` from the route, the template can simply use `{{ name }}`:

```html
{% extends "base.html" %}
{% block title %}Secrets{% endblock %}
{% block content %}
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to the secret page. Only logged-in users can see this.</p>
    <a href="{{ url_for('download') }}">Download Your File</a>
{% endblock %}
```

#### 3.11 Update the Base Template to Use `current_user`

In `base.html`, you can now conditionally show/hide navigation links based on `current_user.is_authenticated`.

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
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

- `current_user` is automatically available in templates when Flask‑Login is installed.
- `current_user.is_authenticated` returns `True` if the user is logged in.

---

### 4. Testing the Complete Flow

1. **Run the application.**
2. **Visit the home page.** You should see Login and Register links.
3. **Register a new user.** After submission, you should be redirected to the secrets page, and the navigation bar should show **Logout** instead of Login/Register. The secrets page should greet you by name.
4. **Log out** by clicking the Logout link. You'll be redirected to the home page, and the navigation links return to Login/Register.
5. **Try to access `/secrets` directly** without logging in. You should be redirected to the login page.
6. **Log in** with the credentials you registered. You should be redirected to the secrets page.
7. **Click the download link** – the PDF should be served.
8. **Try to access `/download` directly** while logged out – you'll be redirected to login.

---

### 5. Important Concepts Explained

#### 5.1 The `user_loader` Callback

Flask‑Login stores only the user's ID in the session (specifically, in the Flask session cookie). On each request, Flask‑Login calls the `user_loader` function you provided, passing it the ID. Your function must return the corresponding user object (or `None`). Flask‑Login then makes that user available as `current_user`.

#### 5.2 `UserMixin`

`UserMixin` provides default implementations of four methods that Flask‑Login expects:

- `is_authenticated`: Returns `True` for a valid user (unless you override).
- `is_active`: Returns `True` if the account is active (you can override to check a flag).
- `is_anonymous`: Returns `False` for regular users.
- `get_id()`: Returns a string that uniquely identifies the user (Flask‑Login uses the `id` column by default).

By inheriting from `UserMixin`, you don't have to write these methods yourself.

#### 5.3 `login_user()`

This function takes a user object and optionally a "remember me" flag. It stores the user's ID in the session and optionally sets a cookie for persistent login. After calling it, `current_user` becomes that user for the remainder of the session.

#### 5.4 `@login_required`

A decorator that checks if `current_user.is_authenticated` is `True`. If not, it aborts the request and redirects to the login page (or returns a 401 error if you haven't set `login_view`). It must be placed **above** the route decorator.

#### 5.5 `current_user`

A proxy that represents the logged‑in user. It is available in both routes and templates. If no user is logged in, `current_user` is an `AnonymousUser` object (which also has an `is_authenticated` property returning `False`).

---

### 6. Potential Issues and Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| `@login_required` redirects to the wrong page | `login_manager.login_view` not set or set incorrectly | Ensure it is set to the name of your login route function, e.g., `'login'`. |
| `current_user` is always an anonymous user | User not properly logged in, or `user_loader` not returning the user | Check that `login_user(user)` is called. Verify `user_loader` returns the correct user. |
| AttributeError: 'User' object has no attribute 'is_active' | `User` class does not inherit from `UserMixin` | Add `UserMixin` to the inheritance list. |
| Session errors or `secret_key` warnings | `SECRET_KEY` not set | Set `app.config['SECRET_KEY']` to a random string. |
| `check_password_hash` returns `False` even with correct password | Password hashing method mismatch | Ensure you used the same method and salt length as when hashing. |

---

### 7. Complete Code for `main.py` (After This Lesson)

Here is the consolidated `main.py` with all the changes from this lesson and previous ones:

```python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered. <a href='/login'>Login</a>"
        
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('secrets'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            return "Invalid email or password. <a href='/login'>Try again</a>"
    
    return render_template('login.html')

@app.route('/secrets')
@login_required
def secrets():
    return render_template('secrets.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')

if __name__ == '__main__':
    app.run(debug=True)
```

---

### 8. Next Steps

You now have a fully functional authentication system:

- Passwords are securely hashed and salted with Werkzeug.
- Flask‑Login manages user sessions.
- The secrets page and download route are protected.
- Users can register, log in, and log out.

In the next lesson, you will enhance the user experience by adding **flash messages** to provide feedback for errors like duplicate registration or incorrect login attempts. You will also learn how to conditionally show/hide elements in templates based on login status.