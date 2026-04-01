## Tuple — What It Is and Why It Matters Here

A **tuple** is an ordered collection of values, similar to a list, but **immutable**.

| Aspect      | Tuple                               | List                 |
| ----------- | ----------------------------------- | -------------------- |
| Syntax      | `( )`                               | `[ ]`                |
| Mutability  | Immutable (cannot change)           | Mutable (can change) |
| Performance | Slightly faster                     | Slightly slower      |
| Safety      | Data cannot be altered accidentally | Data can be modified |

Why tuples are used for RGB colors:

* RGB values represent a **fixed color**
* Once created, `(R, G, B)` should **not change**
* Turtle expects RGB colors as **exact 3-value sequences**
* Tuples clearly express “this is a constant color unit”

---

## RGB Color Concept (Quick)

RGB color is defined as:

```
(Red, Green, Blue)
```

Each value:

* Integer range: `0 → 255`
* `0` = no intensity
* `255` = full intensity

Examples:

* `(255, 0, 0)` → Red
* `(0, 255, 0)` → Green
* `(0, 0, 255)` → Blue

---

## Enabling RGB Mode in Turtle

By default, turtle uses color names.
To use RGB tuples, the color mode must be set.

```python
t.colormode(255)
```

This tells turtle:

> Expect RGB values in the range `0–255`

---

## Small Sample: Random RGB Color Using Tuple

```python
import turtle as t
from random import randint

# setup turtle
tim = t.Turtle()
tim.speed(0)
tim.pensize(5)
tim.hideturtle()

# enable RGB (0–255)
t.colormode(255)

def random_rgb_color():
    """
    Returns a tuple of three random integers.
    Each tuple represents one RGB color.
    """
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)   # tuple

# draw sample lines with random RGB colors
for _ in range(20):
    tim.color(random_rgb_color())
    tim.forward(30)
    tim.right(18)

t.done()
```

---

## Expected Output

```
• Turtle window opens
• 20 connected line segments drawn
• Each segment has a randomly generated RGB color
• Smooth color variation (not limited to named colors)
• Turtle cursor hidden
```

---

## Why Tuple Is the Correct Choice Here

| Reason            | Explanation                      |
| ----------------- | -------------------------------- |
| Fixed size        | RGB must be exactly 3 values     |
| Immutability      | Prevents accidental modification |
| Semantic clarity  | One tuple = one color            |
| API compatibility | Turtle expects RGB as tuple      |

---

## Key Takeaway

> Lists are for **changing collections**
> Tuples are for **fixed meaning data**

RGB colors are fixed units —
that is exactly why **tuples are the right tool** here.
