## Project Overview: Analyzing Programming Language Popularity

This project aims to determine the popularity of various programming languages over time by analyzing data from Stack Overflow. Stack Overflow, a widely used question-and-answer platform for programmers, tags each post with the programming language it relates to. By counting the number of posts associated with each language tag, we can gauge the relative popularity and track trends across different time periods. The analysis will leverage Python's data manipulation and visualization libraries—Pandas and Matplotlib—to process, reshape, and visualize time-series data.

### Objectives

The primary goals of this analysis are:

1. **Data Acquisition and Preliminary Exploration**: Load the provided dataset (or optionally fetch fresh data via a StackExchange query) and perform initial inspections to understand its structure, dimensions, and any missing values.

2. **Data Cleaning and Transformation**: Convert date strings into proper datetime objects for easier manipulation and plotting. Reshape the data so that each programming language becomes its own column, with rows representing monthly post counts. Handle missing values appropriately (e.g., fill with zeros) to prepare for visualization.

3. **Data Analysis and Grouping**: Use Pandas' `groupby()` to aggregate posts per language and count the number of monthly entries per language. This step reveals the total posts for each language and the time span covered.

4. **Data Visualization with Matplotlib**: Create line charts to display the popularity trends of programming languages over time. Techniques covered include:
   - Plotting single and multiple lines on the same chart.
   - Customizing chart appearance (size, axis labels, ticks, legends).
   - Smoothing noisy time-series data using rolling averages to better identify long-term trends.

5. **Interpretation and Insights**: Based on the visualizations, identify which languages have gained or lost popularity and discuss potential reasons (e.g., emergence of new languages, shifts in technology).

### Dataset Description

The dataset used in this project is derived from Stack Overflow and contains monthly post counts for a selection of programming languages. Each record includes three fields:

- **DATE**: The month and year of the posts, formatted as `YYYY-MM-DD 00:00:00` (initially a string, later converted to datetime).
- **TAG**: The programming language name (e.g., 'python', 'java', 'c#').
- **POSTS**: The number of posts on Stack Overflow tagged with that language during that month.

The dataset covers a period from July 2008 to July 2020 (or a similar range, depending on the query). The included languages are: assembly, c, c#, c++, delphi, go, java, javascript, perl, php, python, r, ruby, swift. Note that some languages like Go and Swift are newer and therefore have fewer monthly entries.

### Optional Fresh Data

Instead of using the provided `QueryResults.csv`, you can obtain the most up-to-date data by running an SQL query on StackExchange's data explorer. The following query (provided in the notebook) retrieves monthly post counts for the same set of languages up to the current month:

```sql
select dateadd(month, datediff(month, 0, q.CreationDate), 0) m, TagName, count(*)
from PostTags pt
join Posts q on q.Id=pt.PostId
join Tags t on t.Id=pt.TagId
where TagName in ('java','c','c++','python','c#','javascript','assembly','php','perl','ruby','visual basic','swift','r','object-c','scratch','go','swift','delphi')
and q.CreationDate < dateadd(month, datediff(month, 0, getdate()), 0)
group by dateadd(month, datediff(month, 0, q.CreationDate), 0), TagName
order by dateadd(month, datediff(month, 0, q.CreationDate), 0)
```

This query groups posts by month and tag, ensuring the data is aggregated for analysis.

### Tools and Libraries

- **Pandas**: For data loading, cleaning, manipulation, and aggregation. Key methods include `read_csv()`, `groupby()`, `pivot()`, `fillna()`, `rolling()`, and datetime conversion.
- **Matplotlib**: For creating static, interactive, and animated visualizations. We'll use `pyplot` for line charts and customization.

The final notebook (`Programming_Languages_(complete).ipynb`) provides a step-by-step implementation of the entire workflow, which will be referenced throughout this documentation.

---

## Data Import and Initial Exploration

### Loading the Data

The first step is to import the necessary libraries and load the dataset. The notebook begins with:

```python
import pandas as pd
import matplotlib.pyplot as plt
```

The data is read from the `QueryResults.csv` file using Pandas' `read_csv()` function. To simplify column handling, custom column names are assigned: `['DATE', 'TAG', 'POSTS']`. The `header=0` argument indicates that the first row of the CSV contains the original headers, which we are overriding.

```python
df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
```

### Examining the Data

After loading, it's essential to inspect the DataFrame to ensure it loaded correctly and understand its structure.

- **First five rows** with `df.head()`:

```
                  DATE         TAG  POSTS
0  2008-07-01 00:00:00          c#      3
1  2008-08-01 00:00:00    assembly      8
2  2008-08-01 00:00:00  javascript    162
3  2008-08-01 00:00:00           c     85
4  2008-08-01 00:00:00      python    124
```

- **Last five rows** with `df.tail()`:

```
                     DATE    TAG  POSTS
1986  2020-07-01 00:00:00      r   5694
1987  2020-07-01 00:00:00     go    743
1988  2020-07-01 00:00:00   ruby    775
1989  2020-07-01 00:00:00   perl    182
1990  2020-07-01 00:00:00  swift   3607
```

