# Virtual Bookshelf: Integrating a SQLite Database into the Flask Website

## 1. Introduction

In the previous phases, we built a functional virtual bookshelf website using an in‑memory Python list (`all_books`) to store book data. While the website worked correctly during a single server session, all books disappeared when the server was restarted. This demonstrated the fundamental limitation of volatile storage.

Now, we will solve this problem by integrating a persistent **SQLite database** using **Flask‑SQLAlchemy**. We will replace the in‑memory list with database queries, ensuring that books added by users are saved permanently. Additionally, we will extend the application to support full **CRUD** (Create, Read, Update, Delete) operations, allowing users to edit book ratings and delete books from the shelf.

By the end of this phase, the virtual bookshelf will be a fully functional, database‑driven web application with the following features:

- Home page (`/`) displays all books stored in the database.
- Add page (`/add`) allows users to insert a new book (title, author, rating).
- Each book listing includes an **Edit Rating** link that takes the user to a page where they can update the rating.
- Each book listing includes a **Delete** link that removes the book from the database.
- All data persists across server restarts.

## 2. Prerequisites

Before starting, ensure you have:

- The Flask application from the previous challenges (files 438, 439) with the `main.py` and templates (`index.html`, `add.html`).
- A virtual environment with the required packages installed, including `Flask-SQLAlchemy` and `SQLAlchemy`. The `requirements.txt` (or `requirements_3.13.txt`) should list these dependencies. If not, install them:

  ```bash
  pip install flask-sqlalchemy
  ```

- Basic understanding of SQLAlchemy models and CRUD operations (covered in files 441–443).
- (Optional) DB Browser for SQLite to inspect the database file.

## 3. Step 1: Setting Up Flask‑SQLAlchemy

First, we need to integrate SQLAlchemy into our existing Flask application. Open `main.py` and modify the imports and configuration.

### 3.1 Imports

Add the necessary imports from `flask_sqlalchemy` and `sqlalchemy`. We will use the new 2.0 style with `Mapped` and `mapped_column`.

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
```

### 3.2 Create the Flask App and Configure the Database URI

```python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
```

This tells SQLAlchemy to use a SQLite database file named `books-collection.db` in the project root. If the file does not exist, it will be created automatically when we initialize the database.

### 3.3 Define the Base Class and Initialize SQLAlchemy

```python
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

This setup follows the Flask‑SQLAlchemy 3.x pattern. The `Base` class is required for the declarative model definition.

### 3.4 Define the Book Model

We need a model that represents a book in our database. It should match the structure we used for the in‑memory dictionary: `title`, `author`, `rating`, plus an `id` as the primary key.

```python
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```

**Explanation of constraints:**

- `unique=True` on `title` prevents duplicate book entries (assuming each book title is unique). This is a reasonable assumption for a personal library.
- `nullable=False` ensures that title, author, and rating are always provided.
- The `id` is an auto‑incrementing integer primary key.

### 3.5 Create the Database and Tables

With the model defined, we need to create the actual database tables. This should be done once when the application starts. We can place this inside an `app.app_context()` block.

```python
with app.app_context():
    db.create_all()
```

**Important:** The `create_all()` method will create tables only if they do not already exist. If you later modify the model (e.g., add a new column), you will need to either delete the database file and recreate it or use a migration tool like Alembic. For this project, we can simply delete the `.db` file and let it be recreated whenever we change the model.

Now the database is ready. The in‑memory `all_books` list is no longer needed; we will remove it and replace all operations with database calls.

## 4. Step 2: Updating the Home Route to Read from the Database

Previously, the home route rendered `index.html` with the `all_books` list. Now we will query all books from the database and pass them to the template.

```python
@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', books=all_books)
```

- `db.select(Book)` creates a SELECT query for the `Book` table.
- `.order_by(Book.title)` sorts the books alphabetically by title.
- `result.scalars().all()` returns a list of `Book` objects.
- We pass this list to the template as `books`.

The template `index.html` remains largely the same because it expects a list of objects with `title`, `author`, and `rating` attributes. The `Book` objects have exactly those attributes, so no changes are required in the template for displaying the list.

