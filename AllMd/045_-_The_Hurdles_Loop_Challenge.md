### Hurdles Loop Challenge (Python)

---

### Problem statement

A robot is moving forward on a straight path.
There are hurdles of **unknown positions and unknown number**.
The robot can:

* move forward
* jump over a hurdle

Goal: **Reach the end while jumping only when a hurdle is present**, using loops instead of repeating code.

This is a classic loop + condition challenge (commonly used in logic building).

---

### Core concepts used

| Concept        | Purpose                              |
| -------------- | ------------------------------------ |
| `while` loop   | Repeat actions until goal is reached |
| `if` condition | Check whether a hurdle exists        |
| Function calls | `move()` and `jump()`                |
| Abstraction    | Hide repeated logic inside functions |

---

### Assumed helper functions (environment-provided)

```python
move()        # moves robot forward by 1 step
jump()        # jumps over a hurdle
front_is_clear()  # returns True if no hurdle ahead
at_goal()     # returns True if destination reached
```

You **do not define** these in the challenge; they are given by the environment (like Reeborg / Hurdle challenges).

---

### Naive (wrong) approach – hardcoded

```python
move()
jump()
move()
jump()
move()
```

Problem:

* Fails if hurdles count or positions change
* Not scalable
* Violates DRY principle

---

### Correct approach using loop + condition

```python
while not at_goal():           # keep running until destination reached
    if front_is_clear():       # if no hurdle ahead
        move()                 # move normally
    else:                      # if hurdle detected
        jump()                 # jump over it
```

---

### Explanation (line by line)

```python
while not at_goal():
```

* Loop runs **until robot reaches the end**
* Handles unknown distance automatically

```python
if front_is_clear():
```

* Checks if the next step is safe
* Prevents unnecessary jumping

```python
move()
```

* Moves forward when no hurdle exists

```python
else:
    jump()
```

* Executes only when a hurdle blocks the path

---

### Logical flow (human reasoning)

| Step               | Decision      |
| ------------------ | ------------- |
| Is goal reached?   | No → continue |
| Is path clear?     | Yes → move    |
| Is there a hurdle? | Yes → jump    |
| Repeat             | Until goal    |

---

### Sample simulation (conceptual)

Assume path:

```
⬜ ⬜ 🚧 ⬜ 🚧 ⬜ ⬜ 🏁
```

Robot actions:

```
move
move
jump
move
jump
move
move
```

---

### Output (conceptual trace)

```
Moved forward
Moved forward
Jumped hurdle
Moved forward
Jumped hurdle
Moved forward
Moved forward
Reached goal
```

---

### Why this solution is optimal

| Reason   | Explanation                        |
| -------- | ---------------------------------- |
| Dynamic  | Works for any number of hurdles    |
| Clean    | No repeated code                   |
| Scalable | Path length doesn’t matter         |
| Logical  | Mirrors real-world decision making |

---

### Key takeaway

This challenge is **not about jumping**.
It is about:

* thinking in loops
* reacting to conditions
* writing future-proof logic

Once you understand this, most loop-based problems become straightforward.
