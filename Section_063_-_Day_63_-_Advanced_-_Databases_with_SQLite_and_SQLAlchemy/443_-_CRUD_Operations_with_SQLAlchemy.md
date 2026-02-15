# SQLAlchemy CRUD Operations: Create, Read, Update, Delete

## 1. Overview

Now that you have a basic understanding of how to set up a database with SQLAlchemy and define a model (the `Book` class), it is time to explore the four fundamental operations that any persistent storage system must support: **Create, Read, Update, and Delete** – collectively known as **CRUD**.

CRUD operations are the backbone of most web applications. In the context of our virtual bookshelf:

- **Create** – adding a new book to the library.
- **Read** – displaying all books or fetching a specific book (e.g., to edit).
- **Update** – changing a book’s rating.
- **Delete** – removing a book from the shelf.

SQLAlchemy provides a high‑level, Pythonic interface for performing these operations. Instead of writing raw SQL statements like `INSERT INTO books ...`, you work with Python objects and methods. This makes your code cleaner, safer, and easier to maintain.

This document will walk you through each CRUD operation using SQLAlchemy (specifically, the Flask‑SQLAlchemy integration) and explain the syntax introduced in SQLAlchemy 2.0. We will use the `Book` model defined in the previous lesson:

```python
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```

All database operations must be performed within an **application context** because Flask‑SQLAlchemy relies on the Flask app’s configuration. You will see the pattern:

```python
with app.app_context():
    # perform database operation
```

This ensures that the database session and connection are properly managed.

## 2. Review: Creating the Database and Table

Before diving into CRUD, let’s briefly recap how to create the database and the table using SQLAlchemy. This step is a prerequisite for any subsequent operations.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()
```

Running this code creates a SQLite database file `books.db` with a table `books` containing the four columns. If the table already exists, `create_all()` does nothing – it will not overwrite or modify it.

## 3. Create – Adding New Records

The **Create** operation corresponds to inserting a new row into the database. In SQLAlchemy, you:

1. Create an instance of the model class (e.g., `Book`).
2. Add it to the session.
3. Commit the session.

### 3.1 Simple Insert

```python
with app.app_context():
    new_book = Book(
        title="Harry Potter and the Sorcerer's Stone",
        author="J.K. Rowling",
        rating=9.5
    )
    db.session.add(new_book)
    db.session.commit()
```

**Important notes:**

- The `id` field is omitted; because it is an auto‑incrementing primary key, SQLite will assign the next available integer automatically. You *can* specify an `id` manually, but it’s usually better to let the database handle it.
- The `title` column has a `UNIQUE` constraint, so attempting to insert a book with a title that already exists will raise an `IntegrityError`. This is desirable because we don’t want duplicate entries for the same book.
- After `commit()`, the `new_book` object is updated with its generated `id` (you can access `new_book.id` to see it).

### 3.2 Inserting Multiple Records

To add several books at once, you can call `db.session.add_all()` with a list of objects, then commit once:

```python
with app.app_context():
    book1 = Book(title="1984", author="George Orwell", rating=9.0)
    book2 = Book(title="To Kill a Mockingbird", author="Harper Lee", rating=9.8)
    db.session.add_all([book1, book2])
    db.session.commit()
```

This is more efficient than committing after each individual add.

### 3.3 Handling Duplicates Gracefully

If you are inserting data that might conflict with existing records (e.g., a book with a duplicate title), you may want to check existence first or use a “upsert” pattern. For simplicity in our bookshelf, we assume titles are unique and rely on the database constraint.

## 4. Read – Retrieving Records

Reading data is the most frequent operation. SQLAlchemy provides a flexible query system using the `select()` function. The general pattern is:

```python
with app.app_context():
    result = db.session.execute(db.select(Book).where(...).order_by(...))
    books = result.scalars().all()   # or .first(), .one(), etc.
