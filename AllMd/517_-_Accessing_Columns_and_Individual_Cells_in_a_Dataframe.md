## Accessing Columns and Individual Cells in a Dataframe

After cleaning the dataset, the next step is to access specific parts of the DataFrame to extract meaningful information. Pandas provides multiple ways to select columns, rows, and individual cells. This section demonstrates how to retrieve data using bracket notation, the `.loc` and `.iloc` accessors, and how to combine them with aggregation methods like `.max()` and `.idxmax()` to answer questions about the data.

---

### 1. Accessing a Single Column

To access a column, use the square bracket notation with the column name as a string. This returns a **Series** (a one‑dimensional array) containing the values of that column.

```python
clean_df['Starting Median Salary']
```

**Expected Output (first few rows):**

```
0    46000
1    57200
2    42600
3    37300
4    42300
...
Name: Starting Median Salary, dtype: int64
```

The output shows the index (original row number) and the corresponding salary. The data type is integer.

#### 1.1. Selecting Multiple Columns

If you need more than one column, pass a list of column names inside the brackets. This returns a DataFrame (a subset).

```python
clean_df[['Undergraduate Major', 'Starting Median Salary']]
```

**Expected Output (first five rows):**

|     | Undergraduate Major   | Starting Median Salary |
|-----|-----------------------|------------------------|
| 0   | Accounting            | 46000                  |
| 1   | Aerospace Engineering | 57200                  |
| 2   | Agriculture           | 42600                  |
| 3   | Anthropology          | 37300                  |
| 4   | Architecture          | 42300                  |

---

### 2. Finding the Highest Starting Salary

The `.max()` method, applied to a Series, returns the maximum value.

```python
clean_df['Starting Median Salary'].max()
```

**Expected Output:**

```
74300
```

This tells us the highest starting salary among all majors is $74,300.

#### 2.1. Locating the Row with the Maximum Value

To find which major earns that salary, we need the index (row number) where the maximum occurs. The `.idxmax()` method returns the index of the first occurrence of the maximum value.

```python
clean_df['Starting Median Salary'].idxmax()
```

**Expected Output:**

```
43
```

The maximum starting salary is at row index 43.

#### 2.2. Retrieving the Corresponding Major Name

With the index, we can look up the value in the `'Undergraduate Major'` column.

**Using `.loc` with column name and index:**

```python
clean_df['Undergraduate Major'].loc[43]
```

**Expected Output:**

```
'Physician Assistant'
```

**Using double brackets (direct indexing):**

```python
clean_df['Undergraduate Major'][43]
```

Both yield the same result. The double‑bracket approach is shorter, but `.loc` is more explicit and can be safer when dealing with label‑based indexing.

#### 2.3. Retrieving the Entire Row

If you want all information about that major, use `.loc` with just the index.

```python
clean_df.loc[43]
```

**Expected Output (as a Series):**

```
Undergraduate Major              Physician Assistant
Group                                          STEM
Spread                                         81300
Starting Median Salary                         74300
Mid-Career Median Salary                       91700
Mid-Career 10th Percentile                     48200
Mid-Career 90th Percentile                     129500
Name: 43, dtype: object
```

The output shows all columns for the major at index 43. Note that the `Spread` column was added earlier; if you haven't added it, it may not appear.

---

### 3. Differences Between `.loc`, `.iloc`, and Direct Indexing

Understanding the distinction between these access methods is crucial for avoiding errors.

- **`.loc`** is label‑based. It uses the index labels (in this case, the row numbers as they appear in the DataFrame, even after reordering or dropping rows).  
  Example: `clean_df.loc[43]` accesses the row with index label 43.

- **`.iloc`** is integer position‑based. It uses the row’s position in the DataFrame (0‑based).  
  Example: `clean_df.iloc[0]` returns the first row.

- **Direct indexing** like `clean_df['Undergraduate Major'][43]` works because Pandas first selects the column (Series) and then uses the index label to get the value. However, this can cause ambiguity if the index is not unique or if you mix label and position. It is generally recommended to use `.loc` for clarity.

#### 3.1. Example Using `.iloc`

To get the first row (position 0):

```python
clean_df.iloc[0]
```

**Expected Output:** The first row of the DataFrame (index 0 in this case, which is Accounting).

---

### 4. Challenge: Highest and Lowest Earning Degrees

Based on the techniques shown, the following challenges can be solved:

- Which major has the highest mid‑career salary? How much do graduates with this major earn?
- Which major has the lowest starting salary and how much do graduates earn after university?
- Which major has the lowest mid‑career salary and how much can people expect to earn with this degree?

#### 4.1. Solution: Highest Mid‑Career Salary

```python
# Find the maximum mid-career salary
max_mid = clean_df['Mid-Career Median Salary'].max()
print(f"Highest mid-career salary: ${max_mid}")

# Find the index of that maximum
idx_max_mid = clean_df['Mid-Career Median Salary'].idxmax()
print(f"Index of max mid-career salary: {idx_max_mid}")

# Retrieve the major name
major_max_mid = clean_df['Undergraduate Major'].loc[idx_max_mid]
print(f"Major with highest mid-career salary: {major_max_mid}")
```

