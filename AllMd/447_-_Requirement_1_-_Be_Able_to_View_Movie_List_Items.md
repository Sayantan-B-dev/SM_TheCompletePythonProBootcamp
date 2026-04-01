# Requirement 1: Be Able to View Movie List Items

## 1. Introduction

The first step in building the Top 10 Movies website is to create a database that can store information about movies and then display that information on the home page. This requirement focuses on:

- Setting up a SQLite database using **Flask-SQLAlchemy**.
- Defining a `Movie` model (table) with the necessary fields.
- Adding at least two sample movie entries to the database.
- Querying all movies from the database when a user visits the home page.
- Passing the movie data to the `index.html` template so that it is rendered as movie cards.

By the end of this requirement, the home page will show the two sample movies with their details (title, year, description, rating, review, poster image). The ranking field will be populated later (Requirement 5), so initially it may appear as `None` or a placeholder.

---

## 2. Database Setup with Flask-SQLAlchemy

### 2.1. Why Use an ORM?

Flask-SQLAlchemy is an extension that provides an Object Relational Mapper (ORM) for Flask. It allows you to work with databases using Python classes and objects instead of writing raw SQL. This makes your code more readable, maintainable, and less prone to errors.

### 2.2. Configuring the Database in `main.py`

Open `main.py`. At the top, you should already have the necessary imports:

```python
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
```

Now, create the Flask app instance and configure the database URI. SQLite is a file‑based database, so we specify the path to the database file. By convention, SQLite databases are stored inside an `instance` folder, which Flask automatically creates if it doesn’t exist.

Add the following code after creating the `app` object:

```python
app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# Suppress a warning about tracking modifications (not needed for now)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the extension
db = SQLAlchemy(app)
```

- `SQLALCHEMY_DATABASE_URI` tells SQLAlchemy where the database file is located. `sqlite:///movies.db` means a file named `movies.db` will be created inside the `instance` folder.
- `SQLALCHEMY_TRACK_MODIFICATIONS = False` disables a feature that signals the application every time a change is about to be made to the database. This feature is not required for most projects and can be turned off to save memory.

### 2.3. Creating the `Movie` Model

A model is a Python class that corresponds to a database table. Each attribute of the class represents a column in the table. Define the `Movie` class below the database configuration:

```python
class Movie(db.Model):
    __tablename__ = 'movies'  # Optional: specify the table name (defaults to class name lowercase)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)   # Can be NULL initially
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
```

Explanation of each field:

- **id**: An integer that is the primary key. It uniquely identifies each record and auto‑increments.
- **title**: A string (max 250 characters) that must be unique. This prevents duplicate movies. It cannot be null (`nullable=False`).
- **year**: An integer representing the release year. Cannot be null.
- **description**: A longer string (max 500 characters) describing the movie. Cannot be null.
- **rating**: A float for the user’s rating. It is optional (`nullable=True`) because when we first add a movie via the API, the rating won’t be provided immediately.
- **ranking**: An integer for the movie’s position in the top 10. Also optional; will be assigned later.
- **review**: A string for the user’s personal review. Optional.
- **img_url**: A string containing the URL of the movie’s poster image. Cannot be null.

### 2.4. Creating the Database and Tables

With the model defined, we need to create the actual database file and the `movies` table. You can do this in a Python interactive shell, but a convenient way is to add a temporary block of code in `main.py` that runs only once.

After the model definition, add:

```python
with app.app_context():
    db.create_all()
```

- `app.app_context()` creates an application context, which is necessary for Flask extensions like SQLAlchemy to know which application they are working with.
- `db.create_all()` creates all tables that are defined as models (if they don’t already exist). It does **not** drop or modify existing tables.

Run the script once (e.g., by executing `main.py`). After execution, you will see a new folder named `instance` appear in your project directory. Inside it, you’ll find `movies.db`. You can open this file with a database viewer (like DB Browser for SQLite) to inspect the table structure.

**Important**: After the first run, you should either comment out or remove the `db.create_all()` line. If you leave it, it will run every time you start the app, but since the table already exists, nothing will change. However, it’s good practice to remove such setup code to avoid confusion later.

---

## 3. Adding Sample Movies

Now we need to insert at least two movies into the database so that we have something to display. There are several ways to do this:

- Using a Python script (temporarily) as shown below.
- Using a database GUI tool to manually insert records.

We’ll use Python code because it’s easy and fits into our development flow.

### 3.1. First Movie Entry

Add the following code **after** the `db.create_all()` line (or instead of it, if you’ve already created the table). This code creates a new `Movie` object and adds it to the database.

```python
with app.app_context():
    # Check if the movie already exists to avoid duplicate errors
    movie_exists = db.session.execute(db.select(Movie).where(Movie.title == "Phone Booth")).scalar()
    if not movie_exists:
        new_movie = Movie(
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )
        db.session.add(new_movie)
        db.session.commit()
        print("Phone Booth added to database.")
    else:
        print("Phone Booth already exists.")
```

Explanation:

- We use `db.session.execute()` with a SQLAlchemy select statement to check if a movie with the title "Phone Booth" already exists. This prevents trying to insert a duplicate, which would raise an `IntegrityError` because the `title` column is unique.
- `db.select(Movie).where(Movie.title == "Phone Booth")` builds a SELECT query.
- `.scalar()` returns the first result or `None`. It’s a convenient way to get a single value.
- If no movie is found, we create a new `Movie` instance and assign values to its attributes.
- `db.session.add(new_movie)` stages the object for insertion.
- `db.session.commit()` permanently saves the changes to the database.

### 3.2. Second Movie Entry

Similarly, add a second movie. You can place this code right after the first addition (still inside the `with app.app_context()` block) or in a separate block.

