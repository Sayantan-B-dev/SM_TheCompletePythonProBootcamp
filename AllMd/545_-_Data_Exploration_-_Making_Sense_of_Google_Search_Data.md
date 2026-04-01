# Data Exploration – Making Sense of Google Search Data

## Introduction
Before diving into visualisation or analysis, it's crucial to understand the raw data we're working with. Data exploration helps us answer fundamental questions:

- **What is the size and structure of the dataset?** (rows, columns, data types)
- **What do the columns represent?** (column names)
- **What is the range of values?** (min, max, descriptive statistics)
- **What is the time frequency?** (daily, monthly, etc.)
- **What do the numbers actually mean?** (especially for Google Trends data)

In this lesson, we explore four DataFrames: Tesla, unemployment, Bitcoin search, and Bitcoin price. We'll use pandas methods like `.shape`, `.head()`, `.describe()`, and `.max()` to gain insights.

---

## 1. Setting Up
Assuming the data is already loaded (as per the notebook):

```python
import pandas as pd

df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')
df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
```

Let's begin exploration.

---

## 2. Tesla DataFrame

### 2.1 Shape and Columns
```python
print("Tesla DataFrame shape:", df_tesla.shape)
print("Column names:", df_tesla.columns.tolist())
df_tesla.head()
```
**Output:**
```
Tesla DataFrame shape: (124, 3)
Column names: ['MONTH', 'TSLA_WEB_SEARCH', 'TSLA_USD_CLOSE']
```

|    | MONTH      | TSLA_WEB_SEARCH | TSLA_USD_CLOSE |
|----|------------|-----------------|----------------|
| 0  | 2010-06-01 | 3               | 4.766          |
| 1  | 2010-07-01 | 3               | 3.988          |
| 2  | 2010-08-01 | 2               | 3.896          |
| 3  | 2010-09-01 | 2               | 4.082          |
| 4  | 2010-10-01 | 2               | 4.368          |

- **Rows:** 124 → 124 monthly records.
- **Columns:** 3 – date, search popularity (0‑100 scale), stock closing price (USD).

### 2.2 Search Value Range
```python
print(f"Largest Tesla web search value: {df_tesla.TSLA_WEB_SEARCH.max()}")
print(f"Smallest Tesla web search value: {df_tesla.TSLA_WEB_SEARCH.min()}")
```
**Output:**
```
Largest Tesla web search value: 31
Smallest Tesla web search value: 2
```

The highest popularity for "Tesla" in this time span (2010‑2020) was 31 (relative to a peak of 100). The lowest was 2.

### 2.3 Descriptive Statistics
```python
df_tesla.describe()
```
**Output:**

|       | TSLA_WEB_SEARCH | TSLA_USD_CLOSE |
|-------|-----------------|----------------|
| count | 124.000000      | 124.000000     |
| mean  | 8.725806        | 50.962145      |
| std   | 5.870332        | 65.908389      |
| min   | 2.000000        | 3.896000       |
| 25%   | 3.750000        | 7.352500       |
| 50%   | 8.000000        | 44.653000      |
| 75%   | 12.000000       | 58.991999      |
| max   | 31.000000       | 498.320007     |

- The mean search value is about 8.7, with a standard deviation of 5.9.
- Stock price ranges from ~$3.90 to $498, showing extreme growth.

### 2.4 Periodicity
Looking at the `MONTH` column values (all first of the month), we see **monthly** data. This is consistent with Google Trends monthly export.

---

## 3. Unemployment DataFrame (2004‑2019)

```python
print("Unemployment DataFrame shape:", df_unemployment.shape)
df_unemployment.head()
```
**Output:**
```
Unemployment DataFrame shape: (181, 3)
```

