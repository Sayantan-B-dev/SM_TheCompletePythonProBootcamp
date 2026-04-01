## 491 - Requirement 2 - Login Registered Users

This document details the implementation of user login functionality for the blog project. Building upon the user registration system, this phase introduces session management using Flask-Login, allowing registered users to authenticate, maintain their login state across requests, and access protected features. The implementation covers login form creation, session handling, conditional UI updates, and logout functionality, all while integrating with the existing database and form structures.

### Overview

The login system requires several interconnected components to function correctly:

- **Flask-Login configuration**: Setting up the `LoginManager` and the `user_loader` callback to manage user sessions.
- **Login form**: A WTForm to collect email and password, with validation.
- **Login route (`/login`)**: Handling both GET (display form) and POST (authenticate user) requests.
- **Integration with registration**: Automatically logging in users upon successful registration.
- **Error handling**: Providing informative flash messages for various failure scenarios (duplicate email, invalid credentials).
- **Conditional navigation**: Updating the navigation bar to reflect the user's authentication state.
- **Logout route (`/logout`)**: Clearing the user session and redirecting to the home page.

The primary reference for Flask-Login functionality is the official documentation at [Flask-Login#Login Example](https://flask-login.readthedocs.io/en/latest/#login-example), which provides the foundational patterns used throughout this implementation.

### Prerequisites

Before proceeding, ensure the following are in place:

- User registration is fully implemented and functional (see document 490).
- The `User` model exists with `set_password` and `check_password` methods.
- The `blog.db` database contains at least one registered user for testing.
- Flask-Login is installed (`pip install flask-login`) and imported in `main.py`.
- The application's `SECRET_KEY` is properly configured (required for session security).

### Step 1: Configure Flask-Login and User Loader

The first task is to initialize Flask-Login and define how to load a user from the session. This setup is typically placed near the top of `main.py`, after creating the Flask app instance.

**Example: LoginManager configuration in main.py**

```python
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-strong-secret-key-here'  # Replace with a secure key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configure login view (where to redirect unauthorized users)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in the session."""
    return User.query.get(int(user_id))
```

**Explanation**:

- `LoginManager` is the core object that coordinates the extension.
- `init_app(app)` binds the manager to the Flask application.
- `login_view` specifies the endpoint name (the function name of the login route) to redirect to when a user tries to access a `@login_required` page without being authenticated.
- `login_message` and `login_message_category` customize the flash message shown upon redirection.
- The `user_loader` callback is essential: it takes a `user_id` (stored in the session) and returns the corresponding `User` object. Flask-Login uses this to populate `current_user` for every request. If the user ID is invalid, it returns `None`, and the session is cleared.

### Step 2: Create the Login Form

In `forms.py`, define a `LoginForm` class. This form will collect the user's email and password, and optionally a "remember me" checkbox.

**Example: LoginForm in forms.py**

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Optional: persists login across browser restarts
    submit = SubmitField('Log In')
```

**Explanation**:

- `DataRequired()` ensures the fields are not left empty.
- `Email()` validates the email format.
- `BooleanField('Remember Me')` renders as a checkbox; when checked, `login_user` will be called with `remember=True`, setting a long-lived cookie.
- The submit button triggers form submission.

### Step 3: Implement the Login Route

The `/login` route must handle both GET requests (displaying the form) and POST requests (processing login attempts). The logic follows a standard pattern: instantiate the form, validate on submit, check credentials against the database, and either log the user in or show an error.

**Example: Login route in main.py**

```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user
from forms import LoginForm
from models import User  # Adjust import as needed

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Verify user exists and password matches
        if user and user.check_password(form.password.data):
            # Log the user in
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')

            # Handle 'next' parameter for redirecting to originally requested page
            next_page = request.args.get('next')
            if next_page and url_has_allowed_host_and_scheme(next_page, request.host):
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            # Invalid credentials
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    # GET request or failed validation
    return render_template('login.html', form=form)
```

**Key points**:

- `form.validate_on_submit()` handles both POST detection and WTForm validation.
- `User.query.filter_by(email=...).first()` retrieves the user by email. Using `filter_by` is more concise than `where()` clauses in raw SQL.
- `check_password()` is the method defined on the `User` model that uses Werkzeug to compare the plaintext password with the stored hash.
- `login_user()` from Flask-Login creates the session for the user. Passing `remember=form.remember.data` enables persistent login if the checkbox was checked.
- The `next` parameter handling is critical for security: after login, users should be redirected to the page they originally tried to access (if any). The `url_has_allowed_host_and_scheme` function (which you must define or import) prevents open redirect vulnerabilities by ensuring the next URL is safe. A simple implementation can check that the next path is relative (starts with `/`) and does not contain external schemes. For production, consider using a library or Django's implementation referenced in the Flask-Login docs.
- Flash messages use categories (`'success'`, `'danger'`) that can be styled in templates with Bootstrap.

**Security note on the `next` parameter**:
The Flask-Login documentation warns: "You MUST validate the value of the `next` parameter. If you do not, your application will be vulnerable to open redirects." A minimal safe check is:

```python
def url_has_allowed_host_and_scheme(url, allowed_host):
    # Simple check: ensure the URL is relative (starts with '/') and not external
    return url.startswith('/') and not url.startswith('//') and '\\' not in url
```

### Step 4: Update Registration Route to Auto-Login

Requirement 2.2 specifies that after successful registration, the user should be automatically logged in and redirected to the home page. This eliminates an extra step for new users.

**Modified /register route in main.py**

```python
from flask_login import login_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with that email already exists. Please log in instead.', 'info')
            return redirect(url_for('login'))

        # Create new user
        new_user = User(
            name=form.name.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the new user
        login_user(new_user)
        flash('Registration successful! Welcome to the blog.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
```

**Changes**:

- After committing the new user, `login_user(new_user)` is called, establishing a session for them.
- The success flash message is updated to welcome the user.
- The redirect now goes directly to `home` instead of the login page.

### Step 5: Handle Duplicate Email During Registration

Requirement 2.3 expands on the duplicate email handling: if a user tries to register with an email that already exists, they are redirected to the login page with a flash message prompting them to log in instead. This logic is already present in the modified registration route above (the `if existing_user:` block). The flash message uses class `"flash"` as requested, but for Bootstrap styling we typically use categories like `'info'` and then render them appropriately.

### Step 6: Implement Error Handling in Login Route

Requirement 2.4 requires that if the email does not exist or the password is incorrect, the user is redirected back to the login page with a flash message explaining the issue. This is also already implemented in the login route (the `else` block after credential checking). The flash message category `'danger'` will be used to style the error message.

### Step 7: Update Login Template to Display Flash Messages

To display flash messages, the `login.html` template must include code to iterate over flashed messages and render them. Using Bootstrap-Flask's `render_form()` macro does not automatically include flash rendering, so we add it manually.

**Example: login.html with flash messages**

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Log In{% endblock %}

{% block content %}
<div class="container">
    <h1>Log In</h1>

    <!-- Flash messages section -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {{ render_form(form) }}
</div>
{% endblock %}
```

**Explanation**:

- `get_flashed_messages(with_categories=true)` retrieves all queued flash messages along with their categories.
- Bootstrap's alert classes (`alert-success`, `alert-danger`, etc.) correspond to the categories we used (`'success'`, `'danger'`, `'info'`).
- The dismiss button allows users to close the message.

This same flash-rendering code should be added to `register.html` and any other templates where flash messages may appear.

### Step 8: Update Navigation Bar Based on Authentication State

Requirement 2.5 involves updating the navigation bar (located in `header.html`) to show different links depending on whether the user is authenticated. Flask-Login makes the `current_user` proxy available in all templates.

**Example: Conditional navbar in header.html**

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('home') }}">My Blog</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('home') }}">Home</a>
                </li>
                {% if current_user.is_authenticated %}
                    <!-- Links for logged-in users -->
                    <li class="nav-item">
                        <span class="nav-link">Welcome, {{ current_user.name }}!</span>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('logout') }}">Log Out</a>
                    </li>
                {% else %}
                    <!-- Links for guests -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('login') }}">Log In</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('register') }}">Register</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

