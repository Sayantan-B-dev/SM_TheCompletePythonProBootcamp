# Errors, Exceptions, `try–except–else–finally` in Python

*A deep, job-level, practical reference*

---

## 1. What is an error vs an exception

### 1.1 Error (general concept)

An **error** is any situation where a program cannot proceed as written.

Two broad categories exist:

| Category                      | When it happens  | Can program continue? |
| ----------------------------- | ---------------- | --------------------- |
| **Syntax Error**              | Before execution | No                    |
| **Exception (Runtime Error)** | During execution | Yes (if handled)      |

---

## 2. Syntax Errors (cannot be caught)

### Definition

Mistakes in Python grammar detected **before execution**.

### Examples

```python
# Missing colon
if x == 5
    print(x)
```

```python
# Invalid indentation
def test():
print("hello")
```

### Key facts

* Detected by the parser
* **Cannot** be handled with `try–except`
* Must be fixed in code

---

## 3. Exceptions (runtime errors)

### Definition

Errors raised **while the program is running**.

They interrupt normal execution **unless handled**.

---

## 4. Built-in exception hierarchy (important for interviews)

```
BaseException
 ├── Exception
 │    ├── ValueError
 │    ├── TypeError
 │    ├── IndexError
 │    ├── KeyError
 │    ├── AttributeError
 │    ├── ZeroDivisionError
 │    ├── FileNotFoundError
 │    ├── PermissionError
 │    ├── ImportError
 │    └── RuntimeError
 ├── SystemExit
 ├── KeyboardInterrupt
 └── GeneratorExit
```

**Rule**
Catch subclasses of `Exception`, not `BaseException`.

---

## 5. The `try–except` block (core mechanism)

### Basic structure

```python
try:
    # code that may fail
except SomeException:
    # recovery path
```

---

## 6. Why `try–except` exists (design reasoning)

Without handling:

```python
x = int("abc")  # program crashes
```

With handling:

```python
try:
    x = int("abc")
except ValueError:
    x = 0
```

**Goal**
Control failure, not avoid it.

---

## 7. Single specific exception handling

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero is not allowed")
```

**Output**

```
Division by zero is not allowed
```

---

## 8. Multiple `except` blocks (professional pattern)

```python
try:
    x = int(input())
    y = int(input())
    print(x / y)

except ValueError:
    print("Invalid integer input")

except ZeroDivisionError:
    print("Cannot divide by zero")
```

**Why this matters**

* Precise error recovery
* Clear user feedback
* Avoids masking bugs

---

## 9. Catching multiple exceptions together

```python
try:
    value = int(data["age"])
except (KeyError, ValueError):
    value = 0
```

**Use when**

* Recovery logic is identical
* Errors are conceptually related

---

## 10. Catching *any* exception (dangerous)

```python
try:
    risky_operation()
except Exception:
    print("Something went wrong")
```

### Why interviewers dislike this

* Hides bugs
* Makes debugging harder
* Breaks observability

**Correct usage**

* Logging
* Cleanup
* Re-raising

---

## 11. Accessing exception object

```python
try:
    int("abc")
except ValueError as e:
    print(e)
```

**Output**

```
invalid literal for int() with base 10: 'abc'
```

**Use cases**

* Logging
* Debugging
* Error transformation

---

## 12. The `else` block (rare but powerful)

### Definition

Runs **only if no exception occurred**.

```python
try:
    x = int("10")
except ValueError:
    print("Invalid")
else:
    print("Parsed:", x)
```

**Output**

```
Parsed: 10
```

### Why it exists

* Keeps success logic separate from failure logic
* Cleaner than flags

---

## 13. The `finally` block (guaranteed execution)

### Definition

Runs **always**, regardless of exception or return.

```python
try:
    file = open("data.txt")
    data = file.read()
finally:
    file.close()
```

### Key guarantees

* Executes even if:

  * Exception occurs
  * `return` is executed
  * Exception is not caught

---

## 14. `try–except–else–finally` full structure

```python
try:
    # risky operation
except ValueError:
    # handle specific failure
else:
    # runs only if no exception
finally:
    # cleanup always
```

---

## 15. Tricky behavior: `return` vs `finally`

```python
def test():
    try:
        return 1
    finally:
        print("cleanup")

