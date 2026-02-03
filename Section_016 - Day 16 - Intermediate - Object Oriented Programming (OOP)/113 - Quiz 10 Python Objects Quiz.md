## QUIZ — OBJECT-ORIENTED PROGRAMMING & PYTHON PACKAGES

*(Based strictly on what you learned so far)*

---

## SECTION 1 — Core OOP Concepts (MCQs)

### Q1

Which statement best describes a **class**?

A. A function that runs repeatedly
B. A blueprint that defines data and behavior
C. A variable holding multiple values
D. A memory location

**Answer:** B

---

### Q2

An **object** is:

A. A copy of a function
B. A reference to a module
C. A runtime instance of a class
D. A static data structure

**Answer:** C

---

### Q3

Why does `__init__` exist?

A. To destroy objects
B. To declare global variables
C. To initialize object state
D. To import packages

**Answer:** C

---

### Q4

What does `self` represent inside a class method?

A. The class itself
B. A global variable
C. The current object instance
D. The parent class

**Answer:** C

---

### Q5

Which of the following best explains **encapsulation**?

A. Writing shorter code
B. Hiding data and controlling access through methods
C. Using inheritance
D. Avoiding classes

**Answer:** B

---

## SECTION 2 — Classes, Objects & Methods (MCQs)

### Q6

Given:

```python
user = User("sayantan")
```

What is `user`?

A. A class
B. A function
C. An object
D. A module

**Answer:** C

---

### Q7

Which syntax correctly calls a method?

A. `User.greet`
B. `user.greet`
C. `user.greet()`
D. `User.greet()`

**Answer:** C

---

### Q8

Which statement is TRUE?

A. Methods belong to objects only
B. Attributes belong to classes only
C. Objects hold state
D. Classes change at runtime

**Answer:** C

---

### Q9

What happens internally when calling:

```python
user.greet()
```

A. `greet()` runs without arguments
B. `greet(user)` is called automatically
C. `self` is ignored
D. The class is reloaded

**Answer:** B

---

### Q10

Why should data and behavior live in the same class?

A. To reduce typing
B. To improve execution speed
C. To enforce ownership and responsibility
D. To avoid imports

**Answer:** C

---

## SECTION 3 — Procedural vs OOP (MCQs)

### Q11

Main problem with large procedural programs:

A. Slow execution
B. Syntax limitations
C. Shared mutable global state
D. Too many files

**Answer:** C

---

### Q12

OOP primarily helps with:

A. Writing fewer lines
B. Managing complexity
C. Faster loops
D. Memory allocation

**Answer:** B

---

### Q13

Which design is better?

A. One function controlling everything
B. One object owning all data
C. Multiple objects with single responsibilities
D. Global dictionaries

**Answer:** C

---

## SECTION 4 — Packages & PyPI (MCQs)

### Q14

What is **PyPI**?

A. A Python compiler
B. A package installer
C. A global repository of Python packages
D. A testing framework

**Answer:** C

---

### Q15

What does `pip install prettytable` do?

A. Compiles Python
B. Downloads a package from PyPI
C. Runs a script
D. Creates a virtual environment

**Answer:** B

---

### Q16

When using a package, what do you mostly interact with?

A. Internal source code
B. Global variables
C. Public classes and methods
D. File system

**Answer:** C

---

### Q17

Why are most packages object-oriented?

A. Python forces it
B. State and behavior must stay together
C. It runs faster
D. It avoids imports

**Answer:** B

---

## SECTION 5 — Package-Based Objects (MCQs)

### Q18

In `turtle`, what is `Turtle()`?

A. A function
B. A module
C. A class constructor
D. A constant

**Answer:** C

---

### Q19

What does this create?

```python
t = Turtle()
```

A. A blueprint
B. A module
C. A turtle object
D. A screen

**Answer:** C

---

### Q20

In `PrettyTable`, what does `add_row()` represent?

A. An attribute
B. A method operating on internal state
C. A global function
D. A constructor

**Answer:** B

---

## SECTION 6 — Coffee Machine OOP Design (MCQs)

### Q21

Which class defines a drink’s **ingredients and cost**?

A. Menu
B. CoffeeMaker
C. MenuItem
D. MoneyMachine

**Answer:** C

---

### Q22

Which class owns machine resources?

A. Menu
B. CoffeeMaker
C. MenuItem
D. main.py

**Answer:** B

---

### Q23

Which object decides if payment is sufficient?

A. CoffeeMaker
B. Menu
C. MoneyMachine
D. MenuItem

**Answer:** C

---

### Q24

Why does `main.py` not manage resources directly?

A. Performance reasons
B. Security reasons
C. Separation of concerns
D. Python limitation

**Answer:** C

---

### Q25

Best statement about the final design:

A. Objects share global state
B. Each object owns its data
C. Functions control everything
D. Logic is duplicated

**Answer:** B

---

## SECTION 7 — Short Answer (Think Carefully)

### Q26

Why is returning a `MenuItem` object better than returning a dictionary?

**Expected Answer:**
Because behavior and data stay together, enabling validation, reuse, and cleaner collaboration between objects.

---

### Q27

What breaks if multiple classes directly modify the same global resource dictionary?

**Expected Answer:**
Unpredictable state changes, hidden dependencies, and fragile code.

---

### Q28

Why is `MoneyMachine` easily replaceable?

**Expected Answer:**
Because payment logic is isolated behind a clear interface.

---

### Q29

What is the biggest mental shift from procedural to OOP?

**Expected Answer:**
Thinking in terms of responsibilities and ownership instead of steps and functions.

---

### Q30

Complete this sentence correctly:

> “OOP is not about classes, it is about __________.”

**Expected Answer:**
Ownership, responsibility, and boundaries.

---

**END OF QUIZ**
