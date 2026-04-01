# Plotly Bar Charts & Scatter Plots: The Most Competitive & Popular App Categories

## Introduction

After cleaning our data and converting key columns to numeric types, we are ready to tackle one of the core business questions: **Which app categories offer the best opportunities?**

Releasing an app is a strategic decision. You need to balance two opposing forces:

- **Competition:** How many other apps are vying for users' attention in the same category? High competition means it's harder to get discovered.
- **Popularity:** How many total downloads does the category attract? High popularity means a larger potential audience.

Ideally, you want a category that is both popular (lots of downloads) and not overly crowded (downloads are spread across many apps, giving new entrants a chance). But are there such categories? Let's investigate.

In this module, we will:

- Determine the number of unique app categories.
- Identify the most competitive categories (by number of apps).
- Identify the most popular categories (by total downloads).
- Create a **scatter plot** that combines both dimensions to reveal category concentration.

We'll use **Plotly Express** to create interactive bar charts and scatter plots that make these insights immediately visible.

---

## 1. Exploring App Categories

First, let's see how many distinct categories exist in our dataset. The `Category` column contains values like `"GAME"`, `"FAMILY"`, `"TOOLS"`, etc.

```python
# Count unique categories
num_categories = df_apps_clean.Category.nunique()
print(f"There are {num_categories} unique app categories.")
```

**Output:**
```
There are 33 unique app categories.
```

So we have 33 different categories to analyse.

---

## 2. Most Competitive Categories (Number of Apps per Category)

The simplest measure of competitiveness is the sheer number of apps in a category. More apps mean more competition for visibility.

We can count apps per category using `value_counts()` and take the top 10.

```python
# Count apps per category and get top 10
top10_category = df_apps_clean.Category.value_counts()[:10]
print(top10_category)
```

**Output:**
```
FAMILY             1606
GAME                910
TOOLS               719
PRODUCTIVITY        301
PERSONALIZATION     298
LIFESTYLE           297
FINANCE             296
MEDICAL             292
PHOTOGRAPHY         263
BUSINESS            262
Name: Category, dtype: int64
```

**Observations:**

- **FAMILY** dominates with 1,606 apps – almost twice as many as the second place.
- **GAME** follows with 910 apps.
- The rest of the categories have between 250 and 300 apps.

### 2.1 Visualising Competition with a Vertical Bar Chart

Let's create a basic bar chart using Plotly Express.

```python
import plotly.express as px

fig = px.bar(
    x=top10_category.index,   # category names on x-axis
    y=top10_category.values,   # app counts on y-axis
    title="Top 10 Most Competitive Categories"
)

fig.show()
```

**What the chart shows:**  
A vertical bar chart where the height of each bar represents the number of apps. The chart is interactive – you can hover over bars to see exact numbers, zoom, and pan.

**Interpretation:**  
The FAMILY and GAME categories are extremely crowded. Launching a new app there means fighting for attention among hundreds (or thousands) of competitors. The other categories, while still competitive, have roughly one‑sixth the number of apps.

---

## 3. Most Popular Categories (Total Downloads)

Competition is only one side of the coin. A category might have many apps, but if it also has a huge user base, there might still be room for a well‑made app. To measure popularity, we sum the number of installs for all apps in each category.

### 3.1 Grouping and Summing Installs

We group by `Category` and aggregate the `Installs` column using `sum`. Because `Installs` is now numeric, this works perfectly.

```python
# Sum installs per category
category_installs = df_apps_clean.groupby('Category').agg({'Installs': 'sum'})
category_installs.sort_values('Installs', ascending=True, inplace=True)
category_installs
```

**Output (showing top and bottom):**

| Category            | Installs     |
|---------------------|-------------:|
| EVENTS              |    15,949,410|
| BEAUTY              |    26,916,200|
| PARENTING           |    31,116,110|
| MEDICAL             |    39,162,676|
| ...                 | ...         |
| TOOLS               | 8,099,724,500|
| COMMUNICATION       |11,039,241,530|
| GAME                |13,858,762,717|

We sorted ascending so that the categories with the fewest downloads appear first; this is useful for a horizontal bar chart where we want the largest at the top.

