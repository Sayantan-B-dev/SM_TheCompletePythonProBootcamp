## What This Program Is Demonstrating (Widget Map)

This single script is a **catalog of core Tkinter input/output widgets**.
Each widget demonstrates **one interaction pattern** used in real GUI apps.

| Widget        | Role              | Interaction Type  |
| ------------- | ----------------- | ----------------- |
| `Label`       | Display           | Output only       |
| `Button`      | Action trigger    | Click event       |
| `Entry`       | Single-line input | Text input        |
| `Text`        | Multi-line input  | Text input        |
| `Spinbox`     | Numeric selection | Incremental input |
| `Scale`       | Range selection   | Continuous input  |
| `Checkbutton` | Boolean toggle    | On / Off          |
| `Radiobutton` | Exclusive choice  | One-of-many       |
| `Listbox`     | Selection list    | Item selection    |

---

## Window (Root Container)

```python
window = Tk()
window.title("Widget Examples")
window.minsize(width=500, height=500)
```

**What it does**

* Creates the **root application window**
* Owns all widgets
* Controls:

  * Event loop
  * Geometry
  * Focus

Without this, no widget can exist.

---

## 1. `Label` — Display-Only Output

```python
label = Label(text="This is old text")
label.config(text="This is new text")
label.pack()
```

### What a Label Is

* A **read-only display widget**
* Shows:

  * Text
  * Images
  * Status messages

### Key Methods

| Method              | Meaning         |
| ------------------- | --------------- |
| `Label(text=...)`   | Initial text    |
| `.config(text=...)` | Update text     |
| `.pack()`           | Place on window |

### Real Use Cases

* Titles
* Instructions
* Status messages
* Error messages

---

## 2. `Button` — Event Trigger

```python
def action():
    print("Do something")

button = Button(text="Click Me", command=action)
button.pack()
```

### How Buttons Work

```text
User clicks
↓
Tkinter detects click
↓
command function executes
```

### Important Rules

* `command=action` → **no parentheses**
* Button **does not return values**
* Logic lives in the callback

### Real Use Cases

* Submit
* Save
* Delete
* Increment counters
* Navigation

---

## 3. `Entry` — Single-Line Text Input

```python
entry = Entry(width=30)
entry.insert(END, string="Some text to begin with.")
print(entry.get())
entry.pack()
```

### Entry Characteristics

* One-line input only
* Always returns a **string**

### Key Methods

| Method      | Purpose   |
| ----------- | --------- |
| `.get()`    | Read text |
| `.insert()` | Pre-fill  |
| `.delete()` | Clear     |

### Real Use Cases

* Username
* Password
* Search bar
* Short commands

---

## 4. `Text` — Multi-Line Text Input

```python
text = Text(height=5, width=30)
text.focus()
text.insert(END, "Example of multi-line text entry.")
print(text.get("1.0", END))
text.pack()
```

### What Makes `Text` Different from `Entry`

| Entry       | Text               |
| ----------- | ------------------ |
| Single-line | Multi-line         |
| Simple      | Rich control       |
| `.get()`    | `.get(start, end)` |

### Position Syntax

```text
"line.character"
"1.0" → first line, first character
END → end of content
```

### Real Use Cases

* Notes
* Comments
* Logs
* Editors

---

## 5. `Spinbox` — Bounded Numeric Input

```python
spinbox = Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.pack()
```

### How Spinbox Works

* User clicks arrows or types
* Value always within range
* Value is returned as **string**

### Common Use Cases

* Age
* Quantity
* Rating
* Steps / repetitions

---

## 6. `Scale` — Continuous Range Selector

```python
scale = Scale(from_=0, to=100, command=scale_used)
scale.pack()
```

### Scale Behavior

* Slider-based input
* Callback fires **on every movement**
* Value passed as parameter

### Real Use Cases

* Volume
* Brightness
* Progress
* Sensitivity controls

---

## 7. `Checkbutton` — Boolean Toggle

```python
checked_state = IntVar()
checkbutton = Checkbutton(
    text="Is On?",
    variable=checked_state,
    command=checkbutton_used
)
checkbutton.pack()
```

### Why `IntVar` Is Required

* Widgets cannot store state alone
* `IntVar` acts as a **shared state container**

| Value | Meaning |
| ----- | ------- |
| `0`   | Off     |
| `1`   | On      |

### Real Use Cases

* Enable feature
* Accept terms
* Remember settings

---

## 8. `Radiobutton` — One-Of-Many Choice

```python
radio_state = IntVar()

Radiobutton(text="Option1", value=1, variable=radio_state)
Radiobutton(text="Option2", value=2, variable=radio_state)
```

### How Radio Buttons Work

* All radio buttons share **one variable**
* Each has a unique `value`
* Only one can be selected

### Real Use Cases

* Gender selection
* Payment method
* Mode selection

---

## 9. `Listbox` — Select from a List

```python
listbox = Listbox(height=len(fruits))
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()
```

### Key Concepts

| Feature             | Meaning         |
| ------------------- | --------------- |
| `.insert()`         | Add item        |
| `.curselection()`   | Selected index  |
| `.get(index)`       | Get value       |
| `<<ListboxSelect>>` | Selection event |

### Event Binding vs `command`

* `Listbox` uses **events**, not `command`
* Selection triggers event object

### Real Use Cases

* Menus
* File lists
* Options panel
* Category selection

---

## Critical Patterns You Just Learned

### 1. Widgets Do Not Store Logic

Logic always lives in **functions**.

---

### 2. Widgets Do Not Store State (Directly)

State is held using:

* `IntVar`
* `StringVar`
* `DoubleVar`
* `BooleanVar`

---

### 3. GUI Is Event-Driven

```text
No loop
No polling
Only callbacks
```

---

## Common Beginner Mistakes (Avoid)

| Mistake                      | Why It Breaks             |
| ---------------------------- | ------------------------- |
| Using `command=action()`     | Function runs immediately |
| Expecting return values      | Callbacks return nothing  |
| Using globals everywhere     | Poor scalability          |
| Mixing `pack()` and `grid()` | Runtime error             |

---
