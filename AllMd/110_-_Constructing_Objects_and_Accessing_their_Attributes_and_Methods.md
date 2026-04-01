## Constructing Objects

---

### 1. What “Constructing an Object” Means

> **Object construction** is the process of creating a real, usable instance from a class blueprint.

Key points:

* A **class** defines structure and behavior
* An **object** is created at runtime
* Construction initializes the object’s **state**

---

### 2. Constructor Method (`__init__`)

```python
class User:
    """
    Represents a system user.
    Responsible for storing and managing user data.
    """

    def __init__(self, username, email):
        # __init__ runs automatically during object creation
        # It initializes the object's internal state
        self.username = username
        self.email = email
```

Why `__init__` exists:

* Guarantees objects start in a **valid state**
* Prevents half-initialized objects
* Centralizes setup logic

---

### 3. Creating (Instantiating) an Object

```python
user1 = User("sayantan", "sayantan@example.com")
```

What happens internally (step-by-step):

```text
1. Memory is allocated for the object
2. __init__ is called automatically
3. self points to the new object
4. Attributes are attached to the object
5. Reference returned to user1
```

---

## Accessing Attributes

---

### 4. Instance Attributes

Attributes belong to **objects**, not the class.

```python
print(user1.username)
print(user1.email)
```

**Expected Output**

```text
sayantan
sayantan@example.com
```

Important:

* `user1.username` reads data from the object
* Each object has its **own copy** of attributes

---

### 5. Modifying Attributes

```python
user1.email = "newmail@example.com"
print(user1.email)
```

**Expected Output**

```text
newmail@example.com
```

This works because:

* Attributes are stored in the object’s namespace
* Python allows controlled mutation by default

---

### 6. Attribute Ownership Model

```text
Class → defines what attributes exist
Object → owns the actual values
```

Two objects, same class:

```python
user2 = User("alex", "alex@example.com")

print(user1.username)
print(user2.username)
```

**Expected Output**

```text
sayantan
alex
```

---

## Accessing Methods

---

### 7. Defining Methods

```python
class User:
    def __init__(self, username):
        self.username = username

    def greet(self):
        # self gives access to the object's own data
        return f"Hello, {self.username}"
```

---

### 8. Calling a Method

```python
user = User("sayantan")
message = user.greet()
print(message)
```

**Expected Output**

```text
Hello, sayantan
```

What actually happens:

```text
user.greet()
↓
User.greet(user)
```

* `self` is passed automatically
* Method operates on that specific object

---

## Attribute vs Method Access (Clear Distinction)

| Aspect      | Attribute     | Method            |
| ----------- | ------------- | ----------------- |
| Purpose     | Store data    | Perform action    |
| Syntax      | `object.attr` | `object.method()` |
| Parentheses | No            | Yes               |
| Uses `self` | Indirectly    | Explicitly        |

---

## Class Attributes vs Instance Attributes

---

### 9. Class Attributes (Shared)

```python
class Car:
    wheels = 4  # Class attribute

    def __init__(self, brand):
        self.brand = brand
```

```python
car1 = Car("Toyota")
car2 = Car("Honda")

print(car1.wheels)
print(car2.wheels)
```

**Expected Output**

```text
4
4
```

---

### 10. Instance Attribute Overrides

```python
car1.wheels = 6

print(car1.wheels)
print(car2.wheels)
```

**Expected Output**

```text
6
4
```

Explanation:

* `car1.wheels` shadows the class attribute
* `car2` still reads from the class

---

## Controlled Access (Encapsulation Convention)

---

### 11. “Private” Attributes (Convention-Based)

```python
class Account:
    def __init__(self, balance):
        self._balance = balance  # internal-use signal

    def get_balance(self):
        return self._balance
```

```python
account = Account(5000)
print(account.get_balance())
```

**Expected Output**

```text
5000
```

Why this matters:

* Prevents uncontrolled mutation
* Centralizes business rules

---

## Object Lifecycle Summary

```text
Class defined
↓
Object constructed (__init__)
↓
Attributes initialized
↓
Methods called using dot operator
↓
Object collaborates with others
```

---

## Core Rules to Remember

```text
• Objects are created using ClassName(...)
• Attributes are accessed with dot notation
• Methods are functions bound to objects
• self always refers to the current object
• Each object owns its own state
```

This is how objects are constructed and how their attributes and methods are accessed in practice.
