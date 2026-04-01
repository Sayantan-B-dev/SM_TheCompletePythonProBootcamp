**Debugging – Stage 5: Squash the Bug with `print()` (Python context)**

This stage uses the simplest, most primitive, and most reliable debugging tool: **printing program state**.
You are not fixing logic here. You are *exposing reality*. `print()` is your microscope.

This stage is especially powerful when:

* You don’t yet trust your mental model
* The bug is logical (no exception)
* Control flow is complex
* Data mutates over time

---

First, **print facts, not guesses**.
Never print messages like:

```python
print("something is wrong")
```

Instead, print:

* Variable values
* Variable types
* Execution checkpoints

Example:

```python
print("a =", a, "type =", type(a))
```

This answers *what is*, not *what you think is*.

---

Second, **print before and after critical lines**.
Any line that:

* Changes state
* Makes a decision
* Mutates data
* Returns a value
  is suspicious until proven correct.

Example:

```python
print("Before conversion:", a, type(a))
a = int(a)
print("After conversion:", a, type(a))
```

If the second print never runs, the failure is between them.

---

Third, **trace execution flow explicitly**.
When code involves conditionals or loops, confirm which paths actually execute.

Example:

```python
print("Reached start of loop")

for i in range(3):
    print("Loop iteration:", i)
```

If you don’t see a print, that path never ran.
Assumptions about flow die instantly here.

---

Fourth, **label prints clearly**.
Unlabeled prints become noise.

Bad:

```python
print(a)
print(b)
```

Good:

```python
print("User input a:", a)
print("Counter b:", b)
```

You should be able to read logs like a story.

---

Fifth, **print inside conditionals**.
This reveals *why* decisions are made.

Example:

```python
if score > 50:
    print("Passed condition: score =", score)
else:
    print("Failed condition: score =", score)
```

This exposes boundary mistakes (`>=` vs `>`), which are extremely common.

---

Sixth, **print loop state and termination conditions**.
Infinite loops or early exits often hide here.

Example:

```python
while lives > 0:
    print("Lives at start of loop:", lives)
    lives -= 1
```

If `lives` never changes, the bug becomes obvious immediately.

---

Seventh, **print data structures fully and incrementally**.
Lists and dictionaries often mutate unexpectedly.

Example:

```python
print("Before append:", my_list)
my_list.append(x)
print("After append:", my_list)
```

For dictionaries:

```python
print("Keys:", my_dict.keys())
print("Values:", my_dict.values())
```

This exposes aliasing and overwrite bugs.

---

Eighth, **print function entry and exit points**.
Functions are black boxes unless you instrument them.

Example:

```python
def add(a, b):
    print("Entering add:", a, b)
    result = a + b
    print("Exiting add:", result)
    return result
```

If “Exiting” never prints, the function failed internally.

---

Ninth, **print error context just before failure**.
If an error happens at line X, print everything *just before X*.

Example:

```python
print("About to add:", a, type(a), b, type(b))
print(a + b)
```

This removes all ambiguity about the cause.

---

Tenth, **reduce prints once the bug is squashed**.
After the bug is understood and fixed:

* Remove exploratory prints
* Keep only intentional logging (if needed)

Leaving random prints is technical debt.

---

A **successful Stage 5 outcome** looks like this:

> Using `print()`, the actual runtime values and types were observed.
> The incorrect state was confirmed before the failing line.
> The fix was validated by observing corrected state through prints.

If `print()` makes the bug obvious, the bug was never mysterious — only hidden.

This stage works because **code cannot lie, but developers often guess**.
