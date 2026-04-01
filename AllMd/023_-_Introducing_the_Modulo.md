### Modulo Operator (`%`) in Python — Complete Guide

The **modulo operator (`%`)** returns the **remainder** when one number is divided by another. It is a fundamental arithmetic operator used heavily in control flow, mathematics, validation logic, and algorithm design.

---

### Basic Syntax

```python
result = a % b
```

This means:
**Divide `a` by `b`, return the remainder.**

---

### Simple Examples

```python
print(10 % 3)   # 1
print(20 % 5)   # 0
print(7 % 2)    # 1
```

Explanation:

* `10 ÷ 3 = 3 remainder 1`
* `20 ÷ 5 = 4 remainder 0`
* `7 ÷ 2 = 3 remainder 1`

---

### Checking Even or Odd Numbers

```python
num = 8

if num % 2 == 0:
    print("Even number")
else:
    print("Odd number")
```

Rule:

* `number % 2 == 0` → even
* `number % 2 != 0` → odd

---

### Modulo with `if` Conditions

```python
num = 15

if num % 3 == 0:
    print("Divisible by 3")
else:
    print("Not divisible by 3")
```

---

### Checking Divisibility by Multiple Numbers

```python
num = 30

if num % 3 == 0 and num % 5 == 0:
    print("Divisible by both 3 and 5")
```

---

### Modulo with Loops

Print all even numbers from 1 to 10:

```python
for i in range(1, 11):
    if i % 2 == 0:
        print(i)
```

---

### Counting Using Modulo

Count how many even numbers exist in a list:

```python
nums = [1, 2, 3, 4, 5, 6]
count = 0

for n in nums:
    if n % 2 == 0:
        count += 1

print(count)
```

---

### Modulo with Negative Numbers (Important Concept)

Python follows this rule:

```text
a % b = a - (b * floor(a / b))
```

Examples:

```python
print(-7 % 3)   # 2
print(7 % -3)   # -2
```

Explanation:

* `-7 ÷ 3 = -2.33 → floor → -3`
* `-7 - (-3 * 3) = 2`

**Key Rule:**
In Python, the result of `%` has the **same sign as the divisor**.

---

### Modulo with Floating Point Numbers

```python
print(7.5 % 2)     # 1.5
print(10.2 % 3.1)  # 0.9
```

Use cautiously due to floating-point precision issues.

---

### Modulo for Cyclic Behavior (Wrapping)

Common in clocks, arrays, games, and rotations.

```python
index = 7
size = 5

print(index % size)  # 2
```

This keeps values within a fixed range.

---

### Using Modulo in Time Calculations

```python
total_seconds = 3675
minutes = (total_seconds // 60) % 60
seconds = total_seconds % 60

print(minutes, seconds)
```

---

### Modulo in Password / Pattern Logic

```python
for i in range(1, 11):
    if i % 3 == 0:
        print("X")
    else:
        print(i)
```

---

### Modulo vs Division Operators

```text
/   → float division
//  → floor division
%   → remainder
```

Example:

```python
a = 17
b = 5

print(a / b)   # 3.4
print(a // b)  # 3
print(a % b)   # 2
```

---

### Common Mistakes

❌ Using `%` for percentage

```python
# WRONG
result = 50 % 100
```

✅ Percentage calculation

```python
result = (50 / 100) * 100
```

❌ Forgetting `%` returns remainder, not quotient

---

### Real-World Use Cases

* Even/odd validation
* Divisibility checks
* Circular buffers
* Pagination logic
* Scheduling tasks
* Game turn systems
* Hashing algorithms
* Pattern printing

---

### Key Takeaways

* `%` returns the remainder of division
* Result follows the sign of the divisor
* Extremely useful in conditions and loops
* Essential for mathematical and logical problem-solving
* Frequently used in competitive programming and interviews

---
