A **namespace** is a mapping between *names* (identifiers) and *objects* (values, functions, classes). In practical terms, it is a dictionary-like structure that tells the interpreter: “when I see this name, this is the object it refers to.”

Scoping answers **where a name can be accessed**.
Namespaces answer **where a name is stored**.

They work together.

In Python, every scope has an associated namespace.

---

Namespaces in Python exist to:

1. Avoid name collisions
2. Organize code logically
3. Control lifetime of objects
4. Make name resolution deterministic

---

### Types of namespaces in Python

1. **Built-in namespace**
   Contains names provided by Python itself.
   Examples: `len`, `print`, `int`, `range`

2. **Global namespace**
   Created when a module (file) is loaded.
   Exists for the entire lifetime of the program.

3. **Local namespace**
   Created when a function is called.
   Destroyed when the function exits.

4. **Enclosing namespace**
   Exists for nested functions (outer function scope).

Python resolves names using **LEGB** order:
Local → Enclosing → Global → Built-in

---

### Global scope

A name is in the global scope if it is defined at the top level of a file.

```
x = 100   # global variable

def show():
    print(x)
```

Properties of global scope:

* Accessible anywhere in the same module (unless shadowed)
* Exists for the entire runtime
* Risky if mutated unintentionally
* Shared state across functions

Global namespace example (conceptually):

```
{
  'x': 100,
  'show': <function show>
}
```

---

### Local scope

A name is in local scope if it is defined inside a function.

```
def func():
    y = 10   # local variable
    print(y)
```

Properties of local scope:

* Exists only during function execution
* Cannot be accessed outside the function
* Safer and predictable
* Preferred for most variables

Local namespace example (conceptually):

```
{
  'y': 10
}
```

Once `func()` finishes, this namespace is destroyed.

---

### Local vs Global: shadowing

Local variables can **shadow** global variables with the same name.

```
x = 50

def test():
    x = 10
    print(x)

test()   # 10
print(x) # 50
```

Here:

* `x = 10` lives in local namespace
* global `x` remains unchanged
* no conflict because namespaces are separate

---

### Modifying global variables

Reading a global variable inside a function is allowed.
Modifying it is **not**, unless explicitly declared.

```
count = 0

def increment():
    count += 1   # ERROR
```

Python raises `UnboundLocalError` because:

* Assignment creates a local name
* Python now treats `count` as local
* But it is read before assignment

Correct way:

```
count = 0

def increment():
    global count
    count += 1
```

Using `global` tells Python:
“Use the global namespace, not the local one.”

This is legal but discouraged in most designs because it couples functions to shared state.

---

### Enclosing (nonlocal) scope

Used with nested functions.

```
def outer():
    x = 5
    def inner():
        return x
    return inner()
```

Here:

* `x` is not local to `inner`
* not global either
* it is in the **enclosing namespace**

If you want to modify it:

```
def outer():
    x = 5
    def inner():
        nonlocal x
        x += 1
    inner()
    return x
```

`nonlocal` means:
“Use the variable from the nearest enclosing scope.”

---

### Why local scope is preferred over global

Local scope:

* reduces side effects
* improves testability
* makes functions reusable
* avoids hidden dependencies
* simplifies debugging

Global scope:

* introduces tight coupling
* increases risk of accidental mutation
* harder to reason about
* harder to maintain at scale

Rule of thumb:
Use **local scope by default**
Use **global scope only for constants or configuration**

---

### Namespace inspection (advanced)

Python exposes namespaces explicitly:

```
globals()   # returns global namespace dictionary
locals()    # returns local namespace dictionary
```

Inside a function, `locals()` shows the local namespace.
At top level, `locals()` ≈ `globals()`.

---

### Mental model summary

* **Namespace**: where names live
* **Scope**: where names are visible
* Local scope = temporary, safe, isolated
* Global scope = persistent, shared, risky
* Python resolves names using LEGB
* `global` and `nonlocal` explicitly break default isolation

Understanding namespaces and local vs global scope is foundational. Every bug related to “variable not defined”, “unexpected value”, or “state changed magically” traces back to misunderstanding these rules.
