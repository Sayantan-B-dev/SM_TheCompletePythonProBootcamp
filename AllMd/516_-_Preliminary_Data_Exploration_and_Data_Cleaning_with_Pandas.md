## Preliminary Data Exploration and Data Cleaning with Pandas

This section focuses on the initial steps after loading a dataset: examining its structure, identifying potential issues, and cleaning the data to ensure a reliable analysis. The operations demonstrated here are fundamental to any data science workflow and are performed using the Pandas library.

---

### 1. Understanding the Dataset Structure

Once the data is loaded into a DataFrame, the first task is to understand its dimensions and the names of its columns. This provides a high-level overview of what the dataset contains.

#### 1.1. Number of Rows and Columns

The `.shape` attribute returns a tuple representing the dimensionality of the DataFrame: `(number_of_rows, number_of_columns)`.

```python
df.shape
```

**Expected Output:**

```
(51, 6)
```

This tells us that the DataFrame has 51 rows and 6 columns. Knowing the size helps in assessing whether the data is complete and sets expectations for subsequent operations.

#### 1.2. Column Names

The `.columns` attribute returns an Index object containing the labels of all columns.

```python
df.columns
```

**Expected Output:**

```
Index(['Undergraduate Major', 'Group', 'Starting Median Salary',
       'Mid-Career Median Salary', 'Mid-Career 10th Percentile',
       'Mid-Career 90th Percentile'],
      dtype='object')
```

The column names are self-explanatory, but it is always useful to verify them. Any unexpected names or misspellings can be caught at this stage.

---

### 2. Detecting Missing Values

Missing data (often represented as `NaN`, Not a Number) can cause errors in calculations and lead to incorrect conclusions. Therefore, identifying and handling missing values is a critical step.

#### 2.1. Using `.isna()` to Find Missing Values

The `.isna()` method returns a DataFrame of the same shape as the original, where each cell is `True` if the original value is missing (or `NaN`), and `False` otherwise.

```python
df.isna()
```

**Partial Expected Output (first few rows):**

|       | Undergraduate Major | Group | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|-------|---------------------|-------|------------------------|--------------------------|----------------------------|----------------------------|
| 0     | False               | False | False                  | False                    | False                      | False                      |
| 1     | False               | False | False                  | False                    | False                      | False                      |
| ...   | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 50    | False               | False | True                   | True                     | True                       | True                       |

The output for the last row (index 50) shows `True` in all salary columns, indicating missing values. The `.isna()` method alone produces a large table; a more efficient way is to aggregate the results.

#### 2.2. Counting Missing Values per Column

Chaining `.sum()` after `.isna()` gives the count of missing values in each column.

```python
df.isna().sum()
```

**Expected Output:**

```
Undergraduate Major             0
Group                           0
Starting Median Salary          1
Mid-Career Median Salary        1
Mid-Career 10th Percentile      1
Mid-Career 90th Percentile      1
dtype: int64
```

This confirms that one row has missing values in all four salary columns.

#### 2.3. Inspecting the Problematic Rows

The `.tail()` method displays the last five rows of the DataFrame. This can help locate the row with missing values.

```python
df.tail()
```

**Expected Output:**

|     | Undergraduate Major | Group | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|-----|---------------------|-------|------------------------|--------------------------|----------------------------|----------------------------|
| 45  | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 46  | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 47  | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 48  | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 49  | ...                 | ...   | ...                    | ...                      | ...                        | ...                        |
| 50  | Spanish             | HASS  | NaN                    | NaN                      | NaN                        | NaN                        |

The last row (index 50) contains the major "Spanish" but all salary columns are `NaN`. Moreover, the preceding rows (45–49) contain valid data, so the issue is isolated to the final row. This row likely represents an artifact (e.g., a footnote) rather than actual salary data.

---

### 3. Cleaning the Data: Removing Missing Values

Because the row with missing values does not contribute useful information, it should be removed before analysis. Two common approaches are:

- **Using `.dropna()`** to automatically remove any row containing at least one missing value.
- **Using `.drop()`** to manually delete a specific row by index.

#### 3.1. Dropping Rows with Missing Values

The `.dropna()` method returns a new DataFrame with rows that contain `NaN` removed. By default, it removes any row that has at least one missing value.