**Explanation**:

- `current_user.is_authenticated` is a property provided by Flask-Login (via `UserMixin`) that returns `True` for logged-in users.
- For authenticated users, we display a welcome message with their name (pulled from the database) and a "Log Out" link.
- For unauthenticated users, we show "Log In" and "Register" links.
- The `ms-auto` class pushes the nav items to the right (Bootstrap utility).

### Step 9: Implement the Logout Route

Requirement 2.6 is straightforward: the `/logout` route should log the user out using Flask-Login's `logout_user()` function and redirect to the home page. The route should be protected with `@login_required` to ensure only authenticated users can access it (though calling `logout_user` on an anonymous user is harmless).

**Example: Logout route in main.py**

```python
from flask_login import logout_user, login_required

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))
```

**Explanation**:

- `@login_required` ensures that if an unauthenticated user somehow navigates to `/logout`, they are redirected to the login page (as configured by `login_manager.login_view`).
- `logout_user()` removes the authentication information from the session.
- A flash message confirms the logout.
- Redirect to home page.

### Complete Integration and Testing

After implementing all steps, the authentication system should function as follows:

1. **New user registration**: User fills out registration form → account created → automatically logged in → redirected to home page with welcome message. Navbar shows welcome message and logout link.
2. **Duplicate registration attempt**: User tries to register with existing email → redirected to login page with flash message "An account with that email already exists. Please log in instead."
3. **Successful login**: User provides correct credentials → logged in → redirected to home (or originally requested page) with success flash. Navbar updates accordingly.
4. **Failed login**: User provides incorrect email/password → redirected back to login page with error flash message.
5. **Logout**: User clicks "Log Out" → logged out → redirected to home with confirmation flash. Navbar reverts to guest links.
6. **Protected route access**: If an unauthenticated user tries to access a page that requires login (e.g., comment submission), they are redirected to the login page with a flash message "Please log in to access this page." After successful login, they are redirected back to the original page.

