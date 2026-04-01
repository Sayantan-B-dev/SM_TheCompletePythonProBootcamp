## Python Sequences — Unified Concept

### What a *sequence* is

A **sequence** is an ordered collection where each element has a position (index). Python treats multiple data types as sequences and gives them a common behavioral contract.

> Indexing, slicing, iteration, membership testing (`in`) all come from the *sequence protocol*.

---

## Built-in Python Sequences

| Type        | Mutable | Ordered | Example             |
| ----------- | ------- | ------- | ------------------- |
| `list`      | Yes     | Yes     | `[1, 2, 3]`         |
| `tuple`     | No      | Yes     | `(1, 2, 3)`         |
| `str`       | No      | Yes     | `"abc"`             |
| `range`     | No      | Yes     | `range(1, 5)`       |
| `bytes`     | No      | Yes     | `b"abc"`            |
| `bytearray` | Yes     | Yes     | `bytearray(b"abc")` |

---

## Shared Sequence Operations (Very Important)

```python
seq = [10, 20, 30, 40]
```

| Operation      | Meaning       | Result             |
| -------------- | ------------- | ------------------ |
| `seq[0]`       | Indexing      | `10`               |
| `seq[-1]`      | Reverse index | `40`               |
| `seq[1:3]`     | Slicing       | `[20, 30]`         |
| `len(seq)`     | Length        | `4`                |
| `30 in seq`    | Membership    | `True`             |
| `for x in seq` | Iteration     | element-by-element |

These work **identically** for strings, tuples, ranges.

---

## List Methods (Behavioral Power)

### Structural Modification

```python
numbers = [1, 2, 3]

numbers.append(4)      # Adds at end
numbers.insert(1, 99)  # Inserts at index
numbers.extend([5, 6]) # Appends multiple items

print(numbers)
```

```text
[1, 99, 2, 3, 4, 5, 6]
```

---

### Removal Operations

```python
nums = [10, 20, 30, 20]

nums.remove(20)   # Removes first matching value
popped = nums.pop()  # Removes last item
del nums[0]       # Deletes by index

print(nums)
print(popped)
```

```text
[30, 20]
20
```

---

### Ordering & Analysis

```python
data = [5, 1, 4, 2]

data.sort()        # In-place sort
print(data)

print(min(data))
print(max(data))
print(sum(data))
```

```text
[1, 2, 4, 5]
1
5
12
```

---

## Why List Comprehension Exists

### Traditional Loop (Verbose)

```python
squares = []
for x in range(1, 6):
    squares.append(x * x)
```

### List Comprehension (Declarative)

```python
squares = [x * x for x in range(1, 6)]
print(squares)
```

```text
[1, 4, 9, 16, 25]
```

> Comprehension expresses **what** you want, not **how** you loop.

---

## Core List Comprehension Equation

```text
new_list = [operation for item in existing_sequence]
```

Breakdown:

* `item` → current element
* `operation` → transformation
* `existing_sequence` → any iterable

---

## List Comprehension with Numbers

```python
numbers = [1, 2, 3, 4, 5]

doubled = [n * 2 for n in numbers]
print(doubled)
```

```text
[2, 4, 6, 8, 10]
```

---

## List Comprehension with Strings (Characters)

Strings are sequences of characters.

```python
word = "python"

letters = [ch.upper() for ch in word]
print(letters)
```

```text
['P', 'Y', 'T', 'H', 'O', 'N']
```

---

## List Comprehension with `range`

```python
evens = [n for n in range(1, 11)]
print(evens)
```

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

---

## Conditional List Comprehension (Filtering)

### Core Equation

```text
new_list = [operation for item in sequence if condition]
```

---

### Example: Even Numbers

```python
numbers = range(1, 11)

evens = [n for n in numbers if n % 2 == 0]
print(evens)
```

```text
[2, 4, 6, 8, 10]
```

**Logic**
Only elements passing the condition survive.

---

### Example: Meaningful Equation (Business Case)

```python
prices = [120, 450, 90, 600, 300]

expensive = [p for p in prices if p >= 300]
print(expensive)
```

```text
[450, 600, 300]
```

---

## Conditional + Transformation Together

```python
numbers = range(1, 11)

squared_evens = [n**2 for n in numbers if n % 2 == 0]
print(squared_evens)
```

```text
[4, 16, 36, 64, 100]
```

---

## Conditional Expression Inside Comprehension

### Equation

```text
new_list = [value_if_true if condition else value_if_false for item in sequence]
```

---

### Example: Pass / Fail Labeling

```python
marks = [35, 80, 22, 90, 50]

results = ["PASS" if m >= 40 else "FAIL" for m in marks]
print(results)
```

```text
['FAIL', 'PASS', 'FAIL', 'PASS', 'PASS']
```

---

## List Comprehension Across Sequences

### Tuple → List

```python
coords = (2, 4, 6)

halved = [x / 2 for x in coords]
print(halved)
```

```text
[1.0, 2.0, 3.0]
```

---

### String → List

```python
sentence = "data science"

vowels = [ch for ch in sentence if ch in "aeiou"]
print(vowels)
```

```text
['a', 'a', 'i', 'e', 'e']
```

---

## Nested List Comprehension (Matrix Thinking)

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

**Order matters**
Left to right mirrors nested loops.

---

## Comprehension vs Loop (Design Rule)

| Situation         | Prefer        |
| ----------------- | ------------- |
| Simple transform  | Comprehension |
| Filtering         | Comprehension |
| Complex branching | Loop          |
| Debug-heavy logic | Loop          |

---

## Edge Cases and Warnings

### Readability Failure

```python
# Avoid this
data = [x*y if x>2 else y-x for x in range(5) for y in range(5) if y%2==0]
```

Better:

```python
result = []
for x in range(5):
    for y in range(5):
        if y % 2 == 0:
            value = x * y if x > 2 else y - x
            result.append(value)
```

---

## Mental Model (Key Insight)

> **Sequence** = ordered data
> **List** = mutable sequence
> **Comprehension** = mathematical mapping + filtering
> **Condition** = gatekeeper
> **Operation** = transformation

When you read a list comprehension, read it **right-to-left**:

1. Source sequence
2. Condition
3. Operation

That removes confusion completely.
