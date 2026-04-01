FIZZBUZZ — COMPLETE, STRUCTURED, EXPLANATORY (PYTHON)

---

1. WHAT FIZZBUZZ IS (LOGIC PROBLEM)

---

FizzBuzz is a classic control-flow + loop problem used to test:

• `for` loops
• modulo operator `%`
• conditional logic order
• clean thinking

RULES (standard version):
• Print numbers from **1 to N**
• If number divisible by **3** → print `"Fizz"`
• If number divisible by **5** → print `"Buzz"`
• If divisible by **both 3 and 5** → print `"FizzBuzz"`
• Otherwise → print the number itself

---

2. WHY ORDER MATTERS (CRITICAL CONCEPT)

---

If you check `3` or `5` first, you will **never reach FizzBuzz**.

Wrong logic order:

```python
if n % 3 == 0:
elif n % 5 == 0:
elif n % 3 == 0 and n % 5 == 0:
```

Correct logic order:
→ **most specific condition first**

---

3. BASIC FIZZBUZZ (1 TO 15)

---

Code:

```python
for i in range(1, 16):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

Line-by-line explanation:
• `range(1, 16)` → generates numbers 1–15
• `%` → checks divisibility
• Combined condition handled first

Output:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

---

4. WHY `%` WORKS HERE

---

Modulo `%` returns remainder.

Examples:

```python
print(6 % 3)
print(10 % 5)
print(15 % 3)
print(15 % 5)
```

Output:

```
0
0
0
0
```

Key rule:
• Remainder `0` → perfectly divisible

---

5. GENERALIZED FIZZBUZZ (USER-DEFINED N)

---

Code:

```python
n = 20

for i in range(1, n + 1):
    if i % 15 == 0:        # 15 = 3 * 5
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

Output:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
```

Why `i % 15 == 0` works:
• Divisible by both 3 and 5
• Cleaner and faster

---

6. COUNTING FIZZ, BUZZ, FIZZBUZZ (COMMON VARIATION)

---

Code:

```python
fizz = 0
buzz = 0
fizzbuzz = 0

for i in range(1, 31):
    if i % 15 == 0:
        fizzbuzz += 1
    elif i % 3 == 0:
        fizz += 1
    elif i % 5 == 0:
        buzz += 1

print("Fizz:", fizz)
print("Buzz:", buzz)
print("FizzBuzz:", fizzbuzz)
```

Output:

```
Fizz: 8
Buzz: 4
FizzBuzz: 2
```

---

7. BUILDING RESULT INTO A LIST (DATA-ORIENTED)

---

Code:

```python
result = []

for i in range(1, 16):
    if i % 15 == 0:
        result.append("FizzBuzz")
    elif i % 3 == 0:
        result.append("Fizz")
    elif i % 5 == 0:
        result.append("Buzz")
    else:
        result.append(i)

print(result)
```

Output:

```
[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']
```

---

8. FIZZBUZZ USING STRING BUILDING (RARE BUT CLEAN)

---

Advanced pattern.

Code:

```python
for i in range(1, 16):
    output = ""

    if i % 3 == 0:
        output += "Fizz"
    if i % 5 == 0:
        output += "Buzz"

    print(output or i)
```

Explanation:
• Build string conditionally
• `output or i` prints number if string is empty

Output:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

---

9. COMMON MISTAKES

---

❌ Checking 3 or 5 before both
❌ Using `range(1, n)` instead of `n+1`
❌ Using `/` instead of `%`
❌ Forgetting condition order

---

10. WHAT FIZZBUZZ ACTUALLY TESTS

---

Not math.

It tests:
• reading requirements carefully
• condition ordering
• loop control
• edge-case handling
• thinking before coding

If you can explain **why your logic order works**, you understand FizzBuzz.
