## DAY 2 — STEP 3

### Detecting Collision With Wall (Technical Validation & Reasoning)

---

## 1. Purpose of Wall Collision Detection

Wall collision defines a **hard terminal condition** for the game:

* If the snake exits the playable area
* The game loop stops
* A game-over state is triggered

This step enforces **spatial constraints**.

---

## 2. Code Under Review

```python
# Detect collision with wall
if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
    game_is_on = False
    scoreboard.game_over()
```

---

## 3. Coordinate-Based Collision Logic

### Turtle Coordinate System

| Axis   | Description          |
| ------ | -------------------- |
| X-axis | Left (-) ↔ Right (+) |
| Y-axis | Down (-) ↔ Up (+)    |

Default screen size ≈ `600 × 600`

---

### Why `±280` Works

| Value           | Reason           |
| --------------- | ---------------- |
| Half-screen     | `300`            |
| Snake head size | `~20`            |
| Safe margin     | `~20`            |
| Final limit     | `300 - 20 = 280` |

This prevents:

* Partial wall overlap
* Visual clipping
* False negatives

---

## 4. Algorithm Breakdown

### Logical Steps

1. Read snake head X coordinate
2. Read snake head Y coordinate
3. Compare against horizontal boundaries
4. Compare against vertical boundaries
5. If any condition is violated:

   * End game loop
   * Display game over message

---

### Pseudocode

```
IF head.x > right_limit OR head.x < left_limit
   OR head.y > top_limit OR head.y < bottom_limit:
       stop_game_loop
       show_game_over
```

---

## 5. Boolean Logic Analysis

Your condition expands to:

```
OUT_OF_BOUNDS = 
    (x > 280) OR (x < -280) OR (y > 280) OR (y < -280)
```

### Why OR (`or`) Is Correct

* Collision occurs if **any one boundary** is crossed
* Using `and` would make collision impossible

---

## 6. Game Loop Interaction

### Correct Placement

This check must happen:

* **After snake movement**
* **Every frame**

Correct loop order:

```
while game_is_on:
    screen.update()
    snake.move()

    check_food_collision
    check_wall_collision
    check_tail_collision
```

---

## 7. Game State Transition

```python
game_is_on = False
```

### What this does

* Cleanly exits the main loop
* Prevents further movement or updates
* Preserves final score state

---

## 8. Scoreboard Interaction

```python
scoreboard.game_over()
```

### Why this is correct

* UI responsibility remains inside Scoreboard
* Main loop only signals the event
* Follows separation of concerns

---

## 9. Expected Runtime Behavior

### Normal Play

* Snake moves freely within bounds

---

### Wall Hit Event

Visual outcome:

* Snake stops moving
* Score remains visible
* “GAME OVER” appears at center

No console output (correct behavior).

---

## 10. Common Mistakes This Code Avoids

| Mistake                                | Avoided                     |
| -------------------------------------- | --------------------------- |
| Using equality (`==`)                  | Yes                         |
| Hardcoding screen width without margin | Yes                         |
| Using `and` instead of `or`            | Yes                         |
| Checking before movement               | Avoided if placed correctly |
| Clearing score on game over            | Avoided                     |

---

## 11. Subtle Edge Case (Handled Implicitly)

* Snake moving fast cannot “skip” the boundary
* Even if it jumps beyond 280 in one frame, condition still catches it

---

## 12. Logical Completeness of Step 3

| Requirement        | Status   |
| ------------------ | -------- |
| Boundary detection | Complete |
| Loop termination   | Correct  |
| UI update          | Correct  |
| State preservation | Correct  |

---
