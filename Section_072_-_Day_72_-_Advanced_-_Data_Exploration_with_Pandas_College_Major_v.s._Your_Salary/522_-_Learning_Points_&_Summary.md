## Complete Documentation: Data Exploration of Post-University Salaries by Major

This document provides an exhaustive walkthrough of the Jupyter notebook `Data_Exploration_Pandas_College_Major_(complete).ipynb`, which analyses a dataset of salaries by college major from PayScale Inc. Every code cell, its output, and the underlying Pandas operations are explained in detail. The analysis aims to answer questions about earning potential, risk, and differences between broad categories of degrees (STEM, Business, HASS). All code examples are taken directly from the notebook, and outputs are reproduced as they appear.

---

### 1. Loading the Dataset

**Cell 1: Import Pandas**

```python
import pandas as pd
```

- **Purpose:** Import the Pandas library, which provides data structures and data analysis tools for Python. It is conventionally imported with the alias `pd`.
- **Why:** Pandas is essential for reading, manipulating, and analysing tabular data like the salary CSV.

**Cell 2: Read the CSV file**

```python
df = pd.read_csv('salaries_by_college_major.csv')
```

- **Function:** `pd.read_csv()` reads a comma-separated values file and returns a DataFrame.
- **Parameters:**
  - `'salaries_by_college_major.csv'`: the filename. The file must be in the same directory as the notebook (or a full path must be provided).
- **Result:** A DataFrame named `df` containing the data from the CSV. The first row of the CSV is automatically used as column headers.

**Cell 3: Display the first few rows**

```python
df.head()
```

- **Method:** `DataFrame.head()` returns the first 5 rows by default. It is used to quickly inspect the data and verify that it loaded correctly.
- **Output:**

|     | Undergraduate Major | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary | Group    |
|-----|---------------------|------------------------|--------------------------|-----------------------------------|------------------------------------|----------|
| 0   | Accounting          | 46000.0                | 77100.0                  | 42200.0                           | 152000.0                           | Business |
| 1   | Aerospace Engineering| 57700.0                | 101000.0                 | 64300.0                           | 161000.0                           | STEM     |
| 2   | Agriculture         | 42600.0                | 71900.0                  | 36300.0                           | 150000.0                           | Business |
| 3   | Anthropology        | 36800.0                | 61500.0                  | 33800.0                           | 138000.0                           | HASS     |
| 4   | Architecture        | 41600.0                | 76800.0                  | 50600.0                           | 136000.0                           | Business |

- **Interpretation:** The dataset contains columns for undergraduate major, starting median salary, mid‑career median salary, 10th percentile of mid‑career salary, 90th percentile of mid‑career salary, and a categorical group (STEM, Business, HASS). The presence of decimal points (`.0`) indicates that the numbers are stored as floats, which is fine for calculations.

---

### 2. Preliminary Data Exploration and Cleaning

**Cell 4: Check the shape of the DataFrame**

```python
df.shape
```

- **Attribute:** `DataFrame.shape` returns a tuple `(number_of_rows, number_of_columns)`.
- **Output:** `(51, 6)`
- **Meaning:** The DataFrame has 51 rows and 6 columns. This gives a quick idea of the dataset's size.

**Cell 5: Display column names**

```python
df.columns
```

- **Attribute:** `DataFrame.columns` returns an Index object containing the column labels.
- **Output:**

```
Index(['Undergraduate Major', 'Starting Median Salary',
       'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary',
       'Mid-Career 90th Percentile Salary', 'Group'],
      dtype='object')
```

- **Use:** Knowing column names is essential for selecting specific columns later. Notice the exact spelling and spacing; they must be used correctly in subsequent code.

**Cell 6: Detect missing values with `.isna()`**

```python
df.isna()
```

- **Method:** `DataFrame.isna()` returns a Boolean DataFrame of the same shape, where `True` indicates a missing (NaN) value.
- **Output:** A large table with 51 rows and 6 columns. Most entries are `False`, but the last row (index 50) shows `True` for all salary columns and the `Group` column. (The output is truncated in the notebook but clearly shows row 50 has `True` in those columns.)
- **Observation:** Row 50 contains missing data, which must be handled.

**Cell 7: Examine the last few rows with `.tail()`**

```python
df.tail()
```

- **Method:** `DataFrame.tail()` returns the last 5 rows by default.
- **Output:**

