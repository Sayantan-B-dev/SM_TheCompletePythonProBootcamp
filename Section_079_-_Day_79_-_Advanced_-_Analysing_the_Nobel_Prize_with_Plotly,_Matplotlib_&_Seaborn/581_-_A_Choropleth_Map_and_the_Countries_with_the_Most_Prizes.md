# Geographic Analysis of Nobel Laureates

This section shifts focus from overall trends to geographic patterns. We examine which countries have produced the most laureates, how these distributions look on a world map, how prize categories vary by country, and how the cumulative counts have evolved over time. Plotly Express is used for its interactive maps and bar charts.

---

## 1. Top 20 Countries by Number of Prizes

### Choosing the Right Country Column

The dataset contains three columns that could indicate a laureate's country:

- `birth_country`: country of birth as recorded at the time (e.g., `"Prussia (Poland)"`).
- `birth_country_current`: modern name of the birth country (e.g., `"Poland"`).
- `organization_country`: country of the affiliated institution.

Each has limitations:

- `birth_country` contains historical country names that no longer exist (e.g., Soviet Union, Czechoslovakia). Aggregating by these would misrepresent modern geography.
- `organization_country` is only available for laureates with an affiliated organization (about 70% of rows) and does not reflect the laureate's origin. It might be more appropriate for studying where research happened, not where laureates came from.
- `birth_country_current` provides a consistent, modern country name for nearly all individuals (organizations have NaN). This is the most suitable for a geographic ranking of laureates by origin, with the caveat that it does not account for nationality or where they lived at the time of the award. It simply records the current name of the country where they were born.

Thus, we use `birth_country_current`.

### Grouping and Sorting

```python
top_countries = df_data.groupby(['birth_country_current'],
                                 as_index=False).agg({'prize': 'count'})
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]   # last 20 rows (largest counts)
```

- `groupby` with `as_index=False` keeps `birth_country_current` as a column.
- `agg({'prize': 'count'})` counts rows per country.
- Sorting ascending places the smallest counts first; we take the last 20 rows to get the top 20.
- The resulting DataFrame has two columns: `birth_country_current` and `prize`.

### Horizontal Bar Chart with Plotly

A horizontal bar chart is effective for displaying ranked categorical data. Plotly Express makes it easy:

```python
fig = px.bar(
    x=top20_countries.prize,
    y=top20_countries.birth_country_current,
    orientation='h',
    color=top20_countries.prize,
    color_continuous_scale='Viridis',
    title='Top 20 Countries by Number of Prizes'
)
fig.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Country',
    coloraxis_showscale=False
)
fig.show()
```

- `orientation='h'` makes the bars horizontal.
- `color` maps the bar color to the prize count, using the `Viridis` color scale.
- `coloraxis_showscale=False` hides the color bar because the values are already on the x‑axis.

**Observations**:
- The United States dominates with **281** prizes.
- The United Kingdom follows with **105**, then Germany with **84**.
- France, Sweden, Japan, and others make up the rest.
- The top 20 list includes mostly European countries plus the US, Canada, Japan, China, Australia, and India.

---

## 2. Choropleth Map: Global Distribution

A choropleth map colors countries based on a numeric value. Plotly’s `px.choropleth` requires country identifiers; we use the ISO three‑letter codes (column `ISO`).

### Preparing the Data

We need a DataFrame with one row per country, containing the country name, its ISO code, and the total prize count. The `ISO` column already matches `birth_country_current` for most rows (but may have NaNs for organizations). We can group by both `birth_country_current` and `ISO` to ensure the ISO code is retained.

```python
df_countries = df_data.groupby(['birth_country_current', 'ISO'],
                                as_index=False).agg({'prize': 'count'})
df_countries.sort_values('prize', ascending=False, inplace=True)
```

- This groups by the combination of country name and ISO, which is safe because each country should have a unique ISO.
- The result includes all countries that appear in the data, even those with only one prize.

### Creating the Map

```python
fig = px.choropleth(
    df_countries,
    locations='ISO',
    color='prize',
    hover_name='birth_country_current',
    color_continuous_scale=px.colors.sequential.matter,
    title='Nobel Prizes by Birth Country'
)
fig.update_layout(coloraxis_showscale=True)
fig.show()
```

- `locations='ISO'` tells Plotly to use the ISO codes to identify countries.
- `color='prize'` sets the color intensity based on prize count.
- `hover_name` displays the country name on hover.
- `color_continuous_scale` can be any Plotly sequential scale; `matter` gives a pleasing gradient from light beige to dark brown.
- `coloraxis_showscale=True` adds a color bar legend.

**Interactive Features**:
- Zoom and pan to explore.
- Hover over any country to see its name and prize count.
- The map clearly shows the concentration in North America and Europe, with few prizes from Africa, Asia (except Japan, China, India), and South America.

---

## 3. Country Bar Chart Broken Down by Category

### Data Preparation for Stacked Categories

To see which categories contribute to each country's total, we need a DataFrame with country, category, and prize count, plus the total per country to preserve sorting order.

**Step 1: Count prizes by country and category**

```python
cat_country = df_data.groupby(['birth_country_current', 'category'],
                              as_index=False).agg({'prize': 'count'})
cat_country.sort_values(by='prize', ascending=False, inplace=True)
```

This gives, for example, USA–Medicine 78, USA–Physics 70, etc.

