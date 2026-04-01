## Grouping and Pivoting Data with Pandas

This section introduces the powerful `groupby` method in Pandas, which allows us to aggregate data based on categorical variables. In the context of the salaries dataset, grouping by the `Group` column (STEM, Business, HASS) enables comparison of average salaries across these broad categories. This operation is analogous to creating a pivot table in spreadsheet software and is essential for high‑level analysis.

---

### 1. The Need for Grouping

The dataset contains a column named `Group` that classifies each major into one of three categories: STEM, Business, or HASS (Humanities, Arts, and Social Science). While we can examine individual majors, we often want to answer questions like:

- Which category has the highest average starting salary?
- Do STEM degrees earn more on average than HASS degrees?
- How does the salary spread differ by category?

Grouping the data by the `Group` column and then applying aggregation functions (e.g., mean, median, count) provides answers to these questions.

---

### 2. Counting Majors per Group with `.groupby()` and `.count()`

The first step is to understand how many majors fall into each category. The `.groupby()` method splits the DataFrame into groups based on the values in the specified column. Chaining the `.count()` method returns the count of non‑null values in each column for each group.

```python
# Group the DataFrame by the 'Group' column and count the entries in each column
clean_df.groupby('Group').count()
```

**Expected Output:**

| Group    | Undergraduate Major | Spread | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|----------|---------------------|--------|------------------------|--------------------------|----------------------------|----------------------------|
| Business | 4                   | 4      | 4                      | 4                        | 4                          | 4                          |
| HASS     | 17                  | 17     | 17                     | 17                       | 17                         | 17                         |
| STEM     | 29                  | 29     | 29                     | 29                       | 29                         | 29                         |

**Interpretation:**  
The output shows the count of non‑null values in each column for each group. Since there are no missing values in the cleaned DataFrame, all counts for a given group are identical. We see that:

- **STEM** has the most majors (29), reflecting its prevalence in the dataset.
- **HASS** has 17 majors.
- **Business** has only 4 majors.

This count information is useful for understanding the composition of the dataset and for assessing the reliability of aggregated statistics (groups with few majors may have more variable averages).

**Note:** The `.count()` method counts non‑null values. If you simply want the number of rows in each group, you can use `.size()`, which returns the group size regardless of missing data. However, `.count()` is more commonly used with groupby to see counts per column.

```python
clean_df.groupby('Group').size()
```

**Expected Output:**

```
Group
Business    4
HASS       17
STEM       29
dtype: int64
```

---

### 3. Calculating Average Salaries by Group with `.mean()`

To compare average salaries across categories, we apply the `.mean()` aggregation function after grouping.

```python
clean_df.groupby('Group').mean()
```

**Expected Output (without formatting):**

| Group    | Spread      | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|----------|-------------|------------------------|--------------------------|----------------------------|----------------------------|
| Business | 74275.000000 | 49650.000000           | 89500.000000             | 48275.000000               | 122550.000000              |
| HASS     | 64276.470588 | 42605.882353           | 66676.470588             | 41452.941176               | 105729.411765              |
| STEM     | 72444.827586 | 48762.068966           | 82493.103448             | 49227.586207               | 121672.413793              |

**Interpretation (raw numbers):**

- **Business** has the highest average starting salary (~$49,650) and mid‑career salary (~$89,500).
- **STEM** follows closely with an average starting salary of ~$48,762 and mid‑career salary of ~$82,493.
- **HASS** has the lowest averages: starting ~$42,606, mid‑career ~$66,676.

The spread column shows the average difference between 90th and 10th percentiles: Business has the largest average spread (~$74,275), followed by STEM (~$72,445) and then HASS (~$64,276). This suggests that Business and STEM degrees not only offer higher average salaries but also come with greater variability (risk).

---

### 4. Improving Readability with Number Formatting

The raw output contains many decimal places and lacks commas, making it difficult to read. Pandas allows us to set a global display option to format floating‑point numbers.

```python
# Set float format to include commas and two decimal places
pd.options.display.float_format = '{:,.2f}'.format
```

After executing this line, any subsequent DataFrame output will display numbers with thousands separators and two decimal places.

**Rerun the groupby mean:**

```python
clean_df.groupby('Group').mean()
```

**Expected Output (formatted):**

| Group    | Spread     | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|----------|------------|------------------------|--------------------------|----------------------------|----------------------------|
| Business | 74,275.00  | 49,650.00              | 89,500.00                | 48,275.00                  | 122,550.00                 |
| HASS     | 64,276.47  | 42,605.88              | 66,676.47                | 41,452.94                  | 105,729.41                 |
| STEM     | 72,444.83  | 48,762.07              | 82,493.10                | 49,227.59                  | 121,672.41                 |

Now the numbers are much easier to interpret at a glance.

**Note:** This formatting applies globally for the remainder of the notebook session. To revert to default formatting, you can set `pd.options.display.float_format = None`.

---

### 5. Additional Aggregations and GroupBy Operations

The `.groupby()` method is extremely versatile. Beyond `.count()` and `.mean()`, you can apply many other aggregations:

- `.median()` – median value per group.
- `.min()` / `.max()` – minimum or maximum per group.
- `.std()` – standard deviation.
- `.agg()` – apply multiple aggregation functions simultaneously.

