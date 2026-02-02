### Indentation in Python (and the tricky parts that actually break code)

---

### What indentation means in Python

Indentation is **syntax**, not style. Python uses indentation to define code blocks instead of `{}` braces.

Other languages:

```
if (x > 0) { do_something(); }
```

Python:

```python
if x > 0:
    do_something()
```

If indentation is wrong, Python **cannot understand program structure**.

---

### Basic indentation rule

| Rule                                    | Meaning          |
| --------------------------------------- | ---------------- |
| Indentation starts a block              | After `:`        |
| Same indentation = same block           | Logical grouping |
| Different indentation = different scope | Block ends       |
| Indentation is mandatory                | No exceptions    |

---

### Correct indentation example

```python
x = 5

if x > 0:
    print("Positive")
    print("Checked successfully")

print("Done")
```

Output:

```
Positive
Checked successfully
Done
```

Explanation:

* Both `print` statements belong to `if`
* Last `print` is outside the block

---

### Wrong indentation (syntax error)

```python
if True:
print("Hello")
```

Error:

```
IndentationError: expected an indented block
```

Explanation:

* Code after `:` must be indented

---

### Unexpected indentation

```python
print("Start")
    print("Wrong")
```

Error:

```
IndentationError: unexpected indent
```

Explanation:

* Indentation used where no block exists

---

### Indentation defines logic (very important)

```python
x = 10

if x > 5:
    print("A")
    print("B")
print("C")
```

Output:

```
A
B
C
```

Now compare:

```python
x = 10

if x > 5:
    print("A")
print("B")
print("C")
```

Output:

```
A
B
C
```

And this:

```python
x = 10

if x > 5:
    print("A")
    if x > 8:
        print("B")
print("C")
```

Output:

```
A
B
C
```

Indentation **changes program meaning**, not just appearance.

---

### Indentation in loops

```python
for i in range(3):
    print(i)
    print("Inside loop")

print("Outside loop")
```

Output:

```
0
Inside loop
1
Inside loop
2
Inside loop
Outside loop
```

If indentation is wrong:

```python
for i in range(3):
    print(i)
print("Inside loop")
```

Output:

```
0
1
2
Inside loop
```

---

### Indentation in functions

```python
def greet():
    print("Hello")
    print("Welcome")

greet()
```

Output:

```
Hello
Welcome
```

Wrong indentation:

```python
def greet():
print("Hello")
```

Error:

```
IndentationError: expected an indented block
```

---

### Nested indentation (blocks inside blocks)

```python
for i in range(2):
    if i == 1:
        print("One")
    else:
        print("Zero")
```

Output:

```
Zero
One
```

Each level adds **one more indentation layer**.

---

### How many spaces? (critical rule)

| Accepted              | Notes                   |
| --------------------- | ----------------------- |
| 4 spaces              | Python standard (PEP 8) |
| Any consistent number | Works but discouraged   |
| Tabs + spaces mixed   | ❌ dangerous             |

---

### Tabs vs spaces (silent killer)

Bad code:

```python
if True:
→→print("Hello")
    print("World")
```

Error:

```
TabError: inconsistent use of tabs and spaces in indentation
```

Explanation:

* Tabs look aligned but are not equal to spaces
* Always use **spaces only**

---

### How to avoid tab issues

| Tool    | Setting                |
| ------- | ---------------------- |
| VS Code | Convert tabs to spaces |
| PyCharm | Smart indentation      |
| Manual  | Press space 4 times    |

---

### Empty blocks are not allowed

❌ Invalid:

```python
if x > 5:
```

✅ Valid:

```python
if x > 5:
    pass
```

Output:
(no output)

Explanation:

* `pass` tells Python “do nothing for now”

---

### Indentation and `else` alignment (very tricky)

```python
for i in range(3):
    if i == 1:
        break
else:
    print("Loop finished")
```

Output:

```
(no output)
```

Explanation:

* `else` belongs to `for`, not `if`
* Runs only if loop finishes without `break`

Now:

```python
for i in range(3):
    if i == 5:
        break
else:
    print("Loop finished")
```

Output:

```
Loop finished
```

Indentation decides **ownership** of `else`.

---

### Indentation mistake that causes logical bugs (no error)

```python
total = 0

for i in range(5):
    total += i
    print(total)
```

Output:

```
0
1
3
6
10
```

But intended:

```python
total = 0

for i in range(5):
    total += i

print(total)
```

Output:

```
10
```

Same code, different indentation → different meaning.

---

### Indentation with `try / except`

```python
try:
    x = int("10")
    print(x)
except ValueError:
    print("Invalid")
```

Output:

```
10
```

Wrong indentation:

```python
try:
    x = int("10")
except ValueError:
print("Invalid")
```

Error:

```
IndentationError
```

---

### Indentation and multiline statements

Correct:

```python
if (10 > 5 and
    20 > 15):
    print("True")
```

Output:

```
True
```

Explanation:

* Line continuation inside parentheses ignores indentation rules

---

### Common indentation mistakes

| Mistake                             | Result                |
| ----------------------------------- | --------------------- |
| Mixing tabs and spaces              | `TabError`            |
| Forgetting indentation after `:`    | `IndentationError`    |
| Over-indenting                      | Unexpected behavior   |
| Under-indenting                     | Logic breaks silently |
| Misaligned `else`, `elif`, `except` | Wrong control flow    |

---

### Mental model (important)

Think of indentation as:

* **Scopes**
* **Ownership**
* **Hierarchy**

If a line is indented under something, it **belongs to it**.

---

### One-line summary

In Python, indentation is not cosmetic.
It defines structure, logic, flow, and correctness.
If indentation is wrong, the program is either broken—or worse—**silently wrong**.
