# Using Locators and DateFormatters to Generate Tick Marks on a Time Line

## Introduction
When plotting time series data, one common challenge is controlling the appearance of tick marks and labels on the x‑axis. By default, Matplotlib may place ticks at intervals that are too dense or too sparse, and the date formatting might not be ideal. This is where **locators** and **formatters** from `matplotlib.dates` come to the rescue.

In this lesson, we will learn how to:
- Use `YearLocator` and `MonthLocator` to set major and minor tick positions.
- Apply a `DateFormatter` to display dates in a custom format (e.g., only the year).
- Integrate these tools into the Tesla stock price vs. search popularity chart.
- Observe how proper tick marks enhance readability and reveal interesting events (like the Tesla Model 3 unveiling spike).

All code examples are based on the completed notebook and assume the data has been cleaned and the basic chart is already built.

---

## 1. The Problem: Default Tick Marks

Let’s revisit the Tesla chart from the previous lesson without any custom tick formatting:

```python
plt.figure(figsize=(14,8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
```

**Output:**  
The chart is already quite readable, but the x‑axis tick labels show the full date (e.g., "2010-06-01") and are rotated 45 degrees. However, the tick density might not be optimal: Matplotlib automatically chooses about 5–10 ticks, which for a 10‑year span could be every 2 years or so. But we might want more control: maybe we want a major tick every year and a minor tick every month, with only the year displayed.

---

## 2. The Solution: Locators and Formatters

`matplotlib.dates` provides classes that control tick placement (`Locator`) and tick label formatting (`Formatter`). Commonly used locators:
- `YearLocator()` – places ticks at the start of each year.
- `MonthLocator()` – places ticks at the start of each month.
- `DayLocator()`, `HourLocator()`, etc., for finer granularity.

Formatters:
- `DateFormatter('%Y')` – formats dates as four‑digit years.
- Other format codes: `'%Y-%m'` for year‑month, `'%b %Y'` for abbreviated month and year, etc.

### 2.1 Importing the Module and Creating Locators/Formatters

```python
import matplotlib.dates as mdates

years = mdates.YearLocator()      # every year
months = mdates.MonthLocator()     # every month
years_fmt = mdates.DateFormatter('%Y')
```

- `years` will be used for **major ticks** – we want a tick at the beginning of each year.
- `months` will be used for **minor ticks** – we want a tick at the beginning of each month (but no labels, just a small tick mark).
- `years_fmt` will format the major tick labels to show only the year.

### 2.2 Applying Locators to the Axis

We need to assign these to the x‑axis of our primary axis (`ax1`). The twin axis `ax2` shares the same x‑axis, so changes to `ax1.xaxis` will automatically affect `ax2`.

```python
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
```

- `set_major_locator()` sets where the big ticks (with labels) appear.
- `set_major_formatter()` defines how those labels are displayed.
- `set_minor_locator()` sets the minor ticks (usually without labels) for a finer grid or visual reference.

---

## 3. Integrating into the Tesla Chart

Here is the complete code with locators and formatters applied:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Assume df_tesla is already loaded and MONTH is datetime

# Create locators and formatter
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Set major and minor ticks on x-axis of ax1
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
```

**Output:**  
The x‑axis now shows major ticks at each year (e.g., 2010, 2011, …) and minor ticks at each month (small unlabeled ticks). The labels are only the year, making the chart cleaner and less cluttered. The rotation is still applied, so the year labels are angled 45 degrees, which works well.

---

## 4. Understanding the Result

With this improved tick formatting, we can more easily pinpoint events:

- The **spike in search interest** around **March 2016** becomes clearly visible between the 2016 and 2017 major ticks. This spike corresponds to the unveiling of the Tesla Model 3.
- The recent surge in both stock price and search interest (2020) is also clearly marked.

Minor ticks help us mentally subdivide the years into months, even though they aren’t labelled. This gives a better sense of the data’s granularity.

**Why not use `plt.xticks()` alone?**  
`plt.xticks()` can manually set tick positions and labels, but for dates it’s cumbersome because you’d have to generate a list of datetime objects and corresponding label strings. Locators are designed to handle dates intelligently, taking into account calendar boundaries.

---

## 5. Additional Customisation

### 5.1 Changing the Date Format
You can use different format codes. For example, to show "Jan 2010", "Feb 2010", etc., use `mdates.DateFormatter('%b %Y')`. However, for yearly ticks, `'%Y'` is usually sufficient.

### 5.2 Adjusting Tick Density
If you want ticks every 2 years, you can pass an argument to `YearLocator`: `YearLocator(2)`.

### 5.3 Removing Minor Ticks
If you don’t want minor ticks, simply omit the `set_minor_locator` line. Or you can disable them with `ax1.xaxis.set_minor_locator(plt.NullLocator())`.

### 5.4 Adding a Grid
You can add a grid to both major and minor ticks:

```python
ax1.grid(True, which='major', linestyle='-', alpha=0.7)
ax1.grid(True, which='minor', linestyle='--', alpha=0.3)
```

This would give a solid line for major years and dashed for months.

---

## 6. Summary

By using `mdates.YearLocator`, `MonthLocator`, and `DateFormatter`, we gained precise control over the x‑axis ticks on our time series chart. This small addition makes the chart more professional and easier to interpret. It also allowed us to visually identify the March 2016 spike as the Tesla Model 3 unveiling.

**Key takeaways:**
- `matplotlib.dates` provides locators for common time intervals (years, months, days, etc.).
- Formatters let you display dates in any string format.
- Major ticks are typically used for labels; minor ticks provide finer visual cues.
- Always register the converters (`register_matplotlib_converters()`) to avoid warnings when using pandas datetime with matplotlib.

