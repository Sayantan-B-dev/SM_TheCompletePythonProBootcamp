**Debugging Difficulty: LEVEL 2 (Silent / Logical Bugs)**
Level 2 bugs are **dangerous** because Python runs *without errors* but produces **wrong results**.
No traceback. No crash. Just incorrect behavior.

These bugs require **reasoning, print-debugging, or stepping through logic**.

Below are **10 Level-2 debugging examples with solutions**, structured the same way.

---

### 1. Off-by-one error in loop

**Buggy code**

```python
total = 0
for i in range(1, 10):
    total += i
print(total)
```

**Expected**

```
55   # sum of 1–10
```

**Actual**

```
45
```

**Fix**

```python
for i in range(1, 11):
    total += i
```

**Why**
`range()` excludes the stop value.

---

### 2. Wrong comparison operator

**Buggy code**

```python
score = 50
if score > 50:
    print("Pass")
else:
    print("Fail")
```

**Expected**

```
Pass
```

**Actual**

```
Fail
```

**Fix**

```python
if score >= 50:
```

**Why**
Boundary condition mistake.

---

### 3. Mutable default argument

**Buggy code**

```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item(1))
print(add_item(2))
```

**Output**

```
[1]
[1, 2]
```

**Fix**

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Why**
Default arguments are evaluated once.

---

### 4. Variable shadowing built-in

**Buggy code**

```python
sum = 0
numbers = [1, 2, 3]
print(sum(numbers))
```

**Actual**

```
TypeError
```

**Fix**

```python
total = 0
print(sum(numbers))
```

**Why**
Built-in function was overwritten.

---

### 5. Condition always true

**Buggy code**

```python
if "a":
    print("Runs")
```

**Output**

```
Runs
```

**Fix**

```python
if "a" in text:
```

**Why**
Non-empty strings are truthy.

---

### 6. List aliasing bug

**Buggy code**

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```

**Output**

```
[[1,0,0],[1,0,0],[1,0,0]]
```

**Fix**

```python
grid = [[0] * 3 for _ in range(3)]
```

**Why**
All rows referenced the same list.

---

### 7. Early return inside loop

**Buggy code**

```python
def find_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
        else:
            return None
```

**Output**

```
None   # even if later element is even
```

**Fix**

```python
def find_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return None
```

**Why**
`return` exits function immediately.

---

### 8. Using `is` instead of `==`

**Buggy code**

```python
x = 1000
if x is 1000:
    print("Equal")
```

**Fix**

```python
if x == 1000:
```

**Why**
`is` checks identity, not value.

---

### 9. Accumulator not reset

**Buggy code**

```python
total = 0
for i in range(3):
    for j in range(3):
        total += j
    print(total)
```

**Output**

```
3
6
9
```

**Fix**

```python
for i in range(3):
    total = 0
    for j in range(3):
        total += j
    print(total)
```

**Why**
State leaked across iterations.

---

### 10. Wrong logical operator

**Buggy code**

```python
age = 25
if age > 18 or age < 60:
    print("Eligible")
```

**Output**

```
Eligible   # always
```

**Fix**

```python
if age > 18 and age < 60:
```

**Why**
Logic condition was always true.

---

### LEVEL 2 PATTERN SUMMARY

| Signal                   | Meaning        |
| ------------------------ | -------------- |
| No error shown           | Logic bug      |
| Output “looks plausible” | Dangerous      |
| Prints help a lot        | State tracking |
| Debugger clarifies       | Control flow   |

Level-2 bugs teach **thinking like the interpreter**, **state awareness**, and **boundary reasoning**.

When these start feeling obvious, you’re ready for **Level 3 (complex, stateful, multi-layer bugs)**.
