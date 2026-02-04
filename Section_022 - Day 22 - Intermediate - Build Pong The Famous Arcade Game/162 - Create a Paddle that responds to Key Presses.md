## STEP 2 — SINGLE PADDLE WITH KEYBOARD CONTROL (DETAILED GUIDE)

---

## Code Under Discussion

```python
screen.tracer(0)

paddle = Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=5, stretch_len=1)
paddle.penup()
paddle.goto(350, 0)
```

```python
def go_up():
    new_y = paddle.ycor() + 20
    paddle.goto(paddle.xcor(), new_y)

def go_down():
    new_y = paddle.ycor() - 20
    paddle.goto(paddle.xcor(), new_y)
```

```python
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
```

```python
game_is_on = True
while game_is_on:
    screen.update()
```

---

## Paddle Creation & Configuration

### `paddle = Turtle()`

**What**

* Creates a turtle object representing a paddle.

**Why**

* Turtle objects are movable shapes.
* Perfect for paddles and balls in simple arcade games.

---

### `paddle.shape("square")`

**What**

* Sets the base shape to a square (20×20 pixels).

**Why**

* Paddle shape starts as a square so it can be stretched.
* Square scaling is predictable and consistent.

---

### `paddle.color("white")`

**What**

* Sets paddle color to white.

**Why**

* High contrast against black background.
* Classic Pong visual style.

---

### `paddle.shapesize(stretch_wid=5, stretch_len=1)`

**What**

* Scales the turtle shape:

  * Height → `5 × 20 = 100 pixels`
  * Width → `1 × 20 = 20 pixels`

**Why**

* Pong paddles are tall and thin.
* Vertical stretching enables meaningful collision range.

**Mental Model**

```text
stretch_wid → Y-axis scaling
stretch_len → X-axis scaling
```

---

### `paddle.penup()`

**What**

* Lifts the drawing pen.

**Why**

* Prevents lines from being drawn while moving.
* Game objects should move invisibly, not draw trails.

---

### `paddle.goto(350, 0)`

**What**

* Positions the paddle near the right edge.

**Why**

* Right wall is at `x = +400`
* Placing paddle at `x = 350` leaves:

  * Room for ball collision
  * Prevents partial clipping off-screen

---

## Paddle Movement Functions

---

### `def go_up():`

```python
new_y = paddle.ycor() + 20
paddle.goto(paddle.xcor(), new_y)
```

**What**

* Reads current Y position.
* Adds a fixed movement increment.
* Moves paddle upward.

**Why**

* Paddle movement is discrete and predictable.
* Keeps paddle aligned vertically (X never changes).

---

### `def go_down():`

```python
new_y = paddle.ycor() - 20
paddle.goto(paddle.xcor(), new_y)
```

**What**

* Moves paddle downward using the same logic.

**Why**

* Symmetry ensures balanced control.
* Same speed in both directions.

---

## Keyboard Event Binding

---

### `screen.listen()`

**What**

* Tells the screen to start listening for keyboard input.

**Why**

* Without this, key presses are ignored.

---

### `screen.onkey(go_up, "Up")`

**What**

* Maps the **Up Arrow key** to `go_up()`.

**Why**

* Event-driven control avoids blocking loops.
* Function executes only when key is pressed.

---

### `screen.onkey(go_down, "Down")`

**What**

* Maps the **Down Arrow key** to `go_down()`.

**Why**

* Clean separation between input and movement logic.

---

## Game Loop (Manual Rendering)

---

### `game_is_on = True`

**What**

* Boolean flag controlling the game loop.

**Why**

* Enables clean exit later (game over, quit condition).

---

### `while game_is_on:`

```python
screen.update()
```

**What**

* Infinite loop that refreshes the screen manually.

**Why**

* Required because `screen.tracer(0)` disables auto-rendering.
* All movement becomes visible only after `screen.update()`.

**Current Behavior**

* Paddle moves only when keys are pressed.
* Screen refreshes continuously.

---

## What Is Missing (Intentionally)

| Missing Element | Reason                    |
| --------------- | ------------------------- |
| Boundary checks | Introduced in later steps |
| Ball logic      | Not implemented yet       |
| Second paddle   | Step 3                    |
| Frame delay     | Speed control added later |

---

## Hidden Behavior Explained

> Key presses work **inside the while loop**
> Turtle internally handles event callbacks
> Loop only controls screen rendering, not input

---

## Coordinate Safety (Important)

Current paddle limits:

```text
Top boundary    = +300
Bottom boundary = -300
Paddle height   = ~100
```

Without boundary checks:

* Paddle can move off-screen
* This will be fixed in the next refinement

---

## Conceptual Flow at This Stage

> Initialize screen
> Create paddle
> Listen for key input
> On key press → move paddle
> Loop updates screen continuously

This step confirms **input → movement → rendering** is working correctly and sets the foundation for object-oriented paddles and collision logic.
