# Data Cleaning – Resampling Time Series Data

## Introduction
Real‑world data is rarely perfect. Before we can analyse or visualise our time series, we must ensure:

1. **No missing values** – otherwise, calculations and plots may break.
2. **Correct data types** – dates should be proper datetime objects, not strings.
3. **Consistent frequency** – when combining datasets (e.g., daily price vs monthly search), we need to align them.

In this lesson, we’ll clean the four DataFrames: Tesla, unemployment, Bitcoin search, and Bitcoin price. We’ll then resample the daily Bitcoin price to monthly frequency, matching the search data.

---

## 1. Checking for Missing Values

Pandas provides the `.isna()` method to detect missing (NaN) values. It returns a Boolean DataFrame of the same shape. To quickly see if *any* missing values exist, we use `.values.any()`.

### 1.1 Tesla, Unemployment, Bitcoin Search
```python
print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
```
**Output:**
```
Missing values for Tesla?: False
Missing values for U/E?: False
Missing values for BTC Search?: False
```
All three are clean – no missing data.

### 1.2 Bitcoin Price
```python
print(f'Missing values? for BTC price?: {df_btc_price.isna().values.any()}')
```
**Output:**
```
Missing values? for BTC price?: True
```
There *are* missing values. Let's count them:
```python
print(f'Number of missing values: {df_btc_price.isna().values.sum()}')
```
**Output:**
```
Number of missing values: 2
```

### 1.3 Locating the Missing Rows
We can subset the DataFrame where any column is NaN:
```python
df_btc_price[df_btc_price.isna().any(axis=1)]
```
**Output:**
|      | DATE       | CLOSE | VOLUME |
|------|------------|-------|--------|
| 2148 | 2020-08-04 | NaN   | NaN    |

Both `CLOSE` and `VOLUME` are missing for that date. (The notebook shows one row but says 2 missing values; possibly there are two rows, but only one is displayed. We'll assume the count is correct.)

### 1.4 Removing Missing Values
We use `.dropna()` to delete rows with any missing values. The `inplace=True` argument modifies the DataFrame directly.
```python
df_btc_price.dropna(inplace=True)
```
Verify:
```python
print(f'Missing values after drop: {df_btc_price.isna().values.any()}')
```
**Output:**
```
Missing values after drop: False
```

---

## 2. Converting Strings to Datetime Objects

All date columns are initially read as strings. We need proper datetime objects for plotting and resampling.

Check the type of a single entry:
```python
type(df_tesla.MONTH[0])
```
**Output:**
```
str
```

Convert each DataFrame’s date column using `pd.to_datetime()`:
```python
df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)
```

Confirm the conversion:
```python
df_tesla.MONTH.head()
```
**Output:**
```
0   2010-06-01
1   2010-07-01
2   2010-08-01
3   2010-09-01
4   2010-10-01
Name: MONTH, dtype: datetime64[ns]
```
Now the dtype is `datetime64[ns]`, ready for time‑series operations.

---

## 3. Resampling: Daily → Monthly Bitcoin Price

The Bitcoin price is daily, but the search data is monthly. To compare them, we need to convert the price to monthly frequency.

### 3.1 The `.resample()` Method
Pandas’ `.resample()` is a powerful time‑series resampling tool. It requires:
- A **rule** specifying the target frequency (e.g., `'M'` for month end, `'MS'` for month start, `'Y'` for year).
- The **column** to use as the time index (via `on=`).

After resampling, we must decide how to aggregate the data within each month. Common choices:
- `last()` – use the last available value (month‑end price).
- `mean()` – average of all daily prices.
- `max()` / `min()` – highest/lowest price of the month.

For our purpose, we want the month‑end closing price, so we use `.last()`.

```python
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()
```

### 3.2 Understanding the Output
Let's examine the result:
```python
print(df_btc_monthly.shape)
df_btc_monthly.head()
```
**Output:**
```
(73, 3)
```

| DATE       |       CLOSE |      VOLUME |
|------------|-------------|-------------|
| 2014-09-30 | 386.944000  | 34707300.0  |
| 2014-10-31 | 338.321014  | 12545400.0  |
| 2014-11-30 | 378.046997  | 9194440.0   |
| 2014-12-31 | 320.192993  | 13942900.0  |
| 2015-01-31 | 217.464005  | 23348200.0  |

- Now we have **73 rows**, matching the Bitcoin search DataFrame (`df_btc_search` has 73 rows).
- The index is the last day of each month (e.g., 2014-09-30).
- All original columns (`CLOSE`, `VOLUME`) are preserved, but now at monthly frequency.

If we had used `.mean()`, we would get the average price for each month – a different representation.

### 3.3 Available Resampling Rules
Here are some common frequency aliases:
- `'D'` – calendar day
- `'W'` – weekly
- `'M'` – month end
- `'MS'` – month start
- `'Q'` – quarter end
- `'Y'` – year end

Full list: [Pandas Offset Aliases](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)

---

## 4. Summary of Data Cleaning Steps

| Step | Action | Code | Result |
|------|--------|------|--------|
| 1 | Check missing values | `.isna().values.any()` | Identified 2 NaNs in BTC price. |
| 2 | Remove missing rows | `.dropna(inplace=True)` | Clean BTC price DataFrame. |
| 3 | Convert date strings to datetime | `pd.to_datetime()` | All date columns become `datetime64`. |
| 4 | Resample daily price to monthly | `.resample('M', on='DATE').last()` | New monthly DataFrame (73 rows). |

Now our data is clean, correctly typed, and all series are at the same monthly frequency – ready for visualisation and analysis.

---

## 5. Additional Considerations

- **Inplace vs Assignment**: `dropna(inplace=True)` modifies the original DataFrame. Alternatively, you can assign: `df = df.dropna()`.
- **Handling NaN in other ways**: Instead of dropping, you could fill missing values with `.fillna()` (e.g., forward fill, backward fill, or interpolation). For time series, forward fill (`method='ffill'`) is often used.
- **Resampling with other aggregations**: Choose the method that best represents your question. For stock prices, month‑end price is common; for volume, sum might be more appropriate.

