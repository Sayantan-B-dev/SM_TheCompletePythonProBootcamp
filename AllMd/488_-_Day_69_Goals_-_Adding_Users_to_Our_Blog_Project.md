## Day 69 Goals - Adding Users to Our Blog Project

This document outlines the final development phase for the Blog Capstone Project: integrating a complete user authentication and authorization system. The objective is to transform the existing blog from a single-author publication into a multi-user platform where visitors can register, log in, and interact with content through comments. This phase establishes the foundation for community engagement and prepares the application for public launch.

### Core Conceptual Model

The implementation centers on three primary entities: **Users**, **Posts**, and **Comments**. The relationships between these entities define the application's functionality. A User can create multiple Comments. Each Comment belongs to a single User and a single Post. This creates a one-to-many relationship between Users and Comments, and a one-to-many relationship between Posts and Comments. Administrators may retain the ability to create Posts, while registered Users gain the ability to create Comments associated with their account.

### Feature Set and Functional Requirements

**User Registration and Account Management**

The system must allow new visitors to create an account. This requires a registration form capturing essential information such as username, email address, and password. The email address serves as a unique identifier for login and potential account recovery. Password security is paramount; therefore, plain-text passwords must never be stored. The system will implement a hashing algorithm to transform submitted passwords into irreversible, secure strings before database insertion.

**User Authentication and Session Management**

Registered users must be able to authenticate themselves by providing their credentials (email and password) through a login form. Upon successful verification of the credentials against the stored hash, the system establishes a persistent session. This session allows the application to recognize the user across multiple page requests without requiring repeated login. The session typically expires after a defined period of inactivity or upon explicit user logout.

**Authorization and Access Control**

Once a user is authenticated, the system must enforce authorization rules. This determines which actions a user is permitted to perform. For this project, the primary authorization rule is: **only authenticated users may post comments**. Unauthenticated visitors may view posts and comments but are prohibited from submitting new comments. Additionally, users should only be able to edit or delete their own comments, not those belonging to other users. Administrators may retain global editing and deletion privileges across all content.

**Role-Based Access Control for Content Creation**

A distinction must be made between standard registered users and blog authors or administrators. While all registered users can comment, the ability to create, edit, and delete blog posts should likely remain restricted to a specific set of administrative users. This can be implemented by assigning a role attribute to each user, such as 'admin' or 'author'. The system then checks this role before granting access to post-creation endpoints and interface elements.

### Database Schema Modifications

Integrating users requires modifications to the existing database schema. The following tables represent the necessary structure.

**Users Table**

This table stores all information related to registered users. Each user is uniquely identified by a primary key, typically an auto-incrementing integer.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for each user. |
| `username` | String (e.g., VARCHAR(250)) | Unique, Not Null | The user's chosen display name. |
| `email` | String (e.g., VARCHAR(250)) | Unique, Not Null | The user's email address, used for login. |
| `password` | String (e.g., VARCHAR(250)) | Not Null | The securely hashed password string. |
| `name` | String (e.g., VARCHAR(250)) | Nullable | Optional field for the user's real name. |
| `about` | Text | Nullable | Optional biographical information. |
| `role` | String (e.g., VARCHAR(50)) | Default: 'subscriber' | Defines user permissions (e.g., 'admin', 'author', 'subscriber'). |

**Comments Table (Modified)**

The existing comments table requires an additional foreign key column to link each comment to the user who authored it. The previous commenter name and email fields become redundant, as this information is now sourced from the associated user record.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for each comment. |
| `text` | Text | Not Null | The content of the comment. |
| `date` | DateTime | Not Null | Timestamp of when the comment was posted. |
| `post_id` | Integer | Foreign Key referencing `posts.id` | Identifies the post to which the comment belongs. |
| `author_id` | Integer | Foreign Key referencing `users.id` | Identifies the user who wrote the comment. |

### Technical Implementation Strategy: Flask and Flask-Login

For a Flask-based application, the Flask-Login extension provides the standard mechanism for managing user sessions. The implementation process follows a structured pattern.

**Step 1: Install Required Extensions**

The project dependencies must be updated to include Flask-Login and Werkzeug's security utilities for password hashing.

```bash
pip install flask-login
pip install werkzeug  # Often installed with Flask, but ensure it's present
```

**Step 2: Configure the User Model**

The User model must be defined to work with Flask-Login. It requires specific methods for session management. The easiest approach is to inherit from `UserMixin`, which provides default implementations for these methods. The database model is defined using an ORM like Flask-SQLAlchemy.

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship to comments: a user can have many comments
    comments = db.relationship("Comment", back_populates="author")

    def set_password(self, password):
        """Create a hashed password and store it."""
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    # Foreign key linking to the user who wrote it
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Foreign key linking to the post it belongs to
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Relationships
    author = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")
