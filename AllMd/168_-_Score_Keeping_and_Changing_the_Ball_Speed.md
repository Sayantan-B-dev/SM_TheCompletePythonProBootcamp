## STEP 8 — SCORING SYSTEM + BALL SPEED CONTROL (COMPLETE BREAKDOWN)

---

## A. SCOREBOARD CLASS — PURPOSE & DESIGN

### Responsibility

> Maintain game state (scores) and render them on screen
> No physics, no collision logic, no input handling

This separation ensures:

* Clean architecture
* Easy future extensions (win condition, reset, game over)

---

## `scoreboard.py` — Class Structure

### Core State Variables

```text
l_score → left player score
r_score → right player score
```

These live **inside the scoreboard**, not in `main`, because:

* Score is global game state
* Scoreboard owns how scores are displayed

---

## Constructor (`__init__`) Logic

### What Happens Step-by-Step

1. Initialize Turtle internals
2. Configure visual appearance
3. Initialize scores to zero
4. Render the initial scoreboard

---

### Why Each Line Exists

* `self.color("white")`
  Ensures score visibility on dark background

* `self.penup()`
  Prevents drawing lines when moving text cursor

* `self.hideturtle()`
  Cursor should not be visible; only text matters

* `self.l_score = 0`, `self.r_score = 0`
  Explicit score state, avoids magic numbers

* `self.update_scoreboard()`
  Ensures score is visible immediately when game starts

---

## `update_scoreboard()` — Rendering Algorithm

### Algorithmic Flow

> Clear previous text
> → Move to left score position
> → Write left score
> → Move to right score position
> → Write right score

---

### Why `clear()` Is Critical

* Turtle does not overwrite text automatically
* Without `clear()`:

  * Digits overlap
  * Screen becomes unreadable

---

### Coordinate Choice

```text
Left score  → (-100, 200)
Right score → (100, 200)
```

Reasons:

* Symmetry around center
* High enough to avoid gameplay area
* Visually balanced

---

### Font Choice

```text
("Courier", 80, "normal")
```

* Monospace → consistent alignment
* Large size → readable at distance
* Normal weight → clean arcade look

---

## Point Increment Methods

### `l_point()` / `r_point()`

**Algorithm**

> Increment score
> → Refresh display

These methods ensure:

* No manual score manipulation in `main`
* Single source of truth for score updates

---

## B. MAIN FILE — SCORING INTEGRATION

### Scoreboard Instantiation

```text
scoreboard = Scoreboard()
```

Why here:

* Scoreboard must exist once
* Needs access throughout the game loop

---

## Miss Detection + Scoring Logic

### Algorithm (Right Paddle Miss)

> Ball crosses right boundary
> → Reset ball
> → Increment left score

### Algorithm (Left Paddle Miss)

> Ball crosses left boundary
> → Reset ball
> → Increment right score

This matches Pong rules:

* You score when your opponent misses

---

## Why Score Update Happens After Reset

* Prevents visual confusion
* Ensures next rally starts cleanly
* Maintains clear game rhythm

---

## C. BALL SPEED MECHANICS — DIFFICULTY SCALING

---

## New Ball State Variables

```text
x_move      → horizontal direction & speed
y_move      → vertical direction & speed
move_speed  → frame delay multiplier
```

This introduces **three independent control axes**:

* Direction (sign)
* Speed (magnitude)
* Game pacing (time delay)

---

## `move_speed` — What It Actually Controls

> It does **not** change distance
> It changes **how often movement occurs**

Used in main loop as:

```text
time.sleep(ball.move_speed)
```

Lower value → faster game
Higher value → slower game

---

## Ball Movement (`move()`)

### Algorithm

> Read current position
> → Add x_move
> → Add y_move
> → Update position

Because `x_move` and `y_move` are variables:

* Direction can flip
* Speed can scale
* Motion stays consistent

---

## Speed Increase on Paddle Hit

### `bounce_x()` Logic

```text
Reverse x direction  
Reduce move_speed by 10%
```

Why this works:

* Ball moves more frequently
* Difficulty increases gradually
* Rally becomes more intense over time

This mimics real Pong difficulty curves.

---

## Why Speed Change Is Inside `bounce_x()`

* Paddle hits define rally progression
* Walls should not increase difficulty
* Keeps speed logic centralized and predictable

---

## Reset Behavior (`reset_position()`)

### Algorithm

> Move ball to center
> → Reset speed to base value
> → Reverse direction

Why reset speed:

* Prevents runaway difficulty
* Keeps game fair after each point
* Allows fresh rallies

---

## D. FULL RALLY LIFECYCLE (END-TO-END)

### One Complete Point

> Ball starts at center
> → Players rally
> → Ball accelerates on paddle hits
> → One player misses
> → Ball resets
> → Score updates
> → Speed resets
> → New rally begins

---

## E. ARCHITECTURAL STATE AFTER STEP 8

| Component  | Responsibility             |
| ---------- | -------------------------- |
| Paddle     | Player-controlled movement |
| Ball       | Physics, direction, speed  |
| Scoreboard | Game state + rendering     |
| Main loop  | Orchestration              |

No component:

* Knows too much
* Does another’s job
* Depends on internal state of others

---

## F. WHY THIS IS A “COMPLETE” PONG

You now have:

* Real-time input
* Physics-based motion
* Collision handling
* Miss detection
* Scoring
* Difficulty scaling
* Clean object-oriented structure

This is not a demo — this is a **finished arcade system** with room for:

* Win conditions
* AI opponent
* Sound effects
* Visual polish

At this point, the game logic is correct, scalable, and professionally structured.
