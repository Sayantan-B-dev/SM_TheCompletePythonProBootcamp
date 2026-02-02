### CONSTRAINTS + GLOBAL SCOPE (HOW THEY INTERACT IN REAL SYSTEMS)

---

## 1. WHAT “CONSTRAINTS” MEAN IN PRACTICAL CODING

A **constraint** is a rule that limits:

* where data can be accessed
* how data can be modified
* who is allowed to modify it
* when it is allowed to change

Constraints exist to:

* prevent bugs
* control side effects
* preserve invariants
* enforce business rules

Global scope is **powerful**, so it must be **constrained intentionally**.

---

## 2. WHY GLOBAL SCOPE IS DANGEROUS WITHOUT CONSTRAINTS

### Unconstrained global variable

```python
balance = 1000

def withdraw():
    global balance
    balance -= 500

def deposit():
    global balance
    balance += 200

withdraw()
deposit()
withdraw()
print(balance)
```

**Output**

```
200
```

### Problem

* Any function can mutate `balance`
* No validation
* No audit trail
* No access control
* Order-dependent bugs

This code *works* but is **professionally unacceptable**.

---

## 3. CONSTRAINT TYPE 1 — READ-ONLY GLOBALS (CONSTANTS)

### Proper global usage: constants

```python
TAX_RATE = 0.18
MAX_RETRY = 3

def calculate_tax(amount):
    return amount * TAX_RATE

print(calculate_tax(1000))
```

**Output**

```
180.0
```

### Constraint applied

* Global values are **never mutated**
* Uppercase naming signals immutability
* Safe, predictable, professional

---

## 4. CONSTRAINT TYPE 2 — WRITE RESTRICTION VIA FUNCTIONS

### Controlled mutation (no direct global writes)

```python
_balance = 1000   # internal global (convention)

def get_balance():
    return _balance

def update_balance(amount):
    global _balance
    if _balance + amount < 0:
        raise ValueError("Insufficient funds")
    _balance += amount

update_balance(-200)
update_balance(300)
print(get_balance())
```

**Output**

```
1100
```

### Constraint applied

* Only one function can mutate state
* Validation enforced
* State access controlled

---

## 5. CONSTRAINT TYPE 3 — STATE RETURN (FUNCTIONAL, PROFESSIONAL)

### No global mutation at all

```python
def update_balance(balance, amount):
    if balance + amount < 0:
        raise ValueError("Insufficient funds")
    return balance + amount

balance = 1000
balance = update_balance(balance, -200)
balance = update_balance(balance, 300)
print(balance)
```

**Output**

```
1100
```

### Why this is preferred

* No hidden dependencies
* Thread-safe by design
* Easy to test
* Deterministic behavior

---

## 6. CONSTRAINT TYPE 4 — CONFIGURATION GLOBALS (REAL LIFE)

### Real-world example: application config

```python
DEBUG = False
DB_HOST = "localhost"
DB_PORT = 5432

def connect():
    if DEBUG:
        print("Debug mode ON")
    return f"Connecting to {DB_HOST}:{DB_PORT}"

print(connect())
```

**Output**

```
Connecting to localhost:5432
```

### Constraint applied

* Globals are **configuration only**
* Set once at startup
* Read-only during runtime

Used in:

* web servers
* CLI tools
* ML pipelines
* system scripts

---

## 7. CONSTRAINT TYPE 5 — MUTABLE GLOBALS (WHY THEY’RE RARE)

### Example: cache (controlled mutation)

```python
_cache = {}

def get_square(n):
    if n not in _cache:
        _cache[n] = n * n
    return _cache[n]

print(get_square(4))
print(get_square(4))
print(_cache)
```

**Output**

```
16
16
{4: 16}
```

### Constraint applied

* Single responsibility
* Performance optimization
* Predictable mutation

Used for:

* memoization
* caching
* lookup tables

---

## 8. CONSTRAINT TYPE 6 — CLASS-ENCAPSULATED STATE (BEST PRACTICE)

### Real-life pattern: service state

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def update(self, amount):
        if self.balance + amount < 0:
            raise ValueError("Insufficient funds")
        self.balance += amount

acc = BankAccount(1000)
acc.update(-200)
acc.update(300)
print(acc.balance)
```

**Output**

```
1100
```

### Constraint applied

* State owned by object
* Access only through methods
* Invariants preserved

---

## 9. GLOBAL SCOPE IN REAL SYSTEMS (WHERE IT’S ACTUALLY USED)

### Acceptable professional uses

| Use case                       | Why global works    |
| ------------------------------ | ------------------- |
| Constants                      | Never mutate        |
| Configuration                  | Loaded once         |
| Logging setup                  | Shared service      |
| Dependency injection container | Central registry    |
| Feature flags                  | Read-only           |
| Caches                         | Controlled mutation |

---

## 10. WHERE GLOBAL SCOPE IS A RED FLAG 🚨

* Business logic data
* User state
* Financial values
* Request/session data
* Anything time-dependent
* Anything multi-user

If you see these as globals → architecture problem.

---

## 11. DECISION RULE (VERY IMPORTANT)

Ask these questions:

1. **Does this value change over time?**
   → ❌ Don’t use global

2. **Is this value shared intentionally?**
   → Maybe (add constraints)

3. **Can this be passed as an argument?**
   → ✅ Do that instead

4. **Can this belong to an object?**
   → ✅ Best option

---

## 12. FINAL MENTAL MODEL

* Global scope = **shared power**
* Constraints = **safety rails**
* Professional code = **explicit data flow**
* Globals should be:

  * few
  * obvious
  * constrained
  * boring

Most real-world bugs caused by globals are not syntax bugs — they are **design failures**.
