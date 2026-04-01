## 1) Why HTML entities exist in trivia data

The Open Trivia Database stores questions in a **web-safe format**.
That means special characters are encoded as HTML entities.

Examples returned by the API:

```
What does &quot;CPU&quot; stand for?
Who invented C&#039;s predecessor language?
```

If shown directly in Tkinter:

* Quotes appear as `&quot;`
* Apostrophes appear as `&#039;`
* Symbols look broken

This is **not a UI problem** — it’s a **data normalization problem**.

So your app fixes it **once**, at the data layer.

---

## 2) Where HTML unescaping happens (single source of truth)

Unescaping is handled in **exactly one place**:

`quiz_constants.py`

```python
from html import unescape

def clean_html_text(text):
    return unescape(text)
```

Why this is important:

* No UI file needs to know about HTML
* No logic file repeats cleanup
* Text is cleaned **once and only once**

This prevents double-unescaping bugs.

---

## 3) When unescaping happens (timing matters)

Unescaping happens in **questions.py**, immediately after the API response is received.

```python
def clean_data(self, data):
    cleaned = []
    for q in data:
        cleaned.append({
            "question": clean_html_text(q["question"]),
            "correct_answer": clean_html_text(q["correct_answer"]),
            "incorrect_answers": [
                clean_html_text(a) for a in q["incorrect_answers"]
            ],
        })
    return cleaned
```

Key point:

> **Raw API data never leaves `questions.py`**

From this moment forward:

* All text is normal Python strings
* No HTML entities exist anywhere else in the app

---

## 4) Resulting internal data format (normalized)

After cleaning, the app works only with this structure:

```python
{
    "question": "What does \"CPU\" stand for?",
    "correct_answer": "Central Processing Unit",
    "incorrect_answers": [
        "Computer Personal Unit",
        "Central Process Utility",
        "Control Processing Unit"
    ]
}
```

This format is:

* Human-readable
* UI-safe
* Logic-safe
* Immutable during gameplay

---

## 5) How formatting stays consistent in the UI

Once text is unescaped:

### Question text formatting

```python
tk.Label(
    text=question_text,
    wraplength=640,
    justify="center"
)
```

Why this works reliably:

* Unescaped strings contain real characters
* Tkinter’s text wrapping works correctly
* Quotes, punctuation, symbols behave normally

If text were still escaped:

* Wrapping would be visually broken
* Width calculations would be wrong

---

### Answer button formatting

```python
btn.config(text=option)
```

Because options are already cleaned:

* Button width stays consistent
* Highlight colors apply cleanly
* No layout jumps occur

---

## 6) Full dataflow (end-to-end)

Here is the **complete lifecycle of question text**:

### Step 1 — API returns raw HTML text

```
"What does &quot;CPU&quot; stand for?"
```

### Step 2 — `questions.py` cleans it

```python
clean_html_text(text)
```

Becomes:

```
"What does "CPU" stand for?"
```

### Step 3 — Stored in `qn_bank`

```python
self.qn_bank = cleaned_questions
```

### Step 4 — Passed into `quizlogic.load_question`

```python
q = qn_bank[qn_index]
```

### Step 5 — Rendered in UI

```python
question_label.config(text=q["question"])
```

At no point after Step 2 does:

* HTML reappear
* Formatting need fixing
* Text get mutated again

This is **clean dataflow**.

---

## 7) Why unescaping is NOT done in the UI

If unescaping were done in `quiz_ui.py`:

Problems:

* UI becomes responsible for data correctness
* Logic and UI become tightly coupled
* Risk of unescaping the same text multiple times
* Harder to test or reuse logic

Your design avoids this by:

* Treating unescaping as **data normalization**
* Keeping UI strictly presentation-only

This is a professional design decision.

---

## 8) How this affects answer evaluation correctness

Because both:

* `correct_answer`
* `current_options`

are unescaped **before comparison**, this works safely:

```python
if selected == correct_answer:
```

If unescaping were inconsistent:

* String comparison would fail
* Correct answers could be marked wrong

Your app avoids this class of bug entirely.

---

## 9) Overall data integrity guarantees

Your current pipeline guarantees:

✔ No HTML leakage into UI
✔ No double-decoding
✔ No text mutation after load
✔ Deterministic answer comparison
✔ Predictable layout behavior

This is why the app feels “stable” even though it’s simple.

---