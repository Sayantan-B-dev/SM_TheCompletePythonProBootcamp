## Step 2 — Understanding Code Structure, File Responsibilities, and Data Flow

---

## 1. Mental Shift at Step 2

At this stage, the focus moves from

> *“How does the game behave?”*
> to
> *“Which file controls which behavior, and how data moves between them?”*

This step is about **architecture**, not implementation.

---

## 2. File-Level Responsibility Mapping

Each file represents a **system boundary**.
No file should leak responsibility into another.

| File             | Owns                    | Must NOT Own       |
| ---------------- | ----------------------- | ------------------ |
| `main.py`        | Game loop, coordination | Game logic details |
| `player.py`      | Turtle behavior         | Car logic, scoring |
| `car_manager.py` | Cars lifecycle          | Player input       |
| `scoreboard.py`  | UI text, level          | Collision logic    |

This prevents *spaghetti logic*.

---

## 3. Object Creation & Ownership

### Object Lifecycle

All core objects are **created once** in `main.py`.

```
main.py creates:
    Player object
    CarManager object
    Scoreboard object
```

Why this matters:

* Single source of truth
* Centralized control
* Easier debugging

Other files **do not create each other**.

---

## 4. Data Flow Direction (Very Important)

Data always flows **downward**, never sideways.

```
main.py
 ├── calls Player methods
 ├── calls CarManager methods
 └── calls Scoreboard methods
```

### No Cross-Talking Rule

* `Player` never talks to `CarManager`
* `CarManager` never talks to `Scoreboard`
* `Scoreboard` never checks collisions

All decisions are made in `main.py`.

---

## 5. Breaking the Problem into Code Sections

### A. Player System (`player.py`)

**Encapsulated Data**

| Data            | Meaning         |
| --------------- | --------------- |
| Position (x, y) | Turtle location |
| Move distance   | Step size       |
| Finish line Y   | Win threshold   |

**Encapsulated Behavior**

```
initialize player
move up
reset position
report current y-position
```

The player exposes **state**, not decisions.

---

### B. Car System (`car_manager.py`)

**Encapsulated Data**

| Data       | Meaning           |
| ---------- | ----------------- |
| Car list   | Active obstacles  |
| Move speed | Difficulty factor |
| Colors     | Visual variation  |

**Encapsulated Behavior**

```
create new cars
move all cars
increase speed
provide car positions
```

Cars do not know *why* they move — only *how*.

---

### C. Scoreboard System (`scoreboard.py`)

**Encapsulated Data**

| Data          | Meaning        |
| ------------- | -------------- |
| Current level | Progress state |
| Font          | Visual config  |

**Encapsulated Behavior**

```
display level
update level
show game over
```

Scoreboard reacts to state changes, never causes them.

---

## 6. Main Loop as the Data Router (`main.py`)

`main.py` acts as a **traffic controller**.

### What It Knows

* Player position
* Car positions
* Level state
* Game running state

### What It Does Every Frame

```
pause briefly
move cars
check collision
check finish line
update screen
```

All condition checks live here.

---

## 7. Collision Data Flow Example

### Conceptual Flow

```
main.py asks CarManager for cars
main.py asks Player for position
main.py computes collision
```

### Why This Is Correct

* Collision is a **rule**, not a behavior
* Rules belong in the coordinator
* Keeps systems reusable

---

## 8. Level-Up Data Flow Example

```
main.py detects finish line
main.py tells Scoreboard to increase level
main.py tells CarManager to increase speed
main.py tells Player to reset
```

One event → multiple systems updated
All triggered from **one place**

---

## 9. State Ownership Table

| State           | Owner        |
| --------------- | ------------ |
| Game running    | `main.py`    |
| Player position | `Player`     |
| Car speed       | `CarManager` |
| Level number    | `Scoreboard` |

State is never duplicated.

---

## 10. Why This Architecture Scales

Because:

* Each file has one reason to change
* Logic is testable in isolation
* Bugs are localized
* New features fit naturally

Example extensions that fit cleanly:

* Sound system
* Pause feature
* Multiple lanes
* Power-ups

---

## 11. Step 2 Completion Check

You fully understand Step 2 if you can answer:

* Which file decides game over?
* Which file moves cars?
* Where is collision checked?
* Who owns the level number?
* Why don’t classes talk to each other directly?
