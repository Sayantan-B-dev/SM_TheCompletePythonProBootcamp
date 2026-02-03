## STEP 3 — MOVING TO OOP (SNAKE CLASS)

**Detailed explanation of structure, responsibilities, and logic**

---

## IMPORTING THE REQUIRED CLASS

```python
from turtle import Turtle
```

**What**

* Imports only the `Turtle` class.

**Why**

* The `Snake` class is responsible only for snake behavior.
* Screen setup and game loop stay outside this class.
* This separation follows clean architecture principles.

---

## CONFIGURATION CONSTANTS

```python
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
```

### STARTING_POSITIONS

**Purpose**

* Defines the initial body layout of the snake.

**Why constants**

* Prevents magic numbers inside methods.
* Makes adjustments safer and centralized.
* Allows reuse during reset logic later.

### MOVE_DISTANCE

**Purpose**

* Defines how far the snake moves per frame.

**Why 20**

* Matches the turtle square size.
* Keeps movement aligned to a grid.
* Prevents partial overlap and drifting.

---

## DEFINING THE SNAKE CLASS

```python
class Snake:
```

**What**

* Creates a blueprint for snake objects.

**Why a class**

* Snake has:

  * **State** → segments, head
  * **Behavior** → create body, move
* OOP bundles these together logically.

---

## INITIALIZATION METHOD

```python
def __init__(self):
```

**What**

* Runs automatically when a `Snake` object is created.

**Why**

* Sets up the snake once at creation.
* Prevents reliance on external setup logic.

---

### INITIALIZING SEGMENT STORAGE

```python
self.segments = []
```

**What**

* Creates an empty list owned by this snake instance.

**Why**

* Each snake object manages its own body.
* Enables multiple snakes if needed (AI, multiplayer).

---

### CREATING THE INITIAL BODY

```python
self.create_snake()
```

**What**

* Calls an internal method to build the snake.

**Why**

* Keeps `__init__` clean and readable.
* Creation logic can be reused (e.g., reset game).

---

### DEFINING THE HEAD REFERENCE

```python
self.head = self.segments[0]
```

**What**

* Stores a direct reference to the first segment.

**Why**

* Head is accessed frequently.
* Avoids repeatedly writing `self.segments[0]`.
* Improves readability and intent clarity.

**Design Insight**

* The head is the only segment that decides direction.

---

## CREATING THE SNAKE BODY

```python
def create_snake(self):
```

**Responsibility**

* Build the initial snake body from predefined positions.

---

### ITERATING THROUGH POSITIONS

```python
for position in STARTING_POSITIONS:
```

**What**

* Loops through each coordinate tuple.

**Why**

* Makes the body length configurable.
* Avoids hardcoding segment creation.

---

### CREATING A SEGMENT

```python
new_segment = Turtle(shape="square")
```

**What**

* Instantiates a turtle object.

**Why**

* Each segment must be independently movable.
* Shape matches classic snake visuals.

---

### VISUAL CONFIGURATION

```python
new_segment.color("white")
```

**Why**

* Ensures consistent appearance.
* Visual clarity against dark background.

---

### DISABLING DRAWING

```python
new_segment.penup()
```

**Critical Detail**

* Prevents lines when the segment moves.

**Why**

* Snake movement should not leave trails.
* Ensures clean animation.

---

### POSITIONING THE SEGMENT

```python
new_segment.goto(position)
```

**What**

* Places the segment at its initial coordinate.

**Why**

* Establishes spacing and direction.
* Aligns body horizontally.

---

### REGISTERING THE SEGMENT

```python
self.segments.append(new_segment)
```

**What**

* Adds the segment to the snake’s body list.

**Why**

* Preserves order (head → tail).
* Required for movement logic.

---

## MOVEMENT METHOD

```python
def move(self):
```

**Responsibility**

* Advance the snake forward by one frame.

---

## BACKWARD ITERATION THROUGH BODY

```python
for seg_num in range(len(self.segments) - 1, 0, -1):
```

**What**

* Iterates from tail toward the head (excluding head).

**Why backward**

* Prevents overwriting positions.
* Ensures each segment copies the one in front of it.

**Conceptual Flow**

```
tail → body → neck → (head excluded)
```

---

## COPYING PREVIOUS POSITION

```python
new_x = self.segments[seg_num - 1].xcor()
new_y = self.segments[seg_num - 1].ycor()
```

**What**

* Reads coordinates of the segment ahead.

**Why**

* Implements the “follow the leader” behavior.
* Preserves perfect alignment.

---

## MOVING CURRENT SEGMENT

```python
self.segments[seg_num].goto(new_x, new_y)
```

**What**

* Moves the current segment to the captured position.

**Why**

* Ensures rigid snake body.
* Avoids diagonal drift or interpolation errors.

---

## MOVING THE HEAD

```python
self.head.forward(MOVE_DISTANCE)
```

**What**

* Moves only the head forward.

**Why**

* Head is the leader.
* Body movement is derived, not independent.
* Direction control will later modify only the head.

---

## COMPLETE MOVEMENT ALGORITHM (ABSTRACT)

> 1. Start from the tail
> 2. Each segment moves to where the one ahead was
> 3. Head moves forward by fixed distance
> 4. Frame ends

---

## STATE AFTER STEP 3

| Aspect                   | Status  |
| ------------------------ | ------- |
| Snake logic encapsulated | Yes     |
| Body stored internally   | Yes     |
| Head abstraction         | Yes     |
| Movement reusable        | Yes     |
| Direction control        | Not yet |
| Food / collision         | Not yet |

---