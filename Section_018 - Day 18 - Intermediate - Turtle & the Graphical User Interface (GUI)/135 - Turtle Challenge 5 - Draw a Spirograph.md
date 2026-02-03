## Imports and Aliases

```python
import turtle as t
from random import randint
```

| Item          | Purpose                           |
| ------------- | --------------------------------- |
| `turtle as t` | Short alias for turtle graphics   |
| `randint`     | Generates random integers for RGB |

---

## Screen and Turtle Setup

```python
screen = t.Screen()

tim = t.Turtle()
tim.speed(0)
tim.pensize(2)
tim.hideturtle()
```

| Setting        | Meaning                |
| -------------- | ---------------------- |
| `Screen()`     | Creates drawing window |
| `speed(0)`     | Fastest drawing        |
| `pensize(2)`   | Thin, clean lines      |
| `hideturtle()` | Hides cursor           |

---

## Enabling RGB Color Mode

```python
t.colormode(255)
```

Required so turtle accepts colors as `(R, G, B)` tuples where each value is `0–255`.

---

## Random RGB Color Generator

```python
def random_rgb_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)
```

| Aspect      | Explanation                      |
| ----------- | -------------------------------- |
| Return type | Tuple `(r, g, b)`                |
| Why tuple   | Fixed-size, immutable color unit |
| Range       | Valid RGB intensity values       |

---

## Spirograph Drawing Function

```python
def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tim.color(random_rgb_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)
```

### Core Logic

| Step                | What Happens                     |
| ------------------- | -------------------------------- |
| `360 / size_of_gap` | Number of circles needed         |
| `circle(100)`       | Draws one full circle            |
| `setheading(...)`   | Rotates turtle slightly          |
| Random color        | Each circle gets a new RGB color |

Geometric insight:

* A full rotation is `360°`
* Each loop rotates by `size_of_gap`
* Circles overlap evenly, forming a spirograph

---

## Function Call

```python
draw_spirograph(5)
```

| Value      | Effect                        |
| ---------- | ----------------------------- |
| `5`        | Small gap → dense spirograph  |
| Larger gap | Fewer circles, looser pattern |

---

## Program Exit Control

```python
screen.exitonclick()
```

Keeps the window open until the user clicks.

---

## Expected Output

```
• Circular spirograph pattern
• Many overlapping circles
• Each circle has a random RGB color
• Smooth, symmetric design
• Fast, flicker-free rendering
```

---

## Core Insight

> A spirograph is created by
> **repeating the same shape**
> while **rotating by a constant angle**

Random color + fixed geometry = structured generative art.
