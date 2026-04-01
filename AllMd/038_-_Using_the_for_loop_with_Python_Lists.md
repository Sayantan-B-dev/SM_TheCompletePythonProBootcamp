FOR LOOPS — COMPLETE, STRUCTURED, EXPLANATORY (PYTHON)

---

1. WHAT A `for` LOOP IS

---

A `for` loop in Python is used to **iterate over a sequence** (collection) and execute a block of code **once per item** in that sequence.

Sequence can be:
• list
• tuple
• string
• dictionary
• set
• range
• any iterable object

Core idea:
→ “For each item in this collection, do something.”

General syntax:

```python
for variable in iterable:
    # code block
```

---

2. BASIC `for` LOOP WITH LIST

---

Code:

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

Explanation:
• `fruits` is the iterable
• `fruit` is the loop variable (takes one value at a time)
• Loop runs once per element

Output:

```
apple
banana
cherry
```

---

3. LOOPING OVER A STRING

---

Strings are sequences of characters.

Code:

```python
word = "python"

for char in word:
    print(char)
```

Output:

```
p
y
t
h
o
n
```

Explanation:
• Each character is accessed sequentially
• Useful for text processing, validation, parsing

---

4. `range()` FUNCTION WITH `for` LOOP

---

`range()` generates a sequence of numbers.

Forms of range:

| Form                    | Meaning        |
| ----------------------- | -------------- |
| range(n)                | 0 to n-1       |
| range(start, end)       | start to end-1 |
| range(start, end, step) | step size      |

Example 1: range(n)

Code:

```python
for i in range(5):
    print(i)
```

Output:

```
0
1
2
3
4
```

Example 2: range(start, end)

Code:

```python
for i in range(2, 6):
    print(i)
```

Output:

```
2
3
4
5
```

Example 3: range(start, end, step)

Code:

```python
for i in range(1, 10, 2):
    print(i)
```

Output:

```
1
3
5
7
9
```

---

5. LOOPING WITH `len()` AND INDEX

---

Sometimes index is required.

Code:

```python
names = ["Alice", "Bob", "Charlie"]

for i in range(len(names)):
    print(i, names[i])
```

Explanation:
• `len(names)` gives total elements
• `i` acts as index
• `names[i]` accesses element

Output:

```
0 Alice
1 Bob
2 Charlie
```

---

6. `enumerate()` — INDEX + VALUE (BEST PRACTICE)

---

Preferred over manual indexing.

Code:

```python
names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names):
    print(index, name)
```

Output:

```
0 Alice
1 Bob
2 Charlie
```

Why better:
• Cleaner
• Less error-prone
• Pythonic

---

7. LOOPING OVER DICTIONARIES

---

Dictionary components:
• keys
• values
• items (key-value pairs)

Example dictionary:

```python
student = {
    "name": "Rahul",
    "age": 21,
    "course": "CS"
}
```

Loop over keys:

```python
for key in student:
    print(key)
```

Output:

```
name
age
course
```

Loop over values:

```python
for value in student.values():
    print(value)
```

Output:

```
Rahul
21
CS
```

Loop over key-value pairs:

```python
for key, value in student.items():
    print(key, ":", value)
```

Output:

```
name : Rahul
age : 21
course : CS
```

---

8. NESTED `for` LOOPS

---

A loop inside another loop.

Code:

```python
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)
```

Explanation:
• Outer loop controls rows
• Inner loop runs fully for each outer iteration

Output:

```
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
```

---

9. `break` STATEMENT

---

Stops the loop completely.

Code:

```python
for i in range(1, 10):
    if i == 5:
        break
    print(i)
```

Output:

```
1
2
3
4
```

Explanation:
• Loop exits when condition met
• Used in search, validation

---

10. `continue` STATEMENT

---

Skips current iteration and moves to next.

Code:

```python
for i in range(1, 6):
    if i == 3:
        continue
    print(i)
```

Output:

```
1
2
4
5
```

Explanation:
• `3` is skipped
• Loop continues normally

---

11. `else` WITH `for` LOOP

---

Runs only if loop **does NOT break**.

Code:

```python
for i in range(1, 5):
    print(i)
else:
    print("Loop completed successfully")
```

Output:

```
1
2
3
4
Loop completed successfully
```

With break:

```python
for i in range(1, 5):
    if i == 3:
        break
    print(i)
else:
    print("Loop completed successfully")
```

Output:

```
1
2
```

Explanation:
• `else` skipped due to `break`

---

12. LOOPING WITH CONDITIONS (FILTERING)

---

Code:

```python
numbers = [1, 2, 3, 4, 5, 6]

for num in numbers:
    if num % 2 == 0:
        print(num, "is even")
```

Output:

```
2 is even
4 is even
6 is even
```

---

13. FOR LOOP VS WHILE LOOP (COMPARISON)

---

| Feature                 | for loop  | while loop |
| ----------------------- | --------- | ---------- |
| Iteration count known   | Yes       | Usually No |
| Cleaner for collections | Yes       | No         |
| Infinite loop risk      | Low       | High       |
| Best use                | Iterables | Conditions |

---

14. COMMON MISTAKES

---

❌ Modifying list while looping
❌ Off-by-one errors with range
❌ Forgetting indentation
❌ Using index when value is enough

Correct mindset:
• Loop over values when possible
• Use `enumerate()` for index
• Use `break` and `continue` deliberately

---

15. REALISTIC MINI EXAMPLE — BILL SPLIT

---

Code:

```python
bills = [250, 300, 150, 400]
total = 0

for bill in bills:
    total += bill  # accumulating total

print("Total bill:", total)
```

Output:

```
Total bill: 1100
```

Explanation:
• Loop aggregates values
• `+=` updates running total

---

16. MENTAL MODEL TO REMEMBER

---

“Take one item → do something → move to next item → repeat until exhausted”

This model applies to **every `for` loop**, regardless of complexity.
