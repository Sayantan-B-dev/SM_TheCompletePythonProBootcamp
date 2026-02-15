# Virtual Bookshelf

A persistent web application built with Flask and SQLite that lets you keep track of books you have read and rate them. This project demonstrates full **CRUD** (Create, Read, Update, Delete) operations using **Flask‑SQLAlchemy** and follows modern Python practices.

## Features

- 📖 View all books in your library
- ➕ Add a new book with title, author, and rating
- ✏️ Edit the rating of any book
- 🗑️ Delete a book from the collection
- 💾 Persistent storage – data remains after server restarts
- 🎨 Clean, responsive interface with custom CSS

## Technologies Used

| Technology | Version | Usage |
|------------|---------|-------|
| **Python** | 3.13+ | Core programming language |
| **Flask** | 3.1.0 | Web framework – handles routing and request/response cycle |
| **Flask‑SQLAlchemy** | 3.1.1 | Integrates SQLAlchemy ORM with Flask – manages database sessions and models |
| **SQLAlchemy** | 2.0.37 | ORM – maps Python classes to database tables, provides high‑level database abstraction |
| **SQLite** | (built‑in) | Lightweight file‑based database – stores all book data persistently |
| **Jinja2** | 3.1.5 | Templating engine – dynamically renders HTML pages |
| **Werkzeug** | 3.1.3 | WSGI utilities – powers Flask’s request/response handling |
| **CSS3** | – | Custom styles for a pleasant user interface |

## Installation & Setup

1. **Clone or download** this repository.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate



# Fully Commented Version — Virtual Bookshelf (Flask + SQLAlchemy 2.0 Style)

Below is your exact code, preserved structurally, with deep inline explanations added to every non-trivial construct, new keyword, and SQLAlchemy 2.0 concept.

---

```python
"""
Virtual Bookshelf – Flask Application with SQLite and SQLAlchemy
-----------------------------------------------------------------
A simple web app to manage a personal book collection with full CRUD.

CRUD = Create, Read, Update, Delete
SQLite = file-based relational database
SQLAlchemy = ORM (Object Relational Mapper)
"""
```

---

```python
# =========================
# IMPORTS
# =========================

from flask import Flask, render_template, request, redirect, url_for
# Flask → main web framework
# render_template → renders Jinja templates
# request → access HTTP request data (forms, args, etc.)
# redirect → redirect browser to another route
# url_for → dynamically generate route URLs

from flask_sqlalchemy import SQLAlchemy
# Flask extension that integrates SQLAlchemy ORM into Flask

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# DeclarativeBase → base class for modern SQLAlchemy 2.0 models
# Mapped → typing helper for ORM columns
# mapped_column → defines table columns (2.0 style)

from sqlalchemy import Integer, String, Float
# SQL column data types
```

---

# Flask Application Setup

```python
# Create Flask app instance
app = Flask(__name__)
# __name__ tells Flask where to look for templates and static files
```

---

```python
# Configure database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
```

### Explanation

`sqlite:///books.db`

• `sqlite` → database type
• `///` → relative file path
• `books.db` → database file created in project root

This creates a file-based SQLite database automatically.

---

```python
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Disables event tracking system
# Prevents extra memory overhead
# Silences deprecation warnings
```

---

# SQLAlchemy 2.0 Declarative Setup

```python
class Base(DeclarativeBase):
    pass
```

### Why This Exists

SQLAlchemy 2.0 introduced typed ORM models.

`DeclarativeBase` provides:

• Metadata container
• Table registry
• Mapping infrastructure

This is modern style replacing older `declarative_base()` function.

---

```python
db = SQLAlchemy(model_class=Base)
```

Here:

• `model_class=Base` tells Flask-SQLAlchemy to use our custom base
• All models will inherit from this base

---

```python
db.init_app(app)
```

Separates database object creation from app binding.

This pattern supports:

• Factory pattern
• Scalable architecture
• Blueprint-based applications

---

# Model Definition

```python
class Book(db.Model):
```

`db.Model` automatically connects this class to SQLAlchemy metadata.

---

```python
__tablename__ = "books"
```

Explicit table name in database.

Without this, SQLAlchemy would generate `book`.

---

## Column Definitions (Modern 2.0 Style)

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Breakdown:

• `Mapped[int]` → typed ORM mapping
• `mapped_column()` → defines column
• `Integer` → SQL type
• `primary_key=True` → unique identifier

This becomes:

```sql
id INTEGER PRIMARY KEY
```

---

```python
title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
```

