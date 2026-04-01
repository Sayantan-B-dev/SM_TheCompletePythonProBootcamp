## Step 7 — Scoreboard, Level Tracking, and Game-Over Sequence

**Responsibility Analysis, Data Flow, and Correctness Evaluation**

---

## 1. Purpose of Step 7

Step 7 completes the game loop by introducing **persistent feedback** and a **terminal end state**.

> The player must always know:
>
> * What level they are on
> * When the game has ended

This is handled **entirely by the Scoreboard system**.

---

## 2. `Scoreboard(Turtle)` — Why It Inherits from Turtle

### Design Rationale

The scoreboard is a **visual entity**, not a logical one.

Inheritance allows:

* Direct text rendering (`write`)
* Absolute positioning (`goto`)
* Screen-fixed UI behavior

No game logic lives here — only **representation**.

---

## 3. Scoreboard Initialization

```python
def __init__(self):
    super().__init__()
    self.penup()
    self.hideturtle()
    self.level = 1
    self.goto(-200, 250)
    self.update_scoreboard()
```

### Line-by-Line Intent

| Line                  | Reason                  |
| --------------------- | ----------------------- |
| `penup()`             | Prevent drawing lines   |
| `hideturtle()`        | UI text only            |
| `level = 1`           | Initial game state      |
| `goto(-200, 250)`     | Consistent UI placement |
| `update_scoreboard()` | Immediate feedback      |

The scoreboard becomes **self-initializing** and requires no external setup.

---

## 4. `update_scoreboard()` — Single Responsibility Method

```python
def update_scoreboard(self):
    self.write(f"Level: {self.level}", align="center", font=FONT)
```

### Why this method exists

* Centralizes display formatting
* Prevents duplicate `write` logic
* Keeps UI changes isolated

It assumes:

* Screen is already clear
* Position is already set

This keeps it **purely presentational**.

---

## 5. `increase_level()` — Controlled State Mutation

```python
def increase_level(self):
    self.level += 1
    self.clear()
    self.update_scoreboard()
```

### What this method guarantees

| Guarantee     | Explanation                    |
| ------------- | ------------------------------ |
| Atomic update | Level and UI stay in sync      |
| No overlap    | `clear()` removes old text     |
| Encapsulation | No external level manipulation |

The scoreboard **owns the level state** — no other file modifies it.

---

## 6. `game_over()` — Terminal UI State

```python
def game_over(self):
    self.goto(0, 0)
    self.write("GAME OVER", align="center", font=FONT)
```

### Design Intent

* Centered message = visual finality
* No clearing of level text → preserves last achieved level
* No loop control → display only

Game termination logic remains in `main.py`.

---

## 7. Integration in `main.py` — Failure Path

```python
for car in car_manager.all_cars:
    if car.distance(player) < 21:
        game_is_on = False
        scoreboard.game_over()
```

### Why This Is Correct

| Action              | Owner        |
| ------------------- | ------------ |
| Collision detection | `main.py`    |
| Game termination    | `main.py`    |
| End-state display   | `Scoreboard` |

This preserves:

* Rule control in coordinator
* UI control in scoreboard

---

## 8. Integration in `main.py` — Success Path

```python
if player.is_at_finish_line():
    player.reset_position()
    car_manager.increase_speed()
    scoreboard.increase_level()
```

### Event Cascade

```
Player reaches finish line
        ↓
main.py detects success
        ↓
Player resets
Car speed increases
Level increments
```

Three systems update from **one decision point**.

---

## 9. Data Ownership Matrix (Final Form)

| Data                 | Owner           |
| -------------------- | --------------- |
| Player position      | Player          |
| Car positions        | Individual cars |
| Car speed            | CarManager      |
| Level number         | Scoreboard      |
| Game state (running) | main.py         |

No duplicated or conflicting state exists.

---

## 10. Edge Case Handling

### Collision & Finish in Same Frame

Because collision detection occurs first:

* Collision overrides success
* Game ends immediately
* No level increment occurs

This is logically fair and deterministic.

---

## 11. Architectural Completeness Check

At the end of Step 7:

* All game rules exist
* All state transitions are defined
* All feedback is visible
* Game has a clear terminal state

No system oversteps its responsibility.

---

## Step 7 Completion Verification

Step 7 is complete and correct if:

* Level displays on screen at all times
* Level increments only on success
* Game-over message appears on collision
* Game loop stops after failure
* UI logic remains isolated from rules

All criteria are fully satisfied by the provided implementation.
