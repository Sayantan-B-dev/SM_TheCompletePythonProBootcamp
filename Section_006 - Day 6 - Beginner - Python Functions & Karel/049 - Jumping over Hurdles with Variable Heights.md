### Jumping over Hurdles with **Variable Heights** (using `while` loop)

---

### Problem statement

A robot moves forward toward a goal.
Hurdles:

* have **unknown height**
* appear at **unknown positions**
* may differ every time

Robot abilities (environment-provided):

```python
move()
turn_left()
front_is_clear()
wall_in_front()
at_goal()
```

Goal:
➡️ **Detect a hurdle, climb it regardless of height, cross it, come down, and continue until goal is reached**

---

### Why simple `jump()` fails here

This does **not** work:

```python
def jump():
    move()
    move()
    move()
```

Reason:

* Height is not fixed
* Some hurdles are taller
* Robot crashes into wall

So we need **logic**, not hardcoded steps.

---

### Correct strategy (human thinking)

1. If path is clear → move
2. If wall ahead:

   * climb up **until no wall**
   * move across top
   * come down **until ground**
3. Continue until goal

This is a **state-based loop problem**.

---

### Final correct solution (standard & accepted)

```python
def jump():
    # turn left to start climbing the hurdle
    turn_left()

    # climb up until there is no wall in front
    while wall_in_front():
        move()

    # reach the top, move one step forward
    move()

    # turn right to move across the top
    turn_right()

    # move forward while path is clear (crossing the hurdle)
    while front_is_clear():
        move()

    # turn right to start coming down
    turn_right()

    # move down until back on the ground
    move()

    # turn left to face original direction
    turn_left()


while not at_goal():
    if front_is_clear():
        move()
    else:
        jump()
```

---

### Line-by-line explanation (core logic)

#### Detecting the hurdle

```python
if front_is_clear():
    move()
else:
    jump()
```

* Decision maker
* Either walk or overcome obstacle

---

#### Climbing phase

```python
turn_left()
while wall_in_front():
    move()
```

* Turn toward the wall
* Keep climbing until the wall ends
* Works for **any height**

---

#### Crossing phase

```python
move()
turn_right()
while front_is_clear():
    move()
```

* Step onto the top
* Cross the width of the hurdle

---

#### Descending phase

```python
turn_right()
move()
turn_left()
```

* Come down safely
* Re-align direction

---

### Visual mental model

```
      ████
      █  █
R → ██████ → 🏁
```

Robot behavior:

```
climb ↑
cross →
descend ↓
continue →
```

---

### Conceptual execution trace

```
Wall detected
Climbing up
Reached top
Crossing hurdle
Descending
Back on ground
Continuing forward
```

---

### Why `while` is essential here

| Problem           | Why `while` solves it  |
| ----------------- | ---------------------- |
| Unknown height    | Loop until wall ends   |
| Unknown width     | Loop until path blocks |
| Unknown distance  | Loop until goal        |
| Dynamic obstacles | Real-time decisions    |

---

### Common mistakes (very important)

#### ❌ Using `if` instead of `while`

```python
if wall_in_front():
    move()
```

Fails for tall hurdles.

---

#### ❌ Forgetting direction reset

Robot ends facing wrong direction → crashes later.

---

#### ❌ Infinite climb loop

```python
while front_is_clear():
    move()
```

Wrong condition → infinite loop on top.

---

### Key rule to remember

> If you don’t know **how many times** something must happen,
> you must use a `while` loop.

This challenge is a perfect example of **thinking in conditions, not steps**.
