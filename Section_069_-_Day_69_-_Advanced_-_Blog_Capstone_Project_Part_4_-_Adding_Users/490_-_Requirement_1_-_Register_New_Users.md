## 490 - Requirement 1 - Register New Users

This document details the implementation of the first requirement for adding user authentication to the blog project: enabling new users to register by creating an account. The goal is to allow visitors to navigate to the `/register` route, complete a registration form, and have their information securely stored in the database. At this stage, the focus is solely on creating a user record; session management and automatic login will be handled in subsequent steps.

### Overview

The registration process involves several interconnected components:

- A database table (`users`) to store user credentials and profile information.
- A web form (built with Flask-WTF) to collect user input: name, email, and password.
- A route (`/register`) that handles both displaying the form (GET) and processing the submitted data (POST).
- Secure password handling using Werkzeug’s hashing utilities to ensure passwords are never stored in plain text.
- Integration with Bootstrap-Flask to render the form with consistent styling.

Upon successful completion of this step, the application will be able to persist new user records, laying the foundation for later authentication and authorization features.

### Prerequisites

Before proceeding, ensure the following are in place:

- The starting project is correctly set up and runs without errors (see document 489).
- The virtual environment is activated and all required packages are installed (Flask, Flask-SQLAlchemy, Flask-WTF, Werkzeug, Bootstrap-Flask, etc.).
- The `forms.py` file exists and is importable.
- The `blog.db` SQLite database is accessible and can be modified.

### Step 1: Define the User Model

The first task is to create a `User` model that maps to a database table. This model will define the columns and relationships for user data. Open the file where your database models are defined (commonly `main.py` or a separate `models.py`). For clarity, we will assume the models reside in `main.py` alongside the Flask app and SQLAlchemy `db` object.

**Example: Adding the User model**

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    # Optional: Define a relationship to comments (will be added later)
    # comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password):
        """Convert plaintext password to a hash and store it."""
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        """Verify that the given password matches the stored hash."""
        return check_password_hash(self.password, password)
```

**Explanation of each field**:

- `id`: An auto-incrementing integer that uniquely identifies each user.
- `email`: The user's email address. Marked `unique=True` to prevent duplicate accounts. `nullable=False` ensures every user must provide an email.
- `password`: Stores the hashed password. Even though the field name is `password`, it will never contain the original plaintext password.
- `name`: The user's display name (or full name). This will be shown next to their comments.

The `set_password` and `check_password` methods encapsulate the hashing logic and will be used when creating a new user and later during login.

After defining the model, you must create the corresponding table in the database. If you have not yet created the database tables, run the following in a Python shell or add a one-time setup block:

```python
with app.app_context():
    db.create_all()
```

Alternatively, you can simply restart the application if the table creation is triggered automatically (common when using `db.create_all()` inside the main script). If the `blog.db` file already exists, this command will create the new `users` table without affecting existing tables.

### Step 2: Create the Registration Form

Flask-WTF provides an easy way to define forms as Python classes. In `forms.py`, create a new class called `RegisterForm`. This form will include fields for name, email, password, and a submit button. Additionally, we will add validators to ensure required fields are filled and that the email format is correct.

**Example: RegisterForm in forms.py**

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Sign Up')
```

**Explanation of validators**:

- `DataRequired()`: Ensures the field is not submitted empty.
- `Email()`: Checks that the input follows a valid email format.
- `Length(min=8)`: Enforces a minimum password length for security.
- `EqualTo('password')`: Verifies that the confirmation password matches the original.

The `confirm_password` field is a common UX pattern to catch typos during registration. The `EqualTo` validator automatically compares its value with the field named `password`.

### Step 3: Implement the /register Route

In `main.py`, create a new route `/register` that accepts both GET and POST requests. The logic inside the route must:

1. Instantiate the registration form.
2. On GET request, render the template with the form.
3. On POST request, validate the form data.
4. If validation passes, check whether a user with the given email already exists in the database.
5. If the email is available, create a new `User` object, hash the password using `set_password()`, and add it to the database.
6. After successful creation, redirect the user to the login page (or homepage). For now, we will redirect to the login page, as the user is not automatically logged in.
7. If validation fails or the email is taken, re-render the form with appropriate error messages.

**Example: /register route**

```python
from flask import render_template, redirect, url_for, flash
from forms import RegisterForm
from models import User, db  # Adjust import according to your project structure

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with that email already exists. Please log in instead.')
            return redirect(url_for('login'))

        # Create new user instance
        new_user = User(
            name=form.name.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)  # Hash the password

        # Add to database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    # For GET requests or failed validation, render the form
    return render_template('register.html', form=form)
```

**Key points**:

- `form.validate_on_submit()` returns `True` only on POST requests and when all validators pass. This simplifies the logic significantly.
- The email uniqueness check is performed manually because the database constraint (`unique=True`) would raise an integrity error if violated. Handling it manually allows a user-friendly flash message.
- After committing the new user, a flash message informs the user of success and redirects to the login page. (The login route will be implemented later.)
- If validation fails, the form is re-rendered with error messages automatically displayed (provided the template shows them).

