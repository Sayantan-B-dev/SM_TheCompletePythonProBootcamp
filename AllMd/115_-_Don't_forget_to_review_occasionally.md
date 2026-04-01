## PRACTICAL TIPS — WHAT YOU HAVE LEARNED SO FAR (LOCK-IN GUIDE)

---

## 1. Always Think in **Responsibilities**, Not Code

> If you start thinking in syntax, you are already late.

**Rule**

* First decide **who owns what**
* Then decide **who is allowed to change it**

**Application**

* `MenuItem` owns drink data
* `CoffeeMaker` owns resources
* `MoneyMachine` owns money
* `main.py` owns *nothing* except flow

If a file owns data **and** logic that doesn’t belong together → redesign.

---

## 2. One Owner per Data (Non-Negotiable Rule)

**Bad**

```text
Multiple functions modify the same dictionary
```

**Good**

```text
Exactly one object owns the data
Everyone else must ask politely
```

**Heuristic**

> If two classes modify the same variable → design is broken

---

## 3. If a Function Needs Many Parameters, It Wants to Be a Method

**Smell**

```python
make_coffee(drink, water, milk, coffee, machine_state)
```

**Fix**

```python
coffee_maker.make_coffee(drink)
```

Why:

* Parameters often mean missing ownership
* Objects already *know* their own state

---

## 4. `main.py` Is a Conductor, Not a Worker

**What `main.py` should do**

* Ask for input
* Call object methods
* Handle flow

**What it must NOT do**

* Calculate
* Store business data
* Apply rules

If logic grows in `main.py`, push it down into objects.

---

## 5. Objects Should Collaborate, Not Control

**Bad design**

```text
One object knows everything
```

**Good design**

```text
Each object knows little
They cooperate through methods
```

This reduces:

* Bugs
* Coupling
* Fear of change

---

## 6. Encapsulation Is About Safety, Not Hiding

Encapsulation means:

* Protecting valid states
* Forcing rules to be respected

**Example**

* You never directly subtract resources
* You *ask* `CoffeeMaker` to do it

This prevents:

* Negative inventory
* Silent corruption

---

## 7. Treat Packages as Black Boxes with Contracts

When using packages (`turtle`, `prettytable`, `requests`):

**Do**

* Read documentation
* Learn public methods
* Trust the implementation

**Never**

* Depend on internal attributes
* Modify private state
* Assume internal behavior

> You consume **interfaces**, not implementations.

---

## 8. OOP Is a Design Tool, Not a Syntax Requirement

**Do not**

* Create classes just to “use OOP”
* Wrap everything in a class

**Use OOP when**

* State must be preserved
* Rules must be enforced
* System will grow
* Multiple parts interact

Small scripts can stay procedural.

---

## 9. Class Checklist (Before You Write One)

Before creating a class, answer:

* What does it **own**?
* What does it **protect**?
* What does it **decide**?
* What must others **not** do directly?

If you can’t answer → don’t create the class yet.

---

## 10. Files Should Map to Concepts, Not Convenience

**Good**

```text
menu.py         → menu logic
money_machine.py → payment logic
```

**Bad**

```text
helpers.py
utils.py
common.py
```

Generic files hide responsibility and invite chaos.

---

## 11. Design for Change, Not for Today

Ask:

* What if a new drink is added?
* What if payment method changes?
* What if resources increase?

If adding a feature requires changing many files → design is tight.

---

## 12. Prefer Extension Over Modification

**Bad**

```text
Edit existing logic everywhere
```

**Good**

```text
Add a new class or object
```

This is how professional systems scale without breaking.

---

## 13. Use Objects to Reduce Mental Load

OOP works when:

* You think less about *how*
* You focus on *what*

Example:

```python
money_machine.make_payment(cost)
```

You don’t care:

* How coins are counted
* How change is calculated

That mental relief is the real power of OOP.

---

## 14. Debugging Tip Specific to OOP

When something breaks:

1. Identify **which object owns the problem**
2. Check its state
3. Check who last modified it

Never debug the whole system at once.

---

## 15. Final Mental Model to Keep Forever

```text
Class  → Responsibility definition
Object → Responsibility execution
Method → Allowed action
State  → Protected data
System → Object collaboration
```

If you keep this model, everything you build next will be cleaner, safer, and scalable.