```

### 4.1 Read All Records

To get every book in the table:

```python
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
```

- `db.select(Book)` builds a SELECT query for the `Book` table.
- `.order_by(Book.title)` sorts the results by title. You can omit this if order doesn’t matter.
- `result.scalars()` returns the rows as `Book` objects instead of tuples. This is essential when you want to work with model instances.
- `.all()` fetches all matching records as a list. If there are no books, the list is empty.

### 4.2 Read a Specific Record by a Column Value

To retrieve a single book that matches a condition, use `.where()` and then `.scalar()` (or `.one()`/`.first()`).

```python
with app.app_context():
    book = db.session.execute(
        db.select(Book).where(Book.title == "1984")
    ).scalar()
```

- `.scalar()` returns the first element of the result, or `None` if no record matches. If multiple records match (which shouldn’t happen because title is unique), it returns the first one.
- If you are certain that exactly one record should exist, you can use `.one()` – it raises an exception if zero or more than one are found.
- `.first()` is similar to `.scalar()` but explicitly limits the query to one row at the database level.

### 4.3 Read a Record by Primary Key

Because primary keys are frequently used to identify records (e.g., when editing or deleting), Flask‑SQLAlchemy provides a convenience method: `db.get_or_404()`. This is particularly useful inside route handlers.

```python
with app.app_context():
    book = db.get_or_404(Book, book_id)
```

- It returns the `Book` object with the given `book_id`.
- If no such book exists, it automatically raises a `404 Not Found` error, which Flask can handle to show a user‑friendly page. This saves you from writing explicit `if book is None: abort(404)`.

Note: `get_or_404()` is a method of the `SQLAlchemy` instance, not of the session. It works only when you have a Flask request context, so it’s typically used inside route functions (without needing a separate `app.app_context()` because the request context already provides it).

### 4.4 Filtering with Multiple Conditions

You can chain `.where()` clauses or combine conditions using logical operators:

```python
from sqlalchemy import and_, or_

# Books with rating >= 9.0 and author starting with 'J'
books = db.session.execute(
    db.select(Book).where(
        and_(Book.rating >= 9.0, Book.author.startswith("J"))
    )
).scalars().all()
```

### 4.5 Ordering and Limiting

You can control the order and limit the number of results:

```python
# Get the 5 highest‑rated books
top_books = db.session.execute(
    db.select(Book).order_by(Book.rating.desc()).limit(5)
).scalars().all()
```

## 5. Update – Modifying Existing Records

Updating a record involves three steps:

1. Retrieve the book you want to update.
2. Modify its attributes.
3. Commit the session.

### 5.1 Update by Query

```python
with app.app_context():
    book_to_update = db.session.execute(
        db.select(Book).where(Book.title == "1984")
    ).scalar()
    if book_to_update:
        book_to_update.rating = 9.5   # change rating
        db.session.commit()
```

- After modifying the object, calling `commit()` persists the changes. SQLAlchemy tracks which objects have been changed and generates the appropriate UPDATE statement.

### 5.2 Update by Primary Key (using `get_or_404`)

In a Flask route, you would typically have the book’s id from the URL. Then you can use `get_or_404` to fetch it and update:

```python
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    if request.method == 'POST':
        book.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book)
```

Here, the `db.get_or_404()` handles the case where the book does not exist (by raising 404). After updating the rating, we commit and redirect.

### 5.3 Bulk Updates

You can update multiple records that match a condition using the `update()` method on a query. However, this bypasses the ORM and should be used with caution. Example:

```python
from sqlalchemy import update

stmt = update(Book).where(Book.author == "Old Author").values(author="New Author")
db.session.execute(stmt)
db.session.commit()
```

But for most cases, especially in a small application like ours, it’s simpler to fetch, modify, and commit.

## 6. Delete – Removing Records

Deleting records is similar to updating, but you call `db.session.delete()`.

### 6.1 Delete by Query

```python
with app.app_context():
    book_to_delete = db.session.execute(
        db.select(Book).where(Book.title == "1984")
    ).scalar()
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
```

### 6.2 Delete by Primary Key (with `get_or_404`)

Again, in a route:

```python
@app.route('/delete/<int:book_id>')
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
```

This deletes the book and redirects to the home page.

### 6.3 Bulk Delete

You can delete all records that match a condition without fetching them individually:

```python
from sqlalchemy import delete