### Step 4: Hash the Password with Werkzeug

The `set_password` method defined in the `User` class uses `werkzeug.security.generate_password_hash`. It is crucial to understand why hashing is necessary and how it works.

**Why hashing?**  
Storing passwords in plain text is a severe security risk. If the database is compromised, all user passwords are exposed. Hashing converts the password into a fixed-length string that cannot be reversed to obtain the original password. When a user later attempts to log in, the provided password is hashed again and compared to the stored hash.

**How Werkzeug's hashing works**:

- `generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)` takes the plaintext password and:
  - Generates a random salt (a string of random characters) of the specified length.
  - Applies the PBKDF2 algorithm with SHA256 hash function, iterating many times to slow down brute-force attacks.
  - Returns a single string that contains the algorithm, iteration count, salt, and the resulting hash. This string can be stored directly in the database.

- `check_password_hash(hashed_password, plain_password)` extracts the salt and algorithm from the stored hash, hashes the provided plaintext password with the same parameters, and compares the results.

By using these methods, the application never handles plaintext passwords after they are hashed.

### Step 5: Render the Form with Bootstrap-Flask

The project uses Bootstrap-Flask to render forms with consistent Bootstrap styling. In the `register.html` template, we will use the `render_form()` macro to output the entire form.

**Ensure Bootstrap-Flask is installed and initialized**:

- If not already present, install it: `pip install bootstrap-flask`.
- In `main.py`, initialize the extension:
  ```python
  from flask_bootstrap import Bootstrap5
  bootstrap = Bootstrap5(app)
  ```

**Creating the register.html template**:

If the template does not exist, create it inside the `templates` folder. It should extend a base layout (usually `base.html`) and import the Bootstrap-Flask macros.

**Example: register.html**

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="container">
    <h1>Create an Account</h1>
    {{ render_form(form) }}
</div>
{% endblock %}
```

The `render_form(form)` macro automatically renders all fields, labels, validation errors, and the submit button with appropriate Bootstrap classes. It also includes the CSRF token hidden field.

**Customization**:

If you need to customize the form layout (e.g., add extra text, or style the button), you can use the macro's parameters or manually render fields. For now, the default rendering is sufficient.

### Step 6: Testing the Registration

After implementing the above, run the application and navigate to `http://127.0.0.1:5000/register`. You should see a styled form with fields for Name, Email, Password, Confirm Password, and a Sign Up button.

**Test scenarios**:

1. **Valid submission**: Fill out all fields correctly and submit. You should be redirected to the login page with a flash message "Registration successful! Please log in."
2. **Duplicate email**: Attempt to register again with the same email. The form should detect the existing user and redirect to login with a flash message.
3. **Validation errors**: Try submitting an empty form, an invalid email, a short password, or mismatched passwords. The form should re-render with error messages next to the relevant fields.
4. **Database verification**: Use DB Browser for SQLite to open `blog.db` and inspect the `users` table. You should see the new user record with a hashed password (a long string starting with `pbkdf2:sha256:...`).

### Troubleshooting

- **Form not rendering**: Ensure `bootstrap5/form.html` is imported correctly and that the `render_form` macro is used. Check that Bootstrap-Flask is installed and initialized.
- **CSRF token errors**: Flask-WTF requires a secret key. Verify that `app.config['SECRET_KEY']` is set in your main application. If missing, add a random string.
- **IntegrityError when creating user**: If the email uniqueness constraint is violated and you haven't manually checked for existing users, the database will raise an error. Use a try/except block or pre-check as shown.
- **Password not hashed**: Ensure you call `new_user.set_password(form.password.data)` before adding the user to the session. Do not assign the plaintext password directly to `new_user.password`.
- **Module not found**: Double-check imports: `from forms import RegisterForm`, `from main import db, User` (adjust based on your file structure).

### Next Steps

With user registration working, the next requirement is to allow registered users to log in. This will involve:

- Creating a login form.
- Implementing the `/login` route.
- Using Flask-Login to manage user sessions.
- Protecting certain routes (e.g., comment submission) with login requirements.

The foundation laid here ensures that user credentials are stored securely, ready for authentication.

**Resource Links**:
- Flask-WTF documentation: [https://flask-wtf.readthedocs.io/](https://flask-wtf.readthedocs.io/)
- WTForms validators: [https://wtforms.readthedocs.io/en/3.1.x/validators/](https://wtforms.readthedocs.io/en/3.1.x/validators/)
- Werkzeug password hashing: [https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security](https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security)
- Bootstrap-Flask: [https://bootstrap-flask.readthedocs.io/](https://bootstrap-flask.readthedocs.io/)

By following this guide, you have successfully implemented the first requirement: allowing new users to register on your blog. This is a critical step toward building a community‑driven platform.