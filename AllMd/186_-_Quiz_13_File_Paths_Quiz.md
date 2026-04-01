## ADVANCED & TRICKY QUIZ — FILE SYSTEM, PATHS, FILE MODES, `with`, HIGH SCORE LOGIC

---

## SECTION 1 — WORKING DIRECTORY & PATH RESOLUTION (TRICKY)

### Q1

You run this code from an IDE:

```python
with open("data.txt") as f:
    print(f.read())
```

Directory structure:

```
project/
 ├── main.py
 └── data.txt
```

IDE working directory:

```
C:/Users/Alex/
```

**What happens?**

A. File opens correctly
B. FileNotFoundError
C. PermissionError
D. Opens wrong file

> **Answer:** B
> **Reason:** Relative paths resolve from *working directory*, not script location.

---

### Q2

```python
import os
print(os.getcwd())
```

Output:

```
/home/user
```

You execute:

```python
open("../data.txt")
```

Where does Python look?

A. `/home/data.txt`
B. `/home/user/data.txt`
C. `/data.txt`
D. `/home/user/../data.txt`

> **Answer:** A
> **Reason:** `..` moves one level up → `/home`

---

### Q3

Which path is **guaranteed** to work regardless of where the script is launched?

A. `"data.txt"`
B. `"./data.txt"`
C. `os.path.join(os.getcwd(), "data.txt")`
D. `os.path.join(os.path.dirname(__file__), "data.txt")`

> **Answer:** D
> **Reason:** Tied to script location, not cwd.

---

## SECTION 2 — FILE MODES (COMMON CONFUSION)

### Q4

What happens if you open a file like this?

```python
open("log.txt", "w")
```

A. Appends new content
B. Raises error if file exists
C. Deletes old content
D. Opens in read-only mode

> **Answer:** C
> **Reason:** `"w"` truncates file immediately.

---

### Q5

Which mode allows **reading and writing** without deleting existing content?

A. `"w+"`
B. `"r+"`
C. `"a+"`
D. `"x"`

> **Answer:** B
> **Reason:** `"r+"` keeps content intact, cursor at start.

---

### Q6

You want to **create a file only if it does NOT exist**. Which mode?

A. `"w"`
B. `"a"`
C. `"x"`
D. `"r+"`

> **Answer:** C
> **Reason:** `"x"` fails if file already exists.

---

## SECTION 3 — `with` KEYWORD & RESOURCE MANAGEMENT

### Q7

What is the biggest advantage of `with open(...)`?

A. Faster execution
B. Automatic garbage collection
C. Automatic file closing even on error
D. Prevents syntax errors

> **Answer:** C
> **Reason:** Context manager guarantees cleanup.

---

### Q8

What happens here?

```python
with open("data.txt", "r") as f:
    raise ValueError
```

A. File remains open
B. Program crashes and file corrupts
C. File closes before exception propagates
D. Python suppresses the error

> **Answer:** C
> **Reason:** `__exit__()` executes before exception escapes.

---

## SECTION 4 — FILE POINTER (VERY TRICKY)

### Q9

File content:

```
ABCDEFG
```

Code:

```python
with open("data.txt") as f:
    print(f.read(3))
    print(f.read(2))
```

Output?

A.

```
ABC
AB
```

B.

```
ABC
DE
```

C.

```
ABC
CD
```

D.

```
ABC
FG
```

> **Answer:** B
> **Reason:** File cursor advances automatically.

---

### Q10

What does this do?

```python
f.seek(0)
```

A. Deletes file
B. Moves cursor to start
C. Closes file
D. Flushes buffer

> **Answer:** B

---

## SECTION 5 — HIGH SCORE FILE LOGIC (GAME-LEVEL TRAPS)

### Q11

Why is high score written **only during reset**, not every frame?

A. Writing files is illegal during loops
B. Disk I/O is slow and unnecessary
C. Turtle cannot write files while moving
D. Python restricts frequent writes

> **Answer:** B

---

### Q12

What happens if `data.txt` contains:

```
12\n
```

And code is:

```python
int(data.read())
```

A. ValueError
B. Returns `12`
C. Returns `"12"`
D. Returns `None`

> **Answer:** B
> **Reason:** `int()` ignores whitespace.

---

### Q13

Why is this dangerous?

```python
self.high_score = data.read()
if self.score > self.high_score:
```

A. SyntaxError
B. Logical bug
C. Memory leak
D. Runtime crash

> **Answer:** B
> **Reason:** Comparing `int` with `str`.

---

## SECTION 6 — ABSOLUTE vs RELATIVE (EDGE CASES)

### Q14

Which statement is TRUE?

A. Relative paths are faster
B. Absolute paths depend on cwd
C. Relative paths can cross drives
D. Absolute paths ignore cwd

> **Answer:** D

---

### Q15

Why does this fail on Linux?

```python
open("C:/Users/Alex/data.txt")
```

A. Syntax error
B. Permission issue
C. Path is OS-specific
D. File mode missing

> **Answer:** C

---

## SECTION 7 — BINARY vs TEXT (SUBTLE)

### Q16

What does this return?

```python
with open("image.png", "rb") as f:
    data = f.read()
print(type(data))
```

A. `str`
B. `bytes`
C. `bytearray`
D. `memoryview`

> **Answer:** B

---

### Q17

Why must images be opened in binary mode?

A. They are encrypted
B. Encoding corrupts binary data
C. Turtle requires it
D. Files are too large

> **Answer:** B

---

## SECTION 8 — PATH MANIPULATION (PRO LEVEL)

### Q18

Which is the safest cross-platform way?

A. `"assets\\img.png"`
B. `"assets/img.png"`
C. `os.path.join("assets", "img.png")`
D. `"./assets/img.png"`

> **Answer:** C

---

### Q19

What does `__file__` represent?

A. Current working directory
B. Python executable
C. Script file location
D. Imported module list

> **Answer:** C

---

## SECTION 9 — ERROR DIAGNOSIS (REAL SCENARIOS)

### Q20

Error:

```
FileNotFoundError
```

File exists. Most likely cause?

A. Wrong file mode
B. Encoding issue
C. Wrong working directory
D. Corrupted file

> **Answer:** C

---

## SECTION 10 — FINAL BOSS QUESTION

### Q21

Which design is **most robust** for production?

A.

```python
open("data.txt")
```

B.

```python
open(os.getcwd() + "/data.txt")
```

C.

```python
open(os.path.join(os.path.dirname(__file__), "data.txt"))
```

D.

```python
open("../data.txt")
```

> **Answer:** C
> **Reason:** Independent of cwd, OS-safe, relocation-safe.

---

## SCORING GUIDE

| Score | Mastery              |
| ----- | -------------------- |
| 18–21 | Production-ready     |
| 14–17 | Strong foundation    |
| 10–13 | Needs reinforcement  |
| <10   | Revisit fundamentals |

---

If you want, next level can be **debug-the-code quizzes**, **predict-the-output puzzles**, or **design-level questions** where you choose the correct architecture.
