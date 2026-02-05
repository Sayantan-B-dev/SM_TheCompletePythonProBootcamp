## `Canvas` Widget — Complete, Practical Documentation

---

## What the `Canvas` Widget Is

The `Canvas` widget is a **2D drawing surface** in Tkinter designed for **free-form graphics, positioning, animation, and visual composition**. Unlike layout-driven widgets (`Label`, `Button`), `Canvas` is **coordinate-based**.

> Everything on a Canvas is an **item** with an **ID**, not a widget.

---

## Basic Construction

```python
canvas = tk.Canvas(
    master,
    width=200,
    height=224,
    bg="yellow",
    highlightthickness=0
)
canvas.pack()
```

---

## Core Canvas Configuration Options

| Option               | Purpose            | Typical Use               |
| -------------------- | ------------------ | ------------------------- |
| `width`              | Canvas width (px)  | Fixed drawing area        |
| `height`             | Canvas height (px) | Fixed drawing area        |
| `bg`                 | Background color   | Visual theme              |
| `highlightthickness` | Focus border       | Set `0` to remove outline |
| `bd`                 | Border width       | Subtle framing            |
| `relief`             | Border style       | `flat`, `ridge`, `sunken` |
| `cursor`             | Mouse cursor       | Drawing / dragging apps   |
| `scrollregion`       | Virtual area       | Scrollable canvases       |

---

## Coordinate System (Critical Concept)

* Origin `(0, 0)` → **top-left**
* X increases → right
* Y increases → down

```
(0,0) ─────────► X
  │
  │
  ▼
  Y
```

---

## Canvas Items (What You Can Draw)

Canvas supports **items**, not widgets.

| Item Type     | Function             |
| ------------- | -------------------- |
| Line          | `create_line()`      |
| Rectangle     | `create_rectangle()` |
| Oval / Circle | `create_oval()`      |
| Polygon       | `create_polygon()`   |
| Arc           | `create_arc()`       |
| Text          | `create_text()`      |
| Image         | `create_image()`     |
| Window        | `create_window()`    |

Each returns an **item ID**.

---

## `create_image()` — Images on Canvas

```python
image = tk.PhotoImage(file="tomato.png")

image_id = canvas.create_image(
    100, 112,
    image=image,
    anchor="center"
)
```

### Arguments

| Argument | Meaning               |
| -------- | --------------------- |
| `x, y`   | Placement coordinates |
| `image`  | `PhotoImage` object   |
| `anchor` | Reference point       |

### Anchor Values

| Anchor             | Meaning            |
| ------------------ | ------------------ |
| `center`           | Centered (default) |
| `nw`               | Top-left           |
| `ne`               | Top-right          |
| `sw`               | Bottom-left        |
| `se`               | Bottom-right       |
| `n`, `s`, `e`, `w` | Edge-aligned       |

> Always keep a reference to `PhotoImage` or it will disappear due to garbage collection.

---

## `create_text()` — Text Rendering

```python
text_id = canvas.create_text(
    100, 130,
    text="00:00",
    font=("Arial", 35, "bold"),
    fill="white",
    anchor="center"
)
```

### Text Properties

| Option    | Purpose                   |
| --------- | ------------------------- |
| `text`    | Displayed string          |
| `font`    | `(family, size, style)`   |
| `fill`    | Text color                |
| `anchor`  | Alignment                 |
| `width`   | Line wrap width           |
| `justify` | `left`, `center`, `right` |

---

## Shape Drawing Functions

### Lines

```python
line_id = canvas.create_line(
    10, 10, 190, 10,
    fill="black",
    width=3,
    dash=(4, 2)
)
```

### Rectangles

```python
rect_id = canvas.create_rectangle(
    20, 20, 180, 100,
    fill="blue",
    outline="white",
    width=2
)
```

### Ovals / Circles

```python
oval_id = canvas.create_oval(
    50, 50, 150, 150,
    fill="red"
)
```

---

## Styling Options (Universal to Shapes)

