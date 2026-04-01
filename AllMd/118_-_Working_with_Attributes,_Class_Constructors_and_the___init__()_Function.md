## 1. Attributes, Methods, `__init__`, Constructor — One Unified Mental Model

> A **class** defines
> • what data an object will carry → **attributes**
> • what actions it can perform → **methods**
> • how it is born → **constructor (`__init__`)**

Everything else is detail.

---

## 2. Attributes — Data That Lives *Inside* the Object

### 2.1 What an Attribute Really Is

> An attribute is just a **variable stored inside an object**

It is **not global**, **not shared** (unless you make it so).

---

### Example

```python
class User:
    def __init__(self, name, age):
        self.name = name      # attribute
        self.age = age        # attribute
```

### Usage

```python
u1 = User("Amit", 24)
u2 = User("Neha", 30)

print(u1.name)
print(u2.name)
```

### Output

```
Amit
Neha
```

### Key Insight

* `self.name` and `self.age` are stored **inside each object**
* Same attribute names, **different memory**

---

## 3. `__init__` — Constructor (Birth Logic of the Object)

### 3.1 What the Constructor Does

> `__init__` runs **automatically** when an object is created
> It sets the object’s **initial state**

---

### Object Creation Timeline

```text
User("Amit", 24)
│
├─ allocate memory
├─ create empty object
└─ call __init__(self, "Amit", 24)
```

You **never call `__init__` manually**.

---

### Example

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

```python
u = User("Amit", 24)
```

This line:

* creates object
* passes object as `self`
* assigns attributes

---

## 4. `self` — The Most Misunderstood Concept (Demystified)

### 4.1 What `self` Is

> `self` is the **current object itself**

Nothing more.

---

### Method Call Reality (What Python Actually Does)

```python
u.show()
```

Internally becomes:

```python
User.show(u)
```

So `self` receives `u`.

---

### Why `self` Is Required

Without `self`, Python wouldn’t know:

* *which object’s data* to read
* *which object’s data* to modify

---

### Proof Using `id()`

```python
class Test:
    def show(self):
        print(id(self))

t = Test()
print(id(t))
t.show()
```

### Output

```
140351...
140351...
```

Same object. Same identity.

---

## 5. Methods — Functions Bound to Objects

### 5.1 What a Method Really Is

> A method is a function that:
> • belongs to a class
> • operates on the object’s own data

---

### Example

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
```

### Usage

```python
acc = BankAccount("Ravi", 1000)
acc.deposit(500)
print(acc.balance)
```

### Output

```
1500
```

### Important Observation

* `deposit()` **mutates internal state**
* No global variables involved
* Object manages itself

---

## 6. Default Values During Initialization

### 6.1 Why Defaults Exist

> Defaults prevent forcing the user to pass everything every time

They make object creation **flexible**.

---

### Example: Default Attribute Values

```python
class User:
    def __init__(self, name, age=18, active=True):
        self.name = name
        self.age = age
        self.active = active
```

### Usage

```python
u1 = User("Amit")
u2 = User("Neha", 30, False)

print(u1.__dict__)
print(u2.__dict__)
```

### Output

```
{'name': 'Amit', 'age': 18, 'active': True}
{'name': 'Neha', 'age': 30, 'active': False}
```

---

### Rule About Defaults

| Rule                       | Reason                          |
| -------------------------- | ------------------------------- |
| Defaults go last           | Python positional argument rule |
| Mutable defaults forbidden | Shared state bugs               |

---

## 7. Dangerous Default Values (Critical Concept)

### ❌ Wrong (Shared State Bug)

```python
class Cart:
    def __init__(self, items=[]):
        self.items = items
```

### Why This Is Broken

* `items` list is created **once**
* Shared by all objects

---

### Correct Way

```python
class Cart:
    def __init__(self, items=None):
        if items is None:
            self.items = []
        else:
            self.items = items
```

---

## 8. Attribute Creation Is Dynamic (Power Feature)

### You Can Add Attributes Anytime

```python
class User:
    def __init__(self, name):
        self.name = name

u = User("Amit")
u.city = "Kolkata"

print(u.__dict__)
```

### Output

```
{'name': 'Amit', 'city': 'Kolkata'}
```

### Insight

* Python does **not lock attribute definitions**
* Discipline comes from convention, not enforcement

---

## 9. Class Attributes vs Instance Attributes

### Example

```python
class User:
    species = "Human"     # class attribute

    def __init__(self, name):
        self.name = name  # instance attribute
```

```python
u1 = User("Amit")
u2 = User("Neha")

print(u1.species)
print(u2.species)
```

### Output

```
Human
Human
```

---

### Override Behavior

```python
u1.species = "Alien"
print(u1.species)
print(u2.species)
```

### Output

```
Alien
Human
```

### Rule

| Attribute Type     | Ownership      |
| ------------------ | -------------- |
| Instance attribute | Object         |
| Class attribute    | Class (shared) |

---

## 10. Method Using Defaults + Attributes Together

```python
class Timer:
    def __init__(self, seconds=0):
        self.seconds = seconds

    def tick(self, step=1):
        self.seconds += step

    def show(self):
        print(self.seconds)
```

### Usage

```python
t = Timer()
t.tick()
t.tick(5)
t.show()
```

### Output

```
6
```

---

## 11. Reading Objects as Sentences (Mental Hack)

```python
account.deposit(500)
```

Read as:

> “This account deposits 500”

```python
user.is_active()
```

> “This user checks if active”

If a method name doesn’t read naturally → redesign it.

---

## 12. Absolute Rules to Avoid OOP Overwhelm

| Rule                         | Effect                 |
| ---------------------------- | ---------------------- |
| Always use `self.attribute`  | Avoids confusion       |
| Small `__init__`             | Cleaner objects        |
| One responsibility per class | Less mental load       |
| Inspect `__dict__` often     | Removes abstraction    |
| Defaults for safety          | Easier object creation |

---

## 13. Final Mental Compression

> • `__init__` = object birth
> • `self` = the object
> • attributes = stored data
> • methods = object behavior
> • defaults = flexibility

Once these click, **everything else in OOP becomes optional detail**.
