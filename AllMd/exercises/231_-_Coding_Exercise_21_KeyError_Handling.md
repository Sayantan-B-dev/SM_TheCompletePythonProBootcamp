## `KeyError` — definition, mechanics, and **many distinct real-world handling patterns**

---

## 1. What exactly is `KeyError`

**Definition**
`KeyError` is raised when attempting to access a **dictionary key that does not exist**.

Applies to:

* `dict`
* dictionary-like objects (`defaultdict`, `Counter`, JSON objects)

---

## 2. Core rule (mental model)

> A dictionary does **not** guess keys.
> Asking for a missing key is a **contract violation**.

---

## 3. Basic `KeyError`

```python
user = {"name": "Alice", "age": 25}
print(user["email"])
```

**Error**

```
KeyError: 'email'
```

---

## 4. Simple `try–except` handling

```python
user = {"name": "Alice", "age": 25}

try:
    print(user["email"])
except KeyError:
    print("Key not found")
```

**Output**

```
Key not found
```

---

## 5. User input → dictionary access (very common)

```python
config = {"host": "localhost", "port": 5432}

try:
    key = input("Enter config key: ")
    print(config[key])
except KeyError:
    print("Invalid configuration key")
```

---

## 6. Loop-based `KeyError` (dynamic keys)

```python
prices = {"apple": 50, "banana": 30}

items = ["apple", "orange", "banana"]

try:
    for item in items:
        print(prices[item])
except KeyError as e:
    print("Missing price for:", e)
```

**Output**

```
50
Missing price for: 'orange'
```

---

## 7. Handling inside the loop (better control)

```python
prices = {"apple": 50, "banana": 30}

for item in ["apple", "orange", "banana"]:
    try:
        print(item, prices[item])
    except KeyError:
        print(item, "price not available")
```

---

## 8. `KeyError` in nested dictionaries (JSON-like)

```python
user = {
    "profile": {
        "name": "Alice"
    }
}

try:
    print(user["profile"]["email"])
except KeyError:
    print("Email not present in profile")
```

---

## 9. Multi-level protection (stepwise)

```python
data = {}

try:
    level1 = data["a"]
    level2 = level1["b"]
except KeyError:
    print("Missing nested key")
```

---

## 10. `KeyError` in dictionary comprehension

```python
data = {"a": 1, "b": 2}

keys = ["a", "b", "c"]

try:
    values = [data[k] for k in keys]
except KeyError as e:
    print("Key missing in comprehension:", e)
```

---

## 11. `KeyError` with deletion

```python
user = {"id": 1}

try:
    del user["email"]
except KeyError:
    print("Cannot delete non-existing key")
```

---

## 12. `KeyError` from `pop()`

```python
settings = {"theme": "dark"}

try:
    settings.pop("font")
except KeyError:
    print("Setting not found")
```

---

## 13. Safe pop with fallback (contrast)

```python
settings = {"theme": "dark"}
value = settings.pop("font", "default")
print(value)
```

**Output**

```
default
```

---

## 14. `KeyError` in aggregation logic

```python
scores = {"Alice": 90, "Bob": 85}

try:
    total = scores["Alice"] + scores["Charlie"]
except KeyError:
    print("Score missing for a student")
```

---

## 15. `KeyError` in counters (frequency maps)

```python
counts = {}

letters = "abc"

try:
    for ch in letters:
        counts[ch] += 1
except KeyError:
    print("Counter key not initialized")
```

---

## 16. Corrected version using handling

```python
counts = {}

for ch in "abc":
    try:
        counts[ch] += 1
    except KeyError:
        counts[ch] = 1

print(counts)
```

**Output**

```
{'a': 1, 'b': 1, 'c': 1}
```

---

## 17. `KeyError` in function return contracts

```python
def get_env(env, key):
    try:
        return env[key]
    except KeyError:
        raise ValueError("Environment variable missing")
```

---

## 18. `KeyError` turned into domain error (professional)

```python
class MissingFieldError(Exception):
    pass

payload = {"name": "Alice"}

try:
    print(payload["email"])
except KeyError as e:
    raise MissingFieldError("Required field missing") from e
```

---

## 19. `KeyError` with conditional logic (if-else + try)

```python
data = {"x": 10}

key = "y"

if key in data:
    print(data[key])
else:
    try:
        print(data[key])
    except KeyError:
        print("Fallback executed")
```

---

## 20. `KeyError` inside API-style handler

```python
def handle_request(request):
    try:
        user_id = request["user_id"]
    except KeyError:
        return {"error": "user_id required"}

    return {"user_id": user_id}
```

---

## 21. `KeyError` in configuration loading

```python
config = {"debug": True}

try:
    if config["production"]:
        print("Prod mode")
except KeyError:
    print("Production flag missing")
```

---

## 22. `KeyError` in grouping logic

```python
groups = {}

names = ["A", "B", "A"]

try:
    for name in names:
        groups[name].append(name)
except KeyError:
    print("Group not initialized")
```

---

## 23. Safe grouping using handling

```python
groups = {}

for name in ["A", "B", "A"]:
    try:
        groups[name].append(name)
    except KeyError:
        groups[name] = [name]

print(groups)
```

**Output**

```
{'A': ['A', 'A'], 'B': ['B']}
```

---

## 24. `KeyError` in template rendering

```python
template = "Hello {name}"

data = {}

try:
    print(template.format(**data))
except KeyError:
    print("Template variable missing")
```

---

## 25. When to handle vs prevent `KeyError`

| Scenario                   | Preferred approach |
| -------------------------- | ------------------ |
| External JSON / user input | `try–except`       |
| Internal fixed schema      | Bug → fix code     |
| Optional field             | `dict.get()`       |
| Required field             | Raise custom error |

---

## 26. Interview-level insight

> `KeyError` represents **schema uncertainty**.

Senior engineers:

* Handle it at system boundaries
* Convert it into domain language
* Avoid it in internal logic

---

## 27. Final takeaway

* `KeyError` is predictable and meaningful
* Handling strategy depends on context
* Transforming it cleanly shows production-level skill
