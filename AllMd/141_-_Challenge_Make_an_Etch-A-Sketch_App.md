## Etch-A-Sketch — Event-Driven Drawing with `turtle`

![Image](https://opengraph.githubassets.com/4a9dfe87ca4877d7acdb84d5b656011732b02cdf5be2a544f8dd7f8d6283f48c/cmlohr/py-etch-a-sketch)

![Image](https://content.instructables.com/F02/QLJS/HWIBTX26/F02QLJSHWIBTX26.png)

![Image](https://www.oreilly.com/api/v2/epubs/urn%3Aorm%3Abook%3A9781119049517/files/images/9781119049517-fg1201.png)

![Image](https://miro.medium.com/0%2ABdzrHhBRZ9LwBJFe)

---

## 1. What an Etch-A-Sketch Program Really Is

An Etch-A-Sketch is **not** a drawing algorithm.
It is an **event-driven interaction system** where:

* A cursor (player) has **state**: position + heading
* User input **modifies that state**
* The screen **persists history** (lines stay)

This makes it a perfect minimal game-like system.

---

## 2. Core Concepts Involved

### Concept → Turtle Mapping

| Concept    | Turtle Feature            | Purpose              |
| ---------- | ------------------------- | -------------------- |
| Cursor     | `Turtle()`                | Drawing entity       |
| Movement   | `forward()`, `backward()` | Controlled motion    |
| Rotation   | `left()`, `right()`       | Direction control    |
| Input      | `onkey()`                 | User interaction     |
| Reset      | `reset()`                 | Clear screen         |
| Event loop | `mainloop()`              | Continuous listening |

This is a **full event-listener architecture**.

---

## 3. Interaction Model (Mental Flow)

```
User presses key
→ Screen detects event
→ Calls stored function reference
→ Function updates turtle state
→ Turtle redraws automatically
```

No polling. No loops. No `input()`.

---

## 4. Vanilla Logic Breakdown (Before Code)

* Movement functions do **one small action**
* Functions are passed **as references**
* `Screen` acts as an **event dispatcher**
* Turtle draws because pen is down by default

---

## 5. Complete Etch-A-Sketch Implementation

```python
import turtle

# =============================
# SCREEN SETUP
# =============================
screen = turtle.Screen()
screen.title("Etch-A-Sketch — Turtle Event System")
screen.setup(width=700, height=700)

# =============================
# TURTLE SETUP
# =============================
pen = turtle.Turtle()
pen.shape("turtle")
pen.speed(0)        # Fastest drawing speed
pen.pensize(2)      # Visible line thickness

# =============================
# MOVEMENT FUNCTIONS
# =============================

def move_forward():
    """
    Moves the turtle forward in the direction
    it is currently facing.
    """
    pen.forward(20)

def move_backward():
    pen.backward(20)

def turn_left():
    """
    Rotates turtle counter-clockwise
    without changing position.
    """
    pen.left(15)

def turn_right():
    pen.right(15)

def clear_screen():
    """
    Clears drawing and resets turtle
    to center with default orientation.
    """
    pen.reset()
    pen.speed(0)
    pen.pensize(2)

# =============================
# EVENT LISTENERS
# =============================
screen.listen()

# Keyboard bindings (higher-order usage)
screen.onkey(move_forward, "w")
screen.onkey(move_backward, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(clear_screen, "c")

# =============================
# EVENT LOOP
# =============================
screen.mainloop()
```

---

## 6. Expected Output (Observed Behavior)

* Turtle appears at center of window
* Press:

  * `w` → draws forward
  * `s` → draws backward
  * `a` → rotates left
  * `d` → rotates right
  * `c` → clears entire drawing
* Lines persist until cleared
* No movement occurs without key events

---

## 7. Why This Is a Perfect Event-Listener Example

### Higher-Order Function Use

```python
screen.onkey(move_forward, "w")
```

* `move_forward` is **passed**, not executed
* `onkey` stores it internally
* Turtle executes it later on key press

This is **pure higher-order function behavior**.

---

## 8. What Happens If You Write This (Common Mistake)

```python
screen.onkey(move_forward(), "w")
```

### Result

* Function executes immediately
* `None` is passed to `onkey`
* Key press does nothing

### Reason

You passed the **result**, not the **function**.

---

## 9. Game-Level Thinking Hidden Inside Etch-A-Sketch

| Game System        | Present Here |
| ------------------ | ------------ |
| Player control     | Yes          |
| Persistent world   | Yes          |
| Event-driven input | Yes          |
| State changes      | Yes          |
| Reset mechanics    | Yes          |
| Real-time feedback | Yes          |

This is why Etch-A-Sketch is often the **first real interactive system** people truly understand.

---

## 10. Extend This Into Games (Natural Evolution)

* Add boundary checks → maze
* Add collision → obstacles
* Add timer → animation
* Add score → game state
* Add multiple turtles → multiplayer / enemies

Same architecture. Same concepts. Larger ruleset.

---

## 11. One Core Principle to Lock In

> The screen never asks *what to do*.
> It waits for you to tell it *which function to run* when something happens.

That is the heart of event-driven programming, and Etch-A-Sketch makes it visible.
