## FILE PATHS IN PYTHON — ABSOLUTE vs RELATIVE, WORKING DIRECTORY, AND DIRECTORY TREE NAVIGATION

---

## 1. THE FILE SYSTEM AS A TREE (MENTAL MODEL)

Every operating system organizes files as a **hierarchical tree**.

```
Root
 ├── Folder A
 │    ├── file1.txt
 │    └── Folder B
 │         └── file2.txt
 └── Folder C
      └── file3.txt
```

Key rules:

* There is **one root**
* Every file has **exactly one absolute path**
* Relative paths depend on **where your program is running**

---

## 2. WHAT IS THE WORKING DIRECTORY (CRITICAL CONCEPT)

### Definition

The **working directory** is the directory Python considers as `"."` (current location).

Python resolves **all relative paths from here**.

---

### Check Current Working Directory

```python
import os

print(os.getcwd())
```

**Expected Output**

```
C:\Users\Alex\Projects\snake_game
```

This means:

```python
open("data.txt")
```

actually means:

```python
open("C:/Users/Alex/Projects/snake_game/data.txt")
```

---

## 3. RELATIVE PATHS (DEPENDENT ON CONTEXT)

### Definition

A **relative path** describes a file location **relative to the working directory**.

---

### Example Directory Structure

```
snake_game/
 ├── main.py
 ├── data.txt
 └── assets/
      └── image.png
```

---

### Same Directory

```python
open("data.txt", "r")
```

Meaning:

```
./data.txt
```

---

### Inside a Subfolder

```python
open("assets/image.png", "rb")
```

Meaning:

```
./assets/image.png
```

---

### Move UP One Level (`..`)

```python
open("../config.txt", "r")
```

Meaning:

```
Parent folder → config.txt
```

---

### Move Up Multiple Levels

```python
open("../../shared/data.txt", "r")
```

Each `..` moves **one level upward**.

---

## 4. ABSOLUTE PATHS (INDEPENDENT, FIXED, GLOBAL)

### Definition

An **absolute path** starts from the **root of the file system**.

It never depends on:

* Working directory
* Script location
* How program was launched

---

### Windows Absolute Path

```python
open("C:/Users/Alex/Documents/data.txt")
```

---

### Linux / macOS Absolute Path

```python
open("/home/alex/Documents/data.txt")
```

---

### Key Property

| Aspect         | Absolute Path |
| -------------- | ------------- |
| Depends on cwd | No            |
| Portable       | No            |
| Reliable       | Yes           |
| Verbose        | Yes           |

---

## 5. DIFFERENT DRIVE, DIFFERENT ROOT (WINDOWS)

Windows has **multiple roots**.

```
C:\  ← one root
D:\  ← another root
```

### Access Different Drive

```python
open("D:/Movies/video.mp4", "rb")
```

Relative paths **cannot cross drives**.

This will **never work**:

```python
open("../D:/Movies/video.mp4")
```

---

## 6. WHY RELATIVE PATHS FAIL (COMMON BUG SOURCE)

### Example

```python
open("data.txt")
```

Works in terminal:

```
cd snake_game
python main.py
```

Fails in IDE or double-click:

* Working directory changes
* File not found

---

### Diagnose

```python
print(os.getcwd())
```

Mismatch between **expected** and **actual** cwd is the cause.

---

## 7. SAFE, PROFESSIONAL PATH HANDLING (`os.path`)

### Join Paths Correctly (Cross-Platform)

```python
import os

path = os.path.join("assets", "image.png")
open(path, "rb")
```

Why this matters:

* Windows uses `\`
* Linux/macOS use `/`
* `os.path.join()` handles both

---

## 8. SCRIPT LOCATION vs WORKING DIRECTORY (IMPORTANT DISTINCTION)

### `__file__` — Location of Script

```python
import os

BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
```

### Build Absolute Path Relative to Script

```python
data_path = os.path.join(BASE_DIR, "data.txt")
open(data_path, "r")
```

This works **no matter where the program is launched from**.

---

## 9. BEST PRACTICE FOR PROJECTS

### Recommended Pattern

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")

with open(DATA_FILE, "r") as f:
    print(f.read())
```

### Why this is correct

| Problem            | Solved |
| ------------------ | ------ |
| IDE cwd mismatch   | Yes    |
| Terminal execution | Yes    |
| Script relocation  | Yes    |
| OS differences     | Yes    |

---

## 10. ACCESSING FILES FROM COMPLETELY DIFFERENT LOCATIONS

### Case 1: User Documents Folder

```python
open("C:/Users/Alex/Documents/report.txt")
```

### Case 2: External Drive

```python
open("E:/backup/data.csv")
```

### Case 3: Network Path (Windows)

```python
open(r"\\Server\Share\data.txt")
```

---

## 11. PATH SYMBOLS SUMMARY

| Symbol | Meaning                      |
| ------ | ---------------------------- |
| `.`    | Current directory            |
| `..`   | Parent directory             |
| `/`    | Root (Unix)                  |
| `C:\`  | Root (Windows drive)         |
| `~`    | Home directory (Unix shells) |

Note:
Python does **not** expand `~` automatically.
Use:

```python
os.path.expanduser("~")
```

---

## 12. PATH DEBUGGING CHECKLIST

When a file fails to load:

1. Print working directory
2. Confirm file exists
3. Confirm correct path separator
4. Check permissions
5. Avoid hardcoding cwd assumptions

---

## 13. DECISION TABLE — WHEN TO USE WHAT

| Situation              | Use                     |
| ---------------------- | ----------------------- |
| Small script           | Relative path           |
| Production app         | Absolute via `__file__` |
| User-selected files    | Absolute                |
| Cross-platform project | `os.path.join()`        |
| Different drive        | Absolute only           |

---

## 14. FINAL EXECUTION MODEL

```
Python does NOT search your computer.
Python opens EXACTLY the path you give.
Relative paths depend on cwd.
Absolute paths ignore cwd.
```

Understanding paths is understanding **how Python sees the file system**, not how you see it visually.
