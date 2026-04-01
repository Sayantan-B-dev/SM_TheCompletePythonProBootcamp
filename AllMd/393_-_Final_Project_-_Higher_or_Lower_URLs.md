# Flask Application – Complete Technical Breakdown

This document explains the full architecture, execution flow, security behavior, decorators, templating system, and static assets of the provided Flask project. The explanation follows a backend-engineering perspective.

---

# 1. High-Level Architecture

| Layer              | Technology      | Responsibility                    |
| ------------------ | --------------- | --------------------------------- |
| Backend Framework  | `Flask`         | HTTP routing and request handling |
| Session Handling   | `Flask session` | Authentication state storage      |
| Environment Config | `python-dotenv` | Secret key loading                |
| Console Logging    | `rich`          | Structured terminal output        |
| Templating         | `Jinja2`        | Dynamic HTML rendering            |
| Styling            | CSS             | Frontend appearance               |
| Client Interaction | HTML Forms      | User input submission             |

The application implements:

• Authentication system
• Protected routes
• Logging decorator
• Performance measurement decorator
• Simple number guessing game
• Session-based state management

---

# 2. Core Application File: `app.py`

## 2.1 Initialization

```python
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
```

### Explanation

• `Flask(__name__)` initializes the WSGI application instance.
• `secret_key` enables cryptographic signing of session cookies.
• `.env` file is optionally loaded using `load_dotenv()`.

If no `SECRET_KEY` is present, a fallback value is used. This is acceptable for development but insecure for production environments.

---

# 3. Decorators System

Three decorators modify route behavior. They demonstrate middleware-style request wrapping.

Decorator execution order is bottom-to-top.

Example:

```python
@log_access
@measure_execution_time
@require_auth
def about_page():
```

Execution order becomes:

1. `log_access`
2. `measure_execution_time`
3. `require_auth`
4. `about_page`

---

## 3.1 `log_access` Decorator

### Purpose

Logs structured request information to console.

### Logs:

| Field        | Value                |
| ------------ | -------------------- |
| Route        | Function name        |
| Method       | HTTP method          |
| Path         | URL path             |
| Session Auth | Authentication state |

It uses:

```python
rich.Table
rich.Console
```

This produces visually structured terminal output instead of plain prints.

This decorator runs for every decorated route before actual route logic executes.

---

## 3.2 `measure_execution_time` Decorator

### Purpose

Measures function runtime.

### Mechanism:

```python
start = time.perf_counter()
result = func()
end = time.perf_counter()
```

`perf_counter()` gives high-precision timing.

Output example:

```
homepage executed in 0.00123 seconds
```

This helps monitor route performance.

---

## 3.3 `require_auth` Decorator

### Purpose

Protects routes from unauthorized access.

### Logic:

```python
if not session.get("is_authenticated"):
    return redirect(url_for("login"))
```

If session does not contain:

```
session["is_authenticated"] = True
```

User is redirected to login page.

This is classic session-based access control.

---

# 4. Route-by-Route Breakdown

---

## 4.1 `/` – Homepage

```python
@app.route("/")
```

• Public route
• Renders `index.html`
• No authentication required

---

## 4.2 `/about`

```python
@app.route("/about")
@require_auth
```

• Protected route
• Requires session authentication
• If not authenticated → redirected to `/login`
• Renders `about.html`

---

## 4.3 `/login`

```python
@app.route("/login", methods=["GET", "POST"])
```

### GET

Renders login form.

### POST

Processes credentials:

```python
if username == "admin" and password == "1234":
```

If valid:

```
session["is_authenticated"] = True
session["secret_number"] = random.randint(1, 10)
```

Redirects to `/guess_number`.

If invalid:

Returns plain string: `"Invalid credentials"`.

Important: Credentials are hardcoded. This is for demonstration only.

---

## 4.4 `/logout`

```python
session.clear()
```

Removes all session data:

• Authentication state
• Secret number

User is redirected to homepage.

---

## 4.5 `/guess_number`

Protected route.

### On Login

`secret_number` stored in session.

### POST Logic

```python
user_guess = int(request.form.get("guess"))
```

Then compares:

| Condition | Message  |
| --------- | -------- |
| Equal     | Correct  |
| Greater   | Too high |
| Lower     | Too low  |

If invalid input → `Invalid input.`

State is preserved across requests using session storage.

---

# 5. Templates Analysis

Flask uses Jinja2 templating.

Templates located in:

```
/templates
```

---

## 5.1 `index.html`

• Displays homepage
• Links to `/about`
• Links to `/guess_number`

Note:
Even if user clicks Guess Number without login, they will be redirected automatically.

---

## 5.2 `login.html`

Basic login form:

```html
<form method="POST">
```

Submits username and password.

No CSRF protection implemented.

---

## 5.3 `about.html`

Simple protected page.

---

## 5.4 `guess_number.html`

Contains:

• Numeric input
• Submit button
• Conditional message block:

```html
{% if message %}
<p>{{ message }}</p>
{% endif %}
```

Jinja renders message dynamically.

---

# 6. Static Files

## 6.1 CSS (`style.css`)

### Design Characteristics

• Dark theme
• Centered layout
• White text
• Minimal UI

### Notable CSS

```css
a:hover {
    background-color: white;
    color: black;
    scale: 1.1;
}
```

Important:
`&:hover` syntax is invalid in pure CSS.
That syntax belongs to SCSS or pre-processors.

Correct CSS should be:

```css
a:hover { }
a:active { }
```

---

## 6.2 `script.js`

Currently empty.

Reserved for client-side JavaScript logic.

---

# 7. Session Flow

### Before Login

```
session = {}
```

### After Login

```
session = {
    "is_authenticated": True,
    "secret_number": <random 1-10>
}
```

### After Logout

```
session = {}
```

Session is stored client-side but cryptographically signed using secret key.

---

# 8. Security Analysis

| Area                   | Status    | Comment                 |
| ---------------------- | --------- | ----------------------- |
| Password Storage       | Weak      | Hardcoded plaintext     |
| CSRF Protection        | Missing   | Forms unprotected       |
| Brute Force Protection | None      | Unlimited attempts      |
| Secret Key             | Env-based | Correct approach        |
| Session Handling       | Valid     | Standard Flask usage    |
| Debug Mode             | Enabled   | Not safe for production |

`debug=True` exposes stack traces. Should be disabled in production.

---

# 9. Execution Flow Summary

Application startup:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Flask development server launches.

On each request:

1. Request hits route
2. Decorators execute
3. Authentication verified (if applied)
4. Route logic runs
5. Template rendered
6. Response returned
7. Execution time printed

---

# 10. Design Patterns Used

| Pattern                   | Implementation            |
| ------------------------- | ------------------------- |
| Decorator Pattern         | Logging and auth wrappers |
| Session-based Auth        | Cookie session storage    |
| MVC Separation            | Templates + backend logic |
| Middleware-style Wrapping | Stacked decorators        |

---

# 11. Improvements for Production Readiness

• Replace hardcoded credentials with database-backed authentication
• Use password hashing (`werkzeug.security`)
• Add CSRF protection (`Flask-WTF`)
• Fix CSS hover syntax
• Disable debug mode
• Use environment-based configuration class
• Add error handlers (`404`, `500`)
• Add logging persistence instead of console only

---

# 12. Conceptual Understanding

This project demonstrates:

• How Flask routing works
• How decorators modify route behavior
• How sessions maintain user state
• How backend renders frontend
• How to measure performance
• How to implement basic access control

It is a clean educational demonstration of middleware, session logic, and route protection within a minimal Flask application.
