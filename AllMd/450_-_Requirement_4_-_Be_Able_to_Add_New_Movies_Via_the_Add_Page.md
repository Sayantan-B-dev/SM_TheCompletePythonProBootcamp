# Requirement 4: Be Able to Add New Movies Via the Add Page

## 1. Introduction

The fourth requirement introduces the ability for users to add new movies to their list dynamically, without having to modify the database manually. Previously, we inserted sample movies using hard‑coded Python code. Now, we will build a user‑friendly interface that allows any user to search for a movie by its title, select the correct film from search results, and automatically populate the database with details fetched from **The Movie Database (TMDB) API**. After adding the movie, the user is redirected to the edit page so they can immediately provide a rating and review.

This feature consists of several interconnected steps:

- An “Add Movie” button on the home page leads to a simple form (movie title only).
- Submitting the form triggers a search against the TMDB API.
- The search results are displayed on a selection page, showing each movie’s title and release year.
- The user picks one movie; its unique TMDB ID is used to fetch full details (poster, description, year) from the API.
- A new `Movie` record is created with these details and saved to the database.
- Finally, the user is redirected to the edit page for that movie to add a rating and review.

By the end of this requirement, the application will be fully functional: users can add any movie they wish, and the list will grow organically.

---

## 2. Prerequisites

Before starting, ensure you have:

