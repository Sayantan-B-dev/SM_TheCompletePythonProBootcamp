## Exploring Post-University Salaries by Major with Pandas

This documentation provides a comprehensive walkthrough of the data analysis process using Pandas, based on the PayScale dataset of salaries by college major. The goal is to explore, clean, and analyze the data to answer key questions about earnings across different degree programs. Each section corresponds to a step in the workflow, with detailed explanations, code examples, and expected outputs.

---

### Overview and Learning Objectives

The dataset originates from a year-long survey conducted by PayScale Inc., involving 1.2 million Americans holding only a bachelor's degree. The survey captures salary information at different career stages, allowing us to investigate:

- Which majors yield the highest starting salaries?
- Which majors have the lowest earnings immediately after college?
- Which degrees offer the greatest earning potential over a career?
- Which majors are considered low‑risk, i.e., have a narrow range between low and high earners?
- How do broad categories (STEM, Business, HASS) compare in average earnings?

By the end of this analysis, you will be familiar with fundamental Pandas operations for data exploration, cleaning, selection, sorting, grouping, and column manipulation.

---

### Setting Up the Environment

Two common environments for data science work are **Google Colab** (cloud‑based) and **Jupyter Notebook** (local via Anaconda). Both support the notebook format where code, output, and narrative text coexist.

**Google Colab Setup**

1. Open your Google Drive.
2. Click **New** → **More** → **Google Colaboratory**. If the option is not visible, go to **Connect more apps**, search for “Colaboratory”, and install it.
3. A new notebook opens in your browser. It automatically connects to a runtime (free CPU/GPU provided by Google).

**Alternative: Local Jupyter Notebook with Anaconda**

