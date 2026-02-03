## Imports and Aliases

```python
import turtle as t
from random import choice
```

| Item          | Purpose                       |
| ------------- | ----------------------------- |
| `turtle as t` | Short alias for turtle module |
| `choice`      | Random selection from a list  |

---

## Turtle Initialization

```python
tim = t.Turtle()
tim.speed(0)
tim.width(3)
tim.hideturtle()
tim.pensize(10)
```

| Setting        | Effect                      |
| -------------- | --------------------------- |
| `speed(0)`     | Fastest possible drawing    |
| `width(3)`     | Base outline width          |
| `pensize(10)`  | Thick stroke for visibility |
| `hideturtle()` | Hides cursor                |

Note:
`pensize(10)` overrides `width(3)` — the **last call wins**.

---

## Configuration Data

```python
color = ["red","blue","green","purple","orange","cyan"]
direction = [0, 90, 180, 270]
```

| Variable    | Meaning                                     |
| ----------- | ------------------------------------------- |
| `color`     | Possible pen colors                         |
| `direction` | Cardinal directions (right, up, left, down) |

Angle meaning:

* `0°` → right
* `90°` → up
* `180°` → left
* `270°` → down

---

## Main Drawing Loop

```python
for _ in range(200):
    tim.color(choice(color))
    tim.forward(55)
    tim.setheading(choice(direction))
```

### Logic Breakdown

| Step           | What Happens        |
| -------------- | ------------------- |
| Random color   | Visual variation    |
| `forward(55)`  | Draws one segment   |
| `setheading()` | Forces a sharp turn |

Key behavior:

* Movement is always **axis-aligned**
* No diagonal lines are possible
* Each step is independent of the previous heading

---

## Pattern Generated

| Property  | Result                   |
| --------- | ------------------------ |
| Geometry  | Grid-like random walk    |
| Turns     | Sharp 90° turns only     |
| Thickness | Bold, marker-style lines |
| Speed     | Instant rendering        |

This is a classic **random walk with constrained directions**, often called a *Manhattan walk*.

---

## Program End

```python
turtle.done()
```

Keeps the window open after drawing completes.

---

## Expected Output

```
• Dense abstract pattern
• Thick, straight line segments
• Random color changes
• Only vertical and horizontal movement
• No turtle cursor visible
```

---

## Core Insight

> Randomness comes from **direction and color**,
> structure comes from **restricted angles**.

This balance creates controlled chaos rather than noise.
