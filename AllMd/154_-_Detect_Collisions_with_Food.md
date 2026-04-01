## DAY 2 — STEP 1

### Detecting Collision With Food (Completed Implementation Breakdown)

---

## 1. `food.py` — Food Object Design

### Purpose

The `Food` class represents an **independent game entity** responsible only for:

* Appearing on screen
* Randomly repositioning itself
* Being detected via distance-based collision

This follows **single responsibility principle**.

---

## 2. Class Definition and Inheritance

```python
from turtle import Turtle
import random
```

### Why this import matters

* `Turtle` → allows `Food` to behave like a turtle object (position, shape, distance)
* `random` → enables unpredictable food placement

---

```python
class Food(Turtle):
```

### Explanation

* `Food` **inherits** from `Turtle`
* This gives `Food`:

  * `goto()`
  * `distance()`
  * `shape()`
  * `penup()`
  * Coordinate system support

No need to reimplement movement or geometry logic.

---

## 3. Constructor (`__init__`) — Initialization Logic

```python
def __init__(self):
    super().__init__()
```

### Why `super()` is mandatory here

* Initializes the internal Turtle engine
* Without this, methods like `goto()` or `distance()` will fail

---

```python
self.shape("circle")
```

* Visually represents food
* Circle fits collision logic well

---

```python
self.penup()
```

### Critical reasoning

* Prevents drawing lines while teleporting
* Food should **never leave trails**

---

```python
self.shapesize(stretch_len=0.5, stretch_wid=0.5)
```

### Why scaling is important

* Default turtle size = 20×20 pixels
* Scaling to `0.5` → approx **10×10 pixels**
* Makes collision threshold (`< 15`) accurate

---

```python
self.color("blue")
```

* Visual distinction from snake
* Any color works; no logic dependency

---

```python
self.speed("fastest")
```

### Why fastest

* Prevents animation delay during teleport
* Food should instantly appear elsewhere

---

```python
self.refresh()
```

### Design choice

* Food appears immediately at a random location
* No need for a separate setup call

---

## 4. `refresh()` — Random Relocation Algorithm

```python
def refresh(self):
    random_x = random.randint(-280, 280)
    random_y = random.randint(-280, 280)
    self.goto(random_x, random_y)
```

---

### Algorithm (Step-by-Step)

1. Generate random `x` within safe screen bounds
2. Generate random `y` within safe screen bounds
3. Teleport food to `(x, y)`

---

### Why `-280 to 280`

| Value              | Reason                |
| ------------------ | --------------------- |
| Screen width ≈ 600 | Half = 300            |
| Margin (≈20)       | Prevents wall overlap |
| Final safe range   | `±280`                |

This avoids:

* Food spawning off-screen
* Food spawning half outside walls

---

## 5. Main Game Loop — Collision Detection

```python
if snake.head.distance(food) < 15:
    food.refresh()
```

---

### What `distance()` Does

* Computes **Euclidean distance** between:

  * Snake head position
  * Food position

Mathematically:

```
distance = √((x₂ − x₁)² + (y₂ − y₁)²)
```

---

### Why `< 15`

| Factor                   | Value  |
| ------------------------ | ------ |
| Food radius              | ~5 px  |
| Snake head radius        | ~10 px |
| Safe collision threshold | ~15 px |

Ensures:

* Collision feels natural
* No visual overlap required
* No missed detections

---

### Logical Flow

```
IF distance(head, food) < 15:
    collision detected
    reposition food
```

At this stage:

* Snake does NOT grow yet
* Score does NOT update yet
  Those belong to later steps

---

## 6. Expected Runtime Behavior (Observable Output)

### Visual Output (Not Printed)

* Food appears as a small blue dot
* Food jumps to a new random location when eaten
* No console output (correct behavior)

---

## 7. Why This Implementation Is Correct

| Design Aspect | Correctness                 |
| ------------- | --------------------------- |
| OOP usage     | Food is self-contained      |
| Inheritance   | Turtle functionality reused |
| Collision     | Distance-based (robust)     |
| Randomness    | Prevents predictability     |
| Performance   | Fastest speed used          |

---

## 8. Hidden Edge Cases (Handled Implicitly)

* Food teleport does not draw lines (`penup`)
* Food appears inside screen bounds
* Distance collision avoids direction dependency
* Works regardless of snake speed

---

## 9. What This Step Unlocks Next

With food collision working, the game can now:

* Grow the snake
* Increase score
* Increase difficulty later

This directly enables:

* **Step 2 — Scoreboard**
* **Snake body extension logic**

---

## STATUS
