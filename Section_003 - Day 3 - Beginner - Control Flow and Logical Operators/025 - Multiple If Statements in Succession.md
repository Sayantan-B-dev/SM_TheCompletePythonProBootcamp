### Multiple `if` Statements and Their Need

Multiple `if` statements mean using **more than one independent `if` block**, where **each condition is checked separately**, regardless of whether previous conditions are true or false.

---

### Syntax

```python
if condition1:
    # block 1

if condition2:
    # block 2

if condition3:
    # block 3
```

Each `if` is evaluated independently.

---

### Example: Independent Checks

```python
age = 25

if age >= 18:
    print("Eligible to vote")

if age >= 21:
    print("Eligible to drink")

if age >= 25:
    print("Eligible for car rental")
```

Output:

```text
Eligible to vote
Eligible to drink
Eligible for car rental
```

All true conditions execute.

---

### Why Multiple `if` Is Needed

Multiple `if` statements are used when:

* Conditions are **not mutually exclusive**
* More than one action should occur
* Each rule must be validated independently

---

### Example: Input Validation

```python
password = "Admin@123"

if len(password) < 8:
    print("Password too short")

if "@" not in password:
    print("Missing special character")

if password.islower():
    print("Must contain uppercase letter")
```

Multiple warnings can be shown at once.

---

### Example: System Health Checks

```python
cpu_usage = 85
memory_usage = 70
disk_space = 10

if cpu_usage > 80:
    print("High CPU usage")

if memory_usage > 75:
    print("High memory usage")

if disk_space < 15:
    print("Low disk space")
```

Each alert is independent.

---

### Multiple `if` vs `if–elif–else`

#### Using `if–elif–else` (Mutually Exclusive)

```python
marks = 90

if marks >= 90:
    print("A")
elif marks >= 75:
    print("B")
else:
    print("C")
```

Only one block executes.

---

#### Using Multiple `if` (Independent)

```python
marks = 90

if marks >= 50:
    print("Passed")

if marks >= 75:
    print("Good score")

if marks >= 90:
    print("Excellent")
```

All applicable blocks execute.

---

### Common Mistake

❌ Using `elif` when multiple outputs are required

```python
# WRONG
if temp > 30:
    print("Hot")
elif temp > 20:
    print("Warm")
elif temp > 10:
    print("Cool")
```

Only one description prints.

---

### Correct Approach

```python
# RIGHT
if temp > 10:
    print("Cool")

if temp > 20:
    print("Warm")

if temp > 30:
    print("Hot")
```

---

### Key Differences Summary

| Multiple `if`                        | `if–elif–else`           |
| ------------------------------------ | ------------------------ |
| All true conditions execute          | Only one executes        |
| Conditions are independent           | Conditions are exclusive |
| Used for validations, checks, alerts | Used for classification  |

---

### When to Use Multiple `if`

* Validation systems
* Rule engines
* Monitoring systems
* Feature toggles
* Permission checks
* Scoring systems

Multiple `if` statements give full control when logic must **accumulate results instead of choosing one path**.
