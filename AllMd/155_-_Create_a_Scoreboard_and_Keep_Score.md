## DAY 2 — STEP 2

### Scoreboard Implementation (Detailed Technical Breakdown)

---

## 1. Purpose of `Scoreboard`

The `Scoreboard` class is a **UI-only component** whose sole responsibility is:

* Tracking score state
* Rendering score text on screen
* Updating score when food is eaten
* Displaying a game-over message

It **does not** control game logic, collisions, or snake movement.

This is a correct separation of concerns.

---

## 2. Constants (UI Configuration)

```python
ALIGNMENT = "center"
FONT = ("Arial", 16, "normal")
```

### Why constants are used

* Avoids hardcoding magic values
* Easy to tweak UI appearance globally
* Improves readability and maintainability

### Meaning

| Constant    | Purpose                       |
| ----------- | ----------------------------- |
| `ALIGNMENT` | Horizontal text alignment     |
| `FONT`      | Font family, size, and weight |

---

## 3. Class Definition and Inheritance

```python
class Scoreboard(Turtle):
```

### Why inherit from `Turtle`

* Allows direct usage of:

  * `write()`
  * `goto()`
  * `clear()`
  * `hideturtle()`
* No need to manage drawing manually

---

## 4. Constructor (`__init__`) — Initialization Logic

```python
def __init__(self):
    super().__init__()
```

### Why `super()` is mandatory

* Initializes Turtle’s internal state
* Without this, drawing and positioning will fail

---

```python
self.score = 0
```

### Purpose

* Stores game score as internal state
* Score persists across updates

---

```python
self.color("white")
```

* Score text color
* Must contrast background (usually black)

---

```python
self.penup()
```

### Why this is critical

* Prevents unwanted lines when moving the scoreboard
* Scoreboard must never draw paths

---

```python
self.hideturtle()
```

### Reason

* Cursor should not be visible
* Only text should appear on screen

---

```python
self.goto(0, 270)
```

### Positioning Logic

| Axis      | Reason                   |
| --------- | ------------------------ |
| `x = 0`   | Center horizontally      |
| `y = 270` | Near top of 600px screen |

Keeps score readable and out of gameplay area.

---

```python
self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
self.update_scoreboard()
```

### Observation

This causes **duplicate writing**.

#### What happens internally

1. Score is written once
2. `update_scoreboard()` writes again without clearing

This does not break the game but is **redundant**.

Correct behavior would be:

* Either write once directly
* Or rely only on `update_scoreboard()`

---

## 5. `update_scoreboard()` — Rendering Logic

```python
def update_scoreboard(self):
    self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
```

### Responsibility

* Writes current score to screen
* Uses current `self.score` value

### Design intent

* Centralized text rendering
* Prevents duplication of formatting logic

---

## 6. `increase_score()` — Score Mutation Logic

```python
def increase_score(self):
    self.score += 1
    self.clear()
    self.update_scoreboard()
```

### Algorithm

1. Increment score
2. Clear previous text
3. Write updated score

---

### Why `clear()` is essential

Without `clear()`:

* New text overlaps old text
* Screen becomes unreadable

---

### Correct Flow

```
score = score + 1
remove old text
render new text
```

This is **state → clear → redraw**, which is correct UI logic.

---

## 7. `game_over()` — End-State UI

```python
def game_over(self):
    self.goto(0, 0)
    self.write("GAME OVER", align=ALIGNMENT, font=FONT)
```

---

### Behavior

* Moves cursor to screen center
* Displays final message
* Does not clear score (intentional)

---

### Why score is not cleared

* Player can still see final score
* Game-over message overlays without destroying state

---

## 8. Expected Runtime Behavior (Visual Output)

### Initial State

```
Score: 0
```

Positioned at top center.

---

### After Eating Food (Once)

```
Score: 1
```

---

### After Multiple Food Collisions

```
Score: 5
```

---

### Game Over

```
GAME OVER
```

Centered on screen.

---

## 9. Logical Integration With Main Loop

Expected usage in `main.py`:

```python
if snake.head.distance(food) < 15:
    food.refresh()
    snake.extend()
    scoreboard.increase_score()
```

For game over:

```python
scoreboard.game_over()
game_is_on = False
```

---

## 10. Design Strengths

| Aspect         | Evaluation |
| -------------- | ---------- |
| OOP separation | Correct    |
| UI isolation   | Correct    |
| State handling | Correct    |
| Redraw logic   | Correct    |
| Turtle usage   | Correct    |

---

## 11. Minor Improvement (Conceptual)

Redundant initial write:

```python
self.write(...)
self.update_scoreboard()
```

Only one is needed.

Preferred pattern:

```
initialize score
position cursor
update_scoreboard()
```

This avoids double rendering.

---
