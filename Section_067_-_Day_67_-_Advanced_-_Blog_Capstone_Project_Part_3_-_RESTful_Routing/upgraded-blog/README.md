<span style="color: red; font-weight: bold;">
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
[WARNING] NOT FIXED !!!
</span>



##  README – Technology Usage

Create a file `README.md` in the project root with the following content:

# RESTful Blog with Flask

This project is a fully functional blog application built with Flask. It demonstrates CRUD operations (Create, Read, Update, Delete) using RESTful principles, with a SQLite database and a Bootstrap-powered front end.

## Technologies Used

- **Flask (2.3.2)** – Core web framework. Handles routing, request/response cycle, and template rendering.
- **Flask-SQLAlchemy (3.1.1)** – ORM for database interactions. Defines the `BlogPost` model and provides session management.
- **SQLAlchemy (2.0.25)** – Underlying SQL toolkit used by Flask-SQLAlchemy.
- **Flask-WTF (1.2.1)** – Integrates WTForms with Flask. Used to create and validate the `CreatePostForm`.
- **WTForms (3.0.1)** – Provides form field classes and validators.
- **Flask-CKEditor (0.4.6)** – Adds a rich text editor to the blog content field (`body`). Stores HTML content safely.
- **Bootstrap-Flask (2.2.0)** – Simplifies rendering Bootstrap 5 components in templates (e.g., `render_form` macro, loading of Bootstrap CSS/JS).
- **Werkzeug (3.0.0)** – WSGI toolkit, used internally by Flask for routing and debugging.

## How Each Technology is Used

- **Flask** – Defines routes (`@app.route`) for home (`/`), individual post (`/post/<id>`), new post (`/new-post`), edit (`/edit-post/<id>`), delete (`/delete/<id>`), about and contact pages.
- **Flask-SQLAlchemy & SQLAlchemy** – The `BlogPost` model maps to the `posts` table. `db.session` is used to query, add, update, and delete records. The database is automatically created on first run (`db.create_all()`).
- **Flask-WTF & WTForms** – `CreatePostForm` inherits from `FlaskForm`. Fields use validators like `DataRequired()` and `URL()`. The form is instantiated in routes and passed to templates.
- **Flask-CKEditor** – Initialised with `CKEditor(app)`. The `CKEditorField` in the form renders as a rich text area. In templates, `{{ ckeditor.load() }}` and `{{ ckeditor.config(name='body') }}` inject the necessary JavaScript.
- **Bootstrap-Flask** – In `header.html`, `{{ bootstrap.load_css() }}` loads Bootstrap CSS. In `make-post.html`, `{{ render_form(form, ...) }}` generates the complete form HTML with Bootstrap styling and CSRF protection.
- **Werkzeug** – Used implicitly for URL routing and the development server.

## Project Structure

```
blog_project/
├── instance/               # Contains the SQLite database (posts.db)
├── static/                 # Static assets (CSS, JS, images)
│   ├── assets/
│   │   ├── favicon.ico
│   │   └── img/            # Header background images (about-bg.jpg, contact-bg.jpg, etc.)
│   ├── css/
│   │   └── styles.css      # Custom and Bootstrap styles
│   └── js/
│       └── scripts.js      # Custom JavaScript (scroll effects)
├── templates/              # Jinja2 HTML templates
│   ├── about.html
│   ├── contact.html
│   ├── footer.html
│   ├── header.html
│   ├── index.html
│   ├── make-post.html
│   └── post.html
├── main.py                  # Flask application
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Running the Application

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python main.py
   ```
3. Open `http://127.0.0.1:5002` in your browser.

> **Note:** The images referenced in the templates (`about-bg.jpg`, `contact-bg.jpg`, etc.) are not included in this code dump. You need to place your own images in `static/assets/img/` or adjust the paths accordingly.

## Features

- View all posts on the home page (reads from database).
- Click a post title to see its full content.
- Create a new post using a form with CKEditor.
- Edit existing posts (form pre‑populated with current data).
- Delete posts via a ✘ icon next to each post.

All changes are persisted in the SQLite database.


---