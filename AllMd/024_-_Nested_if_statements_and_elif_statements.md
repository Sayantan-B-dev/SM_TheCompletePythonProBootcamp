### `elif` in Python

`elif` stands for **else if**. It is used when there are **multiple conditions** to check in sequence. Python evaluates conditions from top to bottom and executes **only the first block that evaluates to `True`**.

---

### Basic `if – elif – else` Structure

```python
if condition1:
    # executes if condition1 is True
elif condition2:
    # executes if condition2 is True
else:
    # executes if none of the above conditions are True
```

---

### Example: Number Classification

```python
num = 0

if num > 0:
    print("Positive number")
elif num < 0:
    print("Negative number")
else:
    print("Zero")
```

---

### Example: Grading System

```python
marks = 82

if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 50:
    print("Grade C")
else:
    print("Fail")
```

Only one block executes, even if multiple conditions are technically true.

---

### Using Relational Operators with `elif`

```python
age = 65

if age < 13:
    print("Child")
elif age >= 13 and age < 60:
    print("Adult")
else:
    print("Senior citizen")
```

---

### Multiple `elif` Blocks

```python
day = 3

if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3:
    print("Wednesday")
elif day == 4:
    print("Thursday")
else:
    print("Invalid day")
```

---

### Nested `if – else`

A nested `if` means placing an `if` statement **inside another `if` or `else` block**. This is used when a decision depends on a previous decision.

---

### Basic Nested Structure

```python
if condition1:
    if condition2:
        # executes when both condition1 and condition2 are True
    else:
        # executes when condition1 is True and condition2 is False
else:
    # executes when condition1 is False
```

---

### Example: Login Validation

```python
username = "admin"
password = "1234"

if username == "admin":
    if password == "1234":
        print("Login successful")
    else:
        print("Incorrect password")
else:
    print("Invalid username")
```

---

### Example: Voting Eligibility with ID Check

```python
age = 20
has_id = True

if age >= 18:
    if has_id == True:
        print("Allowed to vote")
    else:
        print("ID required")
else:
    print("Not eligible to vote")
```

---

### Nested `elif`

```python
score = 78

if score >= 50:
    if score >= 90:
        print("Excellent")
    elif score >= 75:
        print("Very good")
    else:
        print("Pass")
else:
    print("Fail")
```

---

### `elif` vs Nested `if`

Using `elif` (preferred when conditions are mutually exclusive):

```python
x = 10

if x == 5:
    print("Five")
elif x == 10:
    print("Ten")
else:
    print("Other")
```

Using nested `if` (used when conditions depend on each other):

```python
x = 10

if x > 0:
    if x % 2 == 0:
        print("Positive even number")
    else:
        print("Positive odd number")
else:
    print("Non-positive number")
```

---

### Key Rules

* `elif` is checked only if previous conditions are `False`
* Only one block in an `if–elif–else` chain executes
* Nested `if` is useful for dependent conditions
* Indentation defines scope and logic in Python
