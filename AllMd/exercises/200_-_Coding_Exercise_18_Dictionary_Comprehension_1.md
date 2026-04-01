## Dictionary Comprehension — **Difficulty Level 1 (Foundation Control)**

*Scope: one iterable, no nesting, simple transformation, optional simple condition. Goal is clarity, not cleverness.*

---

## Core Equations (Level 1)

```text
new_dict = {new_key: new_value for item in iterable}
new_dict = {key: new_value for key, value in dict.items()}
new_dict = {key: value for key, value in dict.items() if condition}
```

Read **right → left**:

> Take data → optionally filter → compute key → compute value → store pair

---

## Example 1 — Square Numbers as Values

```python
numbers = [1, 2, 3, 4]

result = {n: n**2 for n in numbers}

print(result)
```

```text
{1: 1, 2: 4, 3: 9, 4: 16}
```

**Explanation**

* List is the source
* Each number becomes a key
* Value is a derived computation

---

## Example 2 — Word → Length Mapping

```python
words = ["data", "science", "python"]

length_map = {word: len(word) for word in words}

print(length_map)
```

```text
{'data': 4, 'science': 7, 'python': 6}
```

**Explanation**

* Semantic keys preserved
* Values represent a measurable property

---

## Example 3 — Student → Score Dictionary from Two Lists

```python
students = ["Asha", "Ravi", "Neha"]
scores = [85, 35, 92]

result = {student: score for student, score in zip(students, scores)}

print(result)
```

```text
{'Asha': 85, 'Ravi': 35, 'Neha': 92}
```

**Explanation**

* `zip()` pairs corresponding elements
* Clean replacement for index-based loops

---

## Example 4 — Increase All Scores by Bonus

```python
scores = {"Asha": 80, "Ravi": 60, "Neha": 90}

updated = {name: score + 5 for name, score in scores.items()}

print(updated)
```

```text
{'Asha': 85, 'Ravi': 65, 'Neha': 95}
```

**Explanation**

* Keys remain unchanged
* Values transformed uniformly

---

## Example 5 — Filter Passed Students Only

```python
scores = {"Asha": 85, "Ravi": 35, "Neha": 92}

passed = {name: score for name, score in scores.items() if score >= 40}

print(passed)
```

```text
{'Asha': 85, 'Neha': 92}
```

**Explanation**

* Condition controls existence
* Failures removed completely

---

## Example 6 — Label Students as PASS / FAIL

```python
scores = {"Asha": 85, "Ravi": 35, "Neha": 92}

status = {
    name: "PASS" if score >= 40 else "FAIL"
    for name, score in scores.items()
}

print(status)
```

```text
{'Asha': 'PASS', 'Ravi': 'FAIL', 'Neha': 'PASS'}
```

**Explanation**

* No filtering
* All keys retained
* Value determined conditionally

---

## Example 7 — Filter + Label Together

```python
scores = {"Asha": 85, "Ravi": 35, "Neha": 92, "Amit": 28}

qualified = {
    name: "QUALIFIED"
    for name, score in scores.items()
    if score >= 40
}

print(qualified)
```

```text
{'Asha': 'QUALIFIED', 'Neha': 'QUALIFIED'}
```

**Explanation**

* Filter removes failures
* Remaining keys mapped to constant value

---

## Example 8 — Character → ASCII Value

```python
letters = ["a", "b", "c"]

ascii_map = {ch: ord(ch) for ch in letters}

print(ascii_map)
```

```text
{'a': 97, 'b': 98, 'c': 99}
```

**Explanation**

* Keys are characters
* Values derived via built-in function

---

## Example 9 — Convert Prices to Taxed Prices

```python
prices = {"pen": 10, "book": 50, "bag": 500}

taxed = {item: price * 1.18 for item, price in prices.items()}

print(taxed)
```

```text
{'pen': 11.8, 'book': 59.0, 'bag': 590.0}
```

**Explanation**

* Financial transformation
* Original prices untouched

---

## Example 10 — Index Items Using Enumerate

```python
items = ["apple", "banana", "cherry"]

indexed = {index: item for index, item in enumerate(items)}

print(indexed)
```

```text
{0: 'apple', 1: 'banana', 2: 'cherry'}
```

**Explanation**

* Index becomes key
* Useful for lookups instead of lists

---

## Example 11 — Uppercase All Keys

```python
names = {"asha": 1, "ravi": 2}

upper_keys = {name.upper(): value for name, value in names.items()}

print(upper_keys)
```

```text
{'ASHA': 1, 'RAVI': 2}
```

**Explanation**

* Keys transformed
* Values preserved

---

## Example 12 — Length of Each Sentence

```python
sentences = ["hello world", "python is powerful"]

lengths = {s: len(s) for s in sentences}

print(lengths)
```

```text
{'hello world': 11, 'python is powerful': 18}
```

**Explanation**

* Entire string used as key
* Value is computed metric

---

## Example 13 — Filter Expensive Products

```python
products = {"pen": 10, "laptop": 50000, "phone": 20000}

expensive = {item: price for item, price in products.items() if price > 10000}

print(expensive)
```

```text
{'laptop': 50000, 'phone': 20000}
```

**Explanation**

* Threshold-based filtering
* Common in business logic

---

## Example 14 — Boolean Flag Mapping

```python
scores = {"Asha": 85, "Ravi": 35, "Neha": 92}

is_pass = {name: score >= 40 for name, score in scores.items()}

print(is_pass)
```

```text
{'Asha': True, 'Ravi': False, 'Neha': True}
```

**Explanation**

* Values become boolean indicators
* Useful for validation pipelines

---

## Example 15 — Convert String Numbers to Integers

```python
raw = {"a": "10", "b": "20", "c": "30"}

converted = {k: int(v) for k, v in raw.items()}

print(converted)
```

```text
{'a': 10, 'b': 20, 'c': 30}
```

**Explanation**

* Type normalization
* Prevents downstream numeric errors
