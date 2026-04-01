## Object State and Instances — From Real Life → Python → Turtle

![Image](https://miro.medium.com/1%2A3ub0niVwkL9PYcgUuV1ggA.jpeg)

![Image](https://prepbytes-misc-images.s3.ap-south-1.amazonaws.com/assets/1677064501939-Classes%20and%20Objects%20in%20Python1.png)

![Image](https://open.openclass.ai/files/650666178fb61852f9b042fa.png)

![Image](https://i.sstatic.net/EZxdb.png)

---

## 1. What an **Object** Actually Is (Precise Definition)

An **object** is a **bundle of state + behavior**.

* **State** → current data the object holds
* **Behavior** → actions the object can perform using its state

An object is not the code.
An object is a **live instance created from code**.

---

## 2. Object **State** — Meaning Without Abstraction

**Object state** is the **current snapshot of values** stored inside an object at a given moment.

State answers questions like:

* Where am I?
* What do I look like?
* What values define me *right now*?

State **changes over time** when methods are called.

---

## 3. Real-Life Example — Same Blueprint, Different States

### Example: Mobile Phones

**Class (Blueprint):**

* Brand
* Battery level
* Volume
* Power status

**Instances (Actual Phones):**

| Phone   | Battery | Volume | Power |
| ------- | ------- | ------ | ----- |
| Phone A | 90%     | 40     | ON    |
| Phone B | 12%     | 80     | ON    |
| Phone C | 0%      | 0      | OFF   |

All phones follow the **same design**,
but each has its **own independent state**.

Changing Phone A does **not** affect Phone B.

---

## 4. Mapping This Directly to Python

### Concept Mapping

| Real World        | Python       |
| ----------------- | ------------ |
| Blueprint         | `class`      |
| Real object       | `instance`   |
| Properties        | attributes   |
| Actions           | methods      |
| Current condition | object state |

---

## 5. Professional Python Example (Non-Turtle)

### Scenario

A `BankAccount` class where each account has **independent state**.

```python
class BankAccount:
    """
    Represents a single bank account.
    Each instance has its own balance (state).
    """

    def __init__(self, owner, balance):
        # Instance attributes (state)
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # Modifies the internal state
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds")

# -----------------------------
# INSTANCES
# -----------------------------
account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)

account1.deposit(200)
account2.withdraw(100)

print(account1.balance)
print(account2.balance)
```

### Expected Output

```
1200
400
```

### What This Demonstrates

* `account1` and `account2` share the **same class**
* Their **state is separate**
* Method calls mutate **only that instance’s state**

---

## 6. Key Rule (Often Missed)

> A class defines **structure and behavior**
> An instance holds **actual state**

Without instances, a class does nothing.

---

## 7. Turtle as a Perfect Visualization of Object State

Each `turtle.Turtle()` object maintains its own internal state:

### Turtle State Internally Includes

| Attribute | Meaning         |
| --------- | --------------- |
| Position  | `(x, y)`        |
| Heading   | direction angle |
| Pen state | up / down       |
| Color     | pen & fill      |
| Speed     | animation speed |
| Shape     | visual form     |

You never manage these manually — turtle does.

---

## 8. Turtle Example — Multiple Instances, Independent State

```python
import turtle

# =============================
# SCREEN SETUP
# =============================
screen = turtle.Screen()
screen.setup(600, 600)
screen.title("Object State & Instances with Turtle")

# =============================
# FIRST TURTLE INSTANCE
# =============================
turtle1 = turtle.Turtle()
turtle1.color("blue")
turtle1.penup()
turtle1.goto(-100, 0)

# =============================
# SECOND TURTLE INSTANCE
# =============================
turtle2 = turtle.Turtle()
turtle2.color("red")
turtle2.penup()
turtle2.goto(100, 0)

# =============================
# STATE CHANGES
# =============================
turtle1.forward(50)
turtle2.left(90)
turtle2.forward(50)

screen.mainloop()
```

---

## 9. Expected Output (Observed Behavior)

* Two turtles appear on screen
* Blue turtle moves right
* Red turtle turns and moves upward
* Each turtle remembers:

  * Its own position
  * Its own direction
  * Its own color

No shared state. No interference.

---

## 10. Why This Is Object State in Action

Even though:

* Both turtles come from `turtle.Turtle`
* Both have the same methods

They behave differently because:

> **Methods operate on `self`, and `self` refers to the instance**

---

## 11. What `self` Really Means (Critical Insight)

```python
turtle1.forward(50)
```

Internally becomes:

```
forward(self=turtle1, distance=50)
```

So:

* State updates apply only to `turtle1`
* `turtle2` remains unchanged

---

## 12. Visual Summary — One Class, Many States

```
Turtle Class
   |
   ├── turtle1 → position (-50, 0), heading 0°
   ├── turtle2 → position (100, 50), heading 90°
   └── turtle3 → position (0, -100), heading 180°
```

Same behavior. Different realities.

---

## 13. Why Object State Is Central to Games & GUIs

Every interactive system relies on:

* Player objects with position state
* Enemy objects with health state
* UI objects with visibility state
* Timer objects with time state

Games are **nothing more than state transitions over time**.

---

## 14. Core Principle to Lock In

> A class describes *what something can be*
> An instance represents *what it is right now*

Once this clicks, object-oriented programming stops being abstract and becomes mechanical and predictable.
