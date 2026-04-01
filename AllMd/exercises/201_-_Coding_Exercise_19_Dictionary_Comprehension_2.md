## Dictionary Comprehension — **Difficulty Level 2 (Advanced Composition & Real-World Modeling)**

*Scope: multiple conditions, conditional values, multiple iterables (`zip`, `enumerate`), restructuring data, light nesting logic (but still readable).*

---

## Core Patterns (Level 2)

```text
{key_expr: value_expr for k, v in dict.items() if condition}

{key_expr: value_expr if condition else other_value for k, v in dict.items()}

{key_expr: value_expr for a, b in zip(seq1, seq2)}

{key_expr: value_expr for index, item in enumerate(seq)}
```

Mental rule:

> **Condition at the end decides inclusion**
> **Conditional expression decides meaning**

---

## Example 1 — Student Grades with Classification

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92,
    "Amit": 67
}

grades = {
    name: "DISTINCTION" if score >= 75 else "PASS"
    for name, score in scores.items()
    if score >= 40
}

print(grades)
```

```text
{'Asha': 'DISTINCTION', 'Neha': 'DISTINCTION', 'Amit': 'PASS'}
```

**Explanation**

* First filter removes failures
* Second condition classifies remaining students
* Two logical layers working together

---

## Example 2 — Normalize Scores to Percentage (With Validation)

```python
raw_scores = {
    "Asha": 425,
    "Ravi": -10,
    "Neha": 460,
    "Amit": 390
}

percentages = {
    name: round((score / 500) * 100, 2)
    for name, score in raw_scores.items()
    if 0 <= score <= 500
}

print(percentages)
```

```text
{'Asha': 85.0, 'Neha': 92.0, 'Amit': 78.0}
```

**Explanation**

* Invalid data filtered
* Mathematical transformation applied
* Safe grading pipeline

---

## Example 3 — Invert Dictionary with Condition

```python
employees = {
    "Asha": "HR",
    "Ravi": "IT",
    "Neha": "IT",
    "Amit": "Sales"
}

it_only = {
    dept: name
    for name, dept in employees.items()
    if dept == "IT"
}

print(it_only)
```

```text
{'IT': 'Neha'}
```

**Explanation**

* Key inversion
* Overwriting happens due to duplicate values
* Important real-world caveat

---

## Example 4 — Attendance Status from Two Lists

```python
students = ["Asha", "Ravi", "Neha"]
attendance = [True, False, True]

status = {
    student: "PRESENT" if present else "ABSENT"
    for student, present in zip(students, attendance)
}

print(status)
```

```text
{'Asha': 'PRESENT', 'Ravi': 'ABSENT', 'Neha': 'PRESENT'}
```

**Explanation**

* `zip()` merges parallel data sources
* Conditional value assigns meaning

---

## Example 5 — Index → Value Mapping with Filtering

```python
values = [10, 25, 40, 55, 70]

indexed_even = {
    index: value
    for index, value in enumerate(values)
    if value % 2 == 0
}

print(indexed_even)
```

```text
{0: 10, 2: 40, 4: 70}
```

**Explanation**

* Index preserved
* Only even values included
* Useful for sparse lookups

---

## Example 6 — Categorize Prices (Business Logic)

```python
prices = {
    "pen": 10,
    "book": 250,
    "bag": 1200,
    "laptop": 50000
}

categories = {
    item: "EXPENSIVE" if price > 1000 else "AFFORDABLE"
    for item, price in prices.items()
}

print(categories)
```

```text
{'pen': 'AFFORDABLE', 'book': 'AFFORDABLE', 'bag': 'EXPENSIVE', 'laptop': 'EXPENSIVE'}
```

**Explanation**

* No filtering
* Every item classified
* Typical inventory tagging

---

## Example 7 — Merge Two Lists into Computed Dictionary

```python
products = ["pen", "book", "bag"]
prices = [10, 250, 1200]

price_with_tax = {
    product: round(price * 1.18, 2)
    for product, price in zip(products, prices)
}

print(price_with_tax)
```

```text
{'pen': 11.8, 'book': 295.0, 'bag': 1416.0}
```

**Explanation**

* Parallel iteration
* Derived values
* Real invoice-style computation

---

## Example 8 — Filter + Transform Keys

```python
users = {
    "asha_k": True,
    "ravi_p": False,
    "neha_s": True
}

active_users = {
    username.upper(): "ACTIVE"
    for username, is_active in users.items()
    if is_active
}

print(active_users)
```

```text
{'ASHA_K': 'ACTIVE', 'NEHA_S': 'ACTIVE'}
```

**Explanation**

* Condition controls existence
* Key transformed
* Value standardized

---

## Example 9 — Bucket Scores into Ranges

```python
scores = {
    "Asha": 85,
    "Ravi": 35,
    "Neha": 92,
    "Amit": 67
}

buckets = {
    name: "HIGH" if score >= 80 else "MEDIUM" if score >= 50 else "LOW"
    for name, score in scores.items()
}

print(buckets)
```

```text
{'Asha': 'HIGH', 'Ravi': 'LOW', 'Neha': 'HIGH', 'Amit': 'MEDIUM'}
```

**Explanation**

* Chained conditional expression
* Multi-class classification
* Common in analytics

---

## Example 10 — Extract and Restructure Nested Data

```python
users = [
    {"name": "Asha", "active": True},
    {"name": "Ravi", "active": False},
    {"name": "Neha", "active": True}
]

active_lookup = {
    user["name"]: user["active"]
    for user in users
    if user["active"]
}

print(active_lookup)
```

```text
{'Asha': True, 'Neha': True}
```

**Explanation**

* Source is a list of dictionaries
* Filter + key extraction
* Real API-style data handling

---

## Example 11 — Boolean Flags from Numeric Conditions

```python
inventory = {
    "pen": 100,
    "book": 0,
    "bag": 5
}

in_stock = {
    item: quantity > 0
    for item, quantity in inventory.items()
}

print(in_stock)
```

```text
{'pen': True, 'book': False, 'bag': True}
```

**Explanation**

* Values converted to flags
* Used in validation logic

---

## Example 12 — Compute Discounts Conditionally

```python
prices = {
    "pen": 10,
    "bag": 1200,
    "laptop": 50000
}

discounted = {
    item: price * 0.9 if price > 1000 else price
    for item, price in prices.items()
}

print(discounted)
```

```text
{'pen': 10, 'bag': 1080.0, 'laptop': 45000.0}
```

**Explanation**

* Conditional value logic
* Selective business rules
