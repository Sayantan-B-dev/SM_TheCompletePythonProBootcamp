## DAY 1 — SNAKE GAME (TURTLE + PYTHON)

**Goal:** Build the visual and logical foundation of the Snake game before introducing game rules (food, collision, score).

---

## OVERALL FLOW (DAY 1)

> Convert a static idea (snake on screen) into a moving, controllable object using structured steps.
> Focus is on **screen**, **movement logic**, and **input handling**, not gameplay rules.

---

## STEP 1 — Screen Setup & Initial Snake Body

### Objective

Create the game window and place a visible snake on the screen using multiple segments.

### Logical Breakdown

* Initialize a drawing canvas (game world).
* Define the coordinate system.
* Create multiple square segments aligned in a straight line.
* Each segment represents part of the snake’s body.

### Algorithm

1. Create a screen with fixed width and height.
2. Set background color and title.
3. Decide initial snake length (e.g., 3 segments).
4. Define starting coordinates for each segment:

   * Head at origin
   * Body segments placed behind the head with equal spacing
5. For each coordinate:

   * Create a square object
   * Place it at the corresponding position
6. Store all segments in an ordered structure (important for movement later).

### Key Reasoning

* Using a list-like structure preserves segment order.
* Fixed spacing avoids overlap and simplifies animation.
* No movement yet — only visual placement.

---

## STEP 2 — Animating Snake Segments (Movement Logic)

### Objective

Make the snake move forward smoothly as a single unit.

### Core Idea

The snake does **not** move each segment independently.
Instead:

* The tail follows the segment in front of it.
* The head moves forward in the current direction.

### Algorithm

1. Start an infinite game loop.
2. Pause briefly each loop iteration (controls speed).
3. Move segments **backwards**:

   * Last segment moves to the position of the second last
   * Continue until the first body segment
4. Move the head forward by a fixed distance.
5. Refresh the screen after movement.

### Why Backward Movement?

* Prevents overwriting positions.
* Ensures clean following behavior.
* Mimics real snake motion.

### Edge Considerations

* Movement must be frame-based, not keypress-based.
* Speed must be adjustable later.

---

## STEP 3 — Creating Snake Class (Transition to OOP)

### Objective

Refactor procedural logic into a reusable, maintainable object.

### Why OOP Here?

* Snake has:

  * State → body segments, direction
  * Behavior → move, turn
* OOP groups related data and behavior logically.

### Algorithm

1. Define a Snake blueprint.
2. Inside it:

   * Initialize body segments.
   * Store all segments in an internal structure.
3. Move creation logic into the class.
4. Move animation logic into a method.
5. Expose only necessary controls (e.g., move forward).

### Design Principles

* Screen logic stays outside the snake.
* Snake manages its own movement.
* Clear separation of responsibilities.

---

## STEP 4 — Controlling Snake with Key Presses

### Objective

Allow the user to control the snake direction using keyboard input.

### Core Constraints

* Snake cannot reverse directly (e.g., left → right).
* Direction changes only affect the head.
* Body follows automatically.

### Algorithm

1. Define four direction states:

   * Up
   * Down
   * Left
   * Right
2. Map keys to direction-change functions.
3. On key press:

   * Check current direction.
   * If new direction is opposite → ignore input.
   * Else → update snake’s heading.
4. Movement loop continues independently of input.

### Why This Separation Matters

* Input changes **state**, not movement execution.
* Prevents jitter and illegal moves.
* Scales cleanly when speed increases.

---

## DAY 1 OUTPUT STATE (WHAT SHOULD EXIST)

| Component                 | Status  |
| ------------------------- | ------- |
| Game window               | Created |
| Snake visible             | Yes     |
| Snake moves automatically | Yes     |
| Direction control         | Yes     |
| Food                      | No      |
| Collision detection       | No      |
| Score                     | No      |

---

## MENTAL MODEL TO KEEP

> **Head decides → Body follows → Screen updates → Repeat**

This mental loop is the backbone of the entire Snake game.
