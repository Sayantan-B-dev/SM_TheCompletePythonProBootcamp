# Data Exploration and Cleaning

This document provides a detailed walkthrough of the initial data exploration and cleaning steps performed on the movie budget and revenue dataset. Proper data cleaning is essential to ensure that subsequent analysis, visualisation, and modelling are accurate and meaningful. The dataset is stored in a CSV file named `cost_revenue_dirty.csv`, which contains information about films, their release dates, production budgets, and gross revenues.

The primary goals of this phase are to:

- Understand the structure and content of the dataset.
- Identify and handle any missing values or duplicate rows.
- Convert columns to appropriate data types for numerical and temporal analysis.
- Remove any extraneous characters (e.g., dollar signs, commas) from monetary values.

All operations are performed using the **pandas** library in Python.

---

## 1. Loading the Dataset

First, we import pandas and read the CSV file into a DataFrame. The file is located in the same directory as the notebook.

```python
import pandas as pd

data = pd.read_csv('cost_revenue_dirty.csv')
```

After loading, the DataFrame `data` contains 5391 rows and 6 columns, as we will confirm in the next steps.

---

## 2. Initial Inspection

Before making any changes, it is crucial to get a preliminary understanding of the data. We use several pandas methods:

### 2.1 Check the Shape

```python
data.shape
```

Output: `(5391, 6)`

This tells us there are 5391 rows (films) and 6 columns.

### 2.2 View Random Samples

Using `sample()` gives a random selection of rows, which helps detect any obvious formatting issues or anomalies.

```python
data.sample(5)
```

A typical output might look like:

| Rank | Release_Date | Movie_Title                  | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|------------------------------|-----------------------|---------------------|--------------------|
| 4283 | 6/30/1985    | Day of the Dead              | $3,500,000            | $34,004,262         | $5,804,262         |
| 4128 | 3/27/1998    | Karakter                     | $4,500,000            | $713,413            | $713,413           |
| 1123 | 11/16/2012   | Anna Karenina                | $49,000,000           | $71,004,627         | $12,816,367        |
| 1952 | 9/19/2008    | The Duchess                  | $27,000,000           | $45,160,110         | $13,848,978        |
| 2900 | 5/21/1999    | The Love Letter              | $15,000,000           | $8,322,608          | $8,322,608         |

Notice that the monetary columns contain dollar signs (`$`) and commas, which will need to be removed before numerical analysis.

### 2.3 View the Last Few Rows

```python
data.tail()
```

This reveals that some films have release dates in the future (e.g., 2018-10-08, 2020-12-31) and show zero revenue. These are likely unreleased films at the time of data collection (May 1, 2018).

---

## 3. Checking for Missing Values and Duplicates

Data integrity is critical. We verify that there are no missing values or duplicate rows.

### 3.1 Missing Values

```python
data.isna().values.any()
```

Output: `False`

This indicates that no column contains `NaN` (Not a Number) values. All cells are populated.

### 3.2 Duplicate Rows

```python
data.duplicated().values.any()
```

Output: `False`

There are no duplicate rows. To double‑check, we can create a subset of duplicates and count them:

```python
duplicated_rows = data[data.duplicated()]
len(duplicated_rows)
```

Output: `0`

Thus, the dataset is free of both missing values and duplicates, simplifying the cleaning process.

---

## 4. Examining Data Types

The `info()` method provides a concise summary of the DataFrame, including column names, non‑null counts, and data types.

```python
data.info()
```

Output:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5391 entries, 0 to 5390
Data columns (total 6 columns):
 #   Column                 Non-Null Count  Dtype 
---  ------                 --------------  ----- 
 0   Rank                   5391 non-null   int64 
 1   Release_Date           5391 non-null   object
 2   Movie_Title            5391 non-null   object
 3   USD_Production_Budget  5391 non-null   object
 4   USD_Worldwide_Gross    5391 non-null   object
 5   USD_Domestic_Gross     5391 non-null   object
dtypes: int64(1), object(5)
memory usage: 252.8+ KB
```

Observations:

- The `Rank` column is already an integer (`int64`).
- `Release_Date` is stored as an `object` (string). For time‑series analysis, it should be converted to a datetime type.
- The three monetary columns are also `object` because they contain strings with dollar signs and commas. These must be converted to numeric types.

---

## 5. Cleaning Monetary Columns

The goal is to transform columns like `"$110,000"` into integers `110000`. This involves two steps for each column:

1. Remove all dollar signs (`$`) and commas (`,`).
2. Convert the resulting string to a numeric type (here, `int64`).

A nested `for` loop efficiently processes all three columns.

```python
chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget', 
                    'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']

