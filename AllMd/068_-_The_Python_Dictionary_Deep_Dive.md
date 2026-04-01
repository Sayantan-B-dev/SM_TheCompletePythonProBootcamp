### 1. Dictionary fundamentals (internal behavior)

A dictionary is a **hash table**.

* Keys are passed through a hash function.
* Hash → index → value stored.
* Lookup, insert, delete ≈ **O(1)** average time.

Key rules:

* Keys → **immutable + hashable**
* Values → **any data type**
* Order → **insertion-ordered (Python 3.7+)**

```python
d = {"a": 1, "b": 2, "c": 3}
print(d)
```

Output:

```
{'a': 1, 'b': 2, 'c': 3}
```

---

### 2. Valid vs invalid key data types

| Data Type                  | Allowed as Key | Reason    |
| -------------------------- | -------------- | --------- |
| str                        | ✅              | immutable |
| int                        | ✅              | immutable |
| float                      | ✅              | immutable |
| tuple (immutable contents) | ✅              | hashable  |
| list                       | ❌              | mutable   |
| dict                       | ❌              | mutable   |
| set                        | ❌              | mutable   |

```python
valid = {(1, 2): "tuple key"}
print(valid)
```

Output:

```
{(1, 2): 'tuple key'}
```

```python
invalid = {[1, 2]: "list key"}
```

Error:

```
TypeError: unhashable type: 'list'
```

---

### 3. Accessing values and KeyError

```python
student = {"name": "A", "age": 22}
print(student["name"])
```

Output:

```
A
```

```python
print(student["city"])
```

Error:

```
KeyError: 'city'
```

Safe access using `.get()`:

```python
print(student.get("city"))
print(student.get("city", "Not Found"))
```

Output:

```
None
Not Found
```

---

### 4. Updating vs inserting (same syntax, different behavior)

```python
data = {"x": 10}
data["x"] = 20     # update
data["y"] = 30     # insert
print(data)
```

Output:

```
{'x': 20, 'y': 30}
```

No error is thrown. Dictionary decides based on key existence.

---

### 5. Deleting keys and related errors

```python
d = {"a": 1, "b": 2}
del d["a"]
print(d)
```

Output:

```
{'b': 2}
```

```python
del d["c"]
```

Error:

```
KeyError: 'c'
```

Safe deletion:

```python
d.pop("c", None)
print(d)
```

Output:

```
{'b': 2}
```

---

### 6. Dictionary methods and behaviors

| Method   | Behavior                   |
| -------- | -------------------------- |
| keys()   | returns view of keys       |
| values() | returns view of values     |
| items()  | returns (key, value) pairs |
| clear()  | empties dictionary         |
| copy()   | shallow copy               |

```python
d = {"a": 1, "b": 2}

print(d.keys())
print(d.values())
print(d.items())
```

Output:

```
dict_keys(['a', 'b'])
dict_values([1, 2])
dict_items([('a', 1), ('b', 2)])
```

---

### 7. Iteration patterns (critical for logic)

```python
for key in d:
    print(key)
```

Output:

```
a
b
```

```python
for value in d.values():
    print(value)
```

Output:

```
1
2
```

```python
for key, value in d.items():
    print(key, value)
```

Output:

```
a 1
b 2
```

---

### 8. Dictionary with mixed data types

```python
profile = {
    "name": "A",
    "age": 22,
    "skills": ["Python", "JS"],
    "address": {
        "city": "Kolkata",
        "zip": 700001
    }
}

print(profile["address"]["city"])
```

Output:

```
Kolkata
```

Common error:

```python
print(profile["address"]["country"])
```

Error:

```
KeyError: 'country'
```

---

### 9. Mutable values side effects

```python
d = {"nums": [1, 2]}
x = d["nums"]
x.append(3)

print(d)
```

Output:

```
{'nums': [1, 2, 3]}
```

Explanation:

* Value reference is shared
* Mutating value mutates dictionary

---

### 10. Shallow copy vs reference assignment

```python
a = {"x": [1, 2]}
b = a
b["x"].append(3)

print(a)
```

Output:

```
{'x': [1, 2, 3]}
```

```python
import copy
c = copy.deepcopy(a)
c["x"].append(4)

print(a)
print(c)
```

Output:

```
{'x': [1, 2, 3]}
{'x': [1, 2, 3, 4]}
```

---

### 11. Dictionary comparison behavior

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}

print(d1 == d2)
```

Output:

```
True
```

Order does not matter for equality.

---

### 12. Using dictionaries as counters

```python
text = "banana"
count = {}

for ch in text:
    count[ch] = count.get(ch, 0) + 1

print(count)
```

Output:

```
{'b': 1, 'a': 3, 'n': 2}
```

---

### 13. Common dictionary errors summary

| Error                  | Cause                           |
| ---------------------- | ------------------------------- |
| KeyError               | Accessing missing key           |
| TypeError (unhashable) | Mutable key                     |
| AttributeError         | Calling dict method on non-dict |
| RuntimeError           | Modifying dict during iteration |

Example:

```python
d = {"a": 1, "b": 2}
for k in d:
    d[k + "x"] = 0
```

Error:

```
RuntimeError: dictionary changed size during iteration
```

Correct approach:

```python
for k in list(d.keys()):
    d[k + "x"] = 0

print(d)
```

Output:

```
{'a': 1, 'b': 2, 'ax': 0, 'bx': 0}
```

---

### 14. Dictionary unpacking and merging

```python
a = {"x": 1}
b = {"y": 2}
c = {**a, **b}
print(c)
```

Output:

```
{'x': 1, 'y': 2}
```

Conflict resolution:

```python
a = {"x": 1}
b = {"x": 99}
print({**a, **b})
```

Output:

```
{'x': 99}
```

---

### 15. Truthiness behavior

```python
print(bool({}))
print(bool({"a": 1}))
```

Output:

```
False
True
```

Empty dictionary → False
Non-empty dictionary → True
