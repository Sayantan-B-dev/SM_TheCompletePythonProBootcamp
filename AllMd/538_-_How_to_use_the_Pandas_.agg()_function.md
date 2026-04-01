# How to Use the Pandas `.agg()` Function

## Overview

The `.groupby()` method is powerful for splitting data into groups, but sometimes you need different aggregations for different columns. The `.agg()` method (short for "aggregate") allows you to apply multiple or custom functions to grouped data. In this lesson, we'll use it to count the number of **unique themes** released each year.

---

## 1. The Problem: Unique Themes per Year

The `sets.csv` has a `theme_id` column that links to the `themes.csv` file. We want to know: **How many distinct themes did LEGO release each year?**  
Simply counting rows per year (as we did for sets) would count duplicate themes. We need the number of **unique** theme IDs per year.

---

## 2. Using `.groupby()` + `.agg()`

We chain `.groupby('year')` with `.agg()` and pass a dictionary specifying the operation for each column.

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')

themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
```

- `groupby('year')` splits the DataFrame by year.
- `.agg({'theme_id': pd.Series.nunique})` applies `nunique()` to the `theme_id` column within each year group, counting unique values.

The result is a DataFrame with `year` as index and one column named `theme_id`.

---

## 3. Cleaning Up the Result

Let's rename the column to something more descriptive.

```python
themes_by_year.columns = ['nr_themes']
themes_by_year.head()
```

**Output:**

| year | nr_themes |
|------|-----------|
| 1949 | 2         |
| 1950 | 1         |
| 1953 | 2         |
| 1954 | 2         |
| 1955 | 4         |

**Interpretation:** In 1949, only 2 themes existed; by 1955 there were 4.

---

## 4. Visualising Themes Over Time

We'll create a line chart, excluding incomplete years (2020–2021) using slicing.

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2])
plt.title('Number of LEGO Themes Released Per Year (1949-2019)')
plt.xlabel('Year')
plt.ylabel('Number of Themes')
plt.grid(True, alpha=0.3)
plt.show()
```

**Chart Insights:**
- Steady increase in themes until the mid-1990s.
- Stagnation for about 10 years (late 1990s–mid 2000s).
- Renewed growth in the 2010s, reaching nearly 100 themes per year.

---

## 5. Comparison with Sets Chart

If we compare with the sets-per-year chart from lesson 537, we see similar patterns but with a plateau in themes during a period when sets were still growing. This suggests LEGO was expanding within existing themes rather than creating new ones.

---

## 6. Complete Code Block

```python
import pandas as pd
import matplotlib.pyplot as plt

sets = pd.read_csv('data/sets.csv')

# Count unique themes per year
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
themes_by_year.columns = ['nr_themes']

# Plot (excluding 2020 & 2021)
plt.figure(figsize=(12,6))
plt.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2])
plt.title('Number of LEGO Themes Released Per Year (1949-2019)')
plt.xlabel('Year')
plt.ylabel('Number of Themes')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 7. Key Takeaways

- **`.agg()`** is used after `.groupby()` to specify different aggregations per column.
- `pd.Series.nunique` counts unique values in a Series.
- The themes count shows a plateau in the late 1990s–2000s, indicating a period of consolidation.
- Slicing (`[:-2]`) ensures we only plot complete years.

---

## 8. Next Steps

In the next lesson, we'll combine the sets and themes charts on a single figure with two y‑axes to compare trends directly.

---

