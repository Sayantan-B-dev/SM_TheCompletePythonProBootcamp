## Requirement 3 - Protect Routes

This document details the implementation of access control for administrative functions within the blog. After establishing user registration and login, the next logical step is to differentiate between regular users and the blog administrator. The first registered user (with `id = 1`) is designated as the admin and is granted exclusive permissions to create, edit, and delete blog posts. All other users, even if logged in, must be prevented from accessing these administrative actions both in the user interface and at the route level.

The implementation is divided into two complementary parts:

1. **Hiding UI elements** – Buttons for “Create New Post”, “Edit Post”, and “Delete” are only rendered in templates when the logged‑in user is the admin.
2. **Protecting routes with a custom decorator** – A Python decorator named `@admin_only` is applied to the underlying route functions (`/new-post`, `/edit-post`, `/delete`). If a non‑admin user attempts to access these URLs directly, the server responds with a **403 Forbidden** error.

By combining these two layers, the blog ensures that administrative functionality is both invisible and inaccessible to unauthorized users, while remaining fully available to the designated administrator.

### Prerequisites

Before proceeding, confirm that the following are in place:

- User authentication is fully implemented (registration, login, logout) using Flask‑Login (see Requirement 2).
- The `current_user` proxy is available in all templates.
- The first user created in the system has an `id` of `1`. (This is typically the case with auto‑incrementing primary keys; if you have already created test users, you may need to adjust accordingly or modify the condition to use a different identifier such as an `is_admin` flag.)
- The routes for creating, editing, and deleting posts already exist and are functional (they may currently be unprotected). If they do not exist yet, you will need to implement them before applying the decorator.

### Step 1: Hide UI Elements Based on Admin Status

The templates `index.html` (which lists all blog posts) and `post.html` (which shows a single post) contain buttons that allow administrative actions. These buttons must only be visible when the currently logged‑in user is the admin – that is, when `current_user.id == 1`.

**Understanding `current_user` in Templates**

Flask‑Login automatically makes the `current_user` proxy available in every Jinja2 template. This object has the same attributes as your `User` model (e.g., `id`, `name`, `email`). It also provides the `is_authenticated` property, but here we are specifically interested in the user’s database ID.

**Modifying index.html**

In `index.html`, locate the section where the “Create New Post” button is placed (usually near the top or bottom of the page). Wrap it in an `{% if %}` block:

```html
{% if current_user.is_authenticated and current_user.id == 1 %}
    <a href="{{ url_for('new_post') }}" class="btn btn-primary">Create New Post</a>
{% endif %}
```

- The check `current_user.is_authenticated` ensures that the user is logged in; otherwise `current_user.id` would be `None` (or an anonymous user object) and the comparison would fail or raise an error. It is good practice to include this guard.
- The condition `current_user.id == 1` is the core admin check.

**Modifying post.html**

In `post.html`, there are typically “Edit Post” and “Delete Post” buttons near the post content. Wrap them similarly:

```html
{% if current_user.is_authenticated and current_user.id == 1 %}
    <a href="{{ url_for('edit_post', post_id=post.id) }}" class="btn btn-secondary">Edit Post</a>
    <a href="{{ url_for('delete_post', post_id=post.id) }}" class="btn btn-danger">Delete Post</a>
{% endif %}
```

If the buttons are placed inside a loop or a conditional block that already checks for existence, ensure the admin check is added.

**Why Two Checks?**

The first check (`current_user.is_authenticated`) prevents the template from trying to access `id` on an anonymous user. Although the `AnonymousUserMixin` provided by Flask‑Login does have an `id` that returns `None`, it is safer and more explicit to verify authentication first. Alternatively, you could rely on the fact that `current_user.id` is `None` for anonymous users and `None == 1` is `False`, but the explicit authentication check makes the intent clearer.

**Result**

After these changes, when a regular user (or a visitor) views the blog, they will not see any administrative buttons. Only the user with `id = 1` will see them, as shown in the target screenshot.

### Step 2: Create the `@admin_only` Decorator

Hiding buttons is only a cosmetic measure; a savvy user could still type the URL of an administrative route (e.g., `/new-post`) into their browser and potentially access the functionality. To prevent this, we must protect the underlying route functions. Flask allows us to create custom decorators that wrap route functions and perform checks before the original function is executed.

