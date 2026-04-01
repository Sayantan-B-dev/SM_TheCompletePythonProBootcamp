## QUIZ SET — Object State, Instances, Higher-Order Functions, Events, Turtle

---

## SECTION 1 — Fundamentals: Objects, Classes, Instances

### Q1

Which statement best defines an **object**?

A. A function that stores variables
B. A blueprint for creating data
C. A bundle of state and behavior
D. A Python file

**Answer:** C
**Explanation:** An object combines **state (data)** and **behavior (methods)** in a live instance.

---

### Q2

What is the relationship between a **class** and an **instance**?

A. Class is created from instance
B. Instance is a copy of another instance
C. Instance is created from a class
D. They are the same thing

**Answer:** C
**Explanation:** A class is a blueprint; an instance is a concrete object created from it.

---

### Q3

If two objects are created from the same class, which is true?

A. They share state
B. They share memory
C. They share behavior but not state
D. They behave differently by default

**Answer:** C
**Explanation:** Methods are shared, but each instance has its own independent state.

---

### Q4

What does “object state” mean?

A. The class variables
B. The current values inside an object
C. The methods an object has
D. The object’s name

**Answer:** B
**Explanation:** State is the snapshot of attribute values at a given time.

---

## SECTION 2 — `self` and Instance Behavior

### Q5

In a method definition, what does `self` represent?

A. The class
B. A global variable
C. The current instance
D. The function itself

**Answer:** C
**Explanation:** `self` refers to the specific object that called the method.

---

### Q6

What happens internally when you call:

```python
turtle1.forward(50)
```

A. All turtles move
B. The Turtle class updates
C. Only `turtle1` updates its position
D. The screen redraws everything manually

**Answer:** C
**Explanation:** `self` is bound to `turtle1`, so only its state mutates.

---

### Q7

Why don’t multiple turtle objects interfere with each other?

A. Turtle uses threads
B. Each turtle has isolated state
C. Python prevents conflicts
D. They run sequentially

**Answer:** B
**Explanation:** Each turtle instance stores its own position, heading, and pen state.

---

## SECTION 3 — Higher-Order Functions

### Q8

What makes a function a **higher-order function**?

A. It uses loops
B. It returns a value
C. It takes or returns another function
D. It is defined inside a class

**Answer:** C
**Explanation:** Higher-order functions operate on other functions.

---

### Q9

Which is passed to an event listener?

A. Function result
B. Function name as string
C. Function reference
D. Function output

**Answer:** C
**Explanation:** Event systems store function references to call later.

---

### Q10

What is the difference between these two?

```python
onkey(move_up, "Up")
onkey(move_up(), "Up")
```

**Answer:**

* First passes the function reference
* Second calls the function immediately and passes `None`

**Explanation:** Parentheses execute the function immediately.

---

## SECTION 4 — Event Listeners and Callbacks

### Q11

Why are event listeners considered *deferred execution*?

A. They use loops
B. They wait for user or time-based events
C. They run in parallel
D. They execute faster

**Answer:** B
**Explanation:** Execution happens later when the event occurs.

---

### Q12

Which turtle method registers a keyboard event?

A. `listen()`
B. `onkey()`
C. `mainloop()`
D. `forward()`

**Answer:** B
**Explanation:** `onkey()` maps keys to callback functions.

---

### Q13

What is the role of `screen.listen()`?

A. Draws the screen
B. Enables event detection
C. Starts animation
D. Clears input buffer

**Answer:** B
**Explanation:** Without `listen()`, key events are ignored.

---

## SECTION 5 — Turtle Object State

### Q14

Which of the following are part of a turtle’s internal state?
(Choose all that apply)

A. Position
B. Heading
C. Color
D. Screen size

**Answer:** A, B, C
**Explanation:** Screen size belongs to the `Screen` object, not the turtle.

---

### Q15

What does `penup()` change?

A. Turtle speed
B. Turtle position
C. Drawing state
D. Screen state

**Answer:** C
**Explanation:** It disables drawing while moving.

---

### Q16

Why does clearing the screen not reset turtle objects automatically?

A. Turtle ignores clear
B. Objects persist in memory
C. Python blocks reset
D. Clear only removes colors

**Answer:** B
**Explanation:** `clear()` removes visuals, not Python objects.

---

## SECTION 6 — Lists, References, and Instances

### Q17

What does a list of turtles store?

A. Copies of turtles
B. Turtle coordinates
C. References to turtle objects
D. Turtle classes

**Answer:** C
**Explanation:** Lists store references to objects, not duplicates.

---

### Q18

If you modify a turtle via a list reference, what happens?

A. Only the list changes
B. The real turtle instance changes
C. A new turtle is created
D. Nothing happens

**Answer:** B
**Explanation:** The reference points to the real object.

---

## SECTION 7 — Game State vs Object State

### Q19

Which is **game state**, not object state?

A. Turtle x-position
B. Turtle color
C. `is_race_on`
D. Turtle heading

**Answer:** C
**Explanation:** `is_race_on` controls game flow, not any turtle.

---

### Q20

Why should objects not control the game outcome directly?

A. Performance reasons
B. Objects lack methods
C. Separation of concerns
D. Turtle limitation

**Answer:** C
**Explanation:** Clean design separates state holders from controllers.

---

## SECTION 8 — Reasoning & Edge Cases

### Q21

What would happen if you reused the same turtle instead of creating new ones on restart?

**Answer:**
Old state (position, direction, color) would leak into the new race, causing unpredictable behavior.

---

### Q22

Why is randomness applied inside the race loop?

**Answer:**
Because state must change incrementally over simulated time, not all at once.

---

### Q23

Why is the winner detected using `xcor()` instead of color comparison?

**Answer:**
Winning is a spatial condition; color is only metadata used for result evaluation.

---

## SECTION 9 — True / False

| Statement                                  | True / False |
| ------------------------------------------ | ------------ |
| Classes hold state                         | False        |
| Instances mutate state                     | True         |
| Event listeners call functions immediately | False        |
| `self` is optional                         | False        |
| Turtle objects are state machines          | True         |

---

## SECTION 10 — One-Line Concept Checks

* **Class:** blueprint
* **Instance:** live object
* **State:** current data
* **Behavior:** methods
* **Callback:** deferred function
* **Event system:** function dispatcher
* **Game loop:** controlled state mutation over time

---

This quiz set covers conceptual understanding, code-level reasoning, and architectural thinking for everything learned so far.
