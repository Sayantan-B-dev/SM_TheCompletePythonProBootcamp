# How to Merge DataFrames and Create Bar Charts

## Overview

We now know that `theme_id` in `sets.csv` links to `id` in `themes.csv`. To get human-readable theme names alongside the set counts, we need to **merge** the two DataFrames. After merging, we'll create a bar chart of the top 10 themes by number of sets.

This lesson covers:

- Converting a Pandas Series to a DataFrame.
- Using `pd.merge()` to join on a common column.
- Creating and customizing bar charts with Matplotlib.
- Interpreting the results.

---

## 1. Preparing the Set Count Data

We previously used `value_counts()` to count sets per theme, which returned a Series.

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')
set_theme_count = sets['theme_id'].value_counts()
print(set_theme_count.head())
```

**Output:**
```
158    753
501    656
494    398
435    356
503    329
Name: theme_id, dtype: int64
```

To merge, we need a DataFrame with columns `id` (theme ID) and `set_count`. We'll convert the Series.

```python
set_theme_count = pd.DataFrame({
    'id': set_theme_count.index,
    'set_count': set_theme_count.values
})
print(set_theme_count.head())
```

**Output:**

| id  | set_count |
|-----|-----------|
| 158 | 753       |
| 501 | 656       |
| 494 | 398       |
| 435 | 356       |
| 503 | 329       |

Now we have a clean DataFrame ready for merging.

---

## 2. Loading the Themes Data

```python
themes = pd.read_csv('data/themes.csv')
print(themes.head())
```

**Output:**

| id | name            | parent_id |
|----|-----------------|-----------|
| 1  | Technic         | NaN       |
| 2  | Arctic Technic  | 1.0       |
| 3  | Competition     | 1.0       |
| 4  | Expert Builder  | 1.0       |
| 5  | Model           | 1.0       |

---

## 3. Merging the DataFrames

We merge on the common column `id`. By default, `pd.merge()` performs an inner join, keeping only rows with matching keys in both DataFrames.

```python
merged_df = pd.merge(set_theme_count, themes, on='id')
print(merged_df.head())
```

**Output:**

| id  | set_count | name        | parent_id |
|-----|-----------|-------------|-----------|
| 158 | 753       | Star Wars   | NaN       |
| 501 | 656       | Gear        | NaN       |
| 494 | 398       | Friends     | NaN       |
| 435 | 356       | City 2010   | 435.0     |
| 503 | 329       | City 2009   | 503.0     |

**Insight:** The largest theme by set count is **Star Wars** with 753 sets, followed by **Gear** (promotional merchandise) with 656 sets, then **Friends** with 398 sets.

---

## 4. Creating a Bar Chart of the Top 10 Themes

We'll plot the top 10 themes by set count. First, sort by `set_count` descending (though the merge result is already sorted if we kept original order).

```python
import matplotlib.pyplot as plt

# Get top 10
top10 = merged_df.head(10)

plt.figure(figsize=(14,8))
plt.bar(top10['name'], top10['set_count'])
plt.xlabel('Theme Name')
plt.ylabel('Number of Sets')
plt.title('Top 10 LEGO Themes by Number of Sets')
plt.show()
```

**Problem:** The x‑axis labels overlap and are unreadable.

---

## 5. Customising the Bar Chart

We can fix readability by:

- Increasing figure size.
- Rotating x‑axis labels.
- Adding more space and adjusting fonts.

```python
plt.figure(figsize=(14,8))
plt.bar(top10['name'], top10['set_count'])
plt.xlabel('Theme Name', fontsize=14)
plt.ylabel('Number of Sets', fontsize=14)
plt.title('Top 10 LEGO Themes by Number of Sets', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=12)  # rotate and align right
plt.yticks(fontsize=12)
plt.tight_layout()  # ensures everything fits
plt.show()
```

Now the chart is clear and professional.

---

## 6. Interpretation of the Chart

- **Star Wars** is the most prolific theme – a testament to its long‑running popularity and numerous sub‑lines.
- **Gear** (promotional items like keychains, books, etc.) ranks second, showing LEGO's diversification beyond bricks.
- **Friends**, **City** variants, and **Technic** are also major themes.
- The presence of multiple "City" entries (City 2010, City 2009, etc.) indicates that LEGO often splits themes by year or sub‑theme.

**Discussion Point:** Does LEGO's expansion into "Gear" represent successful diversification or a departure from its core product? The data shows it's a significant part of their offering.

---

## 7. Complete Code Block

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
sets = pd.read_csv('data/sets.csv')
themes = pd.read_csv('data/themes.csv')

# Count sets per theme
set_theme_count = sets['theme_id'].value_counts().reset_index()
set_theme_count.columns = ['id', 'set_count']

# Merge with themes
merged_df = pd.merge(set_theme_count, themes, on='id')
merged_df = merged_df.sort_values('set_count', ascending=False)

# Plot top 10
top10 = merged_df.head(10)
plt.figure(figsize=(14,8))
plt.bar(top10['name'], top10['set_count'])
plt.xlabel('Theme Name', fontsize=14)
plt.ylabel('Number of Sets', fontsize=14)
plt.title('Top 10 LEGO Themes by Number of Sets', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
```

---

## 8. Key Takeaways

- **`pd.merge()`** combines DataFrames on a common key (here `id`). It's essential for enriching data with related information.
- Converting a Series to a DataFrame gives you control over column names.
- Bar charts are ideal for comparing categorical counts.
- Always customise your plots (size, rotation, labels) to make them readable.
- The merged data reveals that **Star Wars** is the top theme, but promotional **Gear** is a close second, highlighting LEGO's diversified product range.

---

## 9. Next Steps

The final lesson will summarise everything learned and provide next steps for further analysis.

---