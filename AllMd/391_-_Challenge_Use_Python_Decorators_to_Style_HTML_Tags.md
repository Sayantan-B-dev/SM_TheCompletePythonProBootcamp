# Multiple Decorators on a Single Flask Route — Deep Structural Explanation

In Flask, decorators are layered wrappers applied to a function in **bottom-up order**. When multiple decorators are stacked on a route, each one wraps the function returned by the decorator below it.

Understanding execution order is critical.

---

# 1. Basic Stacking Concept

When you write:

```python
@decorator_one
@decorator_two
def target():
    pass
```

Python internally transforms it into:

```python
target = decorator_one(decorator_two(target))
```

Execution order when called:

```
decorator_one wrapper →
    decorator_two wrapper →
        original function
```

---

# 2. Multiple Decorators on a Flask Route

Example: Add logging and execution timing to a route.

---

## Full Example

```python
from flask import Flask, render_template
import time
import functools

app = Flask(__name__)

# Decorator 1: Log route access
def log_access(original_function):
    """
    Logs whenever the route is accessed.
    """

    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        print(f"Route '{original_function.__name__}' was accessed")
        return original_function(*args, **kwargs)

    return wrapper


# Decorator 2: Measure execution time
def measure_execution_time(original_function):
    """
    Measures execution duration of the route.
    """

    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = original_function(*args, **kwargs)

        end_time = time.perf_counter()
        elapsed = end_time - start_time

        print(f"{original_function.__name__} executed in {elapsed:.4f} seconds")

        return result

    return wrapper


@app.route("/")
@log_access
@measure_execution_time
def homepage():
    time.sleep(1)  # Simulated processing delay
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 3. Execution Flow Breakdown

When `/` is requested:

Step 1:
Flask matches route and calls `homepage`.

Step 2:
But `homepage` is actually:

```
homepage = log_access(measure_execution_time(homepage))
```

Step 3:
Execution order becomes:

```
log_access wrapper →
    measure_execution_time wrapper →
        original homepage →
    return →
return
```

Console Output Example:

```
Route 'homepage' was accessed
homepage executed in 1.0008 seconds
```

---

# 4. Important Rule — Order Matters

If you reverse decorators:

```python
@app.route("/")
@measure_execution_time
@log_access
def homepage():
```

Then execution order changes.

Now:

```
measure_execution_time wrapper →
    log_access wrapper →
        original function
```

Timing now includes logging overhead.

---

# 5. Using Multiple Flask Route Decorators

Flask itself allows multiple `@app.route()` decorators.

Example:

```python
@app.route("/")
@app.route("/home")
def homepage():
    return render_template("index.html")
```

Now both URLs work:

```
/
```

and

```
/home
```

Internally:

Flask registers the same function under multiple URL rules.

---

# 6. Combining Route Decorator with Custom Decorators

You can mix Flask routing with custom logic.

Example: Simple authentication simulation.

```python
from flask import redirect, url_for

def require_auth(original_function):
    """
    Simulated authentication check.
    """

    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        user_authenticated = False

        if not user_authenticated:
            return redirect(url_for("homepage"))

        return original_function(*args, **kwargs)

    return wrapper


@app.route("/about")
@require_auth
def about_page():
    return render_template("about.html")
```

Here:

* Route registered first.
* Then wrapped with authentication logic.
* Unauthorized users redirected.

---

# 7. Correct Ordering Pattern in Flask

Best practice:

```
@app.route()
@custom_decorator
def function():
```

Route decorator should be placed on top so Flask registers the final wrapped function correctly.

---

# 8. Real Backend Use Cases for Multiple Decorators

Common stacked patterns:

```
@app.route("/api/data")
@login_required
@rate_limit
@log_request
def get_data():
```

Each layer handles:

• Authentication
• Rate limiting
• Logging
• Execution

This creates middleware-like behavior.

---

# 9. Conceptual Call Stack Visualization

For:

```python
@app.route("/")
@A
@B
@C
def f():
```

Call stack becomes:

```
A →
    B →
        C →
            f
```

Return path unwinds in reverse order.

---

# 10. Summary of Multi-Decorator Behavior

Multiple decorators allow:

• Layered functionality
• Separation of concerns
• Middleware-style design
• Reusable route modifiers
• Clean route logic

The final function executed is not the original function but a wrapped chain of function objects.

---

# Core Understanding

Decorators stack as nested function calls.

Flask routes are simply decorators that register function references.

Combining multiple decorators enables structured, modular backend architecture similar to middleware pipelines in large frameworks.
