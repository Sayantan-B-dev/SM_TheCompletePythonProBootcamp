### Mathematical Operations in Python — Complete, Clear Guide

---

## 1. **Basic Arithmetic Operators**

| Operator | Name           | Example  | Result |
| -------- | -------------- | -------- | ------ |
| `+`      | Addition       | `5 + 3`  | `8`    |
| `-`      | Subtraction    | `10 - 4` | `6`    |
| `*`      | Multiplication | `6 * 7`  | `42`   |
| `/`      | Division       | `10 / 4` | `2.5`  |

Important:

* `/` **always returns a float**, even if the division is exact.

```python
print(4 / 2)   # 2.0
```

---

## 2. **Floor Division (`//`)**

| Example    | Result | Explanation            |
| ---------- | ------ | ---------------------- |
| `10 // 3`  | `3`    | Removes decimal part   |
| `10 // 4`  | `2`    | Floors the result      |
| `-10 // 3` | `-4`   | Floors toward negative |

```python
print(10 // 3)
```

⚠️ Floor division does **not** mean rounding — it always goes **down**.

---

## 3. **Exponentiation (`**`)**

| Example    | Result |
| ---------- | ------ |
| `2 ** 3`   | `8`    |
| `5 ** 2`   | `25`   |
| `9 ** 0.5` | `3.0`  |

```python
print(2 ** 4)
print(9 ** 0.5)   # square root
```

---

## 4. **Modulus (`%`) — Remainder Operator**

| Example  | Result | Use Case   |
| -------- | ------ | ---------- |
| `10 % 3` | `1`    | Remainder  |
| `8 % 2`  | `0`    | Even check |
| `7 % 2`  | `1`    | Odd check  |

```python
if number % 2 == 0:
    print("Even")
```

---

## 5. **Operator Precedence (Order of Operations)**

Order:

1. `()` Parentheses
2. `**` Exponent
3. `* / // %`
4. `+ -`

```python
result = 10 + 2 * 3
print(result)  # 16
```

With parentheses:

```python
result = (10 + 2) * 3
print(result)  # 36
```

---

## 6. **Operations with Variables**

```python
a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a ** b)
```

---

## 7. **Assignment Operators**

| Operator | Example  | Same As     |
| -------- | -------- | ----------- |
| `+=`     | `x += 1` | `x = x + 1` |
| `-=`     | `x -= 2` | `x = x - 2` |
| `*=`     | `x *= 3` | `x = x * 3` |
| `/=`     | `x /= 2` | `x = x / 2` |

```python
x = 5
x += 2
print(x)  # 7
```

---

## 8. **Math with Different Data Types**

### Int + Float

```python
print(5 + 2.5)  # 7.5
```

Python converts `int` → `float` automatically.

---

### String + Number (Error)

```python
print("Age: " + 25)
```

❌ TypeError

✔ Fix:

```python
print("Age: " + str(25))
print(f"Age: {25}")
```

---

## 9. **Division Edge Cases**

```python
print(0 / 5)    # 0.0
print(5 / 0)    # ZeroDivisionError ❌
```

Always validate before dividing:

```python
if b != 0:
    print(a / b)
```

---

## 10. **Rounding Numbers**

```python
print(round(3.14159, 2))  # 3.14
```

---

## 11. **Common Beginner Mistakes**

| Mistake                  | Result       |
| ------------------------ | ------------ |
| Using `/` expecting int  | Gets float   |
| Forgetting precedence    | Wrong answer |
| Dividing by zero         | Crash        |
| Mixing strings & numbers | TypeError    |

---

## 12. **Real Example (Tip Calculator Logic)**

```python
bill = 4567
tip = 15
people = 788

total = bill * (1 + tip / 100)
per_person = total / people

print(round(per_person, 2))
```

---

## Key Mental Model

* `+ - * /` → basic math
* `//` → floor result
* `%` → remainder
* `**` → power
* Parentheses control everything

Mastering these operators is essential before moving into **conditions, loops, and real-world logic**.
