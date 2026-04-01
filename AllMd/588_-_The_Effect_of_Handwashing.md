## The Effect of Handwashing

In June 1847, Dr. Ignaz Semmelweis mandated that all medical staff wash their hands with a chlorine solution before attending to women in childbirth. This intervention was based on his hypothesis that "cadaverous particles" from autopsies were being transmitted to patients via doctors' hands. The monthly dataset allows us to quantify the impact of this policy by comparing death rates before and after June 1847.

### Dataset Preparation

The monthly data is loaded with the `date` column parsed as datetime. A new column, `pct_deaths`, is added to represent the proportion of deaths per birth for each month.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load monthly data, parsing dates
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])

# Define the exact date handwashing became mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Calculate the proportion of deaths per birth as a decimal
df_monthly['pct_deaths'] = df_monthly['deaths'] / df_monthly['births']
```

**Explanation of variables and code**:

- `pd.read_csv('monthly_deaths.csv', parse_dates=['date'])` reads the CSV and converts the 'date' column to Pandas datetime objects for easy time-based filtering and plotting.
- `handwashing_start` stores the intervention date as a Timestamp.
- `df_monthly['pct_deaths']` creates a new column where each row contains the fraction `deaths / births`. For example, if a month had 300 births and 30 deaths, `pct_deaths = 0.10` (10%).

---

### Challenge 1: Average Death Rates Before and After Handwashing

We split the data into two subsets: before the intervention (dates < 1847-06-01) and after (dates ≥ 1847-06-01). Then we compute the overall death rate (total deaths / total births) for each period.

```python
# Subset: months before handwashing started
before_washing = df_monthly[df_monthly['date'] < handwashing_start]

# Subset: months from handwashing start onward
after_washing = df_monthly[df_monthly['date'] >= handwashing_start]

# Total deaths / total births for the before period, expressed as percentage
bw_rate = before_washing['deaths'].sum() / before_washing['births'].sum() * 100

# Total deaths / total births for the after period, expressed as percentage
aw_rate = after_washing['deaths'].sum() / after_washing['births'].sum() * 100

# Print results with controlled decimal places
print(f'Average death rate before 1847 was {bw_rate:.4}%')   # e.g., 10.53%
print(f'Average death rate AFTER 1847 was {aw_rate:.3}%')    # e.g., 2.15%
```

**Explanation**:

- `df_monthly['date'] < handwashing_start` creates a Boolean mask; using it inside `df_monthly[...]` selects only rows where the condition is True.
- `before_washing['deaths'].sum()` adds all deaths in that period; similarly for births. Dividing gives the overall proportion, then multiplied by 100 converts to percentage.
- The format specifiers `.4` and `.3` in the f‑string control the number of significant digits.

**Result**: The death rate dropped from 10.53% to 2.15% – a dramatic reduction.

---

### Challenge 2: 6‑Month Rolling Average of the Death Rate (Before Handwashing)

To smooth out monthly fluctuations and reveal the underlying trend before the intervention, we compute a 6‑month rolling average of the death proportion. This requires setting the `date` column as the index to avoid losing it during the rolling operation.

```python
# Create a copy of the before-washing data with 'date' as the index
roll_df = before_washing.set_index('date')

# Compute the 6-month rolling mean for all numeric columns
roll_df = roll_df.rolling(window=6).mean()

# The resulting DataFrame contains rolling averages for births, deaths, and pct_deaths
```

**Explanation**:

- `set_index('date')` promotes the date column to the DataFrame index. This index is preserved when applying `.rolling()`.
- `.rolling(window=6)` creates a rolling window of 6 rows (months). The `.mean()` then calculates the average of each column over that window. For the first 5 months, the result is `NaN` because there aren't enough preceding months.
- The new `roll_df` contains the smoothed values. We are particularly interested in `roll_df['pct_deaths']`.

---

### Challenge 3: Highlighting Subsections of a Line Chart

We now create a Matplotlib chart that shows:

- The raw monthly death proportion before handwashing (thin black dashed line).
- The 6‑month rolling average before handwashing (thick crimson dashed line).
- The monthly death proportion after handwashing (skyblue line with round markers).

A legend is added to identify each line.

First, we set up the date locators for the x‑axis (as done previously).

```python
# Create locators for ticks on the time axis
years = mdates.YearLocator()          # marks every year
months = mdates.MonthLocator()         # marks every month (minor ticks)
years_fmt = mdates.DateFormatter('%Y') # formats year as YYYY
```

Now the main plotting code, with comments explaining each part.

```python
# Set figure size and resolution
plt.figure(figsize=(14, 8), dpi=200)

