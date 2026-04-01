## CLASS INHERITANCE IN PYTHON — COMPLETE, DEEP, AND PRACTICAL

---

## 1. What Is Inheritance

### Definition

Inheritance is an OOP mechanism where a **child class** acquires attributes and methods of a **parent class**, allowing **code reuse**, **logical hierarchy**, and **polymorphic behavior**.

> Relationship meaning: **“is-a”**
>
> A Fish *is an* Animal
> A Dog *is an* Animal

---

## 2. Why Inheritance Exists

| Problem Without Inheritance | Solution With Inheritance  |
| --------------------------- | -------------------------- |
| Code duplication            | Shared logic in base class |
| Hard to maintain            | Centralized behavior       |
| Flat structure              | Hierarchical modeling      |
| Poor extensibility          | Easy specialization        |

---

## 3. Basic Inheritance (Single Inheritance)

### Structure

```
ParentClass
     ↑
 ChildClass
```

---

### Algorithm

1. Create a base class with common attributes/methods
2. Create a child class using `class Child(Parent):`
3. Child automatically gets parent methods
4. Child may add new methods

---

### Example

```python
class Animal:
    def eat(self):
        print("Animal is eating")

    def sleep(self):
        print("Animal is sleeping")


class Dog(Animal):
    def bark(self):
        print("Dog is barking")
```

---

### Execution

```python
dog = Dog()
dog.eat()
dog.sleep()
dog.bark()
```

---

### Output

```
Animal is eating
Animal is sleeping
Dog is barking
```

---

### Key Observations

* `Dog` inherits `eat()` and `sleep()`
* `Dog` adds its own behavior
* No code duplication

---

## 4. `super()` — Parent Access Mechanism

### Definition

`super()` is used to **call methods or constructors of the parent class** from the child class.

---

### Why `super()` Is Needed

| Without `super()`   | With `super()`              |
| ------------------- | --------------------------- |
| Parent init ignored | Parent properly initialized |
| Manual duplication  | Clean inheritance           |
| Error-prone         | Safe and scalable           |

---

### Algorithm

1. Parent defines `__init__`
2. Child defines its own `__init__`
3. Child calls `super().__init__()`
4. Parent initialization runs first

---

### Example

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def info(self):
        print(f"Name: {self.name}")


class Fish(Animal):
    def __init__(self, name, water_type):
        super().__init__(name)   # Call parent constructor
        self.water_type = water_type

    def swim(self):
        print("Fish is swimming")
```

---

### Execution

```python
fish = Fish("Goldfish", "Freshwater")
fish.info()
fish.swim()
print(fish.water_type)
```

---

### Output

```
Name: Goldfish
Fish is swimming
Freshwater
```

---

### Rule

> Always use `super()` when the parent has important initialization logic.

---

## 5. Method Overriding

### Definition

Method overriding occurs when a **child class provides its own implementation** of a parent method using the **same method name**.

---

### Why Override

* To change behavior
* To specialize functionality
* To extend parent logic

---

### Algorithm

1. Parent defines a method
2. Child defines a method with the same name
3. Child version is called instead

---

### Example

```python
class Animal:
    def speak(self):
        print("Animal makes a sound")


class Cat(Animal):
    def speak(self):
        print("Cat meows")
```

---

### Execution

```python
cat = Cat()
cat.speak()
```

---

### Output

```
Cat meows
```

---

### Important Rule

> Python chooses the **child version first** (Method Resolution Order).

---

## 6. Extending Overridden Methods Using `super()`

### Purpose

Override **but still use parent behavior**.

---

### Example

```python
class Bird(Animal):
    def speak(self):
        super().speak()
        print("Bird chirps")
```

---

### Execution

```python
bird = Bird("Sparrow")
bird.speak()
```

---

### Output

```
Animal makes a sound
Bird chirps
```

---

## 7. Method Overwriting vs Overriding

| Term        | Meaning                        |
| ----------- | ------------------------------ |
| Overriding  | Child replaces parent behavior |
| Overwriting | Informal term (not official)   |
| Python term | Method overriding              |

---

## 8. Types of Inheritance in Python

---

### 8.1 Single Inheritance

```
Animal → Dog
```

Already covered.

---

### 8.2 Multilevel Inheritance

```
Animal → Mammal → Human
```

---

### Algorithm

1. Base class defines core behavior
2. Intermediate class adds specialization
3. Final class adds more detail

---

### Example

```python
class Animal:
    def breathe(self):
        print("Breathing")