• `String(250)` → VARCHAR(250)
• `unique=True` → no duplicates allowed
• `nullable=False` → cannot be NULL

---

```python
author: Mapped[str] = mapped_column(String(250), nullable=False)
```

---

```python
rating: Mapped[float] = mapped_column(Float, nullable=False)
```

SQLite stores float as REAL.

---

## Special Method

```python
def __repr__(self):
    return f"<Book {self.title} by {self.author}>"
```

Used for debugging in:

• Python shell
• Logging
• Terminal output

---

# Creating Tables

```python
with app.app_context():
    db.create_all()
```

### Why app_context is required

Flask needs active application context to:

• Access config
• Access database connection
• Bind metadata

Without it → runtime error.

`create_all()`:

• Creates tables only if not existing
• Does NOT delete existing tables
• Does NOT migrate schema

---

# Routes Section

---

## Home Route

```python
@app.route('/')
```

Registers route `/`.

---

```python
def home():
    """Display all books sorted by title."""
```

---

```python
result = db.session.execute(db.select(Book).order_by(Book.title))
```

This is modern SQLAlchemy 2.0 style.

Breakdown:

• `db.select(Book)` → SELECT * FROM books
• `.order_by(Book.title)` → ORDER BY title
• `db.session.execute()` → runs SQL

---

```python
all_books = result.scalars().all()
```

Explanation:

• `.scalars()` extracts ORM objects
• `.all()` converts result into list

Equivalent SQL:

```sql
SELECT * FROM books ORDER BY title;
```

---

```python
return render_template('index.html', books=all_books)
```

Passes list to template.

---

# Add Route

```python
@app.route('/add', methods=['GET', 'POST'])
```

Allows two HTTP methods.

GET → show form
POST → process form

---

```python
if request.method == 'POST':
```

Detect form submission.

---

```python
title = request.form['title'].strip()
```

• `request.form` → POST form data
• `.strip()` removes whitespace

---

```python
rating = float(request.form['rating'])
```

Type conversion from string to float.

If invalid → raises ValueError.

---

```python
new_book = Book(title=title, author=author, rating=rating)
```

Creates Python object.

Not saved yet.

---

```python
db.session.add(new_book)
```

Stages object for insertion.

---

```python
db.session.commit()
```

Writes changes permanently to database.

Important:

• Without commit → nothing saved
• Commit flushes transaction

---

# Edit Route

```python
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
```

Dynamic route parameter.

`<int:book_id>` automatically converts URL segment to integer.

---

```python
book = db.get_or_404(Book, book_id)
```

Equivalent to:

```
SELECT * FROM books WHERE id=?
```

If not found → returns HTTP 404 automatically.

Cleaner than manual query.

---

```python
book.rating = new_rating
```

Updates ORM object in memory.

---

```python
db.session.commit()
```

Persists update.

---

# Delete Route

```python
@app.route('/delete/<int:book_id>')
```

---

```python
book = db.get_or_404(Book, book_id)
```

Fetch object.

---

```python
db.session.delete(book)
```

Marks object for deletion.

---

```python
db.session.commit()
```

Executes:

```sql
DELETE FROM books WHERE id=?
```

---

# Application Entry Point

```python
if __name__ == '__main__':
```

Critical guard.

Prevents:

• Flask reloader double execution
• Infinite re-import loop

---

```python
app.run(debug=True)
```

Debug mode:

• Auto reload on file change
• Interactive debugger
• Better error pages

Never use in production.

---

# Tricky / Modern Concepts Used

| Concept                | Why Important            |
| ---------------------- | ------------------------ |
| DeclarativeBase        | SQLAlchemy 2.0 style     |
| Mapped typing          | Type-safe ORM fields     |
| mapped_column          | New 2.0 column API       |
| db.select()            | Modern query API         |
| scalars()              | Extract ORM instances    |
| get_or_404()           | Flask helper integration |
| app_context()          | Required for db binding  |
| session commit pattern | Transaction control      |

---

# Architectural Notes

This app follows:

• Thin controller pattern
• ORM-based data access
• Template rendering
• Explicit transaction boundaries

---

# Production Improvements (Not Implemented Here)

• Form validation with WTForms
• Unique constraint handling for duplicate titles
• Database migrations (Flask-Migrate)
• Error handling with flash messages
• CSRF protection
• Pagination for large datasets

---

# Final Technical Evaluation

This is clean SQLAlchemy 2.0 style code:

• Modern typing
• Proper session management
• Clean routing
• Correct context usage
• No anti-patterns

It is structurally correct and production-expandable.