| Option    | Applies To       | Purpose                        |
| --------- | ---------------- | ------------------------------ |
| `fill`    | Shapes / text    | Interior color                 |
| `outline` | Shapes           | Border color                   |
| `width`   | Lines / outlines | Thickness                      |
| `dash`    | Lines            | Dashed effect                  |
| `stipple` | Shapes           | Pattern fill                   |
| `state`   | All              | `normal`, `hidden`, `disabled` |

---

## Item Manipulation (Most Important API)

### Move Items

```python
canvas.move(item_id, dx=5, dy=0)
```

Moves relative to current position.

---

### Set Absolute Position

```python
canvas.coords(item_id, new_x, new_y)
```

For shapes, requires full coordinate set.

---

### Change Item Properties

```python
canvas.itemconfig(
    text_id,
    text="01:25",
    fill="green"
)
```

---

### Read Properties

```python
current_text = canvas.itemcget(text_id, "text")
```

---

## Tags — Grouping & Control System

Tags allow **bulk control**.

```python
canvas.create_rectangle(..., tags=("box", "ui"))
```

### Use Tags

```python
canvas.itemconfig("box", fill="red")
canvas.move("ui", 10, 0)
canvas.delete("box")
```

---

## Event Binding on Canvas Items

```python
def on_click(event):
    print(event.x, event.y)

canvas.bind("<Button-1>", on_click)
```

### Item-Specific Binding

```python
canvas.tag_bind(
    item_id,
    "<Button-1>",
    handler
)
```

---

## Mouse & Keyboard Events

| Event         | Trigger           |
| ------------- | ----------------- |
| `<Button-1>`  | Left click        |
| `<Button-3>`  | Right click       |
| `<B1-Motion>` | Drag              |
| `<Motion>`    | Mouse move        |
| `<KeyPress>`  | Key pressed       |
| `<Enter>`     | Mouse enters item |
| `<Leave>`     | Mouse leaves item |

---

## Animation Pattern (Correct Way)

Canvas does **manual animation**.

```python
def animate():
    canvas.move(ball, 2, 0)
    window.after(16, animate)  # ~60 FPS

animate()
```

---

## Scrollable Canvas (Advanced Use)

```python
canvas.configure(scrollregion=canvas.bbox("all"))
```

Combined with `Scrollbar`.

---

## Embedding Widgets Inside Canvas

```python
button = tk.Button(text="Click")

canvas.create_window(
    100, 100,
    window=button
)
```

Used for:

* Custom layouts
* Visual editors
* Node graphs

---

## Z-Order Control (Layering)

```python
canvas.tag_raise(item_id)
canvas.tag_lower(item_id)
```

---

## Deleting Items

```python
canvas.delete(item_id)
canvas.delete("all")
```

---

## Performance Considerations

| Issue              | Explanation                      |
| ------------------ | -------------------------------- |
| Too many items     | Canvas slows beyond ~10k objects |
| Frequent redraws   | Prefer `move()` over recreate    |
| Large images       | Resize beforehand                |
| Complex animations | Use low FPS                      |

---

## Common Mistakes

| Mistake                     | Result           |
| --------------------------- | ---------------- |
| Image not referenced        | Image disappears |
| Blocking loop               | UI freezes       |
| Using `place` inside canvas | Redundant        |
| Overusing redraw            | Performance drop |

---

## Real-World Use Cases

* Timers & clocks (like Pomodoro)
* Game boards
* Drawing apps
* Visual simulations
* Flowcharts
* Custom charts
* Drag-and-drop systems
* Mini game engines

---

## Mental Model

> Canvas is a **pixel-precise scene graph**, not a layout manager.

You control **what**, **where**, and **when**—manually.

---

## Minimal Example (Your Code Refined)

```python
import tkinter as tk

FONT_NAME = "Arial"

window = tk.Tk()

canvas = tk.Canvas(
    window,
    width=200,
    height=224,
    bg="yellow",
    highlightthickness=0
)

image = tk.PhotoImage(file="tomato.png")

canvas.create_image(100, 112, image=image)
canvas.create_text(
    100, 130,
    text="00:00",
    font=(FONT_NAME, 35, "bold"),
    fill="white"
)

canvas.pack()
window.mainloop()
```

### Expected Output

```
A yellow window showing a tomato image centered
with white bold timer text below it.
```