for col in columns_to_clean:
    for char in chars_to_remove:
        # Replace each character with an empty string
        data[col] = data[col].astype(str).str.replace(char, "")
    # Convert column to a numeric data type
    data[col] = pd.to_numeric(data[col])
```

**Explanation**:

- `data[col].astype(str)` ensures the column is treated as a string (though it already is, this is a safety measure).
- `.str.replace(char, "")` removes every occurrence of the specified character.
- After both characters are removed, `pd.to_numeric()` converts the cleaned strings to integers (or floats if necessary). Pandas automatically selects the appropriate integer type.

After this operation, we can inspect the DataFrame again:

```python
data.head()
```

| Rank | Release_Date | Movie_Title                  | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|------------------------------|-----------------------|---------------------|--------------------|
| 5293 | 8/2/1915     | The Birth of a Nation        | 110000                | 11000000            | 10000000           |
| 5140 | 5/9/1916     | Intolerance                  | 385907                | 0                   | 0                  |
| 5230 | 12/24/1916   | 20,000 Leagues Under the Sea | 200000                | 8000000             | 8000000            |
| 5299 | 9/17/1920    | Over the Hill to the Poorhouse| 100000               | 3000000             | 3000000            |
| 5222 | 1/1/1925     | The Big Parade               | 245000                | 22000000            | 11000000           |

The monetary values are now clean integers, ready for mathematical operations.

---

## 6. Converting Release Date to Datetime

To work with dates effectively (e.g., extracting year, month, or plotting over time), we convert the `Release_Date` column to a pandas `datetime` type.

```python
data.Release_Date = pd.to_datetime(data.Release_Date)
```

This function automatically parses various date formats. The original format in the CSV is month/day/year (e.g., `8/2/1915`), which `to_datetime` handles correctly.

After conversion, we can verify the change:

```python
data.head()
```

| Rank | Release_Date | Movie_Title                  | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|------------------------------|-----------------------|---------------------|--------------------|
| 5293 | 1915-08-02   | The Birth of a Nation        | 110000                | 11000000            | 10000000           |
| 5140 | 1916-05-09   | Intolerance                  | 385907                | 0                   | 0                  |
| 5230 | 1916-12-24   | 20,000 Leagues Under the Sea | 200000                | 8000000             | 8000000            |
| 5299 | 1920-09-17   | Over the Hill to the Poorhouse| 100000               | 3000000             | 3000000            |
| 5222 | 1925-01-01   | The Big Parade               | 245000                | 22000000            | 11000000           |

The `Release_Date` now appears in ISO format (`YYYY-MM-DD`) and has the correct `datetime64[ns]` data type.

---

## 7. Verifying the Cleaning

We run `data.info()` once more to confirm that all transformations have been applied correctly.

```python
data.info()
```

Output:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5391 entries, 0 to 5390
Data columns (total 6 columns):
 #   Column                 Non-Null Count  Dtype         
---  ------                 --------------  -----         
 0   Rank                   5391 non-null   int64         
 1   Release_Date           5391 non-null   datetime64[ns]
 2   Movie_Title            5391 non-null   object        
 3   USD_Production_Budget  5391 non-null   int64         
 4   USD_Worldwide_Gross    5391 non-null   int64         
 5   USD_Domestic_Gross     5391 non-null   int64         
dtypes: datetime64[ns](1), int64(4), object(1)
memory usage: 252.8+ KB
```

Now all monetary columns are integers, and `Release_Date` is a datetime. The dataset is clean and ready for exploration and analysis.

---

## 8. Summary

Through this data exploration and cleaning phase, we have:

- Confirmed the dataset has 5391 rows and 6 columns.
- Verified there are no missing values or duplicate rows.
- Identified that the monetary columns require cleaning.
- Removed dollar signs and commas, then converted those columns to integers.
- Converted the release date column to a proper datetime type.

The cleaned DataFrame now contains reliable, correctly typed data. Subsequent steps will involve statistical summarisation, filtering, visualisation, and linear regression modelling.

---