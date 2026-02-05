## `*args` and `**kwargs` — Extensive Quiz

**Includes questions, examples, and answers immediately after each section**

---

## Section A — `*args` Basics

### Q1

```python
def demo(*args):
    print(args)

demo(1, 2, 3)
```

**Question**
What is printed?

**Answer**

```
(1, 2, 3)
```

**Explanation**

* `*args` collects all positional arguments into a tuple.

---

### Q2

```python
def add(*nums):
    return sum(nums)

print(add(5))
print(add(5, 10, 15))
```

**Answer**

```
5
30
```

**Explanation**

* `nums` is a tuple of numbers.
* `sum()` works directly on tuples.

---

### Q3

```python
def show(a, *args):
    print(a, args)

show(1)
```

**Answer**

```
1 ()
```

**Explanation**

* `args` can be empty.
* It is still a tuple.

---

### Q4

```python
def test(*args):
    print(len(args))

test()
```

**Answer**

```
0
```

**Explanation**

* No arguments passed → empty tuple.

---

## Section B — `**kwargs` Basics

### Q5

```python
def demo(**kwargs):
    print(kwargs)

demo(a=1, b=2)
```

**Answer**

```
{'a': 1, 'b': 2}
```

**Explanation**

* `**kwargs` collects keyword arguments into a dictionary.

---

### Q6

```python
def show(**kwargs):
    print(kwargs.get("name", "Unknown"))

show(age=25)
```

**Answer**

```
Unknown
```

**Explanation**

* `.get()` safely retrieves missing keys.

---

### Q7

```python
def demo(**kwargs):
    for k, v in kwargs.items():
        print(k, v)

demo(x=10, y=20)
```

**Answer**

```
x 10
y 20
```

---

## Section C — `*args` + Regular Parameters

### Q8

```python
def calc(a, b, *args):
    print(a, b, args)

calc(1, 2, 3, 4)
```

**Answer**

```
1 2 (3, 4)
```

**Explanation**

* First two values bind to `a` and `b`
* Remaining go into `args`

---

### Q9

```python
def f(a, *args):
    return a + sum(args)

print(f(10))
```

**Answer**

```
10
```

**Explanation**

* `args` is empty
* `sum(())` = `0`

---

## Section D — `*args` and `**kwargs` Together

### Q10

```python
def demo(*args, **kwargs):
    print(args)
    print(kwargs)

demo(1, 2, x=10, y=20)
```

**Answer**

```
(1, 2)
{'x': 10, 'y': 20}
```

---

### Q11

```python
def demo(a, *args, **kwargs):
    print(a, args, kwargs)

demo(5, 6, 7, b=10)
```

**Answer**

```
5 (6, 7) {'b': 10}
```

---

## Section E — Argument Order Rules (Very Important)

### Q12

```python
def bad(*args, a):
    pass
```

**Answer**

```
SyntaxError
```

**Explanation**

* Positional parameters cannot appear after `*args`.

---

### Q13

```python
def demo(a, *, b):
    print(a, b)

demo(1, b=2)
```

**Answer**

```
1 2
```

**Explanation**

* `b` is keyword-only.

---

### Q14

```python
def demo(a, *, b):
    print(a, b)

demo(1, 2)
```

**Answer**

```
TypeError
```

**Explanation**

* `b` must be passed as keyword.

---

## Section F — Argument Unpacking

### Q15

```python
def add(a, b, c):
    return a + b + c

values = (1, 2, 3)
print(add(*values))
```

**Answer**

```
6
```

---

### Q16

```python
def show(name, age):
    print(name, age)

data = {"name": "Sam", "age": 30}
show(**data)
```

**Answer**

```
Sam 30
```

---

## Section G — Common Pitfalls

### Q17

```python
def demo(*args):
    args.append(10)
```

**Answer**

```
AttributeError
```

**Explanation**

* `args` is a tuple (immutable).

---

### Q18

```python
def demo(**kwargs):
    print(kwargs["x"])

demo()
```

**Answer**

```
KeyError
```

**Explanation**

* `"x"` does not exist.

---

## Section H — Real-World Patterns

### Q19

```python
def connect(**config):
    host = config.get("host", "localhost")
    port = config.get("port", 5432)
    print(host, port)

connect()
connect(port=3306)
```

**Answer**

```
localhost 5432
localhost 3306
```

---

### Q20

```python
def wrapper(*args, **kwargs):
    return target(*args, **kwargs)
```

**Question**
Why is this pattern important?

**Answer**

* Preserves all positional and keyword arguments
* Used in decorators, middleware, frameworks

---

## Section I — Mixed Difficulty (Think Carefully)

### Q21

```python
def demo(x, *args, y=10):
    print(x, args, y)

demo(1, 2, 3, y=5)
```

**Answer**

```
1 (2, 3) 5
```

---

### Q22

```python
def demo(*args, **kwargs):
    print(len(args), len(kwargs))

demo(1, 2, a=3, b=4, c=5)
```

**Answer**

```
2 3
```

---

## Section J — Conceptual Questions

### Q23

Why should `*args` and `**kwargs` be used carefully in public APIs?

**Answer**

* Too much flexibility hides mistakes
* Misspelled keys are not caught automatically
* Explicit parameters improve readability and safety

---

### Q24

When is `*args` preferable to a list parameter?

**Answer**

* When number of inputs is variable
* When call-site readability matters
  `f(1,2,3)` vs `f([1,2,3])`

---

### Q25

What is the internal type of `*args` and `**kwargs`?

**Answer**

```
*args    → tuple
**kwargs → dict
```

