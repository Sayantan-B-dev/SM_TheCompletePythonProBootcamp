### QUIZ SET — PYTHON SCOPE, NAMESPACES, GLOBALS, CONSTRAINTS

(MCQ + CODE PREDICTION + BUG FINDING)

---

## SECTION A — MULTIPLE CHOICE (SCOPE RULES)

### Q1

Which constructs create a **new scope** in Python?

A. `if`
B. `for`
C. `def`
D. `while`

**Answer:** C

---

### Q2

Python resolves variable names in which order?

A. Global → Local → Built-in → Enclosing
B. Local → Enclosing → Global → Built-in
C. Local → Global → Enclosing → Built-in
D. Built-in → Global → Local → Enclosing

**Answer:** B

---

### Q3

What happens when a variable is assigned inside a function?

A. It becomes global
B. It becomes local unless declared otherwise
C. Python checks global first
D. It modifies the enclosing scope

**Answer:** B

---

### Q4

Which keyword allows modifying an enclosing (non-global) variable?

A. `global`
B. `static`
C. `enclosed`
D. `nonlocal`

**Answer:** D

---

### Q5

Which of the following is a **safe professional use** of global scope?

A. User balance
B. Session data
C. Configuration constants
D. Business logic state

**Answer:** C

---

## SECTION B — CODE OUTPUT PREDICTION

### Q6

```python
x = 5

def f():
    print(x)

f()
```

What is the output?

**Answer**

```
5
```

---

### Q7

```python
x = 5

def f():
    x = 10
    print(x)

f()
print(x)
```

**Answer**

```
10
5
```

---

### Q8

```python
def test():
    if True:
        a = 10
    print(a)

test()
```

**Answer**

```
10
```

---

### Q9

```python
for i in range(3):
    pass

print(i)
```

**Answer**

```
2
```

---

### Q10

```python
x = 10

def outer():
    x = 20
    def inner():
        print(x)
    inner()

outer()
```

**Answer**

```
20
```

---

## SECTION C — ERROR IDENTIFICATION

### Q11

```python
x = 10

def update():
    x += 1

update()
```

What error occurs and why?

**Answer**

```
UnboundLocalError
```

Reason: assignment makes `x` local, but it’s read before assignment.

---

### Q12

```python
def outer():
    x = 5
    def inner():
        x += 1
    inner()

outer()
```

Why does this fail?

**Answer**
`x` becomes local to `inner`; needs `nonlocal x`.

---

## SECTION D — FIX THE CODE

### Q13 (Fix using `global`)

```python
count = 0

def inc():
    count += 1
```

**Correct fix**

```python
count = 0

def inc():
    global count
    count += 1
```

---

### Q14 (Professional fix — no global)

```python
count = 0

def inc(count):
    return count + 1

count = inc(count)
count = inc(count)
print(count)
```

**Output**

```
2
```

---

## SECTION E — CLOSURES & LATE BINDING

### Q15

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

Why?

**Answer**
Late binding: `i` resolved at call time.

---

### Q16 (Fix it)

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

for f in funcs:
    print(f())
```

**Output**

```
0
1
2
```

---

## SECTION F — PRIME CHECK (SCOPE + LOGIC)

### Q17

What is wrong here?

```python
def is_prime(n):
    for i in range(2, int(n**0.5)):
        if n % i == 0:
            return False
    return True

print(is_prime(9))
```

**Answer**

* Upper bound excluded
* √9 = 3 never checked

---

### Q18 (Correct version)

```python
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(9))
print(is_prime(29))
```

**Output**

```
False
True
```

---

## SECTION G — REAL-LIFE DESIGN THINKING

### Q19

Which design is **most professional**?

A.

```python
global balance
```

B.

```python
balance = update(balance)
```

C.

```python
globals()["balance"] += 1
```

D.

```python
import balance
```

**Answer:** B

---

### Q20

Choose the correct statement:

A. Globals are bad always
B. Globals are fine if convenient
C. Globals are acceptable if constrained and intentional
D. Globals should store user data

**Answer:** C

---

## FINAL SCORE GUIDE

* **0–7** → Scope basics shaky
* **8–14** → Intermediate understanding
* **15–18** → Strong grasp
* **19–20** → Production-level reasoning

If you can *explain* every answer, you fully understand Python scope.
