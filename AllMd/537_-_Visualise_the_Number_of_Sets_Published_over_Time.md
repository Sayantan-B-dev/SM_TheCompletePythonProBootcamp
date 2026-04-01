# Visualising the Number of Sets Published Over Time

## Overview

Now we will analyse how LEGO's product offering has evolved over the years. By counting the number of sets released each year and plotting the results, we can identify growth phases, downturns, and the overall trajectory of the company. This lesson introduces:

- Grouping data with `.groupby()` and counting.
- Creating line charts with Matplotlib.
- Slicing DataFrames to exclude incomplete years.

---

## 1. Importing Matplotlib

Before we create visualisations, we import the plotting library.

```python
import matplotlib.pyplot as plt
```

---

## 2. Counting Sets per Year

We use `groupby()` to aggregate the data by year and count the number of sets (using `set_num` as the count column).

```python
sets_by_year = sets.groupby('year').count()
sets_by_year = sets_by_year[['set_num']]  # Keep only the count column
sets_by_year.columns = ['num_sets']       # Rename for clarity

print(sets_by_year.head())
```

**Output:**

```
      num_sets
year          
1949         5
1950         6
1953         4
1954        14
1955        28
```

This Series shows that in 1949 only 5 sets were released; by 1955 that number had grown to 28.

---

## 3. Plotting the Full Data (Including Incomplete Years)

First, let's create a line chart of all years, including 2020 and 2021.

```python
plt.figure(figsize=(12,6))
plt.plot(sets_by_year.index, sets_by_year.num_sets)
plt.title('LEGO Sets Released Per Year (1949-2021)')
plt.xlabel('Year')
plt.ylabel('Number of Sets')
plt.grid(True, alpha=0.3)
plt.show()
```

**Observation:** The chart shows a sharp drop at the end because the data for 2020 and 2021 is incomplete (the dataset was compiled in late 2020). This could mislead someone into thinking LEGO's production collapsed.

---

## 4. Excluding Incomplete Years with Slicing

To get an accurate picture, we slice off the last two rows (2020 and 2021) using Python's list slicing syntax. This works on DataFrame indices as well.

```python
plt.figure(figsize=(12,6))
plt.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2])
plt.title('LEGO Sets Released Per Year (1949-2019)')
plt.xlabel('Year')
plt.ylabel('Number of Sets')
plt.grid(True, alpha=0.3)
plt.show()
```

**Result:** Now the chart shows a steady increase with a dramatic take-off in the mid-1990s, a slight dip around 2000, and strong growth after 2005.

---

## 5. Interpretation

- **Early years (1949–1990):** Fewer than 100 sets per year; slow growth.
- **Mid-1990s explosion:** Rapid expansion, likely due to licensing deals (Star Wars, etc.) and new themes.
- **Early 2000s dip:** Possibly related to the company's financial struggles before the turnaround in 2005.
- **Modern era (2005–2019):** Sustained high output, peaking at over 800 sets annually.

---

## 6. Complete Code Block

```python
import pandas as pd
import matplotlib.pyplot as plt

sets = pd.read_csv('data/sets.csv')

# Count sets per year
sets_by_year = sets.groupby('year').count()[['set_num']]
sets_by_year.columns = ['num_sets']

# Plot without slicing (shows misleading drop)
plt.figure(figsize=(12,6))
plt.plot(sets_by_year.index, sets_by_year.num_sets)
plt.title('LEGO Sets Released Per Year (1949-2021)')
plt.xlabel('Year')
plt.ylabel('Number of Sets')
plt.grid(True, alpha=0.3)
plt.show()

# Plot with slicing (excludes 2020 & 2021)
plt.figure(figsize=(12,6))
plt.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2])
plt.title('LEGO Sets Released Per Year (1949-2019)')
plt.xlabel('Year')
plt.ylabel('Number of Sets')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 7. Key Takeaways

- **`.groupby().count()`** is the standard way to get frequency counts per category.
- **Slicing** (`[:-2]`) helps remove incomplete data and avoids misleading visualisations.
- The line chart reveals LEGO's growth trajectory, including a major expansion in the 1990s and recovery after 2005.

---

## 8. Next Steps

In the next lesson, we'll use the `.agg()` function to calculate more sophisticated aggregates, such as the number of unique themes per year.

---

*This documentation was prepared for lesson 537 of the LEGO data analysis series.*