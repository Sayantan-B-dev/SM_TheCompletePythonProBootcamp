# Virtual Bookshelf: Building a Persistent Web Application with Flask and SQLite

## 1. Introduction

The goal of this project is to create a personal “virtual bookshelf” – a web application where users can keep track of the books they have read, along with a personal rating for each book. This concept is familiar from platforms like LibraryThing or Goodreads, but here we will build our own version from scratch. The key challenge is ensuring that the books a user adds are not lost when the server restarts. This requires persistent storage, which we will achieve by integrating a database into our Flask application.

## 2. The Problem: Data Volatility in Memory‑Only Applications

Many beginners’ Flask examples store data in Python lists or dictionaries that live only in memory while the server is running. Consider the following minimal Flask app:

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In‑memory storage – data disappears when the server stops
all_books = []

@app.route('/')
def home():
    return render_template('index.html', books=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'rating': float(request.form['rating'])
        }
        all_books.append(new_book)
        return redirect(url_for('home'))
    return render_template('add.html')
```

If you run this app, add a few books, and then stop and restart the server, all books will be gone – the list `all_books` is re‑created empty on every start. For a real‑world application, this is unacceptable. Users expect their data to persist.

## 3. The Solution: Using a Database

A database stores data on disk, so it remains available even after the application stops. We will use **SQLite**, a self‑contained, serverless, zero‑configuration database engine. SQLite is included in Python’s standard library, so no additional installation is required. Data is stored in a single file (e.g., `books.db`), making it easy to manage and move between environments.

### 3.1 Why SQLite?

- **Lightweight** – ideal for small to medium web applications.
- **File‑based** – the entire database is a single file, simplifying backups and deployment.
- **No separate server process** – the database engine runs inside your application.
- **ACID compliant** – ensures data integrity even in case of crashes.

## 4. Core Operations: CRUD

Any persistent storage system must support four fundamental operations, collectively known as **CRUD**:

- **Create** – add new records (e.g., a new book with its title, author, and rating).
- **Read** – retrieve existing records (e.g., display all books on the homepage).
- **Update** – modify existing records (e.g., change the rating of a book).
- **Delete** – remove records (e.g., delete a book from the shelf).

In the following lessons, we will implement each of these operations using SQLAlchemy, an Object Relational Mapper (ORM) that lets us work with databases using Python classes and objects instead of writing raw SQL.

## 5. Integrating a Database with Flask

Flask itself does not include database support, but it works seamlessly with extensions. We will use **Flask‑SQLAlchemy**, which integrates SQLAlchemy into Flask, providing convenient helpers and a session management system. With Flask‑SQLAlchemy, we define our data model as a Python class, and each row in the database becomes an instance of that class. For example:

```python
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
```

Then, adding a new book is as simple as:

```python
new_book = Book(title="Harry Potter", author="J.K. Rowling", rating=9.3)
db.session.add(new_book)
db.session.commit()
```

This object‑oriented approach makes database code more readable, maintainable, and less error‑prone than raw SQL.

## 6. Learning Roadmap

Over the course of this project, you will:

1. **Set up an SQLite database** using Flask‑SQLAlchemy.
2. **Define a `Book` model** with fields for id, title, author, and rating.
3. **Create the database and table** within the Flask application context.
4. **Perform Create, Read, Update, and Delete operations** using SQLAlchemy’s ORM methods.
5. **Incorporate these operations into Flask routes**:
   - `/` – display all books from the database.
   - `/add` – accept form data and insert a new book.
   - `/edit/<int:book_id>` – show a form to update a book’s rating.
   - `/delete/<int:book_id>` – remove a book from the database.
6. **Enhance the HTML templates** to include links for editing and deleting, and to show appropriate messages when the library is empty.

## 7. Prerequisites

Before proceeding, you should be comfortable with:

- Basic Python syntax (functions, lists, dictionaries, classes).
- Flask fundamentals (routes, render_template, request, redirect).
- HTML forms and Jinja2 templating basics.

The starting project (available in the resources) provides a skeleton with the necessary HTML files and a `main.py` that currently uses an in‑memory list. You will gradually replace the list with a database, adding persistence and full CRUD functionality.

## 8. Next Steps

Now that you understand why we need a database and what we will build, download the starting project, open it in your IDE, and install the required dependencies. The next lessons will guide you through creating the SQLite database, defining the model, and implementing each CRUD operation step by step.