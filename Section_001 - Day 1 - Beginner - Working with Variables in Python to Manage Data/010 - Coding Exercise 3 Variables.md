### Swapping Variables in Python (Without Using Literal Values)

The goal is to **swap the contents of two variables** using only variables themselves—no hardcoded values like `"milk"` or `"juice"`. This is a classic beginner exercise that teaches how data moves between variables.

---

### Initial State

```python
glass1 = "milk"
glass2 = "juice"
```

---

### Solution (3 Lines, Using a Temporary Variable)

```python
temp = glass1
glass1 = glass2
glass2 = temp
```

---

### How This Works

* `temp` temporarily stores the value of `glass1`
* `glass1` is overwritten with the value of `glass2`
* `glass2` receives the original value of `glass1` from `temp`

This mirrors how swapping is done at a **conceptual memory level**, which is important to understand.

---

### Python Shortcut (Your Version — Also Correct)

```python
[glass1, glass2] = [glass2, glass1]
```

This uses **tuple unpacking**, a Python-specific feature that swaps values in a single statement without a temporary variable.

---

### Professional Note

* The **3-line version** teaches fundamentals and works in all languages.
* The **1-line version** is Pythonic and preferred once you understand what’s happening underneath.

Both are valid. Understanding *why* they work matters more than which one you use.
