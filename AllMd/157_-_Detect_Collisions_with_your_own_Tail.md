## DAY 2 — STEP 4

### Detecting Collision With Tail + Snake Extension (Full Technical Validation)

---

## 1. Scope of Step 4

This step completes **two tightly coupled behaviors**:

1. **Snake body extension** when food is eaten
2. **Self-collision detection** (head collides with tail)

This finalizes all core game-ending logic for Snake.

---

## 2. Snake Growth Logic (Extension Mechanism)

### Code Under Review

```python
def create_snake(self):
    for position in STARTING_POSITIONS:
        self.add_segment(position)
```

---

### Purpose

* Initializes the snake body at game start
* Builds segments using predefined coordinates

---

### Algorithm

```
FOR each starting position:
    create a new segment
    place it at that position
    append to segments list
```

---

### Why This Design Is Correct

* Snake body order is preserved
* Head is always `segments[0]`
* Tail is always `segments[-1]`

---

## 3. Segment Creation Logic

```python
def add_segment(self, position):
    new_segment = Turtle(shape="square")
    new_segment.color("white")
    new_segment.penup()
    new_segment.goto(position)
    self.segments.append(new_segment)
```

---

### Step-by-Step Reasoning

| Line                     | Purpose             |
| ------------------------ | ------------------- |
| `Turtle(shape="square")` | Snake body shape    |
| `color("white")`         | Visual consistency  |
| `penup()`                | Prevent drawing     |
| `goto(position)`         | Spawn segment       |
| `append()`               | Maintain body order |

---

### Why `add_segment()` Is Isolated

* Reusable for:

  * Initial snake creation
  * Snake growth during gameplay
* Avoids duplicated logic

---

## 4. Snake Extension Method

```python
def extend(self):
    self.add_segment(self.segments[-1].position())
```

---

### Why This Works

* `self.segments[-1]` → tail segment
* `.position()` → returns `(x, y)` tuple
* New segment spawns exactly on tail

---

### Critical Design Insight

> Overlapping segments are **not visible** because movement occurs in the next frame.

This avoids:

* Visual gaps
* Jumping segments
* Growth glitches

---

### Extension Algorithm

```
GET tail position
CREATE new segment at same position
APPEND to snake body
```

---

## 5. Tail Collision Detection (Main Loop)

### Code Under Review

```python
# Detect collision with tail
for segment in snake.segments:
    if segment == snake.head:
        pass
    elif snake.head.distance(segment) < 10:
        game_is_on = False
        scoreboard.game_over()
```

---

## 6. Tail Collision Algorithm

### Logical Steps

1. Loop through all snake segments
2. Skip the head itself
3. Measure distance from head to each body segment
4. If distance < collision threshold:

   * End game

---

### Pseudocode

```
FOR each segment in snake body:
    IF segment is head:
        ignore
    ELSE IF distance(head, segment) < threshold:
        end game
```

---

## 7. Why Skipping Head Is Mandatory

```python
if segment == snake.head:
    pass
```

### Without this:

* Head always collides with itself
* Game ends instantly

---

### Cleaner Alternative (Conceptual)

```
FOR segment in snake.segments[1:]:
    IF collision detected:
        end game
```

Your current approach is logically correct.

---

## 8. Collision Threshold (`< 10`)

### Why 10 Is Appropriate

| Factor            | Value  |
| ----------------- | ------ |
| Segment size      | ~20 px |
| Overlap threshold | ~10 px |
| Precision         | High   |

Ensures:

* True collisions detected
* Near-misses ignored

---

## 9. Order Dependency (Critical)

Tail collision must be checked:

* After snake movement
* After food collision
* Before next frame

Correct sequence:

```
snake.move()
check food collision
check wall collision
check tail collision
```

---

## 10. Expected Runtime Behavior

### Normal Play

* Snake grows smoothly
* No false collisions

---

### Self-Collision Event

Visual result:

* Snake stops moving
* “GAME OVER” appears
* Final score remains visible

No console output (correct behavior).

---

## 11. Edge Cases (Handled)

| Scenario               | Outcome                    |
| ---------------------- | -------------------------- |
| Short snake            | No tail collision          |
| Immediate growth       | No false collision         |
| Fast movement          | Distance check still valid |
| Multiple body segments | Loop handles all           |

---

## 12. Overall Design Assessment

| Component        | Status  |
| ---------------- | ------- |
| Snake creation   | Correct |
| Growth logic     | Correct |
| Tail collision   | Correct |
| OOP separation   | Correct |
| Game termination | Correct |

---

## 13. Final Day 2 Completion Check

| Step           | Status   |
| -------------- | -------- |
| Food collision | Complete |
| Scoreboard     | Complete |
| Wall collision | Complete |
| Tail collision | Complete |

---
