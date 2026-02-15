# SQLAlchemy: Object Relational Mapping for Python Databases

## 1. Introduction to SQLAlchemy

SQLAlchemy is a powerful SQL toolkit and Object Relational Mapping (ORM) library for Python. It provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access. The ORM layer maps database tables to Python classes, rows to instances of those classes, and columns to instance attributes. This allows developers to work with databases using familiar Python objects and methods instead of writing raw SQL strings, which are error‑prone and harder to maintain.

In the context of our virtual bookshelf project, SQLAlchemy will replace the raw `sqlite3` commands with a more Pythonic and robust interface. We will use **Flask‑SQLAlchemy**, an extension that integrates SQLAlchemy with Flask, providing useful defaults and helpers.

**Why use an ORM?**

- **Abstraction** – You work with objects, not SQL. This makes code more readable and maintainable.
- **Portability** – The same Python code can work with different database backends (SQLite, PostgreSQL, MySQL) with minimal changes.
- **Security** – ORMs automatically escape values, preventing SQL injection attacks.
- **Productivity** – You can define relationships and queries using Python syntax; the ORM generates efficient SQL.
- **IDE support** – With type hints, your IDE can provide auto‑completion and detect errors early.

## 2. Prerequisites

Before proceeding, ensure you have:

- The virtual bookshelf project set up with a virtual environment.
- The required packages installed. The `requirements.txt` file should include:
  - `Flask`
  - `Flask-SQLAlchemy`
  - `SQLAlchemy`
  (The specific versions are listed in the file; for Python 3.13, a `requirements_3.13.txt` is provided.)

If not already installed, run:

```bash
pip install -r requirements.txt
```

We will start a new Python script (or reuse the existing `main.py` after commenting out the previous code) to experiment with SQLAlchemy independently before integrating it into the Flask application.

## 3. Setting Up Flask‑SQLAlchemy

Flask‑SQLAlchemy is a wrapper around SQLAlchemy that simplifies configuration and session management. We need to import the necessary classes and initialize the extension with our Flask app.

### 3.1 Import Statements

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
```

- `Flask` – the web framework.
- `SQLAlchemy` – the main extension class.
- `DeclarativeBase` – a base class for defining models using the new declarative mapping style (introduced in SQLAlchemy 2.0). It replaces the older `declarative_base()` function.
- `Mapped` – a generic type that indicates a mapped attribute; used with type hints.
- `mapped_column` – a function to define column properties with type hints.
- `Integer`, `String`, `Float` – SQLAlchemy data types.

### 3.2 Create the Flask App and Configure Database URI

```python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
```

The `SQLALCHEMY_DATABASE_URI` tells SQLAlchemy which database to connect to. The format for SQLite is `sqlite:///path/to/file.db`. Using three slashes after the colon indicates a relative path; absolute paths can be specified with four slashes (e.g., `sqlite:////absolute/path.db`).

### 3.3 Define the Declarative Base Class

```python
class Base(DeclarativeBase):
    pass
```

This class will serve as the base for all our database models. It is required by Flask‑SQLAlchemy to set up the declarative mapping.

### 3.4 Initialize the SQLAlchemy Object

```python
db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

We create an instance of `SQLAlchemy`, passing our custom `Base` class as `model_class`. Then we call `init_app(app)` to bind it to the Flask application.

## 4. Defining a Model (Table)

A model is a Python class that represents a database table. Each attribute of the class corresponds to a column in the table. We will define a `Book` model with the same fields as before: `id`, `title`, `author`, `rating`.

### 4.1 Model Class Definition

```python
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```

**Explanation:**

- `class Book(db.Model)` – Inherits from `db.Model`, which is the base class for all models in Flask‑SQLAlchemy.
- `id: Mapped[int]` – Uses type hints to declare that `id` is an integer column. The `Mapped` type indicates that this attribute is mapped to a database column.
- `= mapped_column(Integer, primary_key=True)` – Configures the column: data type `Integer`, and it is the primary key.
- `title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)` – A string column with maximum length 250, must be unique, and cannot be NULL.
- `author: Mapped[str] = mapped_column(String(250), nullable=False)` – Similar to title but without the uniqueness constraint.
- `rating: Mapped[float] = mapped_column(Float, nullable=False)` – A float column that cannot be NULL.

**Note:** The `mapped_column` function replaces the older `db.Column` syntax. It works seamlessly with type hints and provides better IDE integration.

## 5. Creating the Database and Tables

With the model defined, we need to create the actual database file and the `books` table. This is done within an **application context**, because Flask‑SQLAlchemy needs access to the app’s configuration.

```python
with app.app_context():
    db.create_all()
