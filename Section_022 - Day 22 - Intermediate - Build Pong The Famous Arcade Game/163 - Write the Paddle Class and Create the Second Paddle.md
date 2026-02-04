## STEP 3 — PADDLE CLASS + TWO PADDLES (DETAILED GUIDE)

---

## `paddle.py` — Class Definition

### Code Under Discussion

```python
from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)
```

---

## Class Design Explanation

### `class Paddle(Turtle):`

**What**

* Creates a new class that **inherits from `Turtle`**.

**Why**

* A paddle *is a turtle*, just with:

  * Predefined shape
  * Predefined size
  * Restricted movement
* Inheritance avoids rewriting movement and positioning logic already provided by `Turtle`.

**Mental Model**

```text
Turtle  → generic drawable object
Paddle  → specialized Turtle with vertical-only movement
```

---

### `def __init__(self, position):`

**What**

* Constructor executed when a new `Paddle` object is created.

**Why**

* Ensures every paddle is initialized consistently.
* Allows dynamic positioning via `position` parameter.

---

### `super().__init__()`

**What**

* Calls the parent (`Turtle`) constructor.

**Why (Critical)**

* Without this:

  * The paddle will not render
  * Turtle methods like `goto()` will fail
* This sets up the internal turtle state.

---

### Shape & Visual Configuration

```python
self.shape("square")
self.color("white")
self.shapesize(stretch_wid=5, stretch_len=1)
```

**What**

* Configures appearance once, inside the class.

**Why**

* Centralizes configuration.
* Prevents duplication in the main file.
* Any future visual change needs to be done in one place only.

---

### `self.penup()`

**What**

* Disables drawing.

**Why**

* Paddle movement should not leave trails.
* Essential for all moving game objects.

---

### `self.goto(position)`

**What**

* Moves paddle to the passed `(x, y)` tuple.

**Why**

* Enables reusable paddle placement:

  * Left paddle
  * Right paddle
  * Potential AI paddle later

---

## Paddle Movement Methods

---

### `go_up()` Method

```python
new_y = self.ycor() + 20
self.goto(self.xcor(), new_y)
```

**What**

* Moves paddle upward by a fixed increment.

**Why**

* Keeps movement predictable and controllable.
* X position remains constant → vertical-only movement.

---

### `go_down()` Method

```python
new_y = self.ycor() - 20
self.goto(self.xcor(), new_y)
```

**What**

* Moves paddle downward symmetrically.

**Why**

* Ensures balanced control in both directions.

---

## `main.py` — Using the Paddle Class

---

### Code Under Discussion

```python
from paddle import Paddle

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
```

---

### Paddle Instantiation

**What**

* Creates two independent paddle objects.

**Why**

* Same class, different positions.
* Demonstrates object reuse.

**Position Logic**

```text
Right paddle → x = +350
Left paddle  → x = -350
```

This keeps paddles:

* Inside screen bounds
* Symmetrically placed

---

## Keyboard Binding for Two Players

---

### Code Under Discussion

```python
screen.listen()

screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")

screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")
```

---

### `screen.listen()`

**What**

* Activates keyboard event listening.

**Why**

* Required once before binding keys.

---

### Right Paddle Controls

**Mapping**

```text
Up Arrow    → r_paddle.go_up
Down Arrow  → r_paddle.go_down
```

**Why**

* Natural mapping for Player 2 (right side).

---

### Left Paddle Controls

**Mapping**

```text
W → l_paddle.go_up
S → l_paddle.go_down
```

**Why**

* Classic WASD-style control for Player 1.
* Avoids key conflict.

---

## Event-Driven Architecture Insight

> The `while` loop **does not** move paddles
> Key presses trigger movement instantly
> Turtle internally manages event callbacks

This separation keeps:

* Input handling clean
* Game loop focused on rendering and physics

---

## What This Step Achieves Architecturally

| Improvement            | Benefit                |
| ---------------------- | ---------------------- |
| Paddle class           | Reusability            |
| Inheritance            | Less code duplication  |
| Parameterized position | Flexible instantiation |
| Encapsulated movement  | Cleaner main file      |
| Dual controls          | Multiplayer readiness  |

---

## Known Missing Safeguards (Expected)

* Paddle boundary checks (top/bottom)
* Movement speed tuning
* AI paddle logic

These are intentionally deferred to later steps.

---

## Conceptual Model at This Stage

> **Class = Blueprint**
> **Object = Player paddle**
> **Keyboard input = Event**
> **Movement = Method call**

This step transitions the game from procedural code to a clean object-oriented structure, which is essential before introducing the ball, collision logic, and scoring.
