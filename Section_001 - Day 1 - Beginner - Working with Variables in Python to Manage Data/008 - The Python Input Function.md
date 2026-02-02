### Input in Python — Complete Guide

---

### 1. What `input()` Does

```python
name = input("Enter your name: ")
print(name)
```

* `input()` pauses the program and waits for user input.
* Whatever the user types is returned as a **string**.

---

### 2. Input Is Always a String (Very Important)

```python
age = input("Enter your age: ")
print(type(age))
```

Output:

```
<class 'str'>
```

Even if the user types `25`, Python treats it as `"25"`.

---

### 3. Converting Input to Numbers

```python
age = int(input("Enter your age: "))
height = float(input("Enter your height: "))
```

* `int()` → whole numbers
* `float()` → decimal numbers

❌ Without conversion:

```python
print("Next year you will be " + age)
```

✔ With conversion:

```python
print(f"Next year you will be {age + 1}")
```

---

### 4. Input with Prompt Messages

```python
city = input("Which city did you grow up in? ")
pet = input("What is your pet's name? ")
```

Prompts guide the user and improve UX.

---

### 5. Storing and Using Input

```python
name = input("Name: ")
print(f"Welcome, {name}")
```

Input is usually stored in variables for later use.

---

### 6. Input in Calculations

```python
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print(num1 + num2)
```

Always convert before math operations.

---

### 7. Multiple Inputs (One by One)

```python
username = input("Username: ")
password = input("Password: ")
```

Python does not support multiple inputs in one `input()` call like some languages.

---

### 8. Stripping Extra Spaces

```python
name = input("Enter name: ").strip()
```

Removes accidental leading/trailing spaces.

---

### 9. Lowercase / Uppercase Normalization

```python
choice = input("Yes or No: ").lower()
```

Useful for comparisons:

```python
if choice == "yes":
    print("Confirmed")
```

---

### 10. Input Validation (Basic)

```python
age = input("Enter age: ")

if age.isdigit():
    age = int(age)
else:
    print("Invalid input")
```

Prevents crashes due to bad input.

---

### 11. Common Input Errors

**TypeError**

```python
age = input("Age: ")
print(age + 1)   # ❌
```

**ValueError**

```python
age = int(input("Age: "))  # ❌ if user types text
```

---

### 12. Input Inside Loops

```python
while True:
    command = input("Enter command: ")
    if command == "exit":
        break
```

Used in CLI apps, games, tools.

---

### 13. Input vs Hardcoded Values

```python
# Hardcoded
name = "Alex"

# Dynamic
name = input("Enter name: ")
```

Professional programs prefer **dynamic input**.

---

### 14. Best Practices

* Always assume user input can be wrong
* Convert types explicitly
* Strip and normalize strings
* Validate before processing
* Keep prompts clear and simple

---

### Core Idea

`input()` is how your program **talks to humans**.
Understanding it properly is essential before moving to projects, games, automation, or APIs.

Master input early — it unlocks real interaction.


### Commenting in Python — Complete Guide

---

### 1. What Comments Are

Comments are **notes written in code** that Python ignores during execution.
They are used to explain *why* something exists, not just *what* it does.

---

### 2. Single-Line Comments (`#`)

```python
# This prints a welcome message
print("Hello, World")
```

* Everything after `#` on the line is ignored by Python.
* Most commonly used type of comment.

---

### 3. Inline Comments

```python
age = 25  # user's age in years
```

Use inline comments **sparingly** and only when clarity is needed.

---

### 4. Multi-Line Comments (Recommended Way)

```python
# Step 1: Ask the user for input
# Step 2: Convert input to integer
# Step 3: Perform calculation
```

Python does not have true multi-line comments.
Multiple `#` lines are the correct professional approach.

---

### 5. Docstrings (Documentation Comments)

```python
def add(a, b):
    """
    Adds two numbers and returns the result.
    """
    return a + b
```

* Used to document functions, classes, and modules
* Accessible using `help(add)`

---

### 6. Module-Level Docstrings

```python
"""
This module handles user authentication
and input validation.
"""
```

Placed at the top of a file to describe its purpose.

---

### 7. Commenting Bad vs Good

❌ Bad:

```python
x = x + 1  # add 1 to x
```

✔ Good:

```python
# Increment retry count after failed login
retry_count += 1
```

---

### 8. Commenting for Debugging

```python
# print(user_data)
```

Quick way to disable lines during testing.

---

### 9. When NOT to Comment

```python
print("Hello")  # prints hello ❌
```

Obvious code does not need comments.

---

### 10. Indentation and Comments

```python
if is_logged_in:
    # Allow access to dashboard
    show_dashboard()
```

Comments must follow Python’s indentation rules.

---

### 11. Common Beginner Mistakes

* Over-commenting obvious code
* Commenting *what* instead of *why*
* Leaving outdated comments
* Using comments instead of clean code

---

### 12. Professional Commenting Rules

* Explain intent, not syntax
* Keep comments up to date
* Use docstrings for public APIs
* Let code be readable first

---

### Core Principle

Good code explains **how**.
Good comments explain **why**.

Master commenting early and your code will scale, survive reviews, and stay readable.