print(test())
```

**Output**

```
cleanup
1
```

**Rule**

* `finally` runs **before** returning

---

## 16. Overriding return inside `finally` (dangerous)

```python
def test():
    try:
        return 1
    finally:
        return 2

print(test())
```

**Output**

```
2
```

**Why this is bad**

* Silently overrides logic
* Hard to debug
* Avoid in production

---

## 17. Raising exceptions manually (`raise`)

### Why raise manually

* Enforce business rules
* Fail fast
* Validate inputs

```python
age = -5
if age < 0:
    raise ValueError("Age cannot be negative")
```

---

## 18. Re-raising exceptions (critical skill)

```python
try:
    process_data()
except Exception:
    log_error()
    raise
```

**Why this matters**

* Preserves stack trace
* Allows upstream handling

---

## 19. Creating custom exceptions (senior-level)

```python
class PaymentError(Exception):
    pass

class InsufficientBalance(PaymentError):
    pass
```

```python
raise InsufficientBalance("Not enough funds")
```

**Why companies care**

* Domain-specific errors
* Clean APIs
* Better debugging

---

## 20. Exception chaining (`from` keyword)

```python
try:
    int("abc")
except ValueError as e:
    raise RuntimeError("Parsing failed") from e
```

**Benefit**

* Full causal chain preserved
* Essential for production debugging

---

## 21. Common exceptions you *must* know

| Exception         | When it occurs            |
| ----------------- | ------------------------- |
| ValueError        | Correct type, wrong value |
| TypeError         | Wrong type                |
| IndexError        | List index out of range   |
| KeyError          | Missing dict key          |
| AttributeError    | Missing attribute         |
| FileNotFoundError | File not found            |
| PermissionError   | Access denied             |
| ImportError       | Module import fails       |
| TimeoutError      | Operation timed out       |

---

## 22. Exception handling with files (real-world)

```python
try:
    with open("data.txt") as f:
        content = f.read()
except FileNotFoundError:
    content = ""
```

**Why `with` is preferred**

* Implicit `finally`
* Automatic cleanup

---

## 23. Exception handling in loops (tricky)

```python
for item in items:
    try:
        process(item)
    except Exception:
        continue
```

**Behavior**

* One failure doesn’t stop loop
* Useful for batch processing

---

## 24. Silent failure anti-pattern (very bad)

```python
try:
    risky()
except:
    pass
```

**Why it’s dangerous**

* Hides production bugs
* Breaks observability
* Fails interviews

---

## 25. When *not* to use `try–except`

| Situation           | Better approach       |
| ------------------- | --------------------- |
| Input validation    | `if` checks           |
| Expected conditions | Guard clauses         |
| Control flow        | Logic, not exceptions |

---

## 26. Performance considerations (advanced)

* Exceptions are **slow**
* Do not use for normal flow

**Bad**

```python
try:
    value = data[key]
except KeyError:
    value = 0
```

**Good**

```python
value = data.get(key, 0)
```

---

## 27. Exception handling in APIs (high-paying job topic)

### Pattern

* Catch internally
* Log with context
* Return clean error

```python
try:
    process_request()
except DatabaseError as e:
    logger.error(e)
    raise ServiceUnavailable()
```

---

## 28. Logging exceptions properly

```python
import logging

try:
    1 / 0
except Exception:
    logging.exception("Unexpected error")
