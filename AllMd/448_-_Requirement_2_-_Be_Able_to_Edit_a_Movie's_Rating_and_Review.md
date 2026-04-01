# Requirement 2: Be Able to Edit a Movie's Rating and Review

## 1. Introduction

After successfully displaying the movie list on the home page, the next logical step is to allow users to modify the details of a movie. The most common updates are the **rating** (a numerical score) and the **personal review** (text). This requirement focuses on building an edit page that:

- Appears when the user clicks the “Edit” button on any movie card.
- Presents a form pre‑filled with the current rating and review of that movie.
- Allows the user to change these values and submit them.
- Updates the corresponding record in the database and redirects back to the home page.

By the end of this requirement, the edit functionality will be fully operational, and users will be able to fine‑tune their movie rankings.

---

## 2. Why Use WTForms?

WTForms is a flexible forms validation and rendering library for Python web frameworks. It integrates seamlessly with Flask via the **Flask-WTF** extension (which we have installed as part of the requirements). Using WTForms provides several advantages:

- **Validation**: Automatically check that the rating is a number, that the review text is within a certain length, etc.
- **CSRF Protection**: Built‑in protection against Cross‑Site Request Forgery attacks.
- **HTML Rendering**: With Bootstrap‑Flask, we can render forms with Bootstrap styling effortlessly.
- **Security**: Helps prevent malicious input.

The starter project already includes Bootstrap‑Flask, so we can take advantage of its `render_form()` macro to quickly generate styled forms.

---

## 3. Creating the RateMovieForm

We need a form class that defines the fields we want on the edit page. According to the requirement, the form should contain two fields: **rating** (a float) and **review** (a text area). We’ll also include a submit button.

Create a new file called `forms.py` in the root directory of your project (next to `main.py`). This keeps form definitions separate from application logic. Alternatively, you can define the form inside `main.py`, but separating concerns is cleaner.

### 3.1. Install Flask-WTF (if not already)

Check your `requirements.txt`. It should include `Flask-WTF`. If not, you can add it and run `pip install -r requirements.txt`. The starter project likely includes it.

### 3.2. Define the Form

In `forms.py`, write:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class RateMovieForm(FlaskForm):
    rating = FloatField(
        "Your Rating Out of 10 e.g. 7.5",
        validators=[
            DataRequired(message="Rating is required."),
            NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
        ]
    )
    review = StringField(
        "Your Review",
        validators=[
            DataRequired(message="Review cannot be empty."),
            Length(min=1, max=250, message="Review must be between 1 and 250 characters.")
        ]
    )
    submit = SubmitField("Done")
```

Explanation:

- `FlaskForm` is the base class for all WTForms in Flask. It adds CSRF protection automatically.
- `FloatField` renders as an `<input type="text">` but expects a floating‑point number. The label "Your Rating Out of 10 e.g. 7.5" will be displayed next to the field.
- `StringField` is used for the review. We could also use `TextAreaField` for a larger input box, but `StringField` works fine. If you prefer a multi‑line input, change it to `TextAreaField`.
- `validators`:
  - `DataRequired()` ensures the field is not empty.
  - `NumberRange(min=0, max=10)` restricts the rating to a sensible range.
  - `Length(min=1, max=250)` limits the review length. Adjust max to match your database column size (the `review` field in the `Movie` model is `String(250)`).
- `SubmitField` creates a submit button labelled "Done".

---

## 4. Setting Up the Edit Route

In `main.py`, we need to create a new route that handles both GET requests (to display the form) and POST requests (to process the submitted form).

### 4.1. Import the Form and Required Modules

At the top of `main.py`, add:

```python
from forms import RateMovieForm
from flask import request, redirect, url_for, render_template
```

(You may already have `render_template` imported.)

### 4.2. Define the Route

Add the following code below the home route:

```python
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    # Retrieve the movie from the database by its primary key
    movie = db.get_or_404(Movie, movie_id)
    # Create the form, passing the current movie data if it's a GET request
    form = RateMovieForm(
        rating=movie.rating,
        review=movie.review
    )
    
    if form.validate_on_submit():
        # Update the movie record with form data
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        # Redirect to the home page after successful update
        return redirect(url_for('home'))
    
    # For GET requests (or if validation fails), render the edit template
    return render_template("edit.html", movie=movie, form=form)
