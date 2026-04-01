## Preliminary Data Exploration and Visualization of Births and Deaths

This section details the initial examination of the dataset used in Dr. Semmelweis’s investigation. The goal is to understand the structure, quality, and basic statistics of the monthly and yearly records, and to create a visual overview that reveals patterns over time.

### Dataset Overview

Two CSV files are provided:

- **`monthly_deaths.csv`**: Contains 98 rows of monthly totals for births and deaths from January 1841 to March 1849.
- **`annual_deaths_by_clinic.csv`**: Contains 12 rows of yearly totals for births and deaths, split by clinic (clinic 1 and clinic 2), covering the years 1841 to 1846.

Both datasets are loaded into pandas DataFrames. The monthly data’s `date` column is parsed as a datetime object to facilitate time‑series operations.

```python
import pandas as pd

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])
```

---

### Challenge 1: Preliminary Data Exploration

The first challenge is to inspect the DataFrames and answer basic questions about their content and quality.

#### Shape and Column Names

```python
print(df_yearly.shape)   # (12, 4)
print(df_yearly.columns) # Index(['year', 'births', 'deaths', 'clinic'], dtype='object')

print(df_monthly.shape)  # (98, 3)
print(df_monthly.columns) # Index(['date', 'births', 'deaths'], dtype='object')
```

The yearly data has 12 rows and 4 columns; the monthly data has 98 rows and 3 columns.

#### Years Included

Using `df_yearly['year'].unique()` we see the years 1841 through 1846 are present. The monthly data, as shown by `df_monthly['date'].dt.year.unique()`, spans 1841 to 1849.

#### Missing Values and Duplicates

```python
print(df_yearly.info())
print(df_monthly.info())
```

Both DataFrames have no missing values (all columns are non‑null). An alternative check:

```python
print(f'Any yearly NaN values? {df_yearly.isna().values.any()}')   # False
print(f'Any monthly NaN values? {df_monthly.isna().values.any()}') # False
```

Duplicate checks:

```python
print(f'Any yearly duplicates? {df_yearly.duplicated().values.any()}')   # False
print(f'Any monthly duplicates? {df_monthly.duplicated().values.any()}') # False
```

Thus the data is clean and ready for analysis.

#### Average Births and Deaths per Month

```python
df_monthly.describe()
```

The output shows:

- Mean births per month: 267.00
- Mean deaths per month: 22.47
- Minimum deaths: 0 (some months had no deaths)
- Maximum deaths: 75

These statistics give a first glimpse of the scale of the problem.

---

### Challenge 2: Percentage of Women Dying in Childbirth

Using the annual data, we compute the overall mortality rate for the entire period 1841–1846.

```python
prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')
```

**Output**: `Chances of dying in the 1840s in Vienna: 7.08%`

This means about 7 in 100 women who gave birth at the hospital died. For context, the maternal death rate in the United States in 2013 was 18.5 per 100,000, or 0.018%. The 1840s rate is nearly 400 times higher, highlighting the extreme danger of childbirth in that era.

---

### Challenge 3: Visualising Total Number of Births and Deaths over Time

To see trends and anomalies, we plot the monthly births and deaths on a single chart with twin y‑axes.

#### Setting Up Date Locators

For clear axis ticks, we use Matplotlib’s date locators and formatters:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

years = mdates.YearLocator()      # marks every year
months = mdates.MonthLocator()     # marks every month (minor ticks)
years_fmt = mdates.DateFormatter('%Y')  # format year as YYYY
```

#### Creating the Twin‑Axis Plot

The chart uses two y‑axes: the left for births, the right for deaths. The lines are styled with different colors and thicknesses.

```python
plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)

# Rotate and enlarge tick labels for readability
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()                     # left axis
ax2 = ax1.twinx()                   # right axis sharing same x-axis

ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

# Set x-axis limits to touch the first and last data points
ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--', alpha=0.3)

# Plot births on left axis
ax1.plot(df_monthly.date, df_monthly.births,
         color='skyblue', linewidth=3, label='Births')

# Plot deaths on right axis (dashed line)
ax2.plot(df_monthly.date, df_monthly.deaths,
         color='crimson', linewidth=2, linestyle='--', label='Deaths')

plt.show()
```

#### Interpretation of the Chart

The resulting plot reveals a clear pattern:

- Births increase gradually over the decade, indicating the hospital became busier.
- Deaths fluctuate widely, with several spikes in the early 1840s.
- **Crucially, after mid‑1847, the number of deaths drops sharply and remains low, despite the rising number of births.** This visual clue is the first evidence that something changed around that time – the period when Dr. Semmelweis introduced mandatory handwashing with chlorine.

The twin‑axis plot effectively communicates the divergent trends and sets the stage for deeper analysis.

---

### Summary of Preliminary Findings

- The dataset is complete, with no missing values or duplicates.
- The average monthly death rate from childbirth was 22.47, and the overall mortality rate over six years was 7.08%.
- A time‑series plot of births and deaths shows a dramatic decline in deaths starting in mid‑1847, coinciding with the handwashing intervention.
- This initial exploration confirms that the data is suitable for further analysis and highlights the need to investigate the impact of handwashing more rigorously.