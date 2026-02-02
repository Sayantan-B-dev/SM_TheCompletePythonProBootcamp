### `if` and `else` in Python (with relational operators)

Control flow using `if` and `else` allows a program to make decisions based on conditions. These conditions are formed using **relational (comparison) operators**, which compare two values and return a boolean result (`True` or `False`).

---

### Common Relational Operators

```text
>   greater than
<   less than
>=  greater than or equal to
<=  less than or equal to
==  equal to
!=  not equal to
```

---

### Basic `if` Statement

```python
age = 18

if age >= 18:
    print("You are eligible to vote")
```

Explanation:
The condition `age >= 18` is evaluated. If it is `True`, the indented block executes.

---

### `if` – `else` Structure

```python
age = 16

if age >= 18:
    print("You are eligible to vote")
else:
    print("You are not eligible to vote")
```

Explanation:
If the condition is `True`, the `if` block runs. Otherwise, the `else` block runs.

---

### Using `>` and `<`

```python
a = 10
b = 20

if a > b:
    print("a is greater than b")
else:
    print("a is less than or equal to b")
```

---

### Using `==` (Equality Check)

```python
password = "admin123"

if password == "admin123":
    print("Access granted")
else:
    print("Access denied")
```

Note:
`==` compares values.
`=` is used for assignment.

---

### Using `!=` (Not Equal)

```python
username = "guest"

if username != "admin":
    print("Limited access")
else:
    print("Full access")
```

---

### Using `<=` and `>=`

```python
marks = 40

if marks >= 35:
    print("Pass")
else:
    print("Fail")
```

```python
temperature = 25

if temperature <= 30:
    print("Weather is comfortable")
else:
    print("Weather is hot")
```

---

### Multiple Conditions with `if`, `elif`, `else`

```python
score = 75

if score >= 90:
    print("Grade A")
elif score >= 75:
    print("Grade B")
elif score >= 50:
    print("Grade C")
else:
    print("Fail")
```

---

### Nested `if` Statements

```python
age = 20
has_id = True

if age >= 18:
    if has_id == True:
        print("Entry allowed")
    else:
        print("ID required")
else:
    print("Underage")
```

---

### Key Rules to Remember

* Conditions must evaluate to `True` or `False`
* Indentation is mandatory in Python
* `if` executes only when the condition is `True`
* `else` executes when the condition is `False`
* Use relational operators to build meaningful conditions

---

This structure forms the foundation of decision-making in Python programs.
