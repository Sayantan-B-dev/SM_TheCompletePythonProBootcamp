## 494 - Requirement 4 - Allow Any User to Add Comments to BlogPosts

This document outlines the implementation of user comments in the blog application. With user authentication and relational database structures already in place, the next logical feature is to enable registered users to leave comments on blog posts. This involves creating a new `Comment` model, establishing relationships with `User` and `BlogPost`, building a comment form using CKEditor, and updating the post page to display comments with user avatars via Gravatar.

By the end of this phase, the blog will support a community interaction layer where any logged‑in user can post comments, and all visitors can read them. Comments will be properly linked to both the author (user) and the post, ensuring data integrity and enabling future features like comment moderation or editing.

### Prerequisites

- User authentication (login, logout, registration) is fully implemented (Requirement 2).
- The `User` and `BlogPost` models are correctly defined, with a one‑to‑many relationship between them (Requirement 3).
- Flask‑WTF and CKEditor are available; if not already installed, run:
  ```bash
  pip install flask-ckeditor
  ```
- The application’s database is currently using the schema from Requirement 3 (i.e., `blog_posts` table has `author_id` foreign key).

### Step 1: Create the Comment Form with CKEditorField

In `forms.py`, define a new form class `CommentForm`. This form will contain a single field for the comment text, using `CKEditorField` to provide a rich text editing experience (similar to the blog post body). CKEditor allows users to format text, add links, etc., and stores the content as HTML.

**Example: CommentForm in forms.py**

```python
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_ckeditor import CKEditorField

class CommentForm(FlaskForm):
    comment_text = CKEditorField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')
```

**Explanation**:

- `CKEditorField` is a special field provided by the `Flask-CKEditor` extension. It renders as a rich text editor in the browser.
- The `DataRequired()` validator ensures the comment is not empty.
- A submit button is included for form submission.

**Note**: Ensure that `Flask-CKEditor` is initialized in your main application. Typically, this is done in `main.py`:

```python
from flask_ckeditor import CKEditor
ckeditor = CKEditor(app)
```

Also, include the CKEditor resources in your base template. For Bootstrap‑Flask, you may need to add the following to the `<head>` section of your base layout:

```html
{{ ckeditor.load() }}
```