class Mammal(Animal):
    def give_birth(self):
        print("Giving birth")


class Human(Mammal):
    def think(self):
        print("Thinking")
```

---

### Execution

```python
person = Human()
person.breathe()
person.give_birth()
person.think()
```

---

### Output

```
Breathing
Giving birth
Thinking
```

---

### Insight

> Human inherits behavior from **both ancestors automatically**.

---

### 8.3 Hierarchical Inheritance

```
        Animal
        /    \
     Dog     Fish
```

---

### Example

```python
class Animal:
    def move(self):
        print("Moving")


class Dog(Animal):
    def run(self):
        print("Running")


class Fish(Animal):
    def swim(self):
        print("Swimming")
```

---

### Output

```
Dog → move(), run()
Fish → move(), swim()
```

---

### 8.4 Multiple Inheritance

```
Father   Mother
   \       /
     Child
```

---

### Algorithm

1. Child inherits from multiple parents
2. Python follows **MRO (Method Resolution Order)**

---

### Example

```python
class Father:
    def skill(self):
        print("Driving")


class Mother:
    def skill(self):
        print("Cooking")


class Child(Father, Mother):
    pass
```

---

### Execution

```python
child = Child()
child.skill()
```

---

### Output

```
Driving
```

---

### Why?

MRO order:

```
Child → Father → Mother → object
```

---

### Checking MRO

```python
print(Child.__mro__)
```

---

### Output

```
(<class '__main__.Child'>, <class '__main__.Father'>, <class '__main__.Mother'>, <class 'object'>)
```

---

### 8.5 Hybrid Inheritance

Combination of multiple + multilevel.

```
Animal
   |
Mammal
  /   \
Human  Bat
```

---

## 9. Encapsulation (Data Hiding)

### Definition

Encapsulation restricts direct access to data and protects internal state.

---

### Access Modifiers (Python Convention)

| Type      | Syntax  | Meaning               |
| --------- | ------- | --------------------- |
| Public    | `var`   | Accessible everywhere |
| Protected | `_var`  | Internal use          |
| Private   | `__var` | Name-mangled          |

---

### Example

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance
```

---

### Execution

```python
account = BankAccount(1000)
print(account.get_balance())
```

---

### Output

```
1000
```

---

## 10. Abstraction (Using ABC)

### Definition

Abstraction hides implementation details and forces subclasses to implement required methods.

---

### Algorithm

1. Create abstract base class
2. Define abstract methods
3. Child must implement them

---

### Example

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass


class Square(Shape):
    def area(self):
        return 4 * 4
```

---

### Execution

```python
sq = Square()
print(sq.area())
```

---

### Output

```
16
```

---

### Rule

> Cannot instantiate abstract class directly.

---

## 11. Polymorphism

### Definition

Same method name behaves differently for different objects.

---

### Example

```python
class Dog:
    def sound(self):
        print("Bark")


class Cat:
    def sound(self):
        print("Meow")
```

---

### Execution

```python
animals = [Dog(), Cat()]

for animal in animals:
    animal.sound()
```

---

### Output

```
Bark
Meow
```

---

## 12. Composition vs Inheritance

| Inheritance    | Composition    |
| -------------- | -------------- |
| is-a           | has-a          |
| Tight coupling | Loose coupling |
| Rigid          | Flexible       |

---

### Composition Example

```python
class Engine:
    def start(self):
        print("Engine started")


class Car:
    def __init__(self):
        self.engine = Engine()

    def drive(self):
        self.engine.start()
```

---

### Output

```
Engine started
```

---

## 13. When to Use What

| Scenario             | Use         |
| -------------------- | ----------- |
| Shared behavior      | Inheritance |
| Code reuse           | Inheritance |
| Feature assembly     | Composition |
| Avoid deep hierarchy | Composition |
| Enforced contracts   | Abstraction |

---

## 14. Core Rules Summary

* Use inheritance for **logical hierarchy**
* Use `super()` for **parent initialization**
* Override responsibly
* Prefer composition over deep inheritance
* Respect MRO in multiple inheritance
* Encapsulate data
* Abstract interfaces, not implementations
