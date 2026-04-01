# Finding the Oldest and Largest LEGO Sets

## Overview

Now that we've explored the colours dataset, it's time to dive into the `sets.csv` file. This dataset contains information about individual LEGO sets released over the years. By analyzing it, we can answer:

- When did LEGO release its first sets, and what were they called?
- How many sets were available in the company's first year?
- Which sets have the most pieces (the largest sets ever)?

We'll use pandas to read, filter, sort, and summarise the data.

---

## 1. Loading and Inspecting `sets.csv`

First, import pandas and read the CSV file.

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')
```

Take a look at the first few rows to understand the structure:

```python
sets.head()
```

**Output:**

| set_num | name                        | year | theme_id | num_parts |
|---------|-----------------------------|------|----------|-----------|
| 001-1   | Gears                       | 1965 | 1        | 43        |
| 0011-2  | Town Mini-Figures           | 1978 | 84       | 12        |
| 0011-3  | Castle 2 for 1 Bonus Offer  | 1987 | 199      | 0         |
| 0012-1  | Space Mini-Figures          | 1979 | 143      | 12        |
| 0013-1  | Space Mini-Figures          | 1979 | 143      | 12        |

**Observations:**
- `set_num`: unique identifier for each set.
- `name`: descriptive name of the set.
- `year`: release year.
- `theme_id`: numeric code linking to the `themes.csv` file (foreign key).
- `num_parts`: number of pieces in the set (0 indicates missing or promotional items).

---

## 2. Finding the Earliest LEGO Sets

To find the first sets ever released, we sort the DataFrame by the `year` column in ascending order.

```python
# Sort by year (oldest first)
earliest_sets = sets.sort_values('year')
earliest_sets.head()
```

**Output:**

|      | set_num | name                               | year | theme_id | num_parts |
|------|---------|------------------------------------|------|----------|-----------|
| 9521 | 700.1-1 | Extra-Large Gift Set (ABB)         | 1949 | 365      | 142       |
| 9534 | 700.2-1 | Large Gift Set (ABB)               | 1949 | 365      | 178       |
| 9539 | 700.3-1 | Medium Gift Set (ABB)              | 1949 | 365      | 142       |
| 9544 | 700.A-1 | Small Brick Set (ABB)              | 1949 | 371      | 24        |
| 9545 | 700.B-1 | Small Doors and Windows Set (ABB)  | 1949 | 371      | 12        |

**Insight:** The first LEGO sets were released in **1949**. They were simple sets with names like "Extra-Large Gift Set" and "Small Brick Set". The "(ABB)" likely stands for "Automatic Binding Bricks", the original name for LEGO bricks.

---

## 3. How Many Sets Were Sold in the First Year?

We can filter the DataFrame to include only rows where `year` is 1949, then count the rows.

```python
sets_1949 = sets[sets['year'] == 1949]
print("Number of sets in 1949:", len(sets_1949))
```

**Output:**
```
Number of sets in 1949: 5
```

Alternatively, we can display the actual sets:

```python
sets_1949[['name', 'num_parts']]
```

**Output:**

| name                               | num_parts |
|------------------------------------|-----------|
| Extra-Large Gift Set (ABB)         | 142       |
| Large Gift Set (ABB)               | 178       |
| Medium Gift Set (ABB)              | 142       |
| Small Brick Set (ABB)              | 24        |
| Small Doors and Windows Set (ABB)  | 12        |

So, LEGO started with just **5 different products** in 1949.

---

## 4. Finding the Largest LEGO Sets (Most Parts)

To find the sets with the most pieces, we sort by `num_parts` in descending order.

```python
largest_sets = sets.sort_values('num_parts', ascending=False)
largest_sets.head()
```

**Output:**

| set_num   | name                           | year | theme_id | num_parts |
|-----------|--------------------------------|------|----------|-----------|
| BIGBOX-1  | The Ultimate Battle for Chima  | 2015 | 571      | 9987      |
| 75192-1   | UCS Millennium Falcon          | 2017 | 171      | 7541      |
| 71043-1   | Hogwarts Castle                | 2018 | 246      | 6020      |
| 10256-1   | Taj Mahal                      | 2017 | 673      | 5923      |
| 10189-1   | Taj Mahal                      | 2008 | 673      | 5922      |

**Top 5 Largest Sets (by piece count):**

1. **The Ultimate Battle for Chima** (2015) – 9,987 pieces  
   *(Note: This was a promotional set; only two were ever produced.)*
2. **UCS Millennium Falcon** (2017) – 7,541 pieces  
   *(The largest commercially available set.)*
3. **Hogwarts Castle** (2018) – 6,020 pieces
4. **Taj Mahal** (2017) – 5,923 pieces
5. **Taj Mahal** (2008) – 5,922 pieces

> **Interesting fact:** Two different versions of the Taj Mahal appear in the top five, showing that large landmark sets are popular.

---

## 5. Additional Observations

- Some sets have `num_parts = 0`. These are often promotional items, keychains, or sets where the piece count is unknown. For example, `0011-3` (Castle 2 for 1 Bonus Offer) has 0 parts.
- The `theme_id` column allows us to later merge with `themes.csv` to get actual theme names (like "Star Wars", "Technic", etc.).
- The `set_num` often contains a suffix like `-1`, indicating the version of the set.

---

## 6. Complete Code for This Section

```python
import pandas as pd

# Load data
sets = pd.read_csv('data/sets.csv')

# 1. Earliest sets
earliest = sets.sort_values('year').head()
print("Earliest sets:")
print(earliest[['year', 'name', 'num_parts']])

# 2. Number of sets in 1949
sets_1949 = sets[sets['year'] == 1949]
print("\nSets in 1949:", len(sets_1949))

# 3. Largest sets
largest = sets.sort_values('num_parts', ascending=False).head()
print("\nLargest sets (by parts):")
print(largest[['name', 'year', 'num_parts']])
```

**Expected Output:**
```
Earliest sets:
   year                               name  num_parts
0  1949         Extra-Large Gift Set (ABB)        142
1  1949               Large Gift Set (ABB)        178
2  1949              Medium Gift Set (ABB)        142
3  1949              Small Brick Set (ABB)         24
4  1949  Small Doors and Windows Set (ABB)         12

Sets in 1949: 5

Largest sets (by parts):
                           name  year  num_parts
0  The Ultimate Battle for Chima  2015       9987
1          UCS Millennium Falcon  2017       7541
2                Hogwarts Castle  2018       6020
3                      Taj Mahal  2017       5923
4                      Taj Mahal  2008       5922
```

---

## 7. Markdown Enhancement

To make the notebook look professional, add a heading and an image. For example:

```html
<h1>Finding the Oldest and Largest LEGO Sets</h1>

<img src="https://i.imgur.com/whB1olq.png" width="600">

<p>Let's explore the sets dataset to discover LEGO's origins and the biggest builds ever.</p>
```

This will create a visually appealing section with context.

---

## 8. Key Takeaways

- LEGO's first sets date back to **1949** with only **5 products**.
- The largest set ever (by piece count) is the promotional **"The Ultimate Battle for Chima"** with nearly 10,000 pieces.
- The largest commercially available set is the **UCS Millennium Falcon** (7,541 pieces).
- Sorting and filtering are fundamental operations for extracting insights from tabular data.

---

## 9. Next Steps

Now that we know the oldest and largest sets, the next lesson will focus on visualizing how the number of sets released has changed over time using line charts.

---

