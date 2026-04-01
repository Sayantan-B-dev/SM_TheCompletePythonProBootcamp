## Importing External Package

```python
import colorgram
```

| Item        | Meaning                                               |
| ----------- | ----------------------------------------------------- |
| `colorgram` | Third-party library for extracting colors from images |

Important:

* This is **not** a standard library
* Must be installed before use:

```bash
pip install colorgram.py
```

---

## Data Container

```python
rgb_colors = []
```

| Variable     | Purpose                     |
| ------------ | --------------------------- |
| `rgb_colors` | Stores extracted RGB tuples |

List is used because:

* Number of colors is dynamic
* Colors are accumulated iteratively

---

## Extracting Colors from Image

```python
colors = colorgram.extract('136_image.jpg', 10)
```

| Argument          | Meaning                              |
| ----------------- | ------------------------------------ |
| `'136_image.jpg'` | Image file path                      |
| `10`              | Number of dominant colors to extract |

What this returns:

* A **list of Color objects**
* Each object contains RGB, HSL, and proportion data

---

## Reading RGB Values

```python
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
```

| Access      | Explanation               |
| ----------- | ------------------------- |
| `color.rgb` | RGB color object          |
| `.r .g .b`  | Individual color channels |

Why done explicitly:

* Makes channel extraction clear
* Avoids passing complex objects downstream

---

## Creating RGB Tuple

```python
new_color = (r, g, b)
```

| Reason for Tuple | Explanation                          |
| ---------------- | ------------------------------------ |
| Fixed structure  | RGB must always be 3 values          |
| Immutability     | Color should not change              |
| Compatibility    | Turtle & graphics APIs expect tuples |

---

## Storing the Colors

```python
rgb_colors.append(new_color)
```

| Operation  | Effect                     |
| ---------- | -------------------------- |
| `append()` | Adds one RGB tuple to list |

After loop:

* `rgb_colors` → list of `(R, G, B)` tuples

---

## Output

```python
print(rgb_colors)
```

### Example Expected Output

```
[(245, 239, 232), (33, 40, 48), (199, 164, 124),
 (120, 90, 65), (78, 85, 92), (220, 201, 180),
 (160, 130, 95), (45, 52, 60), (180, 150, 120),
 (98, 102, 110)]
```

Actual values depend on:

* Image content
* Color distribution
* Extraction order

---

## Core Use Case

This pattern is commonly used to:

* Extract a **color palette** from an image
* Feed RGB values into:

  * Turtle graphics
  * Data visualization
  * Generative art
  * UI theming

---

## Key Insight

> `colorgram` converts visual information
> into **pure numeric RGB data**,
> making images usable inside Python logic.
