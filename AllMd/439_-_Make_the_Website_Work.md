# Virtual Bookshelf: Implementing the Basic Web Interface

## 1. Overview

In this phase, we build a functional but non‑persistent version of the virtual bookshelf. The goal is to implement five specific challenges that collectively create a working web application using only Python lists for storage. This serves as a foundation and a clear demonstration of why a database is necessary.

The application will have two pages:

- **Home page** (`/`): Displays a list of books (title, author, rating) and a link to add a new book.
- **Add page** (`/add`): Contains a form to submit a new book’s title, author, and rating. When submitted, the book is added to an in‑memory list, and the user is redirected back to the home page.

All data is stored in a global list named `all_books`. When the Flask server stops, this list is lost – a problem we will address in later lessons.

## 2. Prerequisites

Before starting, ensure you have:

- The starting project opened in PyCharm with a working virtual environment.
- Flask installed (as per `requirements.txt`).
- The HTML templates (`index.html` and `add.html`) present in the `templates/` folder.

If you haven’t set up the project yet, refer to the documentation for file `438`.

## 3. Challenge 1: Homepage with Title and Add Link

**Requirement:** When you visit `http://localhost:5000`, you should see an `<h1>` that says “My Library” and a link (`<a>`) to “Add New Book”.

### 3.1 The Flask Route

In `main.py`, we need a route for the home page. The route will render the `index.html` template and pass the list of books to it (even though the list may be empty initially).

```python
from flask import Flask, render_template

app = Flask(__name__)

# In‑memory storage
all_books = []

@app.route('/')
def home():
    return render_template('index.html', books=all_books)
```

### 3.2 The Template: `index.html`

The `index.html` file must contain an `<h1>` with the text “My Library” and a link to `/add`. Use Jinja2 to display the list of books later.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Library</title>
</head>
<body>
    <h1>My Library</h1>
    <a href="{{ url_for('add') }}">Add New Book</a>
</body>
</html>
```

The `url_for('add')` function generates the URL for the route named `add`. We will define that route next.

## 4. Challenge 2: Add Page with Form

**Requirement:** The `/add` path should display a form with fields for book title, author, and rating.

### 4.1 The Flask Route for `/add`

We need a route that handles both GET (display form) and POST (process form submission). For now, we only implement the GET part.

```python
from flask import Flask, render_template, request, redirect, url_for

# ... (previous code)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will handle POST in Challenge 3
        pass
    return render_template('add.html')
```

### 4.2 The Template: `add.html`

Create a simple HTML form that submits to the same URL (`/add`) using the POST method. The form should have three input fields: title (text), author (text), and rating (number, step="0.1" to allow decimals).

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

The `required` attribute provides basic client‑side validation. The `name` attributes are important – they will be used to retrieve the data in the Flask route.

## 5. Challenge 3: Form Handling to Add a Book

**Requirement:** When the form is submitted, the book details should be added as a dictionary to the list `all_books` in `main.py`. The dictionary structure must be:

```python
{
    "title": "Harry Potter",
    "author": "J. K. Rowling",
    "rating": 9
}
```

### 5.1 Processing the POST Request

Inside the `/add` route, handle the POST method by extracting form data and appending a new dictionary to `all_books`.

```python
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        author = request.form['author']
        rating = float(request.form['rating'])  # Convert to float

        # Create a new book dictionary
        new_book = {
            'title': title,
            'author': author,
            'rating': rating
        }

        # Append to the in‑memory list
        all_books.append(new_book)

        # Redirect to the home page
        return redirect(url_for('home'))
    return render_template('add.html')
```

**Explanation:**

- `request.form` is a dictionary-like object containing the form data. The keys correspond to the `name` attributes in the HTML form.
- `rating` is converted to `float` because form data is always submitted as strings. We want to store it as a number for potential calculations.
- After adding the book, we redirect to the home page. This prevents the form from being resubmitted if the user refreshes the page (POST/Redirect/GET pattern).

### 5.2 Data Structure Consistency

The `all_books` list now contains dictionaries exactly as required. Each dictionary has three keys: `title`, `author`, and `rating`. This structure will be used when displaying the books on the home page.

## 6. Challenge 4: Display Books on the Home Page

**Requirement:** The home page should show each book as a list item `<li>` in an unordered list `<ul>`. Each item should display the title, author, and rating.

### 6.1 Updating the `index.html` Template

We need to loop through the `books` list (passed from the route) and generate an `<li>` for each book. Use Jinja2’s `for` loop.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Library</title>
</head>
<body>
    <h1>My Library</h1>
    <ul>
        {% for book in books %}
        <li>{{ book.title }} - {{ book.author }} - {{ book.rating }}/10</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('add') }}">Add New Book</a>
</body>
</html>
```

