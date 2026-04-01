## 1) Where the flow starts

The flow begins in **`main.py`**, when the user clicks **Start Quiz**.

At this moment:

* The user’s choices (amount, category, difficulty, type) are collected
* These values are converted into API-compatible values
* A single configuration dictionary is created

Example (conceptually):

```python
config = {
    "amount": 10,
    "category": 18,
    "difficulty": "easy",
    "type": "multiple"
}
```

This `config` object is passed **unchanged** into `QuizUI`.

Important:
From this point onward, **UI never asks the user anything again**. Everything is driven by data.

---

## 2) Fetching trivia questions (questions.py)

Inside `QuizUI`, questions are loaded by creating a `Question` object:

```python
self.question_data = Question(
    amount,
    category,
    difficulty,
    q_type
)
```

### What happens internally

1. The Open Trivia API is called with the given parameters
2. The API returns raw JSON data
3. Each question is **cleaned and normalized**
4. The final result is stored in:

```python
self.question_data.question_data
```

This becomes a **list of question dictionaries**.

Example of ONE question after processing:

```python
{
    "question": "What does CPU stand for?",
    "correct_answer": "Central Processing Unit",
    "incorrect_answers": [
        "Computer Personal Unit",
        "Central Process Utility",
        "Control Processing Unit"
    ]
}
```

At this stage:

* No UI logic exists
* No score logic exists
* Only **pure data**

This is a critical separation.

---

## 3) Question bank creation (QuizUI)

Back in `quiz_ui.py`:

```python
self.qn_bank = self.question_data.question_data
self.qn_index = 0
```

Meaning:

* `qn_bank` = full list of questions
* `qn_index` = which question we are currently on

This index drives the entire quiz progression.

---

## 4) Loading a question (quizlogic.py → load_question)

Each question is displayed by calling:

```python
load_question(
    qn_index,
    qn_bank,
    question_label,
    answer_buttons,
    next_button
)
```

### What `load_question()` does internally

1. Picks the current question:

```python
q = qn_bank[qn_index]
```

2. Extracts the correct answer:

```python
correct_answer = q["correct_answer"]
```

3. Builds the options list:

```python
options = q["incorrect_answers"] + [correct_answer]
```

4. Randomizes answer order:

```python
random.shuffle(options)
```

Why this matters:

* The correct answer is **never at a fixed position**
* Prevents pattern memorization

5. Updates UI:

* Question text
* Answer button labels
* Resets button states
* Sets button text to “Submit”

6. Returns important state values:

```python
return correct_answer, options, False, False
```

Meaning:

* `correct_answer`: saved for evaluation later
* `options`: current shuffled answers
* `submitted = False`: user hasn’t answered yet
* `quiz_finished = False`

---

## 5) Selecting an answer (user interaction)

When the user clicks an answer button:

```python
select_answer(index, submitted, answer_buttons)
```

### What happens here

* If the question is already submitted → ignore
* Otherwise:

  * Reset all button backgrounds
  * Highlight the selected button
  * Save the selected index

Important:

* **No correctness check happens here**
* This function only handles **selection state**

This prevents premature evaluation.

---

## 6) Submitting an answer (core logic)

When the user clicks **Submit**:

```python
submit_answer(
    selected_index,
    submitted,
    current_options,
    correct_answer,
    answer_buttons,
    score,
    score_label,
    next_button
)
```

### Internal flow step-by-step

1. Validate selection:

```python
if selected_index is None:
    show warning
```

2. Disable all answer buttons:

```python
for btn in answer_buttons:
    btn.config(state="disabled")
```

This locks the answer.

3. Find correct answer index:

```python
correct_idx = current_options.index(correct_answer)
```

4. Highlight correct answer (green)

5. Compare user choice:

```python
if current_options[selected_index] == correct_answer:
    score += 1
else:
    highlight selected answer in red
```

6. Update score label

7. Change button text:

```python
next_button.config(text="Next")
```

8. Return updated state:

```python
return score, True
```

Meaning:

* Score updated
* Question is now **submitted**

---

## 7) Moving to the next question

On next button click (after submission):

```python
self.qn_index += 1
```

Then:

* If index < total questions → load next question
* Else → quiz ends

This makes the quiz **strictly linear and deterministic**.

---

## 8) End of quiz flow

When `qn_index` reaches the end:

```python
percentage = (score / total_questions) * 100
```

Final results shown:

* Score
* Percentage
* Grade

The window is then closed cleanly.

---

## 9) Why this flow is solid

Key strengths of your design:

* Question data is immutable during play
* Correct answer is never exposed early
* UI never decides correctness
* Logic never touches API
* No hidden state mutations

Every step is:
**Load → Select → Submit → Evaluate → Advance**

---