- **Dimensions** using `df.shape`: `(1991, 3)` indicating 1991 rows and 3 columns.

- **Non-null counts** per column via `df.count()`:

```
DATE     1991
TAG      1991
POSTS    1991
dtype: int64
```

All columns have 1991 entries, meaning there are no missing values at this stage. However, after reshaping, missing values will appear for languages that did not exist or had no posts in certain months.

### Grouping by Programming Language

To get a sense of overall post volume per language, we group by `TAG` and sum the `POSTS` column:

```python
df.groupby('TAG').sum()
```

This produces a table like:

| TAG        | POSTS   |
|------------|---------|
| assembly   | 34852   |
| c          | 336042  |
| c#         | 1423530 |
| ...        | ...     |
| swift      | 273055  |

From this, we can see that JavaScript has the highest total posts, followed by Java and Python. However, total posts alone don't tell the full story because newer languages have had less time to accumulate posts.

Counting the number of months each language has entries reveals the time coverage:

```python
df.groupby('TAG').count()
```

The `count()` method returns the number of non-null entries per column for each group. The `DATE` and `POSTS` counts should be identical for a language, indicating how many months of data exist. For example:

- `c#` has 145 months (the maximum, likely covering the entire period).
- `go` has only 129 months, as it was created later.
- `swift` has 135 months.

This information is crucial for interpreting trends and ensuring fair comparisons.

---

## Data Cleaning: Working with Timestamps

### Date Column Issues

The `DATE` column in the original DataFrame is stored as strings (e.g., `'2008-07-01 00:00:00'`). This format includes unnecessary time information and is not suitable for time-series operations. Using `type(df['DATE'][1])` confirms it is a string.

### Converting to Datetime

Pandas provides `to_datetime()` to convert strings to datetime objects. This conversion enables powerful time-based indexing, resampling, and plotting. Applying it to the entire column:

```python
df['DATE'] = pd.to_datetime(df['DATE'])
```

After conversion, the dates display as `2008-07-01` without the trailing `00:00:00`. The data type becomes `datetime64[ns]`, which is essential for later steps.

**Why datetime matters**: Datetime objects allow us to set the date column as an index, slice by time periods, and use Matplotlib's automatic date formatting on plots.

---

## Data Manipulation: Pivoting the DataFrame

### The Need for Reshaping

Currently, the DataFrame is in a long format: each row represents a month-tag combination with a post count. For time-series analysis and plotting multiple languages on the same chart, a wide format is more convenient—one column per language, with rows representing months.

Pandas' `pivot()` method reshapes data by specifying which column becomes the new index, which becomes columns, and which provides the values.

### Using `pivot()`

The syntax is:

```python
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
```

- `index='DATE'`: Each unique date becomes a row index.
- `columns='TAG'`: Each unique tag becomes a column.
- `values='POSTS'`: The values to fill the cells come from the `POSTS` column.

The result is a DataFrame where the index is datetime, columns are programming languages, and cells are post counts.

### Handling Missing Values

When pivoting, if a combination of date and tag did not exist in the original data, `pivot()` inserts `NaN`. This is expected for languages that were created after the dataset start date (e.g., Swift in July 2008). For analysis and plotting, it's often preferable to treat missing months as zero posts.

The `fillna()` method replaces `NaN` with a specified value. Using `inplace=True` modifies the DataFrame directly:

```python
reshaped_df.fillna(0, inplace=True)
```

Alternatively, `reshaped_df = reshaped_df.fillna(0)` reassigns.

To verify that no `NaN` values remain, use:

```python
reshaped_df.isna().values.any()   # Returns False if all NaN are replaced
```

### Examining the Reshaped DataFrame

- **Shape**: `reshaped_df.shape` gives `(145, 14)` — 145 months and 14 languages.
- **Columns**: `reshaped_df.columns` lists all language tags.
- **Head**: `reshaped_df.head()` shows the first few rows with zeros for languages that had no posts in those months.

This wide format is now ready for visualization.

---

## Data Visualization with Matplotlib

### Basic Line Plot

A simple line chart for a single language can be created with `plt.plot()`. The x-axis should be the dates (the DataFrame index), and the y-axis the post counts for that language:

```python
plt.plot(reshaped_df.index, reshaped_df['java'])
```

This produces a basic chart, but it lacks labels and proper sizing.

### Customizing the Chart

To improve readability and aesthetics, several customizations are applied:

- **Figure size**: `plt.figure(figsize=(16,10))` makes the chart larger.
- **Axis ticks font size**: `plt.xticks(fontsize=14)` and `plt.yticks(fontsize=14)`.
- **Axis labels**: `plt.xlabel('Date', fontsize=14)` and `plt.ylabel('Number of Posts', fontsize=14)`.
- **Y-axis limits**: `plt.ylim(0, 35000)` ensures the chart starts at zero and caps at a reasonable maximum.

