## Errors commonly faced while working with **dictionaries**

including **recursive handling**, **loops**, **if–else**, **comprehensions**, and **creative real-world situations**

---

## 1. Core dictionary-related errors (overview)

| Error            | Why it happens                       |
| ---------------- | ------------------------------------ |
| `KeyError`       | Accessing missing key                |
| `TypeError`      | Using unhashable key or wrong type   |
| `AttributeError` | Calling dict methods on non-dict     |
| `ValueError`     | Invalid value conversion             |
| `RuntimeError`   | Modifying dict during iteration      |
| `RecursionError` | Infinite recursion on nested dict    |
| `IndexError`     | Mixing list logic inside dict values |
| `NameError`      | Wrong variable reference in loops    |

---

## 2. `KeyError` in deeply nested dictionaries (classic JSON issue)

```python
data = {
    "user": {
        "profile": {
            "name": "Alice"
        }
    }
}

try:
    print(data["user"]["profile"]["email"])
except KeyError:
    print("Missing nested key")
```

**Output**

```
Missing nested key
```

---

## 3. Recursive-safe dictionary access (professional pattern)

```python
def safe_get(data, keys):
    """
    Recursively traverse nested dictionaries safely.
    keys: list of keys to traverse in order
    """
    try:
        if not keys:
            return data
        return safe_get(data[keys[0]], keys[1:])
    except (KeyError, TypeError):
        return None

print(safe_get(data, ["user", "profile", "email"]))
```

**Output**

```
None
```

---

## 4. Infinite recursion on malformed data (dangerous)

```python
data = {}
data["self"] = data

def recurse(d):
    return recurse(d["self"])

try:
    recurse(data)
except RecursionError:
    print("Infinite recursion detected")
```

**Output**

```
Infinite recursion detected
```

---

## 5. `TypeError`: unhashable dictionary keys

```python
bad_dict = {}

try:
    bad_dict[["a", "b"]] = 10
except TypeError:
    print("Lists cannot be dictionary keys")
```

---

## 6. `TypeError`: assuming dict but receiving list

```python
data = ["a", "b", "c"]

try:
    print(data["key"])
except TypeError:
    print("Expected dictionary, got list")
```

---

## 7. `RuntimeError`: modifying dictionary during iteration

```python
data = {"a": 1, "b": 2}

try:
    for k in data:
        del data[k]
except RuntimeError:
    print("Cannot modify dictionary while iterating")
```

---

## 8. Correct way to handle modification during iteration

```python
data = {"a": 1, "b": 2}

for k in list(data.keys()):
    del data[k]

print(data)
```

**Output**

```
{}
```

---

## 9. `KeyError` inside dictionary comprehension

```python
scores = {"Alice": 90, "Bob": 80}
names = ["Alice", "Charlie"]

try:
    result = {n: scores[n] for n in names}
except KeyError:
    print("Comprehension failed due to missing key")
```

---

## 10. Safe comprehension with conditional guard

```python
result = {n: scores[n] for n in names if n in scores}
print(result)
```

**Output**

```
{'Alice': 90}
```

---

## 11. `KeyError` in list comprehension accessing dict

```python
data = {"a": 1, "b": 2}

try:
    values = [data[k] for k in ["a", "c"]]
except KeyError:
    print("List comprehension key missing")
```

---

## 12. Handling missing keys inside loop (granular control)

```python
values = []
for k in ["a", "c"]:
    try:
        values.append(data[k])
    except KeyError:
        values.append(0)

print(values)
```

**Output**

```
[1, 0]
```

---

## 13. `AttributeError`: treating dict as object

```python
config = {"debug": True}

try:
    print(config.debug)
except AttributeError:
    print("Dictionaries do not support dot access")
```

---

## 14. `ValueError`: converting dictionary values

```python
data = {"age": "twenty"}

try:
    age = int(data["age"])
except ValueError:
    print("Age must be numeric")
```

---

## 15. `KeyError` in grouping logic (very common)

```python
groups = {}

names = ["A", "B", "A"]

try:
    for n in names:
        groups[n].append(n)
except KeyError:
    print("Group not initialized")
```

---

## 16. Correct grouping using try–except (pattern)

```python
groups = {}

for n in names:
    try:
        groups[n].append(n)
    except KeyError:
        groups[n] = [n]

print(groups)
```

**Output**

```
{'A': ['A', 'A'], 'B': ['B']}
```

---

## 17. Dictionary of lists causing `IndexError`

```python
data = {"scores": []}

try:
    print(data["scores"][0])
except IndexError:
    print("List inside dictionary is empty")
```

---

## 18. Recursive traversal of mixed list + dict structures

```python
def find_key(structure, target):
    """
    Recursively search for a key in nested dict/list structures.
    """
    try:
        if isinstance(structure, dict):
            if target in structure:
                return structure[target]
            for v in structure.values():
                result = find_key(v, target)
                if result is not None:
                    return result
        elif isinstance(structure, list):
            for item in structure:
                result = find_key(item, target)
                if result is not None:
                    return result
    except RecursionError:
        return None

nested = {"a": [{"b": {"c": 5}}]}
print(find_key(nested, "c"))
```

**Output**

```
5
```

---

## 19. `KeyError` in configuration loading (industrial)

```python
config = {"host": "localhost"}

try:
    port = config["port"]
except KeyError:
    port = 5432

print(port)
```

**Output**

```
5432
```

---

## 20. Schema validation using dictionary iteration

```python
required = ["id", "name", "email"]
payload = {"id": 1, "name": "Alice"}

try:
    for field in required:
        if field not in payload:
            raise KeyError(field)
except KeyError as e:
    print("Missing required field:", e)
```

---

## 21. Recursion used to normalize dictionary safely

```python
def normalize(data):
    """
    Recursively convert all values to strings.
    """
    try:
        if isinstance(data, dict):
            return {k: normalize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [normalize(v) for v in data]
        else:
            return str(data)
    except RecursionError:
        return None

print(normalize({"a": [1, 2, {"b": 3}]}))
```

**Output**

```
{'a': ['1', '2', {'b': '3'}]}
```

---

## 22. `NameError` due to shadowing in dict loops

```python
data = {"a": 1}

try:
    for key in data:
        print(value)
except NameError:
    print("Variable referenced before assignment")
```

---

## 23. Defensive dictionary access strategy (summary table)

| Situation        | Best approach               |
| ---------------- | --------------------------- |
| Unknown schema   | `try–except`                |
| Optional key     | `dict.get()`                |
| Required key     | Raise custom error          |
| Nested structure | Recursive safe access       |
| Comprehension    | Guard with `if key in dict` |
| Mutation         | Iterate over copy           |

---

## 24. Senior-level mental model

> Dictionary errors are not bugs — they are **schema mismatches**.

Strong engineers:

* Expect missing keys
* Validate structure early
* Use recursion cautiously
* Never assume shape without proof
