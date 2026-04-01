### Multiple return values (function returning more than one value)

In Python, a function can return **multiple values at once**. Internally, Python packs them into a **tuple**, even if you don’t explicitly write a tuple.

---

### Basic syntax

```python
def function_name():
    return value1, value2, value3
```

This is equivalent to:

```python
return (value1, value2, value3)
```

---

### Example 1: Returning two values

```python
def calculate_sum_diff(a, b):
    sum_ = a + b          # calculate sum
    diff = a - b          # calculate difference
    return sum_, diff     # returning two values
```

Usage and output:

```python
result = calculate_sum_diff(10, 4)
print(result)
```

Output:

```
(14, 6)
```

Explanation:

* Python returns a tuple `(14, 6)`
* Both values are preserved in order

---

### Example 2: Unpacking multiple return values

```python
total, difference = calculate_sum_diff(10, 4)
print("Total:", total)
print("Difference:", difference)
```

Output:

```
Total: 14
Difference: 6
```

Explanation:

* Tuple is unpacked into variables
* Order matters

---

### Example 3: Returning more than two values

```python
def calculate_all(a, b):
    add_ = a + b
    sub_ = a - b
    mul_ = a * b
    div_ = a / b if b != 0 else None
    return add_, sub_, mul_, div_
```

Usage:

```python
a, s, m, d = calculate_all(12, 3)
print(a, s, m, d)
```

Output:

```
15 9 36 4.0
```

Explanation:

* Four values returned
* Division safely handled

---

### Example 4: Partial unpacking using `_`

```python
sum_, _, product, _ = calculate_all(12, 3)
print(sum_, product)
```

Output:

```
15 36
```

Explanation:

* `_` is used to ignore unwanted values
* Common Python convention

---

### Example 5: Returning different types together

```python
def analyze_number(n):
    is_even = n % 2 == 0
    square = n * n
    cube = n ** 3
    return is_even, square, cube
```

Usage:

```python
even, sq, cb = analyze_number(5)
print(even, sq, cb)
```

Output:

```
False 25 125
```

Explanation:

* Mixed data types allowed
* Returned as a tuple

---

### Example 6: Returning a tuple explicitly (same result)

```python
def get_coordinates():
    x = 10
    y = 20
    return (x, y)
```

Usage:

```python
coords = get_coordinates()
print(coords)
```

Output:

```
(10, 20)
```

---

### Example 7: Returning a dictionary instead of tuple (alternative)

```python
def calculate_stats(numbers):
    return {
        "min": min(numbers),
        "max": max(numbers),
        "avg": sum(numbers) / len(numbers)
    }
```

Usage:

```python
stats = calculate_stats([10, 20, 30])
print(stats)
```

Output:

```
{'min': 10, 'max': 30, 'avg': 20.0}
```

Explanation:

* Dictionary return is better when meaning matters more than order

---

### Function with multiple `return` statements (conditional returns)

A function can have **many `return` statements**, but **only one executes per call**.

---

### Example 8: Multiple return paths

```python
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"
```

Usage:

```python
print(grade(92))
print(grade(78))
print(grade(40))
```

Output:

```
A
B
F
```

Explanation:

* Only one return runs
* Function exits immediately after return

---

### Example 9: Early return for validation

```python
def divide(a, b):
    if b == 0:
        return "Error"
    return a / b
```

Usage:

```python
print(divide(10, 2))
print(divide(10, 0))
```

Output:

```
5.0
Error
```

Explanation:

* Early return prevents crash
* Cleaner than nested logic

---

### Table: Multiple values vs multiple returns

| Concept                      | Meaning                       | Example          |
| ---------------------------- | ----------------------------- | ---------------- |
| Multiple return **values**   | Returning many values at once | `return a, b, c` |
| Multiple `return` statements | Different exit points         | `if: return x`   |
| Tuple unpacking              | Splitting returned values     | `x, y = func()`  |
| Dictionary return            | Named outputs                 | `return {"a":1}` |

---

### When to use what

* Few values, fixed order → tuple return
* Many values, clear meaning → dictionary return
* Validation / branching → multiple return statements
* Pipelines / chaining → tuple return

---

### Core takeaway

* Python always returns **one object**
* Multiple values = **one tuple**
* Multiple `return` statements ≠ multiple returns executed
* `return` immediately ends the function
