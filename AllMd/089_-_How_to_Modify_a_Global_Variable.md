### CHANGING A GLOBAL VARIABLE FROM LOCAL SCOPE (AND WHY IT’S USUALLY A BAD IDEA)

---

## METHOD 1 — USING `global` KEYWORD (DIRECT MUTATION)

### Example: Modify global from inside a function

```python
count = 0  # global variable

def increment():
    global count   # tell Python to use global scope
    count += 1     # mutate the global variable

increment()
increment()
print(count)
```

**Output**

```
2
```

### What happens internally

* `count` exists in global namespace
* `global count` disables local binding
* Function directly mutates shared state

### Problems with this approach

* Hidden side effects
* Function depends on external state
* Harder to test
* Breaks function purity
* Dangerous in large programs

Use only for:

* Configuration flags
* Counters tightly controlled in one file
* Quick scripts (not production systems)

---

## METHOD 2 — PROFESSIONAL APPROACH (RETURN VALUE)

### Principle

Functions should:

* Take input
* Return output
* Not mutate external state

---

### Example: Return updated value

```python
def increment(count):
    # count is local to the function
    count += 1
    return count

count = 0
count = increment(count)
count = increment(count)
print(count)
```

**Output**

```
2
```

### Why this is better

* No hidden dependencies
* Easy to test
* Predictable behavior
* Clear data flow
* Functional style

---

## SIDE-BY-SIDE COMPARISON

| Aspect                 | `global` keyword | Return value (preferred) |
| ---------------------- | ---------------- | ------------------------ |
| Mutates external state | Yes              | No                       |
| Function purity        | ❌                | ✅                        |
| Debugging              | Hard             | Easy                     |
| Reusability            | Low              | High                     |
| Testability            | Poor             | Excellent                |
| Professional code      | Rare             | Standard                 |

---

## METHOD 3 — MULTIPLE UPDATES (STATE PIPELINE)

### Bad (global)

```python
total = 0

def add():
    global total
    total += 5
```

### Good (state passing)

```python
def add(total):
    return total + 5

total = 0
total = add(total)
total = add(total)
print(total)
```

**Output**

```
10
```

---

## METHOD 4 — USING A MUTABLE OBJECT (CONTROLLED SHARED STATE)

### Example with dictionary

```python
state = {"count": 0}

def increment(state):
    state["count"] += 1

increment(state)
increment(state)
print(state["count"])
```

**Output**

```
2
```

### When this is acceptable

* Intentional shared state
* Clear ownership
* Structured data
* Used in frameworks and systems

---

## METHOD 5 — CLASS-BASED STATE (MOST PROFESSIONAL)

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

c = Counter()
c.increment()
c.increment()
print(c.count)
```

**Output**

```
2
```

### Why this is best for real systems

* Encapsulation
* Clear ownership
* Scales well
* Extensible
* Thread-safe patterns possible

---

## RULE OF THUMB (MEMORIZE)

1. ❌ Avoid `global`
2. ✅ Prefer return values
3. ✅ Use objects for evolving state
4. ✅ Keep functions pure when possible
5. 🧠 Scope control = bug prevention

If you understand this, you’ve crossed from beginner-level Python into **professional-grade design thinking**.