# Add a title
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)

# Set tick label sizes and rotation for readability
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

# Label the y-axis (note: only one y-axis now, as we plot all lines on same scale)
plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

# Get the current axes
ax = plt.gca()

# Configure x-axis with major (year) and minor (month) ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)

# Set x-axis limits to span the entire dataset
ax.set_xlim([df_monthly['date'].min(), df_monthly['date'].max()])

# Add grid lines for better readability
plt.grid(color='grey', linestyle='--', alpha=0.3)

# --- Plot the 6-month moving average (before handwashing) ---
# The rolling average DataFrame 'roll_df' has the date index; we use that as x.
# The comma after 'ma_line' is because .plot() returns a list of lines; we unpack the first element.
ma_line, = plt.plot(roll_df.index,
                    roll_df['pct_deaths'],
                    color='crimson',
                    linewidth=3,
                    linestyle='--',
                    label='6m Moving Average (before)')

# --- Plot the raw monthly death rate before handwashing ---
bw_line, = plt.plot(before_washing['date'],
                    before_washing['pct_deaths'],
                    color='black',
                    linewidth=1,
                    linestyle='--',
                    label='Before Handwashing')

# --- Plot the raw monthly death rate after handwashing ---
aw_line, = plt.plot(after_washing['date'],
                    after_washing['pct_deaths'],
                    color='skyblue',
                    linewidth=3,
                    marker='o',
                    markersize=4,
                    label='After Handwashing')

# Add a legend, using the handles we captured
plt.legend(handles=[ma_line, bw_line, aw_line], fontsize=18)

# Display the plot
plt.show()
```

**Detailed explanation of each part**:

- `plt.figure(figsize=(14,8), dpi=200)`: Creates a figure with width 14 inches, height 8 inches, and resolution 200 dots per inch.
- `plt.title(...)`: Sets the chart title.
- `plt.yticks(fontsize=14)` and `plt.xticks(...)`: Adjust tick label appearance.
- `plt.ylabel(...)`: Labels the y‑axis.
- `ax = plt.gca()`: Gets the current axes object to manipulate the x‑axis ticks.
- `ax.xaxis.set_major_locator(years)`: Places a major tick at each year.
- `ax.xaxis.set_major_formatter(years_fmt)`: Formats major tick labels as years (e.g., 1841).
- `ax.xaxis.set_minor_locator(months)`: Adds minor ticks for each month (visible as small marks, but no labels).
- `ax.set_xlim(...)`: Ensures the plotted lines touch the left and right edges of the figure.
- `plt.grid(...)`: Adds dashed grey grid lines.
- **Plotting the moving average**: `plt.plot(roll_df.index, roll_df['pct_deaths'], ...)`. The x‑values are the dates from the index of `roll_df`; the y‑values are the 6‑month smoothed death proportions.
- **Plotting before‑handwashing raw data**: `plt.plot(before_washing['date'], before_washing['pct_deaths'], ...)`. The raw monthly values are shown as a thin dashed black line.
- **Plotting after‑handwashing raw data**: `plt.plot(after_washing['date'], after_washing['pct_deaths'], ...)`. This line is skyblue, thick, and includes circular markers at each data point.
- **Legend**: Each `plt.plot()` call returns a list of `Line2D` objects; we capture the first element (e.g., `ma_line, = ...`) to use as handles in the legend. The `label` parameter inside each plot provides the text.
- `plt.legend(handles=[ma_line, bw_line, aw_line], fontsize=18)`: Places the legend with the specified handles and font size.

**Interpretation of the resulting chart**:

- Before handwashing, the death rate fluctuates widely, with several months exceeding 20%. The rolling average hovers around 10% to 12%.
- Immediately after June 1847, the death rate plummets. The after‑handwashing line stays mostly below 5%, with only a few small spikes.
- The contrast between the before and after periods is visually striking, providing strong evidence that handwashing had a profound effect.

---

### Summary

Through this analysis, we have:

- Quantified the reduction in average death rate from 10.53% to 2.15%.
- Smoothed the before‑intervention data with a 6‑month rolling average to reveal the underlying trend.
- Created a multi‑line time‑series chart that clearly highlights the impact of handwashing.
- Added a legend to distinguish the three data series.

These visual and numerical results form a compelling argument for the efficacy of handwashing, directly addressing the question Dr. Semmelweis sought to answer. The next section will use additional statistical and graphical methods to further substantiate these findings.