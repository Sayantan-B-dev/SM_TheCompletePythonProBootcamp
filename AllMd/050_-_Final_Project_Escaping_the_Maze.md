### Reeborg’s World — **Escaping the Maze** (robust solution with edge-case handling)

---

### Problem reality (why this maze is tricky)

* Maze shape is **unknown**
* Paths may loop
* Dead ends exist
* Simple “always turn left” **can infinite-loop**
* Goal position is unknown

So this is **not** a simple loop problem; it’s a **state + rule-based navigation problem**.

---

### Core idea (wall-following, but safe)

Use the **right-hand rule**, with strict priority:

1. If right side is clear → turn right & move
2. Else if front is clear → move
3. Else → turn left

This guarantees progress and avoids oscillation **if written correctly**.

---

### Required helper functions (Reeborg environment)

```python
move()
turn_left()
front_is_clear()
right_is_clear()
at_goal()
```

We’ll define `turn_right()` for clarity.

---

### Helper: turn right

```python
def turn_right():
    turn_left()
    turn_left()
    turn_left()
```

---

### Final SAFE maze solution (no infinite loop)

```python
def turn_right():
    turn_left()
    turn_left()
    turn_left()


while not at_goal():

    # Priority 1: take right turn if available
    if right_is_clear():
        turn_right()
        move()

    # Priority 2: move forward if possible
    elif front_is_clear():
        move()

    # Priority 3: dead end, turn left
    else:
        turn_left()
```

---

### Why this **does not infinite loop**

Let’s break down the guarantees.

#### 1. Direction always changes OR position changes

Every iteration does **at least one** of:

* `move()` → position changes
* `turn_left()` / `turn_right()` → orientation changes

No iteration does “nothing”.

---

#### 2. Right-hand rule prevents back-and-forth oscillation

Without priority, this happens:

```text
move → hit wall → turn left → move → turn right → back again
```

But with strict priority:

* Right > Front > Left
* No ambiguity
* No repeated indecision

---

#### 3. Dead ends are handled correctly

At a dead end:

* `right_is_clear()` ❌
* `front_is_clear()` ❌
* → `turn_left()` rotates until a path opens

This guarantees escape.

---

### Common infinite-loop mistakes (very important)

#### ❌ Mistake 1: wrong priority order

```python
if front_is_clear():
    move()
elif right_is_clear():
    turn_right()
    move()
```

Why bad:

* Robot hugs front wall
* Misses exits
* Loops forever in corridors

---

#### ❌ Mistake 2: moving without turning

```python
if right_is_clear():
    move()
```

Why bad:

* Robot doesn’t face the opening
* Crashes into wall or loops

---

#### ❌ Mistake 3: missing `elif`

```python
if right_is_clear():
    turn_right()
    move()

if front_is_clear():
    move()
```

Why bad:

* Two moves in one iteration
* Skips logic
* Breaks orientation assumptions

---

### Dry run (important)

Maze fragment:

```
█ █ █ █
█ R   █
█ █ █ █
```

Robot behavior:

1. Right blocked → front clear → move
2. Right clear → turn right → move
3. Dead end → turn left
4. Finds exit → continues
5. Reaches goal → loop stops

---

### Why `while not at_goal()` is mandatory

```python
while not at_goal():
```

Because:

* Maze size unknown
* Exit location unknown
* No fixed iteration count

Using `for` would be logically incorrect.

---

### Edge case: starting next to wall

Handled automatically:

* Right is checked first
* If blocked, front checked
* If both blocked, rotate

No special case code needed.

---

### Edge case: spiral / loop maze

Handled because:

* Wall-following guarantees eventual exit
* Orientation always changes
* Robot never repeats same **state + direction** infinitely

---

### Mental rule (lock this in)

> In maze problems, **movement rules matter more than movement speed**.
> Infinite loops come from ambiguous decisions, not from while-loops themselves.

---

### One-screen summary

| Rule                  | Reason              |
| --------------------- | ------------------- |
| `while not at_goal()` | Unknown maze        |
| Right-hand priority   | Prevents loops      |
| `elif` usage          | One action per step |
| Always turn OR move   | Progress guaranteed |
| No hardcoded steps    | Maze-independent    |

This solution is the **canonical, loop-safe** Reeborg maze escape.
