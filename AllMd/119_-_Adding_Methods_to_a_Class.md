## 1. What a Method Really Is (Beyond the Definition)

> A **method** is a function that is **bound to an object or a class**, and therefore has **context**.

That context is what separates:

* a normal function
* from a method

The context is carried through **`self`** (or `cls`).

---

## 2. Method vs Function (Behavioral Difference)

### Plain Function

```python
def add(a, b):
    return a + b
```

* No memory
* No ownership
* No persistent state

---

### Method

```python
class Calculator:
    def __init__(self):
        self.total = 0

    def add(self, value):
        self.total += value
```

* Remembers past operations
* Operates on internal state
* Belongs to an object

---

### Usage

```python
c = Calculator()
c.add(10)
c.add(5)
print(c.total)
```

### Output

```
15
```

The **method modifies the object itself**, not just returns a value.

---

## 3. The Binding Mechanism (Critical Understanding)

### What Actually Happens

```python
c.add(10)
```

Internally becomes:

```python
Calculator.add(c, 10)
```

So:

| Element          | Meaning                        |
| ---------------- | ------------------------------ |
| `Calculator.add` | Function defined in class      |
| `c`              | Passed automatically as `self` |
| `10`             | Normal argument                |

This is called **method binding**.

---

## 4. `self` Is the Glue Between Methods and Attributes

### Without `self`, methods are blind

```python
class User:
    def set_name(self, name):
        self.name = name
```

Here:

* `self.name` stores data **inside that object**
* All methods referencing `self.name` access the same storage

---

### Proof via Object Memory

```python
u = User()
u.set_name("Amit")
print(u.__dict__)
```

### Output

```
{'name': 'Amit'}
```

Every method operates on the same internal dictionary.

---

## 5. Method Categories (Very Important Distinction)

### 5.1 Instance Methods (Most Common)

```python
class Account:
    def deposit(self, amount):
        self.balance += amount
```

* First parameter: `self`
* Can read/write instance attributes
* Requires an object

---

### 5.2 Class Methods

Used when logic belongs to the **class itself**, not a specific object.

```python
class User:
    count = 0

    def __init__(self):
        User.count += 1

    @classmethod
    def total_users(cls):
        return cls.count
```

### Usage

```python
u1 = User()
u2 = User()
print(User.total_users())
```

### Output

```
2
```

| Aspect      | Instance Method | Class Method   |
| ----------- | --------------- | -------------- |
| First param | `self`          | `cls`          |
| Access      | object data     | class data     |
| Decorator   | none            | `@classmethod` |

---

### 5.3 Static Methods

Used when logic is **related** to the class but needs **no data**.

```python
class MathUtils:
    @staticmethod
    def square(x):
        return x * x
```

### Usage

```python
print(MathUtils.square(5))
```

### Output

```
25
```

| Feature         | Static Method |
| --------------- | ------------- |
| `self`          | No            |
| `cls`           | No            |
| Access to state | None          |

---

## 6. Relationship Between `__init__` and Methods

### `__init__` Is Just a Method (Special One)

```python
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(self.name)
```

Key differences:

| `__init__`  | Normal Method       |
| ----------- | ------------------- |
| Auto-called | Manually called     |
| Sets state  | Uses/modifies state |
| Runs once   | Runs many times     |

---

## 7. Methods That Return vs Methods That Mutate

### Mutating Method (Changes Object)

```python
def deposit(self, amount):
    self.balance += amount
```

### Returning Method (Reads Object)

```python
def get_balance(self):
    return self.balance
```

### Why This Matters

* Mutating methods → side effects
* Returning methods → safer, predictable

Good design **separates these roles clearly**.

---

## 8. Methods as State Machines

Objects often behave like **state machines**.

```python
class Door:
    def __init__(self):
        self.is_open = False

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False
```

### Usage

```python
d = Door()
d.open()
print(d.is_open)
```

### Output

```
True
```

Methods:

* change state
* enforce valid transitions

---

## 9. Guarded Methods (Defensive Programming)

```python
class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

Methods are **gatekeepers**, not just actions.

---

## 10. Method Chaining (Advanced Behavior)

```python
class Builder:
    def step1(self):
        print("step1")
        return self

    def step2(self):
        print("step2")
        return self
```

### Usage

```python
b = Builder()
b.step1().step2()
```

### Output

```
step1
step2
```

Why it works:

* Method returns `self`
* Allows fluent APIs

---

## 11. Private Methods (Convention-Based)

```python
class Engine:
    def _ignite(self):
        print("ignition")

    def start(self):
        self._ignite()
```

* `_method` → internal use
* Not enforced, but respected by convention

---

## 12. Method Overriding (Behavior Replacement)

```python
class Animal:
    def speak(self):
        print("sound")

class Dog(Animal):
    def speak(self):
        print("bark")
```

### Usage

```python
a = Dog()
a.speak()
```

### Output

```
bark
```

The method resolution is **dynamic**, based on object type.

---

## 13. Method Resolution Order (Conceptual Only)

When calling a method:

1. Object’s class
2. Parent classes
3. Object base (`object`)

This explains why overrides work.

---

## 14. Common Method Design Mistakes

| Mistake                    | Consequence            |
| -------------------------- | ---------------------- |
| Too many responsibilities  | Cognitive overload     |
| Mutating + returning mixed | Unpredictable behavior |
| Accessing globals          | Hard to debug          |
| Long methods               | Hidden bugs            |

---

## 15. How to Think About Methods (Mental Model)

Read this:

```python
user.login()
```

As:

> “This user logs in”

If the sentence:

* sounds natural
* clearly affects *this object*

The method is well designed.

---

## 16. Final Compression (Deep Truth)

> • Methods are **verbs**
> • `self` is **the noun**
> • `__init__` establishes identity
> • Methods evolve that identity over time
> • Good OOP = predictable state changes

Once this clicks, **methods stop being syntax and start being behavior**.
