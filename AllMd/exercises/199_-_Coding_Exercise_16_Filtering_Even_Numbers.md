## List Comprehension — **Level 2 (Filtering + Transformation Mastery)**

*Goal: master conditions (`if`), meaningful equations, and real-world logic. Still no nesting.*

---

## Core Equation (Level 2 Scope)

```text
new_list = [operation for item in sequence if condition]
```

Read **right → left** in three passes:

1. Take `item` from `sequence`
2. Check `condition`
3. Apply `operation` **only if condition is True**

---

## Example 1 — Extract Even Numbers

```python
numbers = range(1, 11)

evens = [n for n in numbers if n % 2 == 0]

print(evens)
```

```text
[2, 4, 6, 8, 10]
```

**Explanation**

* `% 2 == 0` filters even numbers
* No transformation, only selection
* Order preserved

---

## Example 2 — Square Only Odd Numbers

```python
numbers = range(1, 11)

odd_squares = [n ** 2 for n in numbers if n % 2 != 0]

print(odd_squares)
```

```text
[1, 9, 25, 49, 81]
```

**Explanation**

* Condition decides *who enters*
* Operation transforms *what enters*

---

## Example 3 — Filter Expensive Products

```python
prices = [120, 450, 90, 600, 300]

expensive = [price for price in prices if price >= 300]

print(expensive)
```

```text
[450, 600, 300]
```

**Explanation**

* Common business logic
* Threshold-based filtering
* No mutation of original list

---

## Example 4 — Apply Tax Only to Taxable Amounts

```python
amounts = [50, 120, 80, 200]

taxed = [amount * 1.18 for amount in amounts if amount >= 100]

print(taxed)
```

```text
[141.6, 236.0]
```

**Explanation**

* Condition excludes small values
* Transformation applies tax
* Output list is shorter than input

---

## Example 5 — Keep Words Longer Than 4 Characters

```python
words = ["data", "science", "AI", "python", "ML"]

long_words = [word for word in words if len(word) > 4]

print(long_words)
```

```text
['science', 'python']
```

**Explanation**

* Condition based on `len()`
* Very common in text processing

---

## Example 6 — Extract Vowels from a String

```python
text = "list comprehension"

vowels = [ch for ch in text if ch in "aeiou"]

print(vowels)
```

```text
['i', 'o', 'e', 'e', 'i', 'o']
```

**Explanation**

* String is a sequence of characters
* Membership test filters characters

---

## Example 7 — Convert Valid Scores Only

```python
scores = [95, -5, 88, 120, 70]

valid_scores = [score for score in scores if 0 <= score <= 100]

print(valid_scores)
```

```text
[95, 88, 70]
```

**Explanation**

* Defensive programming
* Invalid data removed early
* Prevents downstream bugs

---

## Example 8 — Extract File Names with `.py` Extension

```python
files = ["app.py", "readme.md", "test.py", "notes.txt"]

python_files = [file for file in files if file.endswith(".py")]

print(python_files)
```

```text
['app.py', 'test.py']
```

**Explanation**

* Real filesystem-style logic
* `endswith()` used as filter

---

## Example 9 — Normalize Positive Numbers Only

```python
values = [-10, 20, -5, 40]

normalized = [v / 10 for v in values if v > 0]

print(normalized)
```

```text
[2.0, 4.0]
```

**Explanation**

* Condition removes invalid inputs
* Operation scales values

---

## Example 10 — Extract Capital Letters

```python
text = "PythonIsFun"

capitals = [ch for ch in text if ch.isupper()]

print(capitals)
```

```text
['P', 'I', 'F']
```

**Explanation**

* Character-level filtering
* Useful in parsing and validation

---

## Level 2 Mental Model

| Component | Role            |
| --------- | --------------- |
| Sequence  | Source of truth |
| Condition | Gatekeeper      |
| Operation | Transformer     |
| Output    | New clean list  |

---

## Common Level 2 Mistake (Important)

```python
# WRONG ORDER
[n for n in numbers if n * 2]
```

Correct:

```python
[n * 2 for n in numbers if n > 5]
```

> Condition must **not** transform — it must **decide**.

---