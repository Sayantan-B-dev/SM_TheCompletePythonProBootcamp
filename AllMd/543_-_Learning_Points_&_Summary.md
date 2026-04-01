# 543: Learning Points & Summary

## Overview

This final lesson consolidates everything we've learned throughout the LEGO data analysis project. Each skill is summarised with a brief explanation and a code example (with output) drawn from the previous lessons. Use this as a reference for future projects involving Pandas, Matplotlib, and relational data.

---

## 1. HTML Markdown in Notebooks

We learned to enhance notebooks using HTML tags in Markdown cells.

### Headings
```html
<h1>Main Title</h1>
<h2>Subheading</h2>
```
Or use Markdown shorthand:
```markdown
# Main Title
## Subheading
```

### Images
```html
<img src="https://i.imgur.com/Sg4lcjx.png" width="600">
```
This embeds the database schema image directly in the notebook.

---

## 2. Grouping and Counting with `.groupby() + .count()`

To count the number of sets released each year:

```python
sets_by_year = sets.groupby('year').count()[['set_num']]
sets_by_year.columns = ['num_sets']
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

---

## 3. Using `.value_counts()` for Frequency Tables

To count how many sets belong to each theme (by ID):

```python
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

---

## 4. Slicing DataFrames

Exclude incomplete years (2020–2021) from a plot:

```python
plt.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2])
```
The `[:-2]` slices off the last two rows.

Select the first 10 rows for a bar chart:

```python
top10 = merged_df.head(10)
```

---

## 5. Using `.agg()` for Custom Aggregations

Calculate the **average number of parts per set** by year:

```python
parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})
parts_per_set.columns = ['avg_parts']
print(parts_per_set.head())
```

**Output:**
```
      avg_parts
year           
1949  99.600000
1950   1.000000
1953  13.500000
1954  12.357143
1955  36.607143
```

Count **unique themes** per year:

```python
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
themes_by_year.columns = ['nr_themes']
```

---

## 6. Renaming Columns

Use `.rename()` to give clearer names:

```python
themes_by_year.rename(columns={'theme_id': 'nr_themes'}, inplace=True)
```
Or assign directly after aggregation:
```python
themes_by_year.columns = ['nr_themes']
```

---

## 7. Dual‑Axis Line Charts with `twinx()`

When two variables have different scales (e.g., sets and themes), use two y‑axes:

```python
fig, ax1 = plt.subplots(figsize=(12,6))
ax1.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2], color='green')
ax1.set_ylabel('Number of Sets', color='green')

ax2 = ax1.twinx()
ax2.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2], color='blue')
ax2.set_ylabel('Number of Themes', color='blue')

plt.title('LEGO Sets and Themes Over Time')
plt.show()
```

---

## 8. Scatter Plots in Matplotlib

Visualise the trend in average parts per set:

```python
plt.figure(figsize=(12,6))
plt.scatter(parts_per_set.index[:-2], parts_per_set.avg_parts[:-2])
plt.xlabel('Year')
plt.ylabel('Average Parts')
plt.title('Average Parts per LEGO Set Over Time')
plt.show()
```

Add a trend line with `numpy.polyfit`:

```python
import numpy as np
years = parts_per_set.index[:-2]
avg = parts_per_set.avg_parts[:-2]
z = np.polyfit(years, avg, 1)
p = np.poly1d(z)
plt.plot(years, p(years), "r--")
```

---

## 9. Understanding Relational Databases: Primary & Foreign Keys

- **Primary key**: a unique identifier for each row in a table (`id` in `themes.csv`).
- **Foreign key**: a column that references a primary key in another table (`theme_id` in `sets.csv` references `themes.id`).

Example: Find all Star Wars theme IDs in `themes.csv`:

```python
themes[themes['name'] == 'Star Wars']
```

**Output:**
```
     id       name  parent_id
17   18  Star Wars        1.0
150 158  Star Wars        NaN
174 209  Star Wars      207.0
211 261  Star Wars      258.0
```

Then retrieve sets for one of those IDs:

```python
sets[sets['theme_id'] == 209][['name', 'year']].head()
```

---

## 10. Merging DataFrames with `pd.merge()`

Combine the set counts per theme with the actual theme names:

```python
set_theme_count = sets['theme_id'].value_counts().reset_index()
set_theme_count.columns = ['id', 'set_count']

merged_df = pd.merge(set_theme_count, themes, on='id')
merged_df.sort_values('set_count', ascending=False).head()
```

**Output:**
```
    id  set_count       name  parent_id
0  158        753  Star Wars        NaN
1  501        656       Gear        NaN
2  494        398    Friends        NaN
...
```

---

## 11. Creating Bar Charts

Plot the top 10 themes by number of sets:

```python
top10 = merged_df.head(10)
plt.figure(figsize=(14,8))
plt.bar(top10['name'], top10['set_count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Theme Name')
plt.ylabel('Number of Sets')
plt.title('Top 10 LEGO Themes by Number of Sets')
plt.tight_layout()
plt.show()
```

---

## 12. Final Reflections

Through this project we've:

- Answered real‑world questions about LEGO's history and product line.
- Mastered core Pandas operations: grouping, aggregating, merging.
- Learned to create informative visualisations with Matplotlib (line charts, dual‑axis plots, scatter plots, bar charts).
- Understood database concepts (primary/foreign keys) and applied them to join tables.
- Enhanced notebooks with HTML/Markdown for better documentation.

These skills are transferable to any data analysis project. Keep practicing with new datasets!

---
