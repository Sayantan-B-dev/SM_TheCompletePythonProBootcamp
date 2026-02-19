## Data Manipulation: Pivoting DataFrames

After cleaning the date column, the DataFrame remains in a **long format**: each row represents a single observation—a specific month (`DATE`) and programming language (`TAG`) with a corresponding number of `POSTS`. While this format is efficient for storage and many operations, it is not ideal for time-series visualization. To plot multiple languages on the same chart, we need a **wide format** where each language becomes a separate column, each row corresponds to a month, and the cell values are the post counts.

Pandas provides the `pivot()` method to reshape data from long to wide. This section explains how `pivot()` works using a simple example, then applies it to our Stack Overflow dataset. We'll also address the inevitable missing values that arise from languages that did not exist or had no posts in certain months, and how to handle them.

### Understanding `pivot()` with a Simple Example

Consider a small DataFrame tracking the "power level" of actors at different ages:

```python
import pandas as pd

test_df = pd.DataFrame({
    'Age': ['Young', 'Young', 'Young', 'Young', 'Old', 'Old', 'Old', 'Old'],
    'Actor': ['Jack', 'Arnold', 'Keanu', 'Sylvester', 'Jack', 'Arnold', 'Keanu', 'Sylvester'],
    'Power': [100, 80, 25, 50, 99, 75, 5, 30]
})
test_df
```

|    | Age   | Actor     | Power |
|----|-------|-----------|-------|
| 0  | Young | Jack      | 100   |
| 1  | Young | Arnold    | 80    |
| 2  | Young | Keanu     | 25    |
| 3  | Young | Sylvester | 50    |
| 4  | Old   | Jack      | 99    |
| 5  | Old   | Arnold    | 75    |
| 6  | Old   | Keanu     | 5     |
| 7  | Old   | Sylvester | 30    |

In this long format, each row is a unique combination of `Age` and `Actor`. To see the power of each actor across the two age categories side by side, we can pivot so that `Age` becomes the index, `Actor` becomes column names, and `Power` fills the cells:

```python
pivoted_df = test_df.pivot(index='Age', columns='Actor', values='Power')
pivoted_df
```

Result:

| Actor | Arnold | Jack | Keanu | Sylvester |
|-------|--------|------|-------|-----------|
| **Age** |        |      |       |           |
| Old   | 75     | 99   | 5     | 30        |
| Young | 80     | 100  | 25    | 50        |

Key points:

- The `index` parameter specifies the column whose unique values become the new row labels (`Age`).
- The `columns` parameter specifies the column whose unique values become the new column names (`Actor`).
- The `values` parameter specifies the column to fill the new DataFrame's cells (`Power`).

If a combination of `index` and `columns` is missing, `pivot()` inserts `NaN` (Not a Number). For example, if we had removed the row for Old Sylvester, the pivot would show `NaN` at that position. This behavior is important when working with real-world data that may have gaps.

### Applying `pivot()` to the Stack Overflow Data

Our DataFrame `df` has three columns: `DATE`, `TAG`, and `POSTS`. Each `(DATE, TAG)` pair is unique (a language can have at most one post count per month), so `pivot()` is directly applicable without needing aggregation.

We create a new DataFrame `reshaped_df`:

```python
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
```

- `index='DATE'`: Each unique date becomes a row in the new DataFrame.
- `columns='TAG'`: Each unique programming language becomes a column.
- `values='POSTS'`: The number of posts populates the cells.

After pivoting, the DataFrame has a `DatetimeIndex` (since `DATE` is now the index) and columns are the language names.

### Examining the Reshaped DataFrame

#### Dimensions

```python
reshaped_df.shape
```
Output: `(145, 14)`

This tells us there are 145 distinct months in the dataset and 14 programming languages.

#### Column Names

```python
reshaped_df.columns
```
Output:
```
Index(['assembly', 'c', 'c#', 'c++', 'delphi', 'go', 'java', 'javascript',
       'perl', 'php', 'python', 'r', 'ruby', 'swift'],
      dtype='object', name='TAG')
```

Note that the column index has a name `'TAG'`, inherited from the original column.

#### First Five Rows

```python
reshaped_df.head()
```

