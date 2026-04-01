### Functions in Python

---

### What a function is

A function is a reusable block of code designed to perform a specific task. It helps break a program into smaller, manageable, and logically isolated pieces.

---

### Why functions are needed

| Need            | Explanation                                           |
| --------------- | ----------------------------------------------------- |
| Reusability     | Write once, use multiple times without rewriting code |
| Modularity      | Split a large problem into smaller logical units      |
| Readability     | Code becomes easier to understand and maintain        |
| Maintainability | Changes in logic are done in one place                |
| Testing         | Individual functions can be tested independently      |
| Abstraction     | Hide implementation details, expose only behavior     |

---

### Defining a function

```python
def greet():
    print("Hello, Python")
```

Explanation:

* `def` keyword tells Python you are defining a function
* `greet` is the function name
* `()` can later accept parameters
* Indented block is the function body

---

### Calling a function

```python
def greet():
    print("Hello, Python")

greet()
```

Output:

```
Hello, Python
```

Explanation:

* Function code does **not** run when defined
* It runs only when the function is called using `()`

---

### Function with parameters

```python
def greet(name):
    print("Hello", name)

greet("Sayantan")
```

Output:

```
Hello Sayantan
```

Explanation:

* `name` is a parameter (placeholder)
* `"Sayantan"` is an argument (actual value passed)

---

### Function with multiple parameters

```python
def add(a, b):
    print(a + b)

add(10, 20)
```

Output:

```
30
```

---

### Return statement

```python
def add(a, b):
    return a + b

result = add(5, 7)
print(result)
```

Output:

```
12
```

Explanation:

* `return` sends a value back to the caller
* Code after `return` inside the function never executes

---

### Difference between `print` and `return`

| `print()`          | `return`                        |
| ------------------ | ------------------------------- |
| Displays output    | Sends value back                |
| Cannot be reused   | Can be stored, reused, modified |
| Used for debugging | Used for logic                  |

Example:

```python
def square_print(n):
    print(n * n)

def square_return(n):
    return n * n

square_print(4)
x = square_return(4)
print(x)
```

Output:

```
16
16
```

---

### Default parameters

```python
def greet(name="Guest"):
    print("Hello", name)

greet()
greet("Alex")
```

Output:

```
Hello Guest
Hello Alex
```

Explanation:

* Default value is used if no argument is provided

---

### Keyword arguments

```python
def user_info(name, age):
    print(name, age)

user_info(age=22, name="Sam")
```

Output:

```
Sam 22
```

Explanation:

* Order does not matter when using keywords

---

### Positional arguments

```python
def user_info(name, age):
    print(name, age)

user_info("Sam", 22)
```

Output:

```
Sam 22
```

Explanation:

* Values are matched by position

---

### Arbitrary arguments (`*args`)

```python
def total(*numbers):
    print(sum(numbers))

total(1, 2, 3, 4)
```

Output:

```
10
```

Explanation:

* `*args` collects multiple positional arguments as a tuple

---

### Arbitrary keyword arguments (`**kwargs`)

```python
def profile(**data):
    print(data)

profile(name="Sam", age=21, city="Delhi")
```

Output:

```
{'name': 'Sam', 'age': 21, 'city': 'Delhi'}
```

Explanation:

* `**kwargs` collects keyword arguments as a dictionary

---

### Function returning multiple values

```python
def calc(a, b):
    return a+b, a-b, a*b

x, y, z = calc(10, 5)
print(x, y, z)
```

Output:

```
15 5 50
```

Explanation:

* Python returns a tuple internally

---

### Nested functions

```python
def outer():
    def inner():
        print("Inside inner")
    inner()

outer()
```

Output:

```
Inside inner
```

Explanation:

* Inner functions exist only inside outer function

---

### Scope: Local vs Global

```python
x = 10

def test():
    x = 5
    print(x)

test()
print(x)
```

Output:

```
5
10
```

Explanation:

* Local variable does not affect global variable

---

### Global keyword

```python
x = 10

def change():
    global x
    x = 20

change()
print(x)
```

Output:

```
20
```

---

### Lambda (anonymous) functions

```python
square = lambda x: x * x
print(square(6))
```

Output:

```
36
```

Explanation:

* One-line function
* Used for short, simple operations

---

### Docstrings (function documentation)

```python
def add(a, b):
    """Returns the sum of two numbers"""
    return a + b

print(add.__doc__)
```

Output:

```
Returns the sum of two numbers
```

---

### Type hints (function annotations)

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 4))
```

Output:

```
7
```

Explanation:

* Improves readability and tooling support
* Does not enforce types at runtime

---

### Common mistakes

| Mistake                       | Example                      |
| ----------------------------- | ---------------------------- |
| Forgetting parentheses        | `greet` instead of `greet()` |
| Using print instead of return | Logic not reusable           |
| Wrong indentation             | Causes `IndentationError`    |
| Mutable default arguments     | Using lists as defaults      |

Mutable default pitfall:

```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item(1))
print(add_item(2))
```

Output:

```
[1]
[1, 2]
```

Explanation:

* Default list is shared across calls
