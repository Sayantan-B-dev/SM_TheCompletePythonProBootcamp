# PASSWORD MANAGER — FULL PROJECT DOCUMENTATION

**Modular Architecture • Event-Driven Flow • Heavily Commented Code**

---

## 1. PROJECT OVERVIEW

This project is a **desktop password manager** built with **Tkinter**, designed to demonstrate:

* Event-driven GUI programming
* Secure password generation
* Modal dialog control (custom message boxes)
* Clean separation of concerns via modular files
* Predictable data flow from UI → logic → storage

The application allows the user to:

* Generate strong passwords
* Enter website, email, password
* Review details via a custom modal popup
* Save credentials to a file safely

---

## 2. DIRECTORY STRUCTURE (FINAL)

```
password_manager/
│
├── main.py
├── ui.py
├── password_generator.py
├── dialogs.py
├── storage.py
├── utils.py
│
├── assets/
│   └── logo.png
│
└── data/
    └── passwords.txt
```

Each file has **one responsibility**.

---

## 3. EXECUTION FLOW (HIGH LEVEL)

```
main.py
   ↓
create Tk window
   ↓
build_ui()
   ↓
user interacts with UI
   ↓
button click → callback
   ↓
password generation / popup / save
```

---

## 4. FILE-BY-FILE DOCUMENTATION + FULL CODE

---

## `password_generator.py`

### Responsibility: **Password generation only**

```python
# password_generator.py

import secrets
import string

# Safe symbols explicitly chosen to avoid shell / file issues
SAFE_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

def generate_strong_password(length=16):
    """
    Generates a cryptographically secure password.

    Why this function exists:
    - Centralizes password logic
    - Keeps UI free from security logic
    - Easy to test independently

    Security guarantees:
    - Uses `secrets` (not random)
    - Ensures at least:
        • one letter
        • one digit
        • one symbol
    """

    # Enforce minimum length for security
    if length < 12:
        raise ValueError("Password length should be at least 12")

    # Character pools
    letters = string.ascii_letters
    digits = string.digits
    symbols = SAFE_SYMBOLS

    # Force minimum complexity first
    password_chars = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Combine all pools for remaining characters
    all_chars = letters + digits + symbols

    # Fill remaining length with random secure choices
    for _ in range(length - 3):
        password_chars.append(secrets.choice(all_chars))

    # Shuffle to remove predictable positions
    secrets.SystemRandom().shuffle(password_chars)

    # Convert list of characters to string
    return ''.join(password_chars)
```

---

## `dialogs.py`

### Responsibility: **Custom modal dialogs**

```python
# dialogs.py

import tkinter as tk

def custom_popup(parent, title, message):
    """
    Displays a modal confirmation dialog.

    Why custom instead of messagebox:
    - Full layout control
    - Multi-line previews
    - Custom styling
    - Predictable return value

    Returns:
        True  → OK clicked
        False → Cancel / close
    """

    # Mutable container to allow modification from nested functions
    result = {"value": False}

    # Create a new dialog window
    popup = tk.Toplevel(parent)

    # Set window properties
    popup.title(title)
    popup.transient(parent)   # Keep above parent
    popup.grab_set()          # Block parent interaction
    popup.resizable(False, False)

    # Message label (supports multi-line text)
    tk.Label(
        popup,
        text=message,
        justify="left",
        padx=20,
        pady=20
    ).pack()

    # Button container
    button_frame = tk.Frame(popup)
    button_frame.pack(pady=10)

    # OK callback
    def on_ok():
        result["value"] = True
        popup.destroy()

    # Cancel callback
    def on_cancel():
        popup.destroy()

    # Buttons
    tk.Button(button_frame, text="OK", width=10, command=on_ok)\
        .pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel)\
        .pack(side="left", padx=5)

    # ---- CENTER POPUP OVER PARENT ----
    popup.update_idletasks()

    px, py = parent.winfo_x(), parent.winfo_y()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    w, h = popup.winfo_width(), popup.winfo_height()

    popup.geometry(
        f"{w}x{h}+{px + pw//2 - w//2}+{py + ph//2 - h//2}"
    )
    # ---------------------------------

    # Pause execution until popup closes
    parent.wait_window(popup)

    # Return user decision
    return result["value"]
```

