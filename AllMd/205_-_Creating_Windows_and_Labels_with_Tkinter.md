## `pack()` — Purpose and Core Idea

> `pack()` is a **geometry manager** in Tkinter.
> Its job is to **decide where a widget goes inside its parent container** and **how much space it occupies**.

When you call `pack()`, Tkinter:

1. Takes the widget
2. Looks at the parent container (here: `window`)
3. Allocates space according to the rules you provide
4. Positions the widget accordingly

No coordinates are used. Everything is **relative and flow-based**.

---

## Your Line Under Focus

```python
label.pack(side="top")
```

This means:

* Use the **pack geometry manager**
* Attach the widget to the **top side** of the available space

---

## All Parameters of `pack()` (Complete)

### 1. `side`

```python
pack(side="top" | "bottom" | "left" | "right")
```

**What it controls**

* Which edge of the parent container the widget sticks to

**Default**

* `"top"`

**Behavior**

* Widgets are packed **one after another**
* Each new widget reduces the remaining free space

| Value      | Effect                              |
| ---------- | ----------------------------------- |
| `"top"`    | Widget placed at top, full width    |
| `"bottom"` | Widget placed at bottom, full width |
| `"left"`   | Widget placed left, full height     |
| `"right"`  | Widget placed right, full height    |

**Example**

```python
label.pack(side="left")
```

Expected visual result:

* Label sticks to the **left edge**
* Occupies vertical space

---

### 2. `fill`

```python
pack(fill="x" | "y" | "both")
```

**What it controls**

* Whether the widget **expands to fill extra space**

**Default**

* `None` (no expansion)

| Value    | Effect                     |
| -------- | -------------------------- |
| `"x"`    | Expands horizontally       |
| `"y"`    | Expands vertically         |
| `"both"` | Expands in both directions |

**Example**

```python
label.pack(fill="x")
```

Expected behavior:

* Label stretches **left to right**
* Height remains content-based

---

### 3. `expand`

```python
pack(expand=True | False)
```

**What it controls**

* Whether the widget is allowed to **claim extra unused space**

**Important distinction**

* `expand` controls **space allocation**
* `fill` controls **space usage**

| Value   | Meaning                              |
| ------- | ------------------------------------ |
| `False` | Widget stays at natural size         |
| `True`  | Widget gets extra space if available |

**Example**

```python
label.pack(expand=True)
```

Expected behavior:

* Label stays centered
* Extra space surrounds it

---

### 4. `padx` and `pady`

```python
pack(padx=10, pady=20)
```

**What they control**

* External spacing **outside the widget**

| Parameter | Direction    |
| --------- | ------------ |
| `padx`    | Left + right |
| `pady`    | Top + bottom |

**Example**

```python
label.pack(pady=20)
```

Expected behavior:

* 20 pixels of vertical breathing room

---

### 5. `ipadx` and `ipady`

```python
pack(ipadx=10, ipady=5)
```

**What they control**

* Internal padding **inside the widget**

| Parameter | Direction                   |
| --------- | --------------------------- |
| `ipadx`   | Horizontal internal padding |
| `ipady`   | Vertical internal padding   |

**Difference from `padx/pady`**

* `padx/pady` → space **outside**
* `ipadx/ipady` → space **inside**

---

### 6. `anchor`

```python
pack(anchor="n")
```

**What it controls**

* Alignment of the widget **within its allocated space**

| Anchor                         | Meaning        |
| ------------------------------ | -------------- |
| `"n"`                          | North (top)    |
| `"s"`                          | South (bottom) |
| `"e"`                          | East (right)   |
| `"w"`                          | West (left)    |
| `"center"`                     | Center         |
| `"ne"`, `"nw"`, `"se"`, `"sw"` | Corners        |

**Example**

```python
label.pack(expand=True, anchor="n")
```

Expected behavior:

* Label sticks to top
* Extra space appears below

---

### 7. `before` and `after`

```python
pack(before=other_widget)
pack(after=other_widget)
```

**What they control**

* Packing order relative to another widget

**Use case**

* Insert widgets dynamically without re-packing everything

---

## How `pack()` Thinks (Mental Model)

```text
1. Choose a side
2. Place widget against that side
3. Reduce remaining free space
4. Move to next widget
```

This is why **order matters** with `pack()`.

---

## Common `pack()` Patterns

### Centered Widget

```python
label.pack(expand=True)
```

Result:

* Widget stays centered
* Extra space distributed evenly

---

### Top Banner Style

```python
label.pack(side="top", fill="x")
```

Result:

* Widget spans full width
* Fixed height

---

### Sidebar Layout

```python
label.pack(side="left", fill="y")
```

Result:

* Vertical bar on left

---

## Full Example Using Multiple Parameters

```python
label.pack(
    side="top",
    fill="x",
    padx=20,
    pady=10,
    ipadx=10,
    ipady=5
)
```

### Expected Visual Output

```
[ Window ]
----------------------------------
|     (20px padding)             |
|   [ Hello World (bold) ]       |
|     (20px padding)             |
----------------------------------
```

---

## Critical Rules of `pack()`

> • `pack()` is **relative**, not coordinate-based
> • Order of packing matters
> • Do not mix `pack()` with `grid()` in the same container
> • Best for simple, linear layouts

---

## When `pack()` Is the Wrong Tool

| Situation          | Better Choice            |
| ------------------ | ------------------------ |
| Form-like layouts  | `grid()`                 |
| Exact positioning  | `place()`                |
| Complex dashboards | Nested frames + `grid()` |

This understanding transfers directly to all GUI layout systems, not just Tkinter.
