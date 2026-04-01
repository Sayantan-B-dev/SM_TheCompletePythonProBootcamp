# Combining Google Trends with Other Time Series Data – A Comprehensive Guide

## Introduction
Google Trends provides an estimate of search volume for any given term. This popularity data can be compared with other time‑series datasets to uncover interesting relationships. In this project, we explore three distinct questions:

1. **Bitcoin**: Does search volume for "Bitcoin" correlate with its price?
2. **Tesla**: How does search interest in Tesla relate to its stock price?
3. **Unemployment Benefits**: Can searches for "unemployment benefits" predict the actual U.S. unemployment rate?

By the end of this guide, you will learn how to:
- Make time series comparable by **resampling** (e.g., daily → monthly).
- Fine‑tune Matplotlib charts using **limits, labels, linestyles, markers, colours, and resolution**.
- Use **grids** to identify seasonality.
- Handle **missing values** (NaN) in DataFrames.
- Work with **locators and formatters** to style time axes.
- Apply concepts from previous days to new datasets.

We will walk through every step with **code examples and expected outputs** drawn from the completed Jupyter notebook.

---

## 1. Importing Required Libraries
We start by importing the essential libraries:

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Optional: Register converters to avoid warnings with datetime plotting
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
```

**Explanation:**
- `pandas` for data manipulation.
- `matplotlib.pyplot` for plotting.
- `matplotlib.dates` provides locators and formatters for nice date ticks on axes.
- `register_matplotlib_converters()` ensures pandas datetime objects are handled correctly by matplotlib.

---

## 2. Reading the Data
The project uses five CSV files. We load them into DataFrames:

```python
df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')
df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
```

---

## 3. Data Exploration
Before any analysis, we must understand the structure and content of each dataset.

### Tesla DataFrame
```python
print(df_tesla.shape)
df_tesla.head()
```
**Output:**
```
(124, 3)
```

|    | MONTH      | TSLA_WEB_SEARCH | TSLA_USD_CLOSE |
|----|------------|-----------------|----------------|
| 0  | 2010-06-01 | 3               | 4.766          |
| 1  | 2010-07-01 | 3               | 3.988          |
| 2  | 2010-08-01 | 2               | 3.896          |
| 3  | 2010-09-01 | 2               | 4.082          |
| 4  | 2010-10-01 | 2               | 4.368          |

- 124 rows, 3 columns.
- Columns: `MONTH` (string), `TSLA_WEB_SEARCH` (int), `TSLA_USD_CLOSE` (float).
- The data appears to be **monthly** (each row is the first day of the month).

**Periodicity:** The `MONTH` column shows dates at monthly intervals → monthly time series.

**What does a value of 100 in Google Trends mean?**  
Google Trends normalises search interest: the highest point in the selected time range is set to 100. All other values are relative to that peak. So a value of 100 indicates the maximum popularity for that term in the given period.

```python
print(f'Largest value for Tesla in Web Search: {df_tesla.TSLA_WEB_SEARCH.max()}')
print(f'Smallest value for Tesla in Web Search: {df_tesla.TSLA_WEB_SEARCH.min()}')
```
**Output:**
```
Largest value for Tesla in Web Search: 31
Smallest value for Tesla in Web Search: 2
```

**Descriptive statistics:**
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

---

### Unemployment Data (2004‑2019)
```python
print(df_unemployment.shape)
df_unemployment.head()
```
**Output:**
```
(181, 3)
```

|    | MONTH   | UE_BENEFITS_WEB_SEARCH | UNRATE |
|----|---------|------------------------|--------|
| 0  | 2004-01 | 34                     | 5.7    |
| 1  | 2004-02 | 33                     | 5.6    |
| 2  | 2004-03 | 25                     | 5.8    |
| 3  | 2004-04 | 29                     | 5.6    |
| 4  | 2004-05 | 23                     | 5.6    |

- 181 rows, 3 columns.
- Columns: `MONTH` (string), `UE_BENEFITS_WEB_SEARCH` (int), `UNRATE` (float).
- Monthly data again.

```python
print('Largest value for "Unemployment Benefits" '
      f'in Web Search: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}')
