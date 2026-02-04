## 📁 Project Starter Code — Conceptual Explanation (No Code Added)

---

## 1. `car_manager.py` — Car System Blueprint

### Constants

| Name                     | Purpose                  | Design Reason                   |
| ------------------------ | ------------------------ | ------------------------------- |
| `COLORS`                 | Possible car colors      | Visual distinction between cars |
| `STARTING_MOVE_DISTANCE` | Initial car speed        | Controls base difficulty        |
| `MOVE_INCREMENT`         | Speed increase per level | Difficulty scaling mechanism    |

**Key idea**

> This file is responsible for **all car-related behavior**, not gameplay rules.

---

### `CarManager` Class (Currently Empty)

**Why this class exists**

* To encapsulate all logic related to cars
* To avoid mixing obstacle logic with player or scoreboard logic

**Planned responsibilities**

| Responsibility | Explanation                          |
| -------------- | ------------------------------------ |
| Car creation   | Spawn cars at random positions       |
| Car movement   | Move cars continuously across screen |
| Speed control  | Increase speed as level increases    |
| Storage        | Maintain a list of all active cars   |
| Cleanup        | Remove cars that leave the screen    |

**Design intention**

> This class will act as a **car controller**, not a single car.

---

## 2. `main.py` — Game Orchestrator

This file coordinates **everything**, but owns **nothing**.

---

### Screen Setup

| Line              | Purpose                 |
| ----------------- | ----------------------- |
| `Screen()`        | Creates game window     |
| `setup(600, 600)` | Fixed coordinate system |
| `tracer(0)`       | Turns off auto-refresh  |

**Why `tracer(0)` matters**

* Manual screen refresh improves performance
* Enables smooth animation
* Prevents flickering

---

### Imports

| Imported Class | Role                       |
| -------------- | -------------------------- |
| `Player`       | Handles turtle movement    |
| `CarManager`   | Manages obstacles          |
| `Scoreboard`   | Displays level & game over |

> `main.py` **does not implement logic**, it *connects systems*.

---

### Game Loop

```
while game_is_on:
    time.sleep(0.1)
    screen.update()
```

**What this loop represents**

* The **heartbeat** of the game
* Runs ~10 frames per second
* Will later contain:

  * Car movement
  * Collision checks
  * Win condition checks

**Why sleep is needed**

* Prevents CPU overuse
* Controls game speed
* Makes motion human-readable

---

## 3. `player.py` — Player Configuration & Contract

### Constants

| Constant            | Meaning                      |
| ------------------- | ---------------------------- |
| `STARTING_POSITION` | Turtle start location        |
| `MOVE_DISTANCE`     | Distance moved per key press |
| `FINISH_LINE_Y`     | Win condition boundary       |

**Why constants are separated**

* Easier balancing
* Clear game tuning
* Avoids magic numbers in logic

---

### `Player` Class (Currently Empty)

**Intended role**

* Represent the turtle character
* Encapsulate movement and state

**Expected behaviors**

| Behavior          | Explanation                     |
| ----------------- | ------------------------------- |
| Initialization    | Create turtle at start position |
| Move up           | Respond to key press            |
| Reset             | Return to start after success   |
| Position tracking | Provide y-coordinate for checks |

**Design philosophy**

> The player **does not know about cars or scores**.

---

## 4. `scoreboard.py` — UI & Feedback System

### Constants

| Name   | Purpose                      |
| ------ | ---------------------------- |
| `FONT` | Standardized text appearance |

**Why font is isolated**

* Visual consistency
* Easy UI adjustment
* Centralized styling

---

### `Scoreboard` Class (Currently Empty)

**Responsibilities**

| Responsibility    | Explanation               |
| ----------------- | ------------------------- |
| Display level     | Show current progress     |
| Update level      | Change display on success |
| Game over message | End-state feedback        |

**What it must NOT do**

* No game logic
* No collision checks
* No player interaction

---

## 5. Architectural Intent (Why This Structure Exists)

### Separation of Concerns

| File             | Owns            |
| ---------------- | --------------- |
| `main.py`        | Game flow       |
| `player.py`      | Player behavior |
| `car_manager.py` | Obstacles       |
| `scoreboard.py`  | UI feedback     |

---

### Why Classes Are Empty Initially

> This is **intentional scaffolding**.

* Forces incremental thinking
* Encourages responsibility-driven design
* Prevents monolithic scripts
* Mirrors real-world software architecture

---

## 6. Execution State at This Stage

**What the game does right now**

* Opens a 600×600 window
* Runs an empty animation loop
* Displays nothing
* Accepts no input
* Never ends

**Why this is useful**

* Confirms screen setup works
* Confirms frame control works
* Establishes timing baseline
* Provides safe foundation to build on

---

## 7. Mental Model Summary

> This starter code is a **skeleton**, not a game.

* Constants define **rules**
* Classes define **roles**
* Main loop defines **time**
* Logic will be layered gradually
* Each file evolves independently

This structure ensures clarity, scalability, and debuggability as complexity increases.
