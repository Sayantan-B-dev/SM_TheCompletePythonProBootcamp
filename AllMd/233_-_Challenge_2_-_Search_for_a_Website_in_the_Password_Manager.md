## Notes to take:

> Changes been done in `storage.py` and `ui.py` files. from `Section_029_-_Day_29_-_Intermediate_-_Building_a_Password_Manager_GUI_App_with_Tkinter/password-manager`

> `storage.py` file has been updated to handle the errors and exceptions that may occur while searching for a website in the password manager. `find_password` function is being add there

> `ui.py` file has been updated to handle the errors and exceptions that may occur while searching for a website in the password manager.
`on_find` function is being add there

## Overall architecture (what files do and why)

You have **three conceptual layers**:

| Layer          | File              | Responsibility             |
| -------------- | ----------------- | -------------------------- |
| Storage layer  | `storage.py`      | Reads / writes JSON safely |
| UI logic layer | `ui.py`           | Handles user actions       |
| UI widgets     | `tkinter widgets` | Visual input/output        |

**Key rule followed**
UI **never** touches JSON directly.
Storage **never** touches UI widgets.

This separation is **industry-grade design**.

---

## 1. `find_password()` in `storage.py` — deep explanation

### Function definition

```python
def find_password(website):
    """
    Finds password for the given website.
    Returns password if found, None otherwise.
    """
```

### Purpose

* Look up credentials for a given website
* Read from persistent storage (JSON)
* Return clean data to UI
* Never crash the app

This function is **pure business logic**.

---

## 2. Entering the `try` block (critical)

```python
try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
```

### What happens step-by-step

1. Opens the JSON file in **read mode**
2. `with` ensures automatic file closing
3. `json.load()`:

   * Reads file contents
   * Validates JSON syntax
   * Converts JSON → Python dictionary

### Result

`data` is now a Python `dict` like:

```python
{
    "google.com": {
        "username": "abc@gmail.com",
        "password": "123"
    }
}
```

---

## 3. Website existence check

```python
if website in data:
```

### Why this check is mandatory

Accessing:

```python
data[website]
```

without checking would raise `KeyError`.

This is **defensive programming**.

---

## 4. Extracting credentials (nested dictionary access)

```python
email = data[website]["username"]
password = data[website]["password"]
```

### Data structure being accessed

```python
data = {
    website: {
        "username": "...",
        "password": "..."
    }
}
```

This means:

* First key → website
* Second-level keys → credential fields

### Why not `.get()` here

Because:

* If `"username"` or `"password"` is missing, that’s **data corruption**
* Failing fast is correct in storage layer

---

## 5. Returning data to caller

```python
return email, password
```

### Important detail

This returns a **tuple**:

```python
(email, password)
```

This makes the function predictable and structured.

---

## 6. Website not found case

```python
else:
    return None, None
```

### Why return `(None, None)` instead of `None`

Because the caller expects **two values**:

```python
email, password = find_password(...)
```

Returning a single `None` would crash the UI.

This preserves the function contract.

---

## 7. Exception handling (critical safety)

### File not found

```python
except FileNotFoundError:
    return None, None
```

Occurs when:

* App runs first time
* File deleted manually

Behavior:

* Treats missing file as “no data exists”
* UI decides how to respond

---

### Corrupted or empty JSON

```python
except json.JSONDecodeError:
    return None, None
```

Occurs when:

* File is empty
* File is partially written
* File manually edited incorrectly

Storage layer **absorbs the failure** and returns a clean signal.

---

## 8. Why storage layer never shows popups

Storage layer:

* Returns values
* Never interacts with UI
* Never shows messages

This keeps logic reusable and testable.

---

## 9. Import connection between files

In `ui.py`:

```python
from storage import save_credentials, find_password
```

### What this does

* Loads `storage.py`
* Makes `find_password()` callable from UI
* Creates a **one-way dependency**

UI → Storage
Storage → nothing

---

## 10. `on_find()` in `ui.py` — event handler

### Function role

```python
def on_find():
    """
    Finds password for the given website.
    """
```

This function:

* Responds to a button click
* Talks to UI widgets
* Calls storage functions
* Displays results

---

## 11. Reading user input from UI

```python
website = website_entry.get()
```

### What happens

* Reads text entered by user
* Returns a string

This is **UI responsibility only**.

---

## 12. Input validation (early exit)

```python
if not website:
    custom_popup(window, "Error", "Please enter a website")
    return
```

### Why this is important

* Prevents useless file access
* Prevents false errors
* Improves UX

This is **guard clause design**.

---

## 13. Calling storage logic

```python
email, password = find_password(website)
```

### Data flow at this moment

```
UI → storage.find_password()
        ↓
     JSON file
        ↓
     Python dict
        ↓
     tuple (email, password)
        ↓
       UI
```

UI does not care **how** storage works.

---

## 14. Handling “not found” result

```python
if email is None and password is None:
    custom_popup(window, "Error", "Password not found")
    return
```

### Why this check works

Because storage guarantees:

* Either valid `(email, password)`
* Or `(None, None)`

Clear contract = clean UI logic.

---

## 15. Successful result handling

```python
password_entry.delete(0, tk.END)
password_entry.insert(0, password)
```

### Why delete first

Tkinter entry fields:

* Do not overwrite automatically
* Must be cleared before inserting new text

---

### Same for username

```python
username_entry.delete(0, tk.END)
username_entry.insert(0, email)
```

---

## 16. Success popup

```python
custom_popup(
    window,
    "Success",
    "Your credentials are :\n\n"
    f"Email: {email}\nPassword: {password}"
)
```

### Responsibility

* UI feedback
* Human-readable message
* No logic, only presentation

---

## 17. Button connection (event binding)

```python
tk.Button(
    window,
    text="Find Password",
    command=on_find
).grid(row=1, column=2, columnspan=1, padx=5, sticky="ew")
```

### What actually happens

1. Button is rendered
2. User clicks it
3. Tkinter calls `on_find`
4. `on_find`:

   * Reads input
   * Calls storage
   * Updates UI

This is **event-driven programming**.

---

## 18. Full execution timeline (end-to-end)

```
User types website
        ↓
User clicks "Find Password"
        ↓
Tkinter triggers on_find()
        ↓
UI validates input
        ↓
find_password(website) called
        ↓
JSON file read
        ↓
Data searched
        ↓
(email, password) returned
        ↓
UI updates fields
        ↓
Popup shown
```

---

## 19. Why this design is correct and scalable

| Aspect                 | Why it’s good               |
| ---------------------- | --------------------------- |
| Separation of concerns | UI ≠ Storage                |
| Error containment      | Storage absorbs file errors |
| Clear contracts        | `(None, None)`              |
| No UI logic in storage | Testable                    |
| No file logic in UI    | Maintainable                |

---

## 20. Final mental model

> UI **asks questions**
> Storage **answers safely**
> UI **decides what to show**

This is **clean architecture**, not beginner scripting.
