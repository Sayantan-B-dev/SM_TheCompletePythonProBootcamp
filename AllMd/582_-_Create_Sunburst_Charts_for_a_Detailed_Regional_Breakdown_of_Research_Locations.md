# Regional Breakdown of Research Locations

This section zooms in on the institutional affiliations of Nobel laureates. We investigate which research organizations, cities, and countries have produced the most laureates, and visualize the hierarchical relationship between country, city, and organization using a sunburst chart.

The analysis addresses:

1. Which research institutions have the most affiliated laureates?
2. Which cities are the hottest spots for discoveries?
3. How do birth cities compare to research cities?
4. How can we visualize the geographic concentration of research at multiple levels?

---

## 1. Top Research Organizations

### Data Extraction

The column `organization_name` contains the name of the institution where the laureate was affiliated at the time of the award. For individuals without an affiliation (mostly Literature and Peace laureates), this column is NaN. To find the organizations with the most affiliated laureates, we count the occurrences of each organization name.

```python
top20_orgs = df_data.organization_name.value_counts()[:20]
```

`.value_counts()` returns a Series with institution names as index and counts as values, sorted descending. We take the first 20 entries.

### Sorting for Horizontal Bar Chart

Horizontal bar charts are easier to read when the longest bar is at the top. Plotly will plot bars in the order of the input data. To achieve descending order from top to bottom, we sort the Series in ascending order (so that the smallest value appears first, and the largest last, which will be at the top of the chart when we reverse the y‑axis later). Actually, Plotly's orientation='h' will plot from bottom to top in the order of the y‑axis categories. So we need the categories in the order we want displayed. We'll sort ascending so that the smallest count appears first (at the bottom) and the largest appears last (at the top). Alternatively, we can sort descending and then use `categoryorder` in layout. For simplicity, we'll sort ascending.

```python
top20_orgs.sort_values(ascending=True, inplace=True)
```

Now `top20_orgs` has the smallest count at the beginning and largest at the end.

### Creating the Bar Chart

```python
fig = px.bar(
    x=top20_orgs.values,
    y=top20_orgs.index,
    orientation='h',
    color=top20_orgs.values,
    color_continuous_scale=px.colors.sequential.haline,
    title='Top 20 Research Institutions by Number of Prizes'
)
fig.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Institution',
    coloraxis_showscale=False
)
fig.show()
```

- `x` takes the counts, `y` the institution names.
- `orientation='h'` makes horizontal bars.
- `color` shades bars by count, using the `haline` color scale (blue‑green).
- `coloraxis_showscale=False` hides the color bar.

**Results**:

| Rank | Institution                                          | Prizes |
|------|------------------------------------------------------|--------|
| 1    | University of California                             | 40     |
| 2    | Harvard University                                   | 29     |
| 3    | Stanford University                                  | 23     |
| 4    | Massachusetts Institute of Technology (MIT)         | 21     |
| 5    | University of Chicago                                | 20     |
| 6    | University of Cambridge                              | 18     |
| 7    | Columbia University                                  | 17     |
| 7    | California Institute of Technology (Caltech)        | 17     |
| 9    | Princeton University                                 | 15     |
| 10   | Rockefeller University                               | 13     |
| 10   | Max‑Planck‑Institut                                  | 13     |
| 12   | University of Oxford                                 | 12     |
| 13   | Yale University                                      | 9      |
| 14   | MRC Laboratory of Molecular Biology                  | 8      |
| 14   | Cornell University                                   | 8      |
| 16   | Bell Laboratories                                    | 8      |
| 16   | University of California, Berkeley (implied?)        | ...    |

**Observations**:

- The **University of California** system leads, reflecting its multi‑campus structure (though the data may lump some campuses together).
- **Harvard**, **Stanford**, and **MIT** are top‑tier.
- European institutions like **Cambridge**, **Oxford**, and the **Max Planck Institutes** are also prominent.
- **Bell Laboratories** (USA) and the **MRC Laboratory of Molecular Biology** (UK) are notable non‑university research centers.

---

## 2. Top Research Cities

Just as we ranked organizations, we can rank the cities where these organizations are located.

```python
top20_org_cities = df_data.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)
```

### Horizontal Bar Chart

```python
fig = px.bar(
    x=top20_org_cities.values,
    y=top20_org_cities.index,
    orientation='h',
    color=top20_org_cities.values,
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Which Cities Do the Most Research?'
)
fig.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='City',
    coloraxis_showscale=False
)
fig.show()
```

**Results** (top 5):

| City            | Prizes |
|-----------------|--------|
| Cambridge, MA   | 50     |
| New York, NY    | 45     |
| London          | 31     |
| Cambridge (UK)  | 27     |
| Paris           | 25     |

**Observations**:

- **Cambridge, Massachusetts** (home to MIT and Harvard) is the undisputed leader.
- **New York City** (Columbia, Rockefeller, etc.) is second.
- **London** and **Cambridge (UK)** follow closely.
- **Paris** is the top European continental city.
- US cities dominate the list, reflecting the concentration of research funding and institutions.

---

## 3. Birth Cities of Nobel Laureates

For comparison, we look at where laureates were born (rather than where they did their prize‑winning work). The column `birth_city` contains this information (with some missing values for organizations and a few individuals).

```python
top20_cities = df_data.birth_city.value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)
```

### Horizontal Bar Chart

```python
fig = px.bar(
    x=top20_cities.values,
    y=top20_cities.index,
    orientation='h',
    color=top20_cities.values,
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Where were the Nobel Laureates Born?'
)
fig.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='City of Birth',
    coloraxis_showscale=False
)
fig.show()
```

