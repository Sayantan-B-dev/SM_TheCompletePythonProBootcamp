## Learning Points & Summary

This project demonstrated a complete workflow for analyzing time-series data using Pandas and Matplotlib. Below is a concise recap of each major step, accompanied by the essential code patterns. Use this as a reference for similar analyses.

---

### 1. Importing Libraries and Data

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV with custom column names
df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
```

- `names` overrides the original headers.
- `header=0` indicates that the first row of the CSV is the original header (which we replace).

---

### 2. Initial Data Inspection

```python
# First and last 5 rows
df.head()
df.tail()

# Dimensions
df.shape                 # e.g., (1991, 3)

# Count non-null entries per column
df.count()
```

---

### 3. Grouping and Aggregating

```python
# Total posts per language
df.groupby('TAG').sum()

# Number of months (entries) per language
df.groupby('TAG').count()
```

- `.sum()` gives total posts.
- `.count()` gives number of rows (months) for each language.

---

### 4. Cleaning Dates

```python
# Convert entire DATE column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])
```

- After conversion, dates become `datetime64[ns]` type, enabling time-series operations.

---

### 5. Reshaping with Pivot

```python
# Pivot from long to wide format
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')

# Check shape and columns
reshaped_df.shape        # e.g., (145, 14)
reshaped_df.columns

# Replace NaN with 0
reshaped_df.fillna(0, inplace=True)

# Verify no NaNs remain
reshaped_df.isna().values.any()   # False
```

- `pivot()` creates one column per language, index = date.
- `fillna(0)` treats missing months as zero posts.

---

### 6. Basic Plotting with Matplotlib

```python
# Single language
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)
plt.plot(reshaped_df.index, reshaped_df['java'])
plt.show()
```

- Customize figure size, tick sizes, labels, and y-axis limits for clarity.

---

### 7. Multiple Lines on Same Chart

```python
# Two languages
plt.plot(reshaped_df.index, reshaped_df['java'], label='Java')
plt.plot(reshaped_df.index, reshaped_df['python'], label='Python')
plt.legend(fontsize=14)
```

- Use `label` in each plot and call `plt.legend()`.

---

### 8. Plotting All Languages with a Loop

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column],
             linewidth=3, label=column)

plt.legend(fontsize=16)
plt.show()
```

- Iterate over columns, assign `label` for legend, increase `linewidth` for visibility.

---

### 9. Smoothing with Rolling Averages

```python
# Compute 6-month rolling average
roll_df = reshaped_df.rolling(window=6).mean()

# Plot the smoothed data
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts (6-month avg)', fontsize=14)
plt.ylim(0, 35000)

for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column],
             linewidth=3, label=column)

plt.legend(fontsize=16)
plt.show()
```

- `rolling(window=n).mean()` computes moving averages.
- Larger windows produce smoother lines but lag more.
- First `n-1` rows are `NaN` (omitted in plot).

---

### 10. Key Takeaways

- **Data Preparation**: Convert strings to datetime, reshape with `pivot()`, handle missing values with `fillna()`.
- **Exploration**: Use `groupby()` for summary statistics.
- **Visualization**: Matplotlib offers flexible plotting; customize size, labels, ticks, and limits.
- **Time-Series Smoothing**: Rolling averages reveal long-term trends by reducing noise.
- **Interpretation**: Smoothed charts highlight which languages are rising, falling, or stable.

---

### 11. Quiz Concepts (from file 532)

The associated quiz tested understanding of:
- Pandas `groupby()` vs `pivot()`.
- Handling `NaN` in pivoted DataFrames.
- Effect of rolling window size.
- Matplotlib customization methods (`figure`, `xticks`, `ylim`, `legend`).
- Interpretation of time-series trends (e.g., Python's growth).

---

This workflow can be adapted to any time-series dataset where you need to compare multiple categories over time. The combination of Pandas for data wrangling and Matplotlib for visualization provides a powerful and flexible toolkit.