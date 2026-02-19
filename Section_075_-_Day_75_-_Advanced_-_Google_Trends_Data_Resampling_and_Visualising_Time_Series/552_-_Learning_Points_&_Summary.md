# Learning Points & Summary – A Comprehensive Review

## Introduction
Congratulations on completing Day 75! This project has taken you through the entire data science workflow: from loading and exploring raw data, cleaning and resampling time series, to creating polished visualisations that reveal meaningful insights. In this final summary, we consolidate all the key techniques and concepts you have learned.

By the end of this lesson, you will have a handy reference for:
- Descriptive statistics with `.describe()`.
- Resampling time series data with `.resample()`.
- Styling time axes using `matplotlib.dates` Locators and Formatters.
- Handling missing values with `.isna()` and `.dropna()`.
- Controlling chart resolution with `dpi`.
- Using different line styles (`--`, `-.`) and markers (`o`, `^`).
- Customising colours (named colours and HEX codes).
- Adding grids with `.grid()` to identify seasonality.

Each point is illustrated with code snippets and explanations drawn directly from the completed notebook.

---

## 1. Using `.describe()` for Quick Descriptive Statistics

The `.describe()` method generates a summary of central tendency, dispersion, and shape of a DataFrame’s distribution. It’s invaluable for an initial glance at your data.

**Example (Tesla DataFrame):**
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

**What it tells us:**
- The average search popularity for Tesla is about 8.7, with a max of 31.
- The stock price ranges from $3.90 to $498, showing huge growth.
- The quartiles help understand the distribution.

**When to use:** Always run `.describe()` after loading a new dataset to get a feel for the numbers and spot potential outliers.

---

## 2. Resampling Time Series Data with `.resample()`

When combining datasets with different frequencies (e.g., daily Bitcoin price vs. monthly Bitcoin search), we must align them. `.resample()` changes the time frequency.

**Example: Converting daily Bitcoin price to monthly (last closing price):**
```python
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()
```

**Explanation:**
- `'M'` specifies month-end frequency.
- `on='DATE'` tells pandas which column contains the datetime.
- `.last()` picks the last value in each month. Alternative aggregations: `.mean()`, `.max()`, `.sum()`.

**Result:** The new DataFrame has the same number of rows (73) as the monthly search data, making them directly comparable.

**Key rule:** Always choose an aggregation that makes sense for your analysis (e.g., last price for month-end value, mean for average over the month).

---

## 3. Styling Time Axes with `matplotlib.dates` Locators and Formatters

Default date ticks are often too dense or poorly formatted. Locators and formatters give you precise control.

**Setup:**
```python
import matplotlib.dates as mdates

years = mdates.YearLocator()      # Major ticks at start of each year
months = mdates.MonthLocator()     # Minor ticks at start of each month
years_fmt = mdates.DateFormatter('%Y')  # Format major ticks as year only
```

**Applying to a chart:**
```python
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
```

**Why this matters:**
- Major ticks with year labels keep the x-axis uncluttered.
- Minor ticks (months) provide a visual guide without extra labels.
- You can customise formats further (e.g., `'%b %Y'` for "Jan 2010").

**Tip:** Always rotate x‑axis labels if they are long: `plt.xticks(rotation=45)`.

---

## 4. Finding and Handling Missing Values with `.isna()` and `.dropna()`

Real-world data often contains missing values. Pandas provides tools to detect and remove them.

**Checking for missing values:**
```python
print(f'Missing values? {df_btc_price.isna().values.any()}')
print(f'Number missing: {df_btc_price.isna().values.sum()}')
```

**Locating missing rows:**
```python
df_btc_price[df_btc_price.isna().any(axis=1)]
```

**Removing missing rows:**
```python
df_btc_price.dropna(inplace=True)
```

**Important:** `.isna()` returns a Boolean DataFrame. `.values.any()` checks if *any* value is True. `.sum()` counts them. Use `axis=1` in `.any()` to find rows with any missing value.