|     | Undergraduate Major      | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary | Group |
|-----|--------------------------|------------------------|--------------------------|-----------------------------------|------------------------------------|-------|
| 46  | Psychology               | 35900.0                | 60400.0                  | 31600.0                           | 127000.0                           | HASS  |
| 47  | Religion                 | 34100.0                | 52000.0                  | 29700.0                           | 96400.0                            | HASS  |
| 48  | Sociology                | 36500.0                | 58200.0                  | 30700.0                           | 118000.0                           | HASS  |
| 49  | Spanish                  | 34000.0                | 53100.0                  | 31000.0                           | 96400.0                            | HASS  |
| 50  | Source: PayScale Inc.    | NaN                    | NaN                      | NaN                               | NaN                                | NaN   |

- **Interpretation:** The last row (index 50) is not a valid major; it contains a source citation and missing numerical data. This row must be removed before analysis.

**Cell 8: Drop rows with missing values and verify**

```python
clean_df = df.dropna()
clean_df.tail()
```

- **Method:** `DataFrame.dropna()` removes any row that contains at least one missing value (NaN). By default, it returns a new DataFrame; the original `df` remains unchanged. Here, the result is stored in `clean_df`.
- **`clean_df.tail()` output:**

|     | Undergraduate Major | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary | Group |
|-----|---------------------|------------------------|--------------------------|-----------------------------------|------------------------------------|-------|
| 45  | Political Science   | 40800.0                | 78200.0                  | 41200.0                           | 168000.0                           | HASS  |
| 46  | Psychology          | 35900.0                | 60400.0                  | 31600.0                           | 127000.0                           | HASS  |
| 47  | Religion            | 34100.0                | 52000.0                  | 29700.0                           | 96400.0                            | HASS  |
| 48  | Sociology           | 36500.0                | 58200.0                  | 30700.0                           | 118000.0                           | HASS  |
| 49  | Spanish             | 34000.0                | 53100.0                  | 31000.0                           | 96400.0                            | HASS  |

- **Result:** The last row is now index 49 (Spanish), and there are no missing values. The cleaned DataFrame has 50 rows (originally 51). We are ready for analysis.

---

### 3. Accessing Columns and Individual Cells

**Cell 9: Find the highest starting salary**

```python
clean_df['Starting Median Salary'].max()
```

- **Method:** Selecting a column with `clean_df['column_name']` returns a Series. The `.max()` method returns the maximum value in that Series.
- **Output:** `74300.0`
- **Meaning:** The highest starting median salary among all majors is $74,300.

**Cell 10: Find the index of the highest starting salary**

```python
clean_df['Starting Median Salary'].idxmax()
```

- **Method:** `.idxmax()` returns the index label (row number) of the first occurrence of the maximum value.
- **Output:** `43`
- **Meaning:** The row with index 43 contains the major with the highest starting salary.

**Cell 11: Retrieve the salary using the index**

```python
clean_df['Starting Median Salary'][43]
```

- **Method:** Direct indexing: `clean_df['column'][index]` accesses the value at that row for the specified column.
- **Output:** `74300.0` – confirms the salary.

**Cell 12: Retrieve the major name using `.loc`**

```python
clean_df['Undergraduate Major'].loc[43]
```

- **Method:** `.loc[index]` is label‑based indexing. Here, it retrieves the value from the 'Undergraduate Major' column at index 43.
- **Output:** `'Physician Assistant'`
- **Interpretation:** The major with the highest starting salary is Physician Assistant.

**Cell 13: Alternative way using direct indexing**

```python
clean_df['Undergraduate Major'][43]
```

- **Output:** Same as above: `'Physician Assistant'`. Both notations work, but `.loc` is more explicit and recommended.

**Cell 14: Retrieve the entire row for index 43**

```python
clean_df.loc[43]
```

- **Method:** `.loc[index]` without a column specification returns the entire row as a Series.
- **Output:**

```
Undergraduate Major                  Physician Assistant
Starting Median Salary                             74300
Mid-Career Median Salary                           91700
Mid-Career 10th Percentile Salary                  66400
Mid-Career 90th Percentile Salary                 124000
Group                                               STEM
Name: 43, dtype: object
```

- **Insight:** Physician Assistant belongs to the STEM group, has a mid‑career median of $91,700, and a 90th percentile of $124,000. The spread (not yet computed) can be inferred later.

---

### 4. Highest and Lowest Earning Degrees (Solutions to Challenges)

**Cell 15: Highest mid‑career salary**

