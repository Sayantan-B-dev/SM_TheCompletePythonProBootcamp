## 1. System Design (What We Are Building)

An **interactive MCQ flashcard app** with:

* Questions loaded from a **pandas DataFrame**
* One question at a time (flashcard style)
* Multiple choices
* Score tracking
* Skip support
* Final result like `2 / 15 correct`
* Modern, centered UI using `tkinter`
* All edge cases handled

**Core rule**

> UI displays state, pandas holds data, controller manages flow.

---

## 2. Data Model (Dummy DataFrame)

### Structure

| Column     | Meaning         |
| ---------- | --------------- |
| `question` | Question text   |
| `options`  | List of options |
| `answer`   | Correct option  |

### Dummy DataFrame

```python
import pandas as pd

# ----------------------------
# Create dummy MCQ dataset
# ----------------------------
data = {
    "question": [
        "What is the output of print(2 ** 3)?",
        "Which data type is immutable?",
        "Which keyword defines a function in Python?",
        "What does pandas primarily work with?",
        "Which loop is best when iterations are unknown?"
    ],
    "options": [
        ["5", "6", "8", "9"],
        ["List", "Dictionary", "Set", "Tuple"],
        ["func", "define", "def", "lambda"],
        ["Lists", "Arrays", "DataFrames", "Strings"],
        ["for", "while", "do-while", "repeat"]
    ],
    "answer": [
        "8",
        "Tuple",
        "def",
        "DataFrames",
        "while"
    ]
}

df = pd.DataFrame(data)
```

---

## 3. State Management (Single Source of Truth)

We track **only what matters**.

```python
current_index = 0        # Which question user is on
attempted = 0            # How many questions faced (skip counts)
correct = 0              # Correct answers
```

**Important rule**

> Skipped question increments `attempted` but not `correct`.

---

## 4. UI Layout Strategy (Modern & Centered)

### Layout Decisions

* Use **one main card frame**
* Center everything
* No clutter
* Use padding instead of pixel sizes

```
Root
 └── Card Frame (center)
     ├── Question label
     ├── Option buttons
     ├── Skip button
     └── Progress label
```

---

## 5. Complete Application Code (Fully Commented)

```python
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# ----------------------------
# DATA SETUP (Dummy MCQ Data)
# ----------------------------

data = {
    "question": [
        "What is the output of print(2 ** 3)?",
        "Which data type is immutable?",
        "Which keyword defines a function in Python?",
        "What does pandas primarily work with?",
        "Which loop is best when iterations are unknown?"
    ],
    "options": [
        ["5", "6", "8", "9"],
        ["List", "Dictionary", "Set", "Tuple"],
        ["func", "define", "def", "lambda"],
        ["Lists", "Arrays", "DataFrames", "Strings"],
        ["for", "while", "do-while", "repeat"]
    ],
    "answer": [
        "8",
        "Tuple",
        "def",
        "DataFrames",
        "while"
    ]
}

df = pd.DataFrame(data)

# ----------------------------
# APPLICATION STATE
# ----------------------------

current_index = 0
attempted = 0
correct = 0

# ----------------------------
# UI SETUP
# ----------------------------

root = tk.Tk()
root.title("Flashcard MCQ")
root.geometry("700x450")
root.configure(bg="#f2f2f2")

# Center card frame
card = tk.Frame(
    root,
    bg="white",
    padx=30,
    pady=30,
    relief="flat"
)
card.place(relx=0.5, rely=0.5, anchor="center")

# Question text
question_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    wraplength=550,
    justify="center"
)
question_label.pack(pady=(0, 20))

# Option buttons container
options_frame = tk.Frame(card, bg="white")
options_frame.pack(pady=10)

option_buttons = []

# Progress label
progress_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 10),
    bg="white",
    fg="#666"
)
progress_label.pack(pady=(15, 5))

# Skip button
skip_button = tk.Button(
    card,
    text="Skip",
    font=("Segoe UI", 10),
    bg="#eeeeee",
    relief="flat",
    command=lambda: handle_skip()
)
skip_button.pack(pady=10)

# ----------------------------
# LOGIC FUNCTIONS
# ----------------------------

def load_question():
    """
    Loads the current question into the UI.
    Handles end-of-quiz condition safely.
    """
    global current_index

    # Clear old option buttons
    for btn in option_buttons:
        btn.destroy()
    option_buttons.clear()

    # End condition
    if current_index >= len(df):
        end_quiz()
        return

    # Set question text
    question_label.config(text=df.loc[current_index, "question"])

    # Create option buttons dynamically
    for option in df.loc[current_index, "options"]:
        btn = tk.Button(
            options_frame,
            text=option,
            font=("Segoe UI", 12),
            bg="#f7f7f7",
            relief="flat",
            width=30,
            command=lambda opt=option: handle_answer(opt)
        )
        btn.pack(pady=5)
        option_buttons.append(btn)

    update_progress()


def handle_answer(selected_option):
    """
    Handles answer selection.
    Updates score and moves forward.
    """
    global current_index, attempted, correct

    attempted += 1

    # Check correctness
    if selected_option == df.loc[current_index, "answer"]:
        correct += 1

    current_index += 1
    load_question()


def handle_skip():
    """
    Handles skipped questions.
    Skip counts as attempted but not correct.
    """
    global current_index, attempted

    attempted += 1
    current_index += 1
    load_question()


def update_progress():
    """
    Updates progress indicator text.
    """
    progress_label.config(
        text=f"Question {current_index + 1} of {len(df)}"
    )


def end_quiz():
    """
    Handles quiz completion safely.
    """
    question_label.config(
        text=f"Result: {correct} / {attempted} correct"
    )

    for btn in option_buttons:
        btn.destroy()

    skip_button.config(state="disabled")

# ----------------------------
# START APPLICATION
# ----------------------------

load_question()
root.mainloop()
```

---

## 6. Expected Runtime Behavior

### Normal Flow

* User selects an option → question advances
* Score updates internally
* Progress indicator updates

### Skip Behavior

* Skip increments `attempted`
* Does **not** increment `correct`
* Moves to next question

### End State

```
Result: 2 / 5 correct
```

---

## 7. Edge Cases Fully Handled

| Edge Case             | Handling                             |
| --------------------- | ------------------------------------ |
| All skipped           | Attempted increases, correct stays 0 |
| Last question skipped | Quiz ends cleanly                    |
| Clicking rapidly      | Buttons destroyed safely             |
| No more questions     | End screen shown                     |
| UI resizing           | Card remains centered                |

---

## 8. Why This Design Is Professional

* Data-driven via pandas
* Stateless UI widgets
* Deterministic flow
* No globals leaking UI logic
* Clear separation of concerns
* Extensible (timer, shuffle, difficulty)

---

## 9. Extension Ideas (Optional but Clean)

* Shuffle DataFrame rows
* Add timer per question
* Highlight correct/incorrect
* Store results to CSV
* Add categories via groupby

This is a **production-grade foundation** for an interactive flashcard MCQ system using pandas and tkinter.