**Alternative:** Instead of dropping, you could fill missing values with `.fillna()` (e.g., forward fill for time series).

---

## 5. Controlling Chart Resolution with `dpi`

The `dpi` (dots per inch) parameter in `plt.figure()` affects the sharpness of your chart, especially when saved or displayed on high-resolution screens.

**Example:**
```python
plt.figure(figsize=(14,8), dpi=120)
```

- A higher `dpi` (e.g., 120, 300) produces a sharper image but increases file size.
- For on-screen viewing in notebooks, 100–120 is usually sufficient. For publication, 300+ is recommended.

**Combined with `figsize`:** `figsize` sets the physical dimensions; `dpi` sets the pixel density. Total pixels = `figsize[0] * dpi` by `figsize[1] * dpi`.

---

## 6. Line Styles: Dashed `'--'` and Dash-Dot `'-.'`

Matplotlib offers several line styles to differentiate multiple series.

**Common styles:**
- `'-'` or `'solid'` (default)
- `'--'` or `'dashed'`
- `':'` or `'dotted'`
- `'-.'` or `'dashdot'`

**Example (Bitcoin price as dashed line):**
```python
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')
```

**Why use different styles?** They help distinguish lines when printed in black and white or for colourblind viewers.

---

## 7. Markers: `'o'` (circle), `'^'` (triangle), and more

Markers highlight individual data points. They are especially useful when the dataset is not too dense.

**Example (Bitcoin search with circle markers):**
```python
ax2.plot(df_btc_search.MONTH, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')
```

**Common markers:**
- `'o'` – circle
- `'^'` – triangle up
- `'s'` – square
- `'*'` – star
- `'.'` – point
- `'x'` – x

**Customising markers:** You can control size (`markersize`), face colour (`markerfacecolor`), edge colour (`markeredgecolor`), and edge width (`markeredgewidth`).

---

## 8. Fine‑tuning Styling: Limits, Labels, Line Width, and Colours

Every element of a chart can be adjusted to improve clarity and aesthetics.

- **Axis limits:** `ax1.set_ylim(0, 600)` and `ax1.set_xlim(start, end)` focus on the relevant data range.
- **Labels:** Use `set_ylabel()` and `set_xlabel()` with `fontsize` and `color` parameters.
- **Line width:** `linewidth=3` makes lines thicker and more visible.
- **Colours:** Use named colours (e.g., `'skyblue'`) or HEX codes (e.g., `'#E6232E'`). HEX codes give precise control.

**Example (Tesla chart with all elements):**
```python
ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)
ax1.set_ylim([0, 600])
ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
```

---

## 9. Using `.grid()` to Identify Seasonality

Grid lines make it easier to align data points with the time axis, revealing patterns like seasonality.

**Example (unemployment chart):**
```python
ax1.grid(color='grey', linestyle='--')
```

**Why it helps:** In the unemployment data, the grid allowed us to see that many search spikes occur in December – a clear seasonal pattern. You can also add separate grids for major and minor ticks:
```python
ax1.grid(True, which='major', linestyle='-', alpha=0.7)
ax1.grid(True, which='minor', linestyle=':', alpha=0.3)
```

---

## 10. Putting It All Together: A Complete Example

Here’s a full code block that incorporates many of the techniques above (from the Bitcoin chart):

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Assume df_btc_monthly and df_btc_search are ready

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

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

ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(df_btc_search.MONTH, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()
```

---

## Final Thoughts

This project has equipped you with a robust toolkit for handling and visualising time series data. You can now:
- Explore any new dataset with confidence.
- Clean and align data from different sources.
- Create professional, informative charts that tell a story.

Remember that the skills you've practiced – from resampling to grid lines – are transferable to countless real‑world problems: finance, economics, marketing, and beyond. Keep experimenting, keep coding, and never stop asking questions of your data.