| DATE       | assembly | c    | c#    | c++   | delphi | go | java  | javascript | perl | php  | python | r    | ruby  | swift |
|------------|----------|------|-------|-------|--------|----|-------|------------|------|------|--------|------|-------|-------|
| 2008-07-01 | NaN      | NaN  | 3.0   | NaN   | NaN    | NaN| NaN   | NaN        | NaN  | NaN  | NaN    | NaN  | NaN   | NaN   |
| 2008-08-01 | 8.0      | 85.0 | 511.0 | 164.0 | 14.0   | NaN| 222.0 | 162.0      | 28.0 | 161.0| 124.0  | NaN  | 73.0  | NaN   |
| 2008-09-01 | 28.0     | 321.0| 1649.0| 755.0 | 105.0  | NaN| 1137.0| 640.0      | 131.0| 482.0| 542.0  | 6.0  | 290.0 | NaN   |
| 2008-10-01 | 15.0     | 303.0| 1989.0| 811.0 | 112.0  | NaN| 1153.0| 725.0      | 127.0| 617.0| 510.0  | NaN  | 249.0 | NaN   |
| 2008-11-01 | 17.0     | 259.0| 1730.0| 735.0 | 141.0  | NaN| 958.0 | 579.0      | 97.0 | 504.0| 452.0  | 1.0  | 160.0 | NaN   |

Notice the `NaN` values. These occur when a language had no posts in that month (e.g., Swift in 2008, because it didn't exist yet) or when the language existed but had zero posts (which the original data does not record). For time-series analysis, we often want to treat missing months as zero posts rather than ignore them. This decision depends on the context: for languages that did not exist, zero is accurate; for languages that existed but had no posts, zero is also correct because the absence of a record means no posts.

### Counting Entries per Language

Before filling `NaN`, it's useful to see how many months each language actually has data. The `.count()` method counts non-null values per column:

```python
reshaped_df.count()
```

Output:

| TAG       | count |
|-----------|-------|
| assembly  | 144   |
| c         | 144   |
| c#        | 145   |
| c++       | 144   |
| delphi    | 144   |
| go        | 129   |
| java      | 144   |
| javascript| 144   |
| perl      | 144   |
| php       | 144   |
| python    | 144   |
| r         | 142   |
| ruby      | 144   |
| swift     | 135   |

These numbers match the counts we obtained earlier when grouping by `TAG` and counting rows. They reflect the number of months for which each language has at least one post recorded. Languages like `go` and `swift` have fewer entries because they are newer.

### Handling Missing Values

We will replace all `NaN` values with `0` to indicate zero posts for those months. The `fillna()` method does this. Using `inplace=True` modifies the DataFrame directly:

```python
reshaped_df.fillna(0, inplace=True)
```

Alternatively, you can reassign: `reshaped_df = reshaped_df.fillna(0)`.

After filling, we verify that no `NaN` values remain:

```python
reshaped_df.isna().values.any()
```
Output: `False`

Now each cell contains a float (or integer) representing the number of posts. The first few rows now show zeros instead of `NaN`:

```python
reshaped_df.head()
```

| DATE       | assembly | c    | c#    | c++   | delphi | go | java  | javascript | perl | php  | python | r    | ruby  | swift |
|------------|----------|------|-------|-------|--------|----|-------|------------|------|------|--------|------|-------|-------|
| 2008-07-01 | 0.0      | 0.0  | 3.0   | 0.0   | 0.0    | 0.0| 0.0   | 0.0        | 0.0  | 0.0  | 0.0    | 0.0  | 0.0   | 0.0   |
| 2008-08-01 | 8.0      | 85.0 | 511.0 | 164.0 | 14.0   | 0.0| 222.0 | 162.0      | 28.0 | 161.0| 124.0  | 0.0  | 73.0  | 0.0   |
| ...        | ...      | ...  | ...    | ...   | ...    | ...| ...   | ...        | ...  | ...  | ...    | ...  | ...   | ...   |

The data is now complete and ready for visualization.

### Why Fill with Zeros?

In time-series analysis, gaps can distort trends and complicate calculations like rolling averages. By filling with zero, we ensure that every language has a value for every month in the dataset's date range. This approach:

- Preserves the fact that newer languages had zero posts before their creation.
- Allows us to plot all languages from the same start date (though lines for newer languages will start at zero and then rise).
- Simplifies mathematical operations across columns (e.g., comparing totals, calculating moving averages).

An alternative would be to keep `NaN` and let plotting libraries handle them (e.g., by not connecting missing points). However, for this analysis, zero is the most appropriate fill value because it accurately reflects the number of posts.

### Summary

- The `pivot()` method reshapes the DataFrame from long to wide, making it suitable for multi-line time-series plots.
- After pivoting, `NaN` values appear for months where a language had no posts.
- Counting non-null entries reveals the data coverage per language.
- Filling `NaN` with zeros creates a complete dataset for analysis and visualization.

Now that the data is in the desired format, we can move on to creating charts with Matplotlib.

---

*Note: If your dataset contains duplicate (DATE, TAG) pairs (which would indicate multiple entries for the same month and language), `pivot()` will raise an error. In that case, you would need to use `pivot_table()` with an aggregation function like `sum()` or `mean()` to combine duplicates. Our dataset has no duplicates, so `pivot()` works perfectly.*