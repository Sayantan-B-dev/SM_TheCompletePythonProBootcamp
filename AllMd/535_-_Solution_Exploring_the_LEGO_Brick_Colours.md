# Solution - Exploring the LEGO Brick Colours

## Overview

This lesson provides the step-by-step solution to the first data challenge: analyzing the `colors.csv` dataset. You will learn how to:

- Load and inspect the dataset.
- Count unique colours using `.nunique()`.
- Count transparent vs. opaque colours using both `.groupby()` and `.value_counts()`.
- Enhance your notebook with headings and images to match the provided example.

---

## 1. Importing Pandas

The first step in any data analysis project is importing the necessary libraries. Here we only need Pandas.

```python
import pandas as pd
```

**Why Pandas?**  
Pandas provides powerful data structures (like DataFrame) and methods for reading CSV files, inspecting data, and performing aggregations.

---

## 2. Reading and Examining the Data

We load the CSV file into a DataFrame and look at the first few rows to understand its structure.

```python
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

**Observations:**
- `id`: internal identifier (note the `-1` for "Unknown").
- `name`: the colour name.
- `rgb`: hexadecimal RGB value (without the `#`).
- `is_trans`: flag indicating if the colour is transparent (`'t'`) or opaque (`'f'`).

---

## 3. Counting Unique Colours

The question: *How many different colours does LEGO produce?*  
We can answer this by counting unique values in the `name` column.

### Using `.nunique()`

```python
unique_colors = colors['name'].nunique()
print(f"Total unique colours: {unique_colors}")
```

**Output:**
```
Total unique colours: 135
```

**Explanation:**  
`.nunique()` returns the number of distinct values in a Series, ignoring NaN (if any). It's more efficient than `len(colors['name'].unique())`.

> **Note:** The `id` column might also have 135 unique values, but the `name` column is what we care about because multiple IDs could theoretically map to the same name? In this dataset, `id` is a primary key, so each colour has a unique ID, but the `name` column is what we want for counting distinct colour names.

---

## 4. Counting Transparent vs. Opaque Colours

The `is_trans` column indicates transparency. We need to count how many colours are transparent (`'t'`) and how many are opaque (`'f'`).

### Method 1: Using `.groupby()` + `.count()`

```python
colors.groupby('is_trans').count()
```

**Output:**

| is_trans | id  | name | rgb |
|----------|-----|------|-----|
| f        | 107 | 107  | 107 |
| t        | 28  | 28   | 28  |

- The `.groupby('is_trans')` splits the DataFrame into two groups (f and t).
- `.count()` counts non-null values in each column for each group.
- Since all columns have the same count (no missing values), any column gives the group size.

### Method 2: Using `.value_counts()`

```python
colors['is_trans'].value_counts()
```

**Output:**
```
f    107
t     28
Name: is_trans, dtype: int64
```

- `.value_counts()` directly counts the frequency of each unique value in a Series.
- It's concise and returns a Series with the counts.

### Method 3: Boolean Filtering (Alternative)

```python
transparent = colors[colors['is_trans'] == 't'].shape[0]
opaque = colors[colors['is_trans'] == 'f'].shape[0]
print(f"Transparent: {transparent}, Opaque: {opaque}")
```

**Output:**
```
Transparent: 28, Opaque: 107
```

- `.shape[0]` returns the number of rows after filtering.

**Insight:** Only 28 out of 135 colours (≈20.7%) are transparent, which makes sense because transparent pieces are typically used for specific elements like windows, windscreens, or lightsaber blades.

---

## 5. Enhancing Your Notebook with Headings and Images

The challenge asks you to make your notebook look like the provided image. This involves adding section headings and images using HTML/Markdown.

### 5.1 Adding a Heading

Use Markdown `#` or HTML `<h1>` tags. For example, above the solution you might add:

```markdown
# Exploring LEGO Brick Colours
```

Or using HTML:

```html
<h1>Exploring LEGO Brick Colours</h1>
```

### 5.2 Adding an Image

You can insert an image using the HTML `<img>` tag. For the provided example, the image might be a collage of LEGO bricks. Use a public URL or a local file (if using Jupyter).

```html
<img src="https://i.imgur.com/49FNOHj.jpg" width="600">
```

If you have the image in an `assets` folder (as in the starter .zip), you can reference it locally (Jupyter only):

```html
<img src="assets/bricks.jpg" width="600">
```

### 5.3 Complete Markdown Cell Example

In your notebook, create a new **Text cell** and paste:

```html
<h1>Exploring LEGO Brick Colours</h1>

<img src="https://i.imgur.com/49FNOHj.jpg" width="600">

<p>Let's find out how many different colours LEGO produces and how many are transparent.</p>
```

This will render a nicely formatted section with an image and introductory text.

---

## 6. Full Code Block for This Lesson

Here's the complete code used in the solution cell:

```python
import pandas as pd

# Load data
colors = pd.read_csv('data/colors.csv')

# Display first few rows
print("First 5 rows:")
print(colors.head())

# Count unique colours
print("\nUnique colours:", colors['name'].nunique())

# Count transparent vs opaque (Method 1)
print("\nUsing groupby + count:")
print(colors.groupby('is_trans').count())

# Count transparent vs opaque (Method 2)
print("\nUsing value_counts():")
print(colors['is_trans'].value_counts())
```

**Expected Output:**

```
First 5 rows:
   id            name     rgb is_trans
0  -1         Unknown  0033B2        f
1   0           Black  05131D        f
2   1            Blue  0055BF        f
3   2           Green  237841        f
4   3  Dark Turquoise  008F9B        f

Unique colours: 135

Using groupby + count:
           id  name  rgb
is_trans               
f         107   107  107
t          28    28   28

Using value_counts():
f    107
t     28
Name: is_trans, dtype: int64
```

---

## 7. Key Takeaways

- **`.nunique()`** quickly counts unique values in a column.
- **`.value_counts()`** is the most direct way to get frequency counts of categorical data.
- **`.groupby()`** is more flexible and can be used for multiple aggregations.
- **HTML in Markdown cells** enhances the notebook's readability and visual appeal.
- The LEGO colour dataset contains **135 unique colours**, with only **28 transparent** shades.

---

## 8. Next Steps

Now that you've mastered the colour data, the next lesson will explore the `sets.csv` to answer questions about the oldest and largest LEGO sets ever produced.

---

