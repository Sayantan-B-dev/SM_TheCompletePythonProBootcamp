# Sayantan's Blog - Full-Stack Flask Blog Application

## Overview

Sayantan's Blog is a fully functional, multi-user blog platform built with Flask. It allows users to register, log in, read blog posts, and leave comments. An administrative user (the first registered user) has exclusive privileges to create, edit, and delete posts. The application demonstrates core web development concepts including user authentication, relational databases, form handling, session management, and secure password storage.

The project is structured as a learning capstone and can be easily extended with additional features such as post categories, user profiles, or moderation tools.

---

## Features

- **User Authentication**
  - Registration with secure password hashing (Werkzeug)
  - Login / Logout using Flask-Login
  - Flash messages for user feedback

- **Blog Posts**
  - Public listing of all posts on the homepage
  - Individual post pages with full content and comments
  - Rich text editing for post body (CKEditor)

- **Comments**
  - Any logged-in user can comment on posts
  - Comments are displayed with author name, timestamp, and Gravatar image
  - CKEditor for comment text (supports formatting)

- **Admin Privileges**
  - The first registered user (id = 1) is automatically the admin
  - Admin-only routes for creating, editing, and deleting posts
  - UI buttons for admin actions are hidden from regular users
  - Custom decorator `@admin_only` protects admin routes

- **Relational Database**
  - SQLite with SQLAlchemy ORM
  - One-to-many relationships: User → BlogPost, User → Comment, BlogPost → Comment

- **Modern UI**
  - Bootstrap 5 for responsive design
  - Custom Clean Blog theme (Start Bootstrap)
  - Gravatar integration for user avatars

---

## Technology Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite, SQLAlchemy (ORM)
- **Authentication**: Flask-Login, Werkzeug Security
- **Forms**: Flask-WTF, WTForms
- **Rich Text**: Flask-CKEditor
- **Avatars**: Flask-Gravatar
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS
- **Templating**: Jinja2

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional)

### Installation Steps

1. **Clone or download the project**  
   If you have Git:
   ```bash
   git clone <repository-url>
   cd sayantan-blog
   ```
   Otherwise, download the ZIP and extract it.

2. **Create and activate a virtual environment**  
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**  
   ```bash
   python main.py
   ```
   The server will start at `http://127.0.0.1:5001`.

5. **Access the blog**  
   Open your browser and go to `http://127.0.0.1:5001`.

### Initial Setup Notes