```python
print(clean_df['Mid-Career Median Salary'].max())
print(f"Index for the max mid career salary: {clean_df['Mid-Career Median Salary'].idxmax()}")
clean_df['Undergraduate Major'][8]
```

- **Explanation:**
  - `print(...)` statements display the maximum mid‑career salary and its index.
  - The last line (without `print`) automatically outputs the major name because it is the last expression in the cell.
- **Output:**
  ```
  107000.0
  Index for the max mid career salary: 8
  'Chemical Engineering'
  ```
- **Interpretation:** Chemical Engineering has the highest mid‑career median salary at $107,000.

**Cell 16: Lowest starting salary**

```python
print(clean_df['Starting Median Salary'].min())
clean_df['Undergraduate Major'].loc[clean_df['Starting Median Salary'].idxmin()]
```

- **Output:**
  ```
  34000.0
  'Spanish'
  ```
- **Interpretation:** Spanish has the lowest starting salary at $34,000.

**Cell 17: Lowest mid‑career salary (entire row)**

```python
clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()]
```

- **Output:**

```
Undergraduate Major                  Education
Starting Median Salary                   34900
Mid-Career Median Salary                 52000
Mid-Career 10th Percentile Salary        29300
Mid-Career 90th Percentile Salary       102000
Group                                     HASS
Name: 18, dtype: object
```

- **Interpretation:** Education has the lowest mid‑career median salary at $52,000. It belongs to the HASS group, with a starting salary of $34,900.

---

### 5. Adding a New Column: Spread (Risk Measure)

**Cell 18: Calculate spread and insert as a new column**

```python
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
clean_df.insert(1, 'Spread', spread_col)
clean_df.head()
```

- **Explanation:**
  - `spread_col` is a Series obtained by subtracting the 10th percentile from the 90th percentile. This arithmetic operation is element‑wise.
  - `clean_df.insert(loc, column, value)` inserts a new column at the specified position. Here `loc=1` means the new column becomes the second column (after the first column, 'Undergraduate Major').
  - `clean_df.head()` displays the first five rows to confirm the new column.
- **Output (first five rows):**

|     | Undergraduate Major   | Spread   | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary | Group    |
|-----|-----------------------|----------|------------------------|--------------------------|-----------------------------------|------------------------------------|----------|
| 0   | Accounting            | 109800.0 | 46000.0                | 77100.0                  | 42200.0                           | 152000.0                           | Business |
| 1   | Aerospace Engineering | 96700.0  | 57700.0                | 101000.0                 | 64300.0                           | 161000.0                           | STEM     |
| 2   | Agriculture           | 113700.0 | 42600.0                | 71900.0                  | 36300.0                           | 150000.0                           | Business |
| 3   | Anthropology          | 104200.0 | 36800.0                | 61500.0                  | 33800.0                           | 138000.0                           | HASS     |
| 4   | Architecture          | 85400.0  | 41600.0                | 76800.0                  | 50600.0                           | 136000.0                           | Business |

- **Interpretation:** The `Spread` column measures the range between high and low earners within each major. A smaller spread indicates more predictable earnings (lower risk). For example, Architecture has a spread of $85,400, while Agriculture has a much larger spread of $113,700.

**Cell 19: Sort by spread to find lowest‑risk majors**

```python
low_risk = clean_df.sort_values('Spread')
low_risk[['Undergraduate Major', 'Spread']].head()
```

- **Method:** `DataFrame.sort_values(by='Spread')` sorts the DataFrame in ascending order of the 'Spread' column by default. The result is stored in `low_risk`.
- **Output (top 5 smallest spread):**

|     | Undergraduate Major        | Spread   |
|-----|----------------------------|----------|
| 40  | Nursing                    | 50700.0  |
| 43  | Physician Assistant        | 57600.0  |
| 41  | Nutrition                  | 65300.0  |
| 49  | Spanish                    | 65400.0  |
| 27  | Health Care Administration | 66400.0  |

- **Interpretation:** Nursing has the smallest spread ($50,700), meaning its graduates' earnings are most tightly clustered. Physician Assistant, despite having the highest starting salary, also has a relatively low spread, indicating good earning potential with moderate risk.

---

### 6. Majors with Highest Potential and Greatest Spread

**Cell 20: Majors with highest 90th percentile (potential)**

```python
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
```

- **Explanation:** Sorting descending by the 90th percentile salary highlights majors where the top earners make the most money.
- **Output:**