stmt = delete(Book).where(Book.author == "George Orwell")
db.session.execute(stmt)
db.session.commit()
```

Again, this is a lower‑level operation and does not load the objects into memory.

## 7. Understanding the New SQLAlchemy 2.0 Syntax

If you have seen older tutorials, you might be familiar with a different style, such as `Book.query.all()` or `Book.query.get(id)`. As of SQLAlchemy 2.0, the “query” interface is deprecated. The recommended approach uses `session.execute()` with `select()`. Flask‑SQLAlchemy 3.x follows this new style.

### 7.1 Key Components

- **`db.select(Entity)`** – creates a SELECT statement for the given model (or columns).
- **`.where(condition)`** – adds a WHERE clause.
- **`.order_by()`**, **`.limit()`**, etc. – further modify the statement.
- **`db.session.execute(statement)`** – executes the statement and returns a `Result` object.
- **`.scalars()`** – extracts the scalar values (i.e., the model instances) from each row.
- **`.all()`** – returns a list of all results.
- **`.scalar()`** – returns a single result or `None`.
- **`.first()`** – limits to 1 row and returns it or `None`.
- **`.one()`** – expects exactly one row, raises an error otherwise.

### 7.2 Why This Change?

The new approach is more explicit and aligns with SQLAlchemy’s core philosophy of treating SQL as Python. It also works better with asynchronous code and type hints. Although it may seem more verbose, it is also more flexible and powerful.

## 8. Common Patterns and Pitfalls

### 8.1 Forgetting to Commit

After calling `db.session.add()` or modifying an object, you **must** call `db.session.commit()` to persist the changes. If you forget, the changes will be lost when the session is closed (at the end of the request or context).

### 8.2 Working Outside of Application Context

All database operations (except `get_or_404` inside a route) need an application context. If you try to run `db.session.execute(...)` without being inside a `with app.app_context():` block, you’ll get a `RuntimeError: Working outside of application context.`

### 8.3 Unique Constraint Violations

Inserting a book with a title that already exists will raise an `IntegrityError`. In a real application, you should catch this and show a user‑friendly message. For simplicity, we can let it propagate (Flask will show an internal server error) but be aware that this can happen.

### 8.4 Handling None When Using `.scalar()`

Always check if the returned object is `None` before accessing its attributes, unless you are certain it exists.

### 8.5 Using `get_or_404` Inside Routes

`get_or_404` is a convenient shortcut that both fetches the object and raises a 404 if not found. It’s perfect for edit and delete routes where the book must exist.

## 9. Complete Example: Integrating CRUD into Flask Routes

Here’s how you might use these operations in the virtual bookshelf project. Assume we have already set up the database and model.

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# ... (app and db initialization as before) ...

@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', books=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=float(request.form['rating'])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    if request.method == 'POST':
        book.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=book)

@app.route('/delete/<int:book_id>')
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
```

This example demonstrates all CRUD operations in a typical Flask application. Notice that we do **not** need explicit `app.app_context()` inside route functions because Flask creates an application context for each request automatically.

## 10. Summary

| Operation | Key Methods | Example |
|-----------|-------------|---------|
| **Create** | `db.session.add()`, `db.session.commit()` | `db.session.add(Book(...))` |
| **Read (all)** | `db.session.execute(db.select(Book)).scalars().all()` | `books = db.session.execute(db.select(Book)).scalars().all()` |
| **Read (one by column)** | `.where().scalar()` | `book = db.session.execute(db.select(Book).where(...)).scalar()` |
| **Read (by id)** | `db.get_or_404(Book, id)` | `book = db.get_or_404(Book, book_id)` |
| **Update** | Retrieve object, modify, commit | `book.rating = 9; db.session.commit()` |
| **Delete** | `db.session.delete()`, commit | `db.session.delete(book); db.session.commit()` |

With these CRUD operations at your disposal, you can now build the fully functional, persistent virtual bookshelf. The next step is to integrate this database into the Flask website you built earlier, replacing the in‑memory list with database queries and adding the edit and delete features.

---