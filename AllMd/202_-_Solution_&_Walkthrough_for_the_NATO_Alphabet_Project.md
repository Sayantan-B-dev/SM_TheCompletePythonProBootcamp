* **Think in pipelines, not lines of code**
  Example:
  `CSV → DataFrame → dict → list comprehension → output`
  Once you see data flowing step by step, debugging becomes trivial.

* **Read comprehensions right-to-left**

  ```python
  [row.name for _, row in df.iterrows() if row.score >= 40]
  ```

  Meaning: *from rows → filter → extract value*.

* **List = repetition, Dictionary = meaning**

  ```python
  names = ["Asha", "Ravi"]
  scores = {"Asha": 85, "Ravi": 35}
  ```

  Use lists for sequences, dicts for relationships.

* **Comprehension replaces boilerplate loops, not logic**
  Good:

  ```python
  squares = [x**2 for x in range(5)]
  ```

  Bad (too complex):

  ```python
  [x*y if x>2 else y-x for x in a for y in b if y%2==0]
  ```

* **Condition at the end = filtering**

  ```python
  [n for n in numbers if n % 2 == 0]
  ```

  Elements not passing the condition never exist in output.

* **Conditional expression = value decision, not filtering**

  ```python
  ["PASS" if s >= 40 else "FAIL" for s in scores]
  ```

  Output length stays the same.

* **Dictionary comprehension transforms relationships**

  ```python
  {name: score+5 for name, score in scores.items()}
  ```

  Keys stay meaningful, values change.

* **Filtering in dict comprehension removes entire key-value pairs**

  ```python
  {n: s for n, s in scores.items() if s >= 40}
  ```

  Failed students completely disappear.

* **Duplicate keys overwrite silently**

  ```python
  {score: name for name, score in scores.items()}
  ```

  Last duplicate wins — dangerous if unnoticed.

* **Strings are sequences too**

  ```python
  [ch for ch in "python" if ch in "aeiou"]
  ```

  Treat characters like list elements.

* **`iterrows()` gives index + Series**

  ```python
  for index, row in df.iterrows():
      print(row.name, row.score)
  ```

  Row behaves like a dictionary.

* **`row.column` works only with clean column names**
  Good: `row.score`
  Bad: `row.total score`

* **Use comprehension with pandas iteration for extraction, not mutation**

  ```python
  passed = [row.name for _, row in df.iterrows() if row.score >= 40]
  ```

  Avoid modifying DataFrame row-by-row.

* **Prefer `itertuples()` when iterating seriously**

  ```python
  [row.name for row in df.itertuples() if row.score >= 40]
  ```

  Faster, safer, cleaner.

* **Always normalize input before lookup**

  ```python
  user_input = input().upper()
  ```

  Prevents `KeyError` due to casing.

* **`try/except` is for protection, not control flow**

  ```python
  try:
      code = nato_dict[letter]
  except KeyError:
      print("Invalid input")
  ```

  Guard against unpredictable user data.

* **Build lookup dictionaries early**

  ```python
  nato = {row.letter: row.code for _, row in df.iterrows()}
  ```

  One-time cost → constant-time access forever.

* **Vectorized pandas operations beat loops**

  ```python
  df["status"] = df["score"].apply(lambda x: "PASS" if x >= 40 else "FAIL")
  ```

  Loops are for learning, vectors are for production.

* **If code is hard to read, it’s probably wrong**
  Rule: if you can’t explain a comprehension in one sentence, rewrite it as a loop.

* **Final mental shortcut**

  ```text
  List comprehension  → values
  Dict comprehension  → relationships
  Pandas iteration    → inspection
  Pandas vectors      → real work
  ```


## Python Interview Quizzes — Topics Covered So Far

*(lists, dictionaries, comprehensions, sequences, pandas iteration, file data, error handling)*

---

### SECTION 1 — Lists & Sequences

**Q1. What will this print?**

```python
data = "python"
print(list(data))
```

**Answer**

```text
['p', 'y', 't', 'h', 'o', 'n']
```

**Why**
Strings are sequences; iterating yields characters.

---

**Q2. Difference between list and tuple in one practical line?**
**Answer**

```text
List = mutable sequence, Tuple = immutable sequence
```

Example:

```python
lst = [1, 2]
lst.append(3)     # works

tpl = (1, 2)
tpl.append(3)     # error
```

---

**Q3. What does slicing return?**

```python
nums = [10, 20, 30, 40]
print(nums[1:3])
```

**Answer**

```text
[20, 30]
```

**Why**
Start index inclusive, end index exclusive.

---

**Q4. Time complexity of searching in list vs dict?**
**Answer**

```text
List search: O(n)
Dict lookup: O(1) average
```

