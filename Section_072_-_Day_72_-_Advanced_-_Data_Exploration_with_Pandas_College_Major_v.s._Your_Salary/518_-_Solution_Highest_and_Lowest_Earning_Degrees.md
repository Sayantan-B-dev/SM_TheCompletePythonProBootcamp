## Solution: Highest and Lowest Earning Degrees

This section presents the solutions to the challenges posed in the previous section. The solutions demonstrate how to combine the `.max()`, `.min()`, `.idxmax()`, `.idxmin()` methods with column and row access to identify specific majors and their corresponding salary figures. Additionally, it covers practical considerations when displaying multiple outputs within a single notebook cell.

---

### 1. Recap of the Challenge

Using the cleaned DataFrame (`clean_df`), the following questions were to be answered:

1. Which college major has the highest mid‑career salary? What is that salary?
2. Which college major has the lowest starting salary? What is that salary?
3. Which college major has the lowest mid‑career salary? What is that salary?

---

### 2. Solution: Highest Mid‑Career Salary

The highest mid‑career salary can be found by applying `.max()` to the `'Mid-Career Median Salary'` column. To identify the corresponding major, we use `.idxmax()` to get the row index of the maximum value, then retrieve the major name from the `'Undergraduate Major'` column.

```python
# Find the maximum mid-career salary
max_mid_career = clean_df['Mid-Career Median Salary'].max()
print(f"Highest mid-career salary: ${max_mid_career}")

# Find the index of the row with the highest mid-career salary
idx_max_mid = clean_df['Mid-Career Median Salary'].idxmax()
print(f"Index of the row with highest mid-career salary: {idx_max_mid}")

# Retrieve the major name at that index
major_max_mid = clean_df['Undergraduate Major'].loc[idx_max_mid]
print(f"Major with highest mid-career salary: {major_max_mid}")
```

**Expected Output:**

```
Highest mid-career salary: $107000
Index of the row with highest mid-career salary: 8
Major with highest mid-career salary: Chemical Engineering
```

**Note on Multiple Outputs:**  
In a Jupyter or Colab notebook, only the last expression of a cell is automatically displayed. Therefore, to see all three pieces of information, we must explicitly use `print()` statements for each line, as shown above.

Alternatively, we could have used a single print statement with formatted string interpolation, but separating them improves readability.

---

### 3. Solution: Lowest Starting Salary

The lowest starting salary is obtained with `.min()` on the `'Starting Median Salary'` column, and the corresponding major is retrieved similarly using `.idxmin()`.

```python
# Find the minimum starting salary
min_start_salary = clean_df['Starting Median Salary'].min()
print(f"Lowest starting salary: ${min_start_salary}")

# Find the index of the row with the lowest starting salary
idx_min_start = clean_df['Starting Median Salary'].idxmin()
print(f"Index of the row with lowest starting salary: {idx_min_start}")

# Retrieve the major name at that index
major_min_start = clean_df['Undergraduate Major'].loc[idx_min_start]
print(f"Major with lowest starting salary: {major_min_start}")
```

**Expected Output:**

```
Lowest starting salary: $34000
Index of the row with lowest starting salary: 38
Major with lowest starting salary: Spanish
```

**Alternative One‑Liner Using Nested Access:**

If you prefer a more compact form, you can nest the operations:

```python
print(clean_df['Undergraduate Major'].loc[clean_df['Starting Median Salary'].idxmin()])
```

This prints the major name directly, but does not show the salary value. For clarity, it is often better to retrieve both the salary and the major explicitly.

---

### 4. Solution: Lowest Mid‑Career Salary

The same pattern is applied to the mid‑career salary column.

```python
# Find the minimum mid-career salary
min_mid_salary = clean_df['Mid-Career Median Salary'].min()
print(f"Lowest mid-career salary: ${min_mid_salary}")

# Find the index of the row with the lowest mid-career salary
idx_min_mid = clean_df['Mid-Career Median Salary'].idxmin()
print(f"Index of the row with lowest mid-career salary: {idx_min_mid}")

# Retrieve the major name at that index
major_min_mid = clean_df['Undergraduate Major'].loc[idx_min_mid]
print(f"Major with lowest mid-career salary: {major_min_mid}")
```

