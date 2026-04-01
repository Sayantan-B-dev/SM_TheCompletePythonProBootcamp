## STEP 7 — BALL OUT-OF-BOUNDS & RESET LOGIC

---

## Purpose of This Step

> Detect when a paddle **fails to hit the ball**,
> reset the rally, and prepare for score handling.

This step defines **what happens when a point ends**.

---

## `ball.py` — Reset Logic

### Code Under Discussion

```python
def reset_position(self):
    self.goto(0, 0)
    self.bounce_x()
```

---

## Why Reset Logic Belongs in the Ball Class

* The ball owns:

  * Its position
  * Its direction
* Main game loop only **detects conditions**
* Ball decides **how to reset**

This maintains clean responsibility boundaries.

---

## Breakdown of `reset_position()`

### `self.goto(0, 0)`

**What**

* Instantly moves the ball back to the center of the screen.

**Why**

* Center is neutral starting position.
* Ensures fair restart for both players.

---

### `self.bounce_x()`

**What**

* Reverses horizontal direction after reset.

**Why**

* Prevents ball from restarting toward the same losing side.
* Ensures alternating serve direction.

**Conceptual Effect**

```text
Miss by right paddle → ball moves left next
Miss by left paddle  → ball moves right next
```

---

## Main Game Loop — Out-of-Bounds Detection

### Code Under Discussion

```python
# Detect when right paddle misses
if ball.xcor() > 380:
    ball.reset_position()

# Detect when left paddle misses
if ball.xcor() < -380:
    ball.reset_position()
```

---

## Why `380` Is Used (Boundary Math)

```text
Screen width  = 800
Right wall    = +400
Left wall     = -400
Ball size     ≈ 20
```

Safe miss detection:

```text
400 - 20 = 380
```

This ensures:

* Ball is fully past the paddle
* Miss is clearly intentional
* No premature reset

---

## Miss Detection Algorithm

> Read ball X position
> → Check beyond horizontal boundary
> → Trigger reset

This logic runs **every frame**, ensuring instant detection.

---

## Timeline of a Miss Event

| Step | Event                    |
| ---- | ------------------------ |
| 1    | Ball passes paddle       |
| 2    | X position exceeds ±380  |
| 3    | Reset triggered          |
| 4    | Ball teleports to center |
| 5    | Direction reverses       |
| 6    | New rally begins         |

---

## Important Behavior Note

At this stage:

* No score is recorded yet
* Ball speed is not reset
* Only direction and position change

This is intentional to keep logic incremental.

---

## Potential Issue (Expected & Acceptable)

> If ball speed increases later,
> it may skip directly from inside → beyond boundary.

Solution later:

* Clamp speed
* Or check with a wider boundary buffer

---

## Common Beginner Errors Avoided

> Resetting ball without reversing direction
> Using wall boundary instead of paddle boundary
> Mixing scoring logic into ball class
> Destroying and recreating ball object

---

## Architectural State After Step 7

| System         | Status      |
| -------------- | ----------- |
| Ball movement  | Active      |
| Wall bounce    | Implemented |
| Paddle bounce  | Implemented |
| Miss detection | Implemented |
| Scoring        | Next step   |

---

## Mental Model Going Forward

> **Hit → bounce**
> **Miss → reset**
> **Score → external system**

This step completes the rally lifecycle and prepares the game for the final layer: scoring and difficulty scaling.
