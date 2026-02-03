## STEP 4 — CONTROLLING THE SNAKE WITH KEY PRESSES

**Direction control logic + event binding explained deeply**

---

## DIRECTION CONTROL METHODS (INSIDE `Snake` CLASS)

These methods **do not move the snake**.
They only **change the heading of the head**.
Actual movement still happens inside `move()`.

---

### `up()` — MOVE NORTH

```python
def up(self):
    if self.head.heading() != DOWN:  # heading() is a Turtle method
        self.head.setheading(UP)
```

**What this does**

* Checks the current direction of the snake’s head.
* If the snake is **not moving down**, it allows moving up.

**Why this check is critical**

* Prevents instant 180° reversal.
* Without this, the snake would collide with itself immediately.

**Underlying turtle mechanics**

* `heading()` returns the current angle in degrees:

  * `UP`    → 90°
  * `DOWN`  → 270°
  * `LEFT`  → 180°
  * `RIGHT` → 0°
* `setheading()` changes direction without moving.

---

### `down()` — MOVE SOUTH

```python
def down(self):
    if self.head.heading() != UP:
        self.head.setheading(DOWN)
```

**Logic symmetry**

* Same logic as `up()`, but inverted.
* Prevents `UP → DOWN` reversal.

**Design consistency**

* Every direction method:

  * Performs a safety check
  * Then updates heading only if valid

---

### `left()` — MOVE WEST

```python
def left(self):
    if self.head.heading() != RIGHT:
        self.head.setheading(LEFT)
```

**Why RIGHT is blocked**

* `LEFT → RIGHT` is a direct reversal.
* Would cause the head to overlap the first body segment.

---

### `right()` — MOVE EAST

```python
def right(self):
    if self.head.heading() != LEFT:
        self.head.setheading(RIGHT)
```

**Important observation**

* Direction logic is **stateless**
* It relies entirely on the turtle’s current heading

---

## CORE RULE ENFORCED BY ALL METHODS

> **The snake can turn left or right relative to its motion,
> but can never reverse into itself.**

This rule is foundational for:

* Collision logic
* Predictable movement
* Classic Snake behavior

---

## KEYBOARD EVENT LISTENING (MAIN FILE)

### ENABLING KEYBOARD INPUT

```python
screen.listen()
```

**What this does**

* Puts the screen into “input listening” mode.

**Why it is required**

* Without this, key presses are ignored.
* Must be called once before using `onkey()`.

---

## BINDING KEYS TO SNAKE METHODS

```python
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
```

### How this works internally

| Component  | Role                                     |
| ---------- | ---------------------------------------- |
| `"Up"`     | Physical key on keyboard                 |
| `snake.up` | Function reference (not a function call) |
| `onkey()`  | Event binding mechanism                  |

---

### VERY IMPORTANT DETAIL

```python
snake.up     # correct
snake.up()   # wrong
```

**Why**

* `snake.up` passes the function **without executing it**.
* `snake.up()` would execute immediately and pass `None`.

This is a common beginner bug.

---

## EVENT-DRIVEN FLOW (MENTAL MODEL)

```
User presses key
        ↓
Turtle screen detects key
        ↓
Bound Snake method is called
        ↓
Snake head direction changes
        ↓
Next game loop frame moves head forward
```

**Key Insight**

* Key presses do **not** move the snake instantly.
* They only affect the **next frame’s movement**.

---

## HOW THIS INTEGRATES WITH `move()`

```text
Game Loop:
  ├─ listen for input (asynchronous)
  ├─ move snake forward
  ├─ redraw screen
  └─ repeat
```

* Direction changes are stored as state.
* Movement consumes that state.

---

## STATE AFTER STEP 4

| Feature                     | Status       |
| --------------------------- | ------------ |
| Snake movement              | Continuous   |
| Direction control           | Implemented  |
| Illegal reversal prevention | Implemented  |
| Input handling              | Event-driven |
| Game rules                  | Not yet      |

---