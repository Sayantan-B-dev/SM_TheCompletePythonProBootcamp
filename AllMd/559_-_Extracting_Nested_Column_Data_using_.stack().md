# Extracting Nested Column Data using .stack()

## Introduction

In our Google Play Store dataset, the `Genres` column provides a more granular classification than `Category`. While `Category` places an app into a broad group (e.g., "GAME", "FAMILY"), `Genres` describes the app's specific style or function (e.g., "Action", "Arcade", "Education"). However, an app can belong to **multiple genres** at once. In the raw data, these multiple genres are concatenated into a single string separated by a semicolon (`;`). For example, an app might have `Genres = "Arcade;Action & Adventure"`.

This nested structure poses a challenge for analysis: if we simply count unique values or use `.value_counts()`, we will treat the combined string as one entity, which undercounts genres and hides the true distribution. To accurately analyse genres, we must **split** the combined strings and **stack** them into a single column.

In this module, we will:

- Understand the problem of nested data.
- Use `.str.split()` to separate the genre names.
- Use `.stack()` to convert the resulting DataFrame of split strings into a single Series.
- Count the true number of distinct genres and their frequencies.
- Visualise the top genres with a stylish bar chart using Plotly, including a custom colour scale and hidden colour axis.

---

## 1. The Problem: Nested Data in the Genres Column

Let's first examine the `Genres` column.

```python
# Check the number of unique values as reported by Pandas
print("Unique genres (raw):", df_apps_clean.Genres.nunique())
```

**Output:**
```
Unique genres (raw): 114
```

At first glance, there appear to be 114 different genres. But is that accurate? Let's look at a few values that appear only once (the least frequent). Sorting `.value_counts()` in ascending order reveals the entries with the smallest counts.

```python
df_apps_clean.Genres.value_counts().sort_values(ascending=True).head(10)
```

**Output:**
```
Music & Audio;Music & Video    1
Racing;Pretend Play            1
Communication;Creativity       1
Parenting;Brain Games          1
Adventure;Brain Games          1
...
Name: Genres, dtype: int64
```

Notice the semicolons! Many entries contain multiple genres separated by `;`. For example, "Music & Audio;Music & Video" actually represents two distinct genres: "Music & Audio" and "Music & Video". The `.nunique()` method counts this combined string as a single unique value, which is misleading. We need to split each such string into its component parts and then count the parts.

---

## 2. Splitting and Stacking to Extract Nested Data

Pandas provides powerful string methods via `.str`. We can use `.str.split(';', expand=True)` to split each entry on the semicolon and place the resulting parts into separate columns. Then we use `.stack()` to pivot those columns into a single long Series.

### Step 1: Split the strings

```python
# Split on ';' and expand into a DataFrame
split_genres = df_apps_clean.Genres.str.split(';', expand=True)
print(split_genres.shape)
split_genres.head()
```

**Output shape:** (8199, 2) – because most apps have at most two genres, but some may have more. The `expand=True` argument creates a DataFrame with as many columns as the maximum number of parts in any row. If an app has only one genre, the second column will be `None`.

|     | 0                 | 1                    |
|----:|:------------------|:---------------------|
| 21  | Medical           | None                 |
| 1230| Medical           | None                 |
| 1227| Lifestyle         | None                 |
| 1224| Sports            | None                 |
| 1223| Photography       | None                 |

As we can see, most apps have a single genre. But some have two (or possibly more).

### Step 2: Stack the columns into a single Series

`.stack()` takes a DataFrame and "melts" the columns into rows, effectively creating a long Series with a multi‑index (original row index and column index). We then drop the extra index level and keep only the values.

```python
stacked = split_genres.stack()
print("Shape after stacking:", stacked.shape)
stacked.head(10)
```

**Output:**
```
Shape after stacking: (8564,)
```

We now have 8,564 rows – more than the original 8,199 apps because apps with two genres contribute two rows.

The first few values look like:
```
21   0    Medical
1230 0    Medical
1227 0    Lifestyle
1224 0    Sports
1223 0    Photography
...
```

### Step 3: Count the true genre frequencies

Now that we have a clean Series where each entry is a single genre, we can use `.value_counts()` to get the true distribution.

```python
true_genre_counts = stacked.value_counts()
print("Number of distinct genres (after splitting):", len(true_genre_counts))
true_genre_counts.head(15)
```

**Output:**
```
Number of distinct genres (after splitting): 53
```

Top 15 genres:

| Genre                | Count |
|----------------------|------:|
| Tools                | 719   |
| Education            | 587   |
| Entertainment        | 498   |
| Action               | 304   |
| Productivity         | 301   |
| Personalization      | 298   |
| Lifestyle            | 298   |
| Finance              | 296   |
| Medical              | 292   |
| Sports               | 270   |
| Photography          | 263   |
| Business             | 262   |
| Communication        | 258   |
| Health & Fitness     | 245   |
| Casual               | 216   |