|     | Undergraduate Major | Mid-Career 90th Percentile Salary |
|-----|---------------------|-----------------------------------|
| 17  | Economics           | 210000.0                          |
| 22  | Finance             | 195000.0                          |
| 8   | Chemical Engineering| 194000.0                          |
| 37  | Math                | 183000.0                          |
| 44  | Physics             | 178000.0                          |

- **Interpretation:** Economics leads with a 90th percentile of $210,000, followed by Finance, Chemical Engineering, Math, and Physics. All are either Business or STEM.

**Cell 21: Majors with greatest spread**

```python
highest_spread = clean_df.sort_values('Spread', ascending=False)
highest_spread[['Undergraduate Major', 'Spread']].head()
```

- **Output:**

|     | Undergraduate Major | Spread   |
|-----|---------------------|----------|
| 17  | Economics           | 159400.0 |
| 22  | Finance             | 147800.0 |
| 37  | Math                | 137800.0 |
| 36  | Marketing           | 132900.0 |
| 42  | Philosophy          | 132500.0 |

- **Interpretation:** Economics again tops the list, with a spread of $159,400, indicating extreme variability. Finance, Math, Marketing, and Philosophy also have wide spreads. Note that three of these (Economics, Finance, Math) also appear in the top‑potential list, illustrating the risk‑reward trade‑off.

**Cell 22: Majors with highest mid‑career median salary**

```python
highest_spread = clean_df.sort_values('Mid-Career Median Salary', ascending=False)
highest_spread[['Undergraduate Major', 'Mid-Career Median Salary']].head()
```

- **Note:** The variable name `highest_spread` is reused here, but it correctly sorts by median salary. (This is a minor inconsistency in the notebook; the intent is to see the top median salaries.)
- **Output:**

|     | Undergraduate Major | Mid-Career Median Salary |
|-----|---------------------|--------------------------|
| 8   | Chemical Engineering| 107000.0                 |
| 12  | Computer Engineering| 105000.0                 |
| 19  | Electrical Engineering| 103000.0                |
| 1   | Aerospace Engineering| 101000.0                 |
| 17  | Economics           | 98600.0                  |

- **Interpretation:** Chemical Engineering has the highest median mid‑career salary at $107,000, followed by other engineering disciplines. Economics, despite its high potential, has a slightly lower median ($98,600) than the top engineers.

---

### 7. Grouping and Pivoting Data

**Cell 23: Count majors per group**

```python
clean_df.groupby('Group').count()
```

- **Method:** `groupby('Group')` splits the DataFrame into groups based on unique values in the 'Group' column. The `.count()` method then counts the number of non‑null entries in each column for each group. Since there are no missing values, all counts are the same for a given group.
- **Output:**

| Group    | Undergraduate Major | Spread | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary |
|----------|---------------------|--------|------------------------|--------------------------|-----------------------------------|------------------------------------|
| Business | 12                  | 12     | 12                     | 12                       | 12                                | 12                                 |
| HASS     | 22                  | 22     | 22                     | 22                       | 22                                | 22                                 |
| STEM     | 16                  | 16     | 16                     | 16                       | 16                                | 16                                 |

- **Interpretation:** The dataset contains 12 Business majors, 22 HASS majors, and 16 STEM majors. This distribution is important when comparing averages, as groups with fewer majors may be more sensitive to outliers.

**Cell 24: Set float format and compute mean salaries by group**

```python
pd.options.display.float_format = '{:,.2f}'.format
clean_df.groupby('Group').mean()
```

- **`pd.options.display.float_format`:** This global setting controls how floating‑point numbers are displayed in DataFrames. The format string `'{:,.2f}'` means: print numbers with commas as thousands separators and two decimal places.
- **`.groupby('Group').mean()`** calculates the mean of all numeric columns for each group.
- **Output:**

| Group    | Spread     | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile Salary | Mid-Career 90th Percentile Salary |
|----------|------------|------------------------|--------------------------|-----------------------------------|------------------------------------|
| Business | 103,958.33 | 44,633.33              | 75,083.33                | 43,566.67                         | 147,525.00                         |
| HASS     | 95,218.18  | 37,186.36              | 62,968.18                | 34,145.45                         | 129,363.64                         |
| STEM     | 101,600.00 | 53,862.50              | 90,812.50                | 56,025.00                         | 157,625.00                         |

