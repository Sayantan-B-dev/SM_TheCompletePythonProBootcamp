## Pandas Data Iteration — Core Mental Model

In **pandas**, data is stored mainly in a **DataFrame** (table-like) and **Series** (column-like).

> A **DataFrame row** is conceptually similar to a dictionary
> A **DataFrame column** is conceptually similar to a list / series

When you iterate over rows, pandas gives you:

* an **index**
* a **row object** (a `Series`)

---

## Sample DataFrame (Used Everywhere Below)

```python
import pandas as pd

data = {
    "name": ["Asha", "Ravi", "Neha"],
    "score": [85, 35, 92],
    "age": [21, 22, 20]
}

df = pd.DataFrame(data)

print(df)
```

### Output

```text
    name  score  age
0   Asha     85   21
1   Ravi     35   22
2   Neha     92   20
```

---

## `iterrows()` — What It Actually Does

### Syntax

```text
for index, row in df.iterrows():
    ...
```

* `index` → row label (usually 0, 1, 2…)
* `row` → a **Series** representing the row

---

## Example 1 — Basic Iteration

```python
for index, row in df.iterrows():
    print(index, row)
```

### Output

```text
0 name     Asha
  score      85
  age        21
Name: 0, dtype: object
1 name     Ravi
  score      35
  age        22
Name: 1, dtype: object
2 name     Neha
  score      92
  age        20
Name: 2, dtype: object
```

**Explanation**

* Each `row` is a `Series`
* Column names become labels
* Values can be accessed like dictionary entries

---

## Accessing Row Values — Three Ways

### 1. Dictionary-style (Most Explicit)

```python
for _, row in df.iterrows():
    print(row["name"], row["score"])
```

### Output

```text
Asha 85
Ravi 35
Neha 92
```

---

### 2. Attribute-style (`row.column_name`)

```python
for _, row in df.iterrows():
    print(row.name, row.score)
```

### Output

```text
Asha 85
Ravi 35
Neha 92
```

**Important Rule**

* Works only if column names are valid Python identifiers
* Avoid spaces and special characters in column names

---

### 3. Index-based (Least Recommended)

```python
for _, row in df.iterrows():
    print(row[0], row[1])
```

**Why avoid**

* Breaks if column order changes
* Hard to read

---

## Example 2 — Filtering Rows with Logic

### Task

Extract students who passed (score ≥ 40)

```python
passed_students = []

for _, row in df.iterrows():
    if row.score >= 40:
        passed_students.append(row.name)

print(passed_students)
```

### Output

```text
['Asha', 'Neha']
```

---

## Same Logic Using List Comprehension (Recommended)

```python
passed_students = [
    row.name
    for _, row in df.iterrows()
    if row.score >= 40
]

print(passed_students)
```

### Output

```text
['Asha', 'Neha']
```

---

## Example 3 — Create a Dictionary from DataFrame Rows

### Name → Score Mapping

```python
score_map = {
    row.name: row.score
    for _, row in df.iterrows()
}

print(score_map)
```

### Output

```text
{'Asha': 85, 'Ravi': 35, 'Neha': 92}
```

---

## Example 4 — Conditional Dictionary Comprehension

### Only Passed Students

```python
passed_score_map = {
    row.name: row.score
    for _, row in df.iterrows()
    if row.score >= 40
}

print(passed_score_map)
```

### Output

```text
{'Asha': 85, 'Neha': 92}
```

---

## Example 5 — Label Rows (PASS / FAIL)

```python
result_map = {
    row.name: "PASS" if row.score >= 40 else "FAIL"
    for _, row in df.iterrows()
}

print(result_map)
```

### Output

```text
{'Asha': 'PASS', 'Ravi': 'FAIL', 'Neha': 'PASS'}
```

---

## Example 6 — Build a New Column Using Iteration (Not Optimal, But Educational)

```python
status = []

for _, row in df.iterrows():
    status.append("PASS" if row.score >= 40 else "FAIL")

df["status"] = status

print(df)
```

### Output

```text
    name  score  age status
0   Asha     85   21   PASS
1   Ravi     35   22   FAIL
2   Neha     92   20   PASS
```

---

## Pandas Way (Vectorized, Better Than Iteration)

```python
df["status"] = df["score"].apply(lambda s: "PASS" if s >= 40 else "FAIL")

print(df)
```

### Output

```text
    name  score  age status
0   Asha     85   21   PASS
1   Ravi     35   22   FAIL
2   Neha     92   20   PASS
```

---

## Why `iterrows()` Is Often Discouraged

| Reason         | Explanation                   |
| -------------- | ----------------------------- |
| Slow           | Python-level loop             |
| Type casting   | Row values may become objects |
| Not vectorized | Ignores pandas’ strength      |

---

## Better Alternatives (Conceptual Overview)

| Method         | Use Case             |
| -------------- | -------------------- |
| `iterrows()`   | Learning, debugging  |
| `itertuples()` | Faster row iteration |
| Column ops     | Best performance     |
| `apply()`      | Row/column logic     |

---

## Example 7 — `itertuples()` (Faster, Cleaner)

```python
for row in df.itertuples():
    print(row.name, row.score)
```

### Output

```text
Asha 85
Ravi 35
Neha 92
```

**Why better**

* Faster
* Attribute access
* Strong typing

---

## Comprehension with `itertuples()`

```python
passed = [row.name for row in df.itertuples() if row.score >= 40]

print(passed)
```

### Output

```text
['Asha', 'Neha']
```

---

## Mental Model (Anchor This)

```text
DataFrame
 ├─ iterrows()   → index + Series (flexible, slow)
 ├─ itertuples() → named tuples (fast, safe)
 ├─ column ops   → vectorized (best)
```