**Expected Output:**

```
Lowest mid-career salary: $52300
Index of the row with lowest mid-career salary: 13
Major with lowest mid-career salary: Education
```

**Retrieving the Entire Row for the Lowest Mid‑Career Salary**

If you want all available information about the major with the lowest mid‑career salary (e.g., its group, starting salary, spread, etc.), you can use `.loc` with the index obtained from `.idxmin()`.

```python
clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()]
```

**Expected Output (as a Series):**

```
Undergraduate Major                    Education
Group                                       HASS
Spread                                      46700
Starting Median Salary                      40000
Mid-Career Median Salary                    52300
Mid-Career 10th Percentile                  36700
Mid-Career 90th Percentile                  83400
Name: 13, dtype: object
```

This shows that Education, a HASS major, has a starting salary of $40,000, a mid‑career median of $52,300, and a spread (difference between 90th and 10th percentile) of $46,700.

---

### 5. Additional Considerations

#### 5.1. Handling Ties

Both `.idxmax()` and `.idxmin()` return the index of the **first** occurrence of the maximum or minimum value if there are ties. In this dataset, no ties exist among the extreme values, but in general, if multiple rows share the same extreme value, you may need to examine them all using boolean indexing.

For example, to see all majors with the lowest starting salary (if there were ties):

```python
lowest_salary = clean_df['Starting Median Salary'].min()
clean_df[clean_df['Starting Median Salary'] == lowest_salary][['Undergraduate Major', 'Starting Median Salary']]
```

#### 5.2. Using `.nlargest()` and `.nsmallest()`

Pandas also provides methods to directly retrieve the top or bottom *n* rows based on a column, without manually extracting indices.

- `.nlargest(n, column)` returns the `n` rows with the largest values in the specified column.
- `.nsmallest(n, column)` returns the `n` rows with the smallest values.

These methods return a DataFrame sorted by the column, making them convenient for quick inspections.

**Example: Top 3 majors by mid‑career salary**

```python
clean_df.nlargest(3, 'Mid-Career Median Salary')[['Undergraduate Major', 'Mid-Career Median Salary']]
```

**Expected Output:**

|     | Undergraduate Major     | Mid-Career Median Salary |
|-----|-------------------------|--------------------------|
| 8   | Chemical Engineering    | 107000                   |
| 43  | Physician Assistant     | 91700                    |
| 1   | Aerospace Engineering   | 104000                   |

**Example: Bottom 3 majors by starting salary**

```python
clean_df.nsmallest(3, 'Starting Median Salary')[['Undergraduate Major', 'Starting Median Salary']]
```

**Expected Output:**

|     | Undergraduate Major | Starting Median Salary |
|-----|---------------------|------------------------|
| 38  | Spanish             | 34000                  |
| 11  | Drama                | 35000                  |
| 12  | Education            | 40000                  |

---

### 6. Summary of Methods Used

| Method / Operation                          | Purpose                                                      |
|---------------------------------------------|--------------------------------------------------------------|
| `.max()`                                    | Returns the maximum value in a Series.                       |
| `.min()`                                    | Returns the minimum value in a Series.                       |
| `.idxmax()`                                 | Returns the index label of the first occurrence of the maximum. |
| `.idxmin()`                                 | Returns the index label of the first occurrence of the minimum. |
| `.loc[row_index, column_name]`               | Accesses a specific cell by label.                           |
| `.loc[row_index]`                           | Accesses an entire row by label.                             |
| `print()`                                   | Explicitly displays output in a notebook cell when multiple lines are present. |
| `.nlargest(n, column)`                       | Returns the top n rows sorted by column in descending order. |
| `.nsmallest(n, column)`                      | Returns the bottom n rows sorted by column in ascending order. |

---

### 7. Next Steps

Having identified the extremes, the analysis can now move toward understanding the distribution of salaries, such as the spread between high and low earners within each major, and comparing average salaries across different categories (STEM, Business, HASS). The next section will cover sorting values and adding new columns to facilitate this analysis.