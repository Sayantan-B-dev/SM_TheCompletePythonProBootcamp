Combining multiple operations in Python means chaining logic so data flows cleanly from input → transformation → output, without unnecessary repetition or side effects. This is mostly about expressions, operator precedence, function composition, control flow, and data pipelines.

Start with **expressions vs statements**. Expressions return values and can be combined; statements control flow.

Basic arithmetic and logical combination:

```python
result = (a + b) * c / d
is_valid = age >= 18 and has_id and not banned
```

Operator precedence matters: `() > ** > *, /, //, % > +, - > comparisons > not > and > or`.

Use parentheses when intent must be explicit. Readability beats cleverness.

---

**Chaining function calls** is the cleanest way to combine operations.

```python
name = input().strip().title()
length = len(name)
```

Instead of intermediate variables when the logic is linear:

```python
length = len(input().strip().title())
```

Readable, single responsibility, no mutation.

---

**Conditional expressions (ternary)** for compact logic:

```python
status = "Pass" if score >= 50 else "Fail"
```

Avoid nesting ternaries; that kills clarity.

---

**Combining loops with conditions** using comprehensions:

```python
squares = [x*x for x in range(10) if x % 2 == 0]
```

Equivalent verbose form:

```python
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x*x)
```

Use comprehensions when transformation + filtering is simple.

---

**Multiple operations on collections** using `map`, `filter`, `sorted`:

```python
numbers = [1, 2, 3, 4, 5]

result = sorted(
    map(lambda x: x * x,
        filter(lambda x: x % 2 == 0, numbers))
)
```

But Pythonic preference:

```python
result = sorted(x*x for x in numbers if x % 2 == 0)
```

Generators keep memory usage low.

---

**Combining string operations**:

```python
sentence = "  hello world  "
cleaned = sentence.strip().replace(" ", "_").upper()
```

Each method returns a new string, so chaining is safe.

---

**Combining dictionary operations**:

```python
data = {"a": 1, "b": 2, "c": 3}

total = sum(v for k, v in data.items() if k != "b")
```

---

**Combining exception handling with logic**:

```python
try:
    value = int(input().strip())
    result = 100 / value
except (ValueError, ZeroDivisionError):
    result = None
```

Do not mix too much logic inside `try`; keep only the risky operations.

---

**Combining multiple conditions cleanly**:

Bad:

```python
if age > 18 and age < 60 and employed == True and banned == False:
```

Better:

```python
is_working_age = 18 < age < 60
if is_working_age and employed and not banned:
```

Readable logic scales.

---

**Function composition (best practice)**

Instead of one giant block:

```python
def process(text):
    text = text.strip()
    text = text.lower()
    text = text.replace(" ", "-")
    return text
```

Break and compose:

```python
def normalize(text):
    return text.strip().lower()

def slugify(text):
    return text.replace(" ", "-")

result = slugify(normalize(input()))
```

This is how “proper code” stays testable and reusable.

---

**Combining I/O + processing + output (realistic example)**

```python
def average_even_numbers(nums):
    evens = (n for n in nums if n % 2 == 0)
    return sum(evens) / len([n for n in nums if n % 2 == 0])

numbers = list(map(int, input().split()))
print(average_even_numbers(numbers))
```

Better optimized:

```python
def average_even_numbers(nums):
    evens = [n for n in nums if n % 2 == 0]
    return sum(evens) / len(evens) if evens else 0

print(average_even_numbers(map(int, input().split())))
```

---

**Core rule for “proper” Python code**

1. Combine operations only when intent is obvious.
2. Prefer expressions over temporary variables, but not at the cost of clarity.
3. Break logic into functions once it exceeds one mental step.
4. Read code top-to-bottom like a sentence.

If you want, I can refactor one of your existing Python snippets and show how to combine operations without making it unreadable.