**Observations:**

- The true number of distinct genres is **53**, not 114. The initial count of 114 was inflated because each combination of two genres was treated as a unique category.
- The most common genres are **Tools**, **Education**, and **Entertainment**, each appearing in hundreds of apps.
- This distribution is more meaningful for understanding the market: it shows which genres are most popular among developers.

---

## 3. Visualising the Top Genres with a Colour‑Scaled Bar Chart

Now that we have the true genre frequencies, we can visualise the top 15 genres using a bar chart. We'll use Plotly Express to create an attractive, interactive chart. Additionally, we'll experiment with a custom colour scale and hide the colour bar to keep the plot clean.

### Challenge 2 Requirements

- Create a bar chart showing the top 15 genres.
- Use the `color_continuous_scale` parameter to apply a built‑in colour scale (e.g., `'Agsunset'`).
- Hide the colour axis using `coloraxis_showscale=False`.
- Add a title and axis labels.

### Solution

```python
import plotly.express as px

# Prepare data: top 15 genres
top_genres = true_genre_counts.head(15)

fig = px.bar(
    x=top_genres.index,          # genre names
    y=top_genres.values,          # counts
    title='Top 15 Genres',
    hover_name=top_genres.index,  # shows genre name on hover
    color=top_genres.values,       # colour bars by count
    color_continuous_scale='Agsunset'  # a beautiful purple‑orange colour scale
)

fig.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Apps',
    coloraxis_showscale=False      # removes the colour bar legend
)

fig.show()
```

**Explanation of parameters:**

- **`x` and `y`**: set the category names and their frequencies.
- **`hover_name`**: makes the genre name appear in bold in the hover tooltip.
- **`color`**: assigns a numeric value to each bar; the bar's colour will be chosen from the colour scale based on this value. Here, we use the count itself, so taller bars get a different colour than shorter ones.
- **`color_continuous_scale`**: selects a built‑in colour scale. `'Agsunset'` is a vibrant purple‑to‑orange gradient. You can choose any from the [Plotly colour scales documentation](https://plotly.com/python/builtin-colorscales/).
- **`coloraxis_showscale=False`**: by default, Plotly would add a colour bar to show the mapping from count to colour. For a bar chart, this is often redundant, so we hide it.

**Resulting chart (description):**  
A bar chart with 15 bars, each representing a genre. The bars are coloured from deep purple (lowest count among the top 15, which is still high) to bright yellow‑orange (highest count). Hovering over a bar shows the genre name and the exact number of apps. The chart is interactive – you can zoom, pan, and download as an image.

### Why Use a Colour Scale?

- It adds an extra dimension of information without cluttering the chart.
- It guides the eye to the most frequent genres (the brightest bars).
- It makes the chart more visually appealing.

---

## 4. Business Insights from the Genres Analysis

- **Tools** and **Education** are the most frequently used genres. This suggests a high supply of apps in these areas – competition is fierce.
- **Entertainment** and **Action** also have many apps, indicating strong developer interest.
- Genres like **Casual**, **Medical**, and **Finance** have moderate counts; they might represent niches with less competition.
- The fact that we uncovered 53 distinct genres (instead of 114) shows that many apps are hybrids, belonging to two genres. This could be a strategy to appear in multiple search categories.

For a new developer, choosing a genre with high demand but not overwhelming competition (e.g., **Medical**, **Finance**, **Weather**) might be a smarter move than entering the crowded **Tools** or **Education** space.

---

## 5. Summary of Techniques

| Method | Purpose |
|--------|---------|
| `.str.split(';', expand=True)` | Splits a string column on a delimiter and expands into multiple columns. |
| `.stack()` | Converts a DataFrame with multiple columns into a long Series, stacking columns into rows. |
| `.value_counts()` | Counts frequencies of unique values in a Series. |
| `px.bar(..., color=..., color_continuous_scale=...)` | Creates a bar chart with bars coloured according to a numeric variable using a continuous colour scale. |
| `coloraxis_showscale=False` | Suppresses the display of the colour bar legend. |

By mastering these tools, you can handle nested data in any column and create rich, informative visualisations.

---

## 6. Final Code Block

Here's the complete code to reproduce the analysis and chart:

```python
# Split and stack genres
split_genres = df_apps_clean.Genres.str.split(';', expand=True)
stacked_genres = split_genres.stack()
true_genre_counts = stacked_genres.value_counts()

print(f"Number of true genres: {len(true_genre_counts)}")
print("Top 15 genres:")
print(true_genre_counts.head(15))

# Plot top 15
top15 = true_genre_counts.head(15)
fig = px.bar(
    x=top15.index,
    y=top15.values,
    title='Top 15 Genres',
    hover_name=top15.index,
    color=top15.values,
    color_continuous_scale='Agsunset'
)
fig.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Apps',
    coloraxis_showscale=False
)
fig.show()
```
