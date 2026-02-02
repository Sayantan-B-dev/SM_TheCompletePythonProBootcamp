### Number Manipulation & f-Strings — Quiz (with Answers)

---

## **Quiz 1: Incrementing**

What is the final value of `x`?

```python
x = 5
x += 3
x -= 2
```

**Answer:** `6`

---

## **Quiz 2: Multiplicative Assignment**

What will this print?

```python
x = 4
x *= 2
x **= 2
print(x)
```

**Answer:** `64`
Explanation: `4 * 2 = 8`, then `8 ** 2 = 64`.

---

## **Quiz 3: Floor Division Assignment**

What is the output?

```python
x = 17
x //= 4
print(x)
```

**Answer:** `4`

---

## **Quiz 4: Modulus Assignment**

What does this print?

```python
x = 29
x %= 5
print(x)
```

**Answer:** `4`

---

## **Quiz 5: Unsupported Operators**

Which line causes an error?

```python
a = 5
b = 10
a++
b += 1
```

**Answer:** `a++`
Explanation: Python does not support `++` or `--`.

---

## **Quiz 6: f-String Expression**

What is printed?

```python
x = 3
y = 4
print(f"Result: {x**2 + y**2}")
```

**Answer:** `Result: 25`

---

## **Quiz 7: Formatting Decimals**

What is the output?

```python
price = 49.999
print(f"₹{price:.2f}")
```

**Answer:** `₹50.00`

---

## **Quiz 8: Combined Assignment + f-String**

What is printed?

```python
count = 1
count += 2
count *= 3
print(f"Count: {count}")
```

**Answer:** `Count: 9`

---

## **Quiz 9: Division Behavior**

What does this print?

```python
x = 10
x /= 4
print(x)
```

**Answer:** `2.5`
Explanation: `/=` always produces a float.

---

## **Quiz 10: Order of Operations in f-Strings**

What is the output?

```python
a = 10
b = 3
print(f"{a + b * 2}")
```

**Answer:** `16`
Explanation: Multiplication before addition.

---

## **Quiz 11: Percentage Calculation**

What is printed?

```python
score = 45
total = 60
print(f"{(score/total)*100:.1f}%")
```

**Answer:** `75.0%`

---

## **Quiz 12: Power Assignment**

What is the final value?

```python
x = 2
x **= 3
x += 1
```

**Answer:** `9`

---

## **Quiz 13: Floor Division with Negatives**

What is printed?

```python
x = -7
x //= 3
print(x)
```

**Answer:** `-3`
Explanation: Floor division rounds **down**.

---

## **Quiz 14: Mixing Types Safely**

Which line is correct?

```python
age = 25
# A
print("Age: " + age)
# B
print(f"Age: {age}")
```

**Answer:** **B**

---

## **Quiz 15: Best Practice**

Which is the cleanest update?

```python
x = x + 1
```

**Answer:**

```python
x += 1
```

---

### Score Guide

* **13–15 correct** → Strong fundamentals
* **9–12 correct** → Solid, revise edge cases
* **< 9** → Revisit assignment operators & f-strings