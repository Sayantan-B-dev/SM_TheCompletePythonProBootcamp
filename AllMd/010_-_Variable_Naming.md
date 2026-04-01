### Variable Naming in Python — Rules, Conventions, and Best Practices

---

### 1. Why Variable Naming Matters

Variable names are **how humans understand your code**.
Good names reduce comments, prevent bugs, and make code maintainable.

---

### 2. Basic Naming Rules (Must Follow)

✔ Allowed:

```python
name = "Alex"
user_age = 25
_total = 100
```

❌ Not allowed:

```python
2name = "Alex"      # cannot start with a number
user-name = "Alex"  # hyphens not allowed
first name = "Alex" # spaces not allowed
class = 10          # Python keyword
```

Rules summary:

* Must start with a letter or `_`
* Can contain letters, numbers, `_`
* Case-sensitive
* Cannot be Python keywords

---

### 3. Snake Case (Python Standard)

```python
user_name = "Sam"
total_price = 499
```

* Lowercase
* Words separated by underscores
* **PEP 8 recommended**

---

### 4. Descriptive Over Short

❌ Bad:

```python
x = 25
y = 500
```

✔ Good:

```python
user_age = 25
account_balance = 500
```

---

### 5. Avoid Single-Letter Names (Except Loops)

✔ Acceptable:

```python
for i in range(10):
    print(i)
```

❌ Avoid:

```python
a = "username"
b = "email"
```

---

### 6. Boolean Variable Naming

```python
is_logged_in = True
has_permission = False
```

* Start with `is`, `has`, `can`
* Reads like plain English

---

### 7. Constants (By Convention)

```python
MAX_RETRIES = 3
API_TIMEOUT = 30
```

* Uppercase
* Signals “do not modify”

---

### 8. Avoid Shadowing Built-ins

❌ Bad:

```python
list = [1, 2, 3]
str = "hello"
```

✔ Good:

```python
numbers = [1, 2, 3]
text = "hello"
```

---

### 9. Meaningful Context

❌ Bad:

```python
data = 100
```

✔ Good:

```python
max_users = 100
```

---

### 10. Consistency Is Critical

❌ Bad:

```python
userName = "Sam"
user_age = 25
```

✔ Good:

```python
user_name = "Sam"
user_age = 25
```

---

### 11. Temporary Variables

```python
temp = glass1
```

* Use `temp` only when its purpose is obvious
* Otherwise, be explicit

---

### 12. Professional Naming Mindset

Ask yourself:

* What does this represent?
* Will this make sense in 6 months?
* Would another developer understand it instantly?

---

### Core Rule

**Code is read more than it is written.**
Clear variable naming is one of the fastest ways to write professional Python.
