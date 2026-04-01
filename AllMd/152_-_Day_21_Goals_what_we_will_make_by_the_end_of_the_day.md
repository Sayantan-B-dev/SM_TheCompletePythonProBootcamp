## DAY 2 — SNAKE GAME (TURTLE + PYTHON)

**Scope:** Logic, algorithms, and flow only
**Assumption:** Day 1 is complete (screen setup, snake body, animation, OOP structure, key controls)
**No code — only algorithms and reasoning**

---

## 1. Detecting Collision With Food

### Objective

Detect when the snake’s head reaches the food and trigger growth, score increment, and food reposition.

---

### Core Concept

In Turtle graphics, collision is distance-based, not pixel-based.
Two objects are considered “collided” if the distance between them is below a threshold.

---

### Algorithm

1. Identify the **snake head**

   * Always the first segment of the snake list

2. Measure distance between:

   * Snake head
   * Food object

3. Define a collision threshold

   * Typical value: `15–20` pixels
   * Based on turtle size and shape

4. If distance < threshold:

   * Consider it a collision
   * Trigger food-consumption logic

---

### Food Collision Flow

```
LOOP (game running):
    IF distance(head, food) < collision_threshold:
        food.relocate_randomly()
        snake.extend_body()
        scoreboard.increase_score()
```

---

### Edge Cases & Notes

* Food must relocate **away from the snake body**
* Collision should trigger only once per contact
* Distance-based detection avoids precision issues

---

## 2. Creating the Scoreboard

### Objective

Track and display the score at the top of the screen and update it dynamically.

---

### Core Concept

The scoreboard is a separate Turtle object responsible only for UI rendering.

---

### Responsibilities of Scoreboard

| Responsibility | Description             |
| -------------- | ----------------------- |
| Store score    | Integer counter         |
| Display score  | Write text on screen    |
| Update score   | Clear and re-write text |
| Game over text | Display final message   |

---

### Algorithm

1. Initialize score to `0`
2. Position scoreboard at top-center
3. Display initial score
4. When food collision occurs:

   * Increment score
   * Clear previous text
   * Write updated score

---

### Score Update Flow

```
INITIALIZE score = 0
DISPLAY "Score: 0"

WHEN food is eaten:
    score += 1
    clear_text()
    write("Score: {score}")
```

---

### Game Over Display Logic

```
IF game ends:
    move_to_center()
    write("GAME OVER")
```

---

### Design Notes

* Scoreboard should **never move**
* Pen must be hidden
* Animation disabled for clean rendering

---

## 3. Detecting Collision With Wall

### Objective

End the game when the snake hits the boundary of the screen.

---

### Core Concept

The snake’s head position (`x`, `y`) is compared against screen limits.

---

### Screen Boundary Logic

| Axis   | Condition                   |
| ------ | --------------------------- |
| X-axis | `x > max_x` or `x < -max_x` |
| Y-axis | `y > max_y` or `y < -max_y` |

Where:

* `max_x = screen_width / 2 - margin`
* `max_y = screen_height / 2 - margin`

---

### Algorithm

1. Get head coordinates `(x, y)`
2. Compare against boundary limits
3. If outside limits:

   * Stop game loop
   * Trigger game over

---

### Wall Collision Flow

```
GET head_x, head_y

IF head_x > max_x OR head_x < -max_x
   OR head_y > max_y OR head_y < -max_y:
       end_game()
```

---

### Edge Cases & Notes

* Margin avoids false positives due to turtle size
* Collision must be checked **every frame**
* This is a hard stop (no recovery)

---

## 4. Detecting Collision With Tail

### Objective

End the game if the snake collides with its own body.

---

### Core Concept

The snake head should never overlap any body segment except itself.

---

### Key Rule

Ignore the head itself during collision checks.

---

### Algorithm

1. Loop through all body segments **except the head**
2. Measure distance between head and each segment
3. If distance < threshold:

   * Collision detected
   * End game

---

### Tail Collision Flow

```
FOR each segment in snake_body[1:]:
    IF distance(head, segment) < collision_threshold:
        end_game()
```

---

### Collision Threshold

* Same as food collision (usually `15–20` pixels)

---

### Edge Cases & Notes

* Early game: tail collision impossible (short snake)
* Distance-based detection avoids direction-based bugs
* Must be checked **after movement**, not before

---

## 5. Full Day 2 Logical Flow (Combined)

```
LOOP (game running):

    snake.move_forward()

    IF head collides with food:
        snake.extend()
        food.relocate()
        scoreboard.update()

    IF head collides with wall:
        game_over()

    IF head collides with tail:
        game_over()
```

---

## 6. Why This Order Matters

| Step           | Reason                            |
| -------------- | --------------------------------- |
| Move snake     | Position must update first        |
| Food collision | Growth happens before next frame  |
| Wall collision | Immediate termination             |
| Tail collision | Depends on updated body positions |

---

## 7. Design Separation (OOP Perspective)

| Component  | Responsibility             |
| ---------- | -------------------------- |
| Snake      | Movement, growth, segments |
| Food       | Random placement           |
| Scoreboard | UI & score                 |
| Main loop  | Collision orchestration    |

---

## 8. Common Mistakes to Avoid

* Checking collisions **before movement**
* Forgetting to ignore head in tail detection
* Using equality (`==`) instead of distance
* Not clearing scoreboard before rewriting
* Hardcoding screen limits without margins
