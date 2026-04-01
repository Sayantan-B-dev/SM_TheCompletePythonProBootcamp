### `while` Loop in Python — complete, practical, and mistake-proof

---

### What a `while` loop is

A `while` loop repeatedly executes a block of code **as long as a condition remains `True`**.

Syntax:

```python
while condition:
    # loop body
```

Key idea:
👉 **Condition first, execution later**
👉 If condition becomes `False`, loop stops immediately

---

### Basic example

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

Output:

```
1
2
3
4
5
```

Explanation (line by line):

* `count = 1` → loop control variable
* `count <= 5` → condition checked before every iteration
* `count += 1` → progress toward stopping condition
* Without increment → infinite loop

---

### How `while` works internally (mental model)

1. Check condition
2. If `True` → execute block
3. Go back to step 1
4. If `False` → exit loop

---

### Infinite loop (most common beginner mistake)

```python
x = 1

while x <= 3:
    print(x)
```

Output:

```
1
1
1
1
...
```

Why:

* `x` never changes
* Condition never becomes `False`

Fix:

```python
x = 1

while x <= 3:
    print(x)
    x += 1
```

---

### Using `break` (force exit)

```python
i = 1

while True:
    print(i)
    if i == 3:
        break
    i += 1
```

Output:

```
1
2
3
```

Explanation:

* `while True` → infinite by design
* `break` exits loop immediately
* Used when stop condition is **inside** the loop

---

### Using `continue` (skip current iteration)

```python
i = 0

while i < 5:
    i += 1
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

* When `i == 3`, `continue` skips `print`
* Loop continues to next iteration

---

### `break` vs `continue`

| Keyword    | Effect                       |
| ---------- | ---------------------------- |
| `break`    | Exits loop completely        |
| `continue` | Skips current iteration only |

---

### `while` with `else` (very misunderstood)

```python
i = 1

while i <= 3:
    print(i)
    i += 1
else:
    print("Loop finished")
```

Output:

```
1
2
3
Loop finished
```

Rule:

* `else` runs **only if loop ends normally**
* `else` does **not** run if `break` is used

Example with `break`:

```python
i = 1

while i <= 3:
    if i == 2:
        break
    print(i)
    i += 1
else:
    print("Loop finished")
```

Output:

```
1
```

---

### `while` loop with user input

```python
password = ""

while password != "admin":
    password = input("Enter password: ")

print("Access granted")
```

Sample interaction:

```
Enter password: test
Enter password: hello
Enter password: admin
Access granted
```

Explanation:

* Loop runs until correct input is given
* Common real-world usage

---

### Counter-controlled vs condition-controlled loops

#### Counter-controlled

```python
i = 1
while i <= 5:
    print(i)
    i += 1
```

#### Condition-controlled

```python
num = int(input("Enter number: "))

while num != 0:
    print(num)
    num = int(input("Enter number: "))
```

Difference:

* Counter → predictable iterations
* Condition → runs until logical condition changes

---

### `while` vs `for`

| Aspect           | while | for |
| ---------------- | ----- | --- |
| Known iterations | ❌     | ✅   |
| Unknown end      | ✅     | ❌   |
| Condition-based  | ✅     | ❌   |
| Safer by default | ❌     | ✅   |

Rule of thumb:

* Use `for` when range/collection is known
* Use `while` when stopping condition is dynamic

---

### Nested `while` loops

```python
i = 1

while i <= 3:
    j = 1
    while j <= 2:
        print(i, j)
        j += 1
    i += 1
```

Output:

```
1 1
1 2
2 1
2 2
3 1
3 2
```

Explanation:

* Inner loop completes fully for each outer iteration

---

### `while` with lists

```python
nums = [1, 2, 3, 4]
i = 0

while i < len(nums):
    print(nums[i])
    i += 1
```

Output:

```
1
2
3
4
```

---

### Removing items safely using `while`

```python
nums = [1, 2, 2, 3, 2]

while 2 in nums:
    nums.remove(2)

print(nums)
```

Output:

```
[1, 3]
```

Why `while` is better here:

* `for` fails when list size changes
* `while` adapts dynamically

---

### `pass` inside `while`

```python
i = 1

while i <= 3:
    pass
    i += 1

print("Done")
```

Output:

```
Done
```

Use case:

* Placeholder for future logic
* Prevents syntax errors

---

### Common logical bugs (no errors, wrong output)

#### Bug 1: increment inside condition

```python
i = 1

while i <= 5:
    print(i)
```

Fix:

```python
i += 1
```

---

#### Bug 2: wrong indentation

```python
i = 1
while i <= 3:
    print(i)
i += 1
```

Output:

```
1
1
1
...
```

Why:

* Increment runs **outside** loop

---

### Dry run example (important)

```python
i = 2

while i <= 8:
    print(i)
    i += 2
```

Output:

```
2
4
6
8
```

Step-by-step:

* i=2 → print → i=4
* i=4 → print → i=6
* i=6 → print → i=8
* i=8 → print → i=10 → stop

---

### When NOT to use `while`

| Situation             | Reason               |
| --------------------- | -------------------- |
| Iterating list        | `for` is safer       |
| Fixed range           | `for` is clearer     |
| Risk of infinite loop | `while` is dangerous |

---

### One-screen summary

| Concept      | Key point                    |
| ------------ | ---------------------------- |
| `while`      | Runs while condition is True |
| Needs update | Or infinite loop             |
| `break`      | Exits loop                   |
| `continue`   | Skips iteration              |
| `else`       | Runs only if no break        |
| Best for     | Unknown stopping point       |

---

### Final mental rule

If you cannot clearly answer **“what will make this condition false?”**,
you are about to write a buggy `while` loop.
