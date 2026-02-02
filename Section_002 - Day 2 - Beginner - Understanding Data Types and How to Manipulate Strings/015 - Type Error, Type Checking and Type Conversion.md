### TypeError, Type Checking, Type Conversion & ValueError — Complete, Practical Guide

---

## 1. **Type Checking (`type()` and `isinstance()`)**

### `type()`

```python
x = 10
print(type(x))
```

Output:

```
<class 'int'>
```

### `isinstance()` (Preferred in real code)

```python
x = "hello"

print(isinstance(x, str))
print(isinstance(x, int))
```

Output:

```
True
False
```

Why `isinstance()` is better:

* Works with inheritance
* Safer for validation
* Used in production code

---

## 2. **Type Conversion (Casting)**

### Common Conversions

```python
int("10")        # 10
float("3.14")    # 3.14
str(100)         # "100"
bool("hi")       # True
bool("")         # False
```

### Valid vs Invalid Conversion

| Conversion  | Example         | Result       |
| ----------- | --------------- | ------------ |
| str → int   | `int("25")`     | ✅ 25         |
| str → int   | `int("25.5")`   | ❌ ValueError |
| str → float | `float("25.5")` | ✅ 25.5       |
| str → int   | `int("abc")`    | ❌ ValueError |
| float → int | `int(3.9)`      | ✅ 3          |

---

## 3. **TypeError (Most Common Beginner Error)**

### What is TypeError?

Occurs when Python encounters **incompatible data types** in an operation.

---

### Common TypeError Examples

#### 1. String + Integer

```python
age = 25
print("Age: " + age)
```

❌ TypeError

✔ Fix:

```python
print("Age: " + str(age))
# or
print(f"Age: {age}")
```

---

#### 2. Input Without Conversion

```python
num = input("Enter number: ")
print(num + 5)
```

❌ TypeError

✔ Fix:

```python
num = int(input("Enter number: "))
print(num + 5)
```

---

#### 3. Wrong Function Argument Type

```python
len(10)
```

❌ TypeError (`len()` expects iterable)

✔ Fix:

```python
len(str(10))
```

---

#### 4. Mixing List and Int

```python
[1, 2, 3] + 4
```

❌ TypeError

✔ Fix:

```python
[1, 2, 3] + [4]
```

---

## 4. **ValueError (Wrong Value, Correct Type)**

### What is ValueError?

Occurs when the **type is correct**, but the **value is invalid**.

---

### Common ValueError Examples

#### 1. Invalid Integer Conversion

```python
int("abc")
```

❌ ValueError

---

#### 2. Decimal to Integer Directly

```python
int("3.14")
```

❌ ValueError

✔ Fix:

```python
int(float("3.14"))
```

---

#### 3. Out-of-range Input

```python
numbers = [1, 2, 3]
numbers.index(10)
```

❌ ValueError

---

## 5. **TypeError vs ValueError (Critical Difference)**

| Error      | Meaning         | Example       |
| ---------- | --------------- | ------------- |
| TypeError  | Wrong data type | `"5" + 5`     |
| ValueError | Wrong value     | `int("five")` |

---

## 6. **Input Validation (Prevent Errors)**

### Using `isdigit()`

```python
value = input("Enter number: ")

if value.isdigit():
    value = int(value)
else:
    print("Invalid input")
```

---

### Using `try-except` (Professional Way)

```python
try:
    num = int(input("Enter number: "))
    print(num + 10)
except ValueError:
    print("Please enter a valid number")
```

---

## 7. **Implicit vs Explicit Conversion**

### Implicit (Python does it)

```python
print(5 + 2.5)
```

Output:

```
7.5
```

---

### Explicit (You do it)

```python
print(str(5) + " apples")
```

---

## 8. **Checking Before Converting**

```python
value = input("Enter age: ")

if isinstance(value, str):
    value = value.strip()
```

---

## 9. **Common Beginner Mistakes Summary**

| Mistake                        | Error      |
| ------------------------------ | ---------- |
| Forgetting input is string     | TypeError  |
| Converting invalid string      | ValueError |
| Using wrong operation          | TypeError  |
| Assuming Python guesses intent | Both       |

---

## 10. **Professional Rules to Avoid Errors**

* Never trust user input
* Convert explicitly
* Validate before processing
* Prefer `isinstance()` over `type()`
* Use `try-except` for user-facing programs

---

### Core Mental Model

* **TypeError** → wrong *type*
* **ValueError** → wrong *value*
* **Type checking** → prevention
* **Type conversion** → control

If you internalize this distinction, Python errors stop being confusing and start becoming **useful signals**.
