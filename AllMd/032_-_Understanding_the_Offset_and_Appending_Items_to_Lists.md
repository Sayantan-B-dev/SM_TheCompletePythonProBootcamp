### Python Lists — complete, structured, and practical

---

## What is a list in Python

A **list** is a **mutable, ordered, indexed collection** that can store **multiple values of any data type**.

Key properties:

* Ordered → items keep insertion order
* Indexed → each item has a position (offset)
* Mutable → items can be changed after creation
* Allows duplicates
* Can store mixed data types

```python
my_list = [10, 20, 30, "apple", True]
print(my_list)
```

Output:

```text
[10, 20, 30, 'apple', True]
```

---

## Understanding offsets (indexing)

### What is an offset

An **offset** is the position of an element in the list.
Python uses **zero-based indexing**.

| Index | Element     |
| ----- | ----------- |
| 0     | first item  |
| 1     | second item |
| 2     | third item  |

```python
nums = [100, 200, 300, 400]

print(nums[0])
print(nums[2])
```

Output:

```text
100
300
```

---

### Negative indexing (reverse offsets)

Negative indexes count from the end.

| Index | Meaning     |
| ----- | ----------- |
| -1    | last item   |
| -2    | second last |

```python
nums = [10, 20, 30, 40]

print(nums[-1])
print(nums[-2])
```

Output:

```text
40
30
```

---

## Appending items to a list

### `append()` — add one item at the end

```python
fruits = ["apple", "banana"]
fruits.append("mango")

print(fruits)
```

Output:

```text
['apple', 'banana', 'mango']
```

Important:

* Adds **one element only**
* Modifies the list in place
* Returns `None`

---

### `extend()` — add multiple items

```python
fruits = ["apple", "banana"]
fruits.extend(["mango", "orange"])

print(fruits)
```

Output:

```text
['apple', 'banana', 'mango', 'orange']
```

Difference:

* `append(["mango", "orange"])` → adds a nested list
* `extend(["mango", "orange"])` → adds elements individually

---

### `insert(index, value)` — add at specific offset

```python
nums = [1, 2, 4]
nums.insert(2, 3)

print(nums)
```

Output:

```text
[1, 2, 3, 4]
```

---

## Modifying list elements

```python
nums = [10, 20, 30]
nums[1] = 25

print(nums)
```

Output:

```text
[10, 25, 30]
```

Lists allow direct modification via offsets.

---

## Removing items

### `remove(value)` — remove by value

```python
nums = [1, 2, 3, 2]
nums.remove(2)

print(nums)
```

Output:

```text
[1, 3, 2]
```

Removes **first occurrence only**.

---

### `pop(index)` — remove by offset

```python
nums = [10, 20, 30]
removed = nums.pop(1)

print(nums)
print(removed)
```

Output:

```text
[10, 30]
20
```

Default: removes last item if index not provided.

---

### `clear()` — remove everything

```python
nums = [1, 2, 3]
nums.clear()

print(nums)
```

Output:

```text
[]
```

---

## Slicing lists

Slicing creates a **new list**.

Syntax:

```python
list[start : stop : step]
```

```python
nums = [0, 1, 2, 3, 4, 5]

print(nums[1:4])
print(nums[:3])
print(nums[::2])
```

Output:

```text
[1, 2, 3]
[0, 1, 2]
[0, 2, 4]
```

---

## Length and membership

```python
nums = [10, 20, 30]

print(len(nums))
print(20 in nums)
print(40 not in nums)
```

Output:

```text
3
True
True
```

---

## Sorting and reversing

### `sort()` — in-place

```python
nums = [3, 1, 4, 2]
nums.sort()

print(nums)
```

Output:

```text
[1, 2, 3, 4]
```

### `sorted()` — returns new list

```python
nums = [3, 1, 4, 2]
new_nums = sorted(nums)

print(nums)
print(new_nums)
```

Output:

```text
[3, 1, 4, 2]
[1, 2, 3, 4]
```

---

### `reverse()`

```python
nums = [1, 2, 3]
nums.reverse()

print(nums)
```

Output:

```text
[3, 2, 1]
```

---

## Copying lists (very important concept)

### Shallow copy

```python
a = [1, 2, 3]
b = a.copy()

b.append(4)
print(a)
print(b)
```

Output:

```text
[1, 2, 3]
[1, 2, 3, 4]
```

### Reference copy (dangerous for beginners)

```python
a = [1, 2, 3]
b = a

b.append(4)
print(a)
```

Output:

```text
[1, 2, 3, 4]
```

---

## Nested lists (2D lists)

```python
matrix = [
    [1, 2],
    [3, 4]
]

print(matrix[1][0])
```

Output:

```text
3
```

---

## Iterating over lists

### Using `for`

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

### Using index

```python
nums = [10, 20, 30]

for i in range(len(nums)):
    print(i, nums[i])
```

Output:

```text
0 10
1 20
2 30
```

---

## List comprehensions (powerful)

```python
squares = [x*x for x in range(5)]
print(squares)
```

Output:

```text
[0, 1, 4, 9, 16]
```

With condition:

```python
evens = [x for x in range(10) if x % 2 == 0]
print(evens)
```

Output:

```text
[0, 2, 4, 6, 8]
```

---

## Common list methods summary

| Method      | Purpose            |
| ----------- | ------------------ |
| `append()`  | add one item       |
| `extend()`  | add multiple items |
| `insert()`  | add at index       |
| `remove()`  | remove by value    |
| `pop()`     | remove by index    |
| `clear()`   | empty list         |
| `index()`   | find position      |
| `count()`   | count value        |
| `sort()`    | sort list          |
| `reverse()` | reverse order      |
| `copy()`    | shallow copy       |

---

## Mental model

* Offset = position (starts at 0)
* Append = add to the end
* Extend = flatten add
* Insert = positional add
* Pop returns value
* Lists are mutable
* Copying matters

Next logical topics:

* List vs tuple vs set
* Deep copy vs shallow copy
* Time complexity of list operations
* Interview traps with lists

