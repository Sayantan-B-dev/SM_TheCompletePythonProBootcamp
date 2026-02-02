### Python Variables & Naming — Quick Quizzes (with Answers)

---

### Quiz 1: Valid or Invalid Variable Names

Which of the following variable names are **valid** in Python?

```text
1. user_name
2. 2score
3. totalPrice
4. _count
5. first-name
```

**Answer:**

* ✅ `user_name`
* ❌ `2score` (cannot start with a number)
* ✅ `totalPrice` (valid, but not Pythonic)
* ✅ `_count`
* ❌ `first-name` (hyphens not allowed)

---

### Quiz 2: Spot the Error

What is wrong with this code?

```python
list = [1, 2, 3]
```

**Answer:**
❌ `list` shadows a Python built-in function.
✔ Better:

```python
numbers = [1, 2, 3]
```

---

### Quiz 3: Best Variable Name

Choose the **best** variable name:

```text
A. x
B. data
C. user_age
D. a1
```

**Answer:**
✅ **C. `user_age`**
Clear, descriptive, and professional.

---

### Quiz 4: Boolean Naming

Which variable name follows best practice?

```text
A. logged
B. login_status
C. is_logged_in
D. value
```

**Answer:**
✅ **C. `is_logged_in`**
Boolean variables should read like true/false statements.

---

### Quiz 5: Reassignment Check

What will be the value of `x`?

```python
x = 10
x = "ten"
```

**Answer:**
✅ `x` will be `"ten"`
Python allows variable reassignment to a different type.

---

### Quiz 6: Multiple Assignment

What is the output?

```python
a, b = 3, 5
a, b = b, a
print(a, b)
```

**Answer:**

```
5 3
```

---

### Quiz 7: Constant Convention

Which one correctly represents a constant?

```text
A. max_users = 100
B. MAX_USERS = 100
C. MaxUsers = 100
D. maxUsers = 100
```

**Answer:**
✅ **B. `MAX_USERS`**

---

### Quiz 8: Case Sensitivity

What is printed?

```python
Age = 20
age = 30
print(Age)
```

**Answer:**

```
20
```

Python is case-sensitive.

---

### Quiz 9: Invalid Keyword Usage

Why does this fail?

```python
class = "Math"
```

**Answer:**
❌ `class` is a Python keyword and cannot be used as a variable name.

---

### Quiz 10: Naming Consistency

Which set is best?

```text
A. userName, user_age
B. user_name, user_age
C. UserName, UserAge
```

**Answer:**
✅ **B. `user_name, user_age`**

---

If you want, I can generate **MCQs only**, **fill-in-the-blanks**, or **code-output prediction quizzes** next.
