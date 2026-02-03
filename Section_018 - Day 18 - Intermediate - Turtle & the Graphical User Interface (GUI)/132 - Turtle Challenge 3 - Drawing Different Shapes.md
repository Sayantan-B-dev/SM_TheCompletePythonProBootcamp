## Imports and Aliases

```python
import turtle as t
from random import choice
```

| Item          | Meaning         | Why Used                             |
| ------------- | --------------- | ------------------------------------ |
| `turtle as t` | Module alias    | Shorter, cleaner access (`t.Turtle`) |
| `choice`      | Random selector | Pick random color per shape          |

---

## Turtle Setup

```python
tim = t.Turtle()
tim.speed(5)
tim.width(3)
tim.hideturtle()
```

| Line           | Purpose                |
| -------------- | ---------------------- |
| `Turtle()`     | Creates drawing object |
| `speed(5)`     | Medium animation speed |
| `width(3)`     | Thicker lines          |
| `hideturtle()` | Clean output           |

---

## Color Palette

```python
color = ["red","blue","green","purple","orange","cyan"]
```

Used only for **visual variation**, not logic.

---

## Shape-Drawing Function

```python
def draw_shape(num_sides):
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(360 / num_sides)
```

### Key Logic

| Concept           | Explanation                       |
| ----------------- | --------------------------------- |
| `num_sides`       | Controls polygon type             |
| `360 / num_sides` | Exterior angle of regular polygon |
| Loop count        | One side per iteration            |

Example:

* `num_sides = 3` → triangle
* `num_sides = 4` → square
* `num_sides = 8` → octagon

---

## Main Drawing Loop

```python
for shape_side in range(3, 11):
    tim.color(choice(color))
    draw_shape(shape_side)
```

| Part            | Meaning                         |
| --------------- | ------------------------------- |
| `range(3, 11)`  | Shapes from triangle to decagon |
| `choice(color)` | Random color each shape         |
| `draw_shape()`  | Draws polygon                   |

Important behavior:

* All shapes share the **same center**
* Orientation accumulates naturally
* Only color changes between shapes

---

## Program End

```python
turtle.done()
```

Keeps the window open after drawing.

---

## Expected Output

```
• Series of regular polygons:
    - Triangle (3 sides)
    - Square (4 sides)
    - ...
    - Decagon (10 sides)
• Each polygon:
    - Same size
    - Random color
• Turtle cursor hidden
• Shapes drawn sequentially
```

---

## Core Idea to Remember

> Regular polygons are created by
> **equal forward movement + constant angle = 360 / sides**

This pattern generalizes to **all polygon-based turtle drawings**.
