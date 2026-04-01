### Hurdle Challenge using `while` loop (Python)

---

### Problem setup

A robot starts at position 0 and must reach the goal.
There are hurdles placed at **unknown positions**.
The robot can:

* `move()` → move forward by 1 step
* `jump()` → jump over a hurdle
* `front_is_clear()` → checks if there is no hurdle ahead
* `at_goal()` → checks if destination is reached

Goal: **Reach the goal without crashing, using a `while` loop**.

---

### Core logic idea

Keep moving **until the goal is reached**.
If the path is clear → move.
If a hurdle is present → jump.

---

### Final solution (standard hurdle challenge)

```python
while not at_goal():          # run until robot reaches destination
    if front_is_clear():      # check if there is no hurdle
        move()                # move forward safely
    else:
        jump()                # hurdle detected, jump over it
```

---

### Line-by-line explanation

```python
while not at_goal():
```

* Loop continues as long as the robot has **not** reached the goal
* Handles unknown distance automatically

```python
if front_is_clear():
```

* Checks the cell directly in front of the robot

```python
move()
```

* Executes only when no hurdle exists

```python
else:
    jump()
```

* Executes only when a hurdle blocks the path

---

### Control flow (decision table)

| Condition        | Action        |
| ---------------- | ------------- |
| Goal not reached | Continue loop |
| Path clear       | `move()`      |
| Hurdle present   | `jump()`      |
| Goal reached     | Exit loop     |

---

### Conceptual path example

Path:

```
⬜ ⬜ 🚧 ⬜ 🚧 ⬜ 🏁
```

Robot decisions:

```
move
move
jump
move
jump
move
```

---

### Conceptual output trace

```
Moved forward
Moved forward
Jumped hurdle
Moved forward
Jumped hurdle
Moved forward
Reached goal
```

---

### Common wrong approach (hardcoding)

```python
move()
jump()
move()
jump()
move()
```

Why wrong:

* Fails if hurdle count changes
* Not scalable
* Not logical programming

---

### Variant: Hurdle with fixed jump logic

If `jump()` is not provided and you must define it:

```python
def jump():
    move()
    move()
    move()

while not at_goal():
    if front_is_clear():
        move()
    else:
        jump()
```

---

### Variant: Hurdle with variable height (advanced logic)

```python
def jump():
    while wall_in_front():    # climb up until no wall
        turn_left()
    move()

    turn_right()
    while front_is_clear():   # move over top of hurdle
        move()

    turn_right()
    move()

    turn_left()

while not at_goal():
    if front_is_clear():
        move()
    else:
        jump()
```

---

### Why `while` is mandatory here

| Reason           | Explanation                 |
| ---------------- | --------------------------- |
| Unknown length   | Goal distance not known     |
| Unknown hurdles  | Positions change            |
| Dynamic decision | React in real time          |
| No repetition    | One logic handles all cases |

---

### Mental model

> “Until I reach the goal, keep checking what’s in front of me.
> If it’s free, move.
> If it’s blocked, overcome it.”

That is exactly what the `while` loop encodes.
