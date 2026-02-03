## Using Code Written by Other Developers (Packages & Objects)

---

## 1. The Core Idea

> **You do not write everything yourself. You reuse tested, packaged objects written by others.**

Modern software is built by:

* Importing **packages**
* Using their **classes**
* Creating **objects**
* Calling **methods**

This is the real-world application of OOP.

---

## 2. What a Package Really Is (Conceptually)

A **package** is:

* A collection of modules
* Containing classes, functions, constants
* Designed to solve a specific problem domain

Internally, a package is still:

```text
Classes + Objects + Methods
```

You are simply **consuming** them instead of writing them.

---

## 3. What Is PyPI

### PyPI (Python Package Index)

> **PyPI is the official global repository of third-party Python packages.**

It answers:

* Where do packages live?
* How do developers share reusable code?

---

### How PyPI Fits Into the Bigger Picture

| Component | Role                         |
| --------- | ---------------------------- |
| PyPI      | Hosts packages               |
| pip       | Downloads packages           |
| Package   | Provides classes & functions |
| You       | Create objects and use them  |

---

### Installing a Package

```bash
pip install prettytable
```

What actually happens:

```text
1. pip connects to PyPI
2. Downloads the package
3. Stores it in site-packages
4. Makes it importable
```

---

## 4. How You Use Someone Else’s OOP Code

### The Pattern (Universal)

```text
import package
↓
find a class
↓
create an object
↓
call methods
```

You **do not** care how the class is implemented internally.

---

## 5. Object-Oriented Example: `turtle`

`turtle` is a **graphics package** built entirely around objects.

---

### 5.1 Turtle Is a Class

```python
from turtle import Turtle
```

* `Turtle` is a **class**
* You create **objects** from it

---

### 5.2 Constructing a Turtle Object

```python
from turtle import Turtle, Screen

# Constructing objects
t = Turtle()
screen = Screen()
```

What happened:

```text
Turtle()  → creates a turtle object
Screen()  → creates a screen object
```

---

### 5.3 Accessing Attributes and Methods

```python
t.shape("turtle")
t.color("green")
t.forward(100)
t.left(90)
t.forward(100)

screen.exitonclick()
```

**Expected Output**

```text
A window opens
A green turtle moves forward, turns left, and moves again
```

---

### 5.4 What You Are Really Doing (OOP View)

| Object   | Responsibility    |
| -------- | ----------------- |
| `t`      | Movement, drawing |
| `screen` | Window control    |

You never touch:

* Canvas logic
* Event loops
* Rendering engines

That complexity is **hidden inside the package**.

---

## 6. Object-Oriented Example: `prettytable`

`prettytable` is a **data presentation package** built around one main class.

---

### 6.1 Importing the Class

```python
from prettytable import PrettyTable
```

---

### 6.2 Constructing the Object

```python
table = PrettyTable()
```

This creates an **empty table object**.

---

### 6.3 Setting Attributes (Indirectly)

```python
table.field_names = ["Name", "Age", "Role"]
```

Here:

* `field_names` is an attribute
* You are configuring the object’s state

---

### 6.4 Calling Methods

```python
table.add_row(["Sayantan", 26, "Developer"])
table.add_row(["Alex", 30, "Designer"])

print(table)
```

**Expected Output**

```text
+----------+-----+-----------+
| Name     | Age | Role      |
+----------+-----+-----------+
| Sayantan |  26 | Developer |
| Alex     |  30 | Designer  |
+----------+-----+-----------+
```

---

## 7. What You Are NOT Doing (Important)

You are NOT:

* Managing spacing
* Drawing borders
* Calculating column width

That logic lives inside the **PrettyTable class**.

---

## 8. How This Looks Internally (Mental Model)

```text
PrettyTable
 ├─ field_names (attribute)
 ├─ add_row()   (method)
 ├─ _rows       (internal state)
 └─ __str__()   (string rendering)
```

You only interact with the **public interface**.

---

## 9. Why Packages Are Almost Always OOP-Based

Reasons:

* State must be preserved
* Behavior must act on that state
* Users need simple interfaces
* Internals must remain changeable

OOP enables all of this.

---

## 10. Comparing Your Code vs Package Code

| Aspect         | Your Code         | Package Code |
| -------------- | ----------------- | ------------ |
| Responsibility | Application logic | Domain logic |
| Visibility     | Full              | Hidden       |
| Stability      | Changes often     | Stable       |
| Interface      | You design        | You consume  |

---

## 11. Real-World Professional Workflow

```text
Problem
↓
Search PyPI
↓
Read documentation
↓
Identify main class
↓
Create object
↓
Call methods
↓
Ship feature
```

---

## 12. Key Rule When Using Packages

> Treat package objects as **black boxes with contracts**.

* Respect method names
* Respect input types
* Trust the implementation

---

## 13. Final Concept Lock

```text
Packages = Other people’s classes
Objects  = Your interaction point
Methods  = Allowed operations
Attributes = Configurable state
```

This is how you use other developers’ code through objects and packages in real Python systems.
