# Learning Points & Summary

## Introduction

Congratulations! You have completed a comprehensive analysis of the Google Play Store app market. Over the course of this day, you transformed raw, messy data into actionable business insights using Python, Pandas, and Plotly. You've learned how to clean data, convert data types, extract nested information, and create a variety of beautiful, interactive visualisations.

This final summary recaps all the key techniques and concepts you've mastered. Use it as a reference for future projects or to reinforce your learning.

---

## 1. Data Cleaning Essentials

### 1.1 Sampling Data
- **`.sample(n)`** – returns a random sample of `n` rows from a DataFrame. Useful for quick, unbiased inspection.
  ```python
  df_apps.sample(5)
  ```

### 1.2 Handling Missing Values
- **`.isna()`** – creates a boolean mask for missing values.
- **`.dropna()`** – removes rows with any missing values.
  ```python
  df_apps_clean = df_apps.dropna()
  ```

### 1.3 Detecting and Removing Duplicates
- **`.duplicated()`** – identifies duplicate rows.
- **`.drop_duplicates(subset=[...])`** – removes duplicates based on specified columns.
  ```python
  df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'], inplace=True)
  ```

### 1.4 Dropping Unnecessary Columns
- **`.drop(columns=['col1', 'col2'], inplace=True)`** or `axis=1`.
  ```python
  df_apps.drop(['Last_Updated', 'Android_Ver'], axis=1, inplace=True)
  ```

---

## 2. Data Type Conversion

### 2.1 Inspecting Data Types
- **`.info()`** – shows data types and non‑null counts.
- **`.describe(include='object')`** – describes object (string) columns.

### 2.2 Converting Strings to Numbers
- **`.str.replace(old, new)`** – removes unwanted characters (commas, dollar signs).
- **`pd.to_numeric()`** – converts a Series to numeric type.
  ```python
  df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', '')
  df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)

  df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', '')
  df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
  ```

### 2.3 Creating New Calculated Columns
- Simple arithmetic on Series:
  ```python
  df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs * df_apps_clean.Price
  ```

---

## 3. Handling Nested Data with `.stack()`

When a column contains multiple values separated by a delimiter (e.g., "Arcade;Action & Adventure"):

1. **`.str.split(';', expand=True)`** – splits into separate columns.
2. **`.stack()`** – stacks those columns into a single long Series.
3. **`.value_counts()`** – counts true frequencies.

```python
split_genres = df_apps_clean.Genres.str.split(';', expand=True)
stacked_genres = split_genres.stack()
true_genre_counts = stacked_genres.value_counts()
```

This technique revealed that the `Genres` column actually contained **53 distinct genres**, not the 114 suggested by the raw unique count.

---

## 4. Data Visualisation with Plotly Express

Plotly Express (`px`) allows you to create interactive, publication‑ready charts with minimal code.

### 4.1 Pie and Donut Charts
- **`px.pie()`** – creates a pie chart. Add `hole` to make a donut.
  ```python
  fig = px.pie(labels=ratings.index, values=ratings.values, hole=0.6)
  fig.update_traces(textposition='inside', textinfo='percent')
  ```

### 4.2 Bar Charts (Vertical and Horizontal)
- **`px.bar()`** – basic bar chart. Use `orientation='h'` for horizontal bars.
  ```python
  # Vertical
  px.bar(x=top10_category.index, y=top10_category.values)

  # Horizontal
  px.bar(x=category_installs.Installs, y=category_installs.index, orientation='h')
  ```

### 4.3 Grouped Bar Charts
- Use `color` to split by a categorical variable and `barmode='group'` for side‑by‑side bars.
  ```python
  px.bar(df_free_vs_paid, x='Category', y='App', color='Type', barmode='group')
  ```

### 4.4 Scatter Plots
- **`px.scatter()`** – plots two numeric variables. Can encode extra dimensions with `size`, `color`, and `hover_name`.
  ```python
  px.scatter(cat_merged_df, x='App', y='Installs', size='App', hover_name=cat_merged_df.index, color='Installs')
  ```

### 4.5 Box Plots
- **`px.box()`** – shows distribution of a numeric variable across categories.
  ```python
  px.box(df_apps_clean, y='Installs', x='Type', notched=True, points='all')
  ```

### 4.6 Customising Layouts
- **`.update_layout()`** – modify titles, axis labels, axis scales, and more.
  ```python
  fig.update_layout(
      xaxis_title='Category',
      yaxis_title='Number of Apps',
      xaxis={'categoryorder': 'total descending'},
      yaxis=dict(type='log')
  )
  ```

### 4.7 Colour Scales
- Use `color_continuous_scale` in `px.bar` or `px.scatter` to apply a built‑in colour gradient.
- Hide the colour bar with `coloraxis_showscale=False`.
  ```python
  px.bar(..., color=num_genres.values, color_continuous_scale='Agsunset')
  fig.update_layout(coloraxis_showscale=False)
  ```

---

## 5. Key Business Insights from the Analysis

| Question | Answer |
|----------|--------|
| Most competitive categories? | FAMILY (1,606 apps), GAME (910), TOOLS (719) |
| Most popular categories (total downloads)? | GAME (13.8B), COMMUNICATION (11.0B), TOOLS (8.1B) |
| Categories with highest paid‑app proportion? | Personalization (22%), Medical (22%), Weather (10%) |
| Median downloads: free vs paid? | Free: ~500,000; Paid: ~5,000 (100× fewer) |
| Top‑grossing paid app? | Minecraft (~$70M estimated revenue) |
| Median price of a paid app? | $2.99 |
| Categories with highest median price? | Medical ($5.49), Business ($4.99), Dating ($6.99) |
| Do most paid apps recoup $30k development cost? | No – only a few categories (e.g., Game, Medical) have median revenue near or above $30k. |

---

## 6. Final Thoughts

You've completed a full data science workflow:

1. **Data acquisition** – loading a CSV.
2. **Data cleaning** – handling missing values, duplicates, and irrelevant columns.
3. **Data transformation** – converting data types and extracting nested information.
4. **Exploratory data analysis** – asking questions and summarising.
5. **Data visualisation** – creating insightful, interactive charts.
6. **Drawing conclusions** – translating visual patterns into business recommendations.

These skills are transferable to any dataset. Whether you're analysing app stores, e‑commerce sales, or scientific data, the principles remain the same: clean thoroughly, explore creatively, and visualise clearly.

---

## 7. Quick Reference of Pandas & Plotly Methods Used

| Purpose | Pandas Method | Plotly Method |
|---------|----------------|----------------|
| Random sample | `.sample()` | – |
| Drop columns | `.drop(axis=1)` | – |
| Find missing | `.isna()` | – |
| Drop missing | `.dropna()` | – |
| Find duplicates | `.duplicated()` | – |
| Drop duplicates | `.drop_duplicates()` | – |
| Split strings | `.str.split()` | – |
| Stack columns | `.stack()` | – |
| Value counts | `.value_counts()` | – |
| Group and aggregate | `.groupby().agg()` | – |
| Merge DataFrames | `.merge()` | – |
| Pie chart | – | `px.pie()` |
| Bar chart | – | `px.bar()` |
| Scatter plot | – | `px.scatter()` |
| Box plot | – | `px.box()` |
| Update layout | – | `.update_layout()` |

---

