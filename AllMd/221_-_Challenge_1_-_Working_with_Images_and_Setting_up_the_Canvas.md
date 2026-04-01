## `tk.Canvas` — COMPLETE METHOD & USAGE BREAKDOWN

---

## 1. What `Canvas` Is (Conceptual Role)

`Canvas` is a **2D drawing surface** in Tkinter used for:

* Drawing shapes
* Rendering images
* Displaying text
* Handling coordinates and layers
* Creating interactive graphics

Unlike `Label`, a `Canvas` is **stateful** and **item-based**.
Each drawn object becomes an **item** with an ID that can be modified later.

---

## 2. Creating a Canvas (Base Syntax)

```python
canvas = tk.Canvas(
    master=window,       # Parent widget
    width=200,            # Canvas width in pixels
    height=200,           # Canvas height in pixels
    bg="white",           # Background color
    highlightthickness=0  # Removes border
)
canvas.pack()
```

---

## 3. Coordinate System (VERY IMPORTANT)

Canvas uses a **top-left origin (0,0)**

```
(0,0) ───────────▶ x
  │
  │
  ▼
  y
```

* x increases → right
* y increases → downward

---

## 4. Core Drawing Methods

### 4.1 `create_line()`

```python
line_id = canvas.create_line(
    20, 20, 180, 20,
    fill="black",
    width=2
)
```

**What it does**

* Draws a straight line from `(x1, y1)` to `(x2, y2)`
* Returns an **item ID**

**Expected Output**

```
A horizontal line near the top of the canvas
```

---

### 4.2 `create_rectangle()`

```python
rect_id = canvas.create_rectangle(
    50, 50, 150, 120,
    outline="blue",
    width=2,
    fill="lightblue"
)
```

**Coordinates**

* `(x1, y1)` → top-left
* `(x2, y2)` → bottom-right

**Expected Output**

```
A filled rectangle with blue border
```

---

### 4.3 `create_oval()` (Circles & Ellipses)

```python
oval_id = canvas.create_oval(
    50, 50, 150, 150,
    fill="red"
)
```

**Rule**

* Bounding box defines the shape
* Perfect circle if width == height

**Expected Output**

```
A red circle
```

---

### 4.4 `create_polygon()`

```python
poly_id = canvas.create_polygon(
    100, 20,
    180, 180,
    20, 180,
    fill="green"
)
```

**Use Case**

* Arbitrary shapes
* Icons, arrows, stars

---

## 5. Text Rendering

### 5.1 `create_text()`

```python
text_id = canvas.create_text(
    100, 100,
    text="Password Manager",
    font=("Arial", 12, "bold"),
    fill="black"
)
```

**Anchor**

* Default anchor = center
* Can use `anchor="nw"`, `"ne"`, etc.

**Expected Output**

```
Centered text inside canvas
```

---

## 6. Images on Canvas (Your Code Context)

```python
logo_img = tk.PhotoImage(file="logo.png")

image_id = canvas.create_image(
    100, 100,
    image=logo_img
)
```

### CRITICAL RULE

> **Keep a reference to the image object**
> Otherwise Python garbage-collects it and image disappears.

Correct:

```python
canvas.image = logo_img
```

---

## 7. Item IDs (Core Concept)

Every `create_*()` method returns an **item ID**

```python
item_id = canvas.create_rectangle(...)
```

Item IDs allow:

* Moving
* Deleting
* Modifying
* Layering

---

## 8. Modifying Canvas Items

### 8.1 `itemconfig()` (Change Properties)

```python
canvas.itemconfig(
    rect_id,
    fill="yellow",
    outline="black"
)
```

---

### 8.2 `coords()` (Move or Reshape)

```python
canvas.coords(
    rect_id,
    60, 60, 160, 130
)
```

**Effect**

```
Rectangle moves to new position
```

---

### 8.3 `move()` (Relative Movement)

```python
canvas.move(
    rect_id,
    10,   # x offset
    20    # y offset
)
```

---

## 9. Layer Control (Z-Index)

### 9.1 Bring Forward / Send Back

```python
canvas.tag_raise(item_id)
canvas.tag_lower(item_id)
```

---

## 10. Tags (VERY POWERFUL)

Tags group items together.

```python
canvas.create_rectangle(10, 10, 50, 50, tags="box")
canvas.create_rectangle(60, 10, 100, 50, tags="box")

canvas.itemconfig("box", fill="orange")
```

**Result**

```
All rectangles with tag "box" change color
```

---

## 11. Deleting Items

### 11.1 Delete Single Item

```python
canvas.delete(rect_id)
```

### 11.2 Delete by Tag

```python
canvas.delete("box")
```

### 11.3 Clear Canvas

```python
canvas.delete("all")
```

---

## 12. Event Handling on Canvas

### 12.1 Mouse Click Detection

```python
def on_click(event):
    print(event.x, event.y)

canvas.bind("<Button-1>", on_click)
```

**Expected Output**

```
120 85
```

---

## 13. Canvas Size & Scaling

### 13.1 Resize Canvas

```python
canvas.config(width=300, height=300)
```

---

### 13.2 Scale Items

```python
canvas.scale(
    "all",
    0, 0,   # origin
    1.5,    # x scale
    1.5     # y scale
)
```

---

## 14. Canvas vs Label (Why Canvas Is Used Here)

| Feature        | Canvas | Label   |
| -------------- | ------ | ------- |
| Images         | Yes    | Yes     |
| Shapes         | Yes    | No      |
| Multiple items | Yes    | No      |
| Movement       | Yes    | No      |
| Events         | Yes    | Limited |

---

## 15. Typical Password Manager Use Cases

| Use Case        | Canvas Role        |
| --------------- | ------------------ |
| App logo        | `create_image()`   |
| Icons           | `create_polygon()` |
| Animations      | `move()`           |
| Click detection | `bind()`           |
| Custom UI       | Shapes + text      |

---

## 16. Your Code (Annotated Deeply)

```python
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
```

* Creates main window
* Adds internal padding

```python
canvas = tk.Canvas(width=200, height=200)
```

* Creates drawing surface
* Independent coordinate space

```python
logo_img = tk.PhotoImage(file="logo.png")
```

* Loads image into memory
* Must be referenced globally

```python
canvas.create_image(100, 100, image=logo_img)
```

* Places image at center `(100,100)`

```python
canvas.pack()
```

* Renders canvas

```python
window.mainloop()
```

* Starts GUI event loop
* Required for interaction