## 5. Step 3: Updating the Add Route to Insert into the Database

The `/add` route currently handles both GET (display form) and POST (process form). We will modify the POST section to create a new `Book` object and save it to the database.

```python
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Create a new Book object with data from the form
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=float(request.form['rating'])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')
```

**Note:** The form data arrives as strings. We convert `rating` to `float` because the model expects a float. If the user enters an invalid number, a `ValueError` will be raised; in a production application you would add error handling, but for simplicity we assume valid input.

## 6. Step 4: Adding an Edit Rating Feature

Now we need to allow users to change the rating of a book. We will add an **Edit** link next to each book on the home page. Clicking this link takes the user to a new page (`/edit/<int:book_id>`) with a form pre‑filled with the current rating. Submitting the form updates the rating in the database.

### 6.1 Update the Template `index.html`

Add an anchor tag after each book’s rating that links to the edit page. We’ll also add a delete link (covered in the next step). The updated list item might look like:

```html
<li>
    {{ book.title }} - {{ book.author }} - {{ book.rating }}/10
    <a href="{{ url_for('edit', book_id=book.id) }}">Edit Rating</a>
    <a href="{{ url_for('delete', book_id=book.id) }}">Delete</a>
</li>
```

The `url_for('edit', book_id=book.id)` generates a URL like `/edit/1` where `1` is the book’s primary key.

### 6.2 Create the Edit Route

We need a route that accepts both GET (to display the form) and POST (to process the update). The book’s id is captured from the URL.

```python
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    if request.method == 'POST':
        # Update the rating from the form
        book.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=book)
```

- `db.get_or_404(Book, book_id)` is a convenience method that fetches the book by its primary key. If no book with that id exists, it automatically raises a 404 error, which Flask will handle by showing a “Not Found” page. This saves us from writing explicit `if book is None: abort(404)`.
- If the request is POST, we update the book’s rating with the submitted value and commit. Then we redirect back to the home page.
- For a GET request, we render an `edit_rating.html` template, passing the `book` object so we can display its current rating and title.

### 6.3 Create the `edit_rating.html` Template

This template contains a simple form with a single field for the new rating. It should also display the book’s title and author for context.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Rating</title>
</head>
<body>
    <h1>Edit Rating for "{{ book.title }}"</h1>
    <p>Current rating: {{ book.rating }}</p>
    <form action="{{ url_for('edit', book_id=book.id) }}" method="POST">
        <label>New Rating:</label>
        <input type="number" step="0.1" name="rating" value="{{ book.rating }}" required>
        <button type="submit">Change Rating</button>
    </form>
    <a href="{{ url_for('home') }}">Back to Library</a>
</body>
</html>
```

The form’s action points back to the same `edit` route (which will process the POST). The input field is pre‑filled with the current rating using `value="{{ book.rating }}"`.

## 7. Step 5: Adding a Delete Feature

Similarly, we add a **Delete** link next to each book. Clicking it should delete the book from the database and redirect to the home page.

### 7.1 Create the Delete Route

We’ll define a route that accepts GET requests (since it’s just a link). In a real application, you might want to use POST for destructive actions, but for simplicity we’ll use GET.

```python
@app.route('/delete/<int:book_id>')
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
```

- The book is fetched by id; if not found, 404 is raised.
- `db.session.delete(book)` stages the deletion.
- `db.session.commit()` permanently removes the row from the database.
- Finally, redirect to the home page.

### 7.2 Update the Template (Already Done)

We already added the delete link in the `index.html` snippet above:

```html
<a href="{{ url_for('delete', book_id=book.id) }}">Delete</a>
```

Now the home page will show both Edit and Delete options for every book.

## 8. Step 6: Handling the Empty Library Message

In the original in‑memory version, the template displayed “Library is empty.” when the list was empty. With the database, the same logic works because we pass a possibly empty list of books. No changes are needed in the template for this condition.

However, we must ensure that the `books` variable passed to `index.html` is always a list (even if empty). Our `home` route does that with `all_books = result.scalars().all()`, which returns an empty list if there are no books.

## 9. Full Code of `main.py`

Here is the complete `main.py` with all routes and database integration:

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

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

if __name__ == '__main__':
    app.run(debug=True)
```

