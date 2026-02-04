## FILE SYSTEM IN PYTHON — COMPLETE, PRECISE, AND PRACTICAL

---

## 1. WHAT “FILE SYSTEM” MEANS IN PYTHON

The **file system** is the OS-managed structure where data is stored permanently on disk.
Python interacts with it through **file objects**, created using the built-in `open()` function.

Key responsibilities:

* Persist data beyond program execution
* Read external data into memory
* Write processed data back to disk
* Log, configure, cache, serialize information

---

## 2. CORE FILE HANDLING API: `open()`

### Function Signature

```python
open(file, mode="r", encoding=None)
```

### Parameters

| Parameter  | Meaning                             |
| ---------- | ----------------------------------- |
| `file`     | Path to file (relative or absolute) |
| `mode`     | How the file is opened              |
| `encoding` | Text encoding (UTF-8 recommended)   |

---

## 3. FILE PATHS (IMPORTANT CONTEXT)

### Relative Path

```python
open("data.txt")
```

Resolved relative to the script’s working directory.

### Absolute Path

```python
open("C:/Users/Alex/Documents/data.txt")
```

### Cross-platform Safe Path

```python
open(r"C:\Users\Alex\Documents\data.txt")
```

---

## 4. FILE MODES — COMPLETE AND CLASSIFIED

### TEXT MODES (DEFAULT)

| Mode   | Meaning          | Behavior        |
| ------ | ---------------- | --------------- |
| `"r"`  | Read             | File must exist |
| `"w"`  | Write            | Overwrites file |
| `"a"`  | Append           | Writes at end   |
| `"x"`  | Exclusive create | Fails if exists |
| `"r+"` | Read + write     | No truncation   |
| `"w+"` | Write + read     | Truncates file  |
| `"a+"` | Append + read    | Cursor at end   |

---

### BINARY MODES

Add `b` to any mode:

| Mode    | Purpose           |
| ------- | ----------------- |
| `"rb"`  | Read binary       |
| `"wb"`  | Write binary      |
| `"ab"`  | Append binary     |
| `"rb+"` | Binary read/write |

Used for:

* Images
* Audio
* Videos
* Encrypted data
* Serialized objects

---

## 5. READING FILES — ALL METHODS

### A. Read Entire File

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(content)
```

**Expected Output**

```
(file contents)
```

**Notes**

* Loads entire file into memory
* Not suitable for large files

---

### B. Read Line by Line

```python
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())
```

**Why this matters**

* Memory efficient
* Ideal for logs and large files

---

### C. Read All Lines into List

```python
with open("data.txt", "r") as f:
    lines = f.readlines()

print(lines)
```

**Expected Output**

```
['line1\n', 'line2\n']
```

---

## 6. WRITING FILES — SAFE AND UNSAFE CASES

### A. Write (Overwrite)

```python
with open("output.txt", "w") as f:
    f.write("Hello\n")
    f.write("World\n")
```

**Result**

```
Hello
World
```

**Critical**

* Deletes existing content

---

### B. Append

```python
with open("log.txt", "a") as f:
    f.write("New entry\n")
```

Adds content safely without deletion.

---

### C. Write Multiple Lines

```python
lines = ["one\n", "two\n", "three\n"]

with open("numbers.txt", "w") as f:
    f.writelines(lines)
```

---

## 7. THE `with` KEYWORD — WHY IT IS NON-NEGOTIABLE

### Problem Without `with`

```python
f = open("data.txt", "r")
data = f.read()
# file remains open if error occurs
```

### Correct Pattern

```python
with open("data.txt", "r") as f:
    data = f.read()
# file ALWAYS closed here
```

### Guarantees

* Automatic file closure
* No file lock leaks
* Exception-safe
* Cleaner code

---

## 8. FILE POINTER (CURSOR) BEHAVIOR

```python
with open("data.txt", "r") as f:
    print(f.read(5))
    print(f.read(5))
```

**Expected Output**

```
Hello
World
```

The cursor moves forward automatically.

---

### Reset Cursor

```python
f.seek(0)
```

---

## 9. ERROR HANDLING WITH FILES

### Common Exceptions

| Exception            | Cause             |
| -------------------- | ----------------- |
| `FileNotFoundError`  | File missing      |
| `PermissionError`    | No access         |
| `IsADirectoryError`  | Opened folder     |
| `UnicodeDecodeError` | Encoding mismatch |

---

### Safe Pattern

```python
try:
    with open("missing.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("File not found")
```

**Expected Output**

```
File not found
```

---

## 10. TEXT VS BINARY — KEY DIFFERENCE

### Text Mode

* Returns `str`
* Encoding applied
* Human-readable

### Binary Mode

* Returns `bytes`
* No encoding
* Raw data

```python
with open("image.png", "rb") as f:
    data = f.read()

print(type(data))
```

**Expected Output**

```
<class 'bytes'>
```

---

## 11. REAL-WORLD FILE HANDLING PATTERNS

### Configuration Files

```python
with open("config.txt") as f:
    settings = f.read()
```

### Logging

```python
with open("app.log", "a") as f:
    f.write("ERROR occurred\n")
```

### Data Persistence

```python
with open("score.txt", "w") as f:
    f.write(str(score))
```

---

## 12. SUMMARY TABLE — MODES AT A GLANCE

| Mode | Exists?  | Truncate? | Cursor |
| ---- | -------- | --------- | ------ |
| `r`  | Must     | No        | Start  |
| `w`  | Optional | Yes       | Start  |
| `a`  | Optional | No        | End    |
| `x`  | Must not | N/A       | Start  |
| `r+` | Must     | No        | Start  |
| `w+` | Optional | Yes       | Start  |
| `a+` | Optional | No        | End    |

---

## 13. WHY PYTHON FILE SYSTEM IS CONSIDERED EXCELLENT

* Minimal syntax
* Explicit behavior
* Strong OS abstraction
* Safe defaults via `with`
* Scales from scripts to production systems
