### Number Manipulation & f-Strings in Python — Practical Guide

---

## 1. Basic Number Manipulation

```python
x = 10
x = x + 1
print(x)   # 11
```

Same logic, cleaner:

```python
x += 1
```

---

## 2. Incrementing & Decrementing Operators

| Operator | Meaning               | Example   | Result       |
| -------- | --------------------- | --------- | ------------ |
| `+=`     | Add and assign        | `x += 3`  | `x = x + 3`  |
| `-=`     | Subtract and assign   | `x -= 2`  | `x = x - 2`  |
| `*=`     | Multiply and assign   | `x *= 4`  | `x = x * 4`  |
| `/=`     | Divide and assign     | `x /= 2`  | `x = x / 2`  |
| `//=`    | Floor divide & assign | `x //= 3` | `x = x // 3` |
| `%=`     | Modulus & assign      | `x %= 4`  | `x = x % 4`  |
| `**=`    | Power & assign        | `x **= 2` | `x = x ** 2` |

---

## 3. Real Example

```python
score = 0

score += 10
score -= 3
score *= 2

print(score)  # 14
```

---

## 4. f-Strings (Formatted Strings)

### Basic Usage

```python
name = "Alex"
age = 25

print(f"My name is {name} and I am {age} years old")
```

---

### Expressions Inside f-Strings

```python
x = 5
y = 3

print(f"Sum: {x + y}")
print(f"Square: {x ** 2}")
```

---

### Formatting Numbers

```python
price = 49.56789

print(f"Price: ₹{price:.2f}")
```

---

### Percentages

```python
score = 87
total = 100

print(f"Score: {(score / total) * 100:.1f}%")
```

---

## 5. f-Strings vs Other Methods

❌ Old style:

```python
print("Age: " + str(age))
```

✔ Modern:

```python
print(f"Age: {age}")
```

---

## 6. Combining Assignment Operators + f-Strings

```python
count = 1
count += 1

print(f"Count is now {count}")
```

---

## 7. Common Beginner Mistakes

❌ Expecting ++ or -- to work:

```python
x++
```

Python does **not** support `++` or `--`.

✔ Correct:

```python
x += 1
```

---

## 8. Precision & Rounding

```python
value = 3.14159
value += 1.5

print(f"Value: {value:.2f}")
```

---

## 9. Practical Example (Game Score)

```python
score = 100
score -= 20
score += 50

print(f"Final score: {score}")
```

---

## 10. Mental Model

* Assignment operators **modify variables in place**
* f-strings **evaluate expressions inside `{}`**
* Cleaner code = fewer bugs

---

### Core Rule

If you see code like:

```python
x = x + 1
```

You should instinctively write:

```python
x += 1
```

Mastering these makes your Python code **shorter, clearer, and more professional**.