**Understanding Python Decorators**

A decorator is a function that takes another function as an argument, extends its behavior, and returns a new function. In the context of Flask routes, decorators like `@app.route` and `@login_required` are commonly used. Here we will create a decorator named `@admin_only` that:

1. Checks whether the current user is authenticated and has `id == 1`.
2. If the check passes, it calls the original route function.
3. If the check fails, it aborts the request with a **403 Forbidden** HTTP error.

**Implementation of `@admin_only`**

Create the decorator in a suitable location, such as at the top of `main.py` or in a separate `decorators.py` module. We will use `functools.wraps` to preserve the original function’s metadata (important for Flask routing).

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not authenticated or their id is not 1, forbid access
        if not current_user.is_authenticated or current_user.id != 1:
            abort(403)  # HTTP 403 Forbidden
        # Otherwise, proceed with the original function
        return f(*args, **kwargs)
    return decorated_function
```

**Explanation**:

- `@wraps(f)` copies the name, docstring, and other metadata from the original function `f` to the wrapper function. This is essential for Flask to work correctly (e.g., for `url_for` generation).
- Inside `decorated_function`, we check `current_user.is_authenticated` and `current_user.id != 1`. If either condition fails, we call `abort(403)`, which immediately halts request processing and returns a 403 error page (Flask provides a default error page, which you can customize if desired).
- If the checks pass, we call the original function with the same arguments and keyword arguments (`*args, **kwargs`) and return its result.

**Applying the Decorator to Routes**

Now apply `@admin_only` to each administrative route. Place it **below** `@app.route` and **above** the function definition. For example:

```python
@app.route('/new-post', methods=['GET', 'POST'])
@admin_only
def new_post():
    # ... existing code to create a new post ...
    pass

@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    # ... existing code to edit a post ...
    pass

@app.route('/delete/<int:post_id>')
@admin_only
def delete_post(post_id):
    # ... existing code to delete a post ...
    pass
```

If you have already used `@login_required` on these routes, you can either replace it with `@admin_only` (since `@admin_only` already includes an authentication check) or keep both. If you keep both, the order matters: decorators are applied from bottom to top. A common pattern is:

```python
@app.route('/new-post')
@login_required
@admin_only
def new_post():
    ...
```

In this order, `@login_required` runs first; if the user is not logged in, they are redirected to the login page. If they are logged in but not admin, `@admin_only` will then abort with 403. This gives a more user‑friendly experience: non‑admin logged‑in users see a 403 page rather than being redirected to login again. For simplicity, you may choose to use only `@admin_only` as it already checks authentication, but then non‑authenticated users will also receive a 403 instead of being prompted to log in. Decide based on your desired user experience. The requirement does not specify, so either approach is acceptable.

**Using `abort(403)`**

The `abort()` function from Flask raises an HTTP exception. With `abort(403)`, Flask will look for a template named `403.html` in your `templates` folder. If that template exists, it will be rendered; otherwise, Flask displays its default error page. You can create a custom `403.html` to match your site’s design. For example:

```html
{% extends "base.html" %}
{% block title %}Forbidden{% endblock %}
{% block content %}
<div class="container">
    <h1>403 Forbidden</h1>
    <p>You do not have permission to access this page.</p>
    <a href="{{ url_for('home') }}">Return to Home</a>
