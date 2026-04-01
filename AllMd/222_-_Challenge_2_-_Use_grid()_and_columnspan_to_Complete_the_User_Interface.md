## `grid()` — DEFINITION (FOUNDATION)

`grid()` is a **geometry manager** in Tkinter that places widgets in a **2D table-like layout** using rows and columns.

Each widget is positioned by:

* `row`
* `column`
* optional layout controls like `columnspan`, `rowspan`, `sticky`, `padx`, `pady`, `weight`

Think of `grid()` as an **invisible spreadsheet**.

---

## CORE MENTAL MODEL

```
Column →   0        1        2        3
        ┌────────┬────────┬────────┬────────┐
Row 0   │        │        │        │        │
        ├────────┼────────┼────────┼────────┤
Row 1   │        │        │        │        │
        ├────────┼────────┼────────┼────────┤
Row 2   │        │        │        │        │
        └────────┴────────┴────────┴────────┘
```

Widgets **occupy cells** — or **merge cells**.

---

## BASIC GRID USAGE

```python
label = tk.Label(window, text="Username")
label.grid(row=0, column=0)
```

### Output (conceptual)

```
[ Username ]
```

---

## COLUMN SPAN — DEFINITION

`columnspan` allows a widget to **span across multiple columns**, merging them horizontally.

### Why it exists

* Headers
* Wide inputs
* Buttons that stretch
* Logos

---

## COLUMN SPAN — SIMPLE EXAMPLE

```python
title = tk.Label(
    window,
    text="PASSWORD MANAGER",
    font=("Arial", 16, "bold")
)

title.grid(row=0, column=0, columnspan=3)
```

### Output (ASCII)

```
┌──────────────────────────────┐
│        PASSWORD MANAGER       │
└──────────────────────────────┘
```

---

## ROW SPAN — DEFINITION

`rowspan` allows a widget to **occupy multiple rows vertically**.

### Use cases

* Sidebars
* Logos
* Vertical menus

---

## ROW SPAN — SIMPLE EXAMPLE

```python
logo = tk.Label(window, text="[ LOGO ]")
logo.grid(row=1, column=0, rowspan=3)
```

### Output (ASCII)

```
┌──────────┬──────────────┐
│ [ LOGO ] │ Username     │
│          ├──────────────┤
│          │ Password     │
│          ├──────────────┤
│          │ Login Btn    │
└──────────┴──────────────┘
```

---

## STICKY — DEFINITION (MOST IMPORTANT)

By default, widgets **float centered** in a grid cell.

`sticky` tells widgets **which direction to stretch**.

| Value  | Meaning        |
| ------ | -------------- |
| `n`    | north (top)    |
| `s`    | south (bottom) |
| `e`    | east (right)   |
| `w`    | west (left)    |
| `nsew` | stretch fully  |

---

## STICKY — EXAMPLE

```python
entry = tk.Entry(window)
entry.grid(row=1, column=1, sticky="ew")
```

### Output Behavior

```
Entry stretches horizontally to fill cell
```

---

## PADDING — DEFINITION

| Parameter | Scope                       |
| --------- | --------------------------- |
| `padx`    | external horizontal spacing |
| `pady`    | external vertical spacing   |
| `ipadx`   | internal horizontal padding |
| `ipady`   | internal vertical padding   |

---

## PADDING — EXAMPLE

```python
btn = tk.Button(window, text="Save")
btn.grid(row=3, column=1, pady=10, ipadx=20)
```

### Visual Effect

```
Button becomes wider and spaced nicely
```

---

## GRID WEIGHT — DEFINITION (RESPONSIVE UI)

Grid cells **do not expand automatically**.

You must assign **weight** to rows/columns.

```python
window.columnconfigure(1, weight=1)
```

### Meaning

> Column 1 grows when window resizes

---

## WEIGHT — EXAMPLE

```python
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)
```

### Behavior

```
Column 1 grows 3× faster than column 0
```

---

## ALIGNMENT EXAMPLE — LOGIN FORM (BAD VS GOOD)

### BAD (no grid control)

```
[User:] [____]
[Pwd :] [____]
[Login]
```

### GOOD (aligned, spaced)

```
┌──────────┬──────────────────┐
│ Username │ [______________] │
│ Password │ [______________] │
│          │     [ Login ]     │
└──────────┴──────────────────┘
```

---

## REALISTIC UI — PASSWORD MANAGER FORM

### LAYOUT PLAN (ASCII)

```
┌────────────────────────────────────────┐
│            PASSWORD MANAGER             │  ← columnspan=3
├──────────┬─────────────────────────────┤
│ Website  │ [_________________________] │
├──────────┼─────────────────────────────┤
│ Email    │ [_________________________] │
├──────────┼─────────────────────────────┤
│ Password │ [_________________________] │
├──────────┼─────────────┬───────────────┤
│          │ [ Generate ]│ [ Save ]      │
└──────────┴─────────────┴───────────────┘
```

---

## REALISTIC CODE — FULL EXAMPLE

```python
import tkinter as tk

window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Make column 1 expandable
window.columnconfigure(1, weight=1)

# Title
title = tk.Label(
    window,
    text="PASSWORD MANAGER",
    font=("Arial", 16, "bold")
)
title.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# Labels
tk.Label(window, text="Website").grid(row=1, column=0, sticky="e")
tk.Label(window, text="Email").grid(row=2, column=0, sticky="e")
tk.Label(window, text="Password").grid(row=3, column=0, sticky="e")

# Entries
website_entry = tk.Entry(window)
website_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)

email_entry = tk.Entry(window)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)

password_entry = tk.Entry(window)
password_entry.grid(row=3, column=1, sticky="ew", padx=5)

# Buttons
generate_btn = tk.Button(window, text="Generate")
generate_btn.grid(row=3, column=2, padx=5)

save_btn = tk.Button(window, text="Save", width=20)
save_btn.grid(row=4, column=1, columnspan=2, pady=15)

window.mainloop()
```

---

## EXPECTED UI BEHAVIOR

* Title centered across full width
* Inputs stretch when window resizes
* Labels right-aligned
* Buttons aligned and spaced
* Professional, balanced layout

---

## GRID RULES (NON-NEGOTIABLE)

1. **Never mix `pack()` and `grid()` in the same container**
2. Use `sticky="ew"` for entries
3. Use `columnspan` for width, not empty columns
4. Always assign `weight` for responsive layouts
5. Think in tables, not pixels