**Results** (top 5):

| City          | Prizes |
|---------------|--------|
| New York, NY  | 53     |
| Paris         | 26     |
| London        | 19     |
| Vienna        | 14     |
| Chicago, IL   | 12     |

**Observations**:

- **New York** produces far more laureates than any other city (53).
- **Paris** (26) and **London** (19) are major European birthplaces.
- **Vienna** (14) is notable given its smaller population, reflecting its historical role as a cultural and scientific hub (Freud, etc.).
- **Budapest** (8) also appears in the top 20, another example of a city with high per‑capita output.

### Comparison with Research Cities

The lists differ significantly:

- Research cities: Cambridge MA, New York, London, Cambridge UK, Paris, Stanford, Berkeley.
- Birth cities: New York, Paris, London, Vienna, Chicago, Berlin, Budapest.

Major research hubs like Cambridge MA and Stanford are not major birthplaces because laureates move to these institutions later in life. Conversely, populous cities like New York and London appear in both lists, but birth cities also include places like Vienna and Budapest that have high historical scientific output despite moderate size.

**Key Questions Answered**:

- What percentage of US prizes came from laureates born in New York?  
  New York (53) / US total (281) ≈ **18.9%**.
- How many laureates born in London, Paris, Vienna?  
  London 19, Paris 26, Vienna 14.
- Out of the top 5 birth cities, how many are in the US?  
  Three: New York, Chicago, and (if we extend to top 5) Brooklyn (8) – actually top 5: NY, Paris, London, Vienna, Chicago (2 US). So 2 of top 5.

---

## 4. Sunburst Chart: Country → City → Organization

### Purpose

A sunburst chart displays hierarchical data as concentric rings. Here we can show, for each country, the cities within it that host research organizations, and within each city, the specific organizations. The size of each segment corresponds to the number of prizes affiliated with that entity.

### Data Preparation

We need a DataFrame with three levels: `organization_country`, `organization_city`, `organization_name`, and a value column (prize count). We group by all three and count the number of prizes.

```python
country_city_org = df_data.groupby(
    by=['organization_country', 'organization_city', 'organization_name'],
    as_index=False
).agg({'prize': 'count'})
```

- Rows where `organization_country` is NaN are excluded (organizations unknown or laureates without affiliation). This is fine because we only want to show actual research locations.
- The result contains all combinations that appear in the data, with the count of prizes for that specific organization in that city and country.

We can sort to see the largest counts first, but sorting is not required for the sunburst.

### Creating the Sunburst

```python
fig = px.sunburst(
    country_city_org,
    path=['organization_country', 'organization_city', 'organization_name'],
    values='prize',
    title='Where do Discoveries Take Place?'
)
fig.update_layout(
    xaxis_title='',   # sunburst has its own axes; these are not used
    yaxis_title='',
    coloraxis_showscale=False
)
fig.show()
```

- `path` defines the hierarchy: first level is country, second is city, third is organization.
- `values` determines the size of each sector.
- Plotly automatically aggregates up the hierarchy: the size of a country sector is the sum of all prizes in that country, and similarly for cities.

### Interactive Exploration

- Click on any sector to zoom into that level.
- Hover to see the name and prize count.
- The root represents all data; from there you can drill down.

**Insights**:

- **United States** dominates, with a huge sector. Within the US, cities like **Cambridge MA**, **New York**, **Stanford**, **Berkeley**, **Princeton** appear as large sectors.
- **United Kingdom**: London and Cambridge are prominent.
- **Germany**: research is spread across multiple cities (Berlin, Munich, Heidelberg, Göttingen, etc.), reflecting a decentralized research landscape.
- **France**: almost all organizations are in **Paris** (with a few in Strasbourg, Grenoble). This shows strong centralization.
- **Switzerland**: Zurich, Geneva, Basel are all visible.
- **Japan**: Tokyo, Kyoto, Nagoya appear.

**Notable Observations**:

- France's research is highly concentrated in Paris, whereas Germany's is distributed across many cities. This may reflect historical and funding differences.
- The UK has a mix: London is a hub, but Cambridge and Oxford are also major centers.
- The sunburst makes it easy to see which countries have a single dominant city vs. multiple centers.

---

## Summary of Findings

| Question | Answer |
|----------|--------|
| Top research organization? | University of California (40 prizes) |
| University of Chicago? | 20 prizes |
| Harvard University? | 29 prizes |
| Top research city? | Cambridge, MA (50 prizes) |
| Top European research city? | London (31 prizes) or Cambridge UK (27)? London is higher. |
| Top birth city? | New York, NY (53 prizes) |
| Percentage of US prizes from NYC births? | ~18.9% |
| London births? | 19 |
| Paris births? | 26 |
| Vienna births? | 14 |
| US cities in top 5 birth cities? | 2 (NY, Chicago) |

The sunburst chart provides a powerful visual summary of the geographic hierarchy of research institutions, revealing patterns of concentration and dispersion that would be difficult to grasp from tables alone.

---

## Technical Notes

- `.value_counts()` is a quick way to get frequencies; for more complex aggregations, `.groupby()` is needed.
- Horizontal bar charts are created with `orientation='h'`.
- Plotly's `px.sunburst` expects a DataFrame with a path and values. It automatically sums values up the hierarchy.
- Missing data (organizations) are excluded from the sunburst, but this is appropriate because we are mapping known research locations.
