## STEP 6 — BALL ↔ PADDLE COLLISION (HORIZONTAL BOUNCE)

---

## `ball.py` — Horizontal Bounce Logic

### Code Under Discussion

```python
def bounce_x(self):
    self.x_move *= -1
```

---

## Why `bounce_x()` Exists

### Conceptual Separation

* `x_move` controls **horizontal direction and speed**
* Flipping its sign reverses left ↔ right movement

**Mental Model**

```text
x_move > 0  → ball moving right
x_move < 0  → ball moving left
```

After bounce:

```text
direction flips, speed remains same
```

This mirrors real Pong behavior:

> paddles affect **horizontal motion**, not vertical.

---

## Collision Detection With Paddles (Main File)

### Code Under Discussion

```python
# Detect ball collision with right paddle
if ball.distance(r_paddle) < 50 and ball.xcor() > 320:
    ball.bounce_x()

# Detect ball collision with left paddle
if ball.distance(l_paddle) < 50 and ball.xcor() < -320:
    ball.bounce_x()
```

---

## Why Two Conditions Are Required

### 1. `ball.distance(paddle) < 50`

**What**

* Measures Euclidean distance between ball and paddle center.

**Why**

* Simple collision detection without complex geometry.
* Paddle height ≈ 100 px
* Ball size ≈ 20 px

A threshold of `50` ensures:

* Ball is close enough vertically
* Ball overlaps paddle hit zone

---

### 2. `ball.xcor() > 320` / `< -320`

**What**

* Confirms the ball is **on the correct side of the screen**.

**Why**

* Prevents false collisions when ball is near paddle vertically
* Ensures collision only triggers when ball reaches paddle face

---

## Why `320` Is Used (Boundary Math)

```text
Right paddle X ≈ +350
Left paddle X  ≈ -350
Ball size      ≈ 20
```

Collision buffer:

```text
350 - 30 = 320
```

This:

* Prevents visual overlap glitches
* Ensures bounce happens before clipping

---

## Combined Collision Algorithm (Logical Flow)

> Check proximity (distance)
> → Confirm correct horizontal side
> → Reverse horizontal direction

Both checks must pass to trigger bounce.

---

## What Happens After Collision

Assume:

```text
Before hit → x_move = +10 (moving right)
```

After:

```python
self.x_move *= -1
```

Result:

```text
After hit → x_move = -10 (moving left)
```

Ball continues with:

* Same vertical motion
* Same speed
* Opposite horizontal direction

---

## Frame-Level Timeline Example

| Frame | X Pos | Distance | Condition       | Result    |
| ----- | ----- | -------- | --------------- | --------- |
| N     | 315   | 48       | Near paddle     | No bounce |
| N+1   | 325   | 45       | Conditions met  | bounce_x  |
| N+2   | 315   | —        | Moving opposite | Correct   |

---

## Why This Logic Is Stable

* Direction flip occurs once per contact
* X-position constraint prevents repeated flips
* Distance check handles vertical alignment

---

## Known Limitations (Acceptable at This Stage)

| Limitation         | Explanation                             |
| ------------------ | --------------------------------------- |
| No angle variation | Ball always reflects symmetrically      |
| No speed change    | Difficulty not scaling yet              |
| No debounce        | High speed could cause double collision |

These are intentionally deferred.

---

## Common Mistakes Avoided

> Bouncing on Y instead of X
> Using only distance check (causes ghost collisions)
> Checking collision without X-bound constraint
> Resetting ball instead of reversing direction

---

## Architectural Progress

| Component | Responsibility           |
| --------- | ------------------------ |
| Ball      | Owns bounce mechanics    |
| Main loop | Detects collision timing |
| Paddle    | Passive collision target |

---

## Mental Model Going Forward

> **Walls flip Y**
> **Paddles flip X**
> **Distance = hit validation**
> **X-bound = side validation**

This step completes the core Pong physics loop and makes rallies possible. The next steps build on this by handling misses, scoring, and speed scaling.
