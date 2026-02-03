## SNAKE BODY STORAGE & MOVEMENT LOGIC

**Line-by-line explanation with algorithmic reasoning**

---

## STORING SNAKE SEGMENTS

```python
segments = []
```

**What**

* Creates an empty list.

**Why**

* This list becomes the **single source of truth** for the snake’s body.
* Order matters:

  * `segments[0]` → head
  * last index → tail

**Design Reason**

* Movement depends on knowing **who follows whom**.
* Lists preserve order and allow reverse iteration.

---

## CREATING & REGISTERING EACH SEGMENT

```python
for position in starting_positions:
```

**What**

* Iterates through predefined coordinates.

**Why**

* Allows flexible snake length without rewriting logic.

---

```python
new_segment = Turtle(shape="square")
```

**What**

* Creates a new turtle object representing one body block.

**Why**

* Each segment must be independent to move individually.

---

```python
new_segment.color("white")
```

**What**

* Sets the visual color of the segment.

**Why**

* High contrast against dark background.
* Visual clarity during motion.

---

```python
new_segment.penup()
```

**What**

* Disables drawing when the turtle moves.

**Why this is critical**

* Without `penup()`, the snake would leave lines behind while moving.
* Snake motion should look like **teleporting blocks**, not drawing paths.

---

```python
new_segment.goto(position)
```

**What**

* Places the segment at its initial coordinate.

**Why**

* Precisely aligns segments with equal spacing.
* Establishes a straight initial body.

---

```python
segments.append(new_segment)
```

**What**

* Adds the newly created segment to the list.

**Why**

* Registers the segment so it can participate in movement.
* Order of insertion defines head-to-tail sequence.

---

## GAME LOOP CONTROL FLAG

```python
game_is_on = True
```

**What**

* Boolean variable controlling the main loop.

**Why**

* Allows the game to be stopped later (collision, quit event).
* Cleaner than `while True`.

---

## MAIN GAME LOOP (FRAME LOOP)

```python
while game_is_on:
```

**What**

* Infinite loop that drives animation.

**Why**

* Games run in frames, not one-time execution.
* Each loop iteration = one frame.

---

## MANUAL SCREEN REFRESH

```python
screen.update()
```

**What**

* Forces the screen to redraw manually.

**Why**

* Screen tracer is assumed to be off.
* Prevents flickering.
* Gives full control over when visuals update.

---

## SPEED CONTROL

```python
time.sleep(0.1)
```

**What**

* Pauses execution for 0.1 seconds.

**Why**

* Controls snake speed.
* Smaller value → faster snake.
* Larger value → slower snake.

**Game Design Insight**

* Speed is part of difficulty scaling later.

---

## CORE MOVEMENT LOGIC (FOLLOWING BEHAVIOR)

```python
for seg_num in range(len(segments) - 1, 0, -1):
```

**What**

* Iterates **backwards** through the segments list.
* Starts from the tail and stops before the head.

**Why backward iteration is mandatory**

* Prevents overwriting positions.
* Ensures each segment copies the position of the one ahead of it.

**Index Flow Example**

```
segments = [head, body1, body2, tail]

Iteration order:
tail → body2 → body1
```

---

## CAPTURING PREVIOUS SEGMENT POSITION

```python
new_x = segments[seg_num - 1].xcor()
new_y = segments[seg_num - 1].ycor()
```

**What**

* Reads the x and y coordinates of the segment **in front**.

**Why**

* Each segment must move to where the previous one was.
* This creates the illusion of continuous motion.

---

## MOVING CURRENT SEGMENT

```python
segments[seg_num].goto(new_x, new_y)
```

**What**

* Teleports the segment to the captured position.

**Why**

* Ensures exact alignment.
* Avoids floating-point drift.
* Keeps snake rigid and grid-aligned.

---

## MOVING THE HEAD FORWARD

```python
segments[0].forward(20)
```

**What**

* Moves the head forward by 20 pixels.

**Why**

* Head is the **leader**.
* Body never decides direction.
* 20 pixels matches segment size → perfect grid movement.

---

## FULL MOVEMENT ALGORITHM (PLAIN LOGIC)

> 1. Pause briefly (speed control)
> 2. From tail to neck:
>
>    * Copy the position of the segment ahead
> 3. Move the head forward
> 4. Redraw the screen
> 5. Repeat

---

## EXPECTED BEHAVIOR (VISIBLE OUTPUT)

```
• Snake moves continuously to the right
• Body follows head perfectly
• No gaps between segments
• No lines drawn on the screen
• Motion appears smooth and unified
```

---