---

## `storage.py`

### Responsibility: **Persistent storage**

```python
# storage.py

# Centralized file path
DATA_FILE = "data/passwords.txt"

def save_credentials(website, username, password):
    """
    Saves credentials to a local file.

    Design choice:
    - Plain text for learning clarity
    - Easy to migrate to encryption or database later
    """

    # Append mode ensures no overwriting
    with open(DATA_FILE, "a") as file:
        file.write(f"{website} | {username} | {password}\n")
```

---

## `utils.py`

### Responsibility: **Shared helper utilities**

```python
# utils.py

def center_window(win):
    """
    Centers a Tkinter window on the screen.

    Why needed:
    - Tkinter does not auto-center windows
    - Improves UX consistency
    """

    # Ensure geometry is calculated
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate centered position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")
```

---

## `ui.py`

### Responsibility: **UI creation + event wiring**

```python
# ui.py

import tkinter as tk

from password_generator import generate_strong_password
from dialogs import custom_popup
from storage import save_credentials

def build_ui(window):
    """
    Builds the entire user interface.

    This function:
    - Creates widgets
    - Places them using grid
    - Binds buttons to callbacks
    """

    # Window configuration
    window.title("Password Manager")
    window.config(padx=40, pady=40)

    # Grid weights for responsive layout
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    window.columnconfigure(2, weight=1)

    # -------- LOGO --------
    canvas = tk.Canvas(window, width=200, height=200, highlightthickness=0)
    logo_img = tk.PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.image = logo_img   # Prevent garbage collection
    canvas.grid(row=0, column=1, pady=(0, 20))
    # ----------------------

    # Labels
    tk.Label(window, text="Website:").grid(row=1, column=0, sticky="w")
    tk.Label(window, text="Username / Email:").grid(row=2, column=0, sticky="w")
    tk.Label(window, text="Password:").grid(row=3, column=0, sticky="w")

    # Entry fields
    website_entry = tk.Entry(window)
    website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
    website_entry.focus()

    username_entry = tk.Entry(window)
    username_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
    username_entry.insert(0, "example@email.com")

    password_entry = tk.Entry(window)
    password_entry.grid(row=3, column=1, sticky="ew")

    # -------- CALLBACKS --------
    def on_generate():
        """
        Generates password and inserts it into password entry.
        """
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generate_strong_password())

    def on_save():
        """
        Validates input, shows confirmation popup,
        and saves credentials if confirmed.
        """

        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # Validation popup
        if not website or not username or not password:
            custom_popup(window, "Error", "Please fill in all fields")
            return

        # Confirmation popup
        confirm = custom_popup(
            window,
            website,
            f"""These are the details entered:

Website : {website}
Email   : {username}
Password: {password}

Is it ok to save?"""
        )

        # Save only if confirmed
        if confirm:
            save_credentials(website, username, password)

            # Clear fields after save
            website_entry.delete(0, tk.END)
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    # ---------------------------

    # Buttons
    tk.Button(
        window,
        text="Generate Password",
        command=on_generate
    ).grid(row=3, column=2, padx=5, sticky="ew")

    tk.Button(
        window,
        text="Add to Vault",
        command=on_save
    ).grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")
```

---

## `main.py`

### Responsibility: **Application entry point**

```python
# main.py

import tkinter as tk
from ui import build_ui
from utils import center_window

# Create main application window
window = tk.Tk()

# Hide window until fully built
window.withdraw()

# Build UI components
build_ui(window)

# Center window on screen
center_window(window)

# Show window
window.deiconify()

# Start Tkinter event loop
window.mainloop()
```

---

## 5. OVERALL FLOW SUMMARY (FINAL)

```
User opens app
   ↓
UI loads (ui.py)
   ↓
User clicks button
   ↓
Callback executes
   ↓
Password generated OR popup shown
   ↓
User confirms
   ↓
Data saved (storage.py)
```

---

## 6. WHY THIS DESIGN IS CORRECT

* UI logic ≠ security logic
* Modal dialogs enforce user intent
* Event callbacks keep flow predictable
* Files are readable in isolation
* Project is extensible (encryption, DB, search, edit)

This documentation + codebase is **complete, readable, and production-grade for learning and extension**.
