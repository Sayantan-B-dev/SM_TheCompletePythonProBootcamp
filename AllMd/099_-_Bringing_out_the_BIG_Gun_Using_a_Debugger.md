**Debugging – Stage 6: Debugger (the big gun)**

This stage is used when `print()` becomes noisy, slow, or insufficient. A debugger lets you **pause time**, **inspect state**, and **walk the program exactly as Python executes it**. This is not guessing; this is controlled execution.

---

First, **understand what a debugger actually does**.
A debugger:

* Stops execution at a chosen line (breakpoint)
* Lets you step line by line
* Shows variable values and types in real time
* Allows expression evaluation mid-execution
* Reveals control-flow paths that never run

This is essentially *Stage 3 (play computer)* automated.

---

Second, **use breakpoints correctly (IDE-based debugging)**.
A breakpoint should be placed:

* Just **before state changes**
* Just **before a decision**
* Just **before a crash**
* At function entry or exit

Bad breakpoint:

* Random line “somewhere in the function”

Good breakpoint:

```python
a = input()        # breakpoint here
a = int(a)
```

This lets you inspect the value *before conversion*.

---

Third, **step types and what they mean**.
Every debugger offers these core controls:

* **Step Over**
  Executes the current line without entering function calls.

* **Step Into**
  Enters the function being called.

* **Step Out**
  Runs until the current function returns.

Use rule:

* Step Into → when you don’t trust the function
* Step Over → when the function is already trusted

---

Fourth, **inspect variables ruthlessly**.
While paused:

* Check value
* Check type
* Check mutability
* Check references (same object or different)

Example:

```python
a = []
b = a
```

Debugger reveals:

* `id(a) == id(b)` → aliasing bug confirmed instantly

---

Fifth, **watch expressions, not just variables**.
Most debuggers allow “watch expressions”.

Example:

```python
len(my_list)
score > 50
type(user_input)
```

These update live as you step, revealing when conditions flip.

---

Sixth, **observe control flow, not just data**.
Debuggers expose:

* Which `if` branch was taken
* How many times a loop runs
* Where a function returns early

This kills bugs caused by:

* Wrong indentation
* Early `return`
* Misplaced `break` or `continue`

---

Seventh, **conditional breakpoints (power move)**.
Break only when a condition is true.

Example:

* Break when `i == 57`
* Break when `user_input is None`
* Break when `len(items) > 1000`

This avoids stepping through 10,000 iterations.

---

Eighth, **exception breakpoints**.
Configure debugger to stop:

* On raised exceptions
* On uncaught exceptions

This shows you the *exact* line and state **before** Python crashes.

Much better than reading tracebacks backward.

---

Ninth, **Python’s built-in debugger (`pdb`)**.
When IDE debugging isn’t available.

Example:

```python
import pdb
pdb.set_trace()
```

This creates a breakpoint in terminal execution.

Useful commands:

* `n` → next line
* `s` → step into
* `c` → continue
* `p var` → print variable
* `l` → list code

Yes, it’s ugly. Yes, it’s powerful.

---

Tenth, **advanced / weird but valid options**.
These are situational, not default:

* `trace` module → execution tracing
* `faulthandler` → low-level crashes
* `sys.settrace()` → custom tracing (advanced)
* Logging frameworks (when prints are not enough)

These are for deep, pathological bugs.

---

Eleventh, **exit debugger with understanding, not relief**.
Do not stop debugging just because:

* “It works now”
* “I changed something and the bug disappeared”

You must be able to state:

* What the bug was
* Why it happened
* Why the fix works

If you can’t, the bug isn’t truly dead.

---

A **successful Stage 6 result** looks like this:

> Using breakpoints and step execution, the incorrect state was observed forming at runtime.
> Control flow and data mutation were confirmed visually.
> The fix was validated by stepping through the corrected execution path.

Debugger is the **courtroom CCTV** of code.
Once you use it properly, many “mysterious” bugs stop feeling mysterious at all.