</div>
{% endblock %}
```

### Testing the Protection

After implementing both the template conditionals and the decorator, perform the following tests:

1. **As admin (user id = 1)**:
   - Log in with the first user account.
   - Verify that the “Create New Post” button appears on the home page.
   - Open a post and confirm that “Edit Post” and “Delete” buttons are visible.
   - Click each button and ensure the corresponding functionality works (e.g., the new post form loads, edit form loads, delete removes the post).
   - Try to access the admin routes directly by typing the URL; they should work.

2. **As a regular logged‑in user** (any user with id != 1):
   - Log in with a second user account.
   - Verify that no admin buttons appear anywhere.
   - Manually navigate to `/new-post`, `/edit-post/1`, and `/delete/1`.
   - For each, you should receive a **403 Forbidden** error (either the default Flask error page or your custom `403.html`).

3. **As an anonymous visitor** (not logged in):
   - Verify no admin buttons appear.
   - Attempt to access the admin routes directly; you should also receive a **403 Forbidden** (if you used only `@admin_only`) or be redirected to login (if you also used `@login_required` above `@admin_only`). Adjust expectations based on your decorator order.

### Important Considerations

- **First User ID Assumption**: The requirement assumes the first registered user has `id = 1`. This is typical when using an auto‑incrementing integer primary key and you have not deleted that user. If you have already created other users before implementing registration, you may need to manually set the admin flag or adjust the condition to check an `is_admin` column in the `User` model. For a production system, a more flexible approach is to add a boolean `is_admin` field to the `User` model and check that instead of a hard‑coded ID. However, for this capstone project, the ID‑based check is sufficient.

- **Multiple Admins**: The current implementation only allows a single admin (id = 1). If you later need multiple admins, you would modify the condition to check for a role or a set of admin IDs.

- **Decorator Order**: When stacking decorators, remember that the one closest to the function runs first. If you use both `@login_required` and `@admin_only`, ensure they are in the correct order to achieve the desired behavior.

- **Custom Error Pages**: You can customize the 403 error page by creating a `403.html` template. Flask will automatically use it if it exists. You can also register an error handler for 403 errors to have more control.

### Troubleshooting Common Issues

- **Buttons still visible to non‑admin users**: Double‑check the template condition. Ensure you are using `current_user.id == 1` and not `current_user.get_id()`. Also confirm that `current_user.is_authenticated` is `True` for logged‑in users. If the user is logged in but `current_user.id` is `None`, your `user_loader` might not be returning the user object correctly.

- **403 error for admin user**: If the admin user (id=1) gets a 403 when accessing admin routes, verify that the `admin_only` decorator’s condition is correct. It should allow access when `current_user.id == 1`. Add a debug print inside the decorator to see the value of `current_user.id`. Also ensure that the admin user is actually logged in before accessing the route.

- **`abort(403)` not working**: `abort` is a Flask function; make sure you have imported it: `from flask import abort`. If you are using a custom error page, confirm that `403.html` is in the `templates` folder.

- **Decorator not found**: If you defined `admin_only` in a separate module, import it where needed: `from decorators import admin_only`.

- **Circular imports**: If you place the decorator in a separate file that also imports from `main` (e.g., to access `current_user`), you may encounter circular imports. To avoid this, define the decorator in the same file as your routes, or use a late‑binding pattern (import `current_user` inside the decorator function). The example above imports `current_user` at the top of the module, which is fine as long as the decorator is defined after `current_user` is available (i.e., after `login_manager` setup). In a typical Flask app, `current_user` is a proxy that works even if imported early.

### Summary

By completing this requirement, you have added a critical authorization layer to your blog. The admin user (the first registered user) now has exclusive access to post management features, while all other users are effectively prevented from creating, editing, or deleting content. This two‑pronged approach (UI hiding and route protection) follows security best practices: never rely solely on the front end for access control.

The skills you have applied – writing custom decorators, using `abort()`, and conditionally rendering templates – are transferable to many other scenarios where role‑based access control is needed. As you continue to develop the blog, you may expand this pattern to other user roles or permissions.

**Next Steps**

With administrative routes secured, the final major feature is to allow logged‑in users (including the admin) to comment on posts. This will involve:

- Updating the `Comment` model to link each comment to a user.
- Creating a form for submitting comments.
- Protecting the comment submission route with `@login_required`.
- Displaying comments with the author’s name (instead of a manually entered name).
- Possibly allowing users to edit or delete their own comments (authorization based on comment ownership).

These features will be covered in the subsequent requirement.

**Resource Links**

- Flask abort() documentation: [https://flask.palletsprojects.com/en/3.0.x/api/#flask.abort](https://flask.palletsprojects.com/en/3.0.x/api/#flask.abort)
- Python functools.wraps: [https://docs.python.org/3/library/functools.html#functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- Flask error handling: [https://flask.palletsprojects.com/en/3.0.x/errorhandling/](https://flask.palletsprojects.com/en/3.0.x/errorhandling/)
- Flask-Login current_user: [https://flask-login.readthedocs.io/en/latest/#flask_login.current_user](https://flask-login.readthedocs.io/en/latest/#flask_login.current_user)

Now that the admin routes are protected, your blog is one step closer to being a fully functional, multi‑user platform.