```

Detailed explanation:

- **URL Parameter**: `<int:movie_id>` captures the movie’s ID from the URL (e.g., `/edit/1`). Flask converts it to an integer and passes it to the function.
- **db.get_or_404(Movie, movie_id)**: This is a convenient SQLAlchemy method that tries to fetch the movie with the given primary key. If it doesn’t exist, it automatically raises a 404 error, which Flask turns into a “Not Found” page. This is safe and avoids manual error handling.
- **Pre‑populating the form**: We create an instance of `RateMovieForm` and pass the current `rating` and `review` values as keyword arguments. This fills the form fields with the existing data when the page is first loaded.
- **form.validate_on_submit()**: This WTForms method checks two things:
  1. If the request method is POST (i.e., the form was submitted).
  2. If all validators pass.
  If both are true, we proceed to update the movie.
- **Updating**: We assign the new values from `form.rating.data` and `form.review.data` to the movie object’s attributes. Then `db.session.commit()` saves the changes.
- **Redirect**: After a successful update, we redirect the user back to the home page. This is a common pattern (Post/Redirect/Get) to prevent duplicate form submissions if the user refreshes the page.
- **GET request**: If the user just navigates to the edit URL (or if validation fails), we render `edit.html` and pass the movie and form objects.

---

## 5. Creating the Edit Template

The starter project likely includes an `edit.html` file. However, we need to ensure it uses Bootstrap‑Flask to render the form nicely. Open `templates/edit.html` and verify its contents. It should contain something like:

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Edit Movie{% endblock %}

{% block content %}
<div class="content">
  <h1 class="heading">{{ movie.title }}</h1>
    <p class="description">Edit Movie Rating and Review</p>
    {{ render_form(form, novalidate=True) }}
  </div>
{% endblock %}
```

Key points:

- `{% from 'bootstrap5/form.html' import render_form %}` imports the Bootstrap‑Flask macro that generates a fully styled form.
- `{{ render_form(form, novalidate=True) }}` renders the form. `novalidate=True` disables the browser’s built‑in validation, allowing our server‑side validation to take over.
- The form will automatically include CSRF protection (a hidden field) because `FlaskForm` adds it.

If the template doesn’t have these lines, update it accordingly. Bootstrap‑Flask version 5 is used here; if you’re using an older version, the import path might be `bootstrap/wtf.html`. Check your Bootstrap‑Flask documentation.

---

## 6. Linking the Edit Button

Now we need to make the “Edit” button on the home page actually point to the correct edit URL. In `index.html`, you should have a line similar to:

```html
<a href="{{ url_for('edit', id=movie.id) }}" class="btn btn-primary">Edit</a>
```

Ensure that the `url_for` uses the correct endpoint name (`'edit'` – the function name we defined) and passes the `id` parameter (which matches `<int:movie_id>`). If you named the function `edit_movie`, you would use `url_for('edit_movie', id=movie.id)`.

---

## 7. Testing the Edit Functionality

1. **Start your Flask application** (run `main.py`).
2. Navigate to the home page (`http://127.0.0.1:5000/`).
3. Click the **Edit** button on any movie card. You should be taken to a URL like `/edit/1`.
4. The edit page should display the movie title and a form pre‑filled with the current rating and review.
5. Change the rating and/or review and click **Done**.
6. You should be redirected to the home page, and the updated information should appear on the movie card.

Try submitting invalid data (e.g., rating above 10, empty review). The form should redisplay with error messages (if you have set up the template to show them). Bootstrap‑Flask’s `render_form` automatically displays validation errors next to the fields.

---

## 8. Handling Validation Errors

WTForms automatically adds error messages to the form object when validation fails. Bootstrap‑Flask’s `render_form` will display these errors if the form is passed back to the template. In our `edit` route, if `form.validate_on_submit()` returns `False`, we simply re‑render the template with the form (which now contains the errors). The user will see the same page with helpful messages.

For example, if the user enters a rating of 11, the message “Rating must be between 0 and 10.” will appear.

---

## 9. CSRF Protection

Flask-WTF automatically includes a CSRF token in every form. This token is a hidden field that must be present and valid when the form is submitted. If the token is missing or incorrect, the submission is rejected. This protects your site from malicious requests from other domains.

Bootstrap‑Flask’s `render_form` automatically includes the CSRF field, so you don’t need to add it manually. Ensure your app has a secret key configured (Flask needs it for CSRF). In `main.py`, set:

```python
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'  # Use a strong, random key in production
```

This key should be kept secret. The starter project may already have one.

---

## 10. Complete Code Example for `main.py` (Relevant Sections)

Here’s how the relevant parts of `main.py` should look after implementing the edit feature:

```python
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RateMovieForm  # import our form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    # ... model definition as before

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.title))
    movies = result.scalars().all()
    return render_template("index.html", movies=movies)

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    form = RateMovieForm(
        rating=movie.rating,
        review=movie.review
    )
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

# ... other routes (delete, add) will be added later

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 11. Summary

You have now implemented the edit functionality:

- Created a WTForm (`RateMovieForm`) with validation.
- Added an `/edit/<int:movie_id>` route that handles both displaying and processing the form.
- Pre‑populated the form with existing data.
- Updated the database on valid submission.
- Linked the edit button from the home page.
- Ensured CSRF protection and validation errors are displayed.

The next requirement will focus on the **delete** feature, allowing users to remove movies from the database entirely.

---

## 12. Additional Considerations

- **Rating Precision**: The `rating` field is a float. You may want to restrict it to one decimal place. You can add a `InputRequired()` validator or use a `DecimalField` with rounding. However, the current setup is sufficient.
- **Review Length**: The model allows up to 250 characters; the form validator enforces that. If you need more, adjust both.
- **Error Handling**: In the edit route, if the movie is not found, `get_or_404` handles it. If the database update fails for some reason, consider wrapping in a try/except and rolling back.
- **Bootstrap Version**: Ensure your `base.html` includes Bootstrap CSS and JavaScript. The starter project likely already does.

