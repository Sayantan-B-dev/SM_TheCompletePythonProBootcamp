## `IndexError` — definition, mechanics, and **many unique real-world handling patterns**

---

## 1. What exactly is `IndexError`

**Definition**
`IndexError` is raised when code tries to access a **sequence index that does not exist**.

Applies to:

* `list`
* `tuple`
* `string`
* `range`
* any index-based container

---

## 2. Core rule (mental model)

> Valid indices are **0 ≤ index < length**

Anything outside → `IndexError`

---

## 3. Basic IndexError (list access)

```python
numbers = [10, 20, 30]
print(numbers[5])
```

**Error**

```
IndexError: list index out of range
```

---

## 4. Handling with `try–except` (simple)

```python
numbers = [10, 20, 30]

try:
    print(numbers[5])
except IndexError:
    print("Index does not exist")
```

**Output**

```
Index does not exist
```

---

## 5. User input driven IndexError (very common)

```python
items = ["apple", "banana", "cherry"]

try:
    index = int(input("Enter index: "))
    print(items[index])
except IndexError:
    print("You selected an invalid index")
except ValueError:
    print("Please enter a number")
```

**Possible output**

```
You selected an invalid index
```

---

## 6. Loop-based IndexError (off-by-one bug)

```python
data = [1, 2, 3]

try:
    for i in range(len(data) + 1):  # BUG: +1
        print(data[i])
except IndexError:
    print("Loop exceeded list bounds")
```

**Output**

```
1
2
3
Loop exceeded list bounds
```

---

## 7. IndexError in nested lists (matrix)

```python
matrix = [
    [1, 2],
    [3, 4]
]

try:
    print(matrix[1][5])
except IndexError:
    print("Invalid row or column index")
```

---

## 8. IndexError with strings (forgot string is indexed)

```python
text = "python"

try:
    print(text[10])
except IndexError:
    print("Character index out of range")
```

---

## 9. IndexError from empty list

```python
values = []

try:
    print(values[0])
except IndexError:
    print("Cannot access elements from empty list")
```

---

## 10. IndexError while popping from list

```python
stack = []

try:
    stack.pop()
except IndexError:
    print("Cannot pop from empty stack")
```

**Why it happens**

* `pop()` internally accesses last index

---

## 11. IndexError in sliding window logic

```python
nums = [1, 2, 3, 4]

try:
    for i in range(len(nums)):
        print(nums[i + 1])  # last iteration fails
except IndexError:
    print("Sliding window exceeded bounds")
```

---

## 12. IndexError in paired list processing

```python
names = ["A", "B", "C"]
scores = [90, 80]

try:
    for i in range(len(names)):
        print(names[i], scores[i])
except IndexError:
    print("Mismatched list lengths")
```

---

## 13. IndexError in manual queue implementation

```python
queue = []

try:
    item = queue[0]
except IndexError:
    print("Queue is empty")
```

---

## 14. IndexError in game logic (grid-based)

```python
board = [
    ["X", "O", "X"],
    ["O", "X", "O"]
]

try:
    print(board[2][1])  # row does not exist
except IndexError:
    print("Move outside the board")
```

---

## 15. IndexError with negative overflow (less known)

```python
data = [1, 2, 3]

try:
    print(data[-5])
except IndexError:
    print("Negative index out of range")
```

---

## 16. IndexError during deletion in loop (classic bug)

```python
items = [1, 2, 3, 4]

try:
    for i in range(len(items)):
        del items[i]
except IndexError:
    print("List size changed during iteration")
```

---

## 17. IndexError from slicing misunderstanding (important)

```python
data = [1, 2, 3]

try:
    print(data[3])      # IndexError
    print(data[1:10])   # safe
except IndexError:
    print("Direct index failed, slicing would not")
```

---

## 18. IndexError in recursive logic

```python
def get_item(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None

print(get_item([1, 2], 5))
```

**Output**

```
None
```

---

## 19. IndexError transformed into domain error (professional)

```python
class InvalidPositionError(Exception):
    pass

positions = ["A", "B", "C"]

try:
    print(positions[10])
except IndexError as e:
    raise InvalidPositionError("Position not available") from e
```

---

## 20. IndexError in API-style access layer

```python
def get_user(users, index):
    try:
        return users[index]
    except IndexError:
        raise ValueError("User index out of range")
```

---

## 21. Handling IndexError with fallback value

```python
data = [10, 20, 30]

try:
    value = data[5]
except IndexError:
    value = 0

print(value)
```

**Output**

```
0
```

---

## 22. IndexError vs prevention (important distinction)

### Handling (reactive)

```python
try:
    item = data[i]
except IndexError:
    item = None
```

### Prevention (proactive, preferred)

```python
if 0 <= i < len(data):
    item = data[i]
else:
    item = None
```

---

## 23. When `try–except IndexError` is justified

| Scenario                  | Use try–except? |
| ------------------------- | --------------- |
| User input index          | Yes             |
| External data             | Yes             |
| Parsing unknown structure | Yes             |
| Internal fixed logic      | No (bug)        |

---

## 24. Interview-level insight

> `IndexError` usually signals **boundary failure**, not logic failure.

Good engineers:

* Handle it at **edges**
* Prevent it in **core logic**
* Transform it into **domain meaning** when exposed externally

---

## 25. Final takeaway

* `IndexError` is predictable
* Handling must be intentional
* Prevention is better than reaction
* Transforming it cleanly is senior-level behavior
