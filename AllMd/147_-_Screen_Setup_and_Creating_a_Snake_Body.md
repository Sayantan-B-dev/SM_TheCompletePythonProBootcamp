## STEP 1 — SCREEN SETUP & INITIAL SNAKE BODY

**Code Explanation (Part-by-Part + Logic)**

---

## IMPORTING CORE COMPONENTS

```python
from turtle import Turtle, Screen
```

**What this does**

* Imports two core classes from the `turtle` module.
* `Screen` → controls the game window.
* `Turtle` → represents drawable objects (snake segments in this case).

**Why this is needed**

* Turtle graphics are object-oriented.
* Each snake segment is an independent turtle object.

---

## CREATING THE GAME WINDOW

```python
screen = Screen()
```

**What**

* Instantiates a screen object.
* This object represents the canvas where everything is drawn.

**Why**

* All visual configuration and event handling happens through this object.
* Without it, nothing can be displayed.

---

## CONFIGURING SCREEN DIMENSIONS

```python
screen.setup(width=600, height=600)
```

**What**

* Sets window size to 600 × 600 pixels.

**Why**

* Square window is ideal for grid-based movement.
* Consistent dimensions simplify collision logic later.

**Hidden Detail**

* Turtle coordinates default to the center `(0, 0)`.
* So the usable coordinate range becomes roughly:

  * X: `-300 → +300`
  * Y: `-300 → +300`

---

## SETTING BACKGROUND COLOR

```python
screen.bgcolor("black")
```

**What**

* Sets the background color to black.

**Why**

* High contrast with white snake segments.
* Reduces visual noise.
* Common arcade-style aesthetic.

---

## SETTING WINDOW TITLE

```python
screen.title("My Snake Game")
```

**What**

* Sets the title text in the window’s title bar.

**Why**

* Helps identify the application.
* Useful when multiple windows are open.

---

## DEFINING INITIAL SNAKE POSITIONS

```python
starting_positions = [(0, 0), (-20, 0), (-40, 0)]
```

**What**

* A list of `(x, y)` coordinate tuples.
* Each tuple represents one snake segment’s position.

**Why these values**

* Each segment is spaced **20 pixels apart**.
* Default turtle square size ≈ 20×20 pixels.
* Prevents overlap and creates a clean body chain.

**Order Importance**

* First tuple → head
* Remaining tuples → body segments behind the head

---

## CREATING SNAKE SEGMENTS (LOOP)

```python
for position in starting_positions:
```

**What**

* Iterates over each coordinate pair.
* One loop iteration = one snake segment.

**Why a loop**

* Avoids repetitive code.
* Makes snake length easily adjustable later.

---

## CREATING A SEGMENT OBJECT

```python
new_segment = Turtle(shape="square")
```

**What**

* Creates a new turtle object.
* Shape is explicitly set to `"square"`.

**Why**

* Snake segments are square blocks.
* Matches classic Snake game visuals.

**Important Detail**

* Each segment is a **separate object**, not a drawing.

---

## SETTING SEGMENT COLOR

```python
new_segment.color("white")
```

**What**

* Sets the segment color to white.

**Why**

* White contrasts sharply with black background.
* Clear visibility for movement and collisions.

---

## POSITIONING THE SEGMENT

```python
new_segment.goto(position)
```

**What**

* Moves the segment to a specific `(x, y)` coordinate.

**Why**

* Precisely places segments in a straight horizontal line.
* Establishes the initial snake body shape.

**Key Insight**

* `goto()` does **not** animate here.
* Turtle starts instantly at the given position.

---

## KEEPING THE WINDOW OPEN

```python
screen.exitonclick()
```

**What**

* Keeps the window open until the user clicks.

**Why**

* Prevents the program from exiting immediately.
* Useful during early visual testing.

---

## EXPECTED OUTPUT (VISUAL RESULT)

```
• A 600x600 black window opens
• Three white square blocks appear
• Blocks are aligned horizontally
• Positions:
  (0, 0)     → head
  (-20, 0)   → body
  (-40, 0)   → tail
• No movement yet
```

---

## LOGICAL STATE AFTER STEP 1

| Element                  | Status                    |
| ------------------------ | ------------------------- |
| Screen initialized       | Yes                       |
| Snake visible            | Yes                       |
| Segments aligned         | Yes                       |
| Movement logic           | Not yet                   |
| Data structure for snake | Implicit (not stored yet) |

---