Example for Java:

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)
plt.plot(reshaped_df.index, reshaped_df.java)
```

### Plotting Multiple Languages

To compare two or more languages, call `plt.plot()` multiple times before showing the chart. For instance, to overlay Java and Python:

```python
plt.plot(reshaped_df.index, reshaped_df.java)
plt.plot(reshaped_df.index, reshaped_df.python)
```

A legend is necessary to distinguish lines. Add labels in the plot calls and then `plt.legend()`:

```python
plt.plot(reshaped_df.index, reshaped_df.java, label='Java')
plt.plot(reshaped_df.index, reshaped_df.python, label='Python')
plt.legend()
```

### Plotting All Languages with a Loop

Instead of manually plotting each column, iterate over the columns:

```python
for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column], linewidth=3, label=column)
plt.legend(fontsize=16)
```

The `linewidth` parameter makes lines thicker, and `label` uses the column name for the legend.

The resulting chart displays all 14 languages on the same axes. However, the overlapping lines and noise can make it difficult to discern trends.

### Smoothing with Rolling Averages

Time-series data often contains short-term fluctuations (noise). A rolling average (moving average) smooths the data by averaging values over a specified window. Pandas' `rolling()` method creates a windowed view, and `mean()` computes the average.

For a 6-month rolling average:

```python
roll_df = reshaped_df.rolling(window=6).mean()
```

Plotting `roll_df` instead of the original data produces smoother curves, making long-term trends more apparent. The same customization and legend can be applied.

**Choosing the window**: A larger window (e.g., 12 months) smooths more but may obscure short-term changes. A smaller window (e.g., 3 months) retains more detail. Experimentation helps find the right balance.

---

## Key Takeaways

- **Data Preparation**: Converting to datetime and reshaping are crucial steps for time-series analysis.
- **Handling Missing Data**: In this context, filling `NaN` with zero is appropriate because missing months imply zero posts.
- **Visualization**: Matplotlib provides flexible tools for creating informative charts. Customizing labels, sizes, and legends enhances readability.
- **Trend Identification**: Rolling averages help reveal underlying trends in noisy time-series data.

By following these steps, the analysis reveals that Python has become the most discussed language on Stack Overflow in recent years, overtaking older languages like Java and C#. This insight aligns with Python's widespread adoption in data science, web development, and education.

---

*Note: The SQL query for fetching fresh data and the complete code implementation are available in the accompanying Jupyter notebook.*

## Complete Code Walkthrough: Analyzing Programming Language Popularity

This document provides a concise, code-focused recap of the entire analysis. Each step includes the essential code and a brief explanation. Use this as a quick reference for replicating the workflow.

---

### 1. Import Libraries

```python
import pandas as pd
import matplotlib.pyplot as plt
```

---

### 2. Load the Dataset

```python
# Read CSV with custom column names
df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
```

---

### 3. Initial Data Inspection

```python
# First and last 5 rows
df.head()
df.tail()

# Dimensions
df.shape

# Count non-null entries per column
df.count()
```

---

### 4. Group and Aggregate

```python
# Total posts per language
df.groupby('TAG').sum()

# Number of months per language
df.groupby('TAG').count()
```

---

### 5. Convert Date to Datetime

```python
df['DATE'] = pd.to_datetime(df['DATE'])
```

---

### 6. Reshape with Pivot

```python
# Pivot: index=DATE, columns=TAG, values=POSTS
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')

# Check new shape and columns
reshaped_df.shape
reshaped_df.columns

# Replace NaN with 0
reshaped_df.fillna(0, inplace=True)

# Confirm no NaNs remain
reshaped_df.isna().values.any()
```

---

### 7. Plot a Single Language

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

plt.plot(reshaped_df.index, reshaped_df['java'])
plt.show()
```

---

### 8. Plot Two Languages with Legend

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

plt.plot(reshaped_df.index, reshaped_df['java'], label='Java', linewidth=3)
plt.plot(reshaped_df.index, reshaped_df['python'], label='Python', linewidth=3)
plt.legend(fontsize=14)
plt.show()
```

---

### 9. Plot All Languages with a Loop

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column],
             linewidth=3, label=column)

plt.legend(fontsize=16)
plt.show()
```

---

### 10. Smooth with Rolling Average

```python
# 6-month rolling average
roll_df = reshaped_df.rolling(window=6).mean()

# Plot smoothed data
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts (6-month avg)', fontsize=14)
plt.ylim(0, 35000)

for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column],
             linewidth=3, label=column)

plt.legend(fontsize=16)
plt.show()
```

- Experiment with `window=3` or `window=12` to see the effect.

---

### 11. (Optional) Export Cleaned Data

```python
# Save reshaped DataFrame to CSV for later use
reshaped_df.to_csv('programming_languages_wide.csv')
```

---

### 12. Key Takeaways

- **Groupby**: Aggregates data by categories.
- **Pivot**: Reshapes from long to wide format.
- **Datetime conversion**: Enables proper time-series handling.
- **Fillna**: Replaces missing values with zeros for continuous data.
- **Rolling mean**: Smooths noisy time-series to reveal trends.
- **Matplotlib customization**: Improves chart readability.

---

This code block summary covers the entire analysis pipeline. Adjust window sizes, languages, or plot parameters as needed for your own investigations.