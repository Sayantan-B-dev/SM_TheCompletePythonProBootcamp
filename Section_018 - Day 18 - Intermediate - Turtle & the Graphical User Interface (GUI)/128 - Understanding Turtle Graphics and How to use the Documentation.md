## Turtle Graphics — Conceptual Model

> Turtle graphics is a **state-based drawing system**.
> A virtual “turtle” moves on a 2D canvas while maintaining **position**, **direction (heading)**, **pen state**, and **style**.

Internal state tracked at all times:

* Current `(x, y)` position
* Current heading (angle in degrees)
* Pen state (up / down)
* Pen attributes (color, width, speed)

---

## Core Execution Flow

```
Initialize Screen
↓
Create Turtle
↓
Issue Movement / Drawing Commands
↓
Turtle Updates State + Draws
↓
Event Loop Keeps Window Open
```

Important behavior:

* Code executes **top to bottom**
* Each command mutates turtle state
* Drawing happens immediately after movement commands

---

## Coordinate System Used by Turtle

| Concept         | Value                     |
| --------------- | ------------------------- |
| Origin          | `(0, 0)` center of screen |
| +X axis         | Right                     |
| -X axis         | Left                      |
| +Y axis         | Up                        |
| -Y axis         | Down                      |
| Default heading | `0°` (facing right)       |
| Angle direction | Counter-clockwise         |

---

## Turtle Initialization Methods

| Method                  | Purpose               | Notes                  |
| ----------------------- | --------------------- | ---------------------- |
| `turtle.Turtle()`       | Create turtle object  | Required to draw       |
| `turtle.Screen()`       | Create drawing window | Manages canvas         |
| `screen.setup(w, h)`    | Set window size       | Pixels                 |
| `screen.bgcolor(color)` | Background color      | String or RGB          |
| `screen.title(text)`    | Window title          | Optional               |
| `screen.exitonclick()`  | Close on click        | Prevents instant close |

### Example

```python
import turtle

screen = turtle.Screen()
screen.setup(600, 400)
screen.bgcolor("black")
screen.title("Turtle Basics")

t = turtle.Turtle()
screen.exitonclick()
```

**Expected Output**

```
Black window opens (600x400)
White turtle arrow appears at center
Window closes on mouse click
```

---

## Movement Methods (Position Control)

| Method                   | Purpose             | State Affected     |
| ------------------------ | ------------------- | ------------------ |
| `forward(d)` / `fd(d)`   | Move forward        | Position           |
| `backward(d)` / `bk(d)`  | Move backward       | Position           |
| `left(angle)` / `lt(a)`  | Turn left           | Heading            |
| `right(angle)` / `rt(a)` | Turn right          | Heading            |
| `goto(x, y)`             | Move to coordinates | Position           |
| `setx(x)`                | Change x only       | Position           |
| `sety(y)`                | Change y only       | Position           |
| `home()`                 | Return to origin    | Position + heading |

### Example: Square

```python
import turtle

t = turtle.Turtle()

for _ in range(4):
    t.forward(100)
    t.left(90)

turtle.done()
```

**Expected Output**

```
A perfect square drawn with 4 equal sides
```

---

## Pen Control Methods (Drawing Control)

| Method               | Purpose             | Typical Use          |
| -------------------- | ------------------- | -------------------- |
| `penup()` / `pu()`   | Lift pen            | Move without drawing |
| `pendown()` / `pd()` | Lower pen           | Resume drawing       |
| `pensize(w)`         | Line thickness      | Emphasis             |
| `pencolor(c)`        | Pen color           | Styling              |
| `fillcolor(c)`       | Fill color          | Shapes               |
| `begin_fill()`       | Start fill region   | Before shape         |
| `end_fill()`         | Fill shape          | After shape          |
| `clear()`            | Clear drawing       | Keep turtle          |
| `reset()`            | Clear + reset state | Full reset           |

### Example: Filled Triangle

```python
import turtle

t = turtle.Turtle()
t.fillcolor("blue")
t.begin_fill()

for _ in range(3):
    t.forward(100)
    t.left(120)

t.end_fill()
turtle.done()
```

**Expected Output**

```
A solid blue equilateral triangle
```

---

## Appearance & Speed Control

| Method         | Purpose          | Values                      |
| -------------- | ---------------- | --------------------------- |
| `shape()`      | Turtle shape     | "arrow", "turtle", "circle" |
| `shapesize()`  | Size scaling     | Stretch factors             |
| `speed()`      | Animation speed  | 0–10                        |
| `hideturtle()` | Hide turtle icon | Clean drawings              |
| `showturtle()` | Show turtle      | Debugging                   |

### Example: Fast Drawing

```python
import turtle

t = turtle.Turtle()
t.speed(0)      # Fastest
t.hideturtle()

for i in range(36):
    t.forward(100)
    t.left(170)

turtle.done()
```

**Expected Output**

```
Complex star-like geometric pattern drawn instantly
```

---

## Position & State Query Methods

| Method       | Returns      | Use Case        |
| ------------ | ------------ | --------------- |
| `position()` | `(x, y)`     | Debugging       |
| `xcor()`     | X coordinate | Alignment       |
| `ycor()`     | Y coordinate | Alignment       |
| `heading()`  | Angle        | Direction logic |
| `isdown()`   | True / False | Pen state       |

### Example: Reading Position

```python
import turtle

t = turtle.Turtle()
t.forward(150)

print(t.position())
print(t.heading())

turtle.done()
```

**Expected Output**

```
(150.00, 0.00)
0.0
```

---

## Shape Drawing Shortcuts

| Shape   | Logic                |
| ------- | -------------------- |
| Circle  | Radius-based         |
| Polygon | Angle = 360 / sides  |
| Spiral  | Incremental movement |

### Example: Circle

```python
import turtle

t = turtle.Turtle()
t.circle(80)

turtle.done()
```

**Expected Output**

```
A circle with radius 80 pixels
```

---

## Event Handling (Interactive Turtle)

| Method             | Purpose            |
| ------------------ | ------------------ |
| `onclick(func)`    | Mouse click events |
| `onkey(func, key)` | Keyboard input     |
| `listen()`         | Enable keyboard    |

### Example: Keyboard Control

```python
import turtle

t = turtle.Turtle()
screen = turtle.Screen()

def move_forward():
    t.forward(20)

screen.listen()
screen.onkey(move_forward, "Up")

turtle.done()
```

**Expected Output**

```
Pressing UP arrow moves turtle forward
```

---

## Common Beginner Pitfalls

| Problem                 | Cause                               |
| ----------------------- | ----------------------------------- |
| Window closes instantly | Missing `done()` or `exitonclick()` |
| No drawing              | Pen lifted                          |
| Strange angles          | Forgetting heading reset            |
| Slow rendering          | Speed too low                       |

---

## Real Use Cases of Turtle Graphics

| Domain                  | Purpose              |
| ----------------------- | -------------------- |
| Education               | Geometry + loops     |
| Algorithm visualization | Pathfinding          |
| Art                     | Generative designs   |
| Logic building          | Coordinate reasoning |
| Robotics concepts       | Directional movement |

---

## Mental Model to Remember

> Turtle does **exactly** what you tell it,
> **from its current state**,
> **relative to its heading**,
> **one command at a time**.

Understanding turtle means understanding **state, flow, and geometry**.
