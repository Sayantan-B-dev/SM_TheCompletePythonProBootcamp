## STEP 5 — BALL BOUNCING OFF TOP & BOTTOM WALLS (DETAILED GUIDE)

---

## `ball.py` — Vertical Bounce Logic

### Code Under Discussion

```python
def bounce_y(self):
    self.y_move *= -1
```

---

## Why `y_move` Exists (Conceptual Shift)

### Before (Step 4)

* Ball movement was:

  * Hardcoded
  * Always moving `+10` in Y direction

### Now (Step 5)

* Movement is **direction-based**, not fixed.
* `y_move` represents:

  * Direction (`+` or `-`)
  * Speed magnitude

**Mental Model**

```text
y_move > 0  → moving upward
y_move < 0  → moving downward
```

Multiplying by `-1` flips direction **without changing speed**.

---

## Why Bounce Logic Belongs in the Ball Class

> The ball should know **how it bounces**,
> not the main game loop.

* Encapsulation:

  * `main.py` decides *when* to bounce
  * `ball.py` decides *how* to bounce

This separation keeps logic clean and scalable.

---

## Wall Collision Detection (Main File)

### Code Under Discussion

```python
# Detect ball collision with top and bottom wall
if ball.ycor() > 280 or ball.ycor() < -280:
    ball.bounce_y()
```

---

## Why These Numbers Matter

### Screen Dimensions Recap

```text
Screen height = 600
Top wall      = +300
Bottom wall   = -300
```

### Why `280` Instead of `300`

* Ball size ≈ 20 pixels
* Half size ≈ 10 pixels

Using:

```text
300 - 20 = 280
```

Prevents:

* Ball clipping through the wall
* Partial off-screen rendering

---

## Collision Check Logic (Algorithm)

> Read current Y position
> → Compare against vertical bounds
> → If exceeded → reverse Y direction

---

## What Happens Internally After Bounce

Assume:

```text
Before collision → y_move = +10
```

After calling:

```python
self.y_move *= -1
```

Result:

```text
After collision → y_move = -10
```

Next frame:

```text
Ball moves downward
```

---

## Frame-by-Frame Behavior

| Frame | Y Position | y_move | Action          |
| ----- | ---------- | ------ | --------------- |
| N     | 279        | +10    | Normal move     |
| N+1   | 289        | +10    | Wall detected   |
| N+2   | 279        | -10    | Bounce downward |

---

## Why This Works Reliably

* Direction flip happens **before next movement**
* Speed remains constant
* No teleporting or resetting required

---

## Important Constraint (Hidden Assumption)

This logic assumes:

```text
|y_move| < wall buffer
```

If `y_move` becomes very large later:

* Ball could skip past boundary detection
* This is why speed increases must be controlled

---

## Common Mistakes Avoided Here

> Reversing position instead of direction
> Resetting ball on wall hit
> Hardcoding `+10` and `-10` everywhere
> Putting bounce logic inside the game loop

---

## Architectural Progress at This Step

| Aspect      | Improvement             |
| ----------- | ----------------------- |
| Movement    | Direction-based         |
| Collision   | Boundary-aware          |
| Design      | Encapsulated            |
| Scalability | Ready for paddle bounce |

---

## What This Enables Next (Step 6)

* Horizontal bounce (`x_move`)
* Paddle collision detection
* Speed scaling on paddle hit

---

## Mental Model Going Forward

> **Walls reverse Y**
> **Paddles reverse X**
> **Ball owns its physics**

This step transforms the ball from a simple moving object into a physics-aware entity, setting the stage for real gameplay interactions.
