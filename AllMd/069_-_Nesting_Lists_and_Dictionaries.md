### 1. What nesting means (core idea)

Nesting = placing one data structure **inside another**.

Possible combinations:

* list inside list
* dict inside dict
* list inside dict
* dict inside list
* deep combinations of all above

Why it exists:

* Real data is **hierarchical**, not flat
* Parent → child → sub-child relationships
* JSON, APIs, configs, DB documents all rely on nesting

---

### 2. List inside list (2D / matrix-like data)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[1])
print(matrix[1][2])
```

Output:

```
[4, 5, 6]
6
```

Use cases:

* grids (games, boards)
* tables
* matrices
* image pixels

Common error:

```python
print(matrix[3][0])
```

Error:

```
IndexError: list index out of range
```

Safe access:

```python
if 1 < len(matrix) and 2 < len(matrix[1]):
    print(matrix[1][2])
```

---

### 3. Dictionary inside dictionary (hierarchical data)

```python
user = {
    "id": 101,
    "profile": {
        "name": "A",
        "age": 22,
        "address": {
            "city": "Kolkata",
            "zip": 700001
        }
    }
}

print(user["profile"]["address"]["city"])
```

Output:

```
Kolkata
```

Real use cases:

* user profiles
* API responses
* configuration files
* permissions & roles

Common error:

```python
print(user["profile"]["address"]["country"])
```

Error:

```
KeyError: 'country'
```

Safe handling:

```python
country = user.get("profile", {}).get("address", {}).get("country", "NA")
print(country)
```

Output:

```
NA
```

---

### 4. List inside dictionary (most common real-world pattern)

```python
student = {
    "name": "A",
    "subjects": ["Math", "Physics", "CS"]
}

print(student["subjects"][1])
```

Output:

```
Physics
```

Use cases:

* skills
* tags
* categories
* followers / likes
* playlists

Unexpected behavior (mutable list):

```python
skills = student["subjects"]
skills.append("AI")

print(student)
```

Output:

```
{'name': 'A', 'subjects': ['Math', 'Physics', 'CS', 'AI']}
```

Reason:

* list reference is shared
* mutation affects original dictionary

Fix:

```python
skills = student["subjects"].copy()
skills.append("ML")
```

---

### 5. Dictionary inside list (records / objects)

```python
students = [
    {"name": "A", "age": 22},
    {"name": "B", "age": 23},
    {"name": "C", "age": 21}
]

print(students[1]["name"])
```

Output:

```
B
```

Use cases:

* database rows
* API results
* search results
* logs

Common error:

```python
print(students["name"])
```

Error:

```
TypeError: list indices must be integers or slices
```

Correct mental model:

* list → index
* dict → key

---

### 6. Deep nesting (real API-style data)

```python
response = {
    "status": 200,
    "data": {
        "users": [
            {
                "id": 1,
                "posts": [
                    {"title": "Hello", "likes": 10},
                    {"title": "World", "likes": 5}
                ]
            }
        ]
    }
}

print(response["data"]["users"][0]["posts"][1]["title"])
```

Output:

```
World
```

Debug trick:
Print step by step instead of one line.

---

### 7. Iterating over nested structures

```python
for user in response["data"]["users"]:
    for post in user["posts"]:
        print(post["title"], post["likes"])
```

Output:

```
Hello 10
World 5
```

Rule:

* each loop handles **one nesting level**

---

### 8. Common errors in nested structures

| Error          | Cause                       |
| -------------- | --------------------------- |
| KeyError       | missing dictionary key      |
| IndexError     | invalid list index          |
| TypeError      | mixing list/dict access     |
| AttributeError | calling dict method on list |

Example:

```python
 reduces = students.get("name")
```

Error:

```
AttributeError: 'list' object has no attribute 'get'
```

Fix:

* confirm data type before access

```python
if isinstance(students, list):
    print(students[0]["name"])
```

---

### 9. Defensive access pattern (important)

```python
def safe_get(data, keys, default=None):
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        elif isinstance(data, list) and isinstance(key, int):
            if key < len(data):
                data = data[key]
            else:
                return default
        else:
            return default
    return data
```

```python
print(safe_get(response, ["data", "users", 0, "posts", 0, "title"]))
```

Output:

```
Hello
```

---

### 10. Shallow vs deep copy (critical with nesting)

```python
import copy

a = {"x": [1, 2]}
b = a.copy()
b["x"].append(3)

print(a)
print(b)
```

Output:

```
{'x': [1, 2, 3]}
{'x': [1, 2, 3]}
```

Reason:

* `.copy()` is shallow

Deep copy:

```python
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

### 11. Modifying nested data during iteration (danger)

```python
d = {"a": [1, 2], "b": [3, 4]}

for k in d:
    d[k].append(0)

print(d)
```

Output:

```
{'a': [1, 2, 0], 'b': [3, 4, 0]}
```

Safe because:

* keys are not modified
* values are mutable but allowed

Unsafe:

```python
for k in d:
    d[k + "x"] = []
```

Error:

```
RuntimeError: dictionary changed size during iteration
```

Fix:

```python
for k in list(d.keys()):
    d[k + "x"] = []
```

---

### 12. When to use nesting vs classes

Use nested dict/list when:

* data is temporary
* structure is dynamic
* API / JSON handling
* configuration data

Avoid over-nesting when:

* logic becomes unreadable
* same structure repeated everywhere
* behavior (methods) is required

Rule of thumb:

* data-heavy → nested structures
* behavior-heavy → classes

---

### 13. Mental checklist while working with nesting

* Know current data type at every level
* Print intermediate values while debugging
* Never assume key/index exists
* Copy mutable objects before modifying
* Prefer readable multi-step access over one-liners
* Treat API data as untrusted

Nested lists and dictionaries are powerful, but they demand **discipline, defensive access, and clarity of structure**.
