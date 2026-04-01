### IndexError in Python and Working with Nested Lists

(fully structured, explanatory, code-heavy, with outputs)

---

## What is an `IndexError`

An **IndexError** occurs when you try to access an index (offset) that **does not exist** in a sequence such as a list, tuple, or string.

In simple terms:
👉 *You asked for a position that is outside the list’s boundary.*

---

## Basic example of IndexError

```python
numbers = [10, 20, 30]

print(numbers[3])
```

Why this fails:

* Valid indexes: `0, 1, 2`
* Index `3` does not exist

Output:

```text
IndexError: list index out of range
```

---

## Understanding list boundaries (offset logic)

For a list of length `n`:

| Type           | Valid range  |
| -------------- | ------------ |
| Positive index | `0` to `n-1` |
| Negative index | `-1` to `-n` |

Example:

```python
nums = [1, 2, 3, 4]

print(nums[-1])
print(nums[-4])
```

Output:

```text
4
1
```

But this fails:

```python
print(nums[-5])
```

Output:

```text
IndexError: list index out of range
```

---

## Common causes of IndexError

### 1. Looping incorrectly

❌ Wrong loop:

```python
nums = [10, 20, 30]

for i in range(len(nums) + 1):
    print(nums[i])
```

Why:

* `len(nums)` is `3`
* Last index accessed is `3` → invalid

Output:

```text
10
20
30
IndexError: list index out of range
```

✅ Correct loop:

```python
for i in range(len(nums)):
    print(nums[i])
```

Output:

```text
10
20
30
```

---

### 2. Assuming user input size

```python
names = ["Alice", "Bob"]

print(names[2])
```

Output:

```text
IndexError: list index out of range
```

Professional fix:

```python
if len(names) > 2:
    print(names[2])
else:
    print("Index not available")
```

Output:

```text
Index not available
```

---

## Preventing IndexError (best practices)

### Method 1: Length check

```python
if index < len(my_list):
    value = my_list[index]
```

---

### Method 2: Try–Except (safe access)

```python
nums = [1, 2, 3]

try:
    print(nums[5])
except IndexError:
    print("Index out of bounds")
```

Output:

```text
Index out of bounds
```

---

### Method 3: Iterate directly (preferred)

```python
nums = [10, 20, 30]

for n in nums:
    print(n)
```

Output:

```text
10
20
30
```

---

## What is a Nested List

A **nested list** is a list **inside another list**.
This is how Python represents:

* Tables
* Matrices
* Grids
* Game boards

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

Here:

* `matrix` → outer list
* Each inner list → row

---

## Accessing nested list elements

Syntax:

```python
list[row_index][column_index]
```

Example:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0][1])
print(matrix[2][2])
```

Output:

```text
2
9
```

---

## Nested IndexError (very common)

```python
matrix = [
    [1, 2],
    [3, 4]
]

print(matrix[1][2])
```

Why:

* Inner list `[3, 4]` has indexes `0, 1`
* Index `2` does not exist

Output:

```text
IndexError: list index out of range
```

---

## Looping through nested lists (correct way)

### Using nested `for` loops

```python
matrix = [
    [1, 2],
    [3, 4],
    [5, 6]
]

for row in matrix:
    for value in row:
        print(value)
```

Output:

```text
1
2
3
4
5
6
```

---

### Using indexes (when positions matter)

```python
matrix = [
    [1, 2],
    [3, 4]
]

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"matrix[{i}][{j}] = {matrix[i][j]}")
```

Output:

```text
matrix[0][0] = 1
matrix[0][1] = 2
matrix[1][0] = 3
matrix[1][1] = 4
```

---

## Jagged nested lists (uneven rows)

Python allows inner lists of different lengths.

```python
data = [
    [1, 2, 3],
    [4, 5],
    [6]
]
```

Wrong assumption:

```python
print(data[1][2])
```

Output:

```text
IndexError: list index out of range
```

Safe iteration:

```python
for row in data:
    for value in row:
        print(value)
```

Output:

```text
1
2
3
4
5
6
```

---

## Real-world example: seating chart

```python
seats = [
    ["A1", "A2", "A3"],
    ["B1", "B2", "B3"]
]

row = 1
col = 2

if row < len(seats) and col < len(seats[row]):
    print(seats[row][col])
else:
    print("Seat does not exist")
```

Output:

```text
B3
```

---

## Common beginner mistakes with nested lists

| Mistake                   | Why it fails            |
| ------------------------- | ----------------------- |
| Using wrong index order   | Row vs column confusion |
| Assuming equal row length | Jagged lists exist      |
| Looping with wrong range  | Off-by-one errors       |
| Shallow copy misuse       | Shared references       |

---

## Mental model to remember

* IndexError = **boundary violation**
* Lists start at index `0`
* Last valid index = `len(list) - 1`
* Nested lists require **two indexes**
* Always validate dimensions when indexing deeply
* Iterate values, not indexes, unless index is required

---

## Interview tip

If you see `IndexError`:

1. Check `len(list)`
2. Check loop range
3. Check nested list dimensions
4. Prefer direct iteration
5. Guard with conditions or `try-except`

Next logical step:

* Shallow vs deep copy in nested lists
* 2D list creation pitfalls (`[[0]*n]*m`)
* Time complexity of list indexing
* Real grid problems (Sudoku, matrices)

