**Debugging – Stage 4: Fixing the Error (watching red underlines, using try/except, and defensive techniques in Python)**

Stage 4 is *surgical*. You already know **where reality diverges** (Stage 3). Now you correct it **without introducing new bugs**. This is not random editing. Every change must correspond to a known cause.

---

First, **respect red underlines (static warnings)**.
Red or yellow underlines in IDEs (PyCharm, VS Code, etc.) are static analysis hints. They often reveal:

* Type mismatches
* Unreachable code
* Undefined variables
* Shadowed names

Example underline:

```python
print(a + b)   # a: str, b: int
```

This is not “noise.” It’s the IDE telling you your mental model is wrong.

Rule:
If you ignore a red underline, you must have a written reason.

---

Second, **fix the cause, not the symptom**.
Do not silence errors by catching them blindly.

Bad fix:

```python
try:
    print(a + b)
except:
    pass
```

This hides the bug and corrupts program logic.

Correct fix (cause-based):

```python
a = int(input())
b = 5
print(a + b)
```

You corrected the state before the failure point.

---

Third, **use try/except as a control boundary, not duct tape**.
`try/except` should guard **external uncertainty**, not programmer mistakes.

Good use cases:

* User input
* File I/O
* Network calls
* Type conversions

Example:

```python
try:
    a = int(input())
except ValueError:
    print("Please enter a valid number")
    exit()
```

This acknowledges reality: users lie, inputs are messy.

---

Fourth, **catch specific exceptions only**.
Never use a bare `except:` unless you re-raise.

Bad:

```python
except:
    print("Error")
```

Good:

```python
except ValueError as e:
    print("Invalid number:", e)
```

Specific catching ensures:

* You don’t swallow unrelated bugs
* Tracebacks remain meaningful

---

Fifth, **fail early, fail loudly**.
If the program cannot continue safely, stop it immediately.

Example:

```python
try:
    age = int(input())
except ValueError:
    raise SystemExit("Age must be a number")
```

Silent recovery creates corrupted state that explodes later.

---

Sixth, **validate assumptions explicitly**.
If your logic requires a condition, enforce it.

Example:

```python
assert isinstance(a, int), "a must be int"
```

Assertions are executable documentation.
They turn hidden assumptions into runtime guarantees.

---

Seventh, **re-run the reproduction case**.
After every fix:

* Use the exact reproduction steps from Stage 2
* Verify the bug is gone
* Confirm no new error appears

Example expected behavior:

```
Input: 5
Output: 10
```

If the original bug still exists → fix failed
If a new bug appears → regression introduced

---

Eighth, **test edge cases immediately**.
Do not trust a single success.

Test:

* Empty input
* Non-numeric input
* Very large numbers
* Negative numbers

Example:

```
Input: hello → handled
Input: -5 → handled
Input: 999999999 → handled
```

A fix that only works for “happy paths” is incomplete.

---

Ninth, **clean up the fix**.
After confirming correctness:

* Remove debug prints
* Remove temporary try/except blocks
* Keep only intentional error handling

The final code should be *clearer than before*, not more cluttered.

---

A **complete Stage 4 fix summary** looks like this:

> The bug was caused by treating `input()` as an integer.
> The fix converts input to `int` and handles invalid input using a `ValueError` exception.
> The program now fails early on bad input and produces correct output for valid cases.

Stage 4 ends only when:

* The original bug is gone
* The fix matches the diagnosed cause
* Error handling is intentional and minimal
* No red underlines remain unexplained
