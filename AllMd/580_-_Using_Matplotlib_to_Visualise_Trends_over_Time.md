# Time Series Analysis of Nobel Prize Trends

This section uses Matplotlib to examine how the number of Nobel prizes awarded and the average prize share have evolved over time. The analysis involves grouping data by year, calculating rolling averages, and creating dual‑axis plots to compare trends.

---

## 1. Number of Prizes Awarded Over Time

### Counting Prizes per Year

The first step is to count how many prizes were awarded each year. Because each row in the dataset represents a single laureate (or a prize awarded to an organization), a simple count of rows per year gives the total number of prizes that year.

```python
prize_per_year = df_data.groupby(by='year').count().prize
```

`groupby('year').count()` returns a DataFrame with the count of non‑null entries in each column for every year. Selecting the `prize` column yields a Series indexed by year, with the count of prizes as values.

### Calculating a 5‑Year Rolling Average

Time series data often contain year‑to‑year fluctuations. A rolling average smooths these fluctuations and reveals the underlying trend.

```python
moving_average = prize_per_year.rolling(window=5).mean()
```

The `.rolling(window=5).mean()` method computes the mean over a sliding window of 5 years (the current year plus the previous four). This produces a Series of the same length, with NaN for the first four years where a full window is not available.

### Basic Scatter Plot with Rolling Average Overlaid

A simple way to visualize both the raw data and the smoothed trend is to overlay a scatter plot of the yearly counts with a line plot of the rolling average.

```python
plt.scatter(x=prize_per_year.index,
            y=prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100)

plt.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3)

plt.show()
```

- The scatter points show the actual number of prizes each year.
- The red line shows the 5‑year moving average, making the trend more visible.

### Enhancing the Plot with Customization

To improve readability and professionalism, we add:

- A larger figure size.
- A descriptive title.
- Properly spaced tick marks on the x‑axis (every 5 years from 1900 to 2020).
- Axis limits and labels.

NumPy’s `arange` function generates the tick positions:

```python
import numpy as np
ticks = np.arange(1900, 2021, step=5)
```

The complete customized chart:

```python
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax = plt.gca()               # get current axes
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3)

plt.show()
```

**Interpretation**:
- The number of prizes per year was relatively low and stable until the 1950s.
- A sharp increase begins around the 1960s.
- The two world wars (1914–1918 and 1939–1945) show noticeable gaps or drops in the number of prizes awarded.
- The upward trend after 1960 coincides with the addition of the Economics prize in 1969 and a general trend toward more collaborative or multiple‑winner prizes.

---

## 2. Investigating Prize Sharing Over Time

The second challenge asks whether prizes are being shared among more laureates over time. If more people share a prize, the average share per laureate (as a fraction) should decrease. The `share_pct` column, created earlier, contains each laureate’s fraction of the prize (e.g., 0.5 for a half‑share).

### Calculating Average Prize Share per Year

We group by year and compute the mean of `share_pct`:

```python
yearly_avg_share = df_data.groupby(by='year').agg({'share_pct': 'mean'})
share_moving_average = yearly_avg_share.rolling(window=5).mean()
```

This produces a Series with the average fraction awarded to a laureate in each year, and its 5‑year rolling average.

### Dual‑Axis Plot

To compare the trend in the number of prizes (increasing) with the trend in average share (expected to decrease), we create a second y‑axis on the same plot. Matplotlib’s `twinx()` method creates a new Axes object that shares the same x‑axis but has an independent y‑axis.

```python
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()               # create second y‑axis
ax1.set_xlim(1900, 2020)

# Plot number of prizes on left axis
ax1.scatter(prize_per_year.index,
            prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100)
ax1.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3,
         label='Number of prizes (5‑yr avg)')

# Plot average share on right axis
ax2.plot(prize_per_year.index,
         share_moving_average.values,
         c='grey',
         linewidth=3,
         label='Average share (5‑yr avg)')

plt.show()
```

**Observations**:
- The grey line (average share) trends downward over time, confirming that the prize is being split among more people.
- The downward trend is especially pronounced after the 1950s, mirroring the increase in the number of prizes.
- Both axes are scaled automatically; however, the relationship is clearer if we **invert** the second y‑axis, so that a decreasing average share appears as a rising line, aligning with the increase in prize count.

### Inverting the Second Axis

Adding `ax2.invert_yaxis()` before plotting flips the direction of the right y‑axis:

```python
ax2.invert_yaxis()
```

After inversion, the two smoothed lines move in the same direction, visually reinforcing the correlation: as more prizes are awarded (and thus more sharing occurs), the average share per laureate decreases.

**Final enhanced plot**:

```python
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2020)

ax2.invert_yaxis()               # invert so that both trends move upward together

ax1.scatter(prize_per_year.index,
            prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100)
ax1.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3,
         label='Number of prizes (5‑yr avg)')

ax2.plot(prize_per_year.index,
         share_moving_average.values,
         c='grey',
         linewidth=3,
         label='Average share (5‑yr avg)')

plt.show()
```

**Key Insights**:
- The number of prizes has steadily increased, with a notable acceleration after 1960.
- The average share per laureate has declined correspondingly, indicating that prizes are more frequently shared among multiple winners.
- World War I and II caused interruptions in the awarding of prizes, visible as gaps in the scatter points.
- The addition of the Economics prize in 1969 contributed to the upward trend in prize counts, but the trend was already rising before that date, suggesting broader changes in scientific collaboration and prize‑giving practices.

---

## Technical Notes

- **Rolling averages** are computed using `.rolling(window=5).mean()`. The window size of 5 years was chosen to smooth out short‑term fluctuations while preserving the long‑term trend. Other window sizes could be experimented with.
- **Dual axes** are created with `twinx()`. This is useful for comparing two series with different units or scales. Care must be taken to label axes clearly; the example uses axis colors to differentiate (but does not add explicit axis labels for the right axis – in practice, adding `ax2.set_ylabel('Average share')` would improve clarity).
- **Inverting the y‑axis** is a visual trick that makes a decreasing trend appear increasing. It should be used only when the goal is to show correlation, not absolute values. In this case, it effectively highlights the inverse relationship between prize count and average share.
- **Missing years**: During the world wars, some years had no prizes. The scatter plot shows these as gaps; the rolling average line interpolates across them (because the rolling mean of a window that includes NaN values returns NaN unless we specify `min_periods`). In this dataset, there are no zero entries, so the gaps appear naturally.

---

## Summary

This time‑series analysis demonstrates:

- How to aggregate data by year and compute rolling statistics.
- How to create a polished Matplotlib chart with custom ticks, labels, and size.
- How to overlay two different datasets using a secondary y‑axis.
- How to invert an axis to better visualize an inverse relationship.
