## Sorting Values and Adding Columns: Majors with the Most Potential vs Lowest Risk

After identifying the extremes (highest and lowest salaries), the next step is to understand the variability within each major. This section focuses on calculating the spread between high and low earners for each degree and using sorting to identify which majors offer the most predictable salaries (lowest risk) and which have the greatest earning potential (highest 90th percentile). Additionally, we introduce how to add new columns to a DataFrame and sort data based on column values.

---

### 1. Defining Risk and Potential

In the context of salary data, **risk** refers to the uncertainty in earnings. A major with a small difference between the 10th percentile and 90th percentile mid‑career salaries is considered low‑risk because most graduates earn within a narrow band. Conversely, a large spread indicates high risk: some graduates earn very little while others earn a great deal.

**Potential** is represented by the 90th percentile salary – the earnings of the top 10% of graduates in that major. High potential means that exceptional earners in that field command very high salaries.

---

### 2. Calculating the Spread

The spread is defined as:

\[
\text{Spread} = \text{Mid-Career 90th Percentile Salary} - \text{Mid-Career 10th Percentile Salary}
\]

Pandas allows arithmetic operations on entire columns, making this calculation straightforward.

#### 2.1. Direct Subtraction

```python
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
```

`spread_col` is a Pandas Series containing the computed spread for each major.

#### 2.2. Using the `.subtract()` Method

Alternatively, you can use the `.subtract()` method, which achieves the same result.

```python
spread_col = clean_df['Mid-Career 90th Percentile Salary'].subtract(clean_df['Mid-Career 10th Percentile Salary'])
```

Both approaches yield identical Series.

---

### 3. Adding the Spread Column to the DataFrame

Once computed, the spread can be inserted into the original DataFrame as a new column. The `.insert()` method allows us to specify the position of the new column.

```python
clean_df.insert(1, 'Spread', spread_col)
```

- The first argument (`1`) is the integer position where the column should be inserted. Column positions start at 0. Inserting at position 1 means the new column becomes the second column (right after the first column, which is `Undergraduate Major`).
- The second argument is the name of the new column, here `'Spread'`.
- The third argument is the data to populate the column – the Series `spread_col`.

**Verification:**

```python
clean_df.head()
```

**Expected Output:**

|     | Undergraduate Major   | Spread | Group    | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|-----|-----------------------|--------|----------|------------------------|--------------------------|----------------------------|----------------------------|
| 0   | Accounting            | 80700  | Business | 46000                  | 77100                    | 43300                      | 124000                     |
| 1   | Aerospace Engineering | 82600  | STEM     | 57200                  | 104000                   | 60400                      | 143000                     |
| 2   | Agriculture           | 58700  | STEM     | 42600                  | 69100                    | 42300                      | 101000                     |
| 3   | Anthropology          | 52800  | HASS     | 37300                  | 61300                    | 35600                      | 88400                      |
| 4   | Architecture          | 80600  | STEM     | 42300                  | 76400                    | 40400                      | 121000                     |

Now the DataFrame contains the spread as the second column.

---

### 4. Sorting the DataFrame by Spread

To identify majors with the lowest risk (smallest spread) or highest risk (largest spread), we use the `.sort_values()` method. This method sorts the DataFrame based on the values in one or more columns.

#### 4.1. Sorting in Ascending Order (Smallest Spread First)

```python
low_risk = clean_df.sort_values('Spread')
```

By default, `sort_values` sorts in ascending order. To view only the major name and its spread, we can select a subset of columns.

```python
low_risk[['Undergraduate Major', 'Spread']].head()
```

**Expected Output (top 5 lowest spread):**

|     | Undergraduate Major | Spread |
|-----|---------------------|--------|
| 13  | Education           | 46700  |
| 12  | Drama               | 47900  |
| 9   | Criminal Justice    | 48000  |
| 38  | Spanish             | 48500  |
| 39  | Theology            | 50300  |

These majors have the smallest gap between the 10th and 90th percentile earners, indicating more predictable salaries.

#### 4.2. Sorting in Descending Order (Largest Spread First)

To see the majors with the greatest spread (highest risk), set `ascending=False`.

```python
high_spread = clean_df.sort_values('Spread', ascending=False)
high_spread[['Undergraduate Major', 'Spread']].head()
```

**Expected Output (top 5 highest spread):**

