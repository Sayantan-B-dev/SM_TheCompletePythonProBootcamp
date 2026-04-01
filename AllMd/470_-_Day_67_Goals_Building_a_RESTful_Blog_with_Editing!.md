### Introduction

This documentation provides a comprehensive overview of the Day 67 project, which extends a basic blog application into a fully functional RESTful web application. The goal is to implement HTTP methods (GET, POST, PUT/PATCH, DELETE) to enable creation, editing, and deletion of blog posts directly from the web interface. The project builds upon previous blog implementations but replaces the external npoint JSON bucket with a local SQLite database managed by Flask-SQLAlchemy.

### Project Overview

The application is a blog website that displays a list of blog posts stored in an SQLite database (`posts.db`). Users can:

- View all posts on the home page.
- Click on a post to read its full content.
- Create new posts via a form.
- Edit existing posts.
- Delete posts.

All operations are performed through HTTP requests that correspond to RESTful conventions. The server is built with Flask and uses Flask-WTF for form handling, Flask-CKEditor for rich text editing, and Bootstrap-Flask for styling.

### RESTful API Design Principles

The application adheres to REST (Representational State Transfer) principles by using standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on blog post resources. Each blog post is identified by a unique `id` and is represented as a resource accessible via a URL.

#### HTTP Methods and Their Meanings

- **GET** – Retrieve a representation of a resource (e.g., list of posts, a single post).
- **POST** – Create a new resource (e.g., a new blog post).
- **PUT/PATCH** – Update an existing resource. (Note: HTML forms only support GET and POST, so the update is implemented via POST with a hidden method override or by using separate routes.)
- **DELETE** – Remove a resource.

### Planned Routes and Functionality

The application exposes the following routes:

| Route               | Method | Description                                                                 |
|---------------------|--------|-----------------------------------------------------------------------------|
| `/`                 | GET    | Home page displaying all blog posts retrieved from the database.           |
| `/post/<int:post_id>` | GET    | Individual post page showing full content of the post with given ID.       |
| `/new-post`         | GET    | Renders a form to create a new blog post.                                  |
| `/new-post`         | POST   | Processes the submitted form data, creates a new blog post in the database, and redirects to home. |
| `/edit-post/<int:post_id>` | GET    | Renders the form pre-populated with the existing data of the specified post for editing. |
| `/edit-post/<int:post_id>` | POST   | Updates the specified post with the submitted form data and redirects to the post's page. |
| `/delete/<int:post_id>` | GET/POST | Deletes the specified post from the database and redirects to home. (Typically implemented as POST to avoid accidental deletions via link prefetching.) |

**Note on HTTP Method Usage:**  
Although editing a resource is conceptually a PUT or PATCH request, HTML forms only support GET and POST. Therefore, the update operation is handled by a POST request to the same `/edit-post/<post_id>` route. The server distinguishes between rendering the form (GET) and updating the post (POST).

### Database Structure

The application uses an SQLite database named `posts.db` with a single table `posts` that contains the following columns (as defined by the SQLAlchemy model):

- `id` – Integer, primary key, auto-incremented.
- `title` – String (not nullable), the title of the post.
- `subtitle` – String (not nullable), the subtitle.
- `date` – String (not nullable), the publication date formatted as "Month day, year" (e.g., "August 31, 2019").
- `body` – Text (not nullable), the main content of the post (supports HTML from CKEditor).
- `author` – String (not nullable), the name of the author.
- `img_url` – String (not nullable), URL of the background image for the post.

The database is pre-populated with three sample posts to facilitate testing.

### Technologies Used

- **Flask** – Micro web framework for Python.
- **Flask-SQLAlchemy** – ORM for database interactions.
- **Flask-WTF** – Integration with WTForms for secure form handling.
- **Flask-CKEditor** – Adds a rich text editor to text areas.
- **Bootstrap-Flask** – Simplifies rendering Bootstrap components in templates.
- **Jinja2** – Templating engine for dynamic HTML generation.
- **SQLite** – Lightweight file-based database.

### Expected Outcome

Upon completion, the blog application will allow users to perform all CRUD operations via a user-friendly web interface. The home page will list all posts with titles, subtitles, authors, and dates. Clicking a post title navigates to the full post view. From there, an edit button leads to a pre-filled form, and a delete link (a ✘ character) removes the post. A "Create New Post" button opens an empty form. All changes are persisted in the SQLite database.

### Implementation Steps Overview

1. **Database Integration** – Modify the home route to query the `posts.db` and pass posts to the template instead of fetching from an external API.
2. **Individual Post Route** – Create a route that retrieves a post by its ID and renders the `post.html` template.
3. **New Post Form** – Build a WTForm class with fields for title, subtitle, author, img_url, and body. Use Flask-CKEditor for the body field.
4. **POST /new-post** – Handle form submission, create a new `BlogPost` object, set the date using `datetime`, and save to the database.
5. **Edit Post** – Create a route that accepts a post ID, queries the post, and renders the same form pre-populated with its data. Handle the POST request to update the record.
6. **Delete Post** – Add a route that deletes the post by ID and redirects to home. Place a delete link (✘) next to each post on the home page.

### Code Snippets (Illustrative)

#### Home Route (GET /)

```python
@app.route('/')
def home():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)
```

#### Individual Post Route (GET /post/<int:post_id>)

```python
@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)
```

#### New Post Form (WTForm)

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
```

#### Handling POST to /new-post

```python
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-post.html", form=form)
```

#### Edit Post (GET and POST)

```python
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)
```

#### Delete Post

```python
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
```

### Conclusion

This documentation outlines the architecture and functionality of the Day 67 RESTful Blog project. By implementing standard HTTP methods and routes, the application provides a complete CRUD interface for managing blog posts, demonstrating practical use of Flask extensions and RESTful design in a real-world scenario.