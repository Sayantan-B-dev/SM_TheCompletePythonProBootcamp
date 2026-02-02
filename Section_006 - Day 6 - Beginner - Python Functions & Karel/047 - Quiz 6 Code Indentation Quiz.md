### Python Quiz (Based on knowledge so far)

Topics covered: variables, functions, loops, conditions, indentation, arguments, return, scope

---

## Section 1: MCQs (Single correct answer)

### Q1

What will be the output?

```python
x = 5

if x > 3:
    print("A")
print("B")
```

A. A
B. B
C. A B
D. Error

**Answer:** C

Output:

```
A
B
```

Explanation:
Only `print("A")` is inside the `if`. `print("B")` always runs.

---

### Q2

Which of the following causes an `IndentationError`?

A.

```python
if True:
    print("Hi")
```

B.

```python
if True:
print("Hi")
```

C.

```python
print("Hi")
```

D.

```python
if True:
    pass
```

**Answer:** B

Explanation:
Code after `:` must be indented.

---

### Q3

What does this function return?

```python
def test():
    print("Hello")

x = test()
print(x)
```

A. Hello
B. None
C. Error
D. 0

**Answer:** B

Output:

```
Hello
None
```

Explanation:
Functions return `None` by default if no `return` is used.

---

### Q4

What is `*args` used for?

A. Passing dictionaries
B. Passing unlimited positional arguments
C. Passing keyword arguments
D. Returning multiple values

**Answer:** B

---

### Q5

Which indentation is correct?

A.

```python
for i in range(3):
print(i)
```

B.

```python
for i in range(3):
    print(i)
```

C.

```python
for i in range(3)
    print(i)
```

D.

```python
for i in range(3):
        print(i)
```

**Answer:** B

Explanation:
4-space indentation after `:` is standard and correct.

---

## Section 2: Predict the Output

### Q6

```python
def add(a, b):
    return a + b

print(add(2, 3) * 2)
```

**Answer:**

```
10
```

Explanation:
`add(2,3)` → `5`, then `5 * 2`.

---

### Q7

```python
for i in range(3):
    if i == 1:
        continue
    print(i)
```

**Answer:**

```
0
2
```

Explanation:
`continue` skips the rest of the loop when `i == 1`.

---

### Q8

```python
x = 10

def change():
    x = 5

change()
print(x)
```

**Answer:**

```
10
```

Explanation:
Local `x` does not affect global `x`.

---

### Q9

```python
def calc(a, b):
    return a+b, a*b

x = calc(2, 3)
print(x)
```

**Answer:**

```
(5, 6)
```

Explanation:
Multiple values are returned as a tuple.

---

## Section 3: True / False

| Question                                | True / False | Answer |
| --------------------------------------- | ------------ | ------ |
| Python ignores indentation              | ❌            | False  |
| `return` exits a function               | ✅            | True   |
| `print()` can send value back to caller | ❌            | False  |
| `else` can belong to loops              | ✅            | True   |
| Tabs and spaces are interchangeable     | ❌            | False  |

---

## Section 4: Fix the Code

### Q10

Fix the indentation error:

```python
def greet():
print("Hello")
```

**Correct code:**

```python
def greet():
    print("Hello")

greet()
```

Output:

```
Hello
```

---

### Q11

Fix logical error (sum should print once):

```python
total = 0
for i in range(5):
    total += i
    print(total)
```

**Correct code:**

```python
total = 0
for i in range(5):
    total += i

print(total)
```

Output:

```
10
```

---

## Section 5: Short Answer

### Q12

Difference between `print` and `return`?

**Answer:**

| print        | return           |
| ------------ | ---------------- |
| Shows output | Sends value back |
| Not reusable | Reusable         |
| For display  | For logic        |

---

### Q13

Why is `pass` used?

**Answer:**
To create an empty block where syntax requires indentation but no action is needed.

---

### Q14

What happens if indentation is wrong but syntax is valid?

**Answer:**
Program runs but produces **wrong logic**, which is more dangerous than errors.

---

## Section 6: Mini Coding Question

### Q15

Write a function that prints numbers from 1 to 3 using a loop.

**Answer:**

```python
def show():
    for i in range(1, 4):
        print(i)

show()
```

Output:

```
1
2
3
```

---

### Skill check summary

| Skill          | Covered |
| -------------- | ------- |
| Indentation    | ✅       |
| Functions      | ✅       |
| Loops          | ✅       |
| Scope          | ✅       |
| Arguments      | ✅       |
| Return values  | ✅       |
| Logical errors | ✅       |

This quiz tests **logic understanding**, not memorization.
