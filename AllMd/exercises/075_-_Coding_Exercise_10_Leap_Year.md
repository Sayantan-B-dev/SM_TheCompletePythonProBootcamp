### 1. Leap year checker (returns Boolean)

```python
def is_leap_year(year):
    # Leap year rules:
    # divisible by 400 → leap
    # divisible by 100 → not leap
    # divisible by 4 → leap
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False
```

Usage and output:

```python
print(is_leap_year(2024))
print(is_leap_year(1900))
print(is_leap_year(2000))
```

Output:

```
True
False
True
```

---

### 2. Even or odd checker

```python
def is_even(number):
    return number % 2 == 0
```

Usage and output:

```python
print(is_even(10))
print(is_even(7))
```

Output:

```
True
False
```

---

### 3. Prime number checker

```python
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

Usage and output:

```python
print(is_prime(7))
print(is_prime(12))
```

Output:

```
True
False
```

---

### 4. Factorial calculator

```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

Usage and output:

```python
print(factorial(5))
```

Output:

```
120
```

---

### 5. Fibonacci number generator (nth term)

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

Usage and output:

```python
print(fibonacci(0))
print(fibonacci(6))
```

Output:

```
0
8
```

---

### 6. Maximum of three numbers

```python
def max_of_three(a, b, c):
    return max(a, b, c)
```

Usage and output:

```python
print(max_of_three(10, 25, 15))
```

Output:

```
25
```

---

### 7. Temperature converter (Celsius → Fahrenheit)

```python
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32
```

Usage and output:

```python
print(celsius_to_fahrenheit(0))
print(celsius_to_fahrenheit(37))
```

Output:

```
32.0
98.6
```

---

### 8. Simple interest calculator

```python
def simple_interest(principal, rate, time):
    return (principal * rate * time) / 100
```

Usage and output:

```python
print(simple_interest(1000, 5, 2))
```

Output:

```
100.0
```

---

### 9. Count vowels in a string

```python
def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count
```

Usage and output:

```python
print(count_vowels("Python Programming"))
```

Output:

```
4
```

---

### 10. Reverse a string

```python
def reverse_string(text):
    return text[::-1]
```

Usage and output:

```python
print(reverse_string("hello"))
```

Output:

```
olleh
```

---

### 11. Palindrome checker

```python
def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]
```

Usage and output:

```python
print(is_palindrome("madam"))
print(is_palindrome("hello"))
```

Output:

```
True
False
```

---

### 12. Sum of digits of a number

```python
def sum_of_digits(n):
    total = 0
    for digit in str(abs(n)):
        total += int(digit)
    return total
```

Usage and output:

```python
print(sum_of_digits(1234))
```

Output:

```
10
```

---

### 13. Grade calculator

```python
def calculate_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"
```

Usage and output:

```python
print(calculate_grade(88))
print(calculate_grade(45))
```

Output:

```
B
F
```

---

### 14. List average calculator

```python
def average(numbers):
    return sum(numbers) / len(numbers)
```

Usage and output:

```python
print(average([10, 20, 30, 40]))
```

Output:

```
25.0
```

---

### 15. Password strength checker (basic)

```python
def is_strong_password(password):
    return len(password) >= 8
```

Usage and output:

```python
print(is_strong_password("hello"))
print(is_strong_password("Secure123"))
```

Output:

```
False
True
```

---

### Summary table

| Function       | Input   | Output        |
| -------------- | ------- | ------------- |
| Leap year      | year    | True / False  |
| Prime check    | number  | True / False  |
| Factorial      | integer | integer       |
| Fibonacci      | index   | integer       |
| Converter      | number  | float         |
| String tools   | string  | string / bool |
| Math utilities | numbers | numeric       |
| Validation     | data    | boolean       |

These examples cover mathematical logic, conditionals, loops, strings, lists, early returns, and reusable outputs—the exact patterns used in real programs.
