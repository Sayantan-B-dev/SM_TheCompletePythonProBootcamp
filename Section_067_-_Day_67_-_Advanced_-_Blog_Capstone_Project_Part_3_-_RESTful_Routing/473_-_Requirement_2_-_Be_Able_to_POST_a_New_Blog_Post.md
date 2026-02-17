## Requirement 2 – Be Able to POST a New Blog Post

### Overview

Requirement 2 introduces the ability to create new blog posts through a web form. This involves:

- Creating a route `/new-post` that responds to both GET and POST requests.
- Designing a WTForm with fields for title, subtitle, author, image URL, and body.
- Integrating Flask-CKEditor to provide a rich text editing experience for the body field.
- Rendering the form in the `make-post.html` template using Bootstrap-Flask macros.
- Handling form submission: validating data, creating a new `BlogPost` instance, setting the publication date automatically, saving to the database, and redirecting to the home page.
- Ensuring the new post appears immediately on the home page.

This requirement adds the "Create" operation to the RESTful interface, completing the basic CRUD functionality.

### Prerequisites

Before implementing this requirement, ensure that:

- The application is configured with Flask-WTF and Flask-CKEditor (the starting project includes these in `requirements.txt`).
- The `BlogPost` model is defined and the database `posts.db` is accessible.
- The home route (`/`) correctly displays posts from the database (Requirement 1 completed).
- The template `make-post.html` exists (provided in the starting project) and is ready to be populated with form elements.

### Step 1: Create the WTForm Class

Flask-WTF extends WTForms and integrates with Flask. Define a form class that matches the fields of a blog post, using `CKEditorField` for the body.

**Code Example – Add to `main.py` (or a separate `forms.py`)**

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
```

**Explanation:**

- `StringField` creates a standard text input.
- `validators=[DataRequired()]` ensures the field is not empty.
- `URL()` validator checks that the image URL is properly formatted (optional but recommended).
- `CKEditorField` is provided by Flask-CKEditor and renders as a rich text editor.
- `SubmitField` creates a submit button.

### Step 2: Configure Flask-CKEditor

Flask-CKEditor requires initialization with the Flask app and may need additional configuration for local resources (or use a CDN). The starting project likely already has this setup, but verify:

**Code Example – in `main.py` after app creation**

```python
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'  # or 'standard', 'full'
ckeditor = CKEditor(app)
```

The `CKEDITOR_PKG_TYPE` determines which CKEditor package to load (basic, standard, full). The default is `basic`. For this project, any package that includes the toolbar for formatting is sufficient.

### Step 3: Create the New Post Route

Define a route `/new-post` that handles both GET and POST requests. For GET, it renders the form. For POST, it validates the submitted data, creates a new post, and redirects.

**Code Example – main.py**

```python
from datetime import date
from flask import render_template, redirect, url_for, request

@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        # Create a new BlogPost object
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")  # e.g., "March 15, 2025"
        )
        # Add to database and commit
        db.session.add(new_post)
        db.session.commit()
        # Redirect to home page
        return redirect(url_for('home'))
    # If GET request or validation fails, render the form
    return render_template("make-post.html", form=form)
```

**Explanation:**

- `methods=['GET', 'POST']` tells Flask this route accepts both HTTP methods.
- `form.validate_on_submit()` checks if the request is POST and if all validators pass. It also populates the form with submitted data.
- On successful validation, a new `BlogPost` instance is created using the form data.
- The `date` field is set to the current date formatted as "Month day, year" (e.g., "August 31, 2019"). This matches the expected format in the database and templates.
- The post is added to the database session and committed.
- After saving, the user is redirected to the home page (`url_for('home')`).
- If the request is GET or validation fails (e.g., missing fields), the `make-post.html` template is rendered with the form (which may show validation errors).

### Step 4: Update the `make-post.html` Template

The `make-post.html` template should render the WTForm using Bootstrap-Flask macros for consistent styling. Bootstrap-Flask provides `render_form()` which handles field rendering, errors, and CSRF tokens automatically.

**Code Example – templates/make-post.html**

```html
{% extends "layout.html" %}
{% from "bootstrap5/form.html" import render_form %}  <!-- or bootstrap4/form.html depending on version -->

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <h1>{% if request.endpoint == 'edit_post' %}Edit Post{% else %}New Post{% endif %}</h1>
            {{ render_form(form, novalidate=True) }}
            {{ ckeditor.load() }}  <!-- Load CKEditor JS -->
            {{ ckeditor.config(name='body') }}  <!-- Configure CKEditor for the body field -->
        </div>
    </div>
