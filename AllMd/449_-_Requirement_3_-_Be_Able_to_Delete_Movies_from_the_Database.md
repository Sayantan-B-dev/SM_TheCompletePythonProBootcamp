# Requirement 3: Be Able to Delete Movies from the Database

## 1. Introduction

After enabling users to view and edit movie entries, the next natural feature is the ability to remove movies from the list. The “Delete” button on each movie card should permanently delete that movie record from the database. This requirement focuses on implementing a deletion mechanism that is both functional and safe, preventing accidental data loss.

By the end of this requirement, clicking the “Delete” button on any movie card will immediately remove that movie from the database and refresh the home page, showing the updated list.

---

## 2. Design Considerations for Deletion

### 2.1. HTTP Method: GET vs. POST

When implementing a delete action, it is important to consider the HTTP method used. Common practice dictates that operations which modify or delete data should be performed using **POST** (or DELETE, but HTML forms only support GET and POST). The reason is that GET requests are idempotent and should not cause side effects; they can be accidentally triggered by search engines, browser pre‑fetching, or a user simply clicking a link again.

If a delete action is implemented as a GET request (e.g., `<a href="/delete/1">Delete</a>`), a search engine crawler visiting that page could inadvertently delete a movie. Therefore, we will implement deletion using a **POST request** (via a small form) to ensure it is intentional.

### 2.2. CSRF Protection

Since we are using a POST request, we should also protect against Cross‑Site Request Forgery (CSRF) attacks. Flask‑WTF provides CSRF protection for all forms. We can either create a dedicated form for deletion or use a simple HTML form with a CSRF token.

---

## 3. Implementing the Delete Route

### 3.1. Adding the Route in `main.py`

In `main.py`, define a new route that accepts POST requests (and optionally GET for simplicity during development, but we will restrict to POST). The route will capture the `movie_id` from the URL, retrieve the corresponding movie, delete it, and redirect to the home page.

```python
from flask import redirect, url_for, request

@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    # Retrieve the movie or return 404 if not found
    movie = db.get_or_404(Movie, movie_id)
    # Delete the movie from the database session
    db.session.delete(movie)
    db.session.commit()
    # Redirect to the home page after successful deletion
    return redirect(url_for('home'))
```

**Explanation:**

- `@app.route("/delete/<int:movie_id>", methods=["POST"])` restricts this route to POST requests only. If someone tries to access it via GET, they will receive a `405 Method Not Allowed` error.
- `db.get_or_404(Movie, movie_id)` attempts to fetch the movie by its primary key. If no movie exists with that ID, a 404 error is raised automatically.
- `db.session.delete(movie)` marks the movie object for deletion.
- `db.session.commit()` executes the deletion and saves the change permanently.
- Finally, we redirect to the home page.

### 3.2. Handling GET Requests (Optional)

If you want to also allow GET requests during development (for quick testing), you can change `methods=["POST"]` to `methods=["GET", "POST"]`. However, for a production application, it is strongly recommended to keep it POST‑only and ensure the delete action is only triggered via a form submission.

---

## 4. Updating the Delete Button to Use POST

Currently, the `index.html` template likely contains a simple anchor tag (`<a>`) for the delete button, similar to:

```html
<a href="{{ url_for('delete', id=movie.id) }}" class="btn btn-danger">Delete</a>
```

This would send a GET request. To convert it to a POST request, we need to replace the anchor with a small HTML form that submits a POST request to the delete route. The form should include a CSRF token for security.

### 4.1. Creating a Delete Form with CSRF Token

We can either create a separate WTForm class for deletion (overkill) or simply embed a hidden CSRF token field using Flask‑WTF’s `csrf_token()` function. Since we are already using Bootstrap‑Flask and Flask‑WTF, the template can access the CSRF token via `{{ csrf_token() }}` if we ensure the template context includes it.

In `index.html`, inside the movie card’s back section, replace the anchor with:

```html
<form action="{{ url_for('delete', movie_id=movie.id) }}" method="POST" style="display: inline;">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
```

**Explanation:**