### 3.2 Visualising Popularity with a Horizontal Bar Chart

A horizontal bar chart is often easier to read when category names are long.

```python
h_bar = px.bar(
    x=category_installs.Installs,
    y=category_installs.index,
    orientation='h',
    title='Category Popularity (Total Downloads)'
)

h_bar.update_layout(
    xaxis_title='Number of Downloads',
    yaxis_title='Category'
)

h_bar.show()
```

**What the chart shows:**  
A horizontal bar chart where the length of each bar represents total downloads. Categories with the most downloads are at the top.

**Interpretation:**

- **GAME** has the highest total downloads by far (over 13.8 billion).
- **COMMUNICATION** and **TOOLS** are next, each around 8–11 billion.
- Categories like **EVENTS**, **BEAUTY**, and **PARENTING** have the fewest downloads (tens of millions).

Now we have two perspectives: competition (number of apps) and popularity (total downloads). But we need to combine them to understand **concentration** – are the downloads spread across many apps or dominated by a few?

---

## 4. Combining Competition and Popularity: Category Concentration Scatter Plot

The scatter plot will allow us to visualise both dimensions at once. Each point represents a category. The x‑axis will be the number of apps (competition), and the y‑axis will be total downloads (popularity). The size of the point can also represent the number of apps (or we can use colour to indicate popularity). We'll follow the challenge specification.

### 4.1 Create a DataFrame with Both Metrics

We already have `top10_category` (which is just a Series, not a full DataFrame) and `category_installs` (DataFrame with one column). We need a combined DataFrame with two columns: `App` (number of apps) and `Installs` (total downloads) per category.

```python
# Number of apps per category (as a DataFrame)
cat_number = df_apps_clean.groupby('Category').agg({'App': 'count'})

# Merge with the installs DataFrame
cat_merged_df = pd.merge(cat_number, category_installs, on='Category', how='inner')
print(f'Merged DataFrame shape: {cat_merged_df.shape}')
cat_merged_df.sort_values('Installs', ascending=False).head()
```

**Output:**

| Category            | App  | Installs     |
|---------------------|-----:|-------------:|
| GAME                |  910 |13,858,762,717|
| COMMUNICATION       |  257 |11,039,241,530|
| TOOLS               |  719 | 8,099,724,500|
| PRODUCTIVITY        |  301 | 5,788,070,180|
| SOCIAL              |  203 | 5,487,841,475|

The merged DataFrame has 33 rows (one per category) and two columns: `App` (number of apps) and `Installs` (total downloads). This is exactly what we need for the scatter plot.

### 4.2 Building the Scatter Plot with Plotly Express

We'll use `px.scatter()` and customise it with the following parameters:

- `x='App'` – number of apps (x‑axis).
- `y='Installs'` – total downloads (y‑axis).
- `size='App'` – makes the size of the marker proportional to the number of apps. (Alternatively, we could use `Installs` for size, but the challenge suggested `size='App'`.)
- `hover_name=cat_merged_df.index` – when hovering, show the category name prominently.
- `color='Installs'` – colour the markers by total downloads (using a continuous colour scale).
- `title` – descriptive title.

We'll also set the y‑axis to a logarithmic scale because the install numbers span many orders of magnitude (from millions to billions). This prevents points from being squashed.

```python
scatter = px.scatter(
    cat_merged_df,
    x='App',
    y='Installs',
    title='Category Concentration',
    size='App',
    hover_name=cat_merged_df.index,
    color='Installs'
)

scatter.update_layout(
    xaxis_title="Number of Apps (Lower=More Concentrated)",
    yaxis_title="Total Downloads",
    yaxis=dict(type='log')   # log scale for y-axis
)

scatter.show()
```

**Explanation of parameters:**

- **`size='App'`** – the marker's area is proportional to the number of apps in the category. Categories with many apps appear as larger circles.
- **`hover_name`** – uses the index (category names) as the bold title in the hover tooltip.
- **`color='Installs'`** – a continuous colour scale (default is Viridis) that shades markers according to total downloads. This adds another dimension of information.
- **`yaxis=dict(type='log')`** – because the y‑axis values range from 15 million to 13.8 billion, a log scale spreads out the points so we can see differences in the lower ranges.