## 10. Updated Templates

### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Library</title>
</head>
<body>
    <h1>My Library</h1>
    {% if books %}
    <ul>
        {% for book in books %}
        <li>
            {{ book.title }} - {{ book.author }} - {{ book.rating }}/10
            <a href="{{ url_for('edit', book_id=book.id) }}">Edit Rating</a>
            <a href="{{ url_for('delete', book_id=book.id) }}">Delete</a>
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Library is empty.</p>
    {% endif %}
    <a href="{{ url_for('add') }}">Add New Book</a>
</body>
</html>
```

### `templates/add.html`

(No changes needed, but here it is for completeness.)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add a New Book</title>
</head>
<body>
    <h1>Add a New Book</h1>
    <form action="{{ url_for('add') }}" method="POST">
        <label>Book Name:</label>
        <input type="text" name="title" required><br>
        <label>Book Author:</label>
        <input type="text" name="author" required><br>
        <label>Rating:</label>
        <input type="number" step="0.1" name="rating" required><br>
        <button type="submit">Add Book</button>
    </form>
</body>
</html>
```

### `templates/edit_rating.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Rating</title>
</head>
<body>
    <h1>Edit Rating for "{{ book.title }}"</h1>
    <p>Current rating: {{ book.rating }}</p>
    <form action="{{ url_for('edit', book_id=book.id) }}" method="POST">
        <label>New Rating:</label>
        <input type="number" step="0.1" name="rating" value="{{ book.rating }}" required>
        <button type="submit">Change Rating</button>
    </form>
    <a href="{{ url_for('home') }}">Back to Library</a>
</body>
</html>
```

## 11. Testing the Application

1. Run `main.py`.
2. Visit `http://127.0.0.1:5000`. You should see “Library is empty.” and the “Add New Book” link.
3. Add a few books using the form. After each addition, you are redirected to the home page, and the new book appears in the list.
4. Click the **Edit Rating** link next to a book. You are taken to the edit page with the current rating pre‑filled. Change the rating and submit. You are redirected to the home page, and the rating is updated.
5. Click the **Delete** link next to a book. The book disappears from the list.
6. Stop the server (Ctrl+C) and restart it. Reload the home page – all books you added are still there. The data has persisted.

## 12. Additional Considerations

### 12.1 Unique Title Constraint

Because we set `unique=True` on the `title` field, attempting to add a book with a title that already exists will raise an `IntegrityError`. In a real application, you would catch this and show a user‑friendly error message (e.g., using Flask’s `flash` system). For now, the application will crash with a 500 error, which is acceptable for a learning exercise but should be addressed in production.

### 12.2 Input Validation

The form does not validate that the rating is a number between, say, 0 and 10. In a robust application, you would add both client‑side (HTML5 `min`/`max`) and server‑side validation.

### 12.3 Using `get_or_404`

This method is very convenient, but it only works inside a request context (i.e., within a route function). That’s perfect for our edit and delete routes.

### 12.4 Database File Location

The database file `books-collection.db` is created in the same directory as `main.py`. If you ever need to reset the database, simply delete this file and restart the application – the `db.create_all()` will recreate it with an empty table.

## 13. Summary

You have successfully built a persistent virtual bookshelf web application using Flask and SQLite. The key achievements are:

- Replaced in‑memory list with a SQLite database.
- Implemented full CRUD operations using SQLAlchemy ORM.
- Added edit and delete functionality with appropriate routes and templates.
- Ensured data persistence across server restarts.

This project demonstrates the core pattern of many web applications: storing user data in a database and providing an interface to manipulate it. You can now extend this application further – for example, by adding user authentication, sorting options, or a search feature.

## 14. Next Steps

- Explore Alembic for database migrations when you need to change the model schema without losing data.
- Add flash messages to provide feedback to the user (e.g., “Book added successfully”, “Rating updated”).
- Enhance the UI with CSS to make the bookshelf visually appealing.
- Deploy the application to a cloud platform (e.g., PythonAnywhere, Render) to make it publicly accessible.

Congratulations on completing the virtual bookshelf project!