|    | MONTH   | UE_BENEFITS_WEB_SEARCH | UNRATE |
|----|---------|------------------------|--------|
| 0  | 2004-01 | 34                     | 5.7    |
| 1  | 2004-02 | 33                     | 5.6    |
| 2  | 2004-03 | 25                     | 5.8    |
| 3  | 2004-04 | 29                     | 5.6    |
| 4  | 2004-05 | 23                     | 5.6    |

- **Rows:** 181 (about 15 years of monthly data).
- **Columns:** date, search popularity for "unemployment benefits", actual unemployment rate (from FRED).

### 3.1 Search Value Range
```python
print(f"Largest UE Benefits search value: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}")
```
**Output:**
```
Largest UE Benefits search value: 100
```
Interestingly, the search popularity reached the maximum possible value (100) at some point. Likely during the 2008 financial crisis or later.

### 3.2 Periodicity
Again, `MONTH` values are in `YYYY-MM` format → **monthly**.

---

## 4. Bitcoin DataFrames

We have two separate files for Bitcoin: daily price and monthly search.

### 4.1 Daily Bitcoin Price

```python
print("Bitcoin price DataFrame shape:", df_btc_price.shape)
df_btc_price.head()
```
**Output:**
```
Bitcoin price DataFrame shape: (2204, 3)
```

|    | DATE       | CLOSE       | VOLUME      |
|----|------------|-------------|-------------|
| 0  | 2014-09-17 | 457.334015  | 21056800.0  |
| 1  | 2014-09-18 | 424.440002  | 34483200.0  |
| 2  | 2014-09-19 | 394.795990  | 37919700.0  |
| 3  | 2014-09-20 | 408.903992  | 36863600.0  |
| 4  | 2014-09-21 | 398.821014  | 26580100.0  |

- **Rows:** 2204 → daily data from 2014‑09‑17 to 2020‑??.
- **Columns:** date, closing price, volume.

### 4.2 Bitcoin Monthly Search

```python
print("Bitcoin search DataFrame shape:", df_btc_search.shape)
df_btc_search.head()
```
**Output:**
```
Bitcoin search DataFrame shape: (73, 2)
```

|    | MONTH   | BTC_NEWS_SEARCH |
|----|---------|-----------------|
| 0  | 2014-09 | 5               |
| 1  | 2014-10 | 4               |
| 2  | 2014-11 | 4               |
| 3  | 2014-12 | 4               |
| 4  | 2015-01 | 5               |

- **Rows:** 73 → roughly 6 years of monthly data.
- **Columns:** month, search popularity.

### 4.3 Largest Search Value
```python
print(f"Largest BTC news search value: {df_btc_search.BTC_NEWS_SEARCH.max()}")
```
**Output:**
```
Largest BTC news search value: 100
```
Again, search peaked at 100 during some period (likely late 2017 bubble).

---

## 5. Understanding Google Trends Values

Google Trends does not provide raw search counts. Instead, it normalises the data:

> **Numbers represent search interest relative to the highest point on the chart for the given region and time. A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. A score of 0 means there was not enough data for this term.**

In simple terms:
- Each data point is divided by the total searches in that region/time to get a proportion.
- These proportions are then scaled so the maximum across the entire dataset becomes 100.
- Thus, a value of 100 indicates the moment (or period) when the term was most popular relative to all searches.

This allows comparison of trends over time, but absolute search volume remains unknown.

**Parameters used in this project** (as noted in the lecture):
- **Tesla**: Worldwide, Web Search
- **Bitcoin**: Worldwide, News Search
- **Unemployment Benefits**: United States, Web Search

The choice of category (Web vs News) affects the data; News search focuses on news-related queries.

---

## 6. Key Takeaways from Data Exploration

- All datasets are time series, but with different frequencies: Tesla and unemployment are monthly; Bitcoin price is daily.
- Search popularity is normalised (0‑100), making it easy to see relative peaks.
- Descriptive statistics reveal the range and distribution of values.
- Understanding the periodicity is essential for later resampling (e.g., aligning daily Bitcoin price with monthly search).

