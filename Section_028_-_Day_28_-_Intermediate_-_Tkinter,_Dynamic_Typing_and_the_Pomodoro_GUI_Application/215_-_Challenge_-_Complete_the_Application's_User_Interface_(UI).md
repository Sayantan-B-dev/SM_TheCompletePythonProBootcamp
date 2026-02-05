## Complete Pomodoro UI — Structured, Clean, Production-Ready

---

## UI Goal

A **Pomodoro Timer interface** with:

* Title header
* Central tomato graphic with countdown text
* Start / Reset controls
* Progress indicator (check marks)
* Consistent spacing, alignment, and theming

This section focuses **only on UI**, not timer logic.

---

## Layout Strategy (Grid Mental Model)

```
┌───────────────┐
│     Timer     │  → row 0
├───────────────┤
│   🍅 00:00    │  → row 1
├───────────────┤
│ Start  Reset  │  → row 2
├───────────────┤
│     ✓✓        │  → row 3
└───────────────┘
```

* **Column 1** → main vertical axis
* **Column 0 & 2** → buttons
* Padding handled at `window` level

---

## Color & Font Constants

```python
# -------------------------
# CONSTANTS (UI THEME)
# -------------------------

YELLOW = "#f7f5dd"
GREEN = "#9bdeac"
RED = "#e7305b"
FONT_NAME = "Courier"
```

Why:

* Centralized theme control
* Easy UI refactoring
* Prevents magic values

---

## Complete UI Code (Clean + Commented)

```python
import tkinter as tk

# -------------------------
# CONSTANTS
# -------------------------

YELLOW = "#f7f5dd"
GREEN = "#9bdeac"
RED = "#e7305b"
FONT_NAME = "Courier"

# -------------------------
# WINDOW SETUP
# -------------------------

window = tk.Tk()

# Window title shown in OS bar
window.title("Pomodoro")

# Padding adds space around all grid widgets
# Background color applies to entire window
window.config(
    padx=100,
    pady=50,
    bg=YELLOW
)

# -------------------------
# TITLE LABEL
# -------------------------

title_label = tk.Label(
    text="Timer",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 50, "bold")
)

# Centered at top
title_label.grid(column=1, row=0)

# -------------------------
# CANVAS (TOMATO + TIMER)
# -------------------------

canvas = tk.Canvas(
    width=200,
    height=224,
    bg=YELLOW,
    highlightthickness=0  # Removes focus border
)

# IMPORTANT: Image must be stored in a variable
# or it will be garbage collected and disappear
tomato_img = tk.PhotoImage(file="tomato.png")

# Place image at canvas center
canvas.create_image(
    100,
    112,
    image=tomato_img
)

# Timer text layered on top of image
timer_text = canvas.create_text(
    100,
    130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)

canvas.grid(column=1, row=1)

# -------------------------
# START BUTTON
# -------------------------

start_button = tk.Button(
    text="Start",
    highlightthickness=0,
    borderwidth=2
)

start_button.grid(column=0, row=2)

# -------------------------
# RESET BUTTON
# -------------------------

reset_button = tk.Button(
    text="Reset",
    highlightthickness=0,
    borderwidth=2
)

reset_button.grid(column=2, row=2)

# -------------------------
# CHECK MARKS (PROGRESS)
# -------------------------

check_marks = tk.Label(
    text="",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 20, "bold")
)

check_marks.grid(column=1, row=3)

# -------------------------
# MAIN LOOP
# -------------------------

window.mainloop()
```

---

## Canvas Layering Explained

| Layer  | Element           |
| ------ | ----------------- |
| Bottom | Canvas background |
| Middle | Tomato image      |
| Top    | Timer text        |

Canvas draws **in creation order**, later items appear on top.

---

## Why Canvas Is Used Here (Not Label)

| Requirement          | Label   | Canvas |
| -------------------- | ------- | ------ |
| Image + Text overlay | No      | Yes    |
| Precise positioning  | Limited | Exact  |
| Animations           | No      | Yes    |
| Layer control        | No      | Yes    |

---

## UI-Only Responsibilities (Separated Cleanly)

| Component | Responsibility     |
| --------- | ------------------ |
| `Label`   | Static text        |
| `Canvas`  | Visual composition |
| `Button`  | User actions       |
| `window`  | Layout + theme     |

No logic mixed into UI.

---

## Expected Visual Output

```
[ Pomodoro Window ]

           Timer

        🍅  00:00

   [ Start ]     [ Reset ]

             ✓✓
```

* Yellow background
* Green title
* Tomato centered
* White timer text over image
* Balanced spacing

---

## UI Is Now Ready For Logic Injection

Timer logic will later:

* Update `timer_text` using `canvas.itemconfig`
* Modify `title_label` color/text
* Append ✓ to `check_marks`
* Disable / enable buttons

The UI structure already supports all of that without changes.
