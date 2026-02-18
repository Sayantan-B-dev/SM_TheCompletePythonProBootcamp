## Passing Authentication Status to Templates

### 1. Introduction

You have built a complete authentication system: users can register, log in, and log out; passwords are securely hashed; routes are protected; and flash messages provide feedback. However, the user interface does not yet reflect whether someone is logged in. When a user is authenticated, they still see the **Login** and **Register** buttons on the home page and in the navigation bar. This is confusing and poor user experience.

The goal of this final lesson is to make the templates **aware of the authentication status** and render content conditionally. Specifically:

- Hide the **Login** and **Register** links in the navigation bar for authenticated users, and show a **Logout** link instead.
- On the home page (`index.html`), hide the large **Login** and **Register** buttons when the user is logged in, and display a simple message: "(you are already logged in)".

This will be achieved using the `current_user` proxy that Flask‑Login makes available in all templates, combined with Jinja2's conditional statements.

---

### 2. Understanding `current_user` in Templates

Flask‑Login automatically injects a variable named `current_user` into the template context. This variable represents the currently authenticated user. If no user is logged in, `current_user` is an `AnonymousUser` object.

**Key properties of `current_user`:**

- `current_user.is_authenticated`: Returns `True` if a real (non‑anonymous) user is logged in.
- `current_user.is_anonymous`: Returns `True` if no user is logged in.
- `current_user.id`, `current_user.name`, etc.: Access attributes of the logged‑in user (only available when authenticated).

In templates, you can use these properties inside `{% if %}` blocks to conditionally show or hide content.

---

### 3. Modifying the Navigation Bar (base.html)

The navigation bar is defined in `base.html`, which is inherited by all other pages. Therefore, changes here will affect the entire site.

**Current `base.html` (simplified):**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('login') }}">Login</a>
        <a href="{{ url_for('register') }}">Register</a>
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**Updated `base.html` with conditional links:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**Explanation:**

- `{% if current_user.is_authenticated %}` checks if a user is logged in.
- If true, only the **Logout** link is shown (pointing to the `/logout` route).
- If false (user not logged in), the **Login** and **Register** links are shown.
- The **Home** link is always visible.

This change immediately improves the navigation: logged‑in users see a way to log out, while visitors see the entry points to authentication.

---

### 4. Modifying the Home Page (index.html)

The home page (`index.html`) currently displays two prominent buttons for **Login** and **Register**. When a user is already logged in, these buttons should be hidden, and a small message should appear instead.

**Current `index.html`:**

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Welcome to the Secret Page</h1>
<p>This is a secret area. You need to log in to see the secrets.</p>
<a href="{{ url_for('login') }}">Login</a> or <a href="{{ url_for('register') }}">Register</a>
{% endblock %}
```

**Updated `index.html` with conditional display:**

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Welcome to the Secret Page</h1>
<p>This is a secret area. You need to log in to see the secrets.</p>

{% if current_user.is_authenticated %}
    <p>(you are already logged in)</p>
{% else %}
    <a href="{{ url_for('login') }}">Login</a> or <a href="{{ url_for('register') }}">Register</a>
{% endif %}
{% endblock %}
```

**Explanation:**

- If the user is authenticated, the paragraph "(you are already logged in)" is displayed, and the login/register links are **not** shown.
- If the user is not authenticated, the original buttons appear as before.

---

### 5. Complete Code for Modified Templates

#### 5.1 `base.html` (final)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

#### 5.2 `index.html` (final)

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Welcome to the Secret Page</h1>
<p>This is a secret area. You need to log in to see the secrets.</p>

{% if current_user.is_authenticated %}
    <p>(you are already logged in)</p>
{% else %}
    <a href="{{ url_for('login') }}">Login</a> or <a href="{{ url_for('register') }}">Register</a>
{% endif %}
{% endblock %}
```

---

### 6. Testing the Changes

1. **Start the Flask application.**
2. **Visit the home page while logged out.** You should see:
   - Navigation: Home, Login, Register.
   - Page content: "Login or Register" buttons.
3. **Log in** (or register a new user). After login, you are redirected to the secrets page.
4. **Navigate back to the home page** (click "Home" in the navigation). You should now see:
   - Navigation: Home, Logout (Login and Register are gone).
   - Page content: The message "(you are already logged in)" appears instead of the login/register buttons.
5. **Click Logout.** You are redirected to the home page, and the login/register buttons reappear.

---

### 7. How Template Inheritance Works with `current_user`

The key to this functionality is that `current_user` is available in **all templates** because Flask‑Login adds it to the global template context. When a template extends `base.html`, the `{% if %}` condition in the base template is evaluated using the same `current_user`. This ensures consistency across the entire site.

If you ever need to access `current_user` in a deeply nested template or a partial (like a header include), it is always available – you do not need to pass it explicitly from the route.

---

### 8. Additional Enhancements (Optional)

You can further improve the user experience with small touches:

- **Greet the user by name on the home page:**  
  Replace `(you are already logged in)` with `(you are already logged in as {{ current_user.name }})`.

- **Show a logout confirmation flash message:**  
  In the `/logout` route, add `flash('You have been logged out successfully.', 'info')` and display it on the home page.

- **Redirect authenticated users away from login/register pages:**  
  If a logged‑in user accidentally navigates to `/login` or `/register`, you could redirect them to the secrets page (or home) with a flash message. This prevents them from seeing forms they don't need.

**Example of protecting login/register routes from authenticated users:**

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
    # ... rest of login logic
```

Similarly for `/register`.

---

### 9. Common Mistakes and Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| `current_user` is not defined in template | Flask‑Login not initialized, or `login_manager.init_app(app)` missing | Ensure Flask‑Login is properly configured. |
| `current_user.is_authenticated` always false | User not actually logged in, or session expired | Check that `login_user()` was called and that the user loader returns the correct object. |
| Links still appear after logout | Browser cache | Hard refresh (Ctrl+F5) or check that logout route correctly calls `logout_user()`. |
| Message "(you are already logged in)" shows for anonymous users | Condition inverted | Verify you used `{% if current_user.is_authenticated %}` not `{% if not current_user.is_authenticated %}`. |

---

### 10. Summary

You have now completed the authentication system with a polished user interface:

- **Secure password storage** using Werkzeug's hashing.
- **User session management** with Flask‑Login.
- **Protected routes** (`/secrets`, `/download`) using `@login_required`.
- **Informative feedback** via flash messages.
- **Context‑aware templates** that adapt to the user's login state.

Your Flask application is now a fully functional, user‑friendly, and reasonably secure system for user registration and login. The skills you have learned – password hashing, session management, route protection, template conditionals – are directly applicable to any future Flask project that involves user accounts.

**You can download the completed project from the lesson resources to compare with your own implementation.**