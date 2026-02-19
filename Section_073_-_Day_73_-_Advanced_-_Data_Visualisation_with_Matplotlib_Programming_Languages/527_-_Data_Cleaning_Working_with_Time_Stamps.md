## Data Cleaning: Working with Time Stamps

After completing the initial grouping and counting of posts per language, the next critical step is to prepare the `DATE` column for time-series analysis. Currently, the dates are stored as strings (e.g., `'2008-07-01 00:00:00'`). While strings can be used for basic plotting, they lack the properties of datetime objects, which are essential for proper time-based operations such as:

- Setting the date as an index for time-series data.
- Resampling to different frequencies (e.g., quarterly, yearly).
- Easily extracting components (year, month, day).
- Automatic formatting of axis labels in plots.
- Performing date arithmetic (e.g., calculating time differences).

This section covers how to inspect the date column, understand its current data type, and convert it to Pandas' `Timestamp` (datetime) format.

### Selecting and Inspecting Individual Date Entries

Before converting the entire column, it's helpful to look at a single entry to confirm its format and type. Pandas offers two convenient ways to access a specific cell:

1. **Using square bracket notation** (recommended for column names with spaces or special characters):
   ```python
   df['DATE'][1]
   ```
2. **Using dot notation** (works for column names without spaces):
   ```python
   df.DATE[1]
   ```

Both return the same value. For our dataset, `df['DATE'][1]` outputs:
```
'2008-08-01 00:00:00'
```

To verify the data type, we use the built-in `type()` function:
```python
type(df['DATE'][1])
```
Output:
```
str
```

This confirms that the entry is a string (Python `str`), not a datetime object. The entire `DATE` column is composed of such strings.

### Why Convert to Datetime?

Using strings for dates has several drawbacks:

- **Incorrect Sorting**: Sorting by string would sort lexicographically (e.g., '2008-10-01' might come before '2008-02-01' because '10' < '2' as strings).
- **Limited Functionality**: String operations cannot perform date arithmetic (e.g., adding months, calculating differences).
- **Plotting Limitations**: Matplotlib can handle strings as x-axis labels, but it treats them as categorical data, not a continuous time line. This leads to poor spacing and missing automatic date formatting.
- **No Time-Based Indexing**: With datetime indices, we can easily slice data by date ranges (e.g., `df['2015':]` for data from 2015 onward).

Converting to datetime resolves these issues and unlocks a wide range of time-series functionalities in both Pandas and Matplotlib.

### Converting a Single Entry with `pd.to_datetime()`

Pandas provides the `to_datetime()` function to parse strings into datetime objects. Let's test it on a single entry:

```python
pd.to_datetime(df.DATE[1])
```

Output:
```
Timestamp('2008-08-01 00:00:00')
```

The result is a `Timestamp` object, Pandas' equivalent of Python's `datetime` but optimized for use in DataFrames. We can also check its type:

```python
type(pd.to_datetime(df.DATE[1]))
```
Output:
```
pandas._libs.tslibs.timestamps.Timestamp
```

Note that the time part `00:00:00` is still present but is now part of the timestamp. When displayed, it may show as `2008-08-01` depending on the display settings, but the underlying object stores the full datetime.

### Converting the Entire Column

Applying `to_datetime()` to the whole column is straightforward:

```python
df['DATE'] = pd.to_datetime(df['DATE'])
```

Alternatively, using dot notation:

```python
df.DATE = pd.to_datetime(df.DATE)
```

After this operation, we can inspect the DataFrame again with `df.head()`:

|    | DATE       | TAG        | POSTS |
|----|------------|------------|-------|
| 0  | 2008-07-01 | c#         | 3     |
| 1  | 2008-08-01 | assembly   | 8     |
| 2  | 2008-08-01 | javascript | 162   |
| 3  | 2008-08-01 | c          | 85    |
| 4  | 2008-08-01 | python     | 124   |

Now the `DATE` column shows only the date part (the time is omitted for brevity, but it's still stored). To confirm the new data type, check the column's dtype:

```python
df['DATE'].dtype
```
Output:
```
datetime64[ns]
```

This indicates that the column is now a proper datetime column with nanosecond precision.

### Benefits Realized

With the `DATE` column as datetime, we can:

- **Set it as the index**: `df.set_index('DATE', inplace=True)` (though we'll do this indirectly via `pivot` later).
- **Plot with proper time axis**: Matplotlib will automatically space dates proportionally.
- **Resample**: For example, to get yearly totals: `df.resample('Y').sum()`.
- **Filter by date**: `df[df.DATE > '2015-01-01']`.

### Next Steps

Now that the date column is correctly formatted, we can proceed to reshape the DataFrame using `pivot()`. This will transform the data from a long format (multiple rows per date, one per language) to a wide format (one row per date, one column per language). The wide format is ideal for plotting multiple time series on a single chart and for applying rolling averages. The following file (528) covers this reshaping process in detail.

---

*Note: When converting strings to datetime, ensure that the format is consistent. In our case, the dates follow the ISO 8601 format (`YYYY-MM-DD HH:MM:SS`), which `to_datetime()` can parse automatically. If you have a different format, you may need to specify it using the `format` parameter (e.g., `format='%d/%m/%Y'`).*