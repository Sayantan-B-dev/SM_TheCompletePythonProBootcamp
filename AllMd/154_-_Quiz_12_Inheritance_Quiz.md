## INHERITANCE — QUIZ SET (WITH ANSWERS)

---

## SECTION 1 — CONCEPTUAL MCQs (FOUNDATION)

### Q1

What best describes inheritance in OOP?

A. Sharing memory between objects
B. Copying code from one class to another
C. Allowing a class to acquire properties of another class
D. Restricting access to class members

**Answer:** C

**Explanation:**
Inheritance models an **“is-a” relationship** where a child class reuses and extends a parent class.

---

### Q2

Which keyword is used to inherit a class in Python?

A. `extends`
B. `inherits`
C. `:`
D. Class name in parentheses

**Answer:** D

**Explanation:**
Python uses `class Child(Parent):` syntax.

---

### Q3

What happens if a child class does NOT define `__init__()`?

A. Error occurs
B. Parent `__init__()` runs automatically
C. Object cannot be created
D. Parent attributes are inaccessible

**Answer:** B

---

### Q4

What relationship does inheritance represent?

A. has-a
B. owns-a
C. is-a
D. uses-a

**Answer:** C

---

### Q5

Which is NOT a benefit of inheritance?

A. Code reuse
B. Logical hierarchy
C. Faster execution
D. Easier maintenance

**Answer:** C

---

## SECTION 2 — CODE BEHAVIOR QUIZ

### Q6

```python
class Animal:
    def eat(self):
        print("Eating")

class Dog(Animal):
    pass

d = Dog()
d.eat()
```

What is the output?

**Answer:**

```
Eating
```

**Explanation:**
`Dog` inherits `eat()` from `Animal`.

---

### Q7

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

obj = B()
obj.show()
```

Output?

**Answer:**

```
B
```

**Explanation:**
Child method **overrides** parent method.

---

### Q8

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        super().show()
        print("B")

obj = B()
obj.show()
```

Output?

**Answer:**

```
A
B
```

**Explanation:**
`super()` explicitly calls the parent version.

---

### Q9

```python
class Parent:
    def __init__(self):
        print("Parent init")

class Child(Parent):
    def __init__(self):
        print("Child init")

c = Child()
```

Output?

**Answer:**

```
Child init
```

**Explanation:**
Parent `__init__()` is skipped because `super()` is not used.

---

### Q10

Fix the above code to call both constructors.

**Answer:**

```python
class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child init")
```

---

## SECTION 3 — `super()` QUIZ

### Q11

What does `super()` refer to?

A. The current class
B. The child class
C. The next class in MRO
D. The base object

**Answer:** C

---

### Q12

Why is `super()` preferred over direct parent calls?

A. Faster execution
B. Avoids hardcoding class names
C. Required syntax
D. Makes code shorter

**Answer:** B

---

### Q13

In multiple inheritance, `super()` follows:

A. Random order
B. Parent order
C. Depth-first search
D. Method Resolution Order (MRO)

**Answer:** D

---

### Q14

What does this print?

```python
class A:
    def show(self):
        print("A")

class B(A):
    pass

print(B.__mro__)
```

**Answer:**

```
(<class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

---

## SECTION 4 — TYPES OF INHERITANCE

### Q15

Which inheritance type allows one child to have multiple parents?

A. Single
B. Multilevel
C. Hierarchical
D. Multiple

**Answer:** D

---

### Q16

Which diagram represents hierarchical inheritance?

A.

```
A → B → C
```

B.

```
A → B
A → C
```

C.

```
A ← B → C
```

D.

```
A → B ← C
```

**Answer:** B

---

### Q17

What inheritance type is this?

```
Animal → Mammal → Human
```

**Answer:** Multilevel inheritance

---

## SECTION 5 — MULTIPLE INHERITANCE & MRO

### Q18

```python
class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    pass

obj = C()
obj.show()
```

Output?

**Answer:**

```
A
```

**Explanation:**
Python searches left-to-right in MRO.

---

### Q19

Change inheritance order to call `B.show()`.

**Answer:**

```python
class C(B, A):
    pass
```

---

### Q20

What problem does MRO solve?

A. Speed
B. Memory leaks
C. Diamond problem
D. Syntax ambiguity

**Answer:** C

---

## SECTION 6 — TRUE / FALSE

### Q21

Inheritance always improves design.
**Answer:** False

---

### Q22

Python supports multiple inheritance.
**Answer:** True

---

### Q23

Overriding requires the same method name.
**Answer:** True

---

### Q24

Private variables (`__var`) are fully inaccessible in child classes.
**Answer:** False

**Explanation:**
They are **name-mangled**, not truly private.

---

## SECTION 7 — FIND THE ERROR

### Q25

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self):
        pass

d = Dog("Tommy")
```

What is wrong?

**Answer:**
`Dog.__init__()` does not accept `name` or call `super().__init__(name)`.

---

### Corrected Version

```python
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)
```

---

## SECTION 8 — OUTPUT PREDICTION (ADVANCED)

### Q26

```python
class A:
    def show(self):
        print("A")

class B(A):
    pass

class C(B):
    pass

obj = C()
obj.show()
```

**Answer:**

```
A
```

---

### Q27

```python
class A:
    x = 10

class B(A):
    x = 20

print(B.x)
```

**Answer:**

```
20
```

---

### Q28

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(B):
    pass

obj = C()
obj.show()
```

**Answer:**

```
B
```

---

## SECTION 9 — SHORT ANSWER

### Q29

When should inheritance NOT be used?

**Answer:**
When classes do not form a true **is-a** relationship or when composition provides better flexibility.

---

### Q30

Inheritance vs Composition — which is more flexible and why?

**Answer:**
Composition, because it avoids tight coupling and deep hierarchies.

---

## SECTION 10 — ONE-LINERS (RAPID FIRE)

| Question                           | Answer            |
| ---------------------------------- | ----------------- |
| What keyword enforces abstraction? | `@abstractmethod` |
| Parent of all Python classes?      | `object`          |
| Child replaces parent method?      | Overriding        |
| Multiple inheritance order?        | MRO               |
| Access parent method?              | `super()`         |

---

## FINAL CHALLENGE QUESTION

### Q31

Predict output:

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()

class C(B):
    pass

obj = C()
obj.show()
```

**Answer:**

```
B
A
```

**Explanation:**
`C` → `B.show()` → calls `super()` → `A.show()`
