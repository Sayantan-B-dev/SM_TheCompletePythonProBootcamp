# File tree

```
quiz-app/
├─ main.py
├─ quiz_ui.py
├─ quizlogic.py
├─ questions.py
├─ quiz_constants.py
└─ (optional) tests/, docs/, assets/
```

# Executive technical summary (one dense paragraph)

This is a small, well-separated desktop quiz application: `questions.py` calls OpenTDB, cleans HTML entities and produces a normalized `qn_bank` (list of dicts). `main.py` builds a minimal setup UI and produces a normalized `config` dict. `quiz_ui.py` is a class-based Tkinter screen that holds the canonical state (`qn_index`, `score`, `selected_index`, `submitted`, `correct_answer`, `current_options`) and delegates deterministic decisions to `quizlogic.py`, which implements three pure-ish behaviors: `load_question(...)` (prepare and render one Q), `select_answer(...)` (visual selection state) and `submit_answer(...)` (evaluation, scoring, visual feedback, and transition preparation). All I/O (HTTP) is isolated, presentation is isolated, logic is isolated. Dataflow is linear: Fetch → Normalize → Present → Select → Submit → Evaluate → Advance → Finalize. This design yields predictable, testable behavior and minimal UI race conditions.

# File-by-file dense reference

### main.py — setup & entry

Role: collect user choices, validate, translate human labels → API params, start quiz. Key points: `IntVar`/`StringVar` hold UI values; `config = {"amount":int,"category":int,"difficulty":str,"type":str}` maps readable labels to values from `quiz_constants`. Failure path: invalid amount triggers messagebox error. Lifecycle: destroys setup window then instantiates `QuizUI(config)`.

### questions.py — API adapter + normalizer

Role: call `https://opentdb.com/api.php` with `params = {"amount", "category","difficulty","type"}`, check `response_code==0` and non-empty `results`. Timeout=10s; `response.raise_for_status()` surfaces HTTP errors. `clean_data()` applies `clean_html_text()` to `question`, `correct_answer`, and each `incorrect_answers` entry. Output: `self.question_data` = list of `{ "question":str, "correct_answer":str, "incorrect_answers":[str...] }`. Edge cases handled: nonzero response_code and missing results raise `ValueError` (propagates to UI). No retries, no token logic.

### quiz_constants.py — constants & HTML clean

`clean_html_text(text)` is `html.unescape(text)`; categories/difficulties/types mapping is single source of truth. Limits: `MIN_QUESTIONS`, `MAX_QUESTIONS`, `DEFAULT_QUESTIONS`.

### quiz_ui.py — class-based presentation + session state

Holds canonical session state as instance attributes. Responsibilities: create window, build layout, call `Question(...)` to fetch data synchronously, set `self.qn_bank`, and iterate questions. UI controls: 4 answer buttons, Submit/Next button (same control), Exit. Key lifecycle: `load_questions()` → `load_question()` → user interaction → `submit_answer()` (delegates to `quizlogic.submit_answer`) → if submitted and user presses button again, advance `qn_index` and call `load_question()` or `show_final_score()`.

### quizlogic.py — core behavior (stateless helpers)

`load_question(qn_index, qn_bank, question_label, answer_buttons, next_button)`:

* If `qn_index >= len(qn_bank)` → return end signal.
* Build `options = incorrect + [correct]` → `random.shuffle(options)`.
* Update `question_label` text and answer button texts; reset buttons to enabled + default colors; set next_button text to `"Submit"`.
  Return: `(correct_answer, options, False, False)`.

`select_answer(index, submitted, answer_buttons)`:

* If `submitted` return index.
* Reset buttons colors → highlight selected index visually (lightblue) → return index.

`submit_answer(selected_index, submitted, current_options, correct_answer, answer_buttons, score, score_label, next_button)`:

* Guard: if `submitted` return.
* Guard: if `selected_index is None` → messagebox warning.
* Disable all answer buttons (lock UI).
* `correct_idx = current_options.index(correct_answer)` (O(n) but n ≤ 4).
* Color: correct button green; if selected wrong, color selected red.
* Score increment only if `current_options[selected_index] == correct_answer`.
* Update score label, set `next_button` text to `"Next"`, return `(score, True)`.

# Linear dataflow (compact)

1. User clicks Start → `config` created in `main.py`.
2. `QuizUI(config)` constructed → `load_questions()` calls `Question(...)`.
3. `Question.get_questions()` → HTTP GET → JSON → `clean_data()` → `qn_bank`.
4. `QuizUI.load_question()` calls `quizlogic.load_question(...)` → UI updated with question + shuffled `options`.
5. User clicks an answer → `QuizUI.select_answer()` calls `quizlogic.select_answer(...)` → `selected_index` set.
6. User clicks Submit → `QuizUI.submit_answer()` calls `quizlogic.submit_answer(...)` → lock buttons, evaluate, update `score`, color buttons, set `submitted=True`.
7. Next press of same button triggers `QuizUI` to increment `qn_index` → back to step 4 or final scoring.

# Minimal ASCII flowchart (compact, narrow)

```
Start
  |
  v
[main.py: collect config]
  |
  v
[QuizUI(config) init]
  |
  v
[questions.Question.get_questions()] --> (HTTP GET) --> API JSON
  |
  v
[clean_data()] -> qn_bank (list of dicts)
  |
  v
loop per question:
  +--> load_question() (shuffle options, render)
  |      |
  |      v
  |   user selects -> select_answer(index)
  |      |
  |      v
  |   user submits -> submit_answer() (lock, eval, color, score++)
  |      |
  |      v
  |   next -> qn_index++ -> if end -> show_final_score -> exit
  |
  v
END
```

