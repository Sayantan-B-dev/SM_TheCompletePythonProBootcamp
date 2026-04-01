## STEP 5 — Refinement, Robustness, and Professional Polish

> Step 5 does **not** change the architecture.
> It **strengthens**, **hardens**, and **professionalizes** what already works.

No new core classes.
No redesign.
Only **quality upgrades**.

---

## 1. Purpose of Step 5

This step answers:

* How do we make the game safer against bad input?
* How do we make replay possible?
* How do we improve clarity and extensibility?
* How do we make the code feel *production-ready*?

---

## 2. Add Input Validation at the Question Level

### Problem

Currently:

* User can enter `99`
* Question silently marks it wrong
* UX is poor

### Design Rule

> Validation close to the data it protects.

---

### Upgrade `Question.is_correct()`

```python
class Question:
    def __init__(self, text, options, correct_index):
        self.text = text
        self.options = options
        self.correct_index = correct_index

    def display(self):
        print(self.text)
        for index, option in enumerate(self.options, start=1):
            print(f"{index}. {option}")

    def is_valid_choice(self, choice):
        """
        Checks if the user's choice is within option range.
        """
        return 1 <= choice <= len(self.options)

    def is_correct(self, choice):
        """
        Assumes choice is already validated.
        """
        return choice == self.correct_index
```

---

## 3. Strengthen Input Handling in `Game`

### Improved `_get_user_input()` (Context-Aware)

```python
class Game:
    ...

    def _get_user_input(self, question):
        """
        Keeps asking until user enters a valid option number.
        """
        while True:
            try:
                choice = int(input("Enter option number: "))
                if question.is_valid_choice(choice):
                    return choice
                else:
                    print("Choice out of range. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")
```

---

### Update `_play_round()` Accordingly

```python
    def _play_round(self):
        question = self.quiz.get_current_question()
        question.display()

        user_choice = self._get_user_input(question)

        if question.is_correct(user_choice):
            print("Correct!\n")
            self.player.increment_score()
        else:
            print("Wrong!\n")

        self.quiz.next_question()
```

---

## 4. Add Replay Capability (Professional Feature)

### Why Replay Matters

* Demonstrates state reset
* Proves object independence
* Common interview expectation

---

### Extend `Game.start()`

```python
    def start(self):
        while True:
            self._run_quiz()

            print(f"Final Score: {self.player.get_score()}")

            choice = input("Play again? (y/n): ").lower()
            if choice != "y":
                break

            self._reset_game()

    def _run_quiz(self):
        print(f"\nWelcome, {self.player.name}!\n")
        while self.quiz.has_more_questions():
            self._play_round()

    def _reset_game(self):
        """
        Resets player score and quiz progress.
        """
        self.player.reset_score()
        self.quiz.reset()
```

---

## 5. Add Defensive Checks in `Quiz`

### Prevent Silent Failures

```python
class Quiz:
    def __init__(self, questions):
        if not questions:
            raise ValueError("Quiz must have at least one question")

        self.questions = questions
        self.current_index = 0
```

This prevents:

* empty quizzes
* runtime confusion

---

## 6. Optional: Shuffle Questions (Zero Architecture Change)

```python
import random

class Quiz:
    def __init__(self, questions, shuffle=False):
        if shuffle:
            random.shuffle(questions)

        self.questions = questions
        self.current_index = 0
```

This adds variability **without touching Game or Question**.

---

## 7. Final Integrated Run (Full System Test)

### Setup

```python
questions = [
    Question("Capital of India?", ["Mumbai", "Delhi", "Chennai"], 2),
    Question("Python is a ___ language?", ["Compiled", "Interpreted", "Markup"], 2),
]

quiz = Quiz(questions, shuffle=True)
player = Player("Amit")
game = Game(quiz, player)

game.start()
```

---

## 8. Expected Output (Sample Session)

```
Welcome, Amit!

Capital of India?
1. Mumbai
2. Delhi
3. Chennai
Enter option number: 5
Choice out of range. Try again.
Enter option number: 2
Correct!

Python is a ___ language?
1. Compiled
2. Interpreted
3. Markup
Enter option number: two
Invalid input. Enter a number.
Enter option number: 2
Correct!

Final Score: 2
Play again? (y/n): n
```

---

## 9. What Step 5 Achieved (Engineering View)

| Aspect         | Improvement |
| -------------- | ----------- |
| Input safety   | Strong      |
| Replay support | Added       |
| Error handling | Defensive   |
| Extensibility  | Preserved   |
| Architecture   | Untouched   |

This is the mark of **good OOP design**.

---

## 10. Final Mental Lock-In (Most Important Insight)

> Steps 1–4 build **structure**
> Step 5 builds **confidence**

If future features feel easy to add,
the design is successful.
