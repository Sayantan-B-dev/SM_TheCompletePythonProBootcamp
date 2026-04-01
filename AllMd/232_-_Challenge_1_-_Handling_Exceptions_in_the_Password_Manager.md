>From  /Section_029_-_Day_29_-_Intermediate_-_Building_a_Password_Manager_GUI_App_with_Tkinter/password-manager/storage.py

## Purpose of this code (high-level intent)

This code implements a **safe, persistent credential storage mechanism** using a JSON file.
It ensures that credentials are **added or updated** without breaking the JSON structure, even when the file is missing, empty, or corrupted.

The design follows the **load → modify → write** rule, which is the only correct way to work with JSON files.

---

## Line-by-line and concept-by-concept explanation

---

## `import json`

### What this does

Imports Python’s **standard JSON module**, which provides tools to:

| Function               | Purpose                               |
| ---------------------- | ------------------------------------- |
| `json.load()`          | Convert JSON file → Python dictionary |
| `json.dump()`          | Convert Python dictionary → JSON file |
| `json.JSONDecodeError` | Error raised for invalid JSON         |

### Why needed

JSON is **text**, Python works with **objects**.
This module is the translator between them.

---

## `DATA_FILE = "data/passwords.json"`

### What this represents

A **single source of truth** for the file path.

### Why this is professional practice

* Avoids hardcoding paths in multiple places
* Easy to change file location later
* Makes testing easier

---

## `def save_credentials(website, username, password):`

### Function responsibility

This function:

1. Accepts credentials
2. Safely loads existing JSON data
3. Inserts or updates credentials
4. Writes everything back to disk

### Design principle used

> **Single responsibility**
> The function does one thing: *persist credentials safely*.

---

## `new_data = { ... }`

```python
new_data = {
    website: {
        "username": username,
        "password": password
    }
}
```

### What this creates

A **nested dictionary**, structured like JSON:

```json
{
  "example.com": {
    "username": "user123",
    "password": "pass123"
  }
}
```

### Why website is used as a key

* Ensures **unique identification**
* Prevents duplicate entries
* Allows overwrite/update behavior

### Important behavior

If the same website already exists, `update()` will **replace it**.

---

## `try:` block (critical part)

```python
try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
```

### What is happening

1. Opens the JSON file in **read mode**
2. Reads the entire file content
3. Parses JSON text into a Python dictionary

### Why wrapped in `try`

Because **multiple things can fail** here:

* File may not exist
* File may exist but contain invalid JSON

---

## `with open(...) as file:`

### Why `with` is used

The `with` statement guarantees:

* File is closed automatically
* Even if an exception occurs
* Prevents file corruption and leaks

Equivalent to:

```python
file = open(...)
try:
    ...
finally:
    file.close()
```

---

## `json.load(file)`

### What it does

* Reads JSON text
* Validates structure
* Converts it into a Python dictionary

### What it returns

Always one Python object (usually a `dict`).

---

## `except FileNotFoundError:`

```python
except FileNotFoundError:
    data = {}
```

### When this happens

* The JSON file does **not exist yet**
* Common on first program run

### Why this is correct handling

Instead of crashing:

* Start with an empty dictionary
* Create the file later during write

### Important design decision

> Missing file is **not an error**, it’s a valid first-run state.

---

## `except json.JSONDecodeError:`

```python
except json.JSONDecodeError:
    data = {}
```

### When this happens

* File exists but:

  * Is empty
  * Is partially written
  * Contains invalid JSON

Examples of invalid JSON:

```json
{ username: "abc" }   // keys not quoted
```

```json
{ "a": 1, }           // trailing comma
```

### Why this handling is necessary

* Prevents program crash
* Allows recovery
* Treats corrupted file as reset state

---

## Why both exceptions are handled separately

| Error               | Meaning                  |
| ------------------- | ------------------------ |
| `FileNotFoundError` | No file yet              |
| `JSONDecodeError`   | File exists but unusable |

They are **semantically different**, even though recovery is the same.

This separation improves:

* Debugging
* Logging clarity
* Future extension

---

## `data.update(new_data)`

### What `update()` does

Merges dictionaries **in place**.

Behavior:

* Adds new key if missing
* Replaces value if key exists

### Example

```python
data = {
    "google.com": {...}
}

new_data = {
    "github.com": {...}
}

data.update(new_data)
```

Result:

```python
{
    "google.com": {...},
    "github.com": {...}
}
```

### Why `update()` instead of append

JSON objects do **not support append**.
Appending would break JSON structure.

---

## Overwrite behavior (important)

If this exists:

```json
"google.com": { "username": "old", "password": "old" }
```

And you add:

```python
"google.com": { "username": "new", "password": "new" }
```

Result:

```json
"google.com": { "username": "new", "password": "new" }
```

This is **intentional** and correct.

---

## Writing back to file

```python
with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)
```

### Why open in `"w"` mode

* Completely rewrites the file
* Ensures valid JSON structure
* Prevents partial updates

### Why rewrite instead of append

JSON must be **one single valid object**.
Appending would corrupt the file.

---

## `json.dump(data, file, indent=4)`

### What it does

* Converts Python dictionary → JSON text
* Writes it to the file

### `indent=4`

Makes JSON human-readable:

```json
{
    "google.com": {
        "username": "abc",
        "password": "xyz"
    }
}
```

Without indent:

```json
{"google.com":{"username":"abc","password":"xyz"}}
```

---

## Full execution flow (step-by-step)

1. User calls `save_credentials(...)`
2. New credential structure is prepared
3. Program attempts to read existing JSON
4. If file missing or broken → start fresh
5. New credentials merged into existing data
6. Entire dataset rewritten safely
7. File closed automatically

---

## Why this pattern is **industry-grade**

This code correctly handles:

| Scenario          | Result       |
| ----------------- | ------------ |
| First run         | File created |
| File deleted      | Recovered    |
| File corrupted    | Recovered    |
| Existing data     | Preserved    |
| Duplicate website | Updated      |
| Crash during read | Safe         |

---

## Why `update()` is better than append (final clarity)

| Action    | Result        |
| --------- | ------------- |
| Append    | Invalid JSON  |
| Overwrite | Data loss     |
| Update    | Correct merge |

---

## Mental model to remember

> JSON files are **snapshots**, not streams.

You must:

```
load → modify → write
```

Anything else is unsafe.

---

## Final professional assessment

This function demonstrates:

* Correct exception handling
* Safe persistence
* JSON integrity preservation
* Clean, maintainable structure

This is **production-quality JSON handling**, not beginner code.
