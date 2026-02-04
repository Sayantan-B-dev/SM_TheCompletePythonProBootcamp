## STEP 4 — BALL CLASS & BASIC MOVEMENT (DETAILED GUIDE)

---

## `ball.py` — Ball Class Definition

### Code Under Discussion

```python
from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.penup()
    
    def move(self):
        new_x = self.xcor() + 10
        new_y = self.ycor() + 10
        self.goto(new_x, new_y)
```

---

## Class Responsibility

> The **Ball** represents an autonomous game object that moves every frame without user input.

This is the first object in the game that:

* Moves continuously
* Depends on the game loop timing
* Will later interact with walls and paddles

---

## Constructor (`__init__`) Breakdown

### `class Ball(Turtle):`

**What**

* The ball class inherits from `Turtle`.

**Why**

* The ball is visually a drawable, movable object.
* Inheritance gives access to:

  * `goto()`
  * `xcor()`, `ycor()`
  * Shape and color controls

---

### `super().__init__()`

**What**

* Initializes the underlying Turtle internals.

**Why**

* Mandatory for rendering and movement.
* Without this call, the object will not behave like a turtle.

---

### Visual Setup

```python
self.color("white")
self.shape("square")
```

**What**

* Sets the ball appearance.

**Why**

* White square is visually distinct.
* Square simplifies collision logic later.

---

### `self.penup()`

**What**

* Disables drawing.

**Why**

* Ball movement must not leave trails.
* Same rule as paddles.

---

## Ball Movement Logic

### `def move(self):`

```python
new_x = self.xcor() + 10
new_y = self.ycor() + 10
self.goto(new_x, new_y)
```

---

### What This Does

* Reads the current ball position.
* Adds a fixed increment to both axes.
* Moves the ball diagonally upward-right.

---

### Why This Is Designed This Way (For Now)

* Simple movement to validate:

  * Game loop timing
  * Rendering updates
  * Continuous motion
* Direction and speed are **hardcoded temporarily**.

---

### Important Limitation (Intentional)

| Aspect    | Current State       |
| --------- | ------------------- |
| Direction | Fixed (↗)           |
| Speed     | Fixed (10 px/frame) |
| Bounce    | Not implemented     |
| Reset     | Not implemented     |

This will be refactored in later steps.

---

## `main.py` — Integrating the Ball

### Code Under Discussion

```python
while game_is_on:
    time.sleep(0.1)
    screen.update()
    ball.move()
```

---

## Game Loop Timing Control

### `time.sleep(0.1)`

**What**

* Pauses execution for 0.1 seconds per loop.

**Why**

* Controls animation speed.
* Prevents ball from moving too fast.
* Simulates a frame rate (~10 FPS).

---

### `screen.update()`

**What**

* Manually redraws the screen.

**Why**

* Required because `screen.tracer(0)` disables auto-rendering.
* Ensures all movements appear simultaneously.

---

### `ball.move()`

**What**

* Moves the ball once per frame.

**Why**

* Ball motion is frame-driven.
* This makes the ball speed dependent on loop timing.

---

## Execution Flow Per Frame

> Pause
> → Update screen
> → Move ball
> → Repeat

---

## Coordinate Behavior (Important)

Given:

```text
Initial position → (0, 0)
Movement step    → (+10, +10)
```

Ball positions over frames:

```text
Frame 1 → (10, 10)
Frame 2 → (20, 20)
Frame 3 → (30, 30)
...
```

The ball will eventually exit the screen without collision logic.

---

## Design Insight (Crucial for Next Steps)

Right now:

```python
+10, +10  ← hardcoded direction + speed
```

Soon this will become:

```text
dx → horizontal direction
dy → vertical direction
move → uses dx, dy
```

This separation allows:

* Wall bouncing
* Paddle collision
* Speed scaling

---

## Common Beginner Confusions Clarified

> Ball movement is NOT event-driven
> Ball must be updated every frame
> `sleep()` controls speed, not movement distance
> `screen.update()` does not move objects

---

## What This Step Unlocks Next

* Wall collision detection (Step 5)
* Direction inversion (`dx`, `dy`)
* Resetting ball position
* Scoring mechanics

---

## Mental Model at This Stage

> **Paddles = reactive (input-driven)**
> **Ball = proactive (loop-driven)**
> **Loop = heartbeat of the game**

This step confirms the game loop is functioning as a real-time animation engine and that autonomous objects behave correctly within it.
