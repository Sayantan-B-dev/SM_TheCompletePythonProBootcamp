**Debugging – Stage 3: Play Computer and Evaluate Each Line (Python context)**

Stage 3 means you stop *thinking like a human with intentions* and start *thinking like the Python interpreter*.
No assumptions, no “what I meant.” Only **what Python actually executes, line by line, state by state**.

This stage answers: *Where does reality diverge from expectation?*

---

First, **freeze the reproduction case**.
Use the minimal, deterministic code from Stage 2. Do not change it.

Example:

```python
a = input()
b = 5
print(a + b)
```

Assume the user types:

```
5
```

---

Second, **track state explicitly**.
After every line, write down:

* Variable names
* Values
* Data types

Python bugs are very often *type-state mismatches*.

Line-by-line execution:

Line 1:

```python
a = input()
```

Python behavior:

* `input()` always returns a `str`
* User enters `"5"`

State now:

```
a = "5"      # type: str
```

No error yet. Important: Python does **not** guess intent.

---

Line 2:

```python
b = 5
```

Python behavior:

* Literal integer assignment

State now:

```
a = "5"      # str
b = 5        # int
```

Still no error.

---

Line 3:

```python
print(a + b)
```

Python evaluation order:

1. Evaluate `a` → `"5"` (str)
2. Evaluate `b` → `5` (int)
3. Apply `+` operator

Python rule:

* `str + str` → concatenation
* `int + int` → arithmetic addition
* `str + int` → **invalid**

At this exact step, Python raises:

```
TypeError: can only concatenate str (not "int") to str
```

This is the **precise failure point**.

---

Third, **identify the first incorrect assumption**.
Ask: where did your mental model diverge from Python’s rules?

Common incorrect assumption here:

* “input gives me a number”

Reality:

* `input()` → `str`, always

The bug is *not* on the `print` line conceptually, but that’s where Python detects it.

---

Fourth, **check hidden evaluations**.
Some lines look simple but do more than expected.

Examples:

* Function calls
* Indexing
* Conditionals
* Short-circuit logic

Example:

```python
if user_age > 18 and scores[2] > 50:
```

Python evaluates:

1. `user_age > 18`
2. Only if true → `scores[2] > 50`

If `scores` has fewer than 3 items, the error only happens conditionally.
Playing computer exposes this.

---

Fifth, **simulate branches explicitly**.
For conditionals and loops, evaluate *each path*.

Example:

```python
if x:
    y = 10
print(y)
```

Play computer:

* If `x` is `False`, `y` is never created
* `print(y)` → `NameError`

This bug is invisible unless you walk both paths.

---

Sixth, **watch for mutation and aliasing**.
Python passes references, not copies.

Example:

```python
a = [1, 2, 3]
b = a
b.append(4)
```

Play computer:

* `a` and `b` point to same list
* Mutation affects both

State tracking reveals this immediately.

---

Seventh, **mark the exact divergence point**.
The goal of Stage 3 is to answer:

> “At line X, Python’s actual behavior stops matching my expectation.”

Not “where the error appears,” but where the **wrong state is created**.

In our example:

* Wrong state created at: `a = input()`
* Error detected at: `print(a + b)`

That distinction matters for correct fixes later.

---

Eighth, **write the execution trace**.
A proper Stage 3 result looks like this:

> Line 1 assigns `a` as a string `"5"`.
> Line 2 assigns `b` as integer `5`.
> Line 3 attempts to apply `+` between `str` and `int`, which is invalid, causing a `TypeError`.

If you can write this without guessing, you have successfully “played computer.”

---

Stage 3 ends only when **every line has been evaluated**, every variable’s **type and value** is known, and the **exact moment of divergence** is identified.
