### Logical Operators in Python

Logical operators are used to **combine multiple conditions** and evaluate them as a single boolean expression. They always return either `True` or `False`.

---

### Logical Operators Overview

| Operator | Meaning     | Description                                |
| -------- | ----------- | ------------------------------------------ |
| `and`    | Logical AND | True if **all** conditions are true        |
| `or`     | Logical OR  | True if **at least one** condition is true |
| `not`    | Logical NOT | Inverts the condition                      |

---

### `and` Operator

Returns `True` only when **both conditions are true**.

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")
```

Truth Table:

| A     | B     | A and B |
| ----- | ----- | ------- |
| True  | True  | True    |
| True  | False | False   |
| False | True  | False   |
| False | False | False   |

---

### `or` Operator

Returns `True` if **any one condition is true**.

```python
is_admin = False
is_moderator = True

if is_admin or is_moderator:
    print("Access granted")
```

Truth Table:

| A     | B     | A or B |
| ----- | ----- | ------ |
| True  | True  | True   |
| True  | False | True   |
| False | True  | True   |
| False | False | False  |

---

### `not` Operator

Reverses the boolean value.

```python
is_logged_in = False

if not is_logged_in:
    print("Please log in")
```

Truth Table:

| A     | not A |
| ----- | ----- |
| True  | False |
| False | True  |

---

### Combining Multiple Logical Operators

```python
age = 22
has_id = True
is_blacklisted = False

if age >= 18 and has_id and not is_blacklisted:
    print("Access approved")
```

---

### Operator Precedence (Important)

Order of evaluation:

1. `not`
2. `and`
3. `or`

```python
result = True or False and False
print(result)  # True
```

Explanation:

* `False and False` → False
* `True or False` → True

---

### Using Parentheses for Clarity

```python
result = (True or False) and False
print(result)  # False
```

---

### Multiple Condition Examples

#### Range Checking

```python
num = 15

if num >= 10 and num <= 20:
    print("Number is within range")
```

Pythonic way:

```python
if 10 <= num <= 20:
    print("Number is within range")
```

---

#### Login Validation

```python
username = "admin"
password = "1234"

if username == "admin" and password == "1234":
    print("Login successful")
```

---

#### Discount Eligibility

```python
age = 65
is_member = True

if age >= 60 or is_member:
    print("Discount applied")
```

---

### Nested Logical Conditions

```python
marks = 78
attendance = 80

if marks >= 50:
    if attendance >= 75:
        print("Eligible for exam")
    else:
        print("Low attendance")
else:
    print("Low marks")
```

Equivalent combined version:

```python
if marks >= 50 and attendance >= 75:
    print("Eligible for exam")
```

---

### Multiple `if` with Logical Operators

```python
temp = 35

if temp > 30:
    print("Hot")

if temp > 20 and temp <= 30:
    print("Warm")

if temp <= 20:
    print("Cool")
```

---

### Common Logical Patterns

#### Exclusive Conditions

```python
if x > 0 and x < 10:
    print("Single digit positive")
```

---

#### Negation

```python
if not (age < 18):
    print("Adult")
```

Equivalent:

```python
if age >= 18:
    print("Adult")
```

---

### Logical Operators with Non-Boolean Values

Python treats some values as `False` automatically.

Falsy values:

* `0`
* `None`
* `""`
* `[]`, `{}`, `()`
* `False`

```python
username = ""

if not username:
    print("Username is empty")
```

---

### Short-Circuit Behavior (Critical Concept)

```python
def check():
    print("Checked")
    return True

if True or check():
    print("Done")
```

`check()` never executes because `True or ...` short-circuits.

---

### Common Mistakes

❌ Using `&` instead of `and`

```python
# WRONG
if a > 5 & b < 10:
    pass
```

✅ Correct

```python
if a > 5 and b < 10:
    pass
```

---

### Summary Table

| Pattern       | Use Case                    |
| ------------- | --------------------------- |
| `and`         | All conditions must be true |
| `or`          | Any condition must be true  |
| `not`         | Reverse logic               |
| Parentheses   | Control precedence          |
| Short-circuit | Performance optimization    |

---

### Interview-Level Example

```python
age = 25
citizen = True
criminal_record = False

if (age >= 18 and citizen) and not criminal_record:
    print("Eligible to vote")
```

Logical operators are the backbone of decision-making, validations, access control, and rule-based systems in Python.
