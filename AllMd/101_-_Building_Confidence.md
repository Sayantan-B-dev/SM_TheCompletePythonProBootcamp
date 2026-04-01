Below is a **comprehensive, structured table of bug categories and error types in Python**, separated cleanly and explained in a debugging-oriented way. This covers **syntax → runtime → logical → design → environment → concurrency → performance → security**. Treat it as a mental map while debugging.

---

### 1. Syntax-Level Bugs (Code cannot start)

| Category | Error / Bug                         | What it means                | Common cause                                   | How to handle                            |
| -------- | ----------------------------------- | ---------------------------- | ---------------------------------------------- | ---------------------------------------- |
| Syntax   | `SyntaxError`                       | Python cannot parse the code | Missing `:`, wrong indentation, invalid syntax | Fix structure, read error line carefully |
| Syntax   | `IndentationError`                  | Indentation rules violated   | Mixed tabs/spaces, missing indent              | Use consistent spaces (PEP8: 4 spaces)   |
| Syntax   | `TabError`                          | Tabs + spaces mixed          | Editor misconfiguration                        | Convert tabs to spaces                   |
| Syntax   | `EOL while scanning string literal` | String not closed            | Missing quote                                  | Close string                             |
| Syntax   | `unexpected EOF`                    | Code ended too early         | Missing `)` `}` `]`                            | Balance brackets                         |

These are caught **before execution**.

---

### 2. Type & Value Bugs (Very common in Python)

| Category | Error               | What it means                               | Typical scenario       | Handling                  |
| -------- | ------------------- | ------------------------------------------- | ---------------------- | ------------------------- |
| Type     | `TypeError`         | Operation between incompatible types        | `"5" + 3`              | Convert types explicitly  |
| Type     | `ValueError`        | Correct type, invalid value                 | `int("abc")`           | Validate input            |
| Type     | `AttributeError`    | Attribute doesn’t exist                     | `"hi".push()`          | Check object methods      |
| Type     | `IndexError`        | Index out of range                          | `lst[5]` on small list | Bounds check              |
| Type     | `KeyError`          | Key missing in dict                         | `d["x"]`               | Use `.get()` or check key |
| Type     | `NameError`         | Variable not defined                        | Typo or scope issue    | Define before use         |
| Type     | `UnboundLocalError` | Local variable referenced before assignment | Conditional assignment | Initialize variable       |

---

### 3. Control-Flow & Logic Bugs (No error, wrong result)

| Category | Bug type           | Description                | Example                | Detection        |
| -------- | ------------------ | -------------------------- | ---------------------- | ---------------- |
| Logic    | Wrong condition    | `>` instead of `>=`        | Boundary bugs          | Print / debugger |
| Logic    | Wrong loop range   | `range(n)` vs `range(1,n)` | Off-by-one             | Test edge cases  |
| Logic    | Early `return`     | Function exits too soon    | Dead code after return | Debugger         |
| Logic    | Infinite loop      | Condition never changes    | `while True`           | Print loop state |
| Logic    | Incorrect operator | `and` vs `or`              | Logic inversion        | Truth table      |
| Logic    | Wrong default      | Bad initial value          | Accumulator bugs       | Step-through     |

These are **hardest** because Python doesn’t complain.

---

### 4. Scope & Lifetime Bugs

| Category | Bug                 | Cause                         | Example            | Fix             |
| -------- | ------------------- | ----------------------------- | ------------------ | --------------- |
| Scope    | Global misuse       | Modifying global accidentally | `global x` abuse   | Avoid globals   |
| Scope    | Shadowing           | Local overrides global        | `sum = 0`          | Rename variable |
| Scope    | Late binding        | Closures capture wrong value  | Loops with lambdas | Use defaults    |
| Lifetime | Dangling state      | Old data reused               | Reusing lists      | Reinitialize    |
| Lifetime | Mutable default arg | Shared state                  | `def f(x=[])`      | Use `None`      |

---

### 5. Data Structure & Mutation Bugs

