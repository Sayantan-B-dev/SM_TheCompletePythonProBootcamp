# Python Special Attributes, Dunder Methods, and Descriptors — Deep Technical Analysis

Python exposes internal behavior through **special attributes** and **special methods** (commonly called *dunder methods* because they begin and end with double underscores). These enable introspection, operator overloading, object lifecycle control, and attribute management.

This document explains:

* Definition
* Internal mechanism
* Purpose
* Step-by-step execution model
* Practical examples
* Expected outputs

---

# 1. `__name__`

## Definition

`__name__` is a built-in attribute available in every Python module.

## Purpose

Determines how a module is being executed:

* `"__main__"` if run directly
* Module name if imported

## Internal Mechanism

When Python executes a file:

1. Interpreter creates a module object.
2. It assigns the module’s `__name__`.
3. If executed directly → `"__main__"`.
4. If imported → module filename.

## Example

### File: `example.py`

```python
# Print module name
print(__name__)

# Conditional execution block
if __name__ == "__main__":
    print("Running as main program")
```

### Case 1 — Direct Execution

```bash
python example.py
```

Expected Output:

```
__main__
Running as main program
```

### Case 2 — Imported

```python
import example
```

Expected Output:

```
example
```

## Backend Relevance

Used to:

* Prevent test code execution on import
* Define entry point in Flask apps
* Separate module logic from execution logic

---

# 2. `__dict__`

## Definition

Stores object’s writable attributes in dictionary form.

## Purpose

Provides runtime introspection capability.

## Internal Mechanism

Every object maintains a namespace mapping:

```
object.attribute → object.__dict__['attribute']
```

## Example

```python
class User:
    def __init__(self, name):
        self.name = name

user_instance = User("Sayantan")

print(user_instance.__dict__)
```

Expected Output:

```
{'name': 'Sayantan'}
```

## Backend Relevance

* Debugging models
* ORM inspection
* Dynamic serialization

---

# 3. `__doc__`

## Definition

Stores documentation string of objects.

## Example

```python
def greet():
    """Returns greeting message."""
    return "Hello"

print(greet.__doc__)
```

Expected Output:

```
Returns greeting message.
```

---

# 4. `__class__`

## Definition

References the class of an object.

## Example

```python
number = 10
print(number.__class__)
```

Expected Output:

```
<class 'int'>
```

## Internal View

Every object contains pointer to its type object.

---

# 5. `__init__`

## Definition

Constructor method invoked during object creation.

## Internal Steps

1. Memory allocated via `__new__`
2. `__init__` initializes attributes

## Example

```python
class Product:
    def __init__(self, name):
        self.name = name

product_instance = Product("Laptop")
print(product_instance.name)
```

Expected Output:

```
Laptop
```

---

# 6. `__new__`

## Definition

Responsible for object creation before initialization.

## Working Flow

1. `__new__` creates instance
2. `__init__` configures instance

## Example

```python
class CustomObject:
    def __new__(cls):
        print("Creating instance")
        return super().__new__(cls)

    def __init__(self):
        print("Initializing instance")

object_instance = CustomObject()
```

Expected Output:

```
Creating instance
Initializing instance
```

---

# 7. `__str__` and `__repr__`

## Purpose

Control string representation of objects.

| Method     | Used For                       |
| ---------- | ------------------------------ |
| `__str__`  | User-readable representation   |
| `__repr__` | Developer/debug representation |

## Example

```python
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"User: {self.name}"

    def __repr__(self):
        return f"User(name='{self.name}')"

user_instance = User("Sayantan")

print(user_instance)
print(repr(user_instance))
```

Expected Output:

```
User: Sayantan
User(name='Sayantan')
```

---

# 8. Operator Overloading (`__add__`, `__len__`, etc.)

## Definition

Special methods override built-in operators.

## Example — `__add__`

```python
class Vector:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Vector(self.value + other.value)

vector_one = Vector(5)
vector_two = Vector(10)

result_vector = vector_one + vector_two

print(result_vector.value)
```

Expected Output:

```
15
```

---

# 9. Descriptors

## Definition

A descriptor is any object implementing:

* `__get__`
* `__set__`
* `__delete__`

## Purpose

Control attribute access behavior.

## Descriptor Protocol

When attribute accessed:

```
instance.attribute →
    descriptor.__get__(instance, owner_class)
```

---

## Step-by-Step Descriptor Execution

1. Python finds attribute in class.
2. Detects it has `__get__`.
3. Calls descriptor method.
4. Returns controlled value.

---

## Example — Custom Descriptor

```python
class PositiveNumber:
    def __get__(self, instance, owner):
        return instance._value

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value must be positive")
        instance._value = value

class Product:
    price = PositiveNumber()

    def __init__(self, price):
        self.price = price

product_instance = Product(100)
print(product_instance.price)
```

Expected Output:

```
100
```

If:

```python
product_instance.price = -5
```

Expected:

```
ValueError: Value must be positive
```

---

## Backend Relevance of Descriptors

* Used in Django ORM fields
* Used in SQLAlchemy model definitions
* Data validation layers
* Lazy attribute evaluation

---

# 10. `__slots__`

## Purpose

Restricts dynamic attribute creation.

## Example

```python
class User:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name

user_instance = User("Sayantan")
user_instance.age = 25
```

Expected Error:

```
AttributeError
```

Backend relevance:
Reduces memory overhead in high-scale systems.

---

# 11. `__call__`

## Definition

Makes object callable like function.

## Example

```python
class Greeter:
    def __call__(self, name):
        return f"Hello {name}"

greeter_instance = Greeter()
print(greeter_instance("Sayantan"))
```

Expected Output:

```
Hello Sayantan
```

---

# 12. `__enter__` and `__exit__` (Context Managers)

## Purpose

Used in `with` statements.

## Example

```python
class FileManager:
    def __enter__(self):
        print("Opening resource")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing resource")

with FileManager():
    print("Inside block")
```

Expected Output:

```
Opening resource
Inside block
Closing resource
```

Backend relevance:
Database connections, file handling, transaction management.

---

# Summary Table of Core Special Attributes

| Attribute   | Role                 |
| ----------- | -------------------- |
| `__name__`  | Module identity      |
| `__dict__`  | Object namespace     |
| `__init__`  | Initialization       |
| `__new__`   | Object creation      |
| `__str__`   | User string output   |
| `__repr__`  | Debug representation |
| `__call__`  | Callable objects     |
| `__get__`   | Descriptor getter    |
| `__set__`   | Descriptor setter    |
| `__enter__` | Context start        |
| `__exit__`  | Context end          |

---

These mechanisms form the backbone of Python’s object model and are heavily used in advanced backend frameworks, ORMs, middleware systems, and metaprogramming environments.
