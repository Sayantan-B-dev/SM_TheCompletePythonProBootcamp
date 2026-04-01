FOR LOOP + `range()` — RARE, EDGE, AND LESS-TAUGHT BEHAVIORS (PYTHON)

---

1. `range()` IS NOT A LIST (IMPORTANT BUT OFTEN MISSED)

---

`range()` returns a **range object**, not an actual list.

Code:

```python
r = range(5)
print(r)
```

Output:

```
range(0, 5)
```

Explanation:
• No numbers are stored in memory
• Values are generated on demand
• Extremely memory-efficient

Proof:

```python
print(list(range(5)))
```

Output:

```
[0, 1, 2, 3, 4]
```

---

2. NEGATIVE STEP IN `range()` (REVERSE LOOPING)

---

Rare but powerful.

Syntax:

```python
range(start, stop, -step)
```

Code:

```python
for i in range(10, 0, -2):
    print(i)
```

Output:

```
10
8
6
4
2
```

Rules:
• Start > Stop
• Step must be negative
• Stop is still **exclusive**

---

3. `range()` WITH SAME START AND STOP (ZERO ITERATIONS)

---

Code:

```python
for i in range(5, 5):
    print(i)
```

Output:

```
(no output)
```

Explanation:
• Loop never executes
• Useful for conditional iteration logic

---

4. `range()` WITH WRONG STEP DIRECTION (SILENT FAILURE)

---

Code:

```python
for i in range(1, 10, -1):
    print(i)
```

Output:

```
(no output)
```

Explanation:
• Step direction contradicts start/stop
• Python does not throw error
• Loop silently skips

---

5. LARGE `range()` DOES NOT CONSUME MEMORY

---

This is **extremely important** for performance.

Code:

```python
r = range(1_000_000_000)
print(r)
```

Output:

```
range(0, 1000000000)
```

Why this matters:
• No billion integers stored
• Only start, stop, step tracked
• Safe for loops and conditions

---

6. LOOP VARIABLE EXISTS AFTER LOOP (SCOPE QUIRK)

---

Unlike some languages, Python keeps loop variable alive.

Code:

```python
for i in range(3):
    pass

print(i)
```

Output:

```
2
```

Explanation:
• `i` retains last value
• Can cause subtle bugs
• Avoid reusing loop variables

---

7. MODIFYING LOOP VARIABLE DOES NOTHING

---

Very common misunderstanding.

Code:

```python
for i in range(5):
    i += 10
    print(i)
```

Output:

```
10
11
12
13
14
```

Explanation:
• `i` is reassigned locally
• Next iteration overwrites it
• Loop control is unaffected

---

8. USING `_` AS THROWAWAY VARIABLE

---

When value is irrelevant.

Code:

```python
for _ in range(3):
    print("Hello")
```

Output:

```
Hello
Hello
Hello
```

Explanation:
• `_` signals intentional ignore
• Improves readability
• Pythonic convention

---

9. `range()` WITH FLOATS (NOT ALLOWED)

---

Code:

```python
for i in range(0, 5, 0.5):
    print(i)
```

Output:

```
TypeError: 'float' object cannot be interpreted as an integer
```

Correct alternative:

```python
for i in range(0, 10):
    print(i / 2)
```

Output:

```
0.0
0.5
1.0
1.5
2.0
...
```

---

10. USING `range()` FOR FIXED REPEAT COUNT

---

Classic but often under-explained.

Code:

```python
for _ in range(5):
    print("Retrying...")
```

Output:

```
Retrying...
Retrying...
Retrying...
Retrying...
Retrying...
```

Use case:
• retries
• polling
• animations
• simulations

---

11. LOOPING BACKWARDS OVER LIST USING `range()`

---

Code:

```python
data = [10, 20, 30, 40]

for i in range(len(data) - 1, -1, -1):
    print(data[i])
```

Output:

```
40
30
20
10
```

Explanation:
• Start at last index
• Stop at -1 (exclusive)
• Step backwards

---

12. SKIPPING ELEMENTS USING STEP

---

Code:

```python
for i in range(0, 10, 3):
    print(i)
```

Output:

```
0
3
6
9
```

Use case:
• sampling
• pagination
• chunk processing

---

13. `range()` OBJECT SUPPORTS MEMBERSHIP TEST

---

Rare but useful.

Code:

```python
print(5 in range(1, 10))
print(15 in range(1, 10))
```

Output:

```
True
False
```

Explanation:
• O(1) check
• No iteration required

---

14. USING `range()` WITH `len()` IS OFTEN A CODE SMELL

---

Less ideal:

```python
items = ["a", "b", "c"]

for i in range(len(items)):
    print(items[i])
```

Better:

```python
for item in items:
    print(item)
```

When `range(len())` is justified:
• index manipulation
• reverse iteration
• parallel indexing

---

15. `for` LOOP CAN ITERATE OVER ANY ITERABLE (NOT JUST RANGE)

---

Example with custom iterable behavior.

Code:

```python
text = "ABC"

for i in range(len(text)):
    print(i, text[i])
```

Output:

```
0 A
1 B
2 C
```

But also:

```python
for char in text:
    print(char)
```

Output:

```
A
B
C
```

Key idea:
• `for` works with iteration protocol
• `range()` is just one iterable

---

16. FOR-ELSE WITH `range()` (VERY RARE, VERY POWERFUL)

---

Code:

```python
for i in range(2, 10):
    if i == 7:
        print("Found 7")
        break
else:
    print("Not found")
```

Output:

```
Found 7
```

If not found:

```python
for i in range(2, 6):
    if i == 7:
        break
else:
    print("Not found")
```

Output:

```
Not found
```

Explanation:
• `else` runs only if loop ends normally
• Skipped when `break` occurs

---

17. MENTAL MODEL FOR RARE BUGS

---

If a `for` + `range()` loop behaves “weird”, check:

• start < stop < step direction
• step ≠ 0
• integer arguments only
• loop variable reuse
• silent zero-iteration cases

These edge behaviors are intentional, not bugs.
