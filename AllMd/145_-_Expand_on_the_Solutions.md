## Practical Tips — Object State, Instances, Events, Higher-Order Functions, Turtle

---

## 1. Lock the Mental Model First (Non-Negotiable)

> **Programs are state machines.**
> Objects store state.
> Functions mutate state.
> Events decide *when* mutations happen.

If you ever feel confused, ask only one question:

> *“Which object’s state is changing right now?”*

If you can answer that, the code is correct or fixable.

---

## 2. Always Separate These Three Layers

| Layer             | Responsibility | Examples                 |
| ----------------- | -------------- | ------------------------ |
| **Object layer**  | Hold state     | Turtle position, color   |
| **Logic layer**   | Decide rules   | race loop, win condition |
| **Control layer** | Decide timing  | events, loops, timers    |

**Never mix them.**
If a turtle decides who wins, design is already broken.

---

## 3. Treat `self` as “THIS OBJECT ONLY”

When reading or writing methods, mentally rewrite:

```python
t.forward(10)
```

As:

```python
forward(self=t, distance=10)
```

This prevents:

* accidental shared-state assumptions
* confusion with multiple instances
* fear of loops over objects

---

## 4. Classes Do Nothing by Themselves

A class:

* does not move
* does not draw
* does not run

Only **instances** do.

If something is “not happening”, check:

* did you create an instance?
* are you calling methods on the instance, not the class?

---

## 5. One Object = One Responsibility

Bad thinking:

> “This turtle should know it won”

Correct thinking:

> “The controller checks turtle state and decides outcome”

Objects should:

* expose state
* respond to commands
* not make global decisions

---

## 6. Event Listeners Are Storage, Not Execution

Whenever you see:

```python
screen.onkey(move, "Up")
```

Understand it as:

> “Store this function for later. Do nothing now.”

If something runs immediately:

* you passed `function()`
* not `function`

This single mistake causes most beginner event bugs.

---

## 7. Never Debug Turtle by Guessing — Inspect State

Use:

```python
print(t.xcor(), t.ycor(), t.heading())
```

Turtle bugs are **state bugs**, not syntax bugs.

If something looks wrong visually:

* print the state
* compare expected vs actual

---

## 8. Recreate Objects Instead of Resetting Them

On restart:

* destroy old objects
* create new instances

Do **not** try to “reset everything manually”.

Fresh instances = clean state = fewer bugs.

---

## 9. Lists Hold References, Not Copies (Burn This In)

If you put objects in a list:

```python
turtles.append(t)
```

You are storing **addresses**, not data.

Any method call through the list:

* affects the real object
* not a duplicate

This is why loops work safely.

---

## 10. Use Flags for Flow, Not Objects

Control variables like:

```python
is_race_on
game_over
running
```

Belong to:

* logic layer
* controller layer

Not inside objects.

Objects should never decide when the program ends.

---

## 11. Randomness Is State Mutation, Not Decoration

Random values:

* must change state
* must happen inside loops
* must be applied incrementally

Randomness outside a loop = instant jump, not simulation.

---

## 12. If You Can Explain It Without Code, You Understand It

Before writing code, be able to say:

* what objects exist
* what state each holds
* what events change that state
* what condition ends the system

If you can’t explain it verbally, coding will be messy.

---

## 13. Turtle Is a Teaching Tool — Treat It Seriously

What Turtle teaches correctly:

* object isolation
* event-driven systems
* real game loops
* state mutation over time

If you master these here, frameworks later feel trivial.

---

## 14. Common Red Flags (Stop and Fix Immediately)

| Red Flag                    | Meaning                  |
| --------------------------- | ------------------------ |
| Global variables everywhere | Poor state design        |
| Objects deciding game flow  | Mixed responsibilities   |
| Functions doing too much    | Missing abstraction      |
| Reset bugs                  | State not recreated      |
| Confusion with `self`       | Instance model not clear |

---

## 15. Final Rule to Keep Forever

> **Good programs are boringly predictable because state changes are controlled.**