**Expected Output:**

```
Highest mid-career salary: $107000
Index of max mid-career salary: 8
Major with highest mid-career salary: Chemical Engineering
```

#### 4.2. Solution: Lowest Starting Salary

```python
min_start = clean_df['Starting Median Salary'].min()
idx_min_start = clean_df['Starting Median Salary'].idxmin()
major_min_start = clean_df['Undergraduate Major'].loc[idx_min_start]
print(f"Lowest starting salary: ${min_start} for {major_min_start}")
```

**Expected Output:**

```
Lowest starting salary: $34000 for Spanish
```

#### 4.3. Solution: Lowest Mid‑Career Salary

```python
min_mid = clean_df['Mid-Career Median Salary'].min()
idx_min_mid = clean_df['Mid-Career Median Salary'].idxmin()
major_min_mid = clean_df['Undergraduate Major'].loc[idx_min_mid]
print(f"Lowest mid-career salary: ${min_mid} for {major_min_mid}")
```

**Expected Output:**

```
Lowest mid-career salary: $52300 for Education
```

You can also retrieve the entire row for the lowest mid‑career salary:

```python
clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()]
```

This returns a Series with all details for the Education major.

---

### 5. Additional Column Operations

#### 5.1. Checking Data Types

The `.dtypes` attribute shows the data type of each column.

```python
clean_df.dtypes
```

**Expected Output:**

```
Undergraduate Major              object
Spread                             int64
Group                             object
Starting Median Salary             int64
Mid-Career Median Salary           int64
Mid-Career 10th Percentile         int64
Mid-Career 90th Percentile         int64
dtype: object
```

#### 5.2. Value Counts for a Categorical Column

To see how many majors belong to each group category:

```python
clean_df['Group'].value_counts()
```

**Expected Output:**

```
STEM        29
HASS        17
Business     4
Name: Group, dtype: int64
```

This shows that STEM majors are the most numerous in the dataset, followed by HASS and Business.

#### 5.3. Descriptive Statistics for a Column

The `.describe()` method works on a Series as well, providing count, mean, standard deviation, min, quartiles, and max.

```python
clean_df['Starting Median Salary'].describe()
```

**Expected Output:**

```
count      50.000000
mean     47380.000000
std       7465.646426
min      34000.000000
25%      41000.000000
50%      45500.000000
75%      52500.000000
max      74300.000000
Name: Starting Median Salary, dtype: float64
```

---

### 6. Common Pitfalls and Best Practices

- **Using `.loc` vs direct indexing:** When you have a DataFrame with a custom index (e.g., after sorting), direct indexing `df['col'][index]` still uses the original labels, which is fine, but `.loc` makes it explicit. For integer positions, use `.iloc`.
- **Chained indexing:** Avoid something like `df[df['col'] > 100]['col']` as it may produce unpredictable results. Instead, use `.loc` with a condition.
- **Missing indices:** After dropping rows, the index labels remain the same. If you need a fresh sequential index, use `.reset_index(drop=True)`.

```python
clean_df = clean_df.reset_index(drop=True)
```

This renumbers rows from 0 to 49.

---

### 7. Summary of Key Methods

| Task                                  | Method/Notation                        | Example                                      |
|---------------------------------------|----------------------------------------|----------------------------------------------|
| Access a single column                | `df['col']`                            | `clean_df['Starting Median Salary']`         |
| Access multiple columns               | `df[['col1', 'col2']]`                 | `clean_df[['Major','Salary']]`               |
| Maximum value in a column             | `.max()`                               | `clean_df['Salary'].max()`                    |
| Index of maximum value                | `.idxmax()`                            | `clean_df['Salary'].idxmax()`                  |
| Access cell by row label and column   | `.loc[row, col]`                       | `clean_df.loc[43, 'Undergraduate Major']`     |
| Access row by label                   | `.loc[row]`                            | `clean_df.loc[43]`                            |
| Access row by integer position        | `.iloc[pos]`                           | `clean_df.iloc[0]`                             |
| Minimum value in a column             | `.min()`                               | `clean_df['Salary'].min()`                    |
| Index of minimum value                | `.idxmin()`                            | `clean_df['Salary'].idxmin()`                  |
| Data types of columns                 | `.dtypes`                              | `clean_df.dtypes`                             |
| Value counts for categorical column   | `.value_counts()`                      | `clean_df['Group'].value_counts()`            |

---

### 8. Next Steps

Now that you can pinpoint specific values and rows, you are ready to perform more complex operations such as sorting the DataFrame, adding new columns, and grouping by categories to compare average salaries across major groups.

---

**Resource:**  
Pandas documentation on indexing: [Indexing and Selecting Data](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html)