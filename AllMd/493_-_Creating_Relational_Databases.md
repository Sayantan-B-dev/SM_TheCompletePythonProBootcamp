## 493 - Creating Relational Databases

This document details the process of establishing a formal relationship between the `User` and `BlogPost` tables within the blog application. Until now, the blog posts have existed independently of user accounts, with the author’s name stored as a plain string in each post. However, now that we have a `User` model and authentication in place, it is logical to connect each blog post to the user who authored it. This connection enables us to:

- Retrieve all posts written by a specific user.
- Easily display the author’s name (and eventually profile information) on each post without duplicating data.
- Lay the groundwork for future features like multiple authors, author profiles, or admin panels.

This transformation involves modifying the database schema: adding a foreign key column to the `BlogPost` table that references the `User` table, and setting up an object‑oriented relationship using SQLAlchemy’s ORM. Because this change alters the database structure, it will break compatibility with the existing `blog.db` file. Therefore, we will also cover the necessary steps to handle this breaking change, including deleting the old database and recreating it with a new admin user and sample posts.

### Why Relational Databases Matter

In a flat file or non‑relational approach, you might store the author’s name directly inside each blog post record. For example, a `BlogPost` record might contain fields like `title`, `date`, `body`, and `author_name`. This works for simple display, but it leads to data redundancy and inconsistency. If the user changes their name, you would have to update every post they ever wrote. More importantly, you cannot easily answer questions like “Which user has written the most posts?” or “Show me all posts by a particular user” without scanning every post and matching strings.

A relational database solves these problems by separating entities into tables and linking them through keys. In our case:

- The `User` table holds information about each user once.
- The `BlogPost` table holds information about each post once, and includes a column (`author_id`) that stores the `id` of the user who wrote it.

This `author_id` is called a **foreign key** because it references the primary key of another table. Using this foreign key, you can join the two tables at query time to bring together the post and its author’s details. SQLAlchemy’s ORM goes a step further: it allows us to navigate these relationships as if they were simple Python attributes. For instance, given a `BlogPost` object `post`, we can access `post.author.name` to get the author’s name. Conversely, given a `User` object `user`, we can iterate over `user.posts` to get all posts they have written.

### Modifying the Database Models

We will modify the existing `User` and `BlogPost` model classes to establish a **one‑to‑many** relationship: one user can have many blog posts, and each blog post belongs to exactly one user. This is the most common type of relationship in web applications.

**Current Model Definitions (before modification):**

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    # No relationship to posts yet

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)   # Old field: stores author name as string
    img_url = db.Column(db.String(250), nullable=False)
```

Notice the `author` field in `BlogPost` is a simple string. We will replace this with a foreign key to the `users` table and add a relationship attribute.

**Updated Models with Relationship:**

```python
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    # This creates a virtual relationship; it does not add a column to the User table.
    # It tells SQLAlchemy that the 'author' field in BlogPost (see below) references this User.
    posts = relationship("BlogPost", back_populates="author")

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # Old 'author' column removed; replaced with author_id foreign key
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # This creates the other side of the relationship, pointing back to the User.
    # 'author' will now be a User object when accessed from a BlogPost instance.
    author = relationship("User", back_populates="posts")
```

**Explanation of changes:**

1. **Foreign Key (`author_id`)**:  
   `db.ForeignKey("users.id")` creates a constraint in the database that ensures every value in `author_id` corresponds to an existing `id` in the `users` table. The `nullable=False` means every post must have an author – there is no such thing as an orphaned post.

2. **Relationship on `User` (`posts`)**:  
   `relationship("BlogPost", back_populates="author")` tells SQLAlchemy that the `User` class has a one‑to‑many relationship with `BlogPost`. The `back_populates` argument connects this relationship to the corresponding one on the `BlogPost` side. When you access `user.posts`, SQLAlchemy will automatically query the `blog_posts` table for all records with `author_id` equal to this user’s `id`.

3. **Relationship on `BlogPost` (`author`)**:  
   Similarly, `relationship("User", back_populates="posts")` allows you to access the author of a post via `post.author`, which returns the corresponding `User` object.

**Important:** The `relationship` calls do **not** create database columns; they are purely for the ORM’s convenience. Only the `author_id` column is physically added to the `blog_posts` table.

### Understanding the SQLAlchemy Relationship Documentation

The code above follows the pattern described in the SQLAlchemy documentation on [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html). Specifically, it demonstrates a **one‑to‑many** relationship using `relationship()` and `ForeignKey`. The documentation explains:

- The “many” side (the `BlogPost`) holds a foreign key that references the “one” side (`User`).
- The `relationship()` is typically defined on the “one” side to give access to the collection of related objects, and optionally on the “many” side to give access to the parent object.
- The `back_populates` parameter tells SQLAlchemy to synchronize these two relationships, so that changes on one side are reflected on the other.

### The Breaking Change: Database Schema Mismatch

After updating the model definitions, restarting the Flask application will cause an error similar to:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: blog_posts.author_id
```