- The `action` attribute points to the delete route, passing the movie ID.
- `method="POST"` ensures the form is submitted using POST.
- The hidden input `csrf_token` carries the CSRF token. Flask‑WTF automatically validates this token on the server side.
- The button is styled as a Bootstrap danger button, matching the previous design.
- `style="display: inline;"` keeps the button inline with any surrounding elements.

### 4.2. Enabling CSRF Token in Templates

For the `{{ csrf_token() }}` function to be available, you must have `CSRFProtect` initialized, or simply ensure that Flask‑WTF’s CSRF protection is active (it is by default if `SECRET_KEY` is set). In `main.py`, after setting the secret key, you can optionally add:

```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

But Flask‑WTF automatically provides the `csrf_token` function to templates if the extension is loaded. The starter project likely already has this.

If you encounter issues where `csrf_token` is undefined, you can manually pass it via the render template context, but that is not typical.

---

## 5. Testing the Delete Functionality

1. Run the Flask application.
2. Navigate to the home page.
3. For any movie, click the **Delete** button (which is now a button inside a form).
4. The page should submit a POST request to `/delete/<id>`.
5. After processing, the browser redirects to the home page, and the deleted movie should no longer appear.
6. Verify that the movie has been removed from the database (using a database viewer or by checking the list).

If you try to access the delete URL directly by typing it into the browser’s address bar (GET request), you should receive a `405 Method Not Allowed` error, confirming that the route is correctly restricted to POST.

---

## 6. Error Handling and Edge Cases

### 6.1. Movie Not Found

If a user somehow submits a delete request for a movie ID that does not exist (e.g., manually crafting a URL with an invalid ID), `db.get_or_404` will raise a 404 error. Flask will display its default 404 page, which is acceptable.

### 6.2. Database Constraints

The `Movie` table does not have any foreign key relationships with other tables, so deletion is straightforward. If there were related data (e.g., comments table), we would need to consider cascading deletes or handling constraints, but that is not required here.

### 6.3. CSRF Validation Failure

If the CSRF token is missing or invalid, Flask‑WTF will reject the request and raise a `400 Bad Request` error. This protects against malicious submissions.

---

## 7. Alternative Approach: Using a WTForm for Deletion

For completeness, you could create a dedicated form class for deletion, but it is unnecessary. However, if you prefer a consistent approach across all forms, you can define a simple form:

```python
from flask_wtf import FlaskForm
class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
```

Then in the template:

```html
<form action="{{ url_for('delete', movie_id=movie.id) }}" method="POST">
    {{ delete_form.hidden_tag() }}
    {{ delete_form.submit(class="btn btn-danger") }}
</form>
```

And in the route, you would pass `delete_form` to the template. This approach adds more boilerplate but keeps everything within the WTForms ecosystem. For this requirement, the simple hidden CSRF token method is sufficient.

---

## 8. Complete Code Example for `main.py` (Relevant Sections)

```python
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RateMovieForm  # our edit form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    # ... model definition

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars().all()
    return render_template("index.html", movies=movies)

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    form = RateMovieForm(rating=movie.rating, review=movie.review)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 9. Summary

The delete functionality has been implemented with the following characteristics:

- A dedicated route `/delete/<int:movie_id>` that only accepts POST requests.
- Retrieval of the movie using `get_or_404` to handle missing records.
- Permanent removal from the database via SQLAlchemy session delete and commit.
- Conversion of the delete button from a GET link to a POST form with CSRF protection.
- Redirection back to the home page after deletion.

This ensures that users can safely remove movies they no longer wish to keep in their top 10 list. The next requirement will focus on adding new movies through an external API, allowing the list to grow beyond the initial sample entries.

---

## 10. Additional Notes

- **Browser Caching**: After deletion, the home page is reloaded, so the updated list appears immediately.
- **User Experience**: Consider adding a confirmation dialog (JavaScript confirm) before submitting the delete form to prevent accidental deletions. This can be done with a simple `onclick` attribute: `onclick="return confirm('Are you sure you want to delete this movie?');"`. This does not replace server‑side validation but improves usability.
- **RESTful Design**: In a more advanced API, you might use the HTTP DELETE method, but for standard browser‑based forms, POST is appropriate.

