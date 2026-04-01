## List Comprehension — **Level 1 (Foundation Mastery)**

*Goal: build absolute clarity on syntax, flow, and meaning. No nesting, no multiple conditions.*

---

## Core Equation (Level 1 Scope)

```text
new_list = [operation for item in sequence]
```

Read it **right → left**

> “For each `item` in `sequence`, apply `operation`, collect results.”

---

## Example 1 — Square Numbers

```python
numbers = [1, 2, 3, 4, 5]

squares = [n ** 2 for n in numbers]

print(squares)
```

```text
[1, 4, 9, 16, 25]
```

**Explanation**

* `numbers` is the source sequence
* `n` receives each value
* `n ** 2` transforms each value
* Output list contains transformed values only

---

## Example 2 — Convert Celsius to Fahrenheit

```python
celsius = [0, 20, 30, 40]

fahrenheit = [(temp * 9/5) + 32 for temp in celsius]

print(fahrenheit)
```

```text
[32.0, 68.0, 86.0, 104.0]
```

**Explanation**

* Mathematical transformation applied uniformly
* No filtering, only mapping

---

## Example 3 — Uppercase Characters from String

```python
word = "python"

uppercase_letters = [ch.upper() for ch in word]

print(uppercase_letters)
```

```text
['P', 'Y', 'T', 'H', 'O', 'N']
```

**Explanation**

* Strings are sequences of characters
* Each character becomes an element
* Result is a list, not a string

---

## Example 4 — Length of Each Word

```python
words = ["data", "science", "python"]

lengths = [len(word) for word in words]

print(lengths)
```

```text
[4, 7, 6]
```

**Explanation**

* `len()` is applied to every element
* Result list preserves order

---

## Example 5 — Add Fixed Bonus to Salaries

```python
salaries = [25000, 30000, 40000]

updated_salaries = [salary + 5000 for salary in salaries]

print(updated_salaries)
```

```text
[30000, 35000, 45000]
```

**Explanation**

* Each value is adjusted equally
* Clean replacement for repetitive loops

---

## Example 6 — Convert Integers to Strings

```python
numbers = [1, 2, 3, 4]

as_strings = [str(n) for n in numbers]

print(as_strings)
```

```text
['1', '2', '3', '4']
```

**Explanation**

* Type transformation
* Useful in formatting and display pipelines

---

## Example 7 — Extract First Letter of Each Name

```python
names = ["Asha", "Ravi", "Neha"]

initials = [name[0] for name in names]

print(initials)
```

```text
['A', 'R', 'N']
```

**Explanation**

* Indexing inside comprehension
* Each element accessed independently

---

## Example 8 — Multiply Range Values

```python
doubled = [x * 2 for x in range(1, 6)]

print(doubled)
```

```text
[2, 4, 6, 8, 10]
```

**Explanation**

* `range()` generates numbers lazily
* Comprehension materializes them into a list

---

## Example 9 — Absolute Values

```python
values = [-10, 5, -3, 8]

absolute_values = [abs(v) for v in values]

print(absolute_values)
```

```text
[10, 5, 3, 8]
```

**Explanation**

* Function application per element
* Original list remains unchanged

---

## Example 10 — Replace Spaces with Underscores

```python
sentence = "data science rocks"

formatted = [ch if ch != " " else "_" for ch in sentence]

print(formatted)
```

```text
['d', 'a', 't', 'a', '_', 's', 'c', 'i', 'e', 'n', 'c', 'e', '_', 'r', 'o', 'c', 'k', 's']
```

**Explanation**

* Conditional expression inside operation
* Still Level 1 because there is:

  * one sequence
  * one condition
  * no filtering

---