```

The `create_all()` method inspects all models that inherit from `db.Model` and creates the corresponding tables in the database. If the database file does not exist, it will be created. If the tables already exist, this method does nothing (it will not overwrite or alter them).

Run this code once. After execution, you should see a file named `new-books-collection.db` in your project directory. You can open it with DB Browser to verify that the `books` table exists with the correct columns.

## 6. Creating a New Record (INSERT)

To add a new book, we create an instance of the `Book` class and add it to the database session, then commit the transaction.

```python
with app.app_context():
    new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()
```

**Explanation:**

- `Book(id=1, ...)` – Creates a new `Book` object. The `id` field is optional; if omitted, SQLite will auto‑generate an id because `INTEGER PRIMARY KEY` columns auto‑increment by default.
- `db.session.add(new_book)` – Stages the object to be inserted into the database. The session tracks changes.
- `db.session.commit()` – Flushes the session to the database, executing the INSERT statement and making the change permanent.

After committing, the book is stored in the database. You can verify by querying (see next section) or by using DB Browser.

**Alternative without specifying id:**

```python
new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
```

In this case, SQLite will assign the next available integer as the id.

## 7. Reading Records (SELECT)

To verify that the book was inserted, we can retrieve all records.

### 7.1 Read All Records

```python
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    for book in all_books:
        print(f"{book.title} by {book.author}, rating: {book.rating}")
```

- `db.select(Book)` creates a SELECT query for the `Book` table.
- `.order_by(Book.title)` orders the results by title.
- `db.session.execute()` runs the query and returns a `Result` object.
- `.scalars()` returns the rows as scalar objects (i.e., `Book` instances) instead of tuples.
- `.all()` fetches all results as a list.

### 7.2 Read a Specific Record by Title

```python
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    if book:
        print(book.rating)
```

`.scalar()` returns a single `Book` object, or `None` if no record matches.

## 8. Complete Example Script

Here is the complete code combining all steps, with comments:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Define base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Define Book model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Insert a new book
with app.app_context():
    new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()

# Read and print all books
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    books = result.scalars().all()
    for book in books:
        print(f"{book.title} - {book.author} - {book.rating}")

if __name__ == "__main__":
    app.run(debug=True)
```

**Note:** The `if __name__ == "__main__"` block is only for running the Flask development server. The database operations above will run regardless of whether the server is started. If you want to separate database setup from server startup, you can comment out the insertion after the first run.

## 9. The Challenge

Now it’s your turn to apply this knowledge. Using the instructions above, you must:

1. Create an SQLite database called `new-books-collection.db`.
2. Define a `Book` model with the fields: `id` (INTEGER, primary key), `title` (VARCHAR(250), unique, not null), `author` (VARCHAR(250), not null), `rating` (FLOAT, not null).
3. Provide the Flask app context and create the database schema (tables).
4. Within the app context, create a new entry with `id: 1`, `title: "Harry Potter"`, `author: "J. K. Rowling"`, `rating: 9.3`.

You can test your work by using DB Browser to inspect the database.

## 10. Solution to the Challenge

The solution is essentially the code provided in Section 8. Ensure you have imported the correct classes and used the `with app.app_context()` blocks appropriately.

**Checklist for success:**

- The database file `new-books-collection.db` appears after running.
- The table `books` exists with four columns.
- A row with id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3 is present.

## 11. Common Pitfalls and Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| **`sqlalchemy.exc.OperationalError: no such table`** | The table was not created because `db.create_all()` was not called, or was called before the model was defined. | Ensure `db.create_all()` is called after all models are defined and within an app context. |
| **`sqlalchemy.exc.IntegrityError: UNIQUE constraint failed`** | You tried to insert a book with a title that already exists. | Use a different title, or delete the existing record before inserting again. |
| **`AttributeError: 'NoneType' object has no attribute 'driver'`** | The database URI is malformed. | Check that the URI string starts with `sqlite:///` and the path is correct. |
| **`RuntimeError: Working outside of application context`** | You attempted a database operation without being inside an `app.app_context()` block. | Wrap the operation with `with app.app_context():`. |
| **Table not visible in DB Browser** | The database file may have been created in a different directory. | Check the full path; use an absolute path in the URI if needed. Also, ensure you close DB Browser before running Python (file locking). |

## 12. Next Steps

Now that you have successfully used SQLAlchemy to create a database, define a model, and insert a record, you are ready to perform full CRUD operations. The next lesson will cover:

- Reading all records to display on the home page.
- Updating a book’s rating.
- Deleting a book.
- Integrating these operations into the Flask routes of the virtual bookshelf website.

You will replace the in‑memory `all_books` list with database queries, making the data persistent and enabling editing and deletion features.