</div>
{% endblock %}
```

**Explanation:**

- The `{% from "bootstrap5/form.html" import render_form %}` imports the macro (adjust for Bootstrap version; starting project may use Bootstrap 4 or 5).
- `render_form(form, novalidate=True)` generates the entire form HTML, including fields, labels, and submit button. `novalidate` disables browser's built-in validation, allowing Flask-WTF validation to take precedence.
- `ckeditor.load()` and `ckeditor.config(name='body')` are provided by Flask-CKEditor. They inject the necessary JavaScript and configure CKEditor to target the field with name `body`. This must be placed after the form is rendered.

**Note on `request.endpoint`:** The conditional heading ("New Post" vs "Edit Post") uses `request.endpoint` to differentiate between the new post route and the future edit route. For now, it will always show "New Post" because the endpoint is `add_new_post` (or whatever you named the function). You can also pass a variable from the route to indicate edit mode.

### Step 5: Link the "Create New Post" Button

The home page (`index.html`) contains a "Create New Post" button that should point to the `/new-post` route. Update the anchor tag accordingly.

**Code Example – in index.html**

```html
<a href="{{ url_for('add_new_post') }}" class="btn btn-primary">Create New Post</a>
```

If the button already exists, ensure the `href` uses `url_for` with the correct function name.

### Step 6: Test the New Post Functionality

1. Run the Flask application.
2. Navigate to the home page (`http://127.0.0.1:5000/`).
3. Click the **Create New Post** button. You should be taken to `/new-post` and see the form with CKEditor for the body.
4. Fill out all fields. Write some formatted text in the body (e.g., bold, italics).
5. Click **Submit Post**.
6. After submission, you should be redirected to the home page. Verify that the new post appears in the list.
7. Click on the new post to view its full content. The body should display with the formatting you applied (because of the `|safe` filter in `post.html`).

If the post does not appear, check:

- Database connection and that the commit was successful.
- The home route queries all posts correctly.
- The date formatting is correct (e.g., "March 15, 2025").

### Detailed Explanation of Key Concepts

#### Flask-WTF Form Validation

`form.validate_on_submit()` combines two checks:

- Is the request method POST? If not, it returns `False`.
- Does all client-side and server-side validation pass? This includes CSRF token verification and field validators.

If validation fails, the form object contains error messages that can be displayed in the template (automatically handled by `render_form`).

#### CSRF Protection

Flask-WTF automatically includes a CSRF token field in the form. To use it, you must set a `SECRET_KEY` in the app configuration. The `render_form` macro includes this hidden field automatically.

#### CKEditor Integration

Flask-CKEditor simplifies adding CKEditor to text areas. The `CKEditorField` behaves like a `TextAreaField` but its rendering is replaced by the CKEditor JavaScript widget. The `ckeditor.load()` function adds the CKEditor library from a CDN, and `ckeditor.config(name='body')` initializes the editor for the specified field. By default, it uses the `basic` package; you can change the package type in the app config.

#### HTML Content and the `safe` Filter

CKEditor generates HTML markup for formatting (e.g., `<strong>bold</strong>`). When this content is stored in the database and later rendered in a template, Jinja escapes HTML by default for security. To render the HTML as intended, the `|safe` filter is applied: `{{ post.body|safe }}`. This tells Jinja that the content is trusted and should not be escaped.

**Security Note:** In a production environment, you should sanitize the HTML to remove potentially malicious scripts. For this tutorial, we assume the blog authors are trusted.

#### Date Formatting

The `date.today().strftime("%B %d, %Y")` method formats the date as "FullMonthName Day, FullYear". This matches the format used in the sample posts. Using `strftime` ensures consistency across different locales (though month names will be in English).

### Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| CKEditor does not appear; plain textarea is shown. | CKEditor JavaScript not loaded. | Ensure `{{ ckeditor.load() }}` and `{{ ckeditor.config(name='body') }}` are placed correctly in the template, after the form. Check that Flask-CKEditor is initialized in `main.py`. |
| Form submission results in 405 Method Not Allowed. | The route does not accept POST requests. | Add `methods=['GET', 'POST']` to the route decorator. |
| Validation errors not displaying. | `novalidate` not set, causing browser to block submission. | Use `novalidate=True` in `render_form` to bypass browser validation. |
| New post does not appear on home page. | Database commit may have failed. | Check for exceptions during commit. Add error handling or print commit result. Also verify the home route queries the database correctly. |
| Date format is incorrect. | Incorrect `strftime` directive. | Use `%B` for full month name, `%d` for day (with leading zero), `%Y` for four-digit year. Example: `date.today().strftime("%B %d, %Y")`. |
| CSRF token missing. | Secret key not set, or form rendering missing CSRF field. | Ensure `app.config['SECRET_KEY']` is set. The `render_form` macro includes the CSRF field automatically. |

### Next Steps

With the ability to create new posts, the blog now supports reading and writing. The next requirement will add editing functionality, allowing users to modify existing posts. This will reuse the same form but pre-populate it with existing data and update the record instead of creating a new one.

### Conclusion

Requirement 2 successfully implements the POST operation for creating new blog posts. By leveraging Flask-WTF for form handling and validation, Flask-CKEditor for rich text editing, and Bootstrap-Flask for clean form rendering, the application provides an intuitive interface for content creation. The integration of these extensions demonstrates how Flask's ecosystem simplifies common web development tasks while maintaining flexibility and control.