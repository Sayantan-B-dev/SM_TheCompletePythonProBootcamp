# Seaborn Data Visualisation: Bubble Charts

This document provides a comprehensive guide to creating advanced scatter plots and bubble charts using the Seaborn library, built on top of Matplotlib. Seaborn simplifies the creation of attractive and informative statistical graphics with minimal code. The analysis uses the cleaned movie dataset (`data_clean`) to visualise the relationship between film budgets, release dates, and worldwide gross revenue.

Key topics covered:

- Importing Seaborn and setting up the plotting environment.
- Creating a basic scatter plot of budget vs. worldwide gross.
- Customising plot appearance (figure size, axis limits, labels) via Matplotlib.
- Transforming a scatter plot into a bubble chart by encoding a third variable through point colour and size.
- Applying Seaborn’s built‑in themes for professional styling.
- Constructing a bubble chart that visualises three dimensions: release date, budget, and worldwide gross.
- Interpreting the resulting chart to understand trends in film budgets over time.

All code examples are drawn from the completed Jupyter Notebook and are presented in a clear, executable format.

---

## 1. Importing Seaborn and Setting Up

Seaborn is typically imported with the alias `sns`. It works seamlessly with pandas DataFrames and integrates with Matplotlib, allowing fine‑tuned control when needed.

```python
import seaborn as sns
import matplotlib.pyplot as plt
```

Additionally, we set some pandas display options and register Matplotlib converters to handle datetime objects correctly:

```python
pd.options.display.float_format = '{:,.2f}'.format

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
```

These settings ensure that numbers are displayed with commas for thousands and that dates are properly formatted on plots.

---

## 2. Basic Scatter Plot with Seaborn

A scatter plot is the simplest way to visualise the relationship between two continuous variables. Using `sns.scatterplot()`, we supply the DataFrame and the column names for the x‑ and y‑axes.

```python
plt.figure(figsize=(8,4), dpi=200)

ax = sns.scatterplot(data=data_clean,
                     x='USD_Production_Budget', 
                     y='USD_Worldwide_Gross')

ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')

plt.show()
```

**Explanation of the code:**

- `plt.figure(figsize=(8,4), dpi=200)` creates a figure with a width of 8 inches, height of 4 inches, and a resolution of 200 dots per inch. This makes the chart larger and sharper than the default.
- `sns.scatterplot()` draws the points. By default, Seaborn uses the column names as axis labels, but we override them later.
- `ax.set(...)` is a Matplotlib method that allows us to set limits and labels. The limits are chosen to focus on the main cluster of data (excluding extreme outliers).
- `plt.show()` displays the plot.

**Result:** A scatter plot showing a positive correlation between production budget and worldwide gross, though many points are scattered.

---

## 3. Adding a Third Dimension: Bubble Charts

A bubble chart extends a scatter plot by encoding a third variable in the size and/or colour of the points. In Seaborn, this is achieved with the `hue` and `size` parameters.

```python
plt.figure(figsize=(8,4), dpi=200)

ax = sns.scatterplot(data=data_clean,
                     x='USD_Production_Budget', 
                     y='USD_Worldwide_Gross',
                     hue='USD_Worldwide_Gross',   # colour by revenue
                     size='USD_Worldwide_Gross')  # size by revenue

ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')

plt.show()
```

**What happens:**

- `hue` assigns different colours to points based on the value in the `USD_Worldwide_Gross` column. By default, Seaborn uses a continuous colour map, with darker colours typically representing higher values.
- `size` scales the diameter of each marker according to the same column. Larger bubbles correspond to films with higher worldwide gross.

Now the chart conveys three dimensions: budget (x‑axis), revenue (y‑axis), and additional emphasis on revenue through colour and size. Films with the highest revenue appear as large, dark dots, making them stand out.

---

## 4. Styling with Seaborn Themes

Seaborn provides several pre‑defined themes that can be applied to a single plot using a context manager. This allows for quick, professional styling without manually tweaking every element.

```python
plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=data_clean,
                         x='USD_Production_Budget', 
                         y='USD_Worldwide_Gross',
                         hue='USD_Worldwide_Gross',
                         size='USD_Worldwide_Gross')

    ax.set(ylim=(0, 3000000000),
           xlim=(0, 450000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')
```

**Available themes:** `'darkgrid'`, `'whitegrid'`, `'dark'`, `'white'`, `'ticks'`. The `with` statement temporarily applies the chosen style only to the indented block, leaving other plots unaffected.

---

## 5. Bubble Chart: Movie Budgets Over Time

A more insightful visualisation is to examine how film budgets have evolved over the years, while also showing the worldwide gross. This requires placing `Release_Date` on the x‑axis and `USD_Production_Budget` on the y‑axis, with colour and size again representing worldwide gross.

```python
plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style("darkgrid"):
    ax = sns.scatterplot(data=data_clean, 
                         x='Release_Date', 
                         y='USD_Production_Budget',
                         hue='USD_Worldwide_Gross',
                         size='USD_Worldwide_Gross')

    ax.set(ylim=(0, 450000000),
           xlim=(data_clean.Release_Date.min(), data_clean.Release_Date.max()),
           xlabel='Year',
           ylabel='Budget in $100 millions')
```

**Key points:**

- `xlim` is set to the minimum and maximum release dates in the dataset, ensuring the entire time range is displayed.
- The y‑axis limits are set to 0–450 million to match the range of budgets.
- The colour and size of the bubbles reflect worldwide gross, so the most successful films are both darker and larger.

---

## 6. Interpreting the Bubble Chart

The resulting chart reveals several important trends:

- **Early decades (pre‑1970):** Very few films are present, and budgets are relatively low (mostly under $50 million). The industry was smaller and production costs were modest.
- **Post‑1970 explosion:** From the 1970s onward, the number of films increases dramatically, and budgets begin to climb. By the 1980s and 1990s, budgets in the $100–200 million range appear.
- **2000s and beyond:** The density of points becomes extremely high, with many films having budgets exceeding $200 million. The largest bubbles (highest grossing films) are concentrated in this period and often correspond to the biggest budgets.
- **Correlation with revenue:** High‑budget films tend to have larger bubbles, confirming that spending more money is associated with higher revenue, especially in the modern era.

This visual evidence supports the hypothesis that higher budgets generally lead to greater worldwide gross, particularly for films released after 1970. It also sets the stage for a more formal linear regression analysis.

---

## 7. Summary

In this section, we have:

- Learned how to create scatter plots with Seaborn and customise them using Matplotlib.
- Transformed a basic scatter plot into a bubble chart by encoding a third variable with `hue` and `size`.
- Applied Seaborn’s built‑in themes for quick styling.
- Constructed a bubble chart of release date vs. budget, coloured and sized by worldwide gross.
- Interpreted the chart to understand the historical evolution of film budgets and the relationship with revenue.

These visualisation techniques are powerful tools for exploratory data analysis and for communicating insights to others. The bubble chart, in particular, allows us to visualise three dimensions simultaneously, revealing patterns that might otherwise remain hidden.
