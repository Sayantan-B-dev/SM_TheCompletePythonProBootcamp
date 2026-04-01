### ALL KINDS OF SCOPES IN PYTHON (COMPLETE + DEEP)

---

## 1. BUILT-IN SCOPE

**What it is**
Names provided automatically by Python. Always available unless shadowed.

**Examples**
`print`, `len`, `range`, `int`, `str`

### Example 1: Using built-in names

```python
print(len("python"))
```

**Output**

```
6
```

### Example 2: Shadowing a built-in (dangerous)

```python
len = 100
print(len)
```

**Output**

```
100
```

Now `len()` no longer works:

```python
print(len("abc"))
```

**Output**

```
TypeError: 'int' object is not callable
```

---

## 2. GLOBAL SCOPE

**What it is**
Variables defined at the top level of a file/module.

### Example 1: Reading global variable

```python
x = 10

def show():
    print(x)

show()
```

**Output**

```
10
```

### Example 2: Shadowing global variable

```python
x = 10

def show():
    x = 5
    print(x)

show()
print(x)
```

**Output**

```
5
10
```

---

## 3. LOCAL SCOPE

**What it is**
Variables created inside a function. Exists only during function execution.

### Example 1: Local variable

```python
def test():
    y = 20
    print(y)

test()
```

**Output**

```
20
```

Accessing it outside:

```python
print(y)
```

**Output**

```
NameError: name 'y' is not defined
```

---

## 4. GLOBAL vs LOCAL ASSIGNMENT RULE (CRITICAL)

### Example: Common beginner error

```python
count = 0

def increment():
    count += 1

increment()
```

**Output**

```
UnboundLocalError: local variable 'count' referenced before assignment
```

**Why**

* Assignment makes `count` local
* Python tries to read it before assignment

### Correct version using `global`

```python
count = 0

def increment():
    global count
    count += 1

increment()
print(count)
```

**Output**

```
1
```

---

## 5. ENCLOSING (NONLOCAL) SCOPE

**What it is**
Scope of an outer function for nested functions.

### Example 1: Accessing enclosing variable

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

### Example 2: Modifying enclosing variable (without `nonlocal`)

```python
def outer():
    x = 10
    def inner():
        x += 1
    inner()

outer()
```

**Output**

```
UnboundLocalError: local variable 'x' referenced before assignment
```

### Example 3: Correct modification using `nonlocal`

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

## 6. LEGB RULE (NAME RESOLUTION ORDER)

Python searches names in this order:

| Order | Scope     |
| ----- | --------- |
| L     | Local     |
| E     | Enclosing |
| G     | Global    |
| B     | Built-in  |

### Example

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

## 7. SCOPE WITH LOOPS (BLOCK SCOPE MYTH)

### IMPORTANT: Python DOES NOT HAVE BLOCK SCOPE

In many languages (`C`, `Java`, `JS` with `let`), `{}` creates a new scope.
In Python, **indentation does NOT create scope**.

### Example 1: Variable from `if` block

```python
if True:
    a = 10

print(a)
```

**Output**

```
10
```

### Example 2: Variable from `for` loop

```python
for i in range(3):
    pass

print(i)
```

**Output**

```
2
```

---

## 8. WHY PYTHON HAS NO BLOCK SCOPE

Python scopes are **function-based**, not block-based.

Reasoning:

* Simpler mental model
* Cleaner syntax
* Avoid excessive shadowing
* Emphasizes functions as logical units

Only these create new scopes:

* `def`
* `class`
* `lambda`
* `module`

---

## 9. LOOP VARIABLE LEAKING (IMPORTANT BEHAVIOR)

### Example

```python
nums = []
for i in range(3):
    nums.append(lambda: i)

for f in nums:
    print(f())
```

**Output**

```
2
2
2
```

**Why**

* `i` is looked up at call time
* All lambdas reference same `i` in enclosing scope

### Correct approach

```python
nums = []
for i in range(3):
    nums.append(lambda i=i: i)

for f in nums:
    print(f())
```

**Output**

```
0
1
2
```

---

## 10. SCOPE WITH CLASSES

### Example

```python
x = 10

class Test:
    x = 20
    def show(self):
        print(x)
        print(self.x)

t = Test()
t.show()
```

**Output**

```
10
20
```

**Explanation**

* `x` → global
* `self.x` → instance/class namespace

---

## 11. `locals()` AND `globals()` (REAL NAMESPACES)

### Example

```python
x = 10

def demo():
    y = 20
    print(locals())

demo()
print(globals()['x'])
```

**Output**

```
{'y': 20}
10
```

---

## 12. COMPLETE SCOPE COMPARISON TABLE

| Scope     | Created By      | Lifetime          | Modifiable     | Example     |
| --------- | --------------- | ----------------- | -------------- | ----------- |
| Built-in  | Python          | Program           | ❌              | `len`       |
| Global    | Module          | Program           | ✅              | `x = 5`     |
| Enclosing | Outer func      | While outer alive | ✅ (`nonlocal`) | closure     |
| Local     | Function        | Call duration     | ✅              | temp vars   |
| Block     | ❌ Not supported | —                 | —              | `if`, `for` |

---

## 13. KEY TAKEAWAYS (STRICT)

* Python uses **function scope**, not block scope
* Loops and conditionals do **not** create scope
* Assignment defines scope unless overridden
* `global` and `nonlocal` explicitly break isolation
* LEGB explains **every name-resolution bug**
* Nested functions rely on enclosing scope (closures)
* Block-scope expectations cause many beginner mistakes

Every strange variable behavior in Python is explained by these rules—no exceptions.
