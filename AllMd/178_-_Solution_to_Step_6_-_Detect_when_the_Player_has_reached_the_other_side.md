## Step 6 — Detecting Successful Crossing & Difficulty Progression

**Logic Evaluation, Responsibility Split, and Data Flow**

---

## 1. Conceptual Meaning of Step 6

This step introduces the **success rule** of the game.

> *If the player reaches the top of the screen, the round is won and the game becomes harder.*

Unlike Step 5 (failure), this step causes **state transformation**, not termination.

---

## 2. Player’s Role — Reporting Win Condition

### `is_at_finish_line()`

```python
def is_at_finish_line(self):
    return self.ycor() > FINISH_LINE_Y
```

#### What this method represents

* A **pure query**
* No side effects
* Converts position into a boolean fact

| Question                         | Answer |
| -------------------------------- | ------ |
| Does the player decide success?  | No     |
| Does the player know game rules? | No     |
| Does the player know about cars? | No     |

The player simply reports **where it is**.

---

### `reset_position()`

```python
def reset_position(self):
    self.goto(STARTING_POSITION)
```

#### Why reset happens inside Player

| Reason        | Explanation                      |
| ------------- | -------------------------------- |
| Encapsulation | Player owns its position         |
| Clean API     | Main loop avoids raw coordinates |
| Reusability   | Reset logic centralized          |

Resetting is a **command**, not a decision.

---

## 3. CarManager’s Role — Difficulty Scaling

### `increase_speed()`

```python
def increase_speed(self):
    self.car_speed *= 0.9
```

#### Interpretation of the logic

* Speed multiplier shrinks delay
* Cars move more frequently
* Difficulty increases exponentially, not linearly

This is **progressive difficulty**, not sudden spikes.

---

### Why `CarManager` owns speed

| Reason               | Explanation              |
| -------------------- | ------------------------ |
| Cars are obstacles   | Difficulty tied to them  |
| Single control point | No scattered speed logic |
| Clean scaling        | Level-based tuning       |

No other class touches `car_speed`.

---

## 4. Main Loop — Coordinating Success Event

```python
if player.is_at_finish_line():
    player.reset_position()
    car_manager.increase_speed()
```

### What main.py is doing here

* Detecting a **rule condition**
* Triggering **multiple system reactions**

This confirms main.py’s role as **event orchestrator**.

---

## 5. Event Cascade (Data Flow)

```
Player crosses finish line
        ↓
player.is_at_finish_line() → True
        ↓
main.py reacts
        ↓
player.reset_position()
        ↓
car_manager.increase_speed()
```

One event → multiple updates
All triggered from **one place**

---

## 6. Why Player Reset Happens Before Speed Increase

Order matters conceptually:

1. Close the current round
2. Reset player state
3. Increase difficulty for next attempt

Even though execution order does not affect correctness here, it preserves **mental clarity**.

---

## 7. Separation of Concerns (Validated Again)

| Component  | Responsibility           |
| ---------- | ------------------------ |
| Player     | Position & movement      |
| CarManager | Obstacle difficulty      |
| Main       | Game rules & transitions |

No circular dependencies are introduced.

---

## 8. Edge Case Considerations

### Finish Line vs Collision (Same Frame)

Current logic assumes:

* Collision check occurs **before** finish-line check
* Collision overrides success

This is acceptable and realistic.

---

### Multiple Level Triggers

Resetting position immediately ensures:

* Finish condition cannot trigger twice
* No accidental level skipping

---

## 9. Difficulty Curve Characteristics

Using multiplicative scaling (`× 0.9`) results in:

| Level | Relative Speed    |
| ----- | ----------------- |
| Early | Gentle            |
| Mid   | Noticeably harder |
| Late  | High-pressure     |

This avoids sudden frustration spikes.

---
