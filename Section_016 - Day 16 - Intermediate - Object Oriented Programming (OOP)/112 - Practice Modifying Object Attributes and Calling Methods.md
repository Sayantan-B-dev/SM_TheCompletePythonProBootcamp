## Important and Interesting Python Packages (What They Do and How You Use Them)

---

## 1. `requests` — Talking to the Internet

### What problem it solves

* Sending HTTP requests (GET, POST, PUT, DELETE)
* Communicating with APIs
* Downloading data from the web

Without it:

* You deal with low-level sockets
* Complex headers and encoding

With it:

* Clean, readable, object-oriented API

---

### Object-Oriented View

```text
Response object
 ├─ status_code
 ├─ headers
 ├─ text
 └─ json()
```

---

### Example

```python
import requests

# Sending a GET request
response = requests.get("https://api.github.com")

# Accessing attributes and methods
print(response.status_code)
print(response.headers["Content-Type"])
```

**Expected Output**

```text
200
application/json; charset=utf-8
```

Why this is OOP:

* `response` is an object
* Data + behavior are bundled
* You interact only via methods and attributes

---

## 2. `datetime` — Time as Objects

### What problem it solves

* Date and time manipulation
* Time arithmetic
* Formatting and parsing

---

### Object Model

```text
datetime object
 ├─ year
 ├─ month
 ├─ day
 ├─ hour
 └─ strftime()
```

---

### Example

```python
from datetime import datetime

now = datetime.now()

print(now.year)
print(now.strftime("%Y-%m-%d %H:%M"))
```

**Expected Output**

```text
2026
2026-02-03 22:15
```

Why it matters:

* Time is stateful
* Methods operate on internal state
* Clean abstraction over system clock

---

## 3. `pathlib` — Files as Objects

### What problem it solves

* File paths across operating systems
* Cleaner than string-based paths

---

### Object-Oriented Idea

```text
Path object
 ├─ name
 ├─ suffix
 ├─ exists()
 ├─ read_text()
 └─ write_text()
```

---

### Example

```python
from pathlib import Path

file = Path("notes.txt")

file.write_text("Learning Python packages")
print(file.exists())
print(file.read_text())
```

**Expected Output**

```text
True
Learning Python packages
```

Why this is powerful:

* Files are treated as objects
* Methods reflect real-world actions

---

## 4. `collections` — Smarter Data Structures

### What problem it solves

* Common patterns like counting, queues, defaults
* Cleaner logic than manual dictionaries

---

### Example: `Counter`

```python
from collections import Counter

data = ["apple", "banana", "apple", "orange", "banana", "apple"]

counter = Counter(data)

print(counter["apple"])
print(counter)
```

**Expected Output**

```text
3
Counter({'apple': 3, 'banana': 2, 'orange': 1})
```

Why it’s OOP:

* `Counter` is a class
* Stores state
* Provides behavior like counting, updating

---

## 5. `random` — Controlled Randomness

### What problem it solves

* Games
* Simulations
* Randomized testing

---

### Example

```python
import random

numbers = [1, 2, 3, 4, 5]

choice = random.choice(numbers)
shuffle = random.sample(numbers, 3)

print(choice)
print(shuffle)
```

**Expected Output**

```text
3
[5, 1, 4]
```

Conceptually:

* Module exposes functions
* Internally uses objects to track state (seed, generator)

---

## 6. `logging` — Professional Output Control

### What problem it solves

* Debug printing chaos
* Production-grade logs

---

### Object Model

```text
Logger object
 ├─ info()
 ├─ warning()
 ├─ error()
 └─ setLevel()
```

---

### Example

```python
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

logger.info("Application started")
logger.warning("Low memory")
```

**Expected Output**

```text
INFO:app:Application started
WARNING:app:Low memory
```

Why professionals use it:

* Output is structured
* Can be redirected to files, servers
* Behavior controlled via objects

---

## 7. `argparse` — Command-Line Interfaces

### What problem it solves

* Reading command-line arguments
* Validation and help messages

---

### Example

```python
import argparse

parser = argparse.ArgumentParser(description="User tool")
parser.add_argument("--name")

args = parser.parse_args(["--name", "Sayantan"])

print(args.name)
```

**Expected Output**

```text
Sayantan
```

OOP angle:

* `ArgumentParser` object
* Stores configuration
* Parses input based on that state

---

## 8. `json` — Data Exchange Format

### What problem it solves

* Data exchange between systems
* API communication
* Configuration files

---

### Example

```python
import json

data = {"name": "Sayantan", "role": "Developer"}

json_string = json.dumps(data)
parsed = json.loads(json_string)

print(json_string)
print(parsed["role"])
```

**Expected Output**

```text
{"name": "Sayantan", "role": "Developer"}
Developer
```

---

## 9. `sqlite3` — Embedded Databases

### What problem it solves

* Lightweight databases
* No server required

---

### Object Interaction

```text
Connection → Cursor → Rows
```

---

### Example

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (name TEXT)")
cursor.execute("INSERT INTO users VALUES ('Sayantan')")

conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
```

**Expected Output**

```text
[('Sayantan',)]
```

Why it matters:

* Database handled via objects
* Clean separation of concerns

---

## 10. How to Think When Choosing a Package

```text
• What problem does it solve?
• What is the main class?
• What objects will I create?
• What methods do I call?
• What state does it manage?
```

---

## Mental Model Lock

```text
Packages give you:
• Ready-made classes
• Battle-tested logic
• Clean object interfaces

You give them:
• Inputs
• Configuration
• Method calls
```

This is how professional Python developers leverage important and interesting packages through objects.