- Download and install Anaconda from [anaconda.com](https://www.anaconda.com/).
- Launch Jupyter Notebook from the Anaconda Navigator or terminal.
- Create a new notebook (Python 3 kernel).

**Notebook Basics**

- A notebook consists of cells that can contain code or markdown text.
- Execute a cell by pressing **Shift+Enter**. The output appears directly below the cell.
- Variables and data persist across cells as long as the kernel is running.

---

### Loading the Dataset

Download the dataset file `salaries_by_college_major.csv` from the course resources. Upload it to your notebook’s working directory.

**In Google Colab:**

- Click the folder icon on the left sidebar.
- Use the upload button to add the CSV file.

**Import Pandas and Read the CSV**

```python
import pandas as pd

df = pd.read_csv('salaries_by_college_major.csv')
```

**View the First Few Rows**

```python
df.head()
```

**Expected Output:**

A table showing the first five rows of the dataframe. Each row represents a college major, with columns for undergraduate major, group category, starting median salary, mid‑career median salary, mid‑career 10th percentile, and mid‑career 90th percentile.

| Undergraduate Major | Group | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|---------------------|-------|------------------------|--------------------------|----------------------------|----------------------------|
| Accounting          | Business | 46000                  | 77100                    | 43300                      | 124000                     |
| ...                 | ...   | ...                    | ...                      | ...                        | ...                        |

---

### Initial Data Exploration and Cleaning

Before analysis, understand the dataframe’s structure and check for missing or problematic data.

**Number of Rows and Columns**

```python
df.shape
```

**Output:** `(51, 6)` – 51 rows and 6 columns.

**Column Names**

```python
df.columns
```

**Output:** `Index(['Undergraduate Major', 'Group', 'Starting Median Salary', 'Mid-Career Median Salary', 'Mid-Career 10th Percentile', 'Mid-Career 90th Percentile'], dtype='object')`

**Check for Missing Values**

The `.isna()` method returns a boolean dataframe indicating where values are missing.

```python
df.isna()
```

Scanning the output, you may notice that the last few rows contain `True` for some columns.

**Inspect the Last Rows**

```python
df.tail()
```

**Output:** The final row (index 50) contains descriptive text about the data source, with all salary columns empty (NaN). This row is not useful for analysis.

**Remove the Last Row (Missing Values)**

Two approaches:

1. **Drop any row containing NaN** using `.dropna()`.
2. **Manually drop by index** (e.g., `df.drop(50, inplace=True)`).

We'll use `.dropna()` to create a clean dataframe:

```python
clean_df = df.dropna()
```

Verify the change:

```python
clean_df.tail()
```

Now the last row should be index 49, containing valid data. The shape will be `(50, 6)`.

---

### Accessing Columns and Individual Cells

**Retrieve a Single Column**

```python
clean_df['Starting Median Salary']
```

This returns a Pandas Series with all values from that column.

**Find the Maximum Value in a Column**

```python
clean_df['Starting Median Salary'].max()
```

**Output:** `74300`

**Find the Index of the Maximum Value**

```python
clean_df['Starting Median Salary'].idxmax()
```

**Output:** `43` (the row index where starting salary is highest).

**Retrieve the Corresponding Major Name**

Using `.loc` with both column and index:

```python
clean_df['Undergraduate Major'].loc[43]
```

**Output:** `'Physician Assistant'`

Alternatively, using double brackets:

```python
clean_df['Undergraduate Major'][43]
```

**Retrieve an Entire Row**

```python
clean_df.loc[43]
```

**Output:** A Series showing all data for the major at index 43.

---

### Challenge: Highest and Lowest Earning Degrees

Based on the above techniques, answer:

1. Which major has the highest mid‑career salary? What is that salary?
2. Which major has the lowest starting salary, and what is it?
3. Which major has the lowest mid‑career salary, and what is it?

**Solutions**

**Highest Mid‑Career Salary**

```python
max_mid_career = clean_df['Mid-Career Median Salary'].max()
print(f"Highest mid-career salary: {max_mid_career}")
idx_max_mid = clean_df['Mid-Career Median Salary'].idxmax()
major_max_mid = clean_df['Undergraduate Major'][idx_max_mid]
print(f"Major with highest mid-career salary: {major_max_mid}")
```

**Output:**

```
Highest mid-career salary: 107000
Major with highest mid-career salary: Chemical Engineering
```

**Lowest Starting Salary**

```python
min_start = clean_df['Starting Median Salary'].min()
idx_min_start = clean_df['Starting Median Salary'].idxmin()
major_min_start = clean_df['Undergraduate Major'][idx_min_start]
print(f"Lowest starting salary: {min_start} for {major_min_start}")
```

**Output:**

```
Lowest starting salary: 34000 for Spanish
```

**Lowest Mid‑Career Salary**

```python
min_mid = clean_df['Mid-Career Median Salary'].min()
idx_min_mid = clean_df['Mid-Career Median Salary'].idxmin()
major_min_mid = clean_df['Undergraduate Major'][idx_min_mid]
print(f"Lowest mid-career salary: {min_mid} for {major_min_mid}")
```

**Output:**

```
Lowest mid-career salary: 52300 for Education
```

You can also retrieve the entire row for the lowest mid‑career salary:

```python
clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()]
```

---

### Sorting Values and Adding Columns: Potential vs. Risk

**Calculating the Spread Between High and Low Earners**

The difference between the 90th percentile and 10th percentile mid‑career salaries indicates the degree’s risk: a smaller spread suggests more predictable earnings.

```python
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
```

**Insert the New Column into the Dataframe**

Use `.insert()` to place it at a specific position (e.g., as the second column, index 1).

```python
clean_df.insert(1, 'Spread', spread_col)
clean_df.head()
```

Now the dataframe has a new column named `Spread`.

**Sorting by Spread to Find Lowest‑Risk Majors**

```python
low_risk = clean_df.sort_values('Spread')
low_risk[['Undergraduate Major', 'Spread']].head()
```

**Output:** The majors with the smallest spread (most predictable earnings) appear at the top. For example, “Accounting” might show a spread of 52,000, while “Education” could have a very narrow spread.

**Sorting by Spread in Descending Order (Highest Spread)**

```python
high_spread = clean_df.sort_values('Spread', ascending=False)
high_spread[['Undergraduate Major', 'Spread']].head()
```

**Output:** Majors with the largest spread, indicating a wide gap between high and low earners. Economics, Finance, and Physics often appear here.

**Sorting by Mid‑Career 90th Percentile (Highest Potential)**

```python
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
```

**Output:** Majors like Economics, Finance, and Physics lead in top‑end earnings potential.

Notice that some majors (e.g., Economics) appear in both high‑spread and high‑potential lists – they offer both high upside and high variability.

---

### Grouping and Pivoting Data

To compare average salaries across broad categories, use the `.groupby()` method, which works like a pivot table.

**Count Majors per Group**

```python
clean_df.groupby('Group').count()
```

**Output:** A table showing the number of majors in each category (STEM, HASS, Business) and counts for each column (all identical because no missing values).

**Calculate Average Salary by Group**

```python
clean_df.groupby('Group').mean()
```

**Output:** The mean starting salary, mid‑career salary, etc., for each group. The numbers may be hard to read because of long decimals.

**Improve Number Formatting**

Set a global display option to format floats with commas and two decimals:

```python
pd.options.display.float_format = '{:,.2f}'.format
```

Now rerun the mean:

```python
clean_df.groupby('Group').mean()
```

**Output:** Numbers like 49,000.00 instead of 49000.1234.

**Interpretation:** Typically, STEM degrees show the highest average salaries, followed by Business, then HASS.

---

### Extra Credit: Updated Data

The original PayScale dataset is from 2008, reflecting the decade prior. Given the 2008 financial crisis, salary rankings may have shifted. Using web scraping skills (Day 45), you can fetch current data from PayScale’s website and repeat the analysis. This demonstrates the importance of keeping analyses up‑to‑date.

---

### Summary of Pandas Techniques Learned

- **Exploration:** `.head()`, `.tail()`, `.shape`, `.columns`
- **Missing data detection and cleaning:** `.isna()`, `.dropna()`
- **Column access:** `df['col']` or `df[['col1', 'col2']]`
- **Cell access:** `df['col'][index]` or `df.loc[index, 'col']`
- **Aggregates:** `.max()`, `.min()`, `.idxmax()`, `.idxmin()`
- **Sorting:** `.sort_values()`
- **Adding columns:** `.insert()`
- **Grouping and aggregation:** `.groupby().mean()`
- **Display formatting:** `pd.options.display.float_format`

These operations form the foundation for any data exploration task in Pandas. By applying them to the salary dataset, you have gained insight into the earning outcomes of different college majors.

---

**Resources:**

- [Pandas Documentation: sort_values](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html)
- [PayScale College Salary Report](https://www.payscale.com/college-salary-report) (for updated data)

The completed notebook with all code and outputs is available in the course resources.