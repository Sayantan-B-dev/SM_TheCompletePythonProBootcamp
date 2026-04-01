## 1. Creating Your Own Custom Class (From First Principles)

### 1.1 What a Custom Class Really Is

> A custom class is a **user-defined data type** that bundles:
> • related data
> • related behavior
> into a single, reusable unit

You are not doing anything magical.
You are **defining a new type**, just like `int`, `str`, or `list`.

---

## 2. Absolute Minimal Custom Class (Skeleton)

### Code

```python
class Person:
    pass
```

### Explanation

* `class` → keyword that tells Python you are defining a new type
* `Person` → name of the new type (PascalCase by convention)
* `pass` → placeholder (class exists but does nothing yet)

### Usage

```python
p1 = Person()
print(p1)
```

### Output

```
<__main__.Person object at 0x...>
```

This confirms:

* `Person` is now a valid type
* `p1` is an object of that type

---

## 3. Adding Data Using `__init__` (Constructor)

### Purpose of `__init__`

> `__init__` runs **automatically** when an object is created
> Used to attach data to the object

---

### Code

```python
class Person:
    def __init__(self, name, age):
        # Store values inside the object
        self.name = name
        self.age = age
```

### Usage

```python
p1 = Person("Rahul", 25)
print(p1.name)
print(p1.age)
```

### Output

```
Rahul
25
```

### Mental Model

* `self.name` → variable living **inside** the object
* Each object gets its **own copy**

---

## 4. Adding Behavior (Methods)

### Code

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        # Method uses object’s own data
        print(f"My name is {self.name} and I am {self.age} years old")
```

### Usage

```python
p1 = Person("Rahul", 25)
p1.greet()
```

### Output

```
My name is Rahul and I am 25 years old
```

---

## 5. Internal Object Inspection (Removes Abstraction)

### Code

```python
print(p1.__dict__)
```

### Output

```
{'name': 'Rahul', 'age': 25}
```

This shows:

* A class object is internally just a **dictionary of attributes**
* OOP is structured data, not magic

---

## 6. Creating Multiple Objects (Independence Proof)

### Code

```python
p2 = Person("Anita", 30)

p1.greet()
p2.greet()
```

### Output

```
My name is Rahul and I am 25 years old
My name is Anita and I am 30 years old
```

Each object:

* has the same structure
* has different internal data

---

## 7. Creating Your Own Module (Single File Module)

### 7.1 What a Module Is

> A module is **just a `.py` file** that contains reusable code

Nothing more.

---

### 7.2 Creating a Custom Module

#### File: `person.py`

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"My name is {self.name} and I am {self.age} years old")
```

---

### 7.3 Importing Your Module

#### File: `main.py`

```python
# Import the class from the module
from person import Person

p1 = Person("Rahul", 25)
p1.greet()
```

### Output

```
My name is Rahul and I am 25 years old
```

---

## 8. Module Execution Control (`if __name__ == "__main__"`)

### Why This Exists

> Prevents code from running when a file is imported

---

### Updated `person.py`

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"My name is {self.name} and I am {self.age} years old")


# Runs only if this file is executed directly
if __name__ == "__main__":
    test_person = Person("Test", 99)
    test_person.greet()
```

### Behavior

| How file is used   | What happens           |
| ------------------ | ---------------------- |
| `python person.py` | Test code runs         |
| Imported elsewhere | Test code does NOT run |

---

## 9. Creating a Package (Module Folder)

### Folder Structure

```
my_package/
│
├── __init__.py
├── person.py
└── utils.py
```

---

### `utils.py`

```python
def say_hello():
    print("Hello from utils")
```

---

### Importing from Package

```python
from my_package.person import Person
from my_package.utils import say_hello

p = Person("Rahul", 25)
p.greet()
say_hello()
```

### Output

```
My name is Rahul and I am 25 years old
Hello from utils
```

---

## 10. Realistic Mini-Project Structure (Mental Clarity)

```
project/
│
├── main.py
├── models/
│   └── user.py
├── services/
│   └── email_service.py
└── utils/
    └── validators.py
```

Each folder:

* groups **related responsibility**
* keeps classes small
* prevents cognitive overload

---

## 11. Common Beginner Mistakes (And Fixes)

| Mistake             | Why It Hurts    | Correct Thought        |
| ------------------- | --------------- | ---------------------- |
| Huge classes        | Mental overload | One job per class      |
| Random method names | Confusion       | Verb-based names       |
| Logic everywhere    | Hard to trace   | Centralize behavior    |
| Fear of modules     | Avoids reuse    | Modules = organization |

---

## 12. Fast Learning Rule (Non-Negotiable)

> Write classes **only after** you feel pain in procedural code.

OOP is a **solution**, not a starting point.
