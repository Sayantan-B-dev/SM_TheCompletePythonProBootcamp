## 1) API used

**Service**: Open Trivia Database
**Endpoint**:

```
https://opentdb.com/api.php
```

This API returns trivia questions in JSON format based on query parameters.

Your app does **not** use tokens, sessions, or authentication — it relies on stateless requests.

---

## 2) Parameters sent to the API

In `questions.py`:

```python
params = {
    "amount": self.amount,
    "category": self.category,
    "difficulty": self.difficulty,
    "type": self.q_type,
}
```

Each parameter maps **directly** to user choices made in `main.py`.

### Parameter meaning

* `amount`

  * Number of questions requested
  * Limited by `MAX_QUESTIONS`
* `category`

  * Numeric category ID (e.g. `18` for Computers)
* `difficulty`

  * `"easy" | "medium" | "hard"`
* `type`

  * `"multiple"` or `"boolean"`

These values come from `quiz_constants.py`, ensuring **no magic strings**.

---

## 3) API request execution

```python
response = requests.get(
    OPEN_TRIVIA_URL,
    params=params,
    timeout=10
)
```

Explanation:

* Uses HTTP **GET**
* `params` automatically encoded into query string
* `timeout=10` prevents UI freeze on bad networks
* Raises an exception on connection issues

This keeps the app responsive and fail-fast.

---

## 4) API response structure

Typical OpenTDB response:

```json
{
  "response_code": 0,
  "results": [
    {
      "question": "What does CPU stand for?",
      "correct_answer": "Central Processing Unit",
      "incorrect_answers": [
        "Computer Personal Unit",
        "Central Process Utility",
        "Control Processing Unit"
      ]
    }
  ]
}
```

Your app relies on **only three fields**:

* `question`
* `correct_answer`
* `incorrect_answers`

Everything else is ignored.

---

## 5) Response validation (important)

```python
data = response.json()

if data["response_code"] != 0 or not data["results"]:
    raise ValueError("No questions found for selected options")
```

Why this matters:

* `response_code != 0` means the API rejected the request
* Empty `results` means the quiz cannot proceed
* Errors are raised **early**, before UI loads questions

This prevents silent failures.

---

## 6) HTML entity cleanup (critical detail)

OpenTDB returns HTML-encoded strings.

Example:

```
What does &quot;CPU&quot; stand for?
```

Your app fixes this using:

```python
from html import unescape

def clean_html_text(text):
    return unescape(text)
```

Used here:

```python
"question": clean_html_text(q["question"]),
"correct_answer": clean_html_text(q["correct_answer"]),
```

Without this:

* Quotes, symbols, and punctuation would render incorrectly
* UI readability would suffer

This is a **professional touch** most beginner projects miss.

---

## 7) Final internal data format

After cleaning, each question becomes:

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

Why this format is good:

* UI doesn’t care about API structure
* Logic doesn’t care about HTTP
* Deterministic, minimal, testable

---

## 8) How the UI consumes API data (decoupled)

In `quiz_ui.py`:

```python
self.question_data = Question(...)
self.qn_bank = self.question_data.question_data
```

After this line:

* The API no longer matters
* The quiz runs entirely on in-memory Python objects
* Gameplay is **offline-safe** once loaded

This is a clean separation between **data-fetching** and **gameplay**.

---

## 9) Why no threading is used (by design)

Your simplified version:

* Fetches questions once
* Blocks briefly during startup
* Avoids race conditions and UI sync issues

This choice:

* Improves reliability
* Reduces code complexity
* Makes debugging trivial

For a desktop quiz app, this is a **correct engineering tradeoff**.

---

## 10) API failure behavior

If anything goes wrong:

* Network error
* Bad parameters
* Empty response

The app:

* Raises a clear exception
* Shows an error dialog
* Exits cleanly

No corrupted state, no half-loaded quiz.

---