**Note:** The `/10` suffix is optional but adds context to the rating. You can adjust the formatting as desired.

### 6.2 Testing the Display

- Start the Flask server.
- Navigate to the home page – you should see an empty list (because no books have been added yet).
- Go to `/add`, fill out the form, and submit. You will be redirected to the home page, and the new book should appear in the list.

## 7. Challenge 5: Handle Empty Library and Ensure Link Works

**Requirement:** If there are no books, the home page should show a paragraph `<p>` that says “Library is empty.” Also, ensure the “Add New Book” link works and takes the user to the `/add` page.

### 7.1 Conditional Rendering in the Template

We already have the link. Now we need to conditionally display the empty message when the `books` list is empty. Modify `index.html`:

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
        <li>{{ book.title }} - {{ book.author }} - {{ book.rating }}/10</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Library is empty.</p>
    {% endif %}
    <a href="{{ url_for('add') }}">Add New Book</a>
</body>
</html>
```

**Explanation:**

- `{% if books %}` checks if the `books` list is not empty. In Jinja2, an empty list evaluates to `False`.
- If there are books, the unordered list is rendered.
- If the list is empty, the paragraph “Library is empty.” is shown.

### 7.2 Verifying the Link

The link uses `url_for('add')`, which we have already defined. Clicking it should navigate to `/add` and display the form. This works regardless of whether there are books or not.

## 8. Complete Code for `main.py`

Here is the full `main.py` after implementing all five challenges:

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In‑memory storage
all_books = []

@app.route('/')
def home():
    return render_template('index.html', books=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = float(request.form['rating'])

        new_book = {
            'title': title,
            'author': author,
            'rating': rating
        }
        all_books.append(new_book)
        return redirect(url_for('home'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## 9. Running and Testing the Application

1. Run `main.py` (e.g., right‑click and select **Run 'main'** in PyCharm, or execute `python main.py` in the terminal with the virtual environment activated).
2. Open your browser to `http://127.0.0.1:5000`.
3. You should see “My Library” and “Library is empty.” with a link “Add New Book”.
4. Click the link, fill out the form (e.g., Title: “Harry Potter”, Author: “J.K. Rowling”, Rating: 9), and click “Add Book”.
5. You are redirected to the home page, and the book appears in the list.
6. Add another book to confirm multiple entries.
7. Stop the server (Ctrl+C in the terminal or click the stop button in PyCharm) and restart it. Reload the home page – the books are gone.

## 10. What We Have Learned

- How to create Flask routes for GET and POST requests.
- How to render templates with dynamic data using Jinja2.
- How to handle form submissions and extract data with `request.form`.
- How to use the POST/Redirect/GET pattern to avoid duplicate submissions.
- How to conditionally display content in templates based on whether a list is empty.
- The limitation of in‑memory storage: data is lost when the server restarts.

## 11. Preview: The Need for a Database

The final observation in Challenge 5 highlights the fundamental problem: any data added is lost when the application stops. In a real‑world scenario, users expect their data to persist. The next lessons will introduce **SQLite** and **SQLAlchemy** to store books in a database, making the data permanent. We will also add features to edit ratings and delete books, which are natural extensions of the CRUD operations.

## 12. Troubleshooting Tips

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| **404 Not Found** when accessing `/add`. | The route for `/add` is not defined, or the method is not allowed. | Ensure the route is defined with `methods=['GET', 'POST']`. |
| **Form submission returns 405 Method Not Allowed**. | The route does not accept POST. | Add `methods=['POST']` or `['GET', 'POST']` to the route decorator. |
| **KeyError: 'title'** when submitting form. | The form field `name` does not match the key used in `request.form`. | Check that the `name` attributes in the HTML form exactly match `'title'`, `'author'`, `'rating'`. |
| **Books disappear after server restart**. | This is expected behavior with in‑memory storage. | Proceed to the next lessons to add a database. |
| **Template not found** (Jinja2 exception). | The HTML file is not in the `templates/` folder, or the folder name is misspelled. | Ensure `templates/` exists in the same directory as `main.py` and contains `index.html` and `add.html`. |

---