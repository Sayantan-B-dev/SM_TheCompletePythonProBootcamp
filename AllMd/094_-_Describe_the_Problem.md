**Debugging – Stage 1: Describe the Problem (Python context)**

At this stage, you are not fixing anything. You are *freezing the situation* and defining the problem with precision. Most bugs survive because the problem is vaguely understood. This stage removes ambiguity.

You must answer **exactly what is going wrong**, **where**, and **under what conditions**.

In Python terms, the problem description should cover these dimensions.

---

First, **what is the expected behavior**.
State clearly what the program *should* do if it were correct. This must be concrete, observable, and testable.

Bad:
“Program should work correctly.”

Good:
“When the user enters `5` and `3`, the program should output `8`.”

Without this, you cannot say whether the program is broken.

---

Second, **what is the actual behavior**.
Describe what *actually happens* when the program runs.

Examples:

* It raises an exception (`TypeError`, `ValueError`, `IndexError`)
* It runs but gives incorrect output
* It hangs or loops forever
* It silently does nothing

You should copy the **exact error message** or **exact wrong output**, not paraphrase it.

Example:

```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

That message is part of the problem definition.

---

Third, **where the problem occurs**.
Pinpoint the location as tightly as possible.

In Python, this usually means:

* File name
* Function name
* Line number (from traceback)

Example:

```
File "calculator.py", line 14, in add_numbers()
```

If the problem is logical (no error), specify the function or block where the output diverges from expectation.

---

Fourth, **when the problem occurs**.
Define the conditions that trigger it.

Ask:

* Does it happen every time or only sometimes?
* Does it depend on user input?
* Does it depend on data size or type?
* Does it happen only after a certain step?

Example:
“The error occurs only when the input is a string, not when it’s an integer.”

This narrows the search space drastically.

---

Fifth, **inputs and environment**.
List all relevant inputs and context.

In Python, this includes:

* User inputs
* Function arguments
* Global variables involved
* Python version
* Libraries used (if relevant)

Example:
“Running on Python 3.12, input is `'5'` (string), not `5` (int).”

Many bugs are environment-specific; this prevents false assumptions.

---

Sixth, **minimal reproduction**.
Reduce the problem to the smallest possible code that still shows the bug.

Instead of a 300-line script, you might end up with this:

```python
a = input()
b = 5
print(a + b)
```

If the bug still appears here, you’ve successfully isolated the problem.
If it disappears, your description was incomplete.

This is still part of *describing* the problem, not solving it.

---

Seventh, **why it is a problem**.
Explain the impact.

Examples:

* Program crashes
* Incorrect business logic
* Security risk
* User confusion
* Data corruption

This matters because it helps prioritize and choose the correct fix later.

---

A **complete Stage 1 problem description** in Python usually looks like this:

> “In `calculator.py`, inside the `add_numbers()` function at line 14, the program raises
> `TypeError: unsupported operand type(s) for +: 'int' and 'str'`.
> Expected behavior: adding two numbers entered by the user should print their sum.
> Actual behavior: program crashes when the first input is entered as `'5'`.
> The issue occurs every time the first input comes from `input()` without conversion.
> Environment: Python 3.12. Minimal reproduction is calling `print(input() + 5)`.”

If you can write something like that, **Stage 1 is done correctly**.

Skipping or rushing this stage is the main reason debugging feels “confusing” or “random” later.
