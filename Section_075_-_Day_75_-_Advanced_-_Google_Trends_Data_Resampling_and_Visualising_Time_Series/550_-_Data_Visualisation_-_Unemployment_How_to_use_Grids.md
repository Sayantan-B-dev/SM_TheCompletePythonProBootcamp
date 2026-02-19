# Data Visualisation – Unemployment: How to Use Grids

## Introduction
In this lesson, we continue our exploration of Google Trends data by examining the relationship between searches for **"unemployment benefits"** and the actual **U.S. unemployment rate** (from FRED). Our goals are:

- Create a dual‑axis chart with proper date formatting (using locators and formatters).
- Add a **grid** to the chart to better visualise time‑based patterns.
- Observe **seasonality** in search volume.
- Compute and plot a **rolling average** (6‑month window) to smooth out noise and identify leading/lagging relationships.

By the end, you will understand how grids can help spot recurring patterns, and how rolling averages can reveal which variable moves first – a classic technique in economic analysis.

---

## 1. Data Preparation (Review)

We assume the unemployment DataFrame (`df_unemployment`) has been loaded and cleaned as in previous lessons:

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Load data (2004-2019)
df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)

# Set up locators/formatters (reused from Tesla lesson)
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
```

The DataFrame has columns: `MONTH` (datetime), `UE_BENEFITS_WEB_SEARCH` (int, 0‑100), and `UNRATE` (float, percentage).

---

## 2. Basic Unemployment Chart with Grid

We start with a chart similar to the Tesla/Bitcoin ones, but now we add a **grid** on the left axis to help align events with time.

### 2.1 Code

```python
plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Format x-axis
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# Labels and colours
ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# Axis limits
ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

# Add grid (dashed grey lines) to the left axis
ax1.grid(color='grey', linestyle='--')

# Plot data
ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE,
         color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3)

plt.show()
```

### 2.2 Explanation of New Elements

- **`ax1.grid(color='grey', linestyle='--')`**  
  This adds a grid to the left axis (`ax1`). The grid lines are drawn at the positions of the major ticks (by default). We specify `color='grey'` and `linestyle='--'` for dashed grey lines. The grid helps visually align data points with the time axis.

- **Axis limits**: We set `ax1.set_ylim(bottom=3, top=10.5)` to focus on the typical range of unemployment rates (excluding the extreme COVID‑19 spike, which is not in this dataset). The x‑axis covers the full range of the data (2004‑2019).

### 2.3 Output and Observations

**Output:** A chart with two lines:
- Purple dashed line: FRED unemployment rate.
- Skyblue solid line: search popularity for "unemployment benefits".

The grid makes it easy to see:
- **Seasonality**: Many spikes in the blue search line occur around **year‑end (December)**. This suggests that searches for unemployment benefits increase during the holiday season, possibly due to seasonal job losses or the end of temporary contracts.
- **Major events**: The 2008‑2009 financial crisis shows a dramatic rise in both unemployment rate and search volume. It took about a decade for unemployment to return to pre‑crisis levels.
- **Anomaly**: A large spike in searches at the end of 2013 is not accompanied by a corresponding rise in unemployment. This could be due to changes in benefit policies, media coverage, or other external factors.

The grid is essential for spotting these patterns – without it, the vertical alignment of spikes with years/months would be much harder.

---

## 3. Smoothing with a Rolling Average

The raw search data is quite noisy month‑to‑month. To see the underlying trend more clearly, we compute a **rolling average** (also called moving average). This smooths out short‑term fluctuations and can reveal lead‑lag relationships.

### 3.1 Calculating the Rolling Average

Pandas provides the `.rolling()` method, which creates a window of a specified size. We then apply `.mean()` to get the average over that window.

```python
# Create a 6-month rolling average for both columns
roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()
```

- `window=6` means we average the current month and the previous 5 months. The result is a DataFrame with the same index, but the first 5 rows will be `NaN` (insufficient data for a full window). We'll plot only the non‑NaN part.

### 3.2 Plotting the Rolling Averages

```python
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

# Plot the rolling averages
ax1.plot(df_unemployment.MONTH, roll_df.UNRATE,
         color='purple', linewidth=3, linestyle='-.')
ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3)

plt.show()
```

### 3.3 Interpreting the Rolling Average Chart

**Observations:**

- Both lines are much smoother. The seasonal spikes in search volume are attenuated, revealing longer‑term trends.
- Crucially, the **blue search line tends to rise before the purple unemployment line**. This is most evident around the 2008 crisis: searches for unemployment benefits started increasing in late 2007 / early 2008, while the official unemployment rate began its steep climb a few months later. Similarly, after the peak, search volume declines before the unemployment rate does.
- This indicates that **Google search data can act as a leading indicator** for the unemployment rate. People start searching for unemployment benefits when they anticipate or experience job loss, whereas the official rate (a lagging indicator) takes time to reflect those changes through surveys and reporting.

The rolling average helps confirm this lead‑lag relationship by removing the noise that might obscure the timing.

---

## 4. Additional Insights and Discussion

### 4.1 Why Use a 6‑Month Window?
The choice of window size is somewhat arbitrary. A 3‑month window would be less smooth but might retain more detail; a 12‑month window would be even smoother but could obscure shorter‑term shifts. Six months is a common compromise for economic indicators, balancing noise reduction and responsiveness.

### 4.2 Seasonality in Raw Data
The raw chart with grid clearly shows annual spikes in December/January. This is consistent with known seasonal patterns in the labour market (e.g., retail hiring for holidays, then layoffs in January). The grid makes this seasonality immediately visible.

### 4.3 The 2013 Anomaly
The unexplained spike in late 2013 (raw data) is a reminder that correlation does not imply causation. Perhaps a specific news event or policy change (like the expiration of extended unemployment benefits) drove searches without affecting the unemployment rate. Further investigation would be needed.

### 4.4 Grid Customisation
We used `ax1.grid(color='grey', linestyle='--')`. You can also control which ticks the grid applies to (`which='major'` or `'minor'`) and add separate grids for minor ticks. For example:
```python
ax1.grid(True, which='major', linestyle='-', alpha=0.7)
ax1.grid(True, which='minor', linestyle=':', alpha=0.3)
```
This would give solid lines for major years and dotted for months.

---

## 5. Summary

In this lesson we:

- Created a dual‑axis chart for unemployment benefits search vs. actual unemployment rate.
- Added a **grid** to the left axis to improve readability and identify seasonal patterns.
- Observed **seasonality** (year‑end spikes) and the impact of the 2008 financial crisis.
- Computed a **6‑month rolling average** to smooth the data.
- Discovered that searches for unemployment benefits **lead** the official unemployment rate – a valuable insight for economic forecasting.

