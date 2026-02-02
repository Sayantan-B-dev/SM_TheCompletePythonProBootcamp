### Printing in Python — Complete Overview

---

### 1. Basic Printing

```python
print("Hello, World")
print(10)
print(3.14)
```

* `print()` displays output to the console.
* Python automatically converts values to strings.

---

### 2. Printing Variables

```python
name = "Alex"
age = 25
print(name)
print(age)
```

* Variables can be printed directly without casting.

---

### 3. Printing Multiple Values

```python
print("Name:", name, "Age:", age)
```

* Commas automatically insert spaces between values.

---

### 4. Custom Separators (`sep`)

```python
print("2026", "02", "01", sep="-")
```

Output:

```
2026-02-01
```

---

### 5. Controlling Line Endings (`end`)

```python
print("Loading", end="...")
print("done")
```

Output:

```
Loading...done
```

---

### 6. Formatted Printing (f-strings — Recommended)

```python
price = 49.5
print(f"Total price: ₹{price:.2f}")
```

* Clean, readable, and fast.
* Supports expressions inside `{}`.

---

### 7. `format()` Method

```python
print("Score: {} / {}".format(8, 10))
```

* Older but still widely used.

---

### 8. Escape Characters

```python
print("Line1\nLine2")
print("Column1\tColumn2")
print("Path: C:\\Users\\Admin")
```

---

### 9. Raw Strings

```python
print(r"C:\new_folder\test")
```

* Useful for file paths and regular expressions.

---

### 10. Printing Data Structures

```python
print([1, 2, 3])
print({"a": 1, "b": 2})
```

For better readability:

```python
from pprint import pprint
pprint({"a": 1, "b": {"x": 10, "y": 20}})
```

---

### 11. Debug Printing

```python
print("Value of x:", x)
```

* Common during development to trace logic.

---

### 12. Printing vs Returning

```python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)
```

* `print()` shows output.
* `return` sends data from a function.
* Professional code favors `return`, not print.

---

### 13. Printing Inside Loops

```python
for i in range(3):
    print("Iteration:", i)
```

---

### 14. Best Practices

* Use `print()` for learning and debugging.
* Avoid excessive printing in production code.
* Prefer logging for real applications.
* Keep output readable and intentional.

---

Printing is your **primary visibility tool** in Python.
If you understand `print()`, debugging and learning become significantly easier.
