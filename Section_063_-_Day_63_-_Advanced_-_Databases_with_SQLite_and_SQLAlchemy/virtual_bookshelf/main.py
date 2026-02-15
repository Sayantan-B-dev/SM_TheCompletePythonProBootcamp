"""
Virtual Bookshelf – Flask Application with SQLite and SQLAlchemy
----------------------------------------------------------------
A simple CRUD web application to manage a personal book collection.

CRUD:
    C → Create
    R → Read
    U → Update
    D → Delete

This project demonstrates:
    • Flask routing
    • SQLite database integration
    • SQLAlchemy ORM (2.0 style)
    • Template rendering
    • Form handling
"""

# =========================
# IMPORTS
# =========================

from flask import Flask, render_template, request, redirect, url_for
# Flask → main web framework class
# render_template → renders Jinja HTML templates
# request → provides access to incoming HTTP request data
# redirect → sends browser to another route
# url_for → dynamically generates URL for a given route function

from flask_sqlalchemy import SQLAlchemy
# Flask extension that integrates SQLAlchemy ORM with Flask

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# DeclarativeBase → new SQLAlchemy 2.0 base class for ORM models
# Mapped → typing helper for ORM fields
# mapped_column → modern way to declare table columns (2.0 style)

from sqlalchemy import Integer, String, Float
# SQL column types used when defining model fields


# =========================
# FLASK APPLICATION SETUP
# =========================

app = Flask(__name__)
# __name__ tells Flask where this file is located.
# Flask uses it to find templates and static folders.


# =========================
# DATABASE CONFIGURATION
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
# sqlite:/// → relative SQLite file path
# books.db → file will be created in project directory
# SQLite is file-based and requires no server.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Disables modification tracking system
# Prevents extra memory usage
# Silences warning message


# =========================
# SQLALCHEMY 2.0 BASE CLASS
# =========================

class Base(DeclarativeBase):
    pass
# DeclarativeBase is SQLAlchemy 2.0 style base.
# It provides metadata and registry for ORM models.


# =========================
# DATABASE OBJECT
# =========================

db = SQLAlchemy(model_class=Base)
# model_class=Base ensures all models use the new 2.0 DeclarativeBase

db.init_app(app)
# Binds database instance to Flask app.
# Required when using factory-compatible patterns.


# =========================
# MODEL DEFINITION
# =========================

class Book(db.Model):
    """
    ORM Model representing the 'books' table.
    Each instance of Book maps to one row in the database.
    """

    __tablename__ = "books"
    # Explicit table name in database

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # id column
    # Integer type
    # primary_key=True makes it unique identifier
    # Auto-incremented automatically by SQLite

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # String(250) → VARCHAR(250)
    # unique=True → prevents duplicate titles
    # nullable=False → must always have a value

    author: Mapped[str] = mapped_column(String(250), nullable=False)
    # Author name column
    # Cannot be NULL

    rating: Mapped[float] = mapped_column(Float, nullable=False)
    # Float column
    # Stores numeric rating value

    def __repr__(self):
        # Used for debugging and console output
        return f"<Book {self.title} by {self.author}>"


# =========================
# TABLE CREATION
# =========================

with app.app_context():
    db.create_all()
    # create_all() creates tables only if they do not exist
    # Requires active application context
    # Does NOT handle migrations
    # Does NOT modify existing schema


# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    """
    Read operation.
    Displays all books sorted alphabetically by title.
    """

    result = db.session.execute(
        db.select(Book).order_by(Book.title)
    )
    # db.select(Book) → SELECT * FROM books
    # order_by(Book.title) → ORDER BY title
    # session.execute() → sends query to database

    all_books = result.scalars().all()
    # scalars() extracts ORM objects
    # all() converts result to list

    return render_template('index.html', books=all_books)
    # Passes books list to template


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Create operation.
    GET  → Show add form
    POST → Insert new book into database
    """

    if request.method == 'POST':

        # Extract form data
        title = request.form['title'].strip()
        # request.form contains POST form values
        # strip() removes leading/trailing spaces

        author = request.form['author'].strip()

        try:
            rating = float(request.form['rating'])
            # Convert rating string to float
        except ValueError:
            # If conversion fails, redirect back
            return redirect(url_for('add'))

        # Create new Book instance
        new_book = Book(
            title=title,
            author=author,
            rating=rating
        )

        db.session.add(new_book)
        # Stages object for insertion

        db.session.commit()
        # Commits transaction to database
        # Without commit → nothing is saved

        return redirect(url_for('home'))
        # Redirect after successful insert

    return render_template('add.html')
    # Render form for GET request


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    """
    Update operation.
    Allows editing rating of existing book.
    """

    book = db.get_or_404(Book, book_id)
    # Fetch book by primary key
    # If not found → automatic 404 error

    if request.method == 'POST':

        try:
            new_rating = float(request.form['rating'])
        except ValueError:
            return redirect(url_for('edit', book_id=book_id))

        book.rating = new_rating
        # Update object in memory

        db.session.commit()
        # Persist update to database

        return redirect(url_for('home'))

    return render_template('edit_rating.html', book=book)
    # Pass book object to template


@app.route('/delete/<int:book_id>')
def delete(book_id):
    """
    Delete operation.
    Removes a book from database.
    """

    book = db.get_or_404(Book, book_id)
    # Fetch book or raise 404

    db.session.delete(book)
    # Mark object for deletion

    db.session.commit()
    # Execute DELETE SQL command

    return redirect(url_for('home'))


# =========================
# APPLICATION ENTRY POINT
# =========================

if __name__ == '__main__':
    # Prevents app from running on import
    # Required when debug mode is enabled
    # Avoids double execution due to reloader

    app.run(debug=True)
    # debug=True enables:
    # • Auto-reload on file change
    # • Interactive debugger
    # • Detailed error trace
    # Should NEVER be used in production
