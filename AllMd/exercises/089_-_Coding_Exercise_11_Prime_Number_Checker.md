### SCOPE-FOCUSED CODING EXERCISES (PYTHON)

Each exercise targets a **specific scope rule**.
All code includes **comments + outputs**.

---

## EXERCISE 1 — LOCAL vs GLOBAL (READ ONLY)

### Task

Understand why reading a global variable works.

```python
x = 10  # global scope

def show():
    # reading global variable is allowed
    print(x)

show()
```

**Output**

```
10
```

**Scope rule**

* No assignment → Python reads from global scope

---

## EXERCISE 2 — LOCAL vs GLOBAL (ASSIGNMENT BUG)

### Task

Find why this crashes.

```python
x = 10

def update():
    x = x + 1  # assignment makes x local

update()
```

**Output**

```
UnboundLocalError: local variable 'x' referenced before assignment
```

**Scope rule**

* Assignment → name becomes local
* Read before assignment → crash

---

## EXERCISE 3 — FIX USING `global`

```python
x = 10

def update():
    global x  # explicitly use global scope
    x = x + 1

update()
print(x)
```

**Output**

```
11
```

---

## EXERCISE 4 — SHADOWING (SAFE BUT CONFUSING)

```python
count = 100

def process():
    count = 5  # local shadow
    print(count)

process()
print(count)
```

**Output**

```
5
100
```

**Scope rule**

* Local shadows global
* No mutation happens to global

---

## EXERCISE 5 — IF BLOCK IS NOT A SCOPE

```python
if True:
    a = 42

print(a)
```

**Output**

```
42
```

**Scope rule**

* Python has **NO block scope**
* `if`, `for`, `while` do not create scopes

---

## EXERCISE 6 — LOOP VARIABLE LEAKING

```python
for i in range(3):
    pass

print(i)
```

**Output**

```
2
```

**Scope rule**

* Loop variable remains in function/global scope

---

## EXERCISE 7 — FUNCTION CREATES A SCOPE

```python
def test():
    x = 10

test()
print(x)
```

**Output**

```
NameError: name 'x' is not defined
```

**Scope rule**

* Function scope is isolated

---

## EXERCISE 8 — ENCLOSING SCOPE (READ)

```python
def outer():
    x = 10
    def inner():
        print(x)
    inner()

outer()
```

**Output**

```
10
```

**Scope rule**

* Inner function can read enclosing scope

---

## EXERCISE 9 — ENCLOSING SCOPE (WRITE BUG)

```python
def outer():
    x = 10
    def inner():
        x = x + 1
    inner()

outer()
```

**Output**

```
UnboundLocalError
```

**Scope rule**

* Assignment makes `x` local to `inner`

---

## EXERCISE 10 — FIX USING `nonlocal`

```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
    inner()
    print(x)

outer()
```

**Output**

```
11
```

---

## EXERCISE 11 — CLOSURE BEHAVIOR

```python
def make_adder(n):
    def add(x):
        return x + n
    return add

add5 = make_adder(5)
print(add5(10))
```

**Output**

```
15
```

**Scope rule**

* `n` lives in enclosing scope (closure)

---

## EXERCISE 12 — LOOP + LAMBDA SCOPE TRAP

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

**Scope rule**

* `i` resolved at call time (not creation time)

---

## EXERCISE 13 — FIX LAMBDA SCOPE

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

## EXERCISE 14 — CLASS SCOPE vs GLOBAL

```python
x = 10

class Demo:
    x = 20
    def show(self):
        print(x)        # global
        print(self.x)   # class / instance

d = Demo()
d.show()
```

**Output**

```
10
20
```

---

## EXERCISE 15 — PRIME CHECK (SCOPE + LOGIC)

### Buggy version (boundary issue)

```python
def is_prime(num):
    for i in range(3, int(num**0.5)):
        if num % i == 0:
            return False
    return True

print(is_prime(9))
```

**Output**

```
True
```

**Why**

* `range` excludes upper bound
* √9 = 3 → loop never runs

---

### Fixed version (scope + correctness)

```python
def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    # i is local to function scope
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
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

## EXERCISE 16 — `locals()` INSPECTION

```python
def demo():
    a = 10
    b = 20
    print(locals())

demo()
```

**Output**

```
{'a': 10, 'b': 20}
```

---

## EXERCISE 17 — `globals()` INSPECTION

```python
x = 99
print(globals()['x'])
```

**Output**

```
99
```

---

## EXERCISE 18 — LEGB RESOLUTION TEST

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()

outer()
```

**Output**

```
local
```

---

## CORE LEARNING CONSOLIDATION (STRICT)

| Concept    | Rule                          |
| ---------- | ----------------------------- |
| Function   | creates scope                 |
| Loop / if  | no scope                      |
| Assignment | defines scope                 |
| Read only  | searches LEGB                 |
| `global`   | breaks isolation upward       |
| `nonlocal` | modifies enclosing scope      |
| Closure    | preserves enclosing variables |
| Lambdas    | late binding by default       |

Every scope bug you will ever face fits into one of these exercises.
