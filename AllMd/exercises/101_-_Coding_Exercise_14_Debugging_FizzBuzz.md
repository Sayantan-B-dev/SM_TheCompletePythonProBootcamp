**Debugging Difficulty: LEVEL 3 (Complex / Stateful / Multi-Layer Bugs)**
Level-3 bugs are **hard not because Python is wrong**, but because **your mental model breaks down**.
They involve **state over time, interactions between parts, environment, mutation, concurrency, or hidden assumptions**.

These bugs:

* Often appear *far away* from the cause
* May disappear when you add `print()`
* May work “sometimes”
* Require debugger, reduction, and deep reasoning

Below are **10 Level-3 debugging examples with explanations and fixes**.

---

### 1. Mutable default argument + conditional mutation (compound bug)

**Buggy code**

```python
def log(msg, logs=[]):
    if msg not in logs:
        logs.append(msg)
    return logs

print(log("A"))
print(log("A"))
print(log("B"))
```

**Output**

```
['A']
['A']
['A', 'B']
```

**Why this is Level 3**
The bug is invisible unless you understand:

* default argument lifetime
* conditional mutation
* cross-call shared state

**Fix**

```python
def log(msg, logs=None):
    if logs is None:
        logs = []
    if msg not in logs:
        logs.append(msg)
    return logs
```

---

### 2. State leak via global variable

**Buggy code**

```python
count = 0

def increment():
    global count
    count += 1
    return count

def process():
    for _ in range(3):
        increment()

process()
process()
print(count)
```

**Output**

```
6
```

**Expected**

```
3
```

**Why Level 3**
The bug isn’t in `process()`.
It’s in **shared global state surviving across calls**.

**Fix**

```python
def process():
    count = 0
    for _ in range(3):
        count += 1
    return count
```

---

### 3. Bug disappears when using `print()` (Heisenbug)

**Buggy code**

```python
import time

ready = False

def worker():
    global ready
    time.sleep(0.1)
    ready = True

def main():
    while not ready:
        pass
    print("Done")

worker()
main()
```

**Symptom**

* Infinite loop
* Sometimes works if you add `print(ready)`

**Why Level 3**
Timing + state + CPU scheduling.

**Fix**

```python
import threading

ready = False

def worker():
    global ready
    ready = True

threading.Thread(target=worker).start()
while not ready:
    time.sleep(0.01)
print("Done")
```

---

### 4. Object aliasing across functions

**Buggy code**

```python
def add_user(users):
    users.append("admin")

data = []
add_user(data)
add_user(data)
print(data)
```

**Output**

```
['admin', 'admin']
```

**Why Level 3**
Mutation happens **outside the function’s visible output**.

**Fix**

```python
def add_user(users):
    return users + ["admin"]

data = []
data = add_user(data)
```

---

### 5. Late binding in closures (classic trap)

**Buggy code**

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

for f in funcs:
    print(f())
```

**Output**

```
2
2
2
```

**Why Level 3**
Closures capture **reference**, not value.

**Fix**

```python
for i in range(3):
    funcs.append(lambda i=i: i)
```

---

### 6. Silent data corruption via shallow copy

**Buggy code**

```python
original = [[1, 2], [3, 4]]
copy = original[:]
copy[0].append(99)

print(original)
```

**Output**

```
[[1, 2, 99], [3, 4]]
```

**Why Level 3**
Top-level copy only; nested objects shared.

**Fix**

```python
import copy
copy = copy.deepcopy(original)
```

---

### 7. Wrong exception caught → hidden bug

**Buggy code**

```python
try:
    value = int(data["age"])
except KeyError:
    value = 0
```

**Bug**

* `ValueError` not handled
* Crash occurs elsewhere later

**Fix**

```python
try:
    value = int(data["age"])
except (KeyError, ValueError):
    value = 0
```

**Why Level 3**
Exception mismatch creates delayed failure.

---

### 8. Incorrect async usage (function never runs)

**Buggy code**

```python
async def fetch():
    return 42

result = fetch()
print(result)
```

**Output**

```
<coroutine object fetch>
```

**Why Level 3**
The function *looks* executed but never was.

**Fix**

```python
import asyncio
result = asyncio.run(fetch())
```

---

### 9. Loop logic depends on mutated list

**Buggy code**

```python
items = [1, 2, 3, 4]

for item in items:
    if item % 2 == 0:
        items.remove(item)

print(items)
```

**Output**

```
[1, 3, 4]
```

**Why Level 3**
You’re modifying the iterable while iterating.

**Fix**

```python
items = [i for i in items if i % 2 != 0]
```

---

### 10. Environment-dependent bug (works on one machine)

**Buggy code**

```python
open("Data.txt")
```

**Works on**

* Windows

**Fails on**

* Linux

**Why Level 3**
Case-sensitive filesystem.

**Fix**

```python
open("data.txt")
```

---

## LEVEL 3 PATTERN SUMMARY

| Signal                  | Meaning                |
| ----------------------- | ---------------------- |
| Bug moves when observed | Timing / state issue   |
| Appears far from cause  | State leakage          |
| Works sometimes         | Mutation / concurrency |
| No single “bad line”    | Mental model failure   |
| Needs debugger          | Yes                    |

---

### Key Mental Shift at Level 3

You stop asking:
❌ “Where is the wrong line?”

You start asking:
✅ “How does state evolve over time?”

Level-3 debugging is where developers stop being syntax writers and become **systems thinkers**.