- **Interpretation:**
  - **Starting Salary:** STEM has the highest average starting salary ($53,862), followed by Business ($44,633) and HASS ($37,186).
  - **Mid‑Career Median Salary:** STEM also leads ($90,812), then Business ($75,083), and HASS ($62,968).
  - **Spread (Risk):** Business has the largest average spread ($103,958), indicating the greatest earnings variability, while HASS has the smallest spread ($95,218). STEM is in between ($101,600).
  - **90th Percentile (Potential):** STEM has the highest average potential ($157,625), followed by Business ($147,525) and HASS ($129,364).

These averages confirm that STEM degrees generally offer higher pay at all career stages, but also come with considerable risk (spread). Business degrees offer good potential but with the highest variability. HASS degrees have lower pay but slightly less variability.

---

### 8. Summary of Pandas Functions Used

| Function / Method                 | Description                                                                 | Example in Notebook                          |
|-----------------------------------|-----------------------------------------------------------------------------|----------------------------------------------|
| `pd.read_csv()`                   | Reads a CSV file into a DataFrame.                                          | `df = pd.read_csv('salaries...csv')`        |
| `DataFrame.head()`                | Returns first n rows (default 5).                                           | `df.head()`                                  |
| `DataFrame.tail()`                | Returns last n rows (default 5).                                            | `df.tail()`                                  |
| `DataFrame.shape`                 | Returns (rows, columns).                                                    | `df.shape`                                   |
| `DataFrame.columns`               | Returns column labels.                                                      | `df.columns`                                 |
| `DataFrame.isna()`                | Detects missing values (NaN).                                               | `df.isna()`                                  |
| `DataFrame.dropna()`              | Removes rows with any missing values.                                       | `clean_df = df.dropna()`                     |
| `Series.max()`                    | Returns maximum value in a Series.                                          | `clean_df['col'].max()`                      |
| `Series.idxmax()`                 | Returns index of first maximum value.                                       | `clean_df['col'].idxmax()`                   |
| `Series.min()`                    | Returns minimum value.                                                      | `clean_df['col'].min()`                      |
| `Series.idxmin()`                 | Returns index of first minimum value.                                       | `clean_df['col'].idxmin()`                   |
| `DataFrame.loc[]`                 | Label‑based indexing for rows and/or columns.                               | `clean_df.loc[43]`, `clean_df.loc[43, 'col']`|
| `DataFrame.insert()`              | Inserts a column at a specified position.                                   | `clean_df.insert(1, 'Spread', spread_col)`   |
| `DataFrame.sort_values()`         | Sorts DataFrame by one or more columns.                                     | `clean_df.sort_values('Spread')`             |
| `DataFrame.groupby()`             | Groups data by categorical column for aggregation.                          | `clean_df.groupby('Group').mean()`           |
| `pd.options.display.float_format` | Sets global display format for floats.                                      | `pd.options.display.float_format = '{:,.2f}'`|
| `DataFrame.count()`               | Counts non‑null values per column (used after groupby).                    | `clean_df.groupby('Group').count()`          |
| `DataFrame.mean()`                | Computes mean of numeric columns (used after groupby).                     | `clean_df.groupby('Group').mean()`           |

---

### 9. Insights and Answers to Original Questions

- **Highest starting salary:** Physician Assistant ($74,300)
- **Lowest starting salary:** Spanish ($34,000)
- **Highest mid‑career median salary:** Chemical Engineering ($107,000)
- **Lowest mid‑career median salary:** Education ($52,000)
- **Highest earning potential (90th percentile):** Economics ($210,000)
- **Lowest risk (smallest spread):** Nursing ($50,700)
- **Highest risk (largest spread):** Economics ($159,400)
- **Average salaries by group:** STEM > Business > HASS for all salary metrics. STEM also has the highest average potential, while Business has the largest average spread.

---

### 10. Extra Credit (From Original Lesson)

The notebook ends here, but the original lesson suggested scraping updated data from PayScale's website. The provided CSV is from a 2008 survey; current data might show different rankings, especially for Finance after the 2008 financial crisis. Students are encouraged to use web scraping (as learned in Day 45) to fetch recent data and repeat the analysis.

---

### 11. Conclusion

This notebook demonstrates a complete data exploration workflow using Pandas: loading data, cleaning, accessing specific values, adding columns, sorting, and grouping. Each step is accompanied by outputs that reveal meaningful patterns about salaries by college major. The analysis highlights the trade‑offs between potential earnings and risk across different degree categories.