- A free account on [The Movie Database (TMDB)](https://www.themoviedb.org/).
- An API key (v3 auth) from TMDB. To obtain one:
  1. Log in to your TMDB account.
  2. Go to **Settings → API**.
  3. Click **Create** or **Request an API Key** and fill out the required form (you may need to provide a brief description of your app).
  4. Once approved, you will receive an API key (a long alphanumeric string). Copy it.
- The `requests` library installed. It is already listed in `requirements.txt`, but if not, install it with `pip install requests`.

---

## 3. The Add Movie Form

### 3.1. Create a WTForm for the Title

We need a simple form with one field: the movie title. Create a new form class in `forms.py` (or add it to the existing file).

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")
```

This form:

- Uses `StringField` for the title input.
- Requires the field to be filled (`DataRequired`).
- Includes a submit button labelled “Add Movie”.

### 3.2. The Add Route

In `main.py`, create a new route `/add` that handles both GET (display the form) and POST (process the submitted title). We will later expand the POST part to call the TMDB API.

```python
from forms import FindMovieForm

@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        # User submitted a title – we will search TMDB
        movie_title = form.title.data
        # TODO: Call TMDB search API and show results
        return redirect(url_for('select'))  # placeholder
    return render_template("add.html", form=form)
```

- The route is accessible at `/add`.
- On GET, it renders `add.html` with an empty form.
- On POST with valid data, it retrieves the title and (for now) redirects to a placeholder `select` route. We will replace this with actual logic.

### 3.3. The `add.html` Template

The starter project includes an `add.html` file. Ensure it uses Bootstrap‑Flask to render the form. It should look similar to:

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Add Movie{% endblock %}

{% block content %}
<div class="content">
    <h1 class="heading">Add a Movie</h1>
    {{ render_form(form, novalidate=True) }}
</div>
{% endblock %}
```

This template:

- Extends a base template (presumably with Bootstrap styling).
- Imports the `render_form` macro.
- Renders the `FindMovieForm` passed from the route.

---

## 4. Integrating The Movie Database API – Search

### 4.1. TMDB Search Endpoint

TMDB provides a search endpoint:

```
https://api.themoviedb.org/3/search/movie
```

Required parameters:

- `api_key` – your TMDB API key.
- `query` – the movie title to search for.

Optional parameters (useful for refining): `language`, `page`, `include_adult`, etc. We will keep it simple.

### 4.2. Performing the Search

Modify the `/add` route to call the API when the form is submitted. We will store the API key in the app configuration or as an environment variable. For simplicity, add it directly to `main.py` (but in production, use environment variables).

```python
import requests

TMDB_API_KEY = "your_api_key_here"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        # Make request to TMDB search API
        response = requests.get(
            TMDB_SEARCH_URL,
            params={
                "api_key": TMDB_API_KEY,
                "query": movie_title
            }
        )
        data = response.json()
        # Extract the list of results (movies)
        results = data.get("results", [])
        # Pass results to a new template (select.html)
        return render_template("select.html", options=results)
    return render_template("add.html", form=form)
```

- We use `requests.get()` with parameters.
- `response.json()` parses the JSON response into a Python dictionary.
- The `results` key contains a list of matching movies. Each movie in the list has fields like `id`, `title`, `release_date`, `overview`, `poster_path`, etc.
- We render a new template `select.html` and pass the results as `options`.

### 4.3. Handling No Results

If the search returns no results, we might want to inform the user. For simplicity, you could flash a message and re-render the add form. Example:

```python
if not results:
    flash("No movies found with that title. Please try again.")
    return render_template("add.html", form=form)
```

You would need to import `flash` from flask and add a block in the base template to display flashed messages.

---

## 5. The Select Page

### 5.1. Purpose

The `select.html` page presents the user with a list of movies returned from the API. Each item should display the movie title and year, and be clickable to select that movie. Clicking will send the TMDB movie ID to the server for detail retrieval.

### 5.2. Template Design

The starter project likely already contains a `select.html` template. We need to ensure it correctly displays the list and provides a way to submit the chosen ID. A typical implementation uses a form for each movie, or a link that includes the ID as a query parameter.

Here’s a possible implementation using a simple anchor tag with a query parameter:

```html
{% extends "base.html" %}

{% block title %}Select Movie{% endblock %}

{% block content %}
<div class="content">
    <h1 class="heading">Select a Movie</h1>
    {% for movie in options %}
    <p>
        <a href="{{ url_for('find', id=movie.id) }}">
            {{ movie.title }} - {{ movie.release_date[:4] if movie.release_date else "N/A" }}
        </a>
    </p>
    {% endfor %}
</div>
{% endblock %}
```

- We loop through `options` (the list of movies from the API).
- For each movie, we display a link. The link points to a new route `/find` (which we will create) and passes the movie’s TMDB `id` as a parameter.
- We extract the year from `release_date` (which is in YYYY-MM-DD format) by slicing the first four characters. If no release date, we show “N/A”.

Alternatively, you could use a form with hidden input for each movie, but a simple GET link is fine because we are just selecting an item, not modifying data. However, we must be careful: this GET request will trigger a database write (creating the movie). That is acceptable in this context because it’s part of a multi-step process, but it's worth noting that normally data modification should be POST. Since the actual creation happens in the `/find` route, and that route could be called directly, we might want to protect it with a POST. We'll discuss this later.

### 5.3. Creating the “Find” Route

This route receives the TMDB movie ID, fetches full details, creates a new `Movie` record, and redirects to edit.

```python
@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        # Fetch movie details from TMDB
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(
            movie_api_url,
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            }
        )
        data = response.json()
        # Extract required fields
        title = data["title"]
        # The release date might be missing; handle gracefully
        year = data.get("release_date", "Unknown")[:4] if data.get("release_date") else "Unknown"
        # Some movies may not have a poster; provide a default placeholder
        img_url = f"{TMDB_IMAGE_BASE_URL}{data['poster_path']}" if data.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Poster"
        description = data.get("overview", "No description available.")
        
        # Create new Movie object
        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            rating=None,
            ranking=None,
            review=None,
            img_url=img_url
        )
        db.session.add(new_movie)
        db.session.commit()
        # Redirect to edit page for this new movie
        return redirect(url_for('edit', movie_id=new_movie.id))
    else:
        # No ID provided; redirect to add page
        return redirect(url_for('add'))
```

Explanation:

- We extract `id` from the query string using `request.args.get("id")`.
- We then call the TMDB **movie details** endpoint: `https://api.themoviedb.org/3/movie/{movie_id}`. This returns comprehensive data about the movie.
- From the response, we extract the title, year (from release_date), poster path, and overview.
- For the poster, we construct the full URL using the base image URL `https://image.tmdb.org/t/p/w500` plus the `poster_path` value. If `poster_path` is `None` (some movies don’t have a poster), we provide a placeholder image URL.
- For the description, we use `overview`. If missing, provide a default string.
- We create a new `Movie` instance with the fetched data. Note that `rating`, `ranking`, and `review` are initially `None`.
- After adding and committing to the database, we redirect to the edit page for that movie (`/edit/<movie_id>`), which we built in Requirement 2.

### 5.4. Handling Errors

If the movie ID is invalid or the API call fails, we should handle it gracefully. For example, wrap the API call in a try/except and redirect with an error message. But for simplicity, we assume the ID is valid.

---

## 6. Complete Workflow

Now, let’s trace the entire process:

1. User clicks “Add Movie” on the home page. This link points to `/add`.
2. On the `/add` page, user enters a movie title and submits the form (POST).
3. The server queries TMDB search, gets results, and renders `select.html` with the list.
4. User clicks on the desired movie (a link to `/find?id=12345`).
5. The `/find` route fetches details from TMDB, creates a database record, and redirects to `/edit/123` (where 123 is the new database ID, not TMDB ID).
6. The edit page shows the form pre‑filled with empty rating/review. User enters values and submits.
7. After submission, the movie is updated with rating/review and appears on the home page with its ranking (to be implemented in Requirement 5).

---

## 7. Full Code Example

Here’s how the relevant parts of `main.py` and `forms.py` should look after adding this feature.

### `forms.py`

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

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")
```

### `main.py` (relevant sections)

```python
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RateMovieForm, FindMovieForm
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

TMDB_API_KEY = "your_api_key_here"  # Better to use os.environ.get("TMDB_API_KEY")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

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

@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(
            TMDB_SEARCH_URL,
            params={
                "api_key": TMDB_API_KEY,
                "query": movie_title
            }
        )
        data = response.json()
        results = data.get("results", [])
        if not results:
            flash("No movies found. Please try again.")
            return render_template("add.html", form=form)
        return render_template("select.html", options=results)
    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if not movie_id:
        return redirect(url_for('add'))
    
    # Fetch movie details from TMDB
    response = requests.get(
        f"{TMDB_DETAILS_URL}/{movie_id}",
        params={
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
    )
    data = response.json()
    
    # Extract data with fallbacks
    title = data.get("title", "Unknown Title")
    year = data.get("release_date", "Unknown")
    if year != "Unknown":
        year = year[:4]  # Extract year from YYYY-MM-DD
    img_path = data.get("poster_path")
    if img_path:
        img_url = f"{TMDB_IMAGE_BASE_URL}{img_path}"
    else:
        img_url = "https://via.placeholder.com/500x750?text=No+Poster"
    description = data.get("overview", "No description available.")
    
    # Create new movie entry
    new_movie = Movie(
        title=title,
        year=year,
        description=description,
        rating=None,
        ranking=None,
        review=None,
        img_url=img_url
    )
    db.session.add(new_movie)
    db.session.commit()
    
    return redirect(url_for('edit', movie_id=new_movie.id))

if __name__ == "__main__":
    app.run(debug=True)
```

### Template: `add.html`

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Add Movie{% endblock %}

{% block content %}
<div class="content">
    <h1 class="heading">Add a Movie</h1>
    {{ render_form(form, novalidate=True) }}
</div>
{% endblock %}
```

### Template: `select.html`

```html
{% extends "base.html" %}

{% block title %}Select Movie{% endblock %}

{% block content %}
<div class="content">
    <h1 class="heading">Select a Movie</h1>
    {% for movie in options %}
    <p>
        <a href="{{ url_for('find_movie', id=movie.id) }}">
            {{ movie.title }} - {{ movie.release_date[:4] if movie.release_date else "N/A" }}
        </a>
    </p>
    {% endfor %}
</div>
{% endblock %}
```

Note: In the anchor tag, we use `find_movie` as the endpoint name (the function name). If you used `find`, adjust accordingly.

### Template: `edit.html` (unchanged from Requirement 2)

---

## 8. Testing the Add Flow

1. Run the Flask application.
2. On the home page, click the **Add Movie** button (you may need to add this button to `index.html`; it should be present in the starter project). If not, add a link to `/add`.
3. Enter a movie title, e.g., “Inception”, and submit.
4. You should see a list of movies matching “Inception” with their titles and years.
5. Click on the correct movie (e.g., “Inception – 2010”).
6. The application should redirect to the edit page for that movie, with the form empty (rating and review fields blank).
7. Enter a rating and review, click **Done**.
8. You are redirected to the home page, where the new movie appears with its details (except ranking, which will be handled later).

Check that the poster image loads correctly. If the movie has no poster, the placeholder should appear.

---

## 9. Important Considerations

### 9.1. Unique Title Constraint

The `Movie` model enforces `title` as unique. If a user tries to add a movie that already exists in the database, the `db.session.commit()` will raise an `IntegrityError`. To handle this gracefully, we should check for duplicates before inserting. For example, before creating `new_movie`, query the database for an existing movie with the same title:

```python
existing_movie = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
if existing_movie:
    flash("Movie already in your list.")
    return redirect(url_for('edit', movie_id=existing_movie.id))
```

This would redirect to the edit page of the existing movie instead of creating a duplicate. However, note that the API might return a slightly different title; perfect matching might not catch all duplicates. A more robust approach could use fuzzy matching, but for this project, exact title match is sufficient.

### 9.2. Security of API Key

Hard‑coding the API key in `main.py` is not safe for production. In a real application, store it in an environment variable and access it via `os.environ.get("TMDB_API_KEY")`. The starter project may have instructions for this.

### 9.3. Rate Limiting

TMDB API has rate limits. If you make too many requests in a short time, you might be temporarily blocked. For a personal project, this is rarely an issue, but be mindful.

### 9.4. Error Handling in `/find`

The `/find` route assumes the API call succeeds. In practice, you should wrap the request in a try/except block and handle possible exceptions (e.g., connection errors, invalid JSON). A simple improvement:

```python
try:
    response = requests.get(...)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    flash("Error contacting TMDB. Please try again.")
    return redirect(url_for('add'))
```

### 9.5. CSRF and GET Request for `/find`

Note that the `/find` route is accessed via GET (from the link in `select.html`). This route creates a new database record. According to REST principles, data‑modifying operations should use POST. However, in this flow, the selection page is rendered after a POST (search), and the link is essentially a continuation of that process. To be safe, you could change the selection mechanism to a form with POST, but that adds complexity. For the purpose of this project, using GET is acceptable. If you want to follow best practices, you could implement the selection as a form that POSTs the movie ID to a different route.

---

## 10. Summary

You have now implemented the complete “Add Movie” feature:

- Created a form for entering a movie title.
- Integrated with the TMDB API to search for movies.
- Displayed search results to the user.
- Allowed selection of a specific movie.
- Fetched full movie details from the API.
- Created a new database record with those details.
- Redirected the user to the edit page to add a rating and review.

The application now supports adding any movie from TMDB’s extensive catalog. The final requirement will involve sorting and ranking the movies based on their ratings.