# State machine (compact table-like description)

State = {qn_index:int, submitted:bool, selected_index:int|None}

* Initial: qn_index=0, submitted=False, selected_index=None
* After load_question: submitted=False, selected_index=None
* On select: selected_index set, submitted still False
* On submit (if selected_index not None): submitted=True; buttons disabled; score possibly incremented
* On next: if submitted True -> qn_index +=1; submitted=False; selected_index=None; call load_question
* Terminal: qn_index >= len(qn_bank) → final screen

# Key invariants and why they matter (dense)

1. `qn_bank` immutable during session → prevents corruption and race issues. 2. `correct_answer` stored separately (not derived from button text) → reliable correctness check independent of UI. 3. `submitted` is single source of truth controlling dual-purpose button (Submit/Next) → prevents double scoring and re-evaluation. 4. Buttons are disabled on submit → no mid-evaluation state changes. 5. Answer order is shuffled every load → prevents positional bias. 6. HTML unescape occurs once during fetch → consistent display and string equality checks.

# Error handling and failure modes

* HTTP exceptions: `response.raise_for_status()` will raise; no retry mechanism exists; `QuizUI.load_questions()` catches exceptions and shows message box then closes window.
* API `response_code != 0` or empty `results`: raises `ValueError` → same user-visible behavior.
* UI-level invalid setup (amount out of bounds): message box error.
* Race conditions: none expected because `get_questions()` is synchronous; drawback: UI will block during fetch (acceptable for small quizzes but may feel frozen on slow networks).
* Edge-case: `current_options.index(correct_answer)` assumes correct answer in options — guaranteed by construction since we append it before shuffle.

# Performance notes

* Network: single GET; payload small for `amount <= MAX_QUESTIONS` (50).  Time dominated by network latency. No heavy CPU work.
* UI: O(1) per question UI updates; `index()` on options is O(4) constant.
* Memory: `qn_bank` stores all questions; acceptable for <100 items. If large quizzes desired, switch to streaming/pagination.

# Security & robustness

* No secrets; OpenTDB is public; avoid trusting content — the app escapes/cleans HTML but does not sanitize for malicious content beyond unescape; Tkinter label text is safe as it's not executing HTML or JS. If you embed images or render HTML later, sanitize inputs.
* Use `timeout` on requests to avoid hang.
* Consider rate limits and add exponential backoff if you expect many requests.

# Testing and validation (practical)

Unit test targets:

* `questions.clean_data()` with sample API payload (assert unescape and shapes).
* `quizlogic.load_question()` returns expected tuple for given qn_index and qn_bank (mock a Label and Buttons objects or use simple stubs with `config` tracking).
* `quizlogic.select_answer()` toggles button background correctly for selection and returns index.
* `quizlogic.submit_answer()` increments score correctly for correct selections, disables buttons, and sets returned `submitted=True`. Use monkeypatch for `messagebox` to intercept warnings.
  Integration test:
* Replace `questions.Question` with a fixture that returns a deterministic `qn_bank`; instantiate `QuizUI` in a headless test environment (or simulate calls to `load_question()`, `select_answer()` and `submit_answer()` without mainloop).

# Extensibility checklist (concrete next tasks)

* Add retries with backoff in `questions.get_questions()` (catch transient `requests` errors).
* Make question fetch asynchronous (thread or `asyncio`) and keep UI responsive; ensure proper cancellation and `after()` scheduling on main thread.
* Persist high scores to local JSON or sqlite; add `high_score` display in header.
* Add keyboard navigation: bind 1–4 keys to `select_answer`.
* Add optional timer per question: store `timer_id` on `QuizUI` and cancel on submit.
* Add localization: wrap strings to a `strings.py` dictionary.
* Replace `random.shuffle` with seeded RNG for reproducible quizzes in tests.

# Debug checklist (when app misbehaves)

* UI blank on start: network fetch likely raised — check exception in `load_questions()`; run `Question(...)` separately in REPL.
* Answers missing or out-of-sync: ensure `load_question()` receives fresh `qn_bank` and `qn_index` in bounds.
* Score not incrementing: verify `current_options[selected_index] == correct_answer` — print both for debugging.
* Buttons not re-enabled on new question: check `load_question()` resets `state="normal"` and colors.

# Minimal recommended refactors (dense)

1. Add a small `SessionState` dataclass: `SessionState(qn_bank, qn_index, score, selected_index, submitted)` to pass less loosely-typed attributes. 2. Make `quizlogic` pure: return a structured `LoadResult(correct_answer, options)` instead of directly mutating UI; let UI apply changes — easier to test. 3. `questions.get_questions()`: add retry/backoff and optional `dt` param for timeout. 4. Add explicit type hints to public APIs.

# Example type hints (compact)

```python
from typing import List, Dict, Tuple, Optional
def load_question(qn_index:int, qn_bank:List[Dict], ...) -> Tuple[str, List[str], bool, bool]: ...
def submit_answer(selected_index:Optional[int], submitted:bool, current_options:List[str], correct_answer:str, answer_buttons:List[tk.Button], score:int, score_label:tk.Label, next_button:tk.Button) -> Tuple[int,bool]: ...
```

# Final mechanical summary (one dense line)

Synchronous fetch produces normalized `qn_bank`; UI class owns session state and delegates deterministic, small, testable logical operations to `quizlogic`, which controls selection, evaluation, coloring and scoring; `submitted` and `qn_index` are authoritative state variables that guarantee single-evaluation per question and clean, repeatable advancement until final scoring.
