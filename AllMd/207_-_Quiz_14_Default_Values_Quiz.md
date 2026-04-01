## Default Arguments & Default Values — Quiz Set (Beginner → Advanced)

---

## Section A — Predict the Output (Core Understanding)

### Q1

```python
def greet(name="Guest"):
    print(name)

greet()
greet("Alex")
```

**What is printed?**

---

### Q2

```python
def add(a, b=10):
    return a + b

print(add(5))
print(add(5, 3))
```

**What is the output?**

---

### Q3

```python
def show(x, y=5, z=10):
    print(x, y, z)

show(1)
show(1, z=20)
```

**What is printed?**

---

### Q4

```python
def f(a=1, b=2, c=3):
    print(a, b, c)

f(10, 20)
```

**What is the output?**

---

## Section B — Keyword vs Positional Arguments

### Q5

```python
def calc(a, b=5, c=10):
    return a + b * c

print(calc(2))
print(calc(2, c=3))
```

**Predict the output.**

---

### Q6

```python
def info(name, age=18, city="Delhi"):
    print(name, age, city)

info("Ravi", city="Mumbai")
```

**What is printed?**

---

### Q7

```python
def demo(x, y=2):
    print(x, y)

demo(y=10, x=5)
```

**Valid or error? If valid, output?**

---

## Section C — Mutable Default Arguments (Critical Thinking)

### Q8

```python
def add_item(item, bag=[]):
    bag.append(item)
    return bag

print(add_item("pen"))
print(add_item("pencil"))
```

**What is printed and why?**

---

### Q9

```python
def counter(count=[0]):
    count[0] += 1
    return count[0]

print(counter())
print(counter())
print(counter())
```

**What is the output?**

---

### Q10

```python
def safe_counter(count=None):
    if count is None:
        count = [0]
    count[0] += 1
    return count[0]

print(safe_counter())
print(safe_counter())
```

**What is printed and how is it different from Q9?**

---

## Section D — Error Detection

### Q11

```python
def bad(a=5, b):
    print(a, b)
```

**Will this function definition work? Why or why not?**

---

### Q12

```python
def test(x, y=x):
    return y
```

**Valid or error? Explain.**

---

### Q13

```python
def demo(a, b=2, c=3):
    print(a, b, c)

demo(1, 2, b=5)
```

**Valid or error? Reason.**

---

## Section E — Keyword-Only Defaults (Advanced)

### Q14

```python
def create_user(name, *, active=True):
    print(name, active)

create_user("Sam", True)
```

**Valid or error? Why?**

---

### Q15

```python
def create_user(name, *, active=True):
    print(name, active)

create_user("Sam", active=False)
```

**What is printed?**

---

## Section F — Variadic + Defaults

### Q16

```python
def log(msg, level=1, *tags):
    print(msg, level, tags)

log("Error", 3, "system", "urgent")
```

**What is the output?**

---

### Q17

```python
def report(title, *items, verbose=False):
    print(title, items, verbose)

report("Report", "A", "B", verbose=True)
```

**Predict the output.**

---

## Section G — Design & Best Practice

### Q18

Which is the **correct professional pattern** for a default list argument?

A)

```python
def f(x, data=[]):
    data.append(x)
```

B)

```python
def f(x, data=None):
    if data is None:
        data = []
```

Explain your choice.

---

### Q19

Why is `None` commonly used as a default instead of `[]` or `{}`?

---

### Q20

What problem do **keyword-only default arguments** (`*`) solve in real-world APIs?

---

## Section H — Mixed Difficulty (Think Carefully)

### Q21

```python
def power(base, exp=2):
    return base ** exp

print(power(3))
print(power(exp=3, base=2))
```

**Output?**

---

### Q22

```python
def f(a, b=10, c=20):
    return a + b + c

print(f(5, c=100))
```

**Output?**

---

### Q23

```python
def demo(x, y=[], z=0):
    y.append(x)
    z += 1
    return y, z

print(demo(1))
print(demo(2))
```

**Predict the output and explain both values.**

---

### Q24

```python
def config(debug=False, timeout=30):
    pass
```

**Give two reasons why this signature is better than handling defaults inside the function body.**

---

### Q25 (Challenge)

Rewrite this function using **default arguments properly**:

```python
def save(data, format, indent):
    if format is None:
        format = "json"
    if indent is None:
        indent = 4
```