```

**Difference**

* `exception()` includes stack trace
* Critical for production

---

## 29. Interview traps to remember

* `except Exception` ≠ catching everything
* `finally` always runs
* `else` only runs on success
* `raise` preserves flow
* Custom exceptions matter
* Never swallow errors
* Prefer clarity over cleverness

---

## 30. Mental model (important)

> Exceptions are **contracts for failure**, not mistakes.

Good engineers **design failure paths** deliberately.


## Big example: one `try` block, many failures possible

```python
def process_user_file(filename):
    """
    Simulates a complex real-world processing pipeline.
    Demonstrates multiple exception types and handling strategies.
    """

    file_handle = None  # declared early so finally can access it

    try:
        # --------------------------------------------------
        # FILE OPERATION (FileNotFoundError, PermissionError)
        # --------------------------------------------------
        file_handle = open(filename, "r")
        raw_data = file_handle.read()

        # --------------------------------------------------
        # PARSING DATA (ValueError)
        # Expecting something like: "age=25,balance=100"
        # --------------------------------------------------
        parts = raw_data.split(",")
        data = {}

        for part in parts:
            key, value = part.split("=")   # ValueError if malformed
            data[key.strip()] = value.strip()

        # --------------------------------------------------
        # KEY ACCESS (KeyError)
        # --------------------------------------------------
        age = int(data["age"])             # KeyError / ValueError
        balance = float(data["balance"])  # KeyError / ValueError

        # --------------------------------------------------
        # BUSINESS RULE (manual raise)
        # --------------------------------------------------
        if age < 18:
            raise InvalidBusinessRule("User must be at least 18 years old")

        # --------------------------------------------------
        # ZERO DIVISION (ZeroDivisionError)
        # --------------------------------------------------
        score = balance / (age - age)      # always zero → intentional

        # --------------------------------------------------
        # ATTRIBUTE ERROR
        # --------------------------------------------------
        score = score.upper()              # float has no upper()

        return score

    # ======================================================
    # LOW-LEVEL EXCEPTIONS (TECHNICAL FAILURES)
    # ======================================================

    except FileNotFoundError as e:
        raise DataPipelineError("Input file is missing") from e

    except PermissionError as e:
        raise DataPipelineError("No permission to read file") from e

    except ValueError as e:
        raise DataPipelineError("Invalid data format") from e

    except KeyError as e:
        raise DataPipelineError(f"Missing required field: {e}") from e

    except ZeroDivisionError as e:
        raise DataPipelineError("Invalid calculation (division by zero)") from e

    except AttributeError as e:
        raise DataPipelineError("Unexpected object type used") from e

    # ======================================================
    # DOMAIN-LEVEL EXCEPTION (already meaningful)
    # ======================================================

    except InvalidBusinessRule:
        # Already a clean domain error → just re-raise
        raise

    # ======================================================
    # LAST RESORT (never swallow)
    # ======================================================

    except Exception as e:
        raise DataPipelineError("Unknown pipeline failure") from e

    # ======================================================
    # SUCCESS PATH
    # ======================================================

    else:
        # Runs only if no exception happened
        print("Processing completed successfully")

    # ======================================================
    # CLEANUP (ALWAYS RUNS)
    # ======================================================

    finally:
        if file_handle:
            file_handle.close()
            print("File handle closed")
```

---

## How to call it (test harness)

```python
try:
    process_user_file("user.txt")
except DataPipelineError as e:
    print("PIPELINE ERROR:", e)
    if e.__cause__:
        print("ROOT CAUSE:", type(e.__cause__).__name__, "-", e.__cause__)
except InvalidBusinessRule as e:
    print("BUSINESS RULE VIOLATION:", e)
```

---

## Example failure outputs (various scenarios)

### 1. File missing

```
PIPELINE ERROR: Input file is missing
ROOT CAUSE: FileNotFoundError - [Errno 2] No such file or directory
```

---

### 2. Malformed data

```
PIPELINE ERROR: Invalid data format
ROOT CAUSE: ValueError - not enough values to unpack
```

---

### 3. Missing key

```
PIPELINE ERROR: Missing required field: 'age'
ROOT CAUSE: KeyError - 'age'
```

---

### 4. Business rule violation

```
BUSINESS RULE VIOLATION: User must be at least 18 years old
```

---

### 5. Division by zero

```
PIPELINE ERROR: Invalid calculation (division by zero)
ROOT CAUSE: ZeroDivisionError - division by zero
```

---

## Why this example matters for high-paying roles

**This single block demonstrates:**

| Skill                        | Why it matters        |
| ---------------------------- | --------------------- |
| Precise exception catching   | Avoids masking bugs   |
| Exception chaining           | Preserves root cause  |
| Custom exceptions            | Clean APIs            |
| Business vs technical errors | Scalable design       |
| Proper cleanup               | Resource safety       |
| Re-raising                   | Debuggable systems    |
| No silent failure            | Production-grade code |

---

## Mental takeaway (very important)

> **Junior code** catches errors to stop crashes
> **Senior code** transforms errors into meaningful, traceable signals

If you can read, write, and explain code like this clearly, you are already operating at a **senior Python backend level**.