#### 5.1. Using `.agg()` for Multiple Statistics

```python
clean_df.groupby('Group')[['Starting Median Salary', 'Mid-Career Median Salary']].agg(['mean', 'median', 'std'])
```

**Expected Output:**

| Group    | Starting Median Salary        | Mid-Career Median Salary        |
|----------|-------------------------------|----------------------------------|
|          | mean    | median | std        | mean    | median | std        |
| Business | 49,650.00| 48,500.00| 2,640.65| 89,500.00| 87,450.00| 4,392.02|
| HASS     | 42,605.88| 41,000.00| 3,653.39| 66,676.47| 65,000.00| 6,273.01|
| STEM     | 48,762.07| 47,000.00| 7,901.33| 82,493.10| 79,000.00| 12,156.68|

This table provides a richer summary: for example, the standard deviation of starting salaries is highest in STEM, indicating greater variation among STEM majors.

#### 5.2. Accessing Group Means for a Single Column

If you only need the mean of a specific column, you can select it before or after grouping:

```python
clean_df.groupby('Group')['Starting Median Salary'].mean()
```

**Expected Output:**

```
Group
Business    49,650.00
HASS        42,605.88
STEM        48,762.07
Name: Starting Median Salary, dtype: float64
```

#### 5.3. Converting GroupBy Result to a DataFrame

By default, a groupby aggregation returns a DataFrame with the grouping column as the index. To convert it to a regular DataFrame with the grouping column as a column, use `.reset_index()`:

```python
grouped_means = clean_df.groupby('Group').mean().reset_index()
grouped_means
```

Now `grouped_means` is a DataFrame with columns: `Group`, `Spread`, `Starting Median Salary`, etc.

---

### 6. Pivot Tables: An Alternative to GroupBy

Pandas also provides the `.pivot_table()` method, which offers similar functionality with additional features like margins and different aggregation functions. While groupby is often sufficient, pivot tables can be more convenient when you want to reshape the data.

**Example: Creating a pivot table of mean salaries by group**

```python
pd.pivot_table(clean_df, 
               values=['Starting Median Salary', 'Mid-Career Median Salary'], 
               index='Group', 
               aggfunc='mean')
```

This yields the same result as the groupby mean but with a slightly different syntax. Pivot tables become especially useful when you have multiple index and column levels.

---

### 7. Extra Credit: Updating the Analysis with Current Data

The PayScale dataset used in this lesson is from 2008 and reflects the prior decade. The financial crisis of 2008 may have altered salary rankings, particularly for Business majors like Finance. As an extra credit exercise, you can use web scraping techniques (covered in Day 45) to extract current salary data from PayScale's website and repeat the groupby analysis to see if the relative standings have changed.

**Steps for extra credit:**

1. Visit the PayScale College Salary Report: [https://www.payscale.com/college-salary-report](https://www.payscale.com/college-salary-report)
2. Inspect the page to locate the table of majors and salaries.
3. Use `requests` and `BeautifulSoup` (or Selenium if the page is dynamic) to scrape the data.
4. Clean the scraped data and load it into a Pandas DataFrame.
5. Replicate the grouping analysis: count majors per category, compute average salaries, and compare with the 2008 results.
6. Document any notable changes.

**Note:** Always check the website's `robots.txt` and terms of service before scraping, and consider using official APIs if available. For educational purposes, you may also find updated datasets on Kaggle or from government sources.

---

### 8. Key Takeaways and Best Practices

- **GroupBy is for aggregation:** Use `.groupby()` to split data into groups, apply a function, and combine the results.
- **Common aggregations:** `.count()`, `.mean()`, `.median()`, `.min()`, `.max()`, `.std()`, `.agg()` for multiple functions.
- **Selecting columns:** You can select a subset of columns before or after grouping to focus on relevant data.
- **Formatting output:** Use `pd.options.display.float_format` to improve readability of numeric output.
- **Resetting index:** After groupby, the grouping column becomes the index; use `.reset_index()` to turn it back into a column if needed.
- **Pivot tables:** An alternative for more complex reshaping, but groupby is often simpler for basic aggregations.

---

### 9. Summary of GroupBy Operations

| Operation                          | Code                                               | Result                                      |
|------------------------------------|----------------------------------------------------|---------------------------------------------|
| Count per group                    | `df.groupby('col').count()`                        | Count of non‑null values in each column     |
| Mean per group                     | `df.groupby('col').mean()`                         | Mean of numeric columns per group           |
| Median per group                   | `df.groupby('col').median()`                       | Median per group                            |
| Multiple aggregations              | `df.groupby('col').agg(['mean', 'median', 'std'])` | DataFrame with multi-level columns          |
| Single column aggregation          | `df.groupby('col')['target'].mean()`               | Series with group means                      |
| Reset index                        | `df.groupby('col').mean().reset_index()`           | DataFrame with group as a column            |
| Pivot table equivalent             | `pd.pivot_table(df, values='val', index='col')`    | Similar to groupby mean                     |

---

### 10. Next Steps

With the grouping analysis complete, we have answered the core questions about salary differences across major categories. The next and final section will summarize all the learning points from this day's lesson and provide a complete overview of the techniques covered.