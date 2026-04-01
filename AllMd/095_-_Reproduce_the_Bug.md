**Debugging – Stage 2: Reproducing the Bug (Python context)**

Stage 2 is about **proving the bug exists in a controlled, repeatable way**.
If you cannot reproduce a bug on demand, you cannot reliably fix it. Any “fix” without reproduction is guesswork.

This stage answers one core question:

Can I make the program fail **every time**, in the **same way**, using **known steps**?

---

First, **define exact reproduction steps**.
These are the precise actions needed to trigger the bug, written like instructions for a machine or another developer.

In Python, this usually includes:

* How the program is started
* What inputs are provided
* In what order actions happen

Example:

1. Run `python calculator.py`
2. Enter `5` when prompted
3. Enter `3` when prompted

If the steps are vague, the reproduction is unreliable.

---

Second, **lock the inputs**.
Randomness, user freedom, or external data must be removed or fixed.

Techniques in Python:

* Replace `input()` with hardcoded values
* Fix random seeds: `random.seed(42)`
* Use static test data instead of files/APIs

Example:

```python
a = "5"   # fixed input
b = 3
print(a + b)
```

If the bug disappears when inputs are locked, then the input variability was part of the problem.

---

Third, **run multiple times to confirm determinism**.
A real reproducible bug behaves consistently.

Run the program:

* At least 3–5 times
* With the same inputs
* In the same environment

Outcomes:

* Same error every time → deterministic bug
* Different behavior → race condition, state leak, or timing issue

Python bugs involving lists, globals, or async code often fail this test.

---

Fourth, **strip the program down**.
Remove everything that is not required to trigger the bug.

This is called **bug isolation**, but still belongs to reproduction.

Example progression:

```python
# original
def add():
    a = input()
    b = input()
    print(int(a) + int(b))
```

↓

```python
a = input()
print(a + 5)
```

↓

```python
print("5" + 5)
```

If the bug still appears, you’ve reached a minimal reproduction.

If it disappears, something you removed was essential.

---

Fifth, **confirm the same error signature**.
The reproduction is valid only if:

* Error type is the same
* Error message is the same
* Stack trace points to the same logic

Example:

```
TypeError: can only concatenate str (not "int") to str
```

If the error changes, you are no longer reproducing the same bug.

---

Sixth, **document the reproduction**.
Write it down exactly. This is not optional.

A good reproduction description includes:

* Command used to run the program
* Exact inputs
* Exact output or traceback

Example:

> Running `python app.py` with input `"5"` causes
> `TypeError: unsupported operand type(s) for +: 'str' and 'int'`
> every time.

This becomes your reference point for later stages.

---

Seventh, **verify the bug is not already fixed**.
Before moving on, ensure:

* You did not accidentally change code
* You did not restart with a different Python version
* No implicit fix occurred

Many debugging sessions fail because the bug silently disappeared and the developer keeps hunting a ghost.

---

A **successful Stage 2 outcome** is this statement:

> “I can reliably trigger this bug with known steps, fixed inputs, and minimal code, and it fails in the same way every time.”

Only after this is true should you move to **Stage 3: Isolating the cause**.

Without Stage 2, debugging becomes superstition instead of engineering.
