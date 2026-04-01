# Using HTML Markdown to Make Your Notebook Look Pretty

## Overview

Jupyter Notebooks (and Google Colab) support two types of cells:

- **Code cells**: for Python code.
- **Text cells**: for formatted text using Markdown or HTML.

This lesson teaches you how to enhance your notebook's appearance with HTML tags, headings, images, and how to tackle the first data challenge: analyzing LEGO colors.

---

## 1. Adding and Formatting Text Cells

### Inserting a Markdown Cell
- In Google Colab: Click `+ Text` below the cell toolbar.
- In Jupyter: Select `Insert` → `Insert Cell Below` and change cell type to `Markdown`.

Once added, you can write plain text, Markdown, or HTML.

### HTML in Text Cells
HTML tags work directly inside text cells. For example:

```html
<h1>This is a heading using H1 tag</h1>
<h2>Smaller heading</h2>
<p>This is a paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
```

**Rendered output:**  
(Shown as formatted HTML headings and paragraph)

---

## 2. Adding Images

Images can be embedded using the HTML `<img>` tag.

### From a URL (Google Colab / Jupyter)
```html
<img src="https://i.imgur.com/49FNOHj.jpg" alt="LEGO bricks" width="400">
```
- `src`: image URL
- `alt`: alternative text (accessibility)
- `width` / `height`: optional size control

### From Local File (Jupyter only)
If you have an image in the `assets` folder (provided in the .zip), use:
```html
<img src="assets/bricks.jpg" width="500">
```
> **Note:** Google Colab cannot access local files unless you upload them separately. For Colab, always use a publicly accessible URL.

---

## 3. Section Headings

Headings can be created using HTML `<h1>` to `<h6>` tags, or Markdown shorthand with `#` symbols.

### Using HTML
```html
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
```

### Using Markdown
```markdown
# Main Title
## Section Title
### Subsection
```

Both render identically.

**Example output:**  
# Main Title  
## Section Title  
### Subsection  

---

## 4. First Data Challenge: Analyzing LEGO Colors

Now that your notebook looks good, it's time to write some Python code. We'll explore the `colors.csv` dataset.

### 4.1 Loading the Data

```python
import pandas as pd

colors = pd.read_csv('data/colors.csv')
colors.head()
```

**Output:**

| id | name           | rgb    | is_trans |
|----|----------------|--------|----------|
| -1 | Unknown        | 0033B2 | f        |
| 0  | Black          | 05131D | f        |
| 1  | Blue           | 0055BF | f        |
| 2  | Green          | 237841 | f        |
| 3  | Dark Turquoise | 008F9B | f        |

### 4.2 Counting Unique Colors

We need the total number of distinct colors. The `name` column contains the color names. Use `.nunique()`:

```python
unique_colors = colors['name'].nunique()
print(f"Total unique colors: {unique_colors}")
```

**Output:**
```
Total unique colors: 135
```

> **Why .nunique()?**  
> `.nunique()` counts unique values in a Series, ignoring NaN. It’s faster than `len(colors['name'].unique())`.

### 4.3 Transparent vs. Opaque Colors

The `is_trans` column indicates whether a color is transparent (`'t'`) or opaque (`'f'`). Count them using **two different methods**.

#### Method 1: `.value_counts()`
```python
transparency_counts = colors['is_trans'].value_counts()
print(transparency_counts)
```

**Output:**
```
f    107
t     28
Name: is_trans, dtype: int64
```

#### Method 2: Groupby and count
```python
transparency_grouped = colors.groupby('is_trans').count()
print(transparency_grouped)
```

**Output:**

| is_trans | id  | name | rgb |
|----------|-----|------|-----|
| f        | 107 | 107  | 107 |
| t        | 28  | 28   | 28  |

All columns show the same count because no nulls exist.

#### Method 3: Boolean filtering
```python
transparent = colors[colors['is_trans'] == 't'].shape[0]
opaque = colors[colors['is_trans'] == 'f'].shape[0]
print(f"Transparent: {transparent}, Opaque: {opaque}")
```

**Output:**
```
Transparent: 28, Opaque: 107
```

### 4.4 Interpretation

- LEGO produces **135 distinct colors**.
- Only **28 colors (≈21%)** are transparent; the rest are opaque.
- This insight can be used later when analyzing sets that use transparent elements (e.g., lightsabers, windscreens).

---

## 5. Complete Code for This Section

Here’s the full code snippet used in the notebook:

```python
import pandas as pd

# Load data
colors = pd.read_csv('data/colors.csv')
print(colors.head())

# Total unique colors
print("Unique colors:", colors['name'].nunique())

# Transparent vs opaque
print("\nUsing value_counts():")
print(colors['is_trans'].value_counts())

print("\nUsing groupby():")
print(colors.groupby('is_trans').count())
```

---

## 6. Key Takeaways

- **HTML in text cells** allows rich formatting beyond plain Markdown (e.g., image sizing, inline styles).
- **Images** can be embedded from URLs or local files (Jupyter only).
- **Headings** help structure the notebook; use `#` for simplicity or `<h1>` for more control.
- **Pandas methods** like `.nunique()` and `.value_counts()` provide quick summary statistics.
- **Multiple approaches** to the same problem reinforce understanding and flexibility.

---

## 7. Next Steps

Now that you've styled your notebook and explored color data, the next lesson will dive into the `sets.csv` to answer questions about the oldest and largest LEGO sets.

---