### 4.3 Interpreting the Scatter Plot

When you run the code, you'll see an interactive plot similar to this (description of what you would see):

- The **x‑axis** shows the number of apps, from about 40 (e.g., `EVENTS`, `BEAUTY`) up to 1600 (`FAMILY`).
- The **y‑axis** (log scale) shows total downloads, from ~1.5×10⁷ (15 million) to ~1.4×10¹⁰ (14 billion).
- **Marker size** is largest for categories with many apps: `FAMILY` (biggest circle), `GAME`, `TOOLS`.
- **Colour** indicates total downloads: dark purple for low downloads, bright yellow for high downloads. `GAME` and `COMMUNICATION` are bright yellow.

**Key observations:**

- **Top‑right corner:** `FAMILY` has the most apps (1606) and relatively high downloads (4.4 billion). This is a **high‑competition, high‑popularity** category. Downloads are spread across many apps, so it's not extremely concentrated.
- **Top‑middle:** `GAME` has 910 apps and the highest downloads (13.8 billion). The marker is large and bright yellow. This is also a high‑competition, high‑popularity category, but with even more downloads per app on average.
- **Left side (few apps):** Categories like `EVENTS`, `BEAUTY`, `PARENTING` have very few apps and low downloads. They are **niche markets**.
- **Some categories have few apps but very high downloads:** Look at `VIDEO_PLAYERS` (148 apps, 3.9 billion downloads) or `ENTERTAINMENT` (102 apps, 2.1 billion downloads). These are **highly concentrated** – a small number of apps capture most of the downloads. If you could break into one of these categories with a superior app, you might capture a significant share.

The scatter plot answers our original question: **the most attractive categories are those with high popularity but relatively low concentration** – i.e., where downloads are spread across many apps. From the plot, `FAMILY` and `GAME` are popular but also crowded, so you'd need a standout app. Categories like `VIDEO_PLAYERS` are popular but dominated by a few giants – very hard to enter. Categories with both low apps and low downloads are too small to bother.

---

## 5. Summary of Insights

| Category           | Apps | Total Downloads | Concentration | Business Implication |
|--------------------|-----:|----------------:|---------------|----------------------|
| GAME               |  910 | 13.9 B          | Moderate      | Huge market, very competitive. Success requires exceptional quality or a novel twist. |
| COMMUNICATION      |  257 | 11.0 B          | Moderate      | Dominated by WhatsApp, Messenger, etc. Hard to compete. |
| TOOLS              |  719 |  8.1 B          | Moderate      | Many apps, high downloads – opportunity for utility apps. |
| FAMILY             | 1606 |  4.4 B          | Spread out    | Many apps, many downloads – good chance for new apps targeting specific age groups. |
| VIDEO_PLAYERS      |  148 |  3.9 B          | Concentrated  | Few apps get most downloads – entry barrier high. |
| ENTERTAINMENT      |  102 |  2.1 B          | Concentrated  | Similar to video players. |
| EVENTS, BEAUTY, etc.|  <50 |  <100 M        | Niche         | Very small markets; only suitable for very targeted apps. |

**Conclusion:** If you were to release an app today, a **FAMILY** app (e.g., educational, kids games) might offer the best balance: high downloads spread across many apps, so you're not competing directly with a single giant. The **GAME** category is also attractive but requires a truly exceptional product to stand out.

---

## 6. Key Takeaways from This Module

- **`nunique()`** quickly tells you how many distinct categories exist.
- **`value_counts()`** gives you a ranked list of category frequencies (competition).
- **Grouping and aggregating** with `groupby().sum()` reveals total downloads per category (popularity).
- **Bar charts** (vertical and horizontal) are excellent for comparing categorical data.
- **Scatter plots** allow you to combine two dimensions and add extra information via marker size and colour.
- **Logarithmic scales** are essential when data spans several orders of magnitude.
- Plotly Express makes it easy to create interactive, informative charts with minimal code.