Refer to the [Flask-CKEditor documentation](https://flask-ckeditor.readthedocs.io/) for more details.

### Step 2: Create the Comment Table

Now we need a database model to store comments. Create a new model class `Comment` that inherits from `db.Model`. It will contain:

- An auto‑incrementing primary key `id`.
- A `text` field to hold the comment content (HTML).
- Foreign keys to link the comment to a user and to a post.
- Relationships to navigate to the author and the post.

**Example: Comment model in main.py (or models.py)**

```python
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

    # Relationships (to be completed in steps 3 and 4)
    # author = relationship("User", back_populates="comments")
    # post = relationship("BlogPost", back_populates="comments")
```

**Explanation**:

- `text` stores the comment content, which may include HTML tags from CKEditor.
- `created_at` records when the comment was posted. Defaults to the current UTC time.
- `author_id` and `post_id` are foreign keys that reference the `users` and `blog_posts` tables respectively. They are marked `nullable=False` to enforce that every comment must belong to a user and a post.
- Relationships are commented out for now; they will be fully defined in the next steps after modifying the related models.

### Step 3: Establish One‑to‑Many Relationship Between User and Comment

Each user can write many comments, and each comment belongs to a single user. This is a classic one‑to‑many relationship. We need to add a `comments` relationship to the `User` model and link it to the `Comment` model.

**Update the User model (add relationship)**

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    # Existing relationship to posts
    posts = relationship("BlogPost", back_populates="author")

    # New relationship to comments
    comments = relationship("Comment", back_populates="author")
```

**Update the Comment model (add the reverse relationship)**

Uncomment and complete the `author` relationship in `Comment`:

```python
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

    # Relationship to User
    author = relationship("User", back_populates="comments")

    # Relationship to BlogPost (to be added next)
    # post = relationship("BlogPost", back_populates="comments")
```

**Explanation**:

- `User.comments` is a list of `Comment` objects associated with that user.
- `Comment.author` gives the `User` object who wrote the comment.
- The `back_populates` argument ensures that the two sides of the relationship are kept in sync. For example, if you add a comment to `user.comments`, SQLAlchemy automatically sets `comment.author` to that user.

### Step 4: Establish One‑to‑Many Relationship Between BlogPost and Comment

Similarly, each blog post can have many comments, and each comment belongs to one post. Add a `comments` relationship to the `BlogPost` model and link it to the `Comment` model.

**Update the BlogPost model**

```python
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Relationship to User
    author = relationship("User", back_populates="posts")

    # New relationship to comments
    comments = relationship("Comment", back_populates="post")
```

**Update the Comment model (complete the reverse relationship)**

```python
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("BlogPost", back_populates="comments")
```

**Explanation**:

- `BlogPost.comments` gives a list of all comments for a given post.
- `Comment.post` gives the `BlogPost` object that the comment belongs to.
- With these relationships in place, we can easily access, for example, all comments for a post in a template: `post.comments`.

### Step 5: Re‑create the Database (Handle Schema Changes)

Adding the `Comment` table and its foreign keys changes the database schema. As before, we will delete the existing `blog.db` file and let SQLAlchemy create a fresh database with all tables (users, blog_posts, comments) based on the updated models.

**Procedure**:

1. **Stop the Flask server** if it is running.
2. **Delete the `blog.db` file** from your project root. Ensure it is permanently removed.
3. **Restart the Flask server**. SQLAlchemy will create a new, empty `blog.db` with the correct schema.
4. **Register the first user** (admin). This user will have `id = 1`.
5. **Create a new blog post** using the admin account. This will populate the `blog_posts` table with one post linked to the admin.
6. **Register a second user** (e.g., a regular reader). This user will have `id = 2` (assuming the first user is id 1). This user will later post comments.

At this point, the database contains:
- One admin user.
- One blog post authored by the admin.
- One regular user.

No comments exist yet, but the `comments` table is ready.

### Step 6: Restrict Comment Submission to Authenticated Users

The `/post/<int:post_id>` route currently handles displaying a single post. We need to enhance it to:

- Instantiate and validate the `CommentForm` on POST requests.
- If the form is valid, create a new `Comment` object linked to the current user and the current post.
- Save the comment to the database.
- Redirect back to the same post page to show the new comment.
- On GET requests, simply render the post page with the comment form.

Crucially, we must ensure that **only logged‑in users can submit comments**. If an unauthenticated user tries to submit a comment, they should be redirected to the login page with a flash message.

**Implementation in main.py**

```python
from flask_login import login_required, current_user
from forms import CommentForm
from models import BlogPost, Comment
from flask import render_template, redirect, url_for, flash, request

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    # Retrieve the blog post by id (or 404 if not found)
    post = BlogPost.query.get_or_404(post_id)

    # Instantiate the comment form
    form = CommentForm()

    if form.validate_on_submit():
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('You need to log in to leave a comment.', 'info')
            return redirect(url_for('login', next=request.url))  # Pass the current page as 'next'

        # Create new comment
        new_comment = Comment(
            text=form.comment_text.data,
            author_id=current_user.id,
            post_id=post.id
        )
        db.session.add(new_comment)
        db.session.commit()

        flash('Your comment has been posted.', 'success')
        return redirect(url_for('show_post', post_id=post.id))

    # For GET requests, simply render the page with the form and existing comments
    return render_template('post.html', post=post, form=form)
```

**Explanation**:

- `form.validate_on_submit()` returns `True` only on POST requests and when all validators pass.
- The check `if not current_user.is_authenticated` ensures only logged‑in users can proceed. If the user is not authenticated, we flash a message and redirect to the login page. Importantly, we pass the current URL as a `next` parameter (`request.url`) so that after successful login, the user is redirected back to this post page. (The login route must handle the `next` parameter appropriately, as implemented in Requirement 2.)
- If the user is authenticated, we create a new `Comment` object, populating its fields with the current user’s ID and the post’s ID. The `created_at` will automatically be set to the current time due to the `default=datetime.utcnow` in the model.
- After adding and committing, we flash a success message and redirect back to the same post page (using a redirect to avoid form resubmission on page refresh).
- For a GET request, we simply render the template, passing the post and an empty form.

**Note on the `next` parameter**: The login route must be modified to use `request.args.get('next')` and redirect to that URL after login. This was already covered in Requirement 2, but ensure it is implemented.

### Step 7: Display Comments on the Post Page

Now that comments are being saved, we need to display them on the post page. The `post.html` template should iterate over `post.comments` (the list of comments associated with the post) and render each comment with its author’s name and the comment text.

**Update post.html**

```html
{% extends "base.html" %}
{% from 'bootstrap5/form.html' import render_form %}

{% block content %}
<div class="container">
    <h1>{{ post.title }}</h1>
    <p class="post-meta">Posted by {{ post.author.name }} on {{ post.date }}</p>
    <img src="{{ post.img_url }}" class="img-fluid" alt="...">
    <div class="post-body">
        {{ post.body|safe }}
    </div>

    <hr>

    <!-- Comments Section -->
    <h3>Comments</h3>
    <div class="comments">
        {% for comment in post.comments %}
        <div class="comment">
            <p class="comment-author">{{ comment.author.name }} said on {{ comment.created_at.strftime('%B %d, %Y') }}:</p>
            <div class="comment-text">
                {{ comment.text|safe }}
            </div>
        </div>
        <hr>
        {% else %}
        <p>No comments yet. Be the first to comment!</p>
        {% endfor %}
    </div>

    <!-- Comment Form -->
    {% if current_user.is_authenticated %}
        <h4>Leave a Comment</h4>
        {{ render_form(form) }}
    {% else %}
        <p><a href="{{ url_for('login', next=request.path) }}">Log in</a> to leave a comment.</p>
    {% endif %}
</div>
{% endblock %}
```

**Explanation**:

- `post.comments` is the list of comments for this post, thanks to the relationship defined in `BlogPost`.
- We loop through `post.comments` and display the author’s name (`comment.author.name`) and the comment text.
- The `|safe` filter is necessary because the comment text contains HTML from CKEditor. Without it, Jinja would escape the HTML, displaying raw tags.
- The `comment.created_at` is formatted using `strftime` to show a human‑readable date.
- If there are no comments, an `{% else %}` clause inside the `for` loop displays a placeholder message.
- The comment form is only rendered if the user is logged in; otherwise, a login link is shown. Note that we also include the `next` parameter in the login link to preserve the intended return URL.

**Important**: Ensure that `created_at` is a `datetime` object. In the model, we set `default=datetime.utcnow`. However, if you store the date as a string, you might need to adjust formatting accordingly. The example above assumes a `datetime` field.

### Step 8: Add Gravatar Images to Comments

Gravatar (Globally Recognized Avatar) is a service that provides profile images based on a user’s email address. It is widely used in comment sections to give each user a unique avatar. We will integrate `Flask-Gravatar` to automatically generate avatar URLs for each commenter.

**Installation**:

```bash
pip install flask-gravatar
```

**Initialize in main.py**:

```python
from flask_gravatar import Gravatar

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=True,
                    base_url=None)
