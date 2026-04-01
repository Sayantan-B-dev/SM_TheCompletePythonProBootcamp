# Superimposing Line Charts with Separate Axes

## Overview

When comparing two related trends that have different scales (e.g., number of sets vs. number of themes), plotting them on the same y‑axis makes one line appear flat and unreadable. The solution is to use **dual axes**: two separate y‑axes sharing the same x‑axis. This lesson shows how to achieve this in Matplotlib using `twinx()`.

---

## 1. The Problem: Different Scales

We have two DataFrames:

- `sets_by_year`: number of sets released per year (range 0–900).
- `themes_by_year`: number of unique themes per year (range 0–90).

If we plot both on the same axis, the themes line gets compressed near zero.

```python
import matplotlib.pyplot as plt

# Assume sets_by_year and themes_by_year are already defined (from previous lessons)
plt.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2])
plt.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2])
plt.show()
```

**Result:** The themes line is nearly invisible because its scale is an order of magnitude smaller.

---

## 2. Creating a Second Y‑Axis with `twinx()`

Matplotlib allows us to create a twin axis that shares the same x‑axis but has its own y‑scale.

```python
# Get the current axis
ax1 = plt.gca()

# Create a second axis that shares the same x-axis
ax2 = ax1.twinx()

# Plot sets on the first axis
ax1.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2])

# Plot themes on the second axis
ax2.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2])

plt.show()
```

Now both lines are visible, but they have the same colour, making them hard to distinguish.

---

## 3. Styling and Labelling the Axes

We can improve readability by:

- Using different colours for the lines.
- Colouring the axis labels accordingly.
- Adding axis labels and a title.

```python
fig, ax1 = plt.subplots(figsize=(12,6))

# First axis (sets)
ax1.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2], color='green')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Sets', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Second axis (themes)
ax2 = ax1.twinx()
ax2.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2], color='blue')
ax2.set_ylabel('Number of Themes', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

plt.title('LEGO Sets and Themes Released Over Time')
plt.show()
```

**Result:** A clear dual‑axis chart with green for sets and blue for themes, each with its own scale.

---

## 4. Complete Code Block

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
sets = pd.read_csv('data/sets.csv')

# Sets per year
sets_by_year = sets.groupby('year').count()[['set_num']]
sets_by_year.columns = ['num_sets']

# Themes per year (unique themes)
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
themes_by_year.columns = ['nr_themes']

# Create dual-axis plot
fig, ax1 = plt.subplots(figsize=(12,6))

# Sets on left axis
ax1.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2], 
         color='green', linewidth=2)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Number of Sets', color='green', fontsize=12)
ax1.tick_params(axis='y', labelcolor='green')

# Themes on right axis
ax2 = ax1.twinx()
ax2.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2], 
         color='blue', linewidth=2)
ax2.set_ylabel('Number of Themes', color='blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='blue')

plt.title('LEGO Sets and Themes Released Over Time (1949–2019)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.show()
```

**Expected Output:** A professional dual‑axis line chart showing both trends clearly.

---

## 5. Interpretation

- Both sets and themes show overall growth, but with different magnitudes.
- The stagnation in themes during the late 1990s–2000s is now clearly visible alongside the continued rise in sets.
- The chart reinforces the idea that LEGO expanded its product line within existing themes before introducing many new ones in the 2010s.

---

## 6. Key Takeaways

- **`twinx()`** creates a second y‑axis that shares the same x‑axis.
- Always style the axes (colours, labels) to avoid confusion.
- Dual axes are essential when comparing variables with different units or scales.
- The same principle applies to `twiny()` for shared y‑axis with two x‑axes.

---

## 7. Next Steps

Now that we've mastered dual‑axis plots, the next lesson will explore scatter plots to analyse the average number of parts per set over time.

---

