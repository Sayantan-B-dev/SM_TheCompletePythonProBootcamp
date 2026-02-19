# Project Summary and Learning Outcomes

This final section consolidates the techniques, tools, and insights gained from the comprehensive analysis of Nobel Prize data. The project demonstrated the full data science workflow: from data cleaning and exploration to advanced visualizations and statistical modeling.

---

## 1. Python and Pandas Techniques Revisited

Throughout the analysis, several fundamental pandas operations were applied:

### Data Inspection and Cleaning
- **Shape and structure**: `df_data.shape`, `df_data.head()`, `df_data.tail()` provided initial overview.
- **Missing values**: `isna().sum()` identified columns with NaNs; filtering (`.loc`) explained their origin (organizations, literature/peace laureates).
- **Duplicate detection**: `duplicated().any()` confirmed no duplicate rows.

### Data Type Conversions
- **String to datetime**: `pd.to_datetime()` converted `birth_date`.
- **String to numeric**: splitting `prize_share` (e.g., `"1/2"`) and computing `share_pct` using `str.split`, `pd.to_numeric`, and division.

### Grouping and Aggregation
- **Simple counts**: `.value_counts()` for gender, category, city, organization.
- **Grouped operations**: `.groupby()` with `.agg()` to compute counts per category and gender, per country, per year, etc.
- **Rolling averages**: `.rolling().mean()` for time‑series smoothing.
- **Cumulative sums**: `.cumsum()` after grouping to show total prizes over time per country.

### Merging DataFrames
- `pd.merge()` combined country‑category counts with total country counts to create a stacked bar chart dataset.

### Sorting and Indexing
- `.sort_values()` arranged rankings; `.reset_index()` prepared data for plotting.

---

## 2. New Visualization Tools and Techniques

The project introduced several advanced plotting methods, primarily using Plotly Express and Seaborn.

### Plotly Express Charts
- **Donut chart**: `px.pie()` with `hole` parameter to show gender proportions.
- **Bar charts**: vertical and horizontal (`orientation='h'`) with color mapping (`color`) and custom color scales (`color_continuous_scale`).
- **Choropleth map**: `px.choropleth()` mapped prize counts by country using ISO codes.
- **Sunburst chart**: `px.sunburst()` displayed hierarchical data (country → city → organization) with sector sizes proportional to prize counts.
- **Line chart**: `px.line()` with color differentiation showed cumulative prizes per country over time.

### Seaborn Statistical Visualizations
- **Histogram**: `sns.histplot()` with adjustable bins visualized age distribution.
- **Box plot**: `sns.boxplot()` compared age distributions across categories.
- **Regression plot**: `sns.regplot()` with `lowess=True` revealed non‑linear trends in age over time.
- **Faceted regression**: `sns.lmplot()` with `row` parameter created separate panels for each category.
- **Hue‑based regression**: `sns.lmplot()` with `hue` overlaid multiple categories on one chart.

### Matplotlib Enhancements
- **Dual‑axis plots**: `twinx()` allowed simultaneous display of prize count and average share.
- **Axis inversion**: `invert_yaxis()` clarified the inverse relationship.
- **Custom tick formatting**: `np.arange()` and `plt.xticks()` controlled tick frequency.
- **Figure styling**: `plt.figure(figsize, dpi)` and `plt.title`, `plt.xlabel` improved readability.

---

## 3. Key Insights from the Analysis

### Gender Representation
- Only **6.2%** of individual Nobel laureates are women.
- First three female winners: Marie Curie (Physics 1903), Bertha von Suttner (Peace 1905), Selma Lagerlöf (Literature 1909).
- Gender gap varies by category: Physics has just 4 women, while Peace has 17; Literature has 16.

### Repeat Winners
- Six laureates (four individuals, two organizations) have won multiple prizes: Marie Curie, Linus Pauling, John Bardeen, Frederick Sanger, International Red Cross, UNHCR.

### Prize Categories
- Most awarded: **Medicine** (222), then Physics (216), Chemistry (186).
- Economics, introduced in 1969, has the fewest (86).

### Geographic Patterns
- **Top countries** by laureate birth: USA (281), UK (105), Germany (84).
- **Choropleth map** shows concentration in North America and Europe.
- **Category breakdown**: USA dominates all categories, especially Economics (49); Germany excels in Physics; France leads in Peace and Literature.
- **Cumulative trends**: USA pulled ahead after WWII; Europe dominated before 1945; the prize has become more global in recent decades.

### Research Institutions and Cities
- **Top institution**: University of California (40 prizes), followed by Harvard (29), Stanford (23).
- **Top research city**: Cambridge, MA (50 prizes); European leader: London (31).
- **Birth cities**: New York (53), Paris (26), London (19) produce most laureates; Vienna (14) and Budapest (8) are notable per‑capita contributors.
- **Sunburst chart** reveals France’s research concentrated in Paris, Germany’s spread across many cities, UK’s dual centers (London and Cambridge).

### Laureate Age
- Average age at award: **60 years** (median 60).
- Oldest: John Goodenough (Chemistry 2019, age 97); youngest: Malala Yousafzai (Peace 2014, age 17).
- Age has increased over time (from ~55 in 1900 to ~70 in 2020) for Physics, Chemistry, Medicine; Peace winners have become younger.
- Economics shows stable age; Literature and Peace have widest age ranges.

---

## 4. Methodological Takeaways

- **Different visualizations reveal different stories**: a box plot aggregates all time, while a time‑series regression shows trends within categories.
- **Handling missing data**: understanding why values are missing (e.g., organizations vs. individuals) is crucial before deciding whether to impute or exclude.
- **Choosing the right geographic column**: `birth_country_current` was preferred over historical `birth_country` for modern comparisons.
- **Interactive charts** (Plotly) allow exploration beyond static images – zooming, panning, hovering.

---

## 5. Conclusion

This project successfully applied a wide range of data science techniques to uncover patterns in Nobel Prize history. The analysis demonstrated:

- How to prepare and clean a real‑world dataset.
- How to create both simple and complex visualizations.
- How to interpret and communicate findings.

