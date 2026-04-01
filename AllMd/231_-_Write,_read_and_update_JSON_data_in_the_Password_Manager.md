## JSON — what it is, why it exists, and how data moves “here and there”

---

## 1. What JSON actually is

**JSON (JavaScript Object Notation)** is a **text-based data interchange format**.

Key properties:

| Property          | Meaning                                 |
| ----------------- | --------------------------------------- |
| Text-based        | Human-readable plain text               |
| Language-agnostic | Works across Python, JS, Java, Go, etc. |
| Structured        | Represents nested data                  |
| Portable          | Easy to send over network or store      |

> JSON is **not a Python feature**.
> Python only *understands* JSON through conversion.

---

## 2. Why JSON exists (real reason)

Before JSON:

* Programs stored data in **language-specific formats**
* Python → `dict`
* Java → `Map`
* C → `struct`

Problem:

* These formats **cannot travel between programs**

Solution:

> Convert internal data → JSON → transmit/store → convert back

---

## 3. JSON data model (very important)

JSON supports **only these types**:

| JSON Type | Example         | Python Equivalent |
| --------- | --------------- | ----------------- |
| object    | `{ "a": 1 }`    | `dict`            |
| array     | `[1, 2, 3]`     | `list`            |
| string    | `"hello"`       | `str`             |
| number    | `10`, `3.14`    | `int`, `float`    |
| boolean   | `true`, `false` | `True`, `False`   |
| null      | `null`          | `None`            |

Anything outside this **cannot exist in JSON**.

---

## 4. Example JSON structure (realistic)

```json
{
  "user": {
    "id": 101,
    "name": "Alice",
    "skills": ["Python", "SQL"],
    "active": true
  }
}
```

---

## 5. JSON vs Python dictionary (critical difference)

| Aspect      | Python dict | JSON                |
| ----------- | ----------- | ------------------- |
| Lives where | Memory      | Text file / network |
| Comments    | Allowed     | Not allowed         |
| Data types  | Any         | Limited             |
| Functions   | Allowed     | Impossible          |

JSON is **data only**, no behavior.

---

## 6. Python JSON module (standard library)

```python
import json
```

This module handles:

* Serialization (Python → JSON)
* Deserialization (JSON → Python)

---

## 7. Loading JSON from a file (read)

### JSON file (`data.json`)

```json
{
  "name": "Alice",
  "age": 25
}
```

### Python code

```python
import json

with open("data.json", "r") as file:
    data = json.load(file)  # JSON → Python dict

print(data)
print(type(data))
```

**Expected output**

```
{'name': 'Alice', 'age': 25}
<class 'dict'>
```

---

## 8. Loading JSON from a string (network-style)

```python
json_text = '{"x": 10, "y": 20}'

data = json.loads(json_text)  # note the 's'
print(data)
```

**Output**

```
{'x': 10, 'y': 20}
```

---

## 9. Writing JSON to a file (basic)

```python
import json

data = {
    "product": "Laptop",
    "price": 75000
}

with open("product.json", "w") as file:
    json.dump(data, file)
```

Resulting file:

```json
{"product": "Laptop", "price": 75000}
```

---

## 10. Making JSON **beautiful / readable** (important)

### Problem

Default JSON is **compressed**, hard to read.

### Solution: `indent` + `sort_keys`

```python
with open("product.json", "w") as file:
    json.dump(data, file, indent=4, sort_keys=True)
```

Readable file:

```json
{
    "price": 75000,
    "product": "Laptop"
}
```

---

## 11. Why loaded JSON looks “ugly” in Python

When loaded:

```python
print(data)
```

You see:

```
{'price': 75000, 'product': 'Laptop'}
```

This is:

* Python’s **representation**
* Not JSON formatting

---

## 12. Pretty-print JSON data in Python

### Option 1: `json.dumps` for display

```python
pretty = json.dumps(data, indent=4)
print(pretty)
```

**Output**

```json
{
    "price": 75000,
    "product": "Laptop"
}
```

---

## 13. Updating JSON file data (correct way)

### ❌ WRONG: appending JSON

```python
# This breaks JSON structure
file.write(new_data)
```

JSON must remain **one valid structure**.

---

## 14. ✅ CORRECT: load → update → write

```python
import json

with open("data.json", "r") as file:
    data = json.load(file)

# Update dictionary
data["age"] = 26

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)
```

---

## 15. Why update is better than append (important)

### Append breaks JSON

```json
{ "a": 1 }
{ "b": 2 }   ← INVALID JSON
```

### JSON must be **single root**

```json
{
  "a": 1,
  "b": 2
}
```

---

## 16. Appending data properly (lists inside JSON)

### JSON file

```json
{
  "users": []
}
```

### Python code

```python
with open("users.json", "r") as file:
    data = json.load(file)

data["users"].append({"id": 1, "name": "Alice"})

with open("users.json", "w") as file:
    json.dump(data, file, indent=4)
```

---

## 17. JSON + loops (reading multiple records)

```python
with open("users.json") as f:
    data = json.load(f)

for user in data["users"]:
    print(user["name"])
```

---

## 18. Handling missing keys while reading JSON

```python
try:
    print(data["email"])
except KeyError:
    print("Email field missing")
```

---

## 19. JSON + comprehension (filtering)

```python
active_users = [
    u for u in data["users"]
    if u.get("active", False)
]
```

---

## 20. JSON + recursion (nested structures)

```python
def print_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(k)
            print_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            print_keys(item)
```

---

## 21. JSON serialization limitations (must-know)

### This fails:

```python
data = {"time": datetime.now()}
json.dumps(data)
```

Reason:

* `datetime` is not JSON-serializable

---

## 22. Fixing non-JSON types

```python
json.dumps(data, default=str)
```

---

## 23. JSON in real systems (where data goes)

| Source       | JSON role               |
| ------------ | ----------------------- |
| REST APIs    | Request / response body |
| Config files | App settings            |
| Databases    | Document storage        |
| Logs         | Structured logging      |
| Frontend     | State transfer          |

---

## 24. Mental model (very important)

> JSON is a **bridge**, not a container.

Flow:

```
Python dict
   ↓ serialize
JSON text
   ↓ store / send
JSON text
   ↓ deserialize
Python dict
```

---

## 25. Final truths to remember

* JSON is strict
* Append breaks JSON
* Update preserves structure
* Pretty-print is for humans
* Load → modify → dump is the only safe workflow
