# Python Decorators — Deep Structural and Execution-Level Explanation

## 1. Formal Definition

A **decorator** is a higher-order function that:

* Accepts another function as input
* Returns a modified or enhanced function
* Extends behavior without modifying original source code

Decorators are implemented using:

* First-class functions
* Nested functions
* Closures

They enable behavior injection around function execution.

---

# 2. Why Decorators Exist — Purpose and Architectural Role

Decorators provide **cross-cutting concerns abstraction**, meaning they isolate functionality that applies to multiple functions without duplicating logic.

Common backend use cases:

* Logging
* Authentication
* Authorization
* Caching
* Rate limiting
* Delayed execution
* Performance measurement
* Transaction management

Instead of embedding logic inside every function, decorators wrap the function externally.

---

# 3. Step-by-Step Internal Mechanism

Consider:

```python
@decorator_name
def target_function():
    pass
```

Python interprets this as:

```python
target_function = decorator_name(target_function)
```

Execution order:

1. `target_function` is created.
2. It is passed into `decorator_name`.
3. Decorator returns a new function.
4. Original name now points to wrapped version.

The original function still exists in memory but is replaced by wrapper reference.

---

# 4. Basic Decorator Construction

## Example 1 — Simple Wrapper

```python
def simple_decorator(original_function):
    """
    Accepts a function and returns a modified version.
    """

    def wrapper_function():
        print("Before execution")
        original_function()
        print("After execution")

    return wrapper_function


@simple_decorator
def say_hello():
    print("Hello")

say_hello()
```

Expected Output:

```
Before execution
Hello
After execution
```

---

## Step-by-Step Flow

1. `say_hello` defined.
2. `@simple_decorator` executes.
3. Python performs: `say_hello = simple_decorator(say_hello)`
4. Calling `say_hello()` actually calls `wrapper_function()`.

---

# 5. Decorator with Arguments Support

To handle any function signature, wrapper must accept `*args` and `**kwargs`.

```python
def flexible_decorator(original_function):
    """
    Supports arbitrary arguments.
    """

    def wrapper(*args, **kwargs):
        print("Before execution")
        result = original_function(*args, **kwargs)
        print("After execution")
        return result

    return wrapper


@flexible_decorator
def add_numbers(a, b):
    return a + b

print(add_numbers(5, 7))
```

Expected Output:

```
Before execution
After execution
12
```

---

# 6. Understanding the Closure in Decorators

Why does `wrapper` remember `original_function`?

Because decorators create a **closure**.

Internal state:

* `original_function` stored in wrapper’s `__closure__`.
* Even after decorator finishes execution, wrapper retains access.

You can inspect:

```python
print(add_numbers.__closure__)
```

---

# 7. Decorator with Parameters (Two-Level Wrapping)

If decorator itself needs arguments:

Example: Add delay of specific seconds.

Structure becomes:

```
decorator_argument →
    decorator →
        wrapper
```

---

## Example — Delay Decorator

```python
import time

def delay_execution(seconds):
    """
    Decorator factory that adds delay before function execution.
    """

    def actual_decorator(original_function):

        def wrapper(*args, **kwargs):
            print(f"Delaying execution by {seconds} seconds")
            time.sleep(seconds)
            return original_function(*args, **kwargs)

        return wrapper

    return actual_decorator


@delay_execution(3)
def process_task():
    print("Task executed")

process_task()
```

Expected Behavior:

Program waits 3 seconds, then:

```
Delaying execution by 3 seconds
Task executed
```

---

## Execution Breakdown

1. `delay_execution(3)` runs first.
2. Returns `actual_decorator`.
3. `process_task` passed into `actual_decorator`.
4. Returns `wrapper`.
5. `process_task` now refers to wrapper.

---

# 8. Applying Delay to Specific Group of Functions

Instead of modifying multiple functions manually:

```python
@delay_execution(2)
def api_call_one():
    print("API call one")

@delay_execution(2)
def api_call_two():
    print("API call two")
```

This enforces consistent delay across selected functions.

---

# 9. Preserving Original Metadata (`functools.wraps`)

Without correction:

```python
print(process_task.__name__)
```

Output becomes:

```
wrapper
```

To preserve metadata:

```python
import functools

def delay_execution(seconds):
    def actual_decorator(original_function):

        @functools.wraps(original_function)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return original_function(*args, **kwargs)

        return wrapper
    return actual_decorator
```

Now:

```
process_task.__name__
```

Correctly outputs:

```
process_task
```

---

# 10. What Additional Functionality Does Decorator Give to a File?

Decorators allow:

* Centralized behavioral control
* Clean separation of concerns
* Reusable execution modifiers
* Modular system design
* Runtime logic injection

They transform file structure from:

```
function logic mixed with utility logic
```

into:

```
core logic isolated
cross-cutting logic layered externally
```

---

# 11. Advanced Backend Use Case — Timing Execution

```python
import time
import functools

def measure_time(original_function):

    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = original_function(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result

    return wrapper


@measure_time
def heavy_computation():
    time.sleep(2)
    return "Done"

print(heavy_computation())
```

Expected Output:

```
Execution time: 2.x seconds
Done
```

---

# 12. Common Real-World Examples in Frameworks

* Flask route decorator
  `@app.route("/")`

* Django login requirement
  `@login_required`

* Caching decorators
  `@lru_cache`

All rely on same mechanism.

---

# 13. Mental Model Summary

Decorator is:

```
Function → Wrapped → Replaced → Enhanced
```

Execution layering:

```
Call →
    Wrapper →
        Pre-logic →
        Original function →
        Post-logic →
    Return result
```

---

# 14. Core Concepts You Must Understand

| Concept               | Importance               |
| --------------------- | ------------------------ |
| First-class functions | Required foundation      |
| Closures              | Variable retention       |
| `*args`, `**kwargs`   | Generic wrapping         |
| Metadata preservation | Debug correctness        |
| Decorator factories   | Parameterized decorators |

---

Decorators are structural tools for runtime behavior modification and are foundational to modern Python backend architecture, middleware pipelines, and scalable codebase organization.
