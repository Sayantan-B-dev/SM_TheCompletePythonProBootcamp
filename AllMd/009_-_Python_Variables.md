### Variables in Python — Complete Guide

---

### 1. What a Variable Is

A variable is a **named reference to a value stored in memory**.
It allows you to store data and reuse it throughout your program.

```python
age = 25
name = "Alex"
```

---

### 2. Creating Variables (Assignment)

```python
x = 10
pi = 3.14
is_active = True
```

* Python is **dynamically typed**
* No need to declare data types explicitly

---

### 3. Variable Types (Common)

```python
count = 5          # int
price = 99.99      # float
username = "sam"   # str
is_logged_in = True  # bool
```

---

### 4. Reassigning Variables

```python
score = 10
score = 20
```

Variables can change values during execution.

---

### 5. Naming Rules

✔ Valid:

```python
user_name = "Sam"
total_score = 100
```

❌ Invalid:

```python
2name = "Sam"
user-name = "Sam"
class = 10
```

Rules:

* Must start with a letter or `_`
* Cannot start with a number
* No spaces
* Cannot use Python keywords

---

### 6. Naming Conventions (Professional)

```python
user_age = 24
total_price = 500
```

* Use **snake_case**
* Use descriptive names
* Avoid single-letter names (except loops)

---

### 7. Multiple Assignment

```python
x, y, z = 1, 2, 3
```

---

### 8. Constants (By Convention)

```python
PI = 3.14159
MAX_USERS = 100
```

Python does not enforce constants, uppercase signals intent.

---

### 9. Variable Types Can Change

```python
x = 10
x = "ten"
```

Allowed, but avoid in professional code.

---

### 10. Using Variables in Strings

```python
name = "Alex"
age = 25

print(f"{name} is {age} years old")
```

---

### 11. Variables and Input

```python
city = input("Enter city: ")
```

Input values are stored as strings.

---

### 12. Variable Scope (Intro)

```python
x = 10

def test():
    y = 5
```

* `x` → global
* `y` → local

---

### 13. Common Variable Mistakes

❌ Using before assignment:

```python
print(x)
x = 5
```

❌ Overwriting built-ins:

```python
list = [1, 2, 3]
```

---

### 14. Best Practices

* Use meaningful names
* Keep variables close to where they’re used
* Avoid global variables when possible
* Don’t reuse variables for different purposes

---

### Core Idea

Variables are the **building blocks of logic**.
Clear variable naming leads to clear thinking and clean code.
