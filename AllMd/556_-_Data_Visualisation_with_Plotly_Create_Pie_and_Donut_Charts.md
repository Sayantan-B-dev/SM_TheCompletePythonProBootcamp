# Data Visualisation with Plotly: Create Pie and Donut Charts

## Introduction

After cleaning our data and performing preliminary exploration, we are ready to create our first visualisations. Visualising categorical data helps us understand the distribution of apps across different groups at a glance. One of the most common categorical variables in our dataset is `Content_Rating`, which indicates the intended audience for each app (e.g., Everyone, Teen, Mature 17+).

In this module, we will learn how to use **Plotly Express**, a high‑level interface for Plotly, to create both pie charts and donut charts. These charts are ideal for showing proportions and will give us immediate insight into the composition of the Google Play Store by content rating.

We will cover:

- Counting categories with `value_counts()`
- Importing Plotly Express
- Creating a basic pie chart
- Customising the chart (title, labels, text position, information displayed)
- Transforming a pie chart into a donut chart using the `hole` parameter
- Understanding the interactive features of Plotly charts

By the end, you'll be able to produce publication‑ready, interactive pie and donut charts with just a few lines of code.

---

## 1. Preparing the Data: Counting Content Ratings

Before we can visualise, we need to know how many apps belong to each content rating category. The `Content_Rating` column contains values such as "Everyone", "Teen", "Mature 17+", etc. We can get the counts using the Pandas `.value_counts()` method.

```python
# Count the number of apps for each content rating
ratings = df_apps_clean.Content_Rating.value_counts()
print(ratings)
```

**Output:**
```
Everyone           6621
Teen                912
Mature 17+          357
Everyone 10+        305
Adults only 18+       3
Unrated               1
Name: Content_Rating, dtype: int64
```

### Interpretation of the Counts

- **Everyone (6,621 apps):** The vast majority of apps are rated "Everyone". This makes sense because developers want to reach the widest possible audience.
- **Teen (912 apps):** A significant number target teenagers, often containing more mature themes or mild violence.
- **Mature 17+ (357 apps):** Apps with adult content, violence, or strong language fall here.
- **Everyone 10+ (305 apps):** A middle ground for slightly older children.
- **Adults only 18+ (3 apps):** Very rare; likely contains explicit content.
- **Unrated (1 app):** Possibly an error or an app that hasn't been rated.

These numbers are our raw data for the charts.

---

## 2. Importing Plotly Express

Plotly Express (usually imported as `px`) is the quickest way to create rich interactive charts. If you haven't already installed Plotly, you can do so with `!pip install plotly` in a notebook cell. In Google Colab, Plotly is pre‑installed.

```python
import plotly.express as px
```

Plotly Express functions return a `plotly.graph_objects.Figure` object, which we can then customise and display with `.show()`.

---

## 3. Creating a Basic Pie Chart

The simplest way to create a pie chart is to pass the category labels and their corresponding values to `px.pie()`. We'll use the index of the `ratings` Series (the content rating names) as the labels, and the values (the counts) as the pie slices.

```python
fig = px.pie(labels=ratings.index, values=ratings.values)
fig.show()
```

**What you see:** An interactive pie chart where you can hover over each slice to see the exact count. The chart uses default colours and places the category names inside the slices.

**Limitations of this basic version:**
- No title
- Category names are inside the slices, which can become cluttered
- Percentages are not shown by default

---

## 4. Customising the Pie Chart

To make the chart more informative, we can add a title, specify the `names` parameter (which is an alias for `labels`), and then use `.update_traces()` to control how the text is displayed.

```python
fig = px.pie(
    labels=ratings.index,
    values=ratings.values,
    title="Content Rating Distribution",
    names=ratings.index
)

fig.update_traces(
    textposition='outside',      # place labels outside the pie
    textinfo='percent+label'     # show both percentage and category name
)

fig.show()
```

**Explanation of parameters and methods:**

- **`title`:** Adds a title above the chart.
- **`names`:** Explicitly sets the names for each slice (same as `labels` here).
- **`.update_traces()`:** Modifies the graphical marks (the "traces"). In a pie chart, the trace is the collection of slices.
  - `textposition='outside'`: Places the category labels and percentages outside the pie, connected by lines, which improves readability when there are many small slices.
  - `textinfo='percent+label'`: Specifies that both the percentage and the category name should be displayed.

**Resulting chart:** A clear pie chart with labels outside, percentages shown, and a title. Hovering over a slice still reveals the exact count.

---

## 5. Creating a Donut Chart

A donut chart is essentially a pie chart with a hole in the middle. It can be aesthetically pleasing and can sometimes make proportions easier to compare because the eye focuses on the arcs rather than the angles. To create a donut, we simply add the `hole` parameter to `px.pie()`. The value should be between 0 and 1, where 0 is a full pie and values closer to 1 create a larger hole.

