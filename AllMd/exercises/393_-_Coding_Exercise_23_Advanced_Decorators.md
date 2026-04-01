```python
import functools

def logging_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Call original function and capture result
        result = func(*args, **kwargs)

        # Format positional arguments exactly as required
        args_str = ", ".join(str(arg) for arg in args)

        # Print exact expected format
        print(f"You called {func.__name__}({args_str})")
        print(f"It returned: {result}")

        return result

    return wrapper


@logging_decorator
def a_function(*args):
    return sum(args)


a_function(4, 5, 6)
```

# Deep Explanation of What Is Actually Happening in Your Decorator

Your code is a textbook example of how Python decorators replace a function with a wrapped version at definition time and execute additional logic at call time. Let us break it down precisely.

---

# 1. What Happens When Python Reads `@logging_decorator`

When Python sees:

```python
@logging_decorator
def a_function(*args):
    return sum(args)
```

Python does NOT simply store `a_function` as written.

Instead, it performs this transformation internally:

```python
a_function = logging_decorator(a_function)
```

This happens immediately after the function is created.

---

# 2. What `logging_decorator(a_function)` Actually Does

Inside `logging_decorator`:

```python
def logging_decorator(func):
```

At this moment:

* `func` refers to the original `a_function`.
* `func` is a function object stored in memory.

Then this line defines another function:

```python
def wrapper(*args, **kwargs):
```

Important:

* `wrapper` has access to `func`.
* This happens because of a **closure**.
* Python stores `func` inside `wrapper.__closure__`.

Finally:

```python
return wrapper
```

So now:

```
a_function = wrapper
```

The original `a_function` is no longer directly referenced by that name.

The name `a_function` now refers to `wrapper`.

---

# 3. What Happens When You Call `a_function(4, 5, 6)`

When you execute:

```python
a_function(4, 5, 6)
```

You are actually calling:

```
wrapper(4, 5, 6)
```

Not the original function.

---

# 4. Inside the Wrapper — Step-by-Step

### Step 1 — Arguments Captured

```python
def wrapper(*args, **kwargs):
```

`args` becomes:

```
(4, 5, 6)
```

`kwargs` becomes:

```
{}
```

---

### Step 2 — Call Original Function

```python
result = func(*args, **kwargs)
```

Remember:

* `func` refers to the original `a_function`.
* So this executes:

```python
sum((4, 5, 6))
```

Result:

```
15
```

---

### Step 3 — Format Arguments

```python
args_str = ", ".join(str(arg) for arg in args)
```

This converts:

```
(4, 5, 6)
```

into:

```
"4, 5, 6"
```

Step breakdown:

* Convert each element to string.
* Join them using comma + space.

---

### Step 4 — Print Logs

```python
print(f"You called {func.__name__}({args_str})")
```

`func.__name__` is `"a_function"` because of `@functools.wraps`.

Output:

```
You called a_function(4, 5, 6)
```

Then:

```
It returned: 15
```

---

### Step 5 — Return Result

```python
return result
```

So the caller still receives:

```
15
```

Even though extra logic executed before returning.

---

# 5. Why `functools.wraps` Is Important

Without this line:

```python
@functools.wraps(func)
```

The decorated function would lose metadata.

Check this:

```python
print(a_function.__name__)
```

Without wraps → prints `"wrapper"`
With wraps → prints `"a_function"`

`wraps` copies:

* `__name__`
* `__doc__`
* `__module__`
* `__annotations__`

This is essential in frameworks like Flask.

---

# 6. Memory Model Visualization

Before decoration:

```
a_function → original function object
```

After decoration:

```
a_function → wrapper
wrapper.__closure__ → reference to original function
```

So the original function is preserved inside the wrapper’s closure.

---

# 7. Call Stack Visualization

When you run:

```
a_function(4, 5, 6)
```

Call stack becomes:

```
wrapper →
    original a_function →
return →
wrapper →
return to caller
```

Execution flow:

```
Caller →
    wrapper →
        original function →
    wrapper prints →
return result
```

---

# 8. Conceptual Summary

Your decorator:

• Intercepts function calls
• Logs function name
• Logs arguments
• Logs return value
• Preserves original result
• Keeps original function intact inside closure
• Replaces function reference with wrapper

This is runtime behavior injection.

You did not modify `a_function`.

You modified how it behaves when called.

---

# 9. Core Mental Model

A decorator is not modifying the function body.

It is:

```
Replacing the function reference with another function
that calls the original function internally.
```

That is the entire mechanism.

---

# Final Understanding

When you call `a_function`, you are no longer calling the original function directly.

You are calling a wrapper that:

1. Receives inputs
2. Calls the original function
3. Captures result
4. Logs information
5. Returns the result

This is how decorators enable logging, authentication, caching, timing, and middleware behavior in real backend systems.