---

### SECTION 2 — List Comprehension

**Q5. Convert this loop to comprehension**

```python
result = []
for x in range(1, 6):
    result.append(x * 2)
```

**Answer**

```python
result = [x * 2 for x in range(1, 6)]
```

---

**Q6. Output?**

```python
[n for n in range(10) if n % 3 == 0]
```

**Answer**

```text
[0, 3, 6, 9]
```

---

**Q7. Filtering vs conditional value — identify**

```python
["PASS" if s >= 40 else "FAIL" for s in [35, 50]]
```

**Answer**

```text
Conditional value, not filtering
```

Output:

```text
['FAIL', 'PASS']
```

---

**Q8. Output?**

```python
[x for x in range(5) if x]
```

**Answer**

```text
[1, 2, 3, 4]
```

**Why**
`0` is falsy, others are truthy.

---

**Q9. What is wrong here?**

```python
[x*y for x in a for y in b if x>2 else y]
```

**Answer**

```text
Invalid syntax: conditional expression placed incorrectly
```

---

### SECTION 3 — Dictionary & Dictionary Comprehension

**Q10. Output?**

```python
scores = {"A": 80, "B": 40}
print({k: v+5 for k, v in scores.items()})
```

**Answer**

```text
{'A': 85, 'B': 45}
```

---

**Q11. What happens here?**

```python
{name[0]: name for name in ["Asha", "Amit"]}
```

**Answer**

```text
{'A': 'Amit'}
```

**Why**
Duplicate keys overwrite silently.

---

**Q12. Filter passed students**

```python
scores = {"Asha": 85, "Ravi": 35}
```

**Answer**

```python
{k: v for k, v in scores.items() if v >= 40}
```

---

**Q13. Output?**

```python
{k: v >= 40 for k, v in scores.items()}
```

**Answer**

```text
{'Asha': True, 'Ravi': False}
```

**Why**
Values converted to booleans.

---

### SECTION 4 — Nested & Advanced Comprehension

**Q14. Output?**

```python
[(x, y) for x in [1, 2] for y in [3, 4]]
```

**Answer**

```text
[(1, 3), (1, 4), (2, 3), (2, 4)]
```

---

**Q15. Flatten result**

```python
matrix = [[1, 2], [3, 4]]
```

**Answer**

```python
[num for row in matrix for num in row]
```

---

**Q16. Output?**

```python
[x for x in range(5) for y in range(2)]
```

**Answer**

```text
[0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
```

**Why**
Inner loop doesn’t affect output variable.

---

### SECTION 5 — Files & Data Fetching

**Q17. Why use `.strip()` when reading files?**
**Answer**

```text
To remove newline and whitespace characters
```

---

**Q18. Output?**

```python
with open("file.txt") as f:
    print(type(f.readlines()))
```

**Answer**

```text
<class 'list'>
```

---

**Q19. Best structure after reading CSV for fast lookup?**
**Answer**

```text
Dictionary
```

Example:

```python
{name: score for name, score in zip(names, scores)}
```

---

### SECTION 6 — Pandas (`iterrows`, `itertuples`)

**Q20. What does `iterrows()` return?**
**Answer**

```text
(index, Series)
```

---

**Q21. Output?**

```python
for _, row in df.iterrows():
    print(type(row))
```

**Answer**

```text
pandas.core.series.Series
```

---

**Q22. Why is `iterrows()` slow?**
**Answer**

```text
Row-wise Python iteration + object conversion
```

---

**Q23. Better alternative for row iteration?**
**Answer**

```python
df.itertuples()
```

---

**Q24. Access column safely**

```python
row["total_score"]    # safe
row.total_score       # works only if name is valid
```

---

### SECTION 7 — Error Handling

**Q25. What error does this raise?**

```python
d = {"A": 1}
print(d["B"])
```

**Answer**

```text
KeyError
```

---

**Q26. Why use try/except instead of `if key in dict`?**
**Answer**

```text
Easier control flow when multiple lookups are involved
```

---

### SECTION 8 — Mixed Real-World Logic

**Q27. Convert user input to safe lookup**

```python
input().upper()
```

**Why**

```text
Prevents KeyError due to casing mismatch
```

---

**Q28. Output?**

```python
[ch for ch in "data science" if ch != " "]
```

**Answer**

```text
['d','a','t','a','s','c','i','e','n','c','e']
```

---

**Q29. When NOT to use comprehension?**
**Answer**

```text
When logic becomes unreadable or debug-heavy
```

---

**Q30. One-line interview summary**

```text
List → sequence of values  
Dict → meaning & lookup  
Comprehension → transformation  
Pandas loops → learning  
Pandas vectors → production
```