```python
fig = px.pie(
    labels=ratings.index,
    values=ratings.values,
    title="Content Rating Distribution",
    names=ratings.index,
    hole=0.6                     # creates a donut with a 60% hole
)

fig.update_traces(
    textposition='inside',       # place text inside the slices
    textfont_size=15,            # increase font size for readability
    textinfo='percent'           # show only the percentage inside
)

fig.show()
```

**What changed:**

- **`hole=0.6`:** Transforms the pie into a donut. The hole occupies 60% of the radius.
- **`textposition='inside'`:** Now that the labels are outside the slices in the previous example, we move them inside for a cleaner look on the donut.
- **`textfont_size=15`:** Makes the percentage numbers larger and easier to read.
- **`textinfo='percent'`:** We display only the percentage inside the slices; the category names are not shown, but they appear in the legend (by default, Plotly adds a legend). You could also keep `'percent+label'` inside, but with many categories it might become crowded.

**Resulting chart:** A modern donut chart where each "ring segment" represents a content rating. Hovering still gives full details (category + count). The legend on the side identifies which colour corresponds to which rating.

---

## 6. Understanding Plotly's Interactivity

One of the biggest advantages of Plotly over static libraries (like Matplotlib) is its built‑in interactivity. With the charts we've created, you can:

- **Hover** over any slice to see a tooltip with the category name, value (count), and percentage.
- **Click** on legend items to toggle the visibility of that category.
- **Zoom** and **pan** (though not very useful for pie charts, it's available).
- **Download** the chart as a PNG image using the camera icon in the toolbar.

These features make Plotly charts ideal for exploratory data analysis and for sharing insights with non‑technical audiences.

---

## 7. Why Visualise Content Ratings?

Visualising the distribution of content ratings is not just an exercise; it provides real business intelligence:

- **Market Opportunity:** Knowing that "Everyone" dominates suggests that if you're building an app, targeting that rating gives you the largest potential audience.
- **Niche Segments:** The small numbers for "Mature 17+" and "Adults only 18+" indicate these are niche markets. However, they may be less competitive, and users in those segments might be willing to pay more.
- **Compliance:** It reminds developers to be aware of rating guidelines and the implications for app visibility.

---

## 8. Summary of Key Concepts

| Concept                  | Description                                                                                   | Code Example                                  |
|--------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------|
| `value_counts()`         | Counts unique values in a Series.                                                             | `df_apps_clean.Content_Rating.value_counts()` |
| `px.pie()`               | Creates a pie or donut chart.                                                                 | `px.pie(labels=..., values=..., hole=0.6)`    |
| `fig.update_traces()`    | Modifies the appearance of the chart elements.                                                | `fig.update_traces(textposition='outside')`   |
| `textposition`           | Where the text appears relative to slices (`'inside'`, `'outside'`, `'auto'`).                | `textposition='inside'`                        |
| `textinfo`               | What information is shown (`'percent'`, `'label'`, `'percent+label'`, `'none'`).              | `textinfo='percent+label'`                     |
| `hole`                   | Creates a donut chart when set between 0 and 1.                                                | `hole=0.6`                                     |

---

## 9. Further Customisation Ideas

Plotly offers many ways to customise your charts. Here are a few you could explore:

- **Colours:** Use the `color_discrete_sequence` parameter to specify a custom colour palette.
- **Legend:** Change the legend position with `fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))`.
- **Pull out a slice:** Use the `pull` parameter in `px.pie()` to explode a slice for emphasis.
- **Add annotations:** Use `fig.add_annotation()` to add text in the center of the donut (e.g., total apps).

---

## 10. Complete Code Example

Here is the entire code block you would run to generate the donut chart from scratch, assuming `df_apps_clean` is already loaded and cleaned.

```python
import pandas as pd
import plotly.express as px

# Assuming df_apps_clean is already defined
ratings = df_apps_clean.Content_Rating.value_counts()

fig = px.pie(
    labels=ratings.index,
    values=ratings.values,
    title="Content Rating Distribution",
    names=ratings.index,
    hole=0.6
)

fig.update_traces(
    textposition='inside',
    textfont_size=15,
    textinfo='percent'
)

fig.show()
```

**Expected output:** An interactive donut chart similar to the one shown in the original lesson.

---

## Conclusion

In this module, we've taken our first steps into data visualisation with Plotly. We've learned how to create both pie and donut charts, customise them to our liking, and interpret the results. These skills form the foundation for more complex charts like bar charts, scatter plots, and box plots, which we will tackle next.

**Key Takeaway:** Pie and donut charts are excellent for showing the composition of a categorical variable. With Plotly, they become interactive and can be easily shared or embedded.
