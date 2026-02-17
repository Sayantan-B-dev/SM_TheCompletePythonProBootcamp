## Requirement 1 – Be Able to GET Blog Post Items

### Overview

The first functional requirement transforms the existing blog application from fetching posts from an external JSON endpoint (npoint) to retrieving them from a local SQLite database (`posts.db`) using Flask-SQLAlchemy. This involves two key endpoints:

1. **Home Page (`/`)** – Displays a list of all blog posts stored in the database.
2. **Individual Post Page (`/post/<int:post_id>`)** – Displays the full content of a single post identified by its unique ID.

Both endpoints must correctly query the database and render the appropriate HTML templates (`index.html` and `post.html`) with the retrieved data.

### Prerequisites

Before implementing this requirement, ensure that:

- The Flask application is configured with SQLAlchemy and has a `BlogPost` model defined (as provided in the starting project).
- The database `posts.db` exists in the project root and contains the `posts` table with at least three sample records.
- The templates `index.html` and `post.html` are present in the `templates` folder and are designed to display post data.

### Implementation Steps

#### 1. Modify the Home Route to Retrieve All Posts

The home route (`/`) currently returns a placeholder or renders the template without data. Replace its implementation to query the database for all `BlogPost` records and pass them to the template.

**Code Example – main.py**

```python
from flask import render_template
from models import BlogPost  # Assuming the model is defined in main.py or imported
from app import db  # db instance

@app.route('/')
def home():
    # Execute a SELECT query on the BlogPost table and retrieve all rows
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)
```

**Explanation:**

- `db.select(BlogPost)` constructs a SQLAlchemy select statement for the `BlogPost` model.
- `db.session.execute(...)` executes the query and returns a `Result` object.
- `.scalars().all()` extracts the model instances from the result rows and returns them as a list.
- The list `posts` is passed to the template with the variable name `all_posts`.

**Template Adaptation (`index.html`)** – Ensure the template loops over `all_posts` and displays relevant fields:

```html
{% for post in all_posts %}
<div class="post-preview">
    <a href="{{ url_for('show_post', post_id=post.id) }}">
        <h2 class="post-title">{{ post.title }}</h2>
        <h3 class="post-subtitle">{{ post.subtitle }}</h3>
    </a>
    <p class="post-meta">
        Posted by {{ post.author }} on {{ post.date }}
        <!-- Delete icon placeholder -->
    </p>
</div>
{% endfor %}
```

The `url_for('show_post', post_id=post.id)` generates a link to the individual post page, which we will implement next.

#### 2. Create the Individual Post Route

Add a new route that captures a post ID from the URL, fetches the corresponding post from the database, and renders `post.html`. If the post does not exist, the application should return a 404 error.

**Code Example – main.py**

```python
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve the post by primary key or return 404 if not found
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)
```

**Alternative Query Method:**

```python
# Using explicit filter
requested_post = db.session.execute(
    db.select(BlogPost).where(BlogPost.id == post_id)
).scalar()
if not requested_post:
    abort(404)
```

The `db.get_or_404()` method is the most concise and automatically raises a 404 error if the record is missing.

**Template Adaptation (`post.html`)** – Display the full content of the post, ensuring the body (which may contain HTML) is rendered safely:

```html
<article class="mb-4">
    <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
            <div class="col-md-10 col-lg-8 col-xl-7">
                {{ post.body|safe }}
            </div>
        </div>
    </div>
</article>
<!-- Edit button placeholder -->
<a href="{{ url_for('edit_post', post_id=post.id) }}" class="btn btn-primary">Edit Post</a>
```

The `|safe` filter tells Jinja not to escape the HTML content, which is necessary because the CKEditor stores formatted HTML in the `body` field. (Note: In production, you may want to sanitize the HTML to prevent XSS attacks, but for this tutorial we assume trusted authors.)

#### 3. Verify Database Connectivity

After implementing the routes, restart the Flask development server. Navigate to `http://127.0.0.1:5000/`. You should see a list of posts populated from the database, each linking to its individual page. Click a post title to verify the individual post view renders correctly.

If no posts appear, check:

- The database file path in `SQLALCHEMY_DATABASE_URI` is correct (`sqlite:///posts.db` relative to the working directory).
- The `BlogPost` model matches the table schema (column names and types).
- The database contains data (use a tool like DB Browser for SQLite to inspect).

### SQLAlchemy Query Breakdown

Understanding the queries used is essential for debugging and further development.

- **`db.select(BlogPost)`** – Equivalent to SQL `SELECT * FROM posts`. It returns a `Select` object.
- **`db.session.execute(...)`** – Executes the query against the database session.
- **`.scalars()`** – Extracts the first element of each row (the model instance) instead of returning tuples.
- **`.all()`** – Fetches all results as a list.
- **`db.get_or_404(BlogPost, post_id)`** – Convenience method that performs a `SELECT ... WHERE id = post_id` and raises a 404 if no result.

### Expected Behavior

After completing this requirement:

- The home page displays all posts with their title, subtitle, author, and date.
- Clicking on a post title navigates to a page showing the full post content, including any HTML formatting.
- The edit button and delete icon are visible but not yet functional (they will be activated in later requirements).

### Code Placement and Organization

All route definitions should reside in `main.py` (or a dedicated routes module if refactored). The model definition is already present; ensure it is imported or defined before the routes that reference `BlogPost`.

### Summary

Requirement 1 establishes the core read functionality of the RESTful blog. By integrating Flask-SQLAlchemy, the application now retrieves data from a persistent database, making it suitable for dynamic content management. The next requirements will build upon this foundation to enable writing (POST), updating (PUT), and deleting (DELETE) operations.