```

The parameters configure the default avatar size, rating, and fallback image (here we use 'retro' as a fun default). Refer to the [Flask-Gravatar documentation](https://github.com/zzzsochi/Flask-Gravatar) for more options.

**Update post.html to include avatars**:

Modify the comment display loop to include an image tag using the gravatar URL. We can generate the gravatar URL by calling `gravatar.url` with the user’s email.

```html
{% for comment in post.comments %}
<div class="comment d-flex">
    <img src="{{ gravatar.url(comment.author.email) }}" alt="Avatar" class="rounded-circle me-3" width="50" height="50">
    <div>
        <p class="comment-author">{{ comment.author.name }} said on {{ comment.created_at.strftime('%B %d, %Y') }}:</p>
        <div class="comment-text">
            {{ comment.text|safe }}
        </div>
    </div>
</div>
<hr>
{% else %}
<p>No comments yet. Be the first to comment!</p>
{% endfor %}
```

**Explanation**:

- `gravatar.url(comment.author.email)` generates the Gravatar URL for the user’s email. If the user has an account on Gravatar, their chosen image appears; otherwise, the default image (retro) is shown.
- We wrap the image and comment text in a flex container (`d-flex`) to align the avatar nicely.
- The avatar is styled with `rounded-circle` for a circular shape and `me-3` for margin.

Now every comment will display the author’s avatar, enhancing the visual appeal of the comment section.

### Testing the Complete Flow

1. **As a logged‑out user**: Navigate to a post page. You should see existing comments (if any) but the comment form should be replaced with a “Log in to leave a comment” link. Clicking the link should take you to the login page with the `next` parameter set to the post URL. After logging in, you should be redirected back to the post page and see the comment form.

2. **As a logged‑in user (not admin)**: Log in with the second user (reader). On a post page, you should see the comment form. Submit a comment. You should be redirected back to the same post page, and your comment should appear at the top (or bottom depending on ordering) with your avatar, name, and comment text. Check the database to verify the comment was stored with the correct `author_id` and `post_id`.

3. **As the admin user**: Log in as admin. The comment form should still be visible (admins can also comment). Post a comment; it should appear with the admin’s avatar and name.

4. **Ordering of comments**: By default, comments are retrieved in the order they were added (ascending by `id`). You may want to display the newest first. To do so, you can modify the relationship to include an order_by clause, or in the template you can sort the list. For example, in the route, you could query comments in descending order and pass them separately, but using the relationship, you can do:

   ```python
   post = BlogPost.query.get_or_404(post_id)
   comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
   return render_template('post.html', post=post, comments=comments, form=form)
   ```

   Then in the template, loop over `comments` instead of `post.comments`. Choose whichever approach fits your design.

### Troubleshooting

- **CKEditor not loading**: Ensure that `{{ ckeditor.load() }}` is included in the base template’s `<head>` and that the CKEditor instance is properly configured.
- **Comment not saving**: Check that the form validates (e.g., required field). Also, ensure that `current_user.id` is not `None` (user is logged in). If using a separate `models.py`, verify that the `Comment` model is imported correctly.
- **Gravatar not showing**: Confirm that `gravatar` is initialized and passed to the template context. Flask-Gravatar makes the `gravatar` object available globally to all templates, but if you encounter issues, you can explicitly pass it via `render_template`.
- **Foreign key constraint fails**: When creating a comment, make sure `author_id` and `post_id` correspond to existing records. This is handled by using `current_user.id` and `post.id`.
- **Database errors after schema changes**: If you forgot to delete the old database, you may see errors about missing columns. Always delete the old `blog.db` when changing models.

### Summary

By completing this requirement, the blog now supports user comments, a core feature for community engagement. The implementation involved:

- Creating a `CommentForm` with CKEditor for rich text.
- Defining a `Comment` model with foreign keys to `User` and `BlogPost`.
- Establishing bidirectional one‑to‑many relationships.
- Handling database schema changes by recreating the database.
- Protecting the comment submission route with authentication checks.
- Rendering comments on the post page, including author names and dates.
- Enhancing the UI with Gravatar avatars for each commenter.

The blog is now a fully interactive platform where users can register, log in, read posts, and leave comments. The relational database structure ensures data integrity and opens possibilities for future enhancements like comment moderation, nested replies, or user profiles.

**Resource Links**:

- Flask-CKEditor Documentation: [https://flask-ckeditor.readthedocs.io/](https://flask-ckeditor.readthedocs.io/)
- Flask-Gravatar Documentation: [https://github.com/zzsochi/Flask-Gravatar](https://github.com/zzsochi/Flask-Gravatar)
- SQLAlchemy Basic Relationships: [https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- Gravatar Site: [https://en.gravatar.com/](https://en.gravatar.com/)

The completed project with all features up to this point can be downloaded from the lesson resources.