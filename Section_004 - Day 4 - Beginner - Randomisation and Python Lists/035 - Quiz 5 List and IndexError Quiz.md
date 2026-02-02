### Python Basics Quiz (Lists, Random, Indexing, Errors, Nested Lists)

**Level:** Beginner → Early Intermediate
**Format:** MCQ + Output-based + Conceptual
**Answers included after the quiz**

---

## Section 1: Multiple Choice Questions (MCQs)

### Q1. What is a Python list?

A. An immutable collection
B. An ordered, mutable collection
C. A key-value store
D. A fixed-size array

**Answer:** B

---

### Q2. What is the index (offset) of the first element in a list?

A. 1
B. -1
C. 0
D. Depends on the list

**Answer:** C

---

### Q3. Which method adds a single element to the end of a list?

A. `add()`
B. `extend()`
C. `append()`
D. `insert()`

**Answer:** C

---

### Q4. What does `random.choice()` do?

A. Returns a random number
B. Returns a random index
C. Returns one random element from a sequence
D. Shuffles the sequence

**Answer:** C

---

### Q5. Which of the following causes an `IndexError`?

A. Accessing index `-1`
B. Accessing index equal to `len(list)`
C. Iterating over a list
D. Using `append()`

**Answer:** B

---

## Section 2: Output-Based Questions

### Q6. What is the output?

```python
nums = [10, 20, 30, 40]
print(nums[-2])
```

**Answer:**

```text
30
```

---

### Q7. What is the output?

```python
import random

random.seed(1)
print(random.randint(1, 5))
```

**Answer:**

```text
2
```

---

### Q8. What is the output?

```python
items = ["a", "b"]
items.append(["c", "d"])
print(items)
```

**Answer:**

```text
['a', 'b', ['c', 'd']]
```

---

### Q9. What is the output?

```python
matrix = [[1, 2], [3, 4]]
print(matrix[1][0])
```

**Answer:**

```text
3
```

---

### Q10. What happens when this code runs?

```python
nums = [1, 2, 3]
print(nums[3])
```

**Answer:**

```text
IndexError: list index out of range
```

---

## Section 3: True or False

### Q11. Lists can contain elements of different data types.

**Answer:** True

---

### Q12. `random.shuffle()` returns a new shuffled list.

**Answer:** False
(Explanation: It modifies the list in place and returns `None`)

---

### Q13. `extend()` adds a list as a single element.

**Answer:** False
(Explanation: `append()` does that; `extend()` adds elements individually)

---

### Q14. Nested lists always have equal-length inner lists.

**Answer:** False

---

### Q15. Using `try-except` can prevent a program from crashing due to `IndexError`.

**Answer:** True

---

## Section 4: Short Answer / Explain

### Q16. Difference between `append()` and `extend()`?

**Answer:**

* `append()` adds one element (even if it’s a list)
* `extend()` adds elements of another iterable individually

---

### Q17. What is an offset in a list?

**Answer:**
An offset is the index position of an element in a list. Python uses zero-based indexing.

---

### Q18. Why is the `random` module not suitable for passwords?

**Answer:**
Because it is deterministic and predictable if the seed is known. It is not cryptographically secure.

---

### Q19. How do you safely access a nested list element?

**Answer:**
By checking both the outer and inner list lengths before indexing or using `try-except`.

---

### Q20. What is the safest way to loop over a list?

**Answer:**
Iterate directly over elements using `for item in list`.

---

## Section 5: Debugging Challenge

### Q21. Fix the error:

```python
nums = [10, 20, 30]

for i in range(len(nums) + 1):
    print(nums[i])
```

**Corrected Code:**

```python
nums = [10, 20, 30]

for i in range(len(nums)):
    print(nums[i])
```

**Output:**

```text
10
20
30
```

---

## Final Score Guide

| Score | Level                 |
| ----- | --------------------- |
| 18–21 | Strong fundamentals   |
| 14–17 | Good, needs practice  |
| 10–13 | Revise basics         |
| <10   | Relearn core concepts |

---