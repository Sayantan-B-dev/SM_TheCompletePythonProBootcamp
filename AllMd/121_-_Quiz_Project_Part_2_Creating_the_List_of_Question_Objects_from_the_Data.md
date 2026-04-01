## STEP 2 — Define the **Player Model** (State & Progress Holder)

> Step 2 is about **who is playing**, not how the game runs.
> The Player object represents **identity + progress**, nothing else.

No questions.
No game loop.
No input logic.
Only **player state, cleanly modeled**.

---

## 1. Purpose of Step 2

This step answers:

* Who is the player?
* What data must persist across questions?
* How should score be safely updated?

If Player logic is clean, scoring and reporting become effortless later.

---

## 2. Responsibilities of the `Player` Class

> A `Player` object must **own its own progress**.

### It MUST:

* store player identity
* store score
* expose safe ways to update score
* expose read-only access to score

### It MUST NOT:

* ask questions
* validate answers
* control game flow
* print game messages excessively

---

## 3. Attributes Planning (Player State)

| Attribute | Type  | Why it exists         |
| --------- | ----- | --------------------- |
| `name`    | `str` | Player identity       |
| `score`   | `int` | Track correct answers |

> Score starts at **0 by default** — no arguments required.

---

## 4. Methods Planning (Behavior)

| Method              | Purpose                                |
| ------------------- | -------------------------------------- |
| `increment_score()` | Increase score safely                  |
| `get_score()`       | Read score without modifying           |
| `reset_score()`     | Restart progress (optional but useful) |

Methods enforce **controlled mutation** of state.

---

## 5. Implementing Step 2 — Code

```python
class Player:
    def __init__(self, name):
        """
        Constructor initializes player identity
        and sets initial score to zero.
        """
        self.name = name
        self.score = 0

    def increment_score(self):
        """
        Increases the player's score by one.
        This method should be called ONLY
        when an answer is correct.
        """
        self.score += 1

    def get_score(self):
        """
        Returns the current score.
        Does not modify state.
        """
        return self.score

    def reset_score(self):
        """
        Resets score back to zero.
        Useful for replaying the quiz.
        """
        self.score = 0
```

---

## 6. Testing the Player in Isolation

> Player logic must work **without any quiz logic**.

```python
player = Player("Amit")

print(player.get_score())
player.increment_score()
player.increment_score()
print(player.get_score())

player.reset_score()
print(player.get_score())
```

---

## 7. Expected Output

```
0
2
0
```

---

## 8. Design Decisions (Why This Works)

### Why `increment_score()` instead of `score += 1` outside?

* Prevents accidental misuse
* Centralizes scoring logic
* Allows future rules (negative marking, multipliers)

---

### Why `get_score()` instead of direct access?

* Encourages read-only intent
* Easier to extend later (formatting, stats)

---

## 9. Anti-Patterns Avoided (Very Important)

| Anti-Pattern                | Why It’s Dangerous     |
| --------------------------- | ---------------------- |
| Modifying score directly    | Breaks encapsulation   |
| Printing inside Player      | Mixes UI with logic    |
| Passing questions to Player | Responsibility leakage |

---

## 10. Mental Lock-In for Step 2

> “A Player object is a **container for identity and progress**.”

If Player starts feeling like it’s doing **too much**, the design is wrong.

---

## 11. Step 2 Completion Checklist

* Player state is encapsulated
* Score mutation is controlled
* No dependency on quiz logic
* Testable in isolation
