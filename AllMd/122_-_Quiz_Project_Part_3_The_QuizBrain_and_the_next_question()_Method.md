## STEP 3 — Define the **Quiz Controller** (Question Sequencing Engine)

> Step 3 is about **managing questions**, not players and not game flow.
> The `Quiz` object is responsible for **order, progression, and access**.

No scoring.
No user input.
No printing results.
Only **question sequencing and control**.

---

## 1. Purpose of Step 3

This step answers:

* How are multiple questions stored?
* How do we know which question is active?
* How do we safely move forward?
* How do we detect the end?

If sequencing is solid, the game loop becomes trivial later.

---

## 2. Responsibilities of the `Quiz` Class

> A `Quiz` object controls **what question comes next**.

### It MUST:

* store a collection of `Question` objects
* track the current position
* provide the current question
* move to the next question
* report when the quiz is finished

### It MUST NOT:

* validate answers
* update player score
* ask for user input
* print final results

---

## 3. Attributes Planning (Internal State)

| Attribute       | Type             | Why it exists      |
| --------------- | ---------------- | ------------------ |
| `questions`     | `list[Question]` | Holds quiz content |
| `current_index` | `int`            | Tracks progress    |

> Index starts at **0**, not 1 — this is internal logic.

---

## 4. Methods Planning (Behavior)

| Method                   | Purpose                               |
| ------------------------ | ------------------------------------- |
| `has_more_questions()`   | Check if quiz should continue         |
| `get_current_question()` | Fetch active question                 |
| `next_question()`        | Advance to next question              |
| `reset()`                | Restart quiz (optional but important) |

---

## 5. Implementing Step 3 — Code

```python
class Quiz:
    def __init__(self, questions):
        """
        Constructor receives a list of Question objects.
        Initializes the quiz at the first question.
        """
        self.questions = questions
        self.current_index = 0

    def has_more_questions(self):
        """
        Returns True if there are still questions left.
        Prevents index overflow.
        """
        return self.current_index < len(self.questions)

    def get_current_question(self):
        """
        Returns the current Question object.
        Assumes caller has checked has_more_questions().
        """
        return self.questions[self.current_index]

    def next_question(self):
        """
        Moves the quiz pointer to the next question.
        """
        self.current_index += 1

    def reset(self):
        """
        Resets quiz progression back to start.
        """
        self.current_index = 0
```

---

## 6. Testing the Quiz in Isolation

> The Quiz must work **without Player or Game**.

```python
q1 = Question("1 + 1 = ?", ["1", "2", "3"], 2)
q2 = Question("2 + 2 = ?", ["2", "3", "4"], 3)

quiz = Quiz([q1, q2])

while quiz.has_more_questions():
    question = quiz.get_current_question()
    question.display()
    quiz.next_question()
```

---

## 7. Expected Output

```
1 + 1 = ?
1. 1
2. 2
3. 3

2 + 2 = ?
1. 2
2. 3
3. 4
```

---

## 8. Why `Quiz` Is a Controller, Not a Model

| Class      | Role                    |
| ---------- | ----------------------- |
| `Question` | Data + validation       |
| `Player`   | State holder            |
| `Quiz`     | Flow control (sequence) |

This separation:

* avoids god classes
* makes testing easier
* enables extensions (shuffle, categories)

---

## 9. Common Design Mistakes (Avoid These)

| Mistake           | Why It Breaks Design            |
| ----------------- | ------------------------------- |
| Score inside Quiz | Leaks responsibility            |
| Input inside Quiz | Mixes UI with logic             |
| Printing results  | Game should decide presentation |
| Using globals     | Breaks testability              |

---

## 10. Extension Hooks (Future-Proofing)

Without changing current logic, you can later add:

```python
import random
random.shuffle(self.questions)
```

or timed quizzes, categories, difficulty filters.

---

## 11. Mental Lock-In for Step 3

> “A Quiz object knows **where you are**, not **how well you’re doing**.”

If Quiz starts caring about score or players, step back.

---

## 12. Step 3 Completion Checklist

* Questions are sequenced cleanly
* Progression is safe and bounded
* Fully testable in isolation
* No player or UI logic