**Step 2: Merge with the total per country**

We already have `top_countries` containing total prize counts per country. Merge on `birth_country_current`:

```python
merged_df = pd.merge(cat_country, top_countries, on='birth_country_current')
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize']
merged_df.sort_values(by='total_prize', inplace=True)
```

- After merging, we rename columns for clarity.
- Sorting by `total_prize` ensures that countries appear in the final bar chart in order of total prize count.

### Stacked Horizontal Bar Chart

```python
fig = px.bar(
    x=merged_df.cat_prize,
    y=merged_df.birth_country_current,
    color=merged_df.category,
    orientation='h',
    title='Top 20 Countries by Number of Prizes and Category'
)
fig.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Country'
)
fig.show()
```

- Now each country's bar is subdivided by category, with colors representing the six prize categories.
- The bars are stacked automatically because we use `color` without specifying a `barmode`; the default is `'relative'` (stacked).

**Insights from the Chart**:
- The United States has an enormous number of prizes in **Medicine** (78) and **Physics** (70), and also leads in **Economics** (49).
- **Germany** and the **UK** have similar totals, but Germany has more in Physics (26 vs 24) while the UK has more in Medicine (28 vs 18).
- **France** has a notable number of Peace and Literature prizes, reflecting its cultural and political influence.
- **Japan** has a strong showing in Physics and Chemistry, but few in Economics.
- **Australia**’s prizes are predominantly in Medicine and Physics.
- The **Netherlands** has half its prizes in Medicine (9 out of 18).
- The US alone has more prizes in Economics (49) than the entire total of France (57) or any other country except the UK and Germany.

This breakdown answers the specific questions posed in the challenge:

| Question | Answer |
|----------|--------|
| In which category are Germany and Japan weakest compared to the US? | **Economics** – US has 49, Germany has 4, Japan has 2. |
| In which category does Germany have more prizes than the UK? | **Physics** – Germany 26, UK 24. |
| In which categories does France have more prizes than Germany? | **Peace** (France 10, Germany 5) and **Literature** (France 11, Germany 8). |
| Which category makes up most of Australia's prizes? | **Medicine** (7 out of 10). |
| Which category makes up half of the Netherlands' prizes? | **Medicine** (9 out of 18). |
| Does the US have more prizes in Economics than all of France? | Yes – US 49, France total 57, but France's total includes all categories; the US has 49 in Economics alone. In Physics, US 70 > France total 57; in Medicine, US 78 > France total 57. |

---

## 4. Cumulative Prizes by Country Over Time

### Motivation

The previous charts show total counts, but we might ask: when did the United States become dominant? Were there periods when other countries led? A cumulative line chart reveals how each country's total grew year by year.

### Data Preparation

We need, for each country and year, the number of prizes awarded that year. Then we compute the cumulative sum for each country over time.

**Step 1: Count prizes per country per year**

```python
prize_by_year = df_data.groupby(by=['birth_country_current', 'year'],
                                as_index=False).count()
prize_by_year = prize_by_year[['year', 'birth_country_current', 'prize']]
prize_by_year.sort_values('year', inplace=True)
```

- `groupby` yields counts for each combination of country and year.
- We select only the columns we need and sort by year for chronological order.

**Step 2: Compute cumulative sum within each country**

```python
cumulative_prizes = prize_by_year.groupby(
    by=['birth_country_current', 'year']
).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)
```

- The first `groupby` with `.sum()` ensures that if a country had multiple prizes in the same year, they are summed (though with our current grouping, each year should have only one row per country). This step is somewhat redundant but safe.
- `groupby(level=[0])` groups by country (the first level of the index after the first groupby), and `.cumsum()` computes the cumulative sum of prizes over years.
- Finally, `reset_index` brings the index back as columns.

### Line Chart

Plotly Express can create a line chart where each country is a separate line, distinguished by color.

```python
fig = px.line(
    cumulative_prizes,
    x='year',
    y='prize',
    color='birth_country_current',
    hover_name='birth_country_current',
    title='Cumulative Nobel Prizes by Country Over Time'
)
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Cumulative Number of Prizes'
)
fig.show()
```

- `color='birth_country_current'` assigns a different line color to each country.
- `hover_name` displays the country name on hover.

**Observations**:

- Prior to **about 1930**, the race was relatively even among several European countries: Germany, UK, France, Sweden.
- The United States began to pull away **after World War II**, around 1945–1950. The devastation in Europe likely contributed to this shift, as scientific talent and resources moved to the US.
- The UK maintained second place but was overtaken by Germany briefly in the 1970s and 90s, then pulled ahead again.
- Sweden shows steady growth, often ranking 5th or 6th, possibly reflecting a home‑country bias in the selection committee? (This is speculation but interesting.)
- Japan's curve steepens after the 1980s, indicating a rise in scientific output.
- Many countries only appear later in the timeline, showing that the prize has become more global over the last 40 years.

---

## Summary

This geographic analysis revealed:

1. **Country rankings**: USA leads by a wide margin, followed by UK, Germany, France.
2. **Choropleth map**: visually confirms the concentration in North America and Europe.
3. **Category breakdown**: shows the strengths and weaknesses of each country – e.g., USA dominates Economics, Germany excels in Physics, France in Peace and Literature.
4. **Cumulative trends**: the US dominance is a post‑WWII phenomenon; before that, European countries were more balanced.