**Why does this happen?**  
The existing `blog.db` file was created based on the old schema, which did not have an `author_id` column in the `blog_posts` table. SQLAlchemy, by default, does **not** automatically alter existing tables to add new columns. It assumes the database schema already matches the model definitions. When it tries to insert or query data, it looks for the `author_id` column, finds it missing, and throws an error.

**Why not just alter the table?**  
In a production environment with live data, you would use a migration tool like Alembic to generate and apply schema changes while preserving data. However, for this development project, we have no critical data to preserve – the existing posts were just samples. Therefore, the simplest solution is to delete the old database and let SQLAlchemy create a fresh one with the correct schema.

### Deleting the Old Database and Recreating

1. **Stop the Flask server** if it is running.
2. **Locate the `blog.db` file** in your project root (the same folder as `main.py`).
3. **Delete it**. In PyCharm, right‑click the file and choose **Delete**. Ensure you confirm the deletion and do not check “Safe delete” (which would look for usages; there are none because the file is external).
4. **Restart the server**. When the Flask application runs again, SQLAlchemy will see that `blog.db` does not exist and will create a new, empty database with all tables defined according to the current models. The new `blog_posts` table will include the `author_id` column.

At this point, the database is empty. You must now:

- Register a new user (which will become the admin with `id = 1`).
- Create at least one blog post via the “Create New Post” functionality.

### Updating Templates to Use the Relationship

After recreating the database and adding a post, you may notice that the author’s name no longer appears on the home page or the individual post page. This is because the templates still expect a simple string `post.author`, but now `post.author` is a `User` object. We need to update the templates to access the user’s name correctly.

**In `index.html` (where posts are listed):**

Find the line that displays the author, for example:

```html
<p class="post-meta">Posted by {{ post.author }} on {{ post.date }}</p>
```

Replace it with:

```html
<p class="post-meta">Posted by {{ post.author.name }} on {{ post.date }}</p>
```

**In `post.html` (the single post view):**

Similarly, locate the author display and update it:

```html
<h2 class="subheading">{{ post.subtitle }}</h2>
<span class="meta">Posted by {{ post.author.name }} on {{ post.date }}</span>
```

**Why this works:**

- `post.author` is the `User` object associated with the post via the foreign key.
- `post.author.name` accesses the `name` attribute of that `User` object, which is the display name we stored during registration.

**If you have other places where the author is displayed** (e.g., in comments or an “about the author” section), apply the same pattern.

### Testing the Changes

After completing the modifications:

1. Run the application.
2. Register a new user (if you haven’t already). This user will have `id = 1` and thus be the admin.
3. Create a new blog post using the “Create New Post” button.
4. Visit the home page and the post page; verify that the author’s name appears correctly.
5. Optionally, register a second user and try to create a post (if you have not yet restricted post creation to admin only, you may be able to; but if you implemented the `@admin_only` decorator from the previous requirement, only the first user will see the “Create New Post” button). In either case, any post created by the second user would have that user’s `author_id`, and the templates would still display the correct name.

### Additional Considerations

- **Non‑nullable Foreign Key**: Because we set `nullable=False` on `author_id`, every post **must** have an author. If you ever try to create a post without assigning it to a user, SQLAlchemy will raise an integrity error. This is good for data consistency.
- **Cascading Deletes**: Currently, if you delete a user, any posts they authored will still exist but their `author_id` would point to a non‑existent user, causing errors when you try to access `post.author`. You might want to configure cascading behavior (e.g., delete all posts when a user is deleted, or set `author_id` to `NULL`). Since we intend the admin to be permanent, we can ignore this for now, but it’s something to consider for future enhancements.
- **Multiple Authors**: The current schema allows only one author per post. If you later want co‑authorship, you would need a many‑to‑many relationship via an association table.

### Summary

By establishing a one‑to‑many relationship between `User` and `BlogPost`, we have:

- Removed data redundancy (author name stored only once in the `User` table).
- Enabled powerful queries (all posts by a user, author details for a post).
- Prepared the database for future features like author profiles or multi‑author blogs.

The process involved:

1. Adding a foreign key `author_id` to the `BlogPost` model.
2. Defining bidirectional relationships using `relationship()` and `back_populates`.
3. Handling the breaking schema change by deleting the old database and recreating it.
4. Updating templates to access the author’s name via the relationship (`post.author.name`).

With this relational structure in place, the blog’s data model is now robust and ready for the next phase: allowing users to comment on posts, which will similarly link comments to both users and posts.

**Resource Links:**

- SQLAlchemy Basic Relationship Patterns: [https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- SQLAlchemy ForeignKey Documentation: [https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
- Flask-SQLAlchemy Quickstart: [https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#define-models](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#define-models)

Now that users and posts are properly linked, we can move forward to the final feature: user comments.