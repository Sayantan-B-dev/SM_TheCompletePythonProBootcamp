### QUIZ — Dictionaries, Lists, Nesting, Errors, Behavior

---

### Section 1: Basics (Concept + Behavior)

**Q1.**
What does this print?

```python
d = {"a": 1, "b": 2}
print(d["a"])
```

A. `"a"`
B. `1`
C. `KeyError`
D. `None`

**Answer:**
B

---

**Q2.**
What happens here?

```python
d = {}
d["x"] = 10
d["x"] = 20
print(d)
```

A. Error
B. `{'x': 10}`
C. `{'x': 20}`
D. Two values stored

**Answer:**
C

---

**Q3.**
Which of the following can be a dictionary key?

A. list
B. dict
C. tuple
D. set

**Answer:**
C

---

### Section 2: Errors & Safe Access

**Q4.**
What error occurs?

```python
d = {"a": 1}
print(d["b"])
```

**Answer:**
`KeyError`

---

**Q5.**
What does this print?

```python
d = {"a": 1}
print(d.get("b"))
```

**Answer:**
`None`

---

**Q6.**
What does this print?

```python
d = {"a": 1}
print(d.get("b", 0))
```

**Answer:**
`0`

---

### Section 3: Iteration & Output Behavior

**Q7.**
What does this loop print?

```python
d = {"x": 10, "y": 20}
for i in d:
    print(i)
```

A. values
B. keys
C. key-value pairs
D. error

**Answer:**
B

---

**Q8.**
What does this print?

```python
d = {"a": 1, "b": 2}
print(list(d.values()))
```

**Answer:**
`[1, 2]`

---

### Section 4: Nesting (List + Dictionary)

**Q9.**
What is the output?

```python
data = {
    "users": [
        {"name": "A"},
        {"name": "B"}
    ]
}
print(data["users"][1]["name"])
```

**Answer:**
`B`

---

**Q10.**
What error occurs?

```python
students = [{"name": "A"}]
print(students["name"])
```

**Answer:**
`TypeError: list indices must be integers or slices`

---

### Section 5: Mutability & Unexpected Behavior

**Q11.**
What is printed?

```python
d = {"nums": [1, 2]}
x = d["nums"]
x.append(3)
print(d)
```

**Answer:**
`{'nums': [1, 2, 3]}`

---

**Q12.**
Why did the dictionary change?

A. Dictionary copies values
B. List is immutable
C. Reference to same list
D. Python bug

**Answer:**
C

---

### Section 6: Copying & Safety

**Q13.**
What does this print?

```python
a = {"x": [1]}
b = a.copy()
b["x"].append(2)
print(a)
```

**Answer:**
`{'x': [1, 2]}`

---

**Q14.**
Which method prevents this shared mutation?

A. `a.copy()`
B. `list()`
C. `deepcopy()`
D. slicing

**Answer:**
C

---

### Section 7: Modification During Iteration

**Q15.**
What happens here?

```python
d = {"a": 1}
for k in d:
    d["b"] = 2
```

**Answer:**
`RuntimeError: dictionary changed size during iteration`

---

**Q16.**
Correct fix?

A. Use `.items()`
B. Use `list(d.keys())`
C. Use `.values()`
D. Use `.copy()`

**Answer:**
B

---

### Section 8: Truthiness & Comparison

**Q17.**
What does this print?

```python
print(bool({}))
print(bool({"a": 1}))
```

**Answer:**

```
False
True
```

---

**Q18.**
What does this print?

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)
```

**Answer:**
`True`

---

### Section 9: Logic & Mental Models

**Q19.**
Choose the correct access pattern:

Data: `users = [{"name": "A"}, {"name": "B"}]`

To access `"B"`:

A. `users["name"][1]`
B. `users[1]["name"]`
C. `users.name[1]`
D. `users.get(1)`

**Answer:**
B

---

**Q20.**
Best structure for API JSON data?

A. tuple
B. set
C. list only
D. nested dict + list

**Answer:**
D

---

### Final Score Guide

* **18–20** → solid understanding
* **14–17** → good, needs edge-case practice
* **10–13** → revise nesting & mutability
* **<10** → rework fundamentals before moving on
