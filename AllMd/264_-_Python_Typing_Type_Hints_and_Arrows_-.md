## 1) The three core actions in the quiz

Your quiz revolves around exactly **three user-driven actions**:

1. **Select an answer**
2. **Submit the answer**
3. **Move to the next question**

Everything else (score, colors, progress) is a side effect of these actions.

---

## 2) Selecting an answer (pre-submit state)

Triggered by clicking an answer button:

```python
command=lambda idx=i: self.select_answer(idx)
```

### What `select_answer()` does

```python
def select_answer(index):
    highlight_selected_button()
    return index
```

Internally:

* Saves which option the user clicked
* Visually highlights it
* Does **not** evaluate correctness

Why this matters:

* The user can change their mind
* No score logic runs prematurely
* No state corruption

At this point:

* `submitted = False`
* `selected_index = index`

---

## 3) Submit button: dual behavior

The **Submit button changes role dynamically**.

### First click → Submit answer

### Second click → Next question

This is controlled by the `submitted` flag.

---

## 4) Submitting an answer (evaluation phase)

Triggered when:

```python
if not self.submitted:
    self.submit_answer()
```

### What happens step-by-step

1. **Validation**

```python
if selected_index is None:
    show warning
```

2. **Lock inputs**

```python
for btn in answer_buttons:
    btn.config(state="disabled")
```

3. **Find correct answer**

```python
correct_idx = current_options.index(correct_answer)
```

4. **Highlight correct answer**

* Green = correct
* Red = wrong selection (if any)

5. **Score update**

```python
if selected == correct_answer:
    score += 1
```

6. **Update UI**

* Score label
* Button text → `"Next"`

7. **State update**

```python
submitted = True
```

Now:

* Answer is frozen
* User cannot change selection
* Quiz is ready to advance

---

## 5) Clicking “Next” (progression phase)

Triggered when:

```python
if self.submitted:
    self.qn_index += 1
```

### What happens next

1. Increase question index
2. Check bounds:

```python
if qn_index >= total_questions:
    show final score
```

3. Otherwise:

```python
load_question()
```

This resets:

* Button states
* Selection
* Submit button text

And loads fresh data.

---

## 6) Loading the next question

Handled by `load_question()` in `quizlogic.py`.

### Responsibilities

* Pull the next question using `qn_index`
* Shuffle answers
* Reset all buttons
* Display question text
* Return:

  * correct answer
  * answer options
  * submission state reset

This ensures:

* Each question is independent
* No data leaks between questions

---

## 7) Why this flow is robust

Key design choices:

* **Single flag (`submitted`)** controls UI mode
* Index-driven question access
* Stateless logic functions
* UI only reacts to returned values

This avoids:

* Double scoring
* Skipped questions
* Accidental resubmissions
* Race conditions

---

## 8) Visual state vs logical state

| State Type | Example             |
| ---------- | ------------------- |
| Logical    | `submitted = True`  |
| Logical    | `qn_index = 3`      |
| Visual     | Button turns green  |
| Visual     | Button text changes |

Logical state always changes **first**, visuals follow.

This prevents visual glitches from breaking logic.

---

## 9) End of quiz detection

Handled centrally:

```python
if qn_index >= len(qn_bank):
    show_final_score()
```

No timers, no listeners, no hacks — just a boundary check.

---

## 10) Why this is the right design for this app

* Easy to reason about
* Linear and predictable
* Easy to extend (timers, review mode)
* Beginner-friendly but professional

---