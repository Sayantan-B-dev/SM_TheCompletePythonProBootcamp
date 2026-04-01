### Python Strings, Data Types, Indexing & Type Conversion — Detailed Tables with Examples

---

## **1. Python Data Types (Core Types)**

| Data Type  | Description        | Example Code      | Result     |
| ---------- | ------------------ | ----------------- | ---------- |
| `int`      | Whole numbers      | `x = 10`          | `10`       |
| `float`    | Decimal numbers    | `pi = 3.14`       | `3.14`     |
| `str`      | Text / characters  | `name = "Python"` | `"Python"` |
| `bool`     | True / False       | `is_valid = True` | `True`     |
| `list`     | Ordered, mutable   | `[1, 2, 3]`       | List       |
| `tuple`    | Ordered, immutable | `(1, 2, 3)`       | Tuple      |
| `set`      | Unordered, unique  | `{1, 2, 3}`       | Set        |
| `dict`     | Key–value pairs    | `{"a": 1}`        | Dictionary |
| `NoneType` | No value           | `x = None`        | `None`     |

---

## **2. String Indexing Methods**

| Index Type       | Example          | Output     | Explanation       |
| ---------------- | ---------------- | ---------- | ----------------- |
| Positive index   | `"Python"[0]`    | `'P'`      | Starts from left  |
| Positive index   | `"Python"[3]`    | `'h'`      | Zero-based        |
| Negative index   | `"Python"[-1]`   | `'n'`      | Last character    |
| Negative index   | `"Python"[-3]`   | `'h'`      | From right        |
| Slice start:end  | `"Python"[0:4]`  | `'Pyth'`   | End excluded      |
| Slice start only | `"Python"[2:]`   | `'thon'`   | From index onward |
| Slice end only   | `"Python"[:3]`   | `'Pyt'`    | From start        |
| Full slice       | `"Python"[:]`    | `'Python'` | Copy string       |
| Step slicing     | `"Python"[::2]`  | `'Pto'`    | Skip chars        |
| Reverse string   | `"Python"[::-1]` | `'nohtyP'` | Reverse order     |

---

## **3. String Functions & Methods**

| Function       | Example                         | Output          | Use Case     |
| -------------- | ------------------------------- | --------------- | ------------ |
| `len()`        | `len("Python")`                 | `6`             | Length       |
| `upper()`      | `"python".upper()`              | `PYTHON`        | Capitalize   |
| `lower()`      | `"PYTHON".lower()`              | `python`        | Normalize    |
| `title()`      | `"hello world".title()`         | `Hello World`   | Headings     |
| `strip()`      | `" hi ".strip()`                | `hi`            | Clean input  |
| `replace()`    | `"hi all".replace("all","you")` | `hi you`        | Modify text  |
| `find()`       | `"python".find("t")`            | `2`             | Index lookup |
| `count()`      | `"banana".count("a")`           | `3`             | Frequency    |
| `split()`      | `"a,b,c".split(",")`            | `['a','b','c']` | Tokenize     |
| `join()`       | `" ".join(["Hi","there"])`      | `Hi there`      | Merge list   |
| `startswith()` | `"hello".startswith("he")`      | `True`          | Validation   |
| `endswith()`   | `"file.txt".endswith(".txt")`   | `True`          | File checks  |

---

## **4. Type Conversion (Casting)**

| Conversion    | Example        | Result  | Notes           |
| ------------- | -------------- | ------- | --------------- |
| `str → int`   | `int("25")`    | `25`    | Must be numeric |
| `str → float` | `float("3.5")` | `3.5`   | Decimal allowed |
| `int → str`   | `str(100)`     | `"100"` | Display         |
| `float → int` | `int(3.9)`     | `3`     | Truncates       |
| `int → float` | `float(5)`     | `5.0`   | Math ops        |
| `any → bool`  | `bool("Hi")`   | `True`  | Non-empty       |
| empty → bool  | `bool("")`     | `False` | Empty false     |

---

## **5. `len()` with Different Data Types**

| Data Type | Example              | Output | Explanation  |
| --------- | -------------------- | ------ | ------------ |
| String    | `len("Code")`        | `4`    | Characters   |
| List      | `len([1,2,3])`       | `3`    | Elements     |
| Tuple     | `len((1,2))`         | `2`    | Items        |
| Set       | `len({1,2,3})`       | `3`    | Unique items |
| Dict      | `len({"a":1,"b":2})` | `2`    | Keys count   |

---

## **6. Common Errors & Fixes**

| Error            | Example           | Fix            |
| ---------------- | ----------------- | -------------- |
| TypeError        | `"Age: " + 25`    | `f"Age: {25}"` |
| ValueError       | `int("abc")`      | Validate input |
| IndexError       | `"Hi"[5]`         | Check length   |
| IndentationError | Mixed spaces/tabs | Use 4 spaces   |

---

## **Key Professional Takeaways**

* Strings are **immutable**
* Indexing is zero-based
* Negative indexing is powerful
* Always convert input explicitly
* Use slicing instead of loops when possible
* Validate before casting

This structure covers **how Python handles text and data internally**, which is critical before moving into logic, loops, and real-world applications.