- The first time you run the app, SQLite database file `posts.db` will be created automatically (if it doesn't exist) with all tables defined in the models.
- To become the admin, **register as the very first user**. That user will have `id = 1` and will see the "Create New Post" button and edit/delete controls.
- If you ever change the database models, you must delete `posts.db` and restart the server to recreate the database with the new schema.

---

## Project Structure

```
sayantan-blog/
│
├── main.py                 # Main Flask application (routes, models, config)
├── forms.py                # WTForms classes (Register, Login, Post, Comment)
├── requirements.txt        # Python dependencies
├── posts.db                # SQLite database (created on first run)
│
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css      # Custom CSS (including Bootstrap overrides)
│   ├── js/
│   │   └── scripts.js      # Custom JavaScript (navbar scroll behavior)
│   └── assets/             # Images (home-bg.jpg, about-bg.jpg, etc.)
│
└── templates/              # Jinja2 HTML templates
    ├── header.html         # Navigation bar and head section
    ├── footer.html         # Footer and scripts
    ├── index.html          # Homepage with list of posts
    ├── post.html           # Single post with comments and comment form
    ├── about.html          # About page (personalized)
    ├── contact.html        # Contact page (simple form)
    ├── login.html          # User login form
    ├── register.html       # User registration form
    └── make-post.html      # Create / Edit post form
```

---

## Database Schema

The application uses three tables with relationships:

### `users`
| Column   | Type    | Constraints          | Description               |
|----------|---------|----------------------|---------------------------|
| id       | Integer | Primary Key          | Unique user ID            |
| email    | String  | Unique, Not Null     | User's email (login)      |
| password | String  | Not Null             | Hashed password           |
| name     | String  | Not Null             | Display name              |

### `blog_posts`
| Column     | Type    | Constraints                 | Description                     |
|------------|---------|-----------------------------|---------------------------------|
| id         | Integer | Primary Key                 | Unique post ID                  |
| author_id  | Integer | Foreign Key (`users.id`)    | ID of the user who wrote it     |
| title      | String  | Unique, Not Null            | Post title                      |
| subtitle   | String  | Not Null                    | Post subtitle                   |
| date       | String  | Not Null                    | Publication date (formatted)    |
| body       | Text    | Not Null                    | Post content (HTML)              |
| img_url    | String  | Not Null                    | Header image URL                |

### `comments`
| Column      | Type    | Constraints                      | Description                     |
|-------------|---------|----------------------------------|---------------------------------|
| id          | Integer | Primary Key                      | Unique comment ID               |
| text        | Text    | Not Null                         | Comment content (HTML)          |
| author_id   | Integer | Foreign Key (`users.id`)         | ID of the user who commented    |
| post_id     | Integer | Foreign Key (`blog_posts.id`)    | ID of the post being commented  |

**Relationships:**
- One `User` can have many `BlogPost` (via `author_id`).
- One `User` can have many `Comment` (via `author_id`).
- One `BlogPost` can have many `Comment` (via `post_id`).

SQLAlchemy `relationship()` definitions in `main.py` allow easy navigation:
- `user.posts` → list of user's blog posts
- `user.comments` → list of user's comments
- `post.author` → the `User` object who wrote the post
- `post.comments` → list of comments on that post
- `comment.author` → the `User` object who wrote the comment
- `comment.post` → the `BlogPost` object the comment belongs to

---

## Dataflow and Application Logic

This section explains how data moves through the application for key user scenarios.

### 1. User Registration

1. User navigates to `/register` (GET request).
2. `register()` route instantiates `RegisterForm`.
3. Template `register.html` renders the form using Bootstrap-Flask's `render_form`.
4. User fills out name, email, password and submits (POST).
5. `form.validate_on_submit()` checks validators.
6. The route queries the database for an existing user with the same email.
   - If found, flash message "You've already signed up..." and redirect to login.
7. Password is hashed using `generate_password_hash()` (pbkdf2:sha256, salt length 8).
8. A new `User` object is created and added to the database.
9. `login_user(new_user)` from Flask-Login automatically logs the user in.
10. Redirect to homepage (`get_all_posts`).
11. The navbar now shows the user's name and "Log Out".

### 2. User Login

1. User visits `/login` (GET) – login form is displayed.
2. User enters email/password and submits (POST).
3. `form.validate_on_submit()` passes.
4. Database is queried for a user with that email using `db.select(User).where(...)`.
   - If no user → flash "That email does not exist", redirect back to login.
5. `check_password_hash(stored_password, submitted_password)` verifies password.
   - If mismatch → flash "Password incorrect", redirect to login.
6. On success, `login_user(user)` creates a session.
7. Redirect to homepage.
8. The navbar updates to show logged-in state.

### 3. Viewing Blog Posts

- **Homepage** (`/`):
  - `get_all_posts()` queries all `BlogPost` records and passes them to `index.html`.
  - Template loops through `all_posts` and displays title, subtitle, author name, date.
  - If the current user is admin (`current_user.id == 1`), a delete (✘) link appears next to each post, and a "Create New Post" button is shown at the bottom.
- **Individual Post** (`/post/<int:post_id>`):
  - `show_post()` retrieves the post by ID (or 404).
  - It instantiates `CommentForm`.
  - On POST (comment submission), it checks if user is authenticated; if not, flashes and redirects to login.
  - If authenticated, creates a new `Comment` linked to the current user and the post, saves to DB, then redirects back to the same post page (to avoid resubmission).
  - On GET, it simply renders `post.html` with the post, existing comments, and the comment form.
  - Comments are displayed using `post.comments` relationship; each comment shows author's Gravatar image (`comment.author.email | gravatar`), text (safe HTML), and author name.

### 4. Posting a Comment

1. Logged-in user scrolls to the comment form at the bottom of a post page.
2. User writes a comment (using CKEditor) and clicks "Submit Comment".
3. POST request to `/post/<post_id>`.
4. `form.validate_on_submit()` succeeds.
5. Route verifies `current_user.is_authenticated` (redundant because form already requires login? but kept as safety).
6. New `Comment` is created with `text`, `author=current_user`, `parent_post=requested_post`.
   - Note: The model uses `comment_author` relationship; the code uses `comment_author=current_user`.
7. Comment is added to session and committed.
8. Redirect back to the same post page, where the new comment now appears.

### 5. Admin: Creating a New Post

1. Admin (user id=1) clicks "Create New Post" button on homepage.
2. GET request to `/new-post`; `add_new_post()` instantiates `CreatePostForm` and renders `make-post.html`.
3. Admin fills in title, subtitle, image URL, and post body (CKEditor), submits.
4. POST request; `form.validate_on_submit()` passes.
5. A new `BlogPost` is created with:
   - `author=current_user` (sets `author_id` automatically)
   - `date=date.today().strftime("%B %d, %Y")`
6. Post is saved to database.
7. Redirect to homepage, where the new post appears at the top (or in default order).

### 6. Admin: Editing a Post

1. Admin visits a post page and clicks "Edit Post".
2. GET request to `/edit-post/<post_id>`.
   - `edit_post()` retrieves the post.
   - It pre-populates `CreatePostForm` with existing post data.
3. Admin modifies fields and submits.
4. POST; form validated; the existing post object is updated with new data.
5. Changes committed; redirect to the updated post page.

### 7. Admin: Deleting a Post

1. Admin clicks the ✘ link next to a post on the homepage.
2. GET request to `/delete/<post_id>`.
3. `delete_post()` retrieves the post, deletes it from the database, and commits.
4. Redirect back to homepage.

### 8. Logout

1. User clicks "Log Out" in navbar.
2. GET request to `/logout`.
3. `logout_user()` clears the session.
4. Redirect to homepage; navbar returns to "Login"/"Register".

---

## Detailed File Descriptions

### `forms.py`

This file defines all WTForm classes used in the application. Each form corresponds to a specific user interaction.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
```

- **`CreatePostForm`** – For creating/editing blog posts.
  - `title` – String field, required.
  - `subtitle` – String field, required.
  - `img_url` – String field, required and must be a valid URL.
  - `body` – CKEditor field (rich text), required.
  - `submit` – Submit button.

- **`RegisterForm`** – For new user registration.
  - `email` – String field, required.
  - `password` – Password field, required.
  - `name` – String field, required.
  - `submit` – "Sign Me Up!" button.

- **`LoginForm`** – For user login.
  - `email` – String field, required.
  - `password` – Password field, required.
  - `submit` – "Let Me In!" button.

- **`CommentForm`** – For submitting comments.
  - `comment_text` – CKEditor field (rich text), required.
  - `submit` – "Submit Comment" button.

All forms use `FlaskForm` as base, which provides CSRF protection automatically.

---

### `main.py`

This is the core application file. It contains:

- Flask app configuration
- Database setup (SQLAlchemy)
- Flask-Login configuration
- Gravatar initialization
- SQLAlchemy model definitions (`User`, `BlogPost`, `Comment`)
- Custom decorator `@admin_only`
- All route handlers

Let's break down its components:

#### 1. Imports and App Initialization

```python
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
```

- Extensions: Bootstrap5, CKEditor, Gravatar, LoginManager, SQLAlchemy.
- `DeclarativeBase` is used for SQLAlchemy 2.0 style models.
- Custom decorator support with `functools.wraps`.
- Security utilities from Werkzeug.

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)
```

- Secret key should be changed in production.

#### 2. Flask-Login Setup

```python
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
```

- `user_loader` reloads the user object from the session-stored ID.

#### 3. Gravatar Configuration

```python
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
```

- Sets default avatar to "retro" style; can be customized.

#### 4. Database Configuration and Models

```python
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

**Model: User**

```python
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
```

- Inherits from `UserMixin` to provide default Flask-Login methods.
- Relationships: one-to-many with BlogPost and Comment.

**Model: BlogPost**

```python
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")
```

- `author_id` foreign key links to users table.
- `comments` relationship to access all comments on this post.

**Model: Comment**

```python
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
```

- Two foreign keys: `author_id` and `post_id`.
- Relationships provide easy navigation.

**Create tables** (if not exist):

```python
with app.app_context():
    db.create_all()
```

#### 5. Admin Decorator

```python
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

- Checks if the logged-in user has `id == 1`. If not, aborts with HTTP 403 Forbidden.
- Applied to routes that only admin should access.

#### 6. Route Handlers

- **`/register`** – GET/POST for registration.  
  - On POST, checks if email exists, hashes password, creates user, logs in, redirects to home.
- **`/login`** – GET/POST for login.  
  - Validates email existence and password, logs in, redirects to home.
- **`/logout`** – Logs out user.
- **`/`** – Homepage: lists all posts.
- **`/post/<int:post_id>`** – Shows single post, handles comment submission.
- **`/new-post`** – Admin only: creates new post.
- **`/edit-post/<int:post_id>`** – Admin only: edits existing post.
- **`/delete/<int:post_id>`** – Admin only: deletes post.
- **`/about`** – Renders about page.
- **`/contact`** – Renders contact page (form not fully functional in this version).

---

### Templates

All templates extend or include `header.html` and `footer.html`. They use Bootstrap-Flask macros for form rendering.

#### `header.html`

- Contains `<head>` with all CSS links (Bootstrap, Font Awesome, custom styles).
- Navigation bar with conditional links based on `current_user.is_authenticated`.
- Sets the page title to "Sayantan's Blog".

#### `footer.html`

- Footer with social media links (dummy) and copyright notice.
- Includes Bootstrap JS and custom `scripts.js`.

#### `index.html`

- Displays a list of all blog posts.
- Each post shows title, subtitle, author name, date.
- If admin, a delete icon (✘) appears next to each post.
- If admin, a "Create New Post" button is shown.

#### `post.html`

- Full post content with header image.
- Below post, a list of comments (each with Gravatar, author name, comment text).
- Comment form (CKEditor) for logged-in users; if not logged in, a login link is shown.
- Admin sees an "Edit Post" button.

#### `about.html`

- Personal information about Sayantan Bharati (from PDF).
- Lists featured projects, education, certifications, and background.

#### `contact.html`

- A simple contact form (not wired to backend in this version). The button is functional but no email logic is implemented.

#### `login.html` and `register.html`

- Render respective forms using `render_form`.
- Display flash messages (e.g., "That email does not exist").

#### `make-post.html`

- Used for both creating and editing posts.
- Contains CKEditor for the body field.
- Conditionally changes heading to "Edit Post" if `is_edit` is passed.

---

### Static Files

- **`css/styles.css`** – Contains Bootstrap 5 overrides, custom styling for comments, flash messages, and the Clean Blog theme.
- **`js/scripts.js`** – Handles the navbar scroll behavior (hides/shows on scroll).

---

## Security Considerations

- **Password Hashing**: All passwords are hashed using `werkzeug.security.generate_password_hash` (pbkdf2:sha256 with salt). No plaintext passwords are stored.
- **Session Management**: Flask-Login uses secure cookies signed with the app's `SECRET_KEY`.
- **CSRF Protection**: Flask-WTF automatically includes CSRF tokens in all forms.
- **Admin Route Protection**: The `@admin_only` decorator ensures only user with id=1 can access post creation, editing, and deletion. Even if a non-admin guesses the URL, they receive a 403 error.
- **SQL Injection**: SQLAlchemy's ORM and parameterized queries prevent injection.

---

## Testing the Application

1. **Register a new user** – This will be the admin if it's the first user.
2. **Log in** as that user – you should see "Create New Post" button.
3. **Create a post** – Fill out the form and submit.
4. **View the post** – Check that it appears on the homepage and that the post page displays correctly.
5. **Register a second user** (different email) – This will be a regular user.
6. **Log in as the second user** – The navbar should show "Log Out" but no admin buttons.
7. **Visit a post** – You should see the comment form. Submit a comment.
8. **Check that the comment appears** with your avatar (Gravatar) and name.
9. **Log out** and verify the navbar returns to "Login"/"Register".
10. **Try accessing admin routes manually** (e.g., `/new-post`) while logged in as a regular user – you should see a 403 error.
11. **Try accessing admin routes while logged out** – you'll either be redirected to login (if route also used `@login_required`) or get 403 (if only `@admin_only`). In this app, admin routes only have `@admin_only`, so logged-out users also get 403.

---

## Deployment Considerations

To deploy this application to a production server (e.g., Heroku, PythonAnywhere, Render), you need to:

1. **Change the secret key** to a strong, environment-specific value.
2. **Use a production database** (e.g., PostgreSQL) instead of SQLite. Update `SQLALCHEMY_DATABASE_URI`.
3. **Set `debug=False`** in `app.run()`.
4. **Configure static files** properly (e.g., use WhiteNoise or serve via web server).
5. **Set up environment variables** for sensitive data (secret key, database URL).
6. **Ensure all dependencies** are listed in `requirements.txt`.

---

## Customization

You can easily customize the blog:

- **Change site title** – Edit `<title>` in `header.html`.
- **Modify about page** – Update `about.html` with your own bio.
- **Change social links** – In `footer.html`, replace `#!` with actual URLs.
- **Add new features** – Extend models, create new routes and templates.

---

## Credits

- Original project concept by Angela Yu (App Brewery).
- Customized and extended by Sayantan Bharati.
- Bootstrap theme: [Clean Blog](https://startbootstrap.com/theme/clean-blog) by Start Bootstrap.
- Icons: Font Awesome.
- Avatars: Gravatar.

---

## License

This project is for educational purposes. Feel free to use and modify it for your own learning. If you publish it, please give appropriate credit to Angela Yu's course https://www.udemy.com/course/100-days-of-code/.

---

**Enjoy blogging with Sayantan's Blog!**