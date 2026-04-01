# Data Visualisation – Tesla Line Charts in Matplotlib

## Introduction
Now that our data is clean and properly formatted (dates as datetime objects, no missing values), we can start creating meaningful visualisations. In this lesson, we will plot Tesla’s stock price against its search popularity using Matplotlib. We'll begin with a basic dual‑axis line chart and then progressively add styling to make it publication‑ready.

By the end of this tutorial, you will know how to:
- Create a figure with two y‑axes using `twinx()`.
- Customise colours using HEX codes and named colours.
- Adjust figure size, resolution (DPI), font sizes, and line thickness.
- Rotate x‑axis labels for better readability.
- Set axis limits to focus on relevant data ranges.
- Handle the common Matplotlib datetime converter warning.

All code examples are taken from the completed notebook and are ready to run after the data cleaning steps from previous lessons.

---

## 1. Basic Dual‑Axis Line Chart

We want to compare two variables that have different scales: Tesla’s stock price (in USD, ranging from ~$4 to $500) and its web search popularity (on a 0–100 scale). Plotting them on the same y‑axis would squash one of the series, so we use two separate y‑axes.

**Code:**
```python
import matplotlib.pyplot as plt

# Create the figure and get the current axis
ax1 = plt.gca()
# Create a twin axis sharing the same x-axis
ax2 = ax1.twinx()

# Label the axes
ax1.set_ylabel('TSLA Stock Price')
ax2.set_ylabel('Search Trend')

# Plot the data
ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH)

# Display the chart
plt.show()
```

**Explanation:**
- `plt.gca()` gets the current axes (or creates one if none exists).
- `ax1.twinx()` creates a second y‑axis that shares the same x‑axis. This allows two different scales on the left and right.
- We then set labels and plot each series on its respective axis.

**Output:**  
A simple line chart with two lines – one for price (blue default) and one for search (orange default). The x‑axis shows dates with default formatting.

---

## 2. Adding Colours

Colours help distinguish the two lines and their corresponding axis labels. Matplotlib accepts:
- **Named colours** (e.g., `'skyblue'`, `'red'`)
- **HEX codes** (e.g., `'#E6232E'` for a vivid red)
- **RGB/RGBA tuples**

**Code:**
```python
ax1 = plt.gca()
ax2 = ax1.twinx()

# Colour the axis labels
ax1.set_ylabel('TSLA Stock Price', color='#E6232E')
ax2.set_ylabel('Search Trend', color='skyblue')

# Colour the lines
ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E')
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue')

plt.show()
```

**Explanation:**
- The `color` parameter in `set_ylabel` changes the label text colour.
- The same `color` parameter in `plot` changes the line colour.
- Using a HEX code for the price line and a named colour for the search line makes them visually distinct.

**Output:**  
Now the price line and its axis label are red (`#E6232E`), while the search line and its label are sky blue.

---

## 3. Enhancing the Chart: Size, Fonts, Title, Line Thickness, and DPI

A small, low‑resolution chart is hard to read. We can improve it by:
- Increasing the **figure size** (`figsize`).
- Raising the **dots per inch** (`dpi`) for sharper output.
- Using larger **font sizes** for titles and labels.
- Making the **lines thicker** (`linewidth`).
- Adding a **title**.

**Code:**
```python
plt.figure(figsize=(14, 8), dpi=120)          # Larger, higher resolution
plt.title('Tesla Web Search vs Price', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
```

**Explanation:**
- `plt.figure(figsize=(14,8), dpi=120)` creates a new figure with width 14 inches, height 8 inches, and 120 dots per inch. This yields a larger, sharper image.
- `plt.title()` adds a title with increased font size.
- `fontsize=14` in `set_ylabel` enlarges the axis labels.
- `linewidth=3` makes the lines thicker, improving visibility.

**Output:**  
A much larger chart with thick lines, clear labels, and a title. The x‑axis tick labels are still horizontal and may overlap if there are many dates.

---

## 4. Rotating X‑Axis Labels and Setting Axis Limits

Overlapping date labels can be fixed by rotating them. Additionally, we can zoom in on the data by setting explicit limits for the y‑ and x‑axes.

**Code:**
```python
plt.figure(figsize=(14, 8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)

# Rotate x-axis labels by 45 degrees and increase font size
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# Set axis limits
ax1.set_ylim([0, 600])                         # Price from 0 to 600
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])  # Full date range

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
```

**Explanation:**
- `plt.xticks(fontsize=14, rotation=45)` sets the tick label size and rotates them 45 degrees, preventing overlap.
- `ax1.set_ylim([0,600])` forces the left y‑axis to start at 0 and end at 600. This ensures the price line is not cut off.
- `ax1.set_xlim()` sets the x‑axis to exactly the range of the data. You could also use fixed dates, e.g., `[pd.Timestamp('2010-01-01'), pd.Timestamp('2020-12-31')]`.

**Output:**  
Now the x‑axis labels are rotated and legible. The chart shows the full time span with price capped at 600 (above the maximum of 498, so all data fits).

---

## 5. Fixing the Matplotlib Datetime Converter Warning

When plotting datetime data, you might see a warning like:
```
UserWarning: Pandas doesn't allow columns to be created via a new attribute name
```
or a suggestion to register converters. This is not an error but a reminder to be explicit. The fix is simple:

```python
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
```

Add these lines at the top of your notebook (after imports) to suppress the warning and ensure proper conversion.

**Full example with all improvements and warning fix:**

```python
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Assume df_tesla is already loaded and MONTH is datetime

plt.figure(figsize=(14, 8), dpi=120)
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

---

## 6. Summary of Key Matplotlib Techniques Used

| Technique | Code | Purpose |
|-----------|------|---------|
| Dual y‑axes | `ax2 = ax1.twinx()` | Overlay two series with different scales. |
| Colour specification | `color='#E6232E'` or `color='skyblue'` | Customise line and label colours. |
| Figure size & DPI | `plt.figure(figsize=(w,h), dpi=n)` | Control chart dimensions and resolution. |
| Title | `plt.title('text', fontsize=size)` | Add a chart title. |
| Tick rotation | `plt.xticks(rotation=45)` | Improve readability of date labels. |
| Axis limits | `ax.set_ylim([min,max])`, `ax.set_xlim([min,max])` | Focus on a specific data range. |
| Line thickness | `linewidth=3` | Make lines more prominent. |
| Suppress converter warning | `register_matplotlib_converters()` | Avoid Pandas/Matplotlib datetime warnings. |

