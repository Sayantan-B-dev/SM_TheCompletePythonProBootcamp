## `quiz_game/` — Full Modular OOP Quiz Game (Terminal, Open Trivia DB)

Directory structure (exact):

```
quiz_game/
│
├── main.py
├── game.py
├── quiz.py
├── question.py
├── player.py
└── trivia_api.py
```

All files below are **complete**, **ready to run**, and **modular**.

---

## `question.py` — Question Model

```python
class Question:
    def __init__(self, text, options, correct_index):
        """
        Represents a single quiz question.

        text          : Question string
        options       : List of answer options
        correct_index : 1-based index of the correct option
        """
        self.text = text
        self.options = options
        self.correct_index = correct_index

    def display(self):
        """
        Displays the question and options
        in a clean, readable terminal format.
        """
        print("\n" + "=" * 60)
        print(self.text)
        print("-" * 60)

        for i, option in enumerate(self.options, start=1):
            print(f"  {i}. {option}")

        print("=" * 60)

    def is_valid_choice(self, choice):
        """
        Ensures the user input is within valid range.
        """
        return 1 <= choice <= len(self.options)

    def is_correct(self, choice):
        """
        Checks if the chosen option is correct.
        """
        return choice == self.correct_index
```

---

## `player.py` — Player Model

```python
class Player:
    def __init__(self, name):
        """
        Stores player identity and score.
        """
        self.name = name
        self.score = 0

    def increment_score(self):
        """
        Increases score by one.
        """
        self.score += 1

    def reset_score(self):
        """
        Resets score to zero.
        """
        self.score = 0

    def get_score(self):
        """
        Returns current score.
        """
        return self.score
```

---

## `quiz.py` — Quiz Controller (Sequencing Engine)

```python
class Quiz:
    def __init__(self, questions):
        """
        Controls question order and progression.
        """
        if not questions:
            raise ValueError("Quiz must contain at least one question.")

        self.questions = questions
        self.current_index = 0

    def has_more_questions(self):
        """
        Checks if questions remain.
        """
        return self.current_index < len(self.questions)

    def get_current_question(self):
        """
        Returns the active Question object.
        """
        return self.questions[self.current_index]

    def next_question(self):
        """
        Advances to the next question.
        """
        self.current_index += 1

    def reset(self):
        """
        Resets quiz progression.
        """
        self.current_index = 0

    def total_questions(self):
        """
        Returns total number of questions.
        """
        return len(self.questions)
```

---

## `trivia_api.py` — Open Trivia Database Integration

```python
import requests
import html
import random

from question import Question


TRIVIA_API_URL = "https://opentdb.com/api.php"


def fetch_questions(amount=5, difficulty="medium"):
    """
    Fetches questions from Open Trivia Database
    and converts them into Question objects.
    """
    params = {
        "amount": amount,
        "type": "multiple",
        "difficulty": difficulty
    }

    response = requests.get(TRIVIA_API_URL, params=params)
    data = response.json()

    questions = []

    for item in data["results"]:
        question_text = html.unescape(item["question"])
        correct_answer = html.unescape(item["correct_answer"])
        incorrect_answers = [
            html.unescape(ans) for ans in item["incorrect_answers"]
        ]

        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        correct_index = options.index(correct_answer) + 1

        questions.append(
            Question(
                question_text,
                options,
                correct_index
            )
        )

    return questions
```

---

## `game.py` — Game Orchestrator (UI + Flow)

```python
class Game:
    def __init__(self, quiz, player):
        """
        Coordinates quiz flow, input, and scoring.
        """
        self.quiz = quiz
        self.player = player

    def start(self):
        """
        Main entry point for the game.
        """
        self._clear_screen()
        print("=" * 60)
        print(f"           QUIZ GAME — Welcome {self.player.name}")
        print("=" * 60)

        while self.quiz.has_more_questions():
            self._play_round()

        self._show_final_score()

    def _play_round(self):
        """
        Executes one full question cycle.
        """
        question = self.quiz.get_current_question()
        question.display()

        user_choice = self._get_user_input(question)

        if question.is_correct(user_choice):
            print("\n✔ Correct!")
            self.player.increment_score()
        else:
            print("\n✘ Wrong!")

        self.quiz.next_question()
        self._show_progress()

        input("\nPress ENTER to continue...")
        self._clear_screen()

    def _get_user_input(self, question):
        """
        Safely handles numeric input.
        """
        while True:
            try:
                choice = int(input("Your answer (number): "))
                if question.is_valid_choice(choice):
                    return choice
                print("Invalid option number.")
            except ValueError:
                print("Please enter a valid number.")

    def _show_progress(self):
        """
        Displays running score in score/total format.
        """
        answered = self.quiz.current_index
        total = self.quiz.total_questions()
        score = self.player.get_score()

        print("\n" + "-" * 60)
        print(f"Score: {score}/{answered}    Progress: {answered}/{total}")
        print("-" * 60)

    def _show_final_score(self):
        """
        Displays final result summary.
        """
        print("\n" + "=" * 60)
        print("                 QUIZ COMPLETED")
        print("=" * 60)
        print(f"Final Score: {self.player.get_score()}/{self.quiz.total_questions()}")
        print("=" * 60)

    def _clear_screen(self):
        """
        Clears terminal screen (cross-platform).
        """
        import os
        os.system("cls" if os.name == "nt" else "clear")
```

---

## `main.py` — Entry Point

```python
from trivia_api import fetch_questions
from quiz import Quiz
from player import Player
from game import Game


def main():
    """
    Application entry point.
    """
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"

    questions = fetch_questions(amount=5, difficulty="medium")

    quiz = Quiz(questions)
    player = Player(name)
    game = Game(quiz, player)

    game.start()


if __name__ == "__main__":
    main()
```

---

## Sample Terminal Session (Expected UX)

```
============================================================
           QUIZ GAME — Welcome Amit
============================================================

What is the capital of Australia?
------------------------------------------------------------
  1. Sydney
  2. Melbourne
  3. Canberra
  4. Perth
============================================================
Your answer (number): 3

✔ Correct!
------------------------------------------------------------
Score: 1/1    Progress: 1/5
------------------------------------------------------------

Press ENTER to continue...
```

---

## Key Design Guarantees

* Fully modular OOP design
* Open Trivia DB live questions
* Clean terminal UI/UX
* Score shown as `{score}/{answered}` after every question
* Easily extendable (timer, categories, difficulty, leaderboard)

This is **production-grade OOP structure**, not a toy script.
