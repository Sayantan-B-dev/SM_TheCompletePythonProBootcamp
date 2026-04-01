**Debugging Difficulty: LEVEL 1 (Beginner / Obvious Bugs)**
Level 1 bugs are **immediate, loud, and local**. Python either refuses to run or crashes instantly. The mistake is usually on the same line where the error appears.

Below are **10 Level-1 debugging examples**, each with:

* buggy code
* error / wrong behavior
* corrected solution
* short reasoning

---

### 1. Missing colon in `if`

**Buggy code**

```python
age = 18
if age >= 18
    print("Adult")
```

**Error**

```
SyntaxError: expected ':'
```

**Fix**

```python
age = 18
if age >= 18:
    print("Adult")
```

**Why**
Python requires `:` to start a block.

---

### 2. Wrong indentation

**Buggy code**

```python
if True:
print("Hello")
```

**Error**

```
IndentationError: expected an indented block
```

**Fix**

```python
if True:
    print("Hello")
```

**Why**
Indentation defines scope in Python.

---

### 3. Using undefined variable

**Buggy code**

```python
print(score)
```

**Error**

```
NameError: name 'score' is not defined
```

**Fix**

```python
score = 0
print(score)
```

**Why**
Variable must exist before use.

---

### 4. Adding string and integer

**Buggy code**

```python
a = input()
b = 10
print(a + b)
```

**Error**

```
TypeError: can only concatenate str (not "int") to str
```

**Fix**

```python
a = int(input())
b = 10
print(a + b)
```

**Why**
`input()` always returns `str`.

---

### 5. Index out of range

**Buggy code**

```python
nums = [1, 2, 3]
print(nums[3])
```

**Error**

```
IndexError: list index out of range
```

**Fix**

```python
nums = [1, 2, 3]
print(nums[2])
```

**Why**
Indexing starts at `0`.

---

### 6. Key not found in dictionary

**Buggy code**

```python
data = {"a": 1}
print(data["b"])
```

**Error**

```
KeyError: 'b'
```

**Fix**

```python
data = {"a": 1}
print(data.get("b", "Not found"))
```

**Why**
Dictionary keys must exist.

---

### 7. Calling non-existent method

**Buggy code**

```python
name = "python"
name.push("!")
```

**Error**

```
AttributeError: 'str' object has no attribute 'push'
```

**Fix**

```python
name = "python"
name += "!"
```

**Why**
Strings are immutable and have fixed methods.

---

### 8. Forgetting to call a function

**Buggy code**

```python
def greet():
    print("Hello")

greet
```

**Output**

```
(no output)
```

**Fix**

```python
def greet():
    print("Hello")

greet()
```

**Why**
Function reference ≠ function call.

---

### 9. Wrong number of arguments

**Buggy code**

```python
def add(a, b):
    print(a + b)

add(5)
```

**Error**

```
TypeError: add() missing 1 required positional argument
```

**Fix**

```python
add(5, 3)
```

**Why**
Function signature must be respected.

---

### 10. Division by zero

**Buggy code**

```python
x = 10
y = 0
print(x / y)
```

**Error**

```
ZeroDivisionError: division by zero
```

**Fix**

```python
x = 10
y = 0

if y != 0:
    print(x / y)
else:
    print("Cannot divide by zero")
```

**Why**
Mathematical rule violated → runtime error.

---

### LEVEL 1 PATTERN SUMMARY

| Signal             | Meaning                     |
| ------------------ | --------------------------- |
| Red underline      | Syntax / obvious type issue |
| Immediate crash    | Runtime error               |
| Error line obvious | Bug is local                |
| Fix is small       | 1–2 line change             |

Level-1 bugs teach **syntax discipline, type awareness, and reading tracebacks**.
Once these feel trivial, you’re ready for **Level 2 (silent logical bugs)**.
