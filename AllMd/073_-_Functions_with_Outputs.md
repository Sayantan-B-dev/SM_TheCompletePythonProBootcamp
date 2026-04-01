### Functions with Output (return values)

A **function with output** is a function that sends a value back to the place where it was called using the `return` keyword.
The returned value can be stored, printed, reused, modified, or passed into another function.

---

### Basic structure

```python
def function_name(parameters):
    # processing
    return value
```

Key rule:
`return` **ends** the function execution and sends data back.

---

### Example 1: Simple return value

```python
def add(a, b):
    return a + b
```

Usage and output:

```python
result = add(3, 5)
print(result)
```

Output:

```
8
```

Explanation:

* `a + b` is calculated
* `return` sends `8`
* `result` stores `8`

---

### Example 2: Return vs print (important difference)

```python
def multiply_print(a, b):
    print(a * b)

def multiply_return(a, b):
    return a * b
```

Usage:

```python
x = multiply_print(4, 5)
y = multiply_return(4, 5)

print("x =", x)
print("y =", y)
```

Output:

```
20
x = None
y = 20
```

Explanation:

* `print()` only displays
* `return` gives a usable value
* Functions without `return` automatically return `None`

---

### Example 3: Returning multiple values

```python
def calculate(a, b):
    sum_ = a + b
    diff = a - b
    return sum_, diff
```

Usage:

```python
result = calculate(10, 4)
print(result)
```

Output:

```
(14, 6)
```

Unpacking:

```python
s, d = calculate(10, 4)
print("Sum:", s)
print("Difference:", d)
```

Output:

```
Sum: 14
Difference: 6
```

Explanation:

* Python returns multiple values as a **tuple**
* Tuple can be unpacked into variables

---

### Example 4: Return based on condition

```python
def check_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"
```

Usage:

```python
print(check_even(10))
print(check_even(7))
```

Output:

```
Even
Odd
```

Explanation:

* `return` executes only for the matched condition
* Function exits immediately after return

---

### Example 5: Early return (short-circuiting)

```python
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b
```

Usage:

```python
print(divide(10, 2))
print(divide(10, 0))
```

Output:

```
5.0
Cannot divide by zero
```

Explanation:

* Function exits early when invalid input detected
* Prevents runtime errors

---

### Example 6: Returning processed data (list)

```python
def square_numbers(numbers):
    result = []
    for n in numbers:
        result.append(n * n)
    return result
```

Usage:

```python
nums = [1, 2, 3, 4]
print(square_numbers(nums))
```

Output:

```
[1, 4, 9, 16]
```

Explanation:

* Function transforms data
* Returns new list instead of printing inside function

---

### Example 7: Function calling another function (chaining)

```python
def add(a, b):
    return a + b

def double(value):
    return value * 2
```

Usage:

```python
result = double(add(3, 4))
print(result)
```

Output:

```
14
```

Explanation:

* `add(3,4)` returns `7`
* `double(7)` returns `14`
* This is how real applications are built

---

### Example 8: Return boolean values

```python
def is_password_strong(password):
    return len(password) >= 8
```

Usage:

```python
print(is_password_strong("hello"))
print(is_password_strong("securePass123"))
```

Output:

```
False
True
```

Explanation:

* Boolean returns are used heavily in validations and conditions

---

### Table: Types of outputs

| Return Type | Example          | Usage             |
| ----------- | ---------------- | ----------------- |
| Integer     | `return 10`      | math, counters    |
| Float       | `return 3.14`    | calculations      |
| String      | `return "OK"`    | messages          |
| Boolean     | `return True`    | conditions        |
| Tuple       | `return a, b`    | multiple results  |
| List        | `return []`      | data processing   |
| Dictionary  | `return {"a":1}` | structured data   |
| None        | no return        | side effects only |

---

### Common mistakes

```python
def wrong():
    print("Hello")
```

```python
x = wrong()
print(x)
```

Output:

```
Hello
None
```

Reason:

* No `return` → Python returns `None`

---

### Mental model

* `print()` → show to user
* `return` → give back to program
* Functions with output make code **reusable, testable, and composable**

---

### Real-world mapping

* Calculator → returns number
* Login check → returns True/False
* API request → returns data
* Encryption → returns encrypted string
* ML model → returns prediction
