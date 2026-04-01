### How to stop algorithms (like maze / hurdles) from *feeling* hard — practical mental techniques

---

### 1. Separate **language difficulty** from **logic difficulty**

Most frustration comes from mixing these two.

| What feels hard | What actually is hard |
| --------------- | --------------------- |
| Syntax          | Logic                 |
| Indentation     | Decision-making       |
| While loop      | Stop condition        |

Rule:

> If you can explain the solution in plain English, the algorithm is already solved.

Before code, force this sentence:

```
Until I reach the goal,
if this happens → do this,
else → do that.
```

If you can’t say this, coding will feel impossible.

---

### 2. Algorithms are not “math problems”, they are **rules**

Beginners think:

> “I must find the correct solution.”

Reality:

> “I must define consistent rules.”

Maze example:

* ❌ “How do I escape the maze?”
* ✅ “What rule do I follow at every step?”

Once rules are fixed, the loop just **executes discipline**, not intelligence.

---

### 3. Reduce every algorithm to 3 questions (always)

Never think about the full problem. Ask only:

1. **When do I stop?**
   → `at_goal()`, `i < n`, `input != 0`

2. **What do I check each time?**
   → `front_is_clear()`, `wall_in_front()`, `x > 5`

3. **What single action do I take?**
   → move / turn / increment / break

If one of these is missing → confusion + infinite loops.

---

### 4. While-loops feel hard because they are *honest*

`for` loops hide the stop condition.
`while` loops expose it.

That’s why your brain resists them.

Mental reframe:

> A `while` loop is just a guard standing at the door saying
> “You’re not allowed to continue unless this is true.”

Once the condition becomes false → escape is automatic.

---

### 5. You are NOT supposed to “see” the full execution

Beginners think good programmers:

* visualize the entire loop execution

False.

Good programmers:

* trust **invariants** (rules that stay true)

Maze invariant:

```
I never walk into a wall.
I always turn when blocked.
I always move when possible.
```

You don’t simulate everything — you trust the rule.

---

### 6. Write comments BEFORE code (this removes fear)

If code feels heavy, stop coding.

Write this first:

```python
# keep running until goal
# if right is open, take it
# else if front is open, move
# else turn left
```

Then convert line-by-line into code.

If you can’t comment it, you can’t code it yet.

---

### 7. Infinite loops are not a failure — they are feedback

An infinite loop means exactly one of these is wrong:

| Cause                        | Fix             |
| ---------------------------- | --------------- |
| Stop condition never changes | Update variable |
| Condition is wrong           | Check logic     |
| Action doesn’t progress      | Add move / turn |
| Indentation wrong            | Fix scope       |

Infinite loop ≠ “I’m bad”
Infinite loop = “One rule is missing”

---

### 8. Algorithms feel hard when you think in **steps**, not **states**

Bad thinking:

```
move
move
turn
move
```

Good thinking:

```
If blocked → turn
If free → move
Until done
```

Algorithms are **state-based**, not step-based.

---

### 9. You’re not slow — your brain is switching modes

Algorithmic thinking uses:

* delayed gratification
* abstraction
* patience with uncertainty

This is cognitively expensive.

Feeling tired or frustrated = **normal adaptation**, not weakness.

---

### 10. One cheat rule to stay calm

Whenever stuck, say this out loud:

> “What must be true for this loop to stop?”

If you answer that clearly, 70% of algorithm fear disappears.

---

### 11. What you’re already doing right (important)

Based on your progress so far:

* You understand **conditions**
* You understand **while**
* You can follow **rules**
* You ask about **edge cases** (this is advanced thinking)

The discomfort you feel is exactly what happens **right before clarity**.

---

### Final mental anchor (keep this)

> Algorithms are not hard problems.
> They are strict rules executed patiently.
> Your job is not to be clever — only to be consistent.