|     | Undergraduate Major | Spread |
|-----|---------------------|--------|
| 17  | Economics           | 120600 |
| 8   | Chemical Engineering| 104400 |
| 1   | Aerospace Engineering | 82600 |
| 41  | Finance             | 82500  |
| 20  | Physics             | 82000  |

These majors exhibit a wide range of earnings, meaning some graduates earn much more than others.

---

### 5. Sorting by 90th Percentile to Find Highest Potential

The 90th percentile salary represents the top earners. Sorting by this column reveals which majors offer the greatest earning potential.

```python
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
```

**Expected Output (top 5 by 90th percentile):**

|     | Undergraduate Major | Mid-Career 90th Percentile Salary |
|-----|---------------------|-----------------------------------|
| 17  | Economics           | 181000                            |
| 8   | Chemical Engineering| 162000                            |
| 41  | Finance             | 148000                            |
| 20  | Physics             | 147000                            |
| 1   | Aerospace Engineering | 143000                          |

Note that Economics, which also has a large spread, tops the list for potential. This illustrates the trade‑off: high potential often comes with high variability.

---

### 6. Understanding the `.sort_values()` Method

The `.sort_values()` method accepts several useful parameters:

- **`by`**: column name or list of column names to sort by.
- **`ascending`**: boolean or list of booleans (default True). If a list, must match the length of `by`.
- **`inplace`**: if True, modifies the DataFrame directly; otherwise returns a new DataFrame (default False).
- **`na_position`**: where to put NaN values, either `'first'` or `'last'` (default `'last'`).

**Example: Sorting by multiple columns**

To sort first by group, then by starting salary within each group:

```python
clean_df.sort_values(['Group', 'Starting Median Salary'], ascending=[True, False]).head()
```

#### 6.1. Quick Documentation

In a notebook, you can view the full documentation of any method by placing the cursor inside the parentheses and pressing **Shift+Tab**. This brings up a popup with the method signature and description.

---

### 7. Challenge

Using the `.sort_values()` method, find:

1. The top 5 degrees with the highest values in the 90th percentile (already done above).
2. The degrees with the greatest spread in salaries (already done above).

The solution will be provided in the next section.

---

### 8. Additional Considerations

#### 8.1. Preserving the Original Index After Sorting

When you sort a DataFrame, the row indices remain associated with their original rows. This is useful because you can still use `.loc` with the original index labels. However, if you want a new sequential index, you can use `.reset_index(drop=True)`.

```python
sorted_df = clean_df.sort_values('Spread').reset_index(drop=True)
```

Now the first row has index 0, second row index 1, etc.

#### 8.2. Using `.nlargest()` and `.nsmallest()` as Alternatives

Instead of sorting the entire DataFrame, you can directly retrieve the top or bottom *n* rows using `.nlargest()` and `.nsmallest()`. These methods are more efficient when you only need a few rows.

**Example: Top 5 by 90th percentile**

```python
clean_df.nlargest(5, 'Mid-Career 90th Percentile Salary')[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']]
```

This returns the same result as sorting descending and taking head, but without rearranging the entire DataFrame.

#### 8.3. Interpreting the Spread

The spread is measured in dollars. A spread of $120,600 (Economics) means that the top 10% of earners earn $120,600 more than the bottom 10%. This indicates a highly unequal distribution of earnings within that major.

---

### 9. Summary of Operations

| Operation                              | Code                                                     |
|----------------------------------------|----------------------------------------------------------|
| Subtract two columns                   | `df['col1'] - df['col2']`                                |
| Insert new column at specific position | `df.insert(pos, 'new_col', data)`                        |
| Sort by column (ascending)             | `df.sort_values('col')`                                  |
| Sort by column (descending)            | `df.sort_values('col', ascending=False)`                 |
| Sort by multiple columns               | `df.sort_values(['col1','col2'], ascending=[True,False])`|
| Get top n rows by column               | `df.nlargest(n, 'col')`                                  |
| Get bottom n rows by column            | `df.nsmallest(n, 'col')`                                 |

---

### 10. Next Steps

The next section will provide the solution to the challenge and further explore the relationship between potential and risk. Following that, we will move on to grouping data by category to compare average salaries across STEM, Business, and HASS majors.

---

**Resource:**  
Pandas documentation on sorting: [pandas.DataFrame.sort_values](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html)