## FILE-BASED HIGH SCORE TRACKING — COMPLETE EXPLANATION

---

## CORE IDEA

The **file system** is used as **persistent storage** so the high score survives **program restarts**.
RAM values (`self.high_score`) disappear when the program closes; files do not.

Your implementation uses:

* `data.txt` → permanent storage
* `open()` → bridge between program memory and disk
* `read()` / `write()` → synchronization between runtime score and stored score

---

## FILE LIFECYCLE IN THIS SCOREBOARD

```
Program starts
    ↓
Read high score from file
    ↓
Game runs (score increases in RAM)
    ↓
Game ends
    ↓
If score > stored high score
    ↓
Overwrite file with new high score
```

---

## STEP-BY-STEP BREAKDOWN OF YOUR CODE

---

## 1. READING HIGH SCORE FROM FILE (INITIALIZATION PHASE)

```python
with open("data.txt", "r") as data:
    self.high_score = int(data.read())
```

### What happens internally

| Step                    | Explanation                              |
| ----------------------- | ---------------------------------------- |
| `open("data.txt", "r")` | Opens file in read-only mode             |
| `with`                  | Guarantees file closure                  |
| `data.read()`           | Reads entire file as a string            |
| `int(...)`              | Converts stored text to integer          |
| Assignment              | Stores value in RAM as `self.high_score` |

### Why conversion is mandatory

Files store **text**, not numbers.
Without `int()`, `self.high_score` would be a string and break comparisons.

---

## 2. WHY `with` IS CRITICAL HERE

```python
with open("data.txt", "r") as data:
```

### Guarantees

* File is **closed automatically**
* Prevents OS-level file locks
* Prevents corruption if an exception occurs
* Production-safe

Equivalent unsafe version (DO NOT USE):

```python
data = open("data.txt", "r")
self.high_score = int(data.read())
data.close()  # might never run if error occurs
```

---

## 3. SCORE INCREASE — MEMORY ONLY

```python
def increase_score(self):
    self.score += 1
    self.update_scoreboard()
```

### Important distinction

| Value             | Storage                 |
| ----------------- | ----------------------- |
| `self.score`      | RAM only (temporary)    |
| `self.high_score` | RAM + file (persistent) |

You **do not write to file every point**, which is correct.

Reason:

* Disk I/O is slow
* Writing every frame is unnecessary
* High score matters only at game end

---

## 4. RESET METHOD — WHERE FILE UPDATE HAPPENS

```python
def reset(self):
    if self.score > self.high_score:
        self.high_score = self.score
        with open("data.txt", "w") as data:
            data.write(f"{self.high_score}")
```

### Logic Flow

| Step               | Purpose                      |
| ------------------ | ---------------------------- |
| Compare scores     | Prevents lowering high score |
| Update RAM         | Immediate display update     |
| Open file in `"w"` | Overwrites old high score    |
| Write new value    | Permanent persistence        |

---

## 5. WHY `"w"` MODE IS CORRECT HERE

```python
with open("data.txt", "w") as data:
```

### `"w"` behavior

* Creates file if missing
* Deletes old content
* Writes clean new value

This guarantees:

* Only **one number** exists in file
* No trailing characters
* No corrupted values

---

## 6. WHY YOU DO NOT WRITE WHEN SCORE IS LOWER

```python
if self.score > self.high_score:
```

### Reasoning

High score rules:

* Must **never decrease**
* Must update **only when beaten**

This condition enforces score integrity.

---

## 7. SCORE RESET — MEMORY ONLY

```python
self.score = 0
```

### Why high score is NOT reset

* High score is historical
* Resetting it would defeat persistence
* File remains untouched unless beaten

---

## 8. DOUBLE CLEAR + REDRAW (WHY IT EXISTS)

```python
self.update_scoreboard()
self.clear()
self.goto(0, 270)
self.update_scoreboard()
```

### Why this is necessary

| Issue                        | Fix                    |
| ---------------------------- | ---------------------- |
| `game_over()` text at center | `clear()` removes it   |
| Cursor moved to center       | `goto(0,270)` restores |
| Score text overwritten       | Final redraw           |

This ensures:

* No overlapping text
* Clean UI reset
* Correct positioning

---

## 9. GAME OVER DOES NOT TOUCH FILE SYSTEM

```python
def game_over(self):
    self.goto(0, 0)
    self.write("GAME OVER ...")
```

### Design choice

* Game over is **visual only**
* Persistence logic belongs to `reset()`
* Separation of concerns

---

## 10. REQUIRED FILE CONTENT FORMAT

### `data.txt`

```
12
```

Rules:

* Only a number
* No spaces
* No newline required (safe either way)

---

## 11. COMMON FAILURE CASES AND FIXES

### File missing on first run

**Problem**

```python
FileNotFoundError
```

**Safe initialization**

```python
try:
    with open("data.txt", "r") as data:
        self.high_score = int(data.read())
except FileNotFoundError:
    self.high_score = 0
    with open("data.txt", "w") as data:
        data.write("0")
```

---

### Empty file

**Problem**

```python
ValueError: invalid literal for int()
```

**Cause**
File exists but contains nothing.

**Fix**
Ensure file always contains a valid number.

---

## 12. WHY THIS DESIGN IS CORRECT AND SCALABLE

| Aspect              | Reason     |
| ------------------- | ---------- |
| File I/O frequency  | Minimal    |
| Data integrity      | Guaranteed |
| Separation of logic | Clean      |
| Persistence         | Reliable   |
| Restart behavior    | Seamless   |

---

## 13. FINAL MENTAL MODEL

```
File = Permanent memory
RAM = Temporary memory

High Score:
    Read once → update conditionally → write once

Score:
    Update constantly → reset freely
```

This is **exactly how real games handle score persistence**, just with simpler storage instead of databases.
