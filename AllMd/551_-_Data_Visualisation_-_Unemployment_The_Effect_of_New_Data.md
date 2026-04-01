# Data Visualisation – Unemployment: The Effect of New Data

## Introduction
In the previous lesson, we visualised the relationship between searches for "unemployment benefits" and the official U.S. unemployment rate using data from 2004 to 2019. We observed the impact of the 2008 financial crisis and noted seasonal patterns. Now, we incorporate data from 2020 – the year of the COVID‑19 pandemic – to see how the unprecedented economic shock affects the picture.

Adding new data to a Google Trends analysis is not trivial: because Google Trends normalises search interest relative to the peak within the selected time range, extending the time period to include a massive spike will **rescale all earlier values**. The new peak (likely in 2020) becomes 100, and all previous data points are recalculated relative to that new maximum. This means the search numbers in the 2004–2020 file will be different from those in the 2004–2019 file. Understanding this rescaling is key to interpreting the chart.

In this lesson, we will:
- Load the extended dataset (`UE Benefits Search vs UE Rate 2004-20.csv`).
- Convert the date column to datetime.
- Create a dual‑axis chart similar to before, but now covering 2004–2020.
- Observe the dramatic effect of the pandemic.
- Discuss the rescaling of search interest.

---

## 1. Loading and Preparing the 2020 Data

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Read the extended CSV
df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')

# Convert the MONTH column to datetime
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

# Check the first few rows
print(df_ue_2020.head())
```

**Output (first 5 rows):**
```
      MONTH  UE_BENEFITS_WEB_SEARCH  UNRATE
0 2004-01-01                       9     5.7
1 2004-02-01                       8     5.6
2 2004-03-01                       7     5.8
3 2004-04-01                       8     5.6
4 2004-05-01                       9     5.6
```

**Important observation:**  
Compare these search values with the 2004–2019 dataset (which had values like 34, 33, 25 for the same months). The numbers are now much smaller because the 2020 spike (which will be set to 100) dwarfs everything before. This rescaling is automatic when you download a new time range from Google Trends. Always be aware that the absolute numbers are only meaningful within a single dataset – you cannot directly compare two separate downloads.

---

## 2. Creating the Chart

We reuse the same plotting code as before, but we must adjust the y‑axis limits to accommodate the huge unemployment spike (the unemployment rate reached nearly 15% in 2020). The previous limit of 10.5 would cut off the top. We can either set a new upper limit (e.g., 15) or let Matplotlib autoscale. For clarity, we'll set `ax1.set_ylim(0, 15)`.

We also keep the same locators and formatters for the x‑axis.

```python
# Set up locators and formatter (same as before)
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly US "Unemployment Benefits" Web Search vs UNRATE incl 2020', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Format x-axis
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# Labels and colours
ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

# Set axis limits: note the y-limit extended to 15 to capture 2020 peak
ax1.set_ylim(0, 15)
ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])

# Plot data (using the new DataFrame)
ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, 'purple', linewidth=3)
ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()
```

**Expected output:**  
A chart with:
- X‑axis: 2004 to 2020, with major ticks at each year.
- Left y‑axis (purple): unemployment rate, now peaking near 15 in 2020.
- Right y‑axis (blue): search popularity, now with a massive spike in 2020 reaching 100, and all previous values compressed to lower numbers (e.g., the 2008 peak is now much smaller than it appeared in the 2004‑2019 chart).

---

## 3. Observations and Interpretation

### 3.1 The COVID‑19 Shock
The chart reveals an unprecedented spike in both the unemployment rate and searches for unemployment benefits during early 2020. The unemployment rate jumped from around 3.5% to nearly 15% in a matter of months – far exceeding the peak of the 2008 financial crisis (which was about 10%). Similarly, search interest rocketed to 100, the maximum possible value.

### 3.2 Rescaling Effect
Because the 2020 search peak is set to 100, the previous peaks (like 2008–2009) now appear much smaller. For example, in the 2004‑2019 dataset, the 2008 search peak was 100; now it might be around 30 or 40. This does **not** mean that searches were lower in 2008 than we previously thought; it simply means the 2020 spike was so much larger that it redefines the scale. Always interpret Google Trends numbers relative to the time range of the downloaded data.

### 3.3 Speed of Increase
Both series show a near‑vertical rise in March–April 2020, reflecting the rapid onset of the pandemic and associated lockdowns. This contrasts with the more gradual rise during the 2008 financial crisis, which unfolded over many months.

### 3.4 Potential for a Faster Recovery?
The lesson note expresses hope that recovery will be swifter. While the chart doesn’t show post‑2020 data, we can speculate that policy responses (stimulus, vaccine rollout) might lead to a quicker rebound than after 2008. However, the long‑term effects remain to be seen.

---

## 4. Adjusting the Chart for Better Comparison

If you want to compare the relative magnitudes of the 2008 and 2020 search spikes more fairly, you would need to download the data separately for each period and keep them as separate series – but then they wouldn't share the same scale. Alternatively, you could use the raw (non‑normalised) data, which is not available from Google Trends. The key takeaway: Google Trends is excellent for showing **timing** and **relative patterns within a dataset**, but cross‑dataset comparisons require caution.

You might also consider using a logarithmic scale for the y‑axis to better visualise the relative changes, but that would complicate interpretation for a general audience.

---

## 5. Summary

- Adding 2020 data dramatically changes the chart: the COVID‑19 pandemic caused an unprecedented spike in both unemployment and related searches.
- Google Trends normalisation rescales all previous data relative to the new peak, so earlier values appear smaller.
- The visualisation reinforces that the 2020 shock was far larger and faster than the 2008 crisis.
- This analysis demonstrates the importance of understanding data provenance and normalisation when working with Google Trends.