| Category | Bug                  | Explanation              | Example        | Prevention      |
| -------- | -------------------- | ------------------------ | -------------- | --------------- |
| Mutation | Aliasing             | Two names, one object    | `b = a`        | Copy explicitly |
| Mutation | Unexpected overwrite | Key collision            | Dict updates   | Check keys      |
| Mutation | In-place ops         | `.sort()` returns `None` | `x = x.sort()` | Know APIs       |
| Mutation | Shared reference     | Nested lists             | `[[0]*3]*3`    | Deep copy       |

---

### 6. Exception-Handling Bugs

| Category   | Bug              | Why it’s bad        | Example                    | Fix            |
| ---------- | ---------------- | ------------------- | -------------------------- | -------------- |
| Exceptions | Bare `except`    | Hides real bugs     | `except:`                  | Catch specific |
| Exceptions | Swallowed errors | Silent failure      | `pass`                     | Log / re-raise |
| Exceptions | Wrong exception  | Catching wrong type | `KeyError` vs `IndexError` | Read traceback |
| Exceptions | Overuse          | Logic in try block  | Large try                  | Narrow try     |

---

### 7. I/O & External Interaction Bugs

| Category | Error               | Cause            | Handling          |
| -------- | ------------------- | ---------------- | ----------------- |
| File I/O | `FileNotFoundError` | Missing file     | Check path        |
| File I/O | `PermissionError`   | No access        | OS permissions    |
| File I/O | Encoding bugs       | Unicode mismatch | Use `encoding=`   |
| Network  | Timeout             | Slow response    | Retry logic       |
| Network  | ConnectionError     | Server down      | Graceful fallback |
| Input    | Unexpected input    | User lies        | Validation        |

---

### 8. Environment & Dependency Bugs

| Category    | Bug               | Cause                  | Fix                 |
| ----------- | ----------------- | ---------------------- | ------------------- |
| Environment | Version mismatch  | Python 3.12 vs 3.8     | Pin versions        |
| Environment | Missing module    | Not installed          | `pip install`       |
| Environment | Wrong interpreter | Virtualenv issues      | Activate venv       |
| Environment | OS differences    | Path, case sensitivity | Cross-platform code |

---

### 9. Performance & Resource Bugs

| Category    | Bug            | Symptom       | Cause           | Fix             |
| ----------- | -------------- | ------------- | --------------- | --------------- |
| Performance | Slow loops     | Program hangs | O(n²)           | Optimize        |
| Performance | Memory leak    | RAM grows     | References kept | Release objects |
| Performance | Blocking I/O   | App freezes   | Sync calls      | Async/threading |
| Performance | Excess logging | Slow output   | Too many prints | Reduce logs     |

---

### 10. Concurrency & Timing Bugs (Advanced)

| Category    | Bug               | Explanation          | Handling       |
| ----------- | ----------------- | -------------------- | -------------- |
| Concurrency | Race condition    | Order-dependent      | Locks          |
| Concurrency | Deadlock          | Threads wait forever | Timeout        |
| Concurrency | Shared state      | Data corruption      | Immutable data |
| Async       | Await missing     | Coroutine not run    | Use `await`    |
| Async       | Event loop misuse | Nested loops         | Proper design  |

---

### 11. Security & Safety Bugs (Often ignored)

| Category | Bug               | Risk            | Fix              |
| -------- | ----------------- | --------------- | ---------------- |
| Security | Input injection   | Code execution  | Sanitize input   |
| Security | Hardcoded secrets | Credential leak | Env vars         |
| Security | Insecure eval     | Arbitrary code  | Avoid `eval()`   |
| Safety   | Unvalidated input | Crashes         | Defensive coding |

---

### Mental Debugging Rule (important)

If Python **crashes** → read traceback
If Python **runs but wrong output** → logic bug
If Python **works sometimes** → state / mutation / timing bug
If Python **works on one machine** → environment bug

This table is essentially a **debugging checklist**.
When stuck, identify which *category* the bug belongs to before trying to fix it.