```
**Output:**
```
Largest value for "Unemployment Benefits" in Web Search: 100
```

---

### Bitcoin Price (Daily)
```python
print(df_btc_price.shape)
df_btc_price.head()
```
**Output:**
```
(2204, 3)
```

|    | DATE       | CLOSE       | VOLUME      |
|----|------------|-------------|-------------|
| 0  | 2014-09-17 | 457.334015  | 21056800.0  |
| 1  | 2014-09-18 | 424.440002  | 34483200.0  |
| 2  | 2014-09-19 | 394.795990  | 37919700.0  |
| 3  | 2014-09-20 | 408.903992  | 36863600.0  |
| 4  | 2014-09-21 | 398.821014  | 26580100.0  |

- 2204 rows, 3 columns.
- Columns: `DATE` (string), `CLOSE` (float), `VOLUME` (float).
- **Daily** frequency.

---

### Bitcoin Search (Monthly)
```python
print(df_btc_search.shape)
df_btc_search.head()
```
**Output:**
```
(73, 2)
```

|    | MONTH   | BTC_NEWS_SEARCH |
|----|---------|-----------------|
| 0  | 2014-09 | 5               |
| 1  | 2014-10 | 4               |
| 2  | 2014-11 | 4               |
| 3  | 2014-12 | 4               |
| 4  | 2015-01 | 5               |

- 73 rows, 2 columns.
- Columns: `MONTH` (string), `BTC_NEWS_SEARCH` (int).
- Monthly data.

```python
print(f'largest BTC News Search {df_btc_search.BTC_NEWS_SEARCH.max()}')
```
**Output:**
```
largest BTC News Search 100
```

---

## 4. Data Cleaning
### 4.1 Checking for Missing Values
```python
print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
print(f'Missing values? for BTC price?: {df_btc_price.isna().values.any()}')
```
**Output:**
```
Missing values for Tesla?: False
Missing values for U/E?: False
Missing values for BTC Search?: False
Missing values? for BTC price?: True
```

The Bitcoin price DataFrame contains missing values. Let's inspect them:

```python
print(f'Number of missing values: {df_btc_price.isna().values.sum()}')
df_btc_price[df_btc_price.CLOSE.isna()]
```
**Output:**
```
Number of missing values: 2
```

|      | DATE       | CLOSE | VOLUME |
|------|------------|-------|--------|
| 2148 | 2020-08-04 | NaN   | NaN    |

We see one row (index 2148) with both `CLOSE` and `VOLUME` missing. Possibly there were two missing rows; the notebook output shows only one, but the count is 2. We will remove them:

```python
df_btc_price.dropna(inplace=True)
```

After this, `df_btc_price.isna().values.any()` should return `False`.

---

### 4.2 Converting Strings to Datetime Objects
All DataFrames have date columns stored as strings. We convert them to proper datetime objects for plotting and resampling.

```python
# Check current type
type(df_tesla.MONTH[0])   # str

df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

# Verify
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

---

### 4.3 Resampling: Daily → Monthly for Bitcoin Price
Because Bitcoin price is daily but search data is monthly, we need to align them. We resample price to monthly frequency, taking the last closing price of each month.

```python
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()
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

Now `df_btc_monthly` has 73 rows, matching the 73 rows of `df_btc_search`. They can be plotted together.

**Note:** `resample('M')` uses the end of each month. The `on='DATE'` tells pandas to use that column as the time index.

---

## 5. Data Visualisation
We will now create compelling charts to visualise relationships.

### 5.1 Setting Up Style Helpers
To get nicely formatted date ticks, we create locators and formatters:

```python
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
```

These will be used to place major ticks at year boundaries and minor ticks at month boundaries, with year labels.

---

### 5.2 Tesla Stock Price vs. Search Volume
**Goal:** Plot Tesla’s stock price (left axis) and its search popularity (right axis) on the same chart.

**Basic chart (without styling):**
```python
ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price')
ax2.set_ylabel('Search Trend')

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH)

