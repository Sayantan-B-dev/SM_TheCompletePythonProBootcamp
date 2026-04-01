## List Comprehension — **Level 3 (Advanced Composition & Reasoning)**

*Goal: nested loops, multiple conditions, conditional expressions, multi-sequence logic. This is where comprehension becomes a modeling tool.*

---

## Core Equations (Level 3 Scope)

### Nested loops

```text
new_list = [operation for a in seq1 for b in seq2]
```

### Nested + condition

```text
new_list = [operation for a in seq1 for b in seq2 if condition]
```

### Conditional expression

```text
new_list = [true_value if condition else false_value for item in sequence]
```

---

## Example 1 — Flatten a Matrix (Classic)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

flattened = [num for row in matrix for num in row]

print(flattened)
```

```text
[1, 2, 3, 4, 5, 6]
```

**Explanation**

* First loop picks each `row`
* Second loop picks each `num` inside the row
* Execution order matches nested `for` loops exactly

---

## Example 2 — Cartesian Product (Pairs)

```python
colors = ["red", "blue"]
sizes = ["S", "M", "L"]

combinations = [(color, size) for color in colors for size in sizes]

print(combinations)
```

```text
[('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ('blue', 'M'), ('blue', 'L')]
```

**Explanation**

* Every color paired with every size
* Very common in testing, product catalogs, simulations

---

## Example 3 — Filtered Cartesian Product

```python
numbers = [1, 2, 3, 4]

pairs = [(a, b) for a in numbers for b in numbers if a < b]

print(pairs)
```

```text
[(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
```

**Explanation**

* Nested loops generate all pairs
* Condition removes symmetric and duplicate pairs
* Logical constraint applied *after* generation

---

## Example 4 — Conditional Expression (Labeling)

```python
scores = [35, 80, 22, 90, 50]

status = ["PASS" if score >= 40 else "FAIL" for score in scores]

print(status)
```

```text
['FAIL', 'PASS', 'FAIL', 'PASS', 'PASS']
```

**Explanation**

* No filtering — all elements retained
* Value changes based on condition
* Think “mapping with decision”

---

## Example 5 — Nested + Conditional Expression

```python
numbers = range(1, 11)

labels = ["EVEN" if n % 2 == 0 else "ODD" for n in numbers if n > 3]

print(labels)
```

```text
['EVEN', 'ODD', 'EVEN', 'ODD', 'EVEN', 'ODD', 'EVEN']
```

**Explanation**

* First filter removes `1, 2, 3`
* Remaining values are labeled
* Two decision layers: inclusion + transformation

---

## Example 6 — Using `enumerate()` Inside Comprehension

```python
names = ["Asha", "Ravi", "Neha"]

indexed = [f"{index}: {name}" for index, name in enumerate(names)]

print(indexed)
```

```text
['0: Asha', '1: Ravi', '2: Neha']
```

**Explanation**

* `enumerate()` provides index + value
* Eliminates manual counter logic
* Very common in reporting and UI generation

---

## Example 7 — Using `zip()` with Condition

```python
students = ["Asha", "Ravi", "Neha"]
marks = [85, 35, 92]

passed_students = [name for name, mark in zip(students, marks) if mark >= 40]

print(passed_students)
```

```text
['Asha', 'Neha']
```

**Explanation**

* `zip()` synchronizes multiple sequences
* Condition applied to combined data
* Clean alternative to index-based access

---

## Example 8 — Deduplication with Logic

```python
numbers = [1, 2, 2, 3, 4, 4, 5]

unique_evens = [n for n in set(numbers) if n % 2 == 0]

print(unique_evens)
```

```text
[2, 4]
```

**Explanation**

* `set()` removes duplicates
* Comprehension applies filtering
* Order not guaranteed due to set behavior

---

## Example 9 — Extract Specific Fields from Complex Data

```python
users = [
    {"name": "Asha", "active": True},
    {"name": "Ravi", "active": False},
    {"name": "Neha", "active": True}
]

active_users = [user["name"] for user in users if user["active"]]

print(active_users)
```

```text
['Asha', 'Neha']
```

**Explanation**

* List of dictionaries as input
* Condition reads dictionary value
* Operation extracts specific field

---

## Example 10 — Multi-Level Flatten + Filter

```python
data = [
    [10, -5, 20],
    [-3, 15, 0]
]

positive_numbers = [num for row in data for num in row if num > 0]

print(positive_numbers)
```

```text
[10, 20, 15]
```

**Explanation**

* Nested structure flattened
* Condition removes invalid values
* Common in data cleaning pipelines

---

## Level 3 Reading Strategy (Critical)

Read **inside-out, right-to-left**:

1. Identify the **source sequences**
2. Expand nested loops mentally
3. Apply `if` filters
4. Apply conditional expressions
5. Collect results

---

## When **NOT** to Use Level 3 Comprehensions

```python
# Avoid this
result = [x*y if x>2 else y-x for x in range(5) for y in range(5) if y%2==0]
```

Prefer clarity:

```python
result = []

for x in range(5):
    for y in range(5):
        if y % 2 == 0:
            value = x * y if x > 2 else y - x
            result.append(value)

print(result)
```

---