```python
    movie_exists = db.session.execute(db.select(Movie).where(Movie.title == "Avatar The Way of Water")).scalar()
    if not movie_exists:
        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        db.session.add(second_movie)
        db.session.commit()
        print("Avatar The Way of Water added to database.")
    else:
        print("Avatar The Way of Water already exists.")
```

After running this code once, the two movies will be in your database.

**Crucial**: Once the movies are added, you should **remove** or **comment out** this insertion code. If you leave it in, every time the application starts it will try to add the movies again, but the `if not movie_exists` check prevents duplicates. Still, it’s cleaner to keep your `main.py` focused on the application logic. A better approach is to run these insertions in a separate one‑time script, but for simplicity, you can just comment them out after the first run.

---

## 4. Displaying Movies on the Home Page

### 4.1. Querying All Movies

Now we need to modify the home route (which is likely defined as `@app.route("/")`) to fetch all movies from the database and pass them to the template.

Open `main.py` and locate the function that handles the home page (it might be named `home()`). It should look something like this:

```python
@app.route("/")
def home():
    # TODO: Query movies and render template
    return render_template("index.html")
```

Replace it with:

```python
@app.route("/")
def home():
    # Query all movies from the database
    result = db.session.execute(db.select(Movie).order_by(Movie.title))
    # .scalars() returns the actual Movie objects instead of rows
    movies = result.scalars().all()
    return render_template("index.html", movies=movies)
```

- `db.select(Movie)` creates a SELECT query for all columns of the `Movie` table.
- `.order_by(Movie.title)` sorts the results alphabetically by title (optional, but helps for consistent display).
- `db.session.execute()` runs the query and returns a `Result` object.
- `.scalars()` converts each row into a `Movie` instance (instead of a tuple). This is the recommended way to get model objects.
- `.all()` returns a list of all movies.
- Finally, we pass this list to the template using the keyword `movies`.

### 4.2. Understanding the Template

The `index.html` template (provided in the starter project) is designed to loop through a list called `movies` and render each movie as a card. It uses Jinja2 syntax. Here is a simplified snippet of what you might find:

```html
{% for movie in movies %}
<div class="card">
    <div class="front" style="background-image: url('{{ movie.img_url }}');">
        <p class="large">{{ movie.ranking if movie.ranking else "None" }}</p>
    </div>
    <div class="back">
        <div>
            <h2>{{ movie.title }}</h2>
            <span>{{ movie.year }}</span>
            <p>{{ movie.description }}</p>
            <p>{{ movie.rating }}</p>
            <p>{{ movie.review }}</p>
            <a href="{{ url_for('edit', id=movie.id) }}" class="btn btn-primary">Edit</a>
            <a href="{{ url_for('delete', id=movie.id) }}" class="btn btn-danger">Delete</a>
        </div>
    </div>
</div>
{% endfor %}
```

Notice how it uses `movie.ranking`, `movie.img_url`, etc. Since we haven’t assigned rankings yet, `movie.ranking` will be `None`, so the template displays “None” (as per the conditional `movie.ranking if movie.ranking else "None"`). That’s expected at this stage.

### 4.3. Testing the Home Page

Run your Flask application. In PyCharm, you can simply run `main.py`. Alternatively, in the terminal with the virtual environment activated, execute:

```bash
python main.py
```

You should see output indicating the server is running, typically on `http://127.0.0.1:5000/`. Open that URL in your browser. You should now see the two movie cards displayed with all their information (except ranking). The poster images should load from the provided TMDB URLs.

If you don’t see any movies, check the console for any errors. Common issues include:

- Database not created (run `db.create_all()` again).
- Movies not inserted (run the insertion code again).
- Template variable name mismatch (the template expects `movies`, so you must pass `movies=movies`).

---

## 5. Handling the Unique Constraint

The `title` field in the `Movie` model is set to `unique=True`. This means the database will reject any attempt to insert a second movie with the same title. This is good because it prevents duplicates. However, it also means you must handle that gracefully if you ever try to add a movie that already exists.

In our insertion code, we used a check (`movie_exists`) to avoid duplicate inserts. In the final application, when users add movies via the web interface, we will also need to check for duplicates and either update the existing entry or inform the user.

---

## 6. Verifying with a Database Viewer

To confirm that your database contains the correct data, you can use a tool like **DB Browser for SQLite** (free). Open the `movies.db` file located inside the `instance` folder. You should see a `movies` table with two rows containing the fields we defined.

This is also a good way to debug if something isn’t appearing on the website: you can directly check if the data is present in the database.

---

## 7. Summary

You have now completed the first requirement:

- Created a SQLite database with Flask‑SQLAlchemy.
- Defined a `Movie` model with all necessary columns.
- Added two sample movies programmatically, avoiding duplicates.
- Queried all movies in the home route and passed them to the template.
- Viewed the movies on the home page, correctly rendered from the database.

The next step is to implement the edit functionality (Requirement 2), allowing users to update the rating and review for each movie.

---

## 8. Additional Notes

- **Scalars vs. All**: In the query, we used `.scalars().all()`. If you only need to iterate once, you can use `.scalars()` directly in the template loop because it returns an iterator. However, `.all()` is clearer and often more efficient if you need to access the list multiple times.
- **Ordering**: We ordered by title for consistency, but later when we implement ranking, we will order by rating.
- **Removing Insertion Code**: After the first successful run, comment out or delete the insertion block to keep your code clean. You can always re‑run it if you need to reset the database.
- **Database Location**: The `instance` folder is automatically created by Flask when you use a relative path like `sqlite:///movies.db`. You can also specify an absolute path if you prefer.
