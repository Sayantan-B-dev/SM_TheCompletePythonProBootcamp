FOR LOOPS — FINDING MAX, MIN, AGGREGATION, SEARCHING, COUNTING, TRANSFORMATION (PYTHON)

---

1. FINDING MAX VALUE USING `for` LOOP (CORE PATTERN)

---

Problem:
Find the largest number in a list **without using `max()`**.

Data:

```python
numbers = [3, 9, 2, 15, 7, 11]
```

Code:

```python
numbers = [3, 9, 2, 15, 7, 11]

max_value = numbers[0]   # assume first element is maximum initially

for num in numbers:
    # compare current element with stored max
    if num > max_value:
        max_value = num  # update max if larger value found

print("Maximum value:", max_value)
```

Step-by-step logic:
• Start with a baseline (first element)
• Compare every element
• Replace when a larger value is found

Output:

```
Maximum value: 15
```

---

2. FINDING MIN VALUE USING `for` LOOP

---

Code:

```python
numbers = [3, 9, 2, 15, 7, 11]

min_value = numbers[0]   # assume first element is minimum

for num in numbers:
    if num < min_value:
        min_value = num  # update minimum

print("Minimum value:", min_value)
```

Output:

```
Minimum value: 2
```

---

3. FINDING BOTH MAX AND MIN IN ONE LOOP

---

Optimized approach (single pass).

Code:

```python
numbers = [3, 9, 2, 15, 7, 11]

max_value = numbers[0]
min_value = numbers[0]

for num in numbers:
    if num > max_value:
        max_value = num
    if num < min_value:
        min_value = num

print("Max:", max_value)
print("Min:", min_value)
```

Output:

```
Max: 15
Min: 2
```

---

4. SUM OF ELEMENTS (ACCUMULATION PATTERN)

---

Code:

```python
numbers = [10, 20, 30, 40]
total = 0

for num in numbers:
    total += num  # add each element to total

print("Sum:", total)
```

Output:

```
Sum: 100
```

Key pattern:
• Initialize accumulator
• Update inside loop

---

5. COUNTING BASED ON CONDITION

---

Problem:
Count how many even numbers exist.

Code:

```python
numbers = [1, 2, 3, 4, 5, 6, 8]
count = 0

for num in numbers:
    if num % 2 == 0:
        count += 1

print("Even count:", count)
```

Output:

```
Even count: 4
```

---

6. SEARCHING FOR A VALUE

---

Problem:
Check if a value exists.

Code:

```python
numbers = [5, 8, 12, 20, 25]
target = 12
found = False

for num in numbers:
    if num == target:
        found = True
        break  # stop once found

print("Found:", found)
```

Output:

```
Found: True
```

---

7. FINDING INDEX OF AN ELEMENT

---

Code:

```python
numbers = [5, 8, 12, 20, 25]
target = 20

for index, value in enumerate(numbers):
    if value == target:
        print("Index:", index)
        break
```

Output:

```
Index: 3
```

---

8. FINDING SECOND LARGEST ELEMENT

---

Important interview use case.

Code:

```python
numbers = [10, 5, 20, 8, 15]

largest = numbers[0]
second_largest = float('-inf')

for num in numbers:
    if num > largest:
        second_largest = largest
        largest = num
    elif num > second_largest and num != largest:
        second_largest = num

print("Largest:", largest)
print("Second largest:", second_largest)
```

Output:

```
Largest: 20
Second largest: 15
```

---

9. FILTERING VALUES INTO NEW LIST

---

Problem:
Create a list of numbers greater than 10.

Code:

```python
numbers = [3, 15, 7, 20, 9, 25]
filtered = []

for num in numbers:
    if num > 10:
        filtered.append(num)

print("Filtered list:", filtered)
```

Output:

```
Filtered list: [15, 20, 25]
```

---

10. TRANSFORMING ELEMENTS

---

Problem:
Square every number.

Code:

```python
numbers = [1, 2, 3, 4]
squares = []

for num in numbers:
    squares.append(num ** 2)  # transformation

print("Squares:", squares)
```

Output:

```
Squares: [1, 4, 9, 16]
```

---

11. FREQUENCY COUNT (VERY COMMON)

---

Problem:
Count occurrences of each element.

Code:

```python
items = ["apple", "banana", "apple", "orange", "banana"]
frequency = {}

for item in items:
    if item in frequency:
        frequency[item] += 1
    else:
        frequency[item] = 1

print("Frequency:", frequency)
```

Output:

```
Frequency: {'apple': 2, 'banana': 2, 'orange': 1}
```

---

12. NESTED LOOP USE CASE — MATRIX

---

Code:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

for row in matrix:
    for element in row:
        print(element, end=" ")
    print()
```

Output:

```
1 2 3
4 5 6
```

---

13. VALIDATION USING `for` LOOP

---

Problem:
Check if password has a digit.

Code:

```python
password = "Pass123"
has_digit = False

for char in password:
    if char.isdigit():
        has_digit = True
        break

print("Contains digit:", has_digit)
```

Output:

```
Contains digit: True
```

---

14. REAL-WORLD THINKING PATTERNS

---

Every `for` loop usually fits into one of these:

| Pattern        | Purpose       |
| -------------- | ------------- |
| Aggregation    | sum, max, min |
| Searching      | find value    |
| Counting       | frequency     |
| Filtering      | select subset |
| Transformation | modify data   |
| Validation     | check rules   |

If you can recognize the pattern, writing the loop becomes trivial.

---

15. KEY TAKEAWAY MENTAL MODEL

---

Initialize → Iterate → Compare/Update → Final Result

This is the universal structure behind **almost all real-world `for` loop use cases**.
