## PONG GAME — ALGORITHM & PLANNING (TURTLE + PYTHON)

---

## 1. Setting Up the Main Screen

### Goal

Create a visual playground where all game objects will live and update smoothly.

### Algorithm

* Initialize a screen object from the turtle graphics system.
* Define fixed width and height to establish game boundaries.
* Set background color to improve object contrast.
* Disable automatic screen refresh (`tracer(0)`) to manually control rendering.
* Decide a consistent coordinate system where:

  * Center = `(0, 0)`
  * Right edge = `+width/2`
  * Left edge = `-width/2`
  * Top edge = `+height/2`
  * Bottom edge = `-height/2`
* Plan a game loop that:

  * Updates screen manually.
  * Runs continuously until game exit.

### Key Reasoning

Manual screen refresh avoids flickering and allows frame-by-frame animation control.

---

## 2. Creating a Paddle That Responds to Key Press

### Goal

Allow user input to control a paddle vertically.

### Algorithm

* Decide paddle movement axis: **Y-axis only**.
* Bind keyboard keys:

  * One key → move paddle up.
  * Another key → move paddle down.
* On key press:

  * Read current paddle Y position.
  * Add or subtract a fixed movement distance.
* Prevent paddle from leaving screen:

  * Before moving, check if next position exceeds top/bottom boundary.
  * If yes, block movement.

### Edge Cases

* Holding key should not allow paddle to disappear off-screen.
* Paddle speed should be constant and predictable.

---

## 3. Writing the Paddle Class & Creating the Second Paddle

### Goal

Avoid duplicated logic and support two paddles cleanly.

### Algorithm

* Define a `Paddle` abstraction conceptually:

  * Properties:

    * Position `(x, y)`
    * Height
    * Movement speed
  * Behaviors:

    * Move up
    * Move down
* Instantiate two paddles:

  * Left paddle at fixed negative X position.
  * Right paddle at fixed positive X position.
* Bind controls:

  * Left paddle → keys like `W` and `S`
  * Right paddle → arrow keys
* Ensure both paddles use the same movement logic but different inputs.

### Reasoning

Class-based structure ensures scalability and clean separation of responsibilities.

---

## 4. Writing the Ball Class & Making the Ball Move

### Goal

Create a moving object with direction and speed.

### Algorithm

* Define a `Ball` abstraction:

  * Properties:

    * Position `(x, y)`
    * Horizontal direction (`dx`)
    * Vertical direction (`dy`)
    * Speed factor
* Initial state:

  * Ball starts at center `(0, 0)`
  * Randomize initial horizontal direction.
* Movement logic per frame:

  * New X = current X + `dx * speed`
  * New Y = current Y + `dy * speed`
* Call move logic inside the main game loop.

### Key Reasoning

Separating direction from speed allows later difficulty scaling.

---

## 5. Adding Ball Bouncing Logic (Top & Bottom Walls)

### Goal

Keep the ball inside vertical boundaries.

### Algorithm

* On every frame:

  * Check ball Y position.
* If:

  * `Y >= top boundary` OR
  * `Y <= bottom boundary`
* Then:

  * Reverse vertical direction (`dy = -dy`)
* Do **not** reset position — only invert direction.

### Edge Cases

* High speed could skip boundary detection.
* Use boundary buffer slightly inside screen edge.

---

## 6. Detecting Collision With the Paddle

### Goal

Make the ball bounce back when it hits a paddle.

### Algorithm

* On each frame:

  * Measure distance between ball and each paddle.
* Collision condition:

  * Ball X position is near paddle X position.
  * Ball Y position is within paddle height range.
* If collision detected:

  * Reverse horizontal direction (`dx = -dx`)
  * Slightly increase ball speed.
  * Optionally adjust `dy` based on hit position for realism.

### Reasoning

Distance-based detection is simpler and faster than shape-based collision.

---

## 7. Detecting If Ball Goes Out of Bounds

### Goal

Determine when a player misses the ball.

### Algorithm

* On each frame:

  * Check ball X position.
* If:

  * Ball X > right boundary:

    * Left player scores.
  * Ball X < left boundary:

    * Right player scores.
* On score:

  * Reset ball to center.
  * Reverse initial direction.
  * Reset speed to base value.

### Edge Cases

* Ensure score updates before ball reset.
* Avoid multiple score triggers for same miss.

---

## 8. Score Keeping & Changing Ball Speed

### Goal

Track points and progressively increase difficulty.

### Algorithm

* Maintain two score counters:

  * `left_score`
  * `right_score`
* Display scores at fixed screen positions.
* When a player scores:

  * Increment their score.
  * Update on-screen text.
* Speed logic:

  * Base speed at game start.
  * On every paddle collision:

    * Multiply speed by a small factor (e.g., `1.05`)
* Optional cap:

  * Define maximum speed to keep game playable.

### Reasoning

Gradual speed increase keeps game engaging without sudden difficulty spikes.

---

## Overall Game Loop Flow

> Screen update
> → Read user input
> → Move paddles
> → Move ball
> → Wall collision check
> → Paddle collision check
> → Out-of-bounds check
> → Score update
> → Speed adjustment
> → Repeat continuously

---

## Conceptual Separation of Responsibilities

| Component    | Responsibility                      |
| ------------ | ----------------------------------- |
| Screen       | Rendering & refresh control         |
| Paddle       | Player-controlled vertical movement |
| Ball         | Autonomous movement & collision     |
| Game Loop    | Order of execution                  |
| Score System | Game state & progression            |

---
