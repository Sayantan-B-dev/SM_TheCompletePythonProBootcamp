## PYTHON FILE OBJECT METHODS — COMPLETE, DEEP, AND PRACTICAL REFERENCE

---

## CORE FILE OBJECT METHODS (TEXT MODE)

| Method        | Syntax           | What It Does      | Cursor Behavior    | Return Type | Real-Life Use Case  | Tricky Detail             |
| ------------- | ---------------- | ----------------- | ------------------ | ----------- | ------------------- | ------------------------- |
| `read()`      | `f.read()`       | Reads entire file | Moves to EOF       | `str`       | Load config file    | Dangerous for large files |
| `read(n)`     | `f.read(10)`     | Reads `n` chars   | Moves `n` chars    | `str`       | Chunk processing    | Cursor remembers position |
| `readline()`  | `f.readline()`   | Reads one line    | Moves to next line | `str`       | Log streaming       | Includes `\n`             |
| `readlines()` | `f.readlines()`  | Reads all lines   | Moves to EOF       | `list[str]` | Small text files    | Memory heavy              |
| iteration     | `for line in f:` | Line-by-line read | Lazy               | `str`       | Best for large logs | Fast & memory-safe        |

---

## READ METHODS — DETAILED EXAMPLES

### `read()`

```python
with open("data.txt", "r") as f:
    content = f.read()
    print(content)
```

**Expected Output**

```
Entire file content
```

**When to use**

* Config files
* Small text files

**When NOT to use**

* Large logs
* Huge datasets

---

### `read(n)` — PARTIAL READ (VERY IMPORTANT)

```python
with open("data.txt") as f:
    print(f.read(4))
    print(f.read(4))
```

**File**

```
ABCDEFGH
```

**Expected Output**

```
ABCD
EFGH
```

Cursor moves forward automatically.

---

### `readline()` — STREAMING BEHAVIOR

```python
with open("data.txt") as f:
    print(f.readline())
    print(f.readline())
```

**File**

```
one
two
three
```

**Expected Output**

```
one

two
```

Newline is preserved.

---

### `readlines()` — BULK READ

```python
with open("data.txt") as f:
    lines = f.readlines()
    print(lines)
```

**Expected Output**

```
['one\n', 'two\n', 'three\n']
```

Not suitable for large files.

---

### ITERATION — BEST PRACTICE

```python
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```

**Why this is best**

* Lazy loading
* Memory efficient
* Clean syntax

---

## WRITE METHODS — ALL VARIANTS

| Method         | Syntax               | Purpose              | Overwrites      | Return        | Real Use            |
| -------------- | -------------------- | -------------------- | --------------- | ------------- | ------------------- |
| `write()`      | `f.write(str)`       | Write text           | Depends on mode | chars written | Logs                |
| `writelines()` | `f.writelines(list)` | Write multiple lines | Depends         | `None`        | Bulk output         |
| `flush()`      | `f.flush()`          | Force disk write     | No              | None          | Critical logs       |
| `close()`      | `f.close()`          | Close file           | No              | None          | Rare (avoid manual) |

---

### `write()`

```python
with open("log.txt", "w") as f:
    f.write("Hello\n")
    f.write("World\n")
```

**Expected Output**

```
Hello
World
```

---

### `writelines()` (NO NEWLINES ADDED)

```python
lines = ["A\n", "B\n", "C\n"]

with open("out.txt", "w") as f:
    f.writelines(lines)
```

**Trick**
`writelines()` does **not** insert `\n`.

---

## FILE POINTER / CURSOR CONTROL

| Method                 | Purpose            | Example         | Tricky Point |
| ---------------------- | ------------------ | --------------- | ------------ |
| `tell()`               | Current cursor pos | `f.tell()`      | Byte-based   |
| `seek(pos)`            | Move cursor        | `f.seek(0)`     | Absolute     |
| `seek(offset, whence)` | Relative seek      | `f.seek(-5, 2)` | Binary only  |

---

### `tell()` & `seek()`

```python
with open("data.txt") as f:
    print(f.read(3))
    print(f.tell())
    f.seek(0)
    print(f.read(3))
```

**Output**

```
ABC
3
ABC
```

---

## FILE STATE & METADATA METHODS

| Method       | Meaning      | Real Use   |
| ------------ | ------------ | ---------- |
| `readable()` | Can read?    | Validation |
| `writable()` | Can write?   | Safety     |
| `seekable()` | Can seek?    | Binary ops |
| `closed`     | File closed? | Debug      |

---

### Example

```python
with open("data.txt", "r") as f:
    print(f.readable())
    print(f.writable())
```

**Output**

```
True
False
```

---

## BINARY FILE METHODS (IMPORTANT)

Binary files behave the same, but data is `bytes`.

```python
with open("image.png", "rb") as f:
    chunk = f.read(1024)
    print(type(chunk))
```

**Output**

```
<class 'bytes'>
```

---

## COMMON TRICKY SITUATIONS (VERY IMPORTANT)

### 1. Reading After Writing Without Seek

```python
with open("data.txt", "w+") as f:
    f.write("Hello")
    print(f.read())
```

**Output**

```
(empty)
```

**Why**
Cursor is at end. Fix:

```python
f.seek(0)
```

---

### 2. Forgetting Newlines in `writelines()`

```python
f.writelines(["A", "B", "C"])
```

Result:

```
ABC
```

---

### 3. Reading Empty Result

```python
f.read()
f.read()
```

Second call returns empty string — cursor already at EOF.

---

### 4. Mixing Text and Binary

```python
open("img.png", "r")  # WRONG
```

Causes decode errors.

---

## REAL-WORLD METHOD SELECTION GUIDE

| Scenario           | Best Method     |
| ------------------ | --------------- |
| Config file        | `read()`        |
| Huge log           | `for line in f` |
| Live streaming     | `readline()`    |
| Small dataset      | `readlines()`   |
| Writing logs       | `write()`       |
| Bulk output        | `writelines()`  |
| File checkpointing | `flush()`       |

---

## FINAL MENTAL MODEL (IMPORTANT)

```
File = stream of characters or bytes
Cursor = invisible pointer
Read/write = moves cursor
seek() = teleport cursor
with = guarantees cleanup
```