```

**Step 3: Initialize Flask-Login**

In the main application factory or creation script, the LoginManager extension is initialized and configured.

```python
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Essential for session security

login_manager = LoginManager()
login_manager.init_app(app)

# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Step 4: Create Registration Route and Form**

A route is created to handle GET requests (displaying the registration form) and POST requests (processing the form submission).

```python
from flask import render_template, redirect, url_for, flash
from forms import RegistrationForm  # Assume a Flask-WTF form is defined

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash('Email address already registered. Please log in.')
            return redirect(url_for('login'))

        # Create new user
        new_user = User(
            email=form.email.data,
            name=form.name.data
        )
        new_user.set_password(form.password.data)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        # Log the user in immediately after registration
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
```

**Step 5: Create Login Route and Form**

The login route authenticates the user and establishes the session.

```python
from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Verify user exists and password is correct
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data) # remember_me is optional
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)
```

**Step 6: Protect Routes with Login Requirement**

Routes that require authentication use the `@login_required` decorator. For example, the route that processes new comment submissions should be protected.

```python
from flask_login import login_required

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    # Logic to create and save a new comment, 
    # associating it with the currently logged-in user (current_user)
    comment_text = request.form.get('comment_text')
    post = Post.query.get_or_404(post_id)
    
    new_comment = Comment(
        text=comment_text,
        created_at=datetime.utcnow(),
        author_id=current_user.id,
        post_id=post.id
    )
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('show_post', post_id=post.id))
```

**Step 7: Template Integration and Conditional Rendering**

Templates must be updated to reflect the user's authentication state. This involves checking `current_user.is_authenticated`.

```html
<!-- Example in a base layout file (e.g., base.html) -->
<nav>
    <!-- ... other nav items ... -->
    <div>
        {% if current_user.is_authenticated %}
            <span>Welcome, {{ current_user.name }}!</span>
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </div>
</nav>
```

```html
<!-- Example on a blog post page -->
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>

<h2>Comments</h2>
{% for comment in post.comments %}
    <div>
        <strong>{{ comment.author.name }}</strong> said on {{ comment.created_at }}:
        <p>{{ comment.text }}</p>
    </div>
{% endfor %}

{% if current_user.is_authenticated %}
    <h3>Leave a Comment</h3>
    <form method="POST" action="{{ url_for('add_comment', post_id=post.id) }}">
        {{ comment_form.hidden_tag() }} <!-- For CSRF protection -->
        {{ comment_form.text.label }} {{ comment_form.text() }}
        <input type="submit" value="Post Comment">
    </form>
{% else %}
    <p><a href="{{ url_for('login') }}">Log in</a> to leave a comment.</p>
{% endif %}
```

**Step 8: Implement Logout Functionality**

A simple route clears the user session.

```python
from flask_login import logout_user

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
```

### Password Hashing Mechanism

The security of user accounts depends entirely on proper password handling. Plain-text passwords are never stored. Instead, the application uses a one-way hashing function. When a user sets a password, the system:

1.  Takes the plain-text password provided by the user.
2.  Generates a cryptographically secure random value called a **salt**.
3.  Combines the password and the salt and runs them through a hashing algorithm (like `pbkdf2:sha256`).
4.  Stores the resulting hash string, which includes the salt and algorithm information, in the database.

When a user attempts to log in, the system:

1.  Retrieves the stored hash for that user from the database.
2.  Extracts the salt and algorithm information from the stored hash.
3.  Hashes the provided login password using the same salt and algorithm.
4.  Compares the newly generated hash with the stored hash. If they match, the password is correct.

This process ensures that even if the database is compromised, the original passwords cannot be easily recovered, as the hashing process is irreversible and the use of salts prevents the use of precomputed rainbow tables.

### Session Management and Security

Flask-Login manages user sessions by storing the user's ID in the Flask session, which is a cookie signed with the application's `SECRET_KEY`. This prevents tampering, as any modification to the cookie would break the signature. The `user_loader` callback is crucial; it tells Flask-Login how to retrieve the full User object from the database each time a request is made, using the ID stored in the session cookie.

### Summary of Implementation Order

1.  Install Flask-Login.
2.  Define or modify database models (User, update Comment).
3.  Initialize LoginManager and define `user_loader`.
4.  Create Registration functionality (route, form, template).
5.  Create Login functionality (route, form, template).
6.  Apply `@login_required` to protected routes (e.g., comment submission).
7.  Update templates to conditionally display content based on `current_user`.
8.  Create Logout functionality.
9.  Test the entire flow: registration, login, commenting, logout, and access restriction.

Upon completion of these steps, the blog project will support user accounts, enabling community interaction through authenticated comments and preparing the application for public deployment.