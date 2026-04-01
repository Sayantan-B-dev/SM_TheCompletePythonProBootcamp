# Scatter Plots – Average Number of Parts per LEGO Set

## Overview

We've seen how LEGO's set count and theme count have evolved. Now we ask: **Have sets become larger and more complex over time?**  
To answer this, we calculate the **average number of parts per set for each year** and visualise the trend with a scatter plot. This lesson covers:

- Using `.groupby()` and `.agg()` to compute averages.
- Creating scatter plots with Matplotlib.
- Interpreting the upward trend in set complexity.

---

## 1. Computing Average Parts per Year

We group the `sets` DataFrame by `year` and apply the `mean` function to the `num_parts` column.

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')

parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})
parts_per_set.columns = ['avg_parts']
parts_per_set.head()
```

**Output:**

| year | avg_parts   |
|------|-------------|
| 1949 | 99.600000   |
| 1950 | 1.000000    |
| 1953 | 13.500000   |
| 1954 | 12.357143   |
| 1955 | 36.607143   |

**Note:** The low averages in early years (e.g., 1950's 1.0) are due to very small sets like promotional items. Later years show more stable values.

---

## 2. Creating a Scatter Plot

We'll plot the average parts per year using `plt.scatter()`. As before, we exclude incomplete years (2020–2021) using slicing.

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.scatter(parts_per_set.index[:-2], parts_per_set.avg_parts[:-2])
plt.title('Average Number of Parts per LEGO Set Over Time')
plt.xlabel('Year')
plt.ylabel('Average Number of Parts')
plt.grid(True, alpha=0.3)
plt.show()
```

**Result:** A scatter plot showing individual data points for each year.

---

## 3. Adding a Trend Line

To better see the trend, we can fit a linear regression line using `numpy.polyfit`.

```python
import numpy as np

# Prepare data (exclude incomplete years)
years = parts_per_set.index[:-2]
avg_parts = parts_per_set.avg_parts[:-2]

# Fit a linear trend (degree 1)
z = np.polyfit(years, avg_parts, 1)
p = np.poly1d(z)

plt.figure(figsize=(12,6))
plt.scatter(years, avg_parts, alpha=0.6, label='Actual average')
plt.plot(years, p(years), "r--", label='Trend line')
plt.title('Average Number of Parts per LEGO Set Over Time')
plt.xlabel('Year')
plt.ylabel('Average Number of Parts')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
```

**Interpretation:** The upward sloping trend line confirms that sets have generally become larger over the decades.

---

## 4. Observations

- **1950s–1960s:** Highly variable, often below 100 parts.
- **1970s–1980s:** Gradual increase to around 150–200 parts.
- **1990s–2000s:** Continued growth, with some years showing spikes (e.g., due to large exclusive sets).
- **2010s:** Average stabilises around 200–250 parts, roughly double the average of the 1960s.

**Conclusion:** LEGO sets have indeed grown in size and complexity over time.

---

## 5. Complete Code Block

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sets = pd.read_csv('data/sets.csv')

# Average parts per year
parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})
parts_per_set.columns = ['avg_parts']

# Exclude incomplete years
years = parts_per_set.index[:-2]
avg_parts = parts_per_set.avg_parts[:-2]

# Scatter plot with trend line
plt.figure(figsize=(12,6))
plt.scatter(years, avg_parts, alpha=0.6, label='Actual average')

# Trend line
z = np.polyfit(years, avg_parts, 1)
p = np.poly1d(z)
plt.plot(years, p(years), "r--", label='Trend line')

plt.title('Average Number of Parts per LEGO Set Over Time')
plt.xlabel('Year')
plt.ylabel('Average Number of Parts')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
```

---

## 6. Key Takeaways

- **`.agg()`** with `pd.Series.mean` computes the average per group.
- **Scatter plots** are ideal for showing individual data points and identifying trends.
- Adding a **trend line** helps quantify the direction and strength of the trend.
- The data clearly shows an upward trend in set complexity, confirming that modern LEGO sets are more elaborate.

---

## 7. Next Steps

Now that we've analysed sets, themes, and complexity, the next lessons will explore **database schemas** and **merging DataFrames** to bring in theme names and create bar charts of the most popular themes.

---
