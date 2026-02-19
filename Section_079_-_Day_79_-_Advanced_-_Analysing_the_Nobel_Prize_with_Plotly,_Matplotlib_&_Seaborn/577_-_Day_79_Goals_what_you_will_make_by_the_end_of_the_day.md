# Nobel Prize Data Analysis: Comprehensive Project Documentation

This documentation provides an in-depth walkthrough of the analysis performed on the Nobel Prize dataset. It covers every step from initial data inspection to advanced visualizations, explaining the rationale behind each method and the insights gained.

---

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Data Acquisition and Setup](#data-acquisition-and-setup)
    -   [Environment Preparation](#environment-preparation)
    -   [Importing Libraries](#importing-libraries)
    -   [Loading the Dataset](#loading-the-dataset)
3.  [Data Exploration and Cleaning](#data-exploration-and-cleaning)
    -   [Initial Data Inspection](#initial-data-inspection)
    -   [Handling Missing Values](#handling-missing-values)
    -   [Type Conversions and Feature Engineering](#type-conversions-and-feature-engineering)
4.  [Analyzing Prize Distribution by Gender and Category](#analyzing-prize-distribution-by-gender-and-category)
    -   [Gender Disparity: Donut Chart](#gender-disparity-donut-chart)
    -   [First Female Laureates](#first-female-laureates)
    -   [Repeat Winners](#repeat-winners)
    -   [Number of Prizes per Category](#number-of-prizes-per-category)
    -   [The Economics Prize](#the-economics-prize)
    -   [Gender Split by Category](#gender-split-by-category)
5.  [Temporal Trends in Prize Awards](#temporal-trends-in-prize-awards)
    -   [Number of Prizes Awarded Over Time](#number-of-prizes-awarded-over-time)
    -   [Prize Sharing Over Time](#prize-sharing-over-time)
6.  [Geographical Analysis of Laureates](#geographical-analysis-of-laureates)
    -   [Top Countries by Number of Prizes](#top-countries-by-number-of-prizes)
    -   [Choropleth Map of Prize Counts](#choropleth-map-of-prize-counts)
    -   [Category Breakdown by Country](#category-breakdown-by-country)
    -   [Cumulative Prizes by Country Over Time](#cumulative-prizes-by-country-over-time)
7.  [Institutional and Urban Hotspots](#institutional-and-urban-hotspots)
    -   [Top Research Organizations](#top-research-organizations)
    -   [Cities Where Discoveries Happen](#cities-where-discoveries-happen)
    -   [Birth Cities of Laureates](#birth-cities-of-laureates)
    -   [Sunburst Chart: Country → City → Organization](#sunburst-chart-country--city--organization)
8.  [Age Analysis of Nobel Laureates](#age-analysis-of-nobel-laureates)
    -   [Calculating Age at Award](#calculating-age-at-award)
    -   [Oldest and Youngest Winners](#oldest-and-youngest-winners)
    -   [Descriptive Statistics and Age Distribution](#descriptive-statistics-and-age-distribution)
    -   [Age Trends Over Time](#age-trends-over-time)
    -   [Age Variation Across Categories](#age-variation-across-categories)
    -   [Combined Trends with `lmplot`](#combined-trends-with-lmplot)
9.  [Summary of Key Insights](#summary-of-key-insights)
10. [Resources and References](#resources-and-references)

---

## Project Overview

The Nobel Prize is one of the most prestigious awards, honoring individuals and organizations for their outstanding contributions to humanity in the fields of Physics, Chemistry, Medicine, Literature, Peace, and Economic Sciences. This project delves into a comprehensive dataset of Nobel laureates from 1901 to 2020, aiming to uncover patterns related to gender, geography, institutional affiliations, and age.

By the end of this analysis, we will have created a series of visualizations:
-   **Donut and bar charts** to display categorical distributions.
-   **Time series plots** with rolling averages and dual axes.
-   **Choropleth maps** for geographic distribution.
-   **Sunburst charts** to represent hierarchical data (country → city → organization).
-   **Regression plots** and box plots to analyze age trends.

---

## Data Acquisition and Setup

### Environment Preparation

The analysis is conducted in a Google Colab environment. One crucial step is ensuring that the `plotly` library is up-to-date, as older versions may lack features like sunburst charts.

```python
# Uncomment and run this cell only in Google Colab to upgrade plotly
# !pip install --upgrade plotly
```

### Importing Libraries

We import the necessary libraries for data manipulation and visualization:

```python
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
```

Additionally, we set a pandas option to display floating-point numbers with two decimal places for better readability:

```python
pd.options.display.float_format = '{:,.2f}'.format
```

### Loading the Dataset

The dataset `nobel_prize_data.csv` is loaded into a pandas DataFrame.

```python
df_data = pd.read_csv('nobel_prize_data.csv')
```

A note in the original notebook mentions that for three individuals (Michael Houghton, Venkatraman Ramakrishnan, and Nadia Murad) the exact birth dates were unknown and substituted with a mid-year estimate (July 2nd). This is important to remember when performing age calculations.

---

## Data Exploration and Cleaning

Before diving into analysis, we must understand the structure and quality of the data.

### Initial Data Inspection

We start by checking the shape and previewing the first and last few rows:

```python
df_data.shape          # (962, 16)
df_data.head()
df_data.tail()
```

**Observations:**
- The dataset contains **962 rows** and **16 columns**.
- The first Nobel Prizes were awarded in **1901**, and the data extends to **2020**.
- Columns include information such as year, category, motivation, prize share, laureate type (individual or organization), full name, birth date, birth city, birth country, current birth country, sex, organization name and location, and ISO country code.

### Handling Missing Values

We check for duplicates and missing values:

```python
print(f'Any duplicates? {df_data.duplicated().values.any()}')   # False
print(f'Any NaN values among the data? {df_data.isna().values.any()}')   # True
```

To identify which columns contain NaNs and how many:

```python
df_data.isna().sum()
```

**NaN Counts:**
- `motivation`: 88
- `birth_date`: 28
- `birth_city`: 31
- `birth_country`: 28
- `birth_country_current`: 28
- `sex`: 28
- `organization_name`: 255
- `organization_city`: 255
- `organization_country`: 254
- `ISO`: 28

**Why do these NaNs exist?**
- The 28 missing `birth_date` values correspond to **organizations** (e.g., Red Cross, UN). Organizations do not have a birth date.
- The high number of missing organization-related fields is because many laureates, especially in Literature and Peace, are not affiliated with a research institution. We can verify this:

```python
col_subset = ['year','category', 'laureate_type','full_name', 'organization_name']
df_data.loc[df_data.organization_name.isna()][col_subset]
```

This shows that individuals in Literature and Peace often lack an affiliated organization.

### Type Conversions and Feature Engineering

#### Convert `birth_date` to Datetime

We convert the `birth_date` column from string to pandas datetime objects. This will enable easy extraction of year, month, etc.

```python
df_data.birth_date = pd.to_datetime(df_data.birth_date)
```

#### Create `share_pct` Column

The `prize_share` column is stored as a string fraction (e.g., "1/2", "1/4"). We split it, convert numerator and denominator to numbers, and compute the percentage share as a float.

```python
separated_values = df_data.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denominator = pd.to_numeric(separated_values[1])
df_data['share_pct'] = numerator / denominator
```

After these transformations, we can inspect the data types with `df_data.info()` to confirm that `birth_date` is `datetime64[ns]` and `share_pct` is `float64`.

---

## Analyzing Prize Distribution by Gender and Category

### Gender Disparity: Donut Chart

We want to visualize the proportion of male vs. female laureates. A donut chart (a pie chart with a hole) is an effective choice.

```python
biology = df_data.sex.value_counts()
fig = px.pie(labels=biology.index, 
             values=biology.values,
             title="Percentage of Male vs. Female Winners",
             names=biology.index,
             hole=0.4)

fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
fig.show()
```

**Insight:** Out of all Nobel laureates (individuals), only about **6.2% are women**. This stark imbalance sets the stage for further investigation across categories.

### First Female Laureates

We extract the earliest three female winners by sorting by year.

```python
df_data[df_data.sex == 'Female'].sort_values('year', ascending=True)[:3]
```

The result includes:
- **Marie Curie, née Sklodowska** (1903, Physics)
- **Baroness Bertha Sophie Felicita von Suttner** (1905, Peace)
- **Selma Ottilia Lovisa Lagerlöf** (1909, Literature)

Notice that Marie Curie's birth country is listed as "Russian Empire (Poland)" with current country "Poland". This illustrates the complexity of nationality data due to historical border changes.

### Repeat Winners

Winning a Nobel Prize is rare, but a few individuals and organizations have been honored multiple times. We can identify duplicates in the `full_name` column.

```python
is_winner = df_data.duplicated(subset=['full_name'], keep=False)
multiple_winners = df_data[is_winner]
print(f'There are {multiple_winners.full_name.nunique()} winners who were awarded the prize more than once.')
```

The output shows **6 winners** with multiple prizes. The list includes:
- **Marie Curie** (Physics 1903, Chemistry 1911)
- **Linus Carl Pauling** (Chemistry 1954, Peace 1962)
- **John Bardeen** (Physics 1956, 1972)
- **Frederick Sanger** (Chemistry 1958, 1980)
- **International Committee of the Red Cross** (Peace 1917, 1944, 1963)
- **Office of the United Nations High Commissioner for Refugees** (Peace 1954, 1981)

Only four of these are individuals; the rest are organizations.

### Number of Prizes per Category

We first determine how many distinct categories exist.

```python
df_data.category.nunique()   # 6
```

Then we count prizes per category and create a bar chart.

```python
prizes_per_category = df_data.category.value_counts()
v_bar = px.bar(
        x = prizes_per_category.index,
        y = prizes_per_category.values,
        color = prizes_per_category.values,
        color_continuous_scale='Aggrnyl',
        title='Number of Prizes Awarded per Category')

v_bar.update_layout(xaxis_title='Nobel Prize Category', 
                    coloraxis_showscale=False,
                    yaxis_title='Number of Prizes')
v_bar.show()
```

**Observations:**
- Medicine has the most prizes (222), followed closely by Physics (216) and Chemistry (186).
- Economics has the fewest (86). This is because the Economics prize was established later (1969).

### The Economics Prize

To confirm when Economics was first awarded:

```python
df_data[df_data.category == 'Economics'].sort_values('year')[:3]
```

The first recipients in 1969 were **Jan Tinbergen** and **Ragnar Frisch**.

### Gender Split by Category

We now break down the number of prizes by both category and gender. This requires grouping and aggregation.

```python
cat_men_women = df_data.groupby(['category', 'sex'], 
                               as_index=False).agg({'prize': pd.Series.count})
cat_men_women.sort_values('prize', ascending=False, inplace=True)
```

The resulting DataFrame shows counts for each combination. We then create a stacked bar chart.

```python
v_bar_split = px.bar(x = cat_men_women.category,
                     y = cat_men_women.prize,
                     color = cat_men_women.sex,
                     title='Number of Prizes Awarded per Category split by Men and Women')

v_bar_split.update_layout(xaxis_title='Nobel Prize Category', 
                          yaxis_title='Number of Prizes')
v_bar_split.show()
```

**Key Findings:**
- Women are most represented in **Peace** (17) and **Literature** (16).
- In **Physics**, only 4 women have won, and in **Economics**, only 2.
- The imbalance is most pronounced in the sciences, especially Physics and Economics.

---

## Temporal Trends in Prize Awards

### Number of Prizes Awarded Over Time

We investigate whether the frequency of Nobel Prizes has changed over the decades. First, we count the number of prizes per year.

```python
prize_per_year = df_data.groupby(by='year').count().prize
```

To smooth out yearly fluctuations, we compute a 5-year rolling average.

```python
moving_average = prize_per_year.rolling(window=5).mean()
```

We then create a scatter plot of the raw counts and overlay the rolling average as a line. Matplotlib is used for finer control.

```python
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5), 
           fontsize=14, 
           rotation=45)

ax = plt.gca()
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index, 
           y=prize_per_year.values, 
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax.plot(prize_per_year.index, 
        moving_average.values, 
        c='crimson', 
        linewidth=3)

plt.show()
```

**Observations:**
- The number of prizes awarded per year has generally increased over time.
- There are noticeable dips during **World War I and World War II**, where fewer prizes were given.
- A sharp increase occurs after 1969, coinciding with the addition of the Economics prize.
- In recent decades, it has become common to award more than one prize per category per year, leading to higher annual counts.

### Prize Sharing Over Time

As more prizes are awarded, it is possible that they are also shared among more laureates. We examine the average prize share (percentage of the prize each laureate receives) over time.

```python
yearly_avg_share = df_data.groupby(by='year').agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()
```

To compare the number of prizes and the average share on the same plot, we use a secondary y-axis.

```python
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5), 
           fontsize=14, 
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()   # create second y-axis
ax1.set_xlim(1900, 2020)

# Plot number of prizes
ax1.scatter(x=prize_per_year.index, 
           y=prize_per_year.values, 
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax1.plot(prize_per_year.index, 
        moving_average.values, 
        c='crimson', 
        linewidth=3)

# Plot average prize share
ax2.plot(prize_per_year.index, 
        share_moving_average.values, 
        c='grey', 
        linewidth=3)

plt.show()
```

To make the inverse relationship clearer, we can invert the secondary y-axis:

```python
ax2.invert_yaxis()
```

**Insight:** As the number of prizes awarded per year increases (crimson line), the average share of the prize (grey line) decreases. This confirms that more prizes are being shared among multiple laureates in recent times.

---

## Geographical Analysis of Laureates

### Top Countries by Number of Prizes

We want to rank countries by the number of Nobel laureates they have produced. There are three candidate columns: `birth_country`, `birth_country_current`, and `organization_country`. Each has its own biases.

- `birth_country` may contain obsolete country names (e.g., Soviet Union).
- `organization_country` reflects where the research was conducted, not the laureate's origin.
- `birth_country_current` updates the birth location to modern country names, which is the most appropriate for a "country of origin" analysis, though it doesn't account for nationality changes.

We'll use `birth_country_current`.

```python
top_countries = df_data.groupby(['birth_country_current'], 
                                  as_index=False).agg({'prize': pd.Series.count})

top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]   # take top 20
```

Now create a horizontal bar chart for readability.

```python
h_bar = px.bar(x=top20_countries.prize,
               y=top20_countries.birth_country_current,
               orientation='h',
               color=top20_countries.prize,
               color_continuous_scale='Viridis',
               title='Top 20 Countries by Number of Prizes')

h_bar.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='Country',
                    coloraxis_showscale=False)
h_bar.show()
```

**Ranking:**
1.  United States of America (281)
2.  United Kingdom (105)
3.  Germany (84)
4.  France (57)
5.  Sweden (29)
...

The United States dominates by a wide margin.

### Choropleth Map of Prize Counts

A choropleth map provides an intuitive geographic visualization. We need a DataFrame with country names, ISO codes, and prize counts.

```python
df_countries = df_data.groupby(['birth_country_current', 'ISO'], 
                               as_index=False).agg({'prize': pd.Series.count})
```

Then we use `px.choropleth`.

```python
world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize', 
                          hover_name='birth_country_current', 
                          color_continuous_scale=px.colors.sequential.matter)

world_map.update_layout(coloraxis_showscale=True)
world_map.show()
```

The map highlights the concentration of Nobel laureates in North America and Europe, with the US, UK, and Western Europe appearing darkest.

### Category Breakdown by Country

To see which categories drive each country's total, we first group by country and category.

```python
cat_country = df_data.groupby(['birth_country_current', 'category'], 
                               as_index=False).agg({'prize': pd.Series.count})
```

Then we merge this with the `top20_countries` DataFrame to retain only the top 20 countries and also include their total prize count (for ordering).

```python
merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize']
merged_df.sort_values(by='total_prize', inplace=True)
```

Now create a stacked horizontal bar chart.

```python
cat_cntry_bar = px.bar(x=merged_df.cat_prize,
                       y=merged_df.birth_country_current,
                       color=merged_df.category,
                       orientation='h',
                       title='Top 20 Countries by Number of Prizes and Category')

cat_cntry_bar.update_layout(xaxis_title='Number of Prizes', 
                            yaxis_title='Country')
cat_cntry_bar.show()
```

**Answers to specific questions:**
- **Germany and Japan** are weakest compared to the US in **Economics** (US has 49, Germany 1, Japan 0).
- **Germany** has more prizes than the UK in **Physics** (26 vs 24).
- **France** has more prizes than Germany in **Peace** (10 vs 5) and **Literature** (11 vs 8).
- Most of **Australia's** prizes are in **Medicine** (7 out of 10).
- Half of the **Netherlands'** prizes are in **Physics** (9 out of 18).
- The **US** has more prizes in **Economics** (49) than **France has in total (57)**, and the US's Physics count (70) alone surpasses France's total.

### Cumulative Prizes by Country Over Time

We examine how countries' total prize counts have accumulated over the years. This reveals when countries rose to prominence.

First, count prizes by country and year.

```python
prize_by_year = df_data.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]
```

Then calculate the cumulative sum for each country.

```python
cumulative_prizes = prize_by_year.groupby(by=['birth_country_current',
                                              'year']).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)
```

Now plot using plotly line chart.

```python
l_chart = px.line(cumulative_prizes,
                  x='year', 
                  y='prize',
                  color='birth_country_current',
                  hover_name='birth_country_current')

l_chart.update_layout(xaxis_title='Year',
                      yaxis_title='Number of Prizes')
l_chart.show()
```

**Observations:**
- Before World War II, the Nobel Prize was a largely **European affair**, with Germany, UK, and France leading.
- The **United States** began to surge after WWII, overtaking all others around the 1960s and continuing to pull away.
- Germany and the UK have traded places multiple times.
- Sweden maintains a steady position in the top 5, possibly reflecting a home-country bias.
- The number of countries represented has expanded significantly in recent decades, indicating a more global prize.

---

## Institutional and Urban Hotspots

### Top Research Organizations

Many laureates are affiliated with universities or research institutes. We can rank these organizations.

```python
top20_orgs = df_data.organization_name.value_counts()[:20]
top20_orgs.sort_values(ascending=True, inplace=True)

org_bar = px.bar(x = top20_orgs.values,
                 y = top20_orgs.index,
                 orientation='h',
                 color=top20_orgs.values,
                 color_continuous_scale=px.colors.sequential.haline,
                 title='Top 20 Research Institutions by Number of Prizes')

org_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='Institution',
                      coloraxis_showscale=False)
org_bar.show()
```

**Top Institutions:**
- **University of California** system leads with 40 prizes.
- **Harvard University** (29) and **Stanford University** (23) follow.
- **University of Chicago** has 20, **MIT** 21, **Cambridge** 18.

### Cities Where Discoveries Happen

We can also look at the cities where these organizations are located.

```python
top20_org_cities = df_data.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)

city_bar2 = px.bar(x = top20_org_cities.values,
                  y = top20_org_cities.index,
                  orientation='h',
                  color=top20_org_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Which Cities Do the Most Research?')

city_bar2.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City',
                       coloraxis_showscale=False)
city_bar2.show()
```

**Hotspots:**
- **Cambridge, MA** (home to Harvard and MIT) is the top city with 50 prizes.
- **New York, NY** comes second with 45.
- **London** leads in Europe with 27.

### Birth Cities of Laureates

Where are Nobel laureates born? This differs from where they do their research.

```python
top20_cities = df_data.birth_city.value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)

city_bar = px.bar(x=top20_cities.values,
                  y=top20_cities.index,
                  orientation='h',
                  color=top20_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Where were the Nobel Laureates Born?')

city_bar.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City of Birth',
                       coloraxis_showscale=False)
city_bar.show()
```

**Observations:**
- **New York** tops the list with 53 laureates.
- **Paris** follows with 26, then **London** with 19.
- **Vienna** has 14, a city of modest size but rich in cultural and scientific history.
- Among the top 5 birth cities, only New York is in the US; the others are European capitals (Paris, London, Vienna, Berlin). This contrasts with the research cities list, which is dominated by US academic hubs.

### Sunburst Chart: Country → City → Organization

To visualize the hierarchical relationship between country, city, and organization, we use a sunburst chart.

First, group the data by these three levels and count prizes.

```python
country_city_org = df_data.groupby(by=['organization_country', 
                                       'organization_city', 
                                       'organization_name'], as_index=False).agg({'prize': pd.Series.count})
```

Then create the sunburst.

```python
burst = px.sunburst(country_city_org, 
                    path=['organization_country', 'organization_city', 'organization_name'], 
                    values='prize',
                    title='Where do Discoveries Take Place?')

burst.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='City',
                    coloraxis_showscale=False)
burst.show()
```

**Interactive Insights:**
- The chart shows the relative contributions of each country, city, and institution.
- **France** is highly centralized: almost all prizes are associated with **Paris**.
- **Germany** is more decentralized, with discoveries spread across multiple cities (Munich, Heidelberg, Berlin, etc.).
- The **UK** is dominated by **Cambridge** and **London**.

---

## Age Analysis of Nobel Laureates

### Calculating Age at Award

We add a column `winning_age` by subtracting the birth year from the award year. Since we converted `birth_date` to datetime, we can extract the year.

```python
birth_years = df_data.birth_date.dt.year
df_data['winning_age'] = df_data.year - birth_years
```

### Oldest and Youngest Winners

```python
display(df_data.nlargest(n=1, columns='winning_age'))
display(df_data.nsmallest(n=1, columns='winning_age'))
```

- **Oldest:** **John Goodenough** (Chemistry 2019) at 97 years old.
- **Youngest:** **Malala Yousafzai** (Peace 2014) at 17 years old.

### Descriptive Statistics and Age Distribution

We use `.describe()` to get summary statistics and a histogram to visualize the distribution.

```python
df_data.winning_age.describe()
```

**Statistics:**
- Count: 934 (excluding organizations)
- Mean: ~59.95 years
- Std: 12.62 years
- Min: 17, Max: 97
- 25%: 51, 50%: 60, 75%: 69

Histogram with 30 bins:

```python
plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data,
             x=df_data.winning_age,
             bins=30)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')
plt.show()
```

The distribution is roughly normal, centered around 60, with a slight right skew (older winners).

### Age Trends Over Time

We use Seaborn's `regplot` with `lowess=True` to show a smoothed trend of winning age over the years.

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(data=df_data,
                x='year',
                y='winning_age',
                lowess=True, 
                scatter_kws = {'alpha': 0.4},
                line_kws={'color': 'black'})
plt.show()
```

**Trend:** The best-fit line (local regression) shows that the average age of Nobel laureates has increased over time. In the early 1900s, laureates were typically in their mid-50s; by 2020, the average age is approaching 70. This suggests that groundbreaking work is being recognized later in life, or that the prize is being awarded after a longer period of validation.

### Age Variation Across Categories

A box plot reveals differences in age distributions by category.

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data,
                x='category',
                y='winning_age')
plt.show()
```

**Observations:**
- **Peace** has the longest whiskers (wide age range) and a relatively high median.
- **Literature** also shows a wide spread and high median.
- **Physics** and **Chemistry** have tighter distributions and slightly lower medians.
- **Economics**, being newer, shows a more compact distribution.

We can also create the box plot using plotly for interactivity:

```python
box = px.box(df_data, 
             x='category', 
             y='winning_age',
             title='How old are the Winners?')
box.update_layout(xaxis_title='Category',
                  yaxis_title='Age at time of Award',
                  xaxis={'categoryorder':'mean ascending'})
box.show()
```

### Combined Trends with `lmplot`

To see how age trends differ by category over time, we use Seaborn's `lmplot` with the `row` parameter.

```python
with sns.axes_style('whitegrid'):
    sns.lmplot(data=df_data,
               x='year', 
               y='winning_age',
               row = 'category',
               lowess=True, 
               aspect=2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'})
plt.show()
```

**Category-Specific Trends:**
- **Physics, Chemistry, and Medicine** show a clear upward trend: winners are getting older.
- **Economics** (starting 1969) shows relative stability.
- **Peace** shows a **downward trend** in recent decades, meaning Peace Prize winners are getting younger. This is a striking divergence from the scientific categories.
- **Literature** shows a slight upward trend but with much variability.

This analysis demonstrates that a simple box plot can be misleading: while Peace has older winners overall, the trend over time is towards younger laureates. The `lmplot` reveals dynamics hidden in the aggregate.

Finally, we can overlay all categories on one chart using the `hue` parameter.

```python
with sns.axes_style("whitegrid"):
    sns.lmplot(data=df_data,
               x='year',
               y='winning_age',
               hue='category',
               lowess=True, 
               aspect=2,
               scatter_kws={'alpha': 0.5},
               line_kws={'linewidth': 5})
plt.show()
```

This makes it easy to compare the trends directly.

---

## Summary of Key Insights

- **Gender imbalance:** Only ~6.2% of Nobel laureates are women, with the lowest representation in Physics and Economics.
- **Repeat winners:** A handful of individuals and organizations have won multiple times.
- **Temporal trends:** The number of prizes per year has increased, prizes are more frequently shared, and winners are getting older, except in the Peace category.
- **Geographic dominance:** The US leads by a large margin, with Europe (especially UK, Germany, France) also strong. The US's rise began after WWII.
- **Research hubs:** Cambridge (MA), New York, and London are top cities. France is centralized in Paris, while Germany is more decentralized.
- **Age patterns:** Average age at award is ~60, but this has increased over time for sciences. Peace laureates are getting younger.

---

## Resources and References

-   [Plotly Documentation](https://plotly.com/python/)
-   [Seaborn Documentation](https://seaborn.pydata.org/)
-   [Matplotlib Documentation](https://matplotlib.org/)
-   [Pandas Documentation](https://pandas.pydata.org/)
-   [Original comic reference](https://www.smbc-comics.com/) (SMBC Comics)