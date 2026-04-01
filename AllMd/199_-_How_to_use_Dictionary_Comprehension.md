## Dictionary Comprehension — Core Idea

### Fundamental Equation (Creation)

```text
new_dict = {new_key: new_value for item in iterable}
```

### When source is a dictionary

```text
new_dict = {new_key: new_value for (key, value) in old_dict.items()}
```

### With filtering

```text
new_dict = {new_key: new_value for (key, value) in old_dict.items() if condition}
```

Read **right → left**:

1. Take items from source
2. Apply condition (optional)
3. Compute new key
4. Compute new value
5. Insert into new dictionary

---

## Why Dictionary Comprehension Exists

* Eliminates verbose loops
* Expresses **mapping logic** clearly
* Preserves semantic relationships
* Enables fast filtering and restructuring

---

## Example 1 — Square Numbers as Keys

```python
numbers = [1, 2, 3, 4]

squares = {n: n**2 for n in numbers}

print(squares)
```

```text
{1: 1, 2: 4, 3: 9, 4: 16}
```

**Explanation**

* Each list item becomes a key
* Value is derived from key
* Equivalent to building a lookup table

---

## Example 2 — Word Length Mapping

```python
words = ["data", "science", "python"]

length_map = {word: len(word) for word in words}

print(length_map)
```

```text
{'data': 4, 'science': 7, 'python': 6}
```

**Explanation**

* Useful for text analysis
* Key retains semantic meaning
* Value stores computed metric

---

## Example 3 — Convert List to Indexed Dictionary

```python
names = ["Asha", "Ravi", "Neha"]

indexed = {index: name for index, name in enumerate(names)}

print(indexed)
```

```text
{0: 'Asha', 1: 'Ravi', 2: 'Neha'}
```

**Explanation**

* `enumerate()` supplies index + value
* Dictionary replaces positional list access

---

## Example 4 — Transform Existing Dictionary Values

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92
}

scaled_scores = {name: score + 5 for name, score in scores.items()}

print(scaled_scores)
```

```text
{'Asha': 90, 'Ravi': 40, 'Neha': 97}
```

**Explanation**

* Keys preserved
* Values transformed
* Original dictionary untouched

---

## Example 5 — Student Scores: Filtering Passed Students

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92,
    "Amit": 28
}

passed = {name: score for name, score in scores.items() if score >= 40}

print(passed)
```

```text
{'Asha': 85, 'Neha': 92}
```

**Explanation**

* Condition acts as a gatekeeper
* Only qualifying key-value pairs survive

---

## Example 6 — Labeling Results (Conditional Value)

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92
}

result = {
    name: "PASS" if score >= 40 else "FAIL"
    for name, score in scores.items()
}

print(result)
```

```text
{'Asha': 'PASS', 'Ravi': 'FAIL', 'Neha': 'PASS'}
```

**Explanation**

* No filtering
* Every key retained
* Value depends on condition

---

## Example 7 — Filtering + Conditional Value Together

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92,
    "Amit": 28
}

top_students = {
    name: "DISTINCTION" if score >= 75 else "PASS"
    for name, score in scores.items()
    if score >= 40
}

print(top_students)
```

```text
{'Asha': 'DISTINCTION', 'Neha': 'DISTINCTION'}
```

**Explanation**

* First condition filters failures
* Second condition classifies remaining students

---

## Example 8 — Swap Keys and Values

```python
grades = {
    "Asha": "A",
    "Ravi": "C",
    "Neha": "A"
}

inverted = {grade: name for name, grade in grades.items()}

print(inverted)
```

```text
{'A': 'Neha', 'C': 'Ravi'}
```

**Explanation**

* Duplicate values overwrite keys
* Important real-world caveat
* Requires awareness of uniqueness

---

## Example 9 — Count Character Frequency (String Source)

```python
text = "data science"

frequency = {ch: text.count(ch) for ch in text if ch != " "}

print(frequency)
```

```text
{'d': 1, 'a': 2, 't': 1, 's': 1, 'c': 2, 'i': 1, 'e': 2, 'n': 1}
```

**Explanation**

* String is an iterable
* Each character becomes a key
* Value computed dynamically

---

## Example 10 — Normalize Marks to Percentage

```python
raw_scores = {
    "Asha": 425,
    "Ravi": 310,
    "Neha": 460
}

percentages = {
    name: round((score / 500) * 100, 2)
    for name, score in raw_scores.items()
}

print(percentages)
```

```text
{'Asha': 85.0, 'Ravi': 62.0, 'Neha': 92.0}
```

**Explanation**

* Real grading system logic
* Clean mathematical transformation
* Dictionary remains semantically rich

---

## Dictionary vs List Comprehension (Design Clarity)

| Goal                       | Use                      |
| -------------------------- | ------------------------ |
| Transform values only      | List comprehension       |
| Preserve key–value meaning | Dictionary comprehension |
| Fast lookup                | Dictionary               |
| Ordered sequence           | List                     |

---

## Common Mistakes (Critical)

### Mistake 1 — Forgetting `.items()`

```python
# WRONG
{k: v for k, v in scores}
```

Correct:

```python
{k: v for k, v in scores.items()}
```

---

### Mistake 2 — Overwriting Keys Unintentionally

```python
{score: name for name, score in scores.items()}
```

**Problem**

* Duplicate scores overwrite earlier entries