**Testing Checklist**:

- Verify that all routes respond correctly with both GET and POST methods.
- Test login with both correct and incorrect credentials.
- Test the "Remember Me" functionality by closing and reopening the browser; the user should remain logged in.
- Ensure the `next` parameter works safely: try accessing a protected page (like `/post/1/comment` directly) while logged out; you should be redirected to login, and after logging in, you should be sent back to that page.
- Confirm that flash messages appear with appropriate styling.
- Check that the navbar updates immediately after login/logout without requiring a manual page refresh (session changes are reflected on the next request).

### Troubleshooting Common Issues

- **`login_user` not persisting**: Ensure `SECRET_KEY` is set and consistent. If the key changes between requests, sessions become invalid.
- **`user_loader` not called or returns `None`**: Verify that the `user_id` stored in the session matches the type expected by `User.query.get()`. If your user IDs are integers, convert as shown. Also check that the `load_user` function is properly decorated and placed where Flask can find it.
- **`current_user.is_authenticated` always `False`**: Confirm that your `User` class inherits from `UserMixin` or implements the required properties and methods.
- **Flash messages not appearing**: Ensure you have the flash rendering code in your template and that you are calling `flash()` before the template is rendered (usually in the route before redirecting or rendering).
- **Redirect loop after login**: This can happen if the login route itself requires login. Ensure the login route is **not** decorated with `@login_required`.
- **`next` parameter causing security errors**: Always validate the next URL. A simple check is to allow only relative paths starting with `/` and disallowing external schemes.

### Summary

This implementation phase transforms the blog from a static site into a dynamic platform with user accounts. Key takeaways include:

- Flask-Login abstracts session management, providing `login_user`, `logout_user`, `current_user`, and `@login_required`.
- The `user_loader` callback is essential for Flask-Login to retrieve user objects from the database based on session IDs.
- Password security is maintained through Werkzeug's hashing functions; the login process uses `check_password` to verify credentials without ever storing or comparing plaintext passwords.
- Flash messages combined with Bootstrap alerts give immediate feedback to users.
- Conditional rendering in templates using `current_user.is_authenticated` personalizes the UI.

With these features in place, the blog is ready for the next phase: integrating users with comments and implementing authorization rules (e.g., only logged-in users can comment, and users can only edit/delete their own comments). The foundation for community interaction is now complete.

**Resource Links**:

- Flask-Login Documentation (Login Example): [https://flask-login.readthedocs.io/en/latest/#login-example](https://flask-login.readthedocs.io/en/latest/#login-example)
- Flask-Login API Reference: [https://flask-login.readthedocs.io/en/latest/#flask_login.login_user](https://flask-login.readthedocs.io/en/latest/#flask_login.login_user)
- Werkzeug Security Utilities: [https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security](https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security)
- Bootstrap Alerts: [https://getbootstrap.com/docs/5.0/components/alerts/](https://getbootstrap.com/docs/5.0/components/alerts/)

By completing these steps, the blog now features a complete user authentication system, ready for deeper integration with content and comments.