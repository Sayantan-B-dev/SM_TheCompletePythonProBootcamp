### Python `random` module — complete, structured, practical

---

## What the `random` module is

The `random` module is a **standard library (internal) module** that provides functions to generate **pseudo-random numbers**.
“Pseudo” means the numbers are *deterministic* under the hood, but they *appear* random.

Internally, Python uses the **Mersenne Twister** algorithm:

* Very fast
* Very uniform distribution
* Deterministic given the same seed
* **Not cryptographically secure**

Use cases:

* Simulations
* Games
* Sampling
* Testing
* Shuffling data
* Randomized algorithms

Do **not** use `random` for passwords, tokens, or security-sensitive data.

---

## Importing the module

```python
import random
```

Or selective import (not recommended for large projects):

```python
from random import randint, choice
```

---

## Core concepts

### 1. Random number generation range

| Function                       | Range               |
| ------------------------------ | ------------------- |
| `random()`                     | `0.0 ≤ x < 1.0`     |
| `randint(a, b)`                | `a ≤ x ≤ b`         |
| `randrange(start, stop, step)` | like `range()`      |
| `uniform(a, b)`                | `a ≤ x ≤ b` (float) |

---

## `random.random()`

Generates a float between **0.0 (inclusive)** and **1.0 (exclusive)**.

```python
import random

value = random.random()
print(value)
```

Output (example):

```text
0.7429318946123804
```

Use case:

* Probability simulations
* Normalizing randomness
* Monte Carlo methods

---

## `random.randint(a, b)`

Generates an **integer** between `a` and `b` **inclusive**.

```python
import random

num = random.randint(1, 6)
print(num)
```

Output:

```text
4
```

Use case:

* Dice rolls
* Random IDs (non-secure)
* Game logic

---

## `random.randrange(start, stop, step)`

Works exactly like `range()` but returns **one random value**.

```python
import random

num = random.randrange(0, 10, 2)
print(num)
```

Possible outputs:

```text
0
2
4
6
8
```

Why use this instead of `randint`:

* When step control matters
* When excluding the end value

---

## `random.uniform(a, b)`

Generates a **float** between `a` and `b`.

```python
import random

value = random.uniform(1.5, 5.5)
print(value)
```

Output:

```text
3.982144177891234
```

Used when you need **continuous values**, not integers.

---

## Choosing from sequences

### `random.choice(sequence)`

Selects **one random element**.

```python
import random

colors = ["red", "green", "blue"]
print(random.choice(colors))
```

Output:

```text
green
```

Raises error if sequence is empty.

---

### `random.choices(sequence, k=n)`

Selects **multiple elements**, **with replacement**.

```python
import random

numbers = [1, 2, 3, 4]
result = random.choices(numbers, k=5)
print(result)
```

Output:

```text
[2, 4, 2, 1, 4]
```

Same value can appear multiple times.

---

### `random.sample(sequence, k=n)`

Selects **unique elements**, **without replacement**.

```python
import random

numbers = [1, 2, 3, 4, 5]
result = random.sample(numbers, k=3)
print(result)
```

Output:

```text
[5, 1, 3]
```

Error if `k > len(sequence)`.

---

## Shuffling data

### `random.shuffle(list)`

Shuffles a list **in place** (modifies original list).

```python
import random

nums = [1, 2, 3, 4, 5]
random.shuffle(nums)
print(nums)
```

Output:

```text
[3, 5, 1, 2, 4]
```

Important:

* Works **only on mutable sequences**
* Returns `None`

---

## Random distributions

### `random.gauss(mu, sigma)`

Gaussian (normal) distribution.

```python
import random

value = random.gauss(0, 1)
print(value)
```

Output:

```text
-0.3428912398123
```

Used in:

* Statistics
* ML simulations
* Noise generation

---

### `random.normalvariate(mu, sigma)`

Similar to `gauss`, but slower and more general.

---

### Other distributions

| Function                      | Purpose                  |
| ----------------------------- | ------------------------ |
| `expovariate(lambd)`          | Exponential distribution |
| `betavariate(a, b)`           | Beta distribution        |
| `lognormvariate(mu, sigma)`   | Log-normal               |
| `triangular(low, high, mode)` | Triangular               |

---

## Seeding (very important)

### `random.seed(value)`

Sets the starting point of randomness.

Same seed ⇒ same results.

```python
import random

random.seed(42)
print(random.randint(1, 10))
print(random.randint(1, 10))
```

Output:

```text
2
1
```

Run again → exact same output.

Use cases:

* Debugging
* Testing
* Reproducible simulations

---

## Why `random` is NOT secure

The sequence is **predictable** if seed is known.

❌ Do NOT use for:

* Passwords
* OTPs
* Tokens
* Cryptography

Use instead:

```python
import secrets
```

Example:

```python
import secrets
print(secrets.randbelow(10))
```

---

## Common patterns (real usage)

### Dice simulation

```python
import random

dice = random.randint(1, 6)
print(f"Dice rolled: {dice}")
```

Output:

```text
Dice rolled: 6
```

---

### Random password (NON-secure example)

```python
import random
import string

chars = string.ascii_letters + string.digits
password = "".join(random.choice(chars) for _ in range(8))
print(password)
```

Output:

```text
A9xQ2mZ7
```

---

### Randomizing test data

```python
import random

users = ["alice", "bob", "charlie", "david"]
random.shuffle(users)
print(users)
```

Output:

```text
['charlie', 'alice', 'david', 'bob']
```

---

## Summary table

| Feature                | Function      |
| ---------------------- | ------------- |
| Float [0,1)            | `random()`    |
| Integer range          | `randint()`   |
| Range with step        | `randrange()` |
| Float range            | `uniform()`   |
| Single item            | `choice()`    |
| Multiple (dup allowed) | `choices()`   |
| Multiple (unique)      | `sample()`    |
| Shuffle list           | `shuffle()`   |
| Reproducibility        | `seed()`      |
| Normal distribution    | `gauss()`     |

---

## Mental model to remember

* `random` = **simulation & convenience**
* `secrets` = **security**
* Seed controls determinism
* Shuffle modifies in place
* Sample ≠ choices
