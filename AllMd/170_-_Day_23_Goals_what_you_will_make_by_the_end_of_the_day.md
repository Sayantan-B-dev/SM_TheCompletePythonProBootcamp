## 🧠 Turtle Car Crossing Game — Planning & Algorithms (No Code)

---

## 1. Gameplay Working Analogy (Mental Model)

**High-level idea**

* The player controls a turtle character that starts at the bottom of the screen.
* Cars continuously move horizontally across the screen at varying speeds.
* The objective is to guide the turtle safely to the top without colliding with any car.
* Each successful crossing increases difficulty.
* A collision ends the game.

**Analogy**

> Think of it like crossing a busy road:
>
> * Turtle = pedestrian
> * Cars = traffic lanes
> * Top of screen = safe destination
> * Levels = increasing traffic speed/density

**Core game loop concept**

```
START GAME
WHILE game is running:
    listen for player input
    move cars
    check collisions
    check win condition
    update score / level
END GAME
```

---

## 2. Breaking Down the Problem (System Decomposition)

Break the game into **independent systems** so each can be reasoned about clearly.

| System            | Responsibility                  |
| ----------------- | ------------------------------- |
| Player system     | Handle turtle movement          |
| Car system        | Create, move, recycle cars      |
| Collision system  | Detect turtle–car impact        |
| Goal system       | Detect reaching the top         |
| Scoreboard system | Display level / game over       |
| Game state system | Control running / stopped state |

**Why this matters**

* Prevents mixing logic (movement vs rules vs UI)
* Makes debugging easier
* Enables incremental development

---

## 3. Creating Player Behavior (Turtle Logic)

**Goal**

Allow the turtle to move upward in response to user input.

**Algorithm**

```
INITIALIZE turtle at bottom center of screen

ON user pressing "Up" key:
    move turtle forward by fixed distance

AFTER movement:
    do NOT allow sideways movement
    do NOT allow backward movement
```

**Behavior rules**

* Movement is **discrete**, not continuous
* Turtle always faces upward
* Turtle speed remains constant
* Turtle position must be trackable (x, y)

**Edge cases**

* Turtle should not move beyond top boundary
* Turtle position must reset after level completion

---

## 4. Creating Car Behavior (Obstacle Logic)

**Goal**

Generate multiple cars that move horizontally across the screen.

**Algorithm**

```
REPEAT periodically:
    create a new car
    place car at random vertical position
    place car at right edge of screen
    assign car a random color
    assign car a speed based on level

FOR each car:
    move car left every frame
    IF car moves off screen:
        remove or recycle car
```

**Design decisions**

* Cars move only horizontally
* Speed increases with level
* Cars are independent objects stored in a collection

**Edge cases**

* Too many cars → performance issue
* Cars spawning too close together → unfair difficulty
* Cars overlapping → visual confusion

---

## 5. Detecting Car and Turtle Collision

**Goal**

End the game if turtle touches any car.

**Collision detection logic**

```
FOR each car in car list:
    calculate distance between turtle and car
    IF distance < collision threshold:
        trigger game over
```

**Why distance-based detection**

* Simple and reliable
* Works well with circular/rectangular sprites
* No physics engine needed

**Edge cases**

* Fast cars skipping collision due to frame jumps
* Threshold must match turtle/car size visually

---

## 6. Detecting Reaching the End (Win Condition)

**Goal**

Detect when the turtle successfully crosses the road.

**Algorithm**

```
IF turtle's y-position >= finish line:
    increment level
    reset turtle to start position
    increase car speed
```

**Design considerations**

* Finish line is an invisible horizontal boundary
* Turtle must cross fully, not just touch edge
* Level progression must be atomic (only once per crossing)

**Edge cases**

* Turtle reaching top during same frame as collision
* Level increasing multiple times if not reset immediately

---

## 7. Scoreboard and Game Over Sequence

### A. Scoreboard (Progress Feedback)

**Responsibilities**

* Display current level
* Update level after successful crossing
* Remain visible at all times

**Algorithm**

```
INITIALIZE level = 1

WHEN level increases:
    clear previous score
    write updated level on screen
```

**Design rules**

* Scoreboard should not move
* Must not interfere with gameplay objects

---

### B. Game Over Sequence (Termination)

**Trigger condition**

```
collision detected == True
```

**Algorithm**

```
STOP all car movement
DISPLAY "GAME OVER" at center of screen
DISABLE player input
END main game loop
```

**Why explicitly stop everything**

* Prevents visual bugs
* Prevents further state changes
* Makes end state deterministic

**Edge cases**

* Collision during level-up
* Multiple collisions triggering game over multiple times

---

## Overall Game Flow (Condensed Algorithm)

```
INITIALIZE screen, player, cars, scoreboard
SET game_running = True

WHILE game_running:
    create cars periodically
    move all cars
    listen for player input
    check collision
    IF collision:
        game_running = False
        show game over
    IF turtle reached finish:
        level += 1
        reset turtle
        increase difficulty
```

---

## Key Design Principles Used

* Separation of concerns
* Frame-based simulation
* Event-driven input
* Deterministic game state transitions
* Incremental difficulty scaling