plt.show()
```
This produces a simple line chart but lacks styling.

**Improved chart with colours, labels, and formatting:**
```python
plt.figure(figsize=(14,8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Format x-axis ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# Set axis limits
ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

# Plot with colours and thicker lines
ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
```
**Explanation of enhancements:**
- `figsize=(14,8)` and `dpi=120` enlarge the chart and improve resolution.
- `plt.xticks(rotation=45)` prevents overlapping date labels.
- `ax1.xaxis.set_major_locator(years)` places major ticks at year boundaries; `set_major_formatter(years_fmt)` shows only the year.
- Minor ticks (`months`) appear but are not labelled, giving a finer grid.
- `set_ylim` and `set_xlim` focus the view on relevant ranges.
- Colour hex `#E6232E` is a vivid red for stock price; `skyblue` for search trend.
- `linewidth=3` makes lines thicker.

**Observation:** Tesla’s stock price remained low for many years, then skyrocketed after 2019. Search interest also increased but not as dramatically; the peak in search volume (31) occurred in 2020, while price exceeded 500.

---

### 5.3 Bitcoin Price vs. Search Volume
**Goal:** Compare Bitcoin’s monthly price (dashed line) with search volume (line with circle markers).

```python
plt.figure(figsize=(14,8), dpi=120)
plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Plot with custom linestyle and markers
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()
```
**Key additions:**
- `linestyle='--'` makes the price line dashed.
- `marker='o'` places circular markers on the search trend line, highlighting each monthly data point.
- Orange colour `#F08F2E` for Bitcoin price.

**Observation:** Spikes in Bitcoin search volume (e.g., late 2017) coincided with huge price increases, suggesting that public interest surged alongside the price rally.

---

### 5.4 Unemployment Benefits Search vs. Actual Unemployment Rate
**Goal:** Plot the search volume for "unemployment benefits" against the official U.S. unemployment rate (FRED data).

**Basic plot with grid:**
```python
plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

# Add grid
ax1.grid(color='grey', linestyle='--')

ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE,
         color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3)

plt.show()
```
**Observations:**
- The unemployment rate (purple, dashed) shows clear peaks during recessions (e.g., 2008‑2009).
- Search volume (blue) rises sharply at the same times, but also exhibits **seasonal patterns** – often spiking in January (perhaps due to year‑end job cuts or new benefit claims). The grid helps to see these annual cycles.
- After the 2008 crisis, search interest remained elevated even as unemployment fell, suggesting persistent public concern.

**Rolling average to smooth noise:**
We can calculate a 6‑month rolling average of both series to see the underlying trend more clearly.

```python
roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()

plt.figure(figsize=(14,8), dpi=120)
plt.title('Rolling Monthly US "Unemployment Benefits" Web Searches vs UNRATE (6‑month avg)', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('FRED U/E Rate (6‑month avg)', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend (6‑month avg)', color='skyblue', fontsize=16)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH[0], df_unemployment.MONTH.max()])

ax1.plot(df_unemployment.MONTH, roll_df.UNRATE, 'purple', linewidth=3, linestyle='-.')
ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()
```
The rolling average smooths out short‑term fluctuations, making the correlation between the two series more apparent.

---

### 5.5 Including 2020 Data
The COVID‑19 pandemic caused unprecedented unemployment. Let's incorporate data up to 2020.

```python
df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

plt.figure(figsize=(14,8), dpi=120)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
plt.title('Monthly US "Unemployment Benefits" Web Search vs UNRATE incl 2020', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])

ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, 'purple', linewidth=3)
ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()
```
**Dramatic observation:** In early 2020, the unemployment rate shot up to nearly 15%, while searches for unemployment benefits exploded to 100 (the maximum normalised value). This shows how Google Trends can be a real‑time indicator of economic distress.

---

## 6. Learning Points & Summary
In this project, you have learned:

1. **Resampling time series** – converting daily data to monthly using `.resample().last()`.
2. **Handling missing data** – identifying and removing NaN values with `.isna()` and `.dropna()`.
3. **Converting string dates** – using `pd.to_datetime()` for proper datetime objects.
4. **Creating dual‑axis charts** – with `twinx()` to overlay two different scales.
5. **Styling charts** – colours, linewidth, linestyle, markers, figure size, DPI, and axis limits.
6. **Formatting time axes** – using `mdates.YearLocator`, `MonthLocator`, and `DateFormatter` for clear date ticks.
7. **Adding grids** – to reveal seasonality and long‑term patterns.
8. **Using rolling averages** – to smooth noisy data and highlight trends.

These techniques are widely applicable in data analysis, finance, economics, and any field involving time‑series data.
