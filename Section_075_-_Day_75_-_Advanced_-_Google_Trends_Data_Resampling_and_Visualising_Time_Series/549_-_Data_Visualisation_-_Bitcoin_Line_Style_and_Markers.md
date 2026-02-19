# Data Visualisation – Bitcoin: Line Style and Markers

## Introduction
After mastering the Tesla chart, we now apply similar techniques to the Bitcoin dataset. However, Bitcoin brings its own nuances: we have resampled the daily price to monthly frequency, and we want to explore whether spikes in search volume correspond to price surges. This lesson focuses on:

- Reusing and adapting the Tesla chart code for Bitcoin.
- Customising **line styles** (e.g., dashed lines) for the price.
- Adding **markers** (e.g., circles) to the search data points.
- Adjusting axis limits and labels appropriately.
- Interpreting the resulting visualisation.

By the end, you will have a polished dual‑axis chart showing Bitcoin’s monthly closing price (dashed orange line) and its monthly news search popularity (solid blue line with circle markers).

---

## 1. Preparing the Data (Review)
Recall from Lesson 546 that we resampled the daily Bitcoin price to monthly frequency using the last closing price of each month. We also have the monthly Bitcoin search data. Both DataFrames have the same number of rows (73) and cover the same time period.

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Load and clean (assuming done previously)
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')
df_btc_price.dropna(inplace=True)
df_btc_price['DATE'] = pd.to_datetime(df_btc_price['DATE'])

df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_search['MONTH'] = pd.to_datetime(df_btc_search['MONTH'])

# Resample price to monthly (end of month)
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()

print("Price monthly shape:", df_btc_monthly.shape)
print("Search shape:", df_btc_search.shape)
```

**Output:**
```
Price monthly shape: (73, 3)
Search shape: (73, 2)
```

Now both datasets are ready for plotting.

---

## 2. Setting Up Locators and Formatters
We reuse the same locators and formatter from the Tesla lesson to have consistent date ticks:

```python
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
```

---

## 3. Creating the Bitcoin Chart

We start with the Tesla code template and modify it for Bitcoin. Key changes:
- Title: `'Bitcoin News Search vs Resampled Price'`
- Left y‑axis label: `'BTC Price'`
- Right y‑axis label: `'Search Trend'` (same)
- Colour for price: orange (`'#F08F2E'`)
- Colour for search: skyblue (same)
- Data for price: `df_btc_monthly.index` (the resampled dates) and `df_btc_monthly.CLOSE`
- Data for search: `df_btc_search.MONTH` and `df_btc_search.BTC_NEWS_SEARCH`
- Y‑axis limits: price from 0 to 15,000 (to cover the range up to ~$19,000 but we cap at 15,000 for better view; you can adjust).
- **Line style for price**: dashed (`linestyle='--'`)
- **Marker for search**: circles (`marker='o'`)

### 3.1 Complete Code

```python
plt.figure(figsize=(14,8), dpi=120)

plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Format x-axis ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# Labels and colours
ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# Axis limits
ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Plot price (dashed line)
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')

# Plot search (solid line with circle markers)
ax2.plot(df_btc_search.MONTH, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()
```

**Explanation of new parameters:**
- `linestyle='--'` produces a dashed line. Other common styles: `'-'` (solid), `':'` (dotted), `'-.'` (dash‑dot).
- `marker='o'` places a circle at each data point. Many markers exist: `'s'` (square), `'^'` (triangle), `'*'` (star), `'.'` (point), etc. The size can be controlled with `markersize` (e.g., `markersize=8`).

---

## 4. Expected Output and Interpretation

When you run the code, you get a chart with:
- X‑axis: years from ~2014 to 2020, with major ticks at each year and minor ticks at each month.
- Left y‑axis (BTC Price): orange dashed line, ranging from 0 to 15,000.
- Right y‑axis (Search Trend): blue solid line with circles, ranging from 0 to 100.

**Observations:**
- The most dramatic spike in Bitcoin price occurred in late 2017 / early 2018, reaching nearly $20,000 (though our y‑limit cuts it at 15,000; you can adjust to see the full peak). This spike was accompanied by a huge surge in search popularity, hitting 100.
- Another price increase in mid‑2019 (up to ~$13,000) saw a much smaller increase in search interest. This suggests that by 2019, Bitcoin had become more widely known, so price movements didn’t generate the same level of new curiosity.
- Search interest remained relatively low before 2017 and after the 2018 crash, despite subsequent price rallies.

Thus, the visualisation clearly shows that **big increases in searches did coincide with the biggest price run‑up**, but later price increases were not mirrored by equally large search spikes.

---

## 5. Customising Markers and Line Styles Further

### 5.1 Marker Size and Edge
You can enhance markers with additional parameters:

```python
ax2.plot(df_btc_search.MONTH, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=2, marker='o', markersize=6,
         markerfacecolor='white', markeredgecolor='skyblue', markeredgewidth=2)
```

This would create hollow circles with a blue edge, which might stand out better.

### 5.2 Different Line Styles for Comparison
If you wanted to compare two different price series (e.g., closing price vs. opening price), you could use different linestyles: one solid, one dashed.

### 5.3 Combining Markers and Lines
You can also plot only markers without lines (using `linestyle=''`) or only lines without markers (the default). The combination helps emphasise individual data points, especially when the dataset is not too dense.

---

## 6. Full Example with Additional Tweaks

Here’s a slightly enhanced version that also adjusts the marker appearance and adds a grid:

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

ax1.set_ylim(0, 20000)   # Extend to capture full 2017 peak
ax1.set_xlim(df_btc_monthly.index.min(), df_btc_monthly.index.max())

# Add grid for better readability
ax1.grid(True, which='major', linestyle='-', alpha=0.5)
ax1.grid(True, which='minor', linestyle=':', alpha=0.3)

# Price line (dashed)
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')

# Search line with markers
ax2.plot(df_btc_search.MONTH, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=2, marker='o', markersize=5,
         markerfacecolor='white', markeredgecolor='skyblue')

plt.show()
```

**Note:** The grid on the left axis (`ax1`) appears behind both lines. The minor grid (dotted) helps see month‑level divisions.

---

## 7. Key Takeaways

- **Line styles** (`linestyle`) and **markers** (`marker`) are simple but powerful ways to differentiate data series.
- Always ensure your time axes are properly formatted with locators and formatters for a professional look.
- Resampling daily data to monthly (using `.resample().last()`) aligns frequencies for comparison.
- The resulting chart can reveal important insights: here, the correlation between Bitcoin’s price and public interest (search volume) was strongest during the 2017 bubble, but later price moves generated less buzz.

