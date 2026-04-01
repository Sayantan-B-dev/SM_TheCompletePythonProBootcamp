## Default Values in Python — Power and Advanced Argument Mechanics

---

## Core Definition

> A **default argument** is a function parameter that assumes a predefined value **if no argument is provided** during the function call.

```python
def greet(name="Guest"):
    print(f"Hello, {name}")
```

```python
greet()
greet("Alice")
```

**Expected Output**

```
Hello, Guest
Hello, Alice
```

---

## Why Default Arguments Are Powerful

Default values enable:

* Optional behavior without extra conditionals
* Clean APIs with minimal required inputs
* Backward compatibility when extending functions
* Declarative configuration-style function calls

They reduce **branching logic** inside functions and shift responsibility to the function signature.

---

## How Python Evaluates Default Arguments (CRITICAL)

> **Default arguments are evaluated once — at function definition time, not at call time.**

This rule explains both their power and their most dangerous pitfall.

---

## Immutable Default Arguments (Safe)

### Example: Integers, Strings, Tuples

```python
def increment(x, step=1):
    return x + step
```

Why this is safe:

* `1` is immutable
* Each call receives a fresh value
* No shared state

```python
increment(5)
increment(5, 3)
```

**Expected Output**

```
6
8
```

---

## Mutable Default Arguments (DANGEROUS)

### The Classic Bug

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
```

```python
add_item("apple")
add_item("banana")
```

**Expected Output**

```
['apple']
['apple', 'banana']
```

### Why This Happens

```text
bucket = []   ← created once
↓
call 1 → append 'apple'
↓
call 2 → append 'banana' to SAME list
```

The list persists across calls.

---

## The Correct Pattern (Professional Standard)

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

```python
add_item("apple")
add_item("banana")
```

**Expected Output**

```
['apple']
['banana']
```

> `None` is immutable and used as a **sentinel value**

---

## Keyword Arguments + Defaults (API Power)

```python
def connect(host="localhost", port=5432, timeout=30):
    print(host, port, timeout)
```

```python
connect()
connect(port=3306)
connect(timeout=5)
```

**Expected Output**

```
localhost 5432 30
localhost 3306 30
localhost 5432 5
```

---

## Default Arguments as Feature Toggles

```python
def log(message, debug=False):
    if debug:
        print("[DEBUG]", message)
```

```python
log("Saved")
log("Saved", debug=True)
```

**Expected Output**

```
[DEBUG] Saved
```

No extra flags. No conditionals outside.

---

## Advanced Pattern: Defaults as Configuration Objects

```python
def train_model(
    epochs=10,
    lr=0.001,
    batch_size=32,
    verbose=True
):
    if verbose:
        print("Training started")
```

This creates:

* Readable signatures
* Self-documenting functions
* IDE-friendly autocompletion

---

## Keyword-Only Default Arguments (Advanced Control)

```python
def create_user(username, *, active=True, admin=False):
    print(username, active, admin)
```

```python
create_user("sam")
create_user("sam", admin=True)
```

**Expected Output**

```
sam True False
sam True True
```

> `*` forces arguments after it to be **explicitly named**

---

## Mixing Positional, Default, and Variadic Arguments

```python
def report(title, level=1, *tags, urgent=False):
    print(title, level, tags, urgent)
```

```python
report("Bug", 2, "backend", "db", urgent=True)
```

**Expected Output**

```
Bug 2 ('backend', 'db') True
```

---

## Default Arguments + Lambdas

```python
def power_factory(exp=2):
    return lambda x: x ** exp
```

```python
square = power_factory()
cube = power_factory(3)

square(4)
cube(4)
```

**Expected Output**

```
16
64
```

Defaults become **behavioral presets**.

---

## Using Defaults to Avoid Conditionals

### Bad Style

```python
def save(data, format):
    if format is None:
        format = "json"
```

### Good Style

```python
def save(data, format="json"):
    pass
```

Logic moves into the signature.

---

## Default Argument Evaluation Timeline

```text
1. def statement runs
2. Default values are created
3. Function object is stored
4. Calls reuse those defaults
```

This is why mutables persist.

---

## Edge Case: Default Depends on Another Argument (NOT ALLOWED)

```python
def bad(x, y=x):  # ERROR
    pass
```

Defaults are evaluated **before parameters exist**.

### Correct Approach

```python
def good(x, y=None):
    if y is None:
        y = x
```

---

## Best Practices (Professional Rules)

| Rule                           | Reason             |
| ------------------------------ | ------------------ |
| Use immutables as defaults     | Safe, predictable  |
| Use `None` for mutables        | Avoid shared state |
| Prefer keyword defaults        | Readability        |
| Use `*` for keyword-only flags | API safety         |
| Treat signature as interface   | Self-documenting   |

