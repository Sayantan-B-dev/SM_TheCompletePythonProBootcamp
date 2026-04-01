## STEP 4 — Define the **Game Orchestrator** (Flow + Coordination)

> Step 4 is where **everything comes together**, but nothing new is invented.
> The `Game` class **does not own data** — it **coordinates objects**.

No business logic duplication.
No deep calculations.
Only **flow control and delegation**.

---

## 1. Purpose of Step 4

This step answers:

* Who controls the game loop?
* Who talks to the player?
* Who connects `Question`, `Quiz`, and `Player`?
* Where does input/output live?

The answer to all: **Game**

---

## 2. Responsibilities of the `Game` Class

> A `Game` object is a **conductor**, not a performer.

### It MUST:

* start the quiz
* fetch questions from `Quiz`
* ask questions to the user
* collect input
* validate answers via `Question`
* update score via `Player`
* decide when the game ends

### It MUST NOT:

* store questions directly
* validate answers itself
* manage scoring logic internally

---

## 3. Attributes Planning (Wiring Objects Together)

| Attribute | Type     | Why it exists             |
| --------- | -------- | ------------------------- |
| `quiz`    | `Quiz`   | Provides questions        |
| `player`  | `Player` | Tracks score and identity |

The `Game` owns **references**, not raw data.

---

## 4. Methods Planning (Flow Control)

| Method              | Purpose                    |
| ------------------- | -------------------------- |
| `start()`           | Run the full game loop     |
| `_play_round()`     | Handle one question cycle  |
| `_get_user_input()` | Centralized input handling |

Methods prefixed with `_` are **internal helpers**.

---

## 5. Implementing Step 4 — Code

```python
class Game:
    def __init__(self, quiz, player):
        """
        Constructor receives already-created
        Quiz and Player objects.
        """
        self.quiz = quiz
        self.player = player

    def start(self):
        """
        Main game loop.
        Runs until there are no more questions.
        """
        print(f"Welcome, {self.player.name}!")

        while self.quiz.has_more_questions():
            self._play_round()

        print("Quiz finished.")
        print(f"Final Score: {self.player.get_score()}")

    def _play_round(self):
        """
        Handles one question cycle:
        - display question
        - get user input
        - validate answer
        - update score
        - move to next question
        """
        question = self.quiz.get_current_question()
        question.display()

        user_choice = self._get_user_input()

        if question.is_correct(user_choice):
            print("Correct!\n")
            self.player.increment_score()
        else:
            print("Wrong!\n")

        self.quiz.next_question()

    def _get_user_input(self):
        """
        Handles and validates user input.
        Ensures input is a valid integer choice.
        """
        while True:
            try:
                choice = int(input("Enter option number: "))
                return choice
            except ValueError:
                print("Invalid input. Please enter a number.")
```

---

## 6. Testing Step 4 (Integration Test)

> This is the **first time** multiple objects talk together.

```python
questions = [
    Question("Capital of India?", ["Mumbai", "Delhi", "Chennai"], 2),
    Question("5 * 2 = ?", ["8", "10", "12"], 2)
]

quiz = Quiz(questions)
player = Player("Amit")

game = Game(quiz, player)
game.start()
```

---

## 7. Expected Output (Sample Run)

```
Welcome, Amit!
Capital of India?
1. Mumbai
2. Delhi
3. Chennai
Enter option number: 2
Correct!

5 * 2 = ?
1. 8
2. 10
3. 12
Enter option number: 2
Correct!

Quiz finished.
Final Score: 2
```

---

## 8. Why This Design Is Correct (Deep Reasoning)

### Delegation Map

| Action             | Who handles it |
| ------------------ | -------------- |
| Display question   | `Question`     |
| Validate answer    | `Question`     |
| Track score        | `Player`       |
| Sequence questions | `Quiz`         |
| Input / Output     | `Game`         |

No overlap.
No confusion.
No god class.

---

## 9. Common Step 4 Mistakes (Avoid These)

| Mistake                   | Why It’s Harmful     |
| ------------------------- | -------------------- |
| Scoring logic in Game     | Breaks encapsulation |
| Answer validation in Game | Duplication          |
| Direct access to `score`  | Unsafe mutation      |
| Printing inside Player    | UI leakage           |

---

## 10. Mental Lock-In for Step 4

> “Game **asks**, others **answer**.”

If the `Game` starts *thinking* instead of *coordinating*, step back.

---

## 11. Step 4 Completion Checklist

* Objects are composed correctly
* Flow is readable top-to-bottom
* Each class does only its job
* System works end-to-end

The system is now **functionally complete**.

Only **Step 5** remains — refinement, robustness, and polish.
