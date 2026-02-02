### Practical Tips from Topics Learned So Far (Python Control Flow & Logic)

---

## 1. Think in **Conditions**, Not Code

Before writing code, clearly state the logic in plain English.

| English Logic             | Python Condition |
| ------------------------- | ---------------- |
| “If age is 18 or more”    | `age >= 18`      |
| “If number is even”       | `num % 2 == 0`   |
| “If both are true”        | `and`            |
| “If at least one is true” | `or`             |
| “If not allowed”          | `not allowed`    |

```python
# Always convert real-world rules into conditions first
if age >= 18 and has_id:
    print("Allowed")
```

---

## 2. Use `elif` Only for **Mutually Exclusive** Conditions

If only **one outcome** should happen, use `if–elif–else`.

```python
# Correct usage
if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
else:
    grade = "C"
```

❌ Wrong logic:

```python
# This blocks valid checks
if marks >= 50:
    print("Pass")
elif marks >= 75:
    print("Good")
```

---

## 3. Use Multiple `if` When You Need **Multiple Outputs**

```python
# Each condition is checked independently
if score >= 50:
    print("Passed")

if score >= 75:
    print("Good score")

if score >= 90:
    print("Excellent")
```

---

## 4. Prefer Combined Conditions Over Deep Nesting

❌ Hard to read:

```python
if age >= 18:
    if has_id:
        if not banned:
            print("Allowed")
```

✅ Cleaner and professional:

```python
if age >= 18 and has_id and not banned:
    print("Allowed")
```

---

## 5. Master Modulo (`%`) — It’s a Power Tool

| Use Case       | Condition      |
| -------------- | -------------- |
| Even number    | `n % 2 == 0`   |
| Odd number     | `n % 2 != 0`   |
| Divisible by 5 | `n % 5 == 0`   |
| Cyclic logic   | `index % size` |

```python
# Pattern logic
for i in range(1, 6):
    if i % 2 == 0:
        print("Even turn")
    else:
        print("Odd turn")
```

---

## 6. Always Remember Operator Precedence

Order:

1. `not`
2. `and`
3. `or`

```python
# This may confuse beginners
if a or b and c:
    pass

# Always prefer clarity
if a or (b and c):
    pass
```

---

## 7. Use Pythonic Range Checks

❌ Avoid:

```python
if x >= 10 and x <= 20:
    pass
```

✅ Prefer:

```python
if 10 <= x <= 20:
    pass
```

---

## 8. Validate Inputs Early

```python
# Defensive programming
if age <= 0:
    print("Invalid age")
    return
```

```python
# Safe numeric input
try:
    num = int(input("Enter number: "))
except ValueError:
    print("Invalid number")
```

---

## 9. Use Boolean Variables Properly

❌ Avoid:

```python
if has_id == True:
    pass
```

✅ Professional:

```python
if has_id:
    pass
```

---

## 10. Learn Short-Circuit Logic (Efficiency)

```python
# Safe evaluation
if user and user.is_active:
    print("Active user")
```

```python
# Prevents crash if user is None
```

---

## 11. Use Meaningful Variable Names

❌ Bad:

```python
if a and b:
    pass
```

✅ Good:

```python
if is_logged_in and has_permission:
    pass
```

---

## 12. Comment the *Why*, Not the *What*

❌ Useless comment:

```python
if x > 5:  # check if x is greater than 5
```

✅ Professional comment:

```python
# Minimum value required to unlock feature
if x > 5:
```

---

## 13. Debug with Truth Tables

| A | B | A and B | A or B |
| - | - | ------- | ------ |
| T | T | T       | T      |
| T | F | F       | T      |
| F | T | F       | T      |
| F | F | F       | F      |

Use tables when logic feels confusing.

---

## 14. Avoid Logical Traps

❌ Always true condition:

```python
if age > 18 or age < 60:
```

✅ Correct:

```python
if age > 18 and age < 60:
```

---

## 15. Real-World Mental Model

| Concept | Real Meaning      |
| ------- | ----------------- |
| `if`    | Decision          |
| `elif`  | Alternative       |
| `else`  | Default           |
| `%`     | Remainder / cycle |
| `and`   | All rules apply   |
| `or`    | Any rule applies  |
| `not`   | Restriction       |

---

## FINAL ADVICE

* Write logic first, code second
* Favor clarity over cleverness
* Reduce nesting with combined conditions
* Always test edge cases
* Treat conditionals as business rules

These foundations are exactly what real-world Python, interviews, and backend systems rely on.