```python
clean_df = df.dropna()
```

After executing this, we can verify that the missing row is gone by checking the shape and the last few rows.

```python
clean_df.shape
```

**Expected Output:**

```
(50, 6)
```

The row count decreased by one, confirming the removal.

```python
clean_df.tail()
```

**Expected Output:** The last row should now be the former index 49, containing valid data. Index 50 is no longer present.

#### 3.2. Alternative: Manual Deletion by Index

If you know the exact index of the row to delete (in this case, index 50), you can use the `.drop()` method with the `index` parameter.

```python
clean_df_v2 = df.drop(index=50)
```

This also yields a DataFrame without the last row. However, using `.dropna()` is generally safer because it catches any unexpected missing values elsewhere in the dataset.

#### 3.3. In-Place vs. Assignment

Both `.dropna()` and `.drop()` return a new DataFrame by default. To modify the original DataFrame directly, you can pass the argument `inplace=True`. However, assignment (as done above) is more explicit and generally recommended.

```python
# In-place version (not used here)
df.dropna(inplace=True)
```

---

### 4. Additional Data Exploration Tools

While the primary focus of this section is on identifying and handling missing values, other Pandas methods can provide complementary information about the dataset.

#### 4.1. Getting a Concise Summary with `.info()`

The `.info()` method prints a summary of the DataFrame, including the number of non-null entries per column and the data types.

```python
df.info()
```

**Expected Output (before cleaning):**

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 51 entries, 0 to 50
Data columns (total 6 columns):
 #   Column                        Non-Null Count  Dtype 
---  ------                        --------------  ----- 
 0   Undergraduate Major            51 non-null     object
 1   Group                          51 non-null     object
 2   Starting Median Salary         50 non-null     float64
 3   Mid-Career Median Salary       50 non-null     float64
 4   Mid-Career 10th Percentile     50 non-null     float64
 5   Mid-Career 90th Percentile     50 non-null     float64
dtypes: float64(4), object(2)
memory usage: 2.5+ KB
```

This output clearly shows that the four salary columns have only 50 non-null values, confirming the presence of one missing value.

#### 4.2. Descriptive Statistics with `.describe()`

The `.describe()` method generates summary statistics for numerical columns.

```python
df.describe()
```

**Expected Output (truncated):**

|       | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|-------|------------------------|--------------------------|----------------------------|----------------------------|
| count | 50.0                    | 50.0                     | 50.0                       | 50.0                       |
| mean  | ...                     | ...                      | ...                        | ...                        |
| std   | ...                     | ...                      | ...                        | ...                        |
| min   | ...                     | ...                      | ...                        | ...                        |
| 25%   | ...                     | ...                      | ...                        | ...                        |
| 50%   | ...                     | ...                      | ...                        | ...                        |
| 75%   | ...                     | ...                      | ...                        | ...                        |
| max   | ...                     | ...                      | ...                        | ...                        |

The `count` row confirms that 50 values are present for each salary column, again highlighting the missing row.

---

### 5. Summary of Key Operations

| Task                          | Method / Attribute       | Example Code                     |
|-------------------------------|--------------------------|----------------------------------|
| Get number of rows and columns| `.shape`                 | `df.shape`                       |
| List column names             | `.columns`               | `df.columns`                     |
| Detect missing values         | `.isna()`                | `df.isna()`                      |
| Count missing values per col  | `.isna().sum()`          | `df.isna().sum()`                |
| View last few rows            | `.tail()`                | `df.tail()`                      |
| Remove rows with missing vals | `.dropna()`              | `clean_df = df.dropna()`         |
| Get concise summary           | `.info()`                | `df.info()`                      |
| Generate descriptive stats    | `.describe()`            | `df.describe()`                  |

---

### 6. Next Steps

After cleaning the data, the DataFrame `clean_df` is ready for deeper exploration and analysis. The subsequent sections will demonstrate how to access specific columns and cells, find extreme values, sort data, and perform grouping operations.

---

**Note:** The dataset used in this analysis is from PayScale Inc. and reflects salary information for college graduates. For the most current data, refer to the [PayScale College Salary Report](https://www.payscale.com/college-salary-report).