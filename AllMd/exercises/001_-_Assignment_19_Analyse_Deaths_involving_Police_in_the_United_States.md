# Complete Documentation: Analysis of Fatal Police Shootings with US Census Data

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup and Import Statements](#setup-and-import-statements)
3. [Loading the Data](#loading-the-data)
4. [Preliminary Data Exploration](#preliminary-data-exploration)
5. [Data Cleaning](#data-cleaning)
6. [Charting Poverty Rate by State](#charting-poverty-rate-by-state)
7. [Charting High School Graduation Rate by State](#charting-high-school-graduation-rate-by-state)
8. [Relationship Between Poverty and Education](#relationship-between-poverty-and-education)
9. [Racial Demographics by State](#racial-demographics-by-state)
10. [Analysis of Fatalities Data](#analysis-of-fatalities-data)
    - 10.1 Race Distribution (Donut Chart)
    - 10.2 Gender Distribution
    - 10.3 Age and Manner of Death (Box Plot)
    - 10.4 Armed Status
    - 10.5 Age Distribution (Histogram/KDE)
    - 10.6 Age by Race (KDE)
    - 10.7 Mental Illness
    - 10.8 Top Cities by Killings
    - 10.9 Rate of Death by Race (City-Level)
    - 10.10 Choropleth Map by State
    - 10.11 Time Series Analysis
11. [Epilogue](#epilogue)
12. [Appendix: Detailed Function Reference](#appendix-detailed-function-reference)

---

## Project Overview

This project combines data from The Washington Post's database of fatal police shootings (since 2015) with US Census data to explore social and economic trends related to police killings. The analysis uses Python with pandas, plotly, matplotlib, and seaborn. The goal is to understand patterns in victim demographics, geographical distribution, and correlation with poverty, education, and racial demographics.

### Datasets
- **Deaths_by_Police_US.csv**: Fatal police shootings (id, name, date, manner_of_death, armed, age, gender, race, city, state, signs_of_mental_illness, threat_level, flee, body_camera)
- **Median_Household_Income_2015.csv**: City-level median income
- **Pct_People_Below_Poverty_Level.csv**: City-level poverty rate
- **Pct_Over_25_Completed_High_School.csv**: City-level high school graduation rate among adults 25+
- **Share_of_Race_By_City.csv**: City-level racial composition percentages

All census data is from 2015.

---

## Setup and Import Statements

```python
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

pd.options.display.float_format = '{:,.2f}'.format
```

**Explanation**:
- `numpy`: Provides numerical operations (not heavily used but imported for compatibility).
- `pandas`: Core data manipulation library. Used for DataFrames, reading CSV, grouping, merging, etc.
- `plotly.express`: High-level interface for creating interactive plots (bar, line, pie, choropleth).
- `matplotlib.pyplot`: Base plotting library; used for customizing plots and creating figures.
- `seaborn`: Statistical data visualization built on matplotlib; used for joint plots, box plots, KDE, regression.
- `Counter`: From collections; can count hashable objects (optional but imported).
- `pd.options.display.float_format`: Sets display format for floats in pandas to two decimal places.

---

## Loading the Data

```python
df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")
```

**`pd.read_csv`**:
- **Purpose**: Reads a comma-separated values file into a pandas DataFrame.
- **Parameters**:
  - `filepath`: Path to CSV file.
  - `encoding`: Specifies character encoding (here `windows-1252` to handle special characters).
- **Returns**: DataFrame.

**Example**:
```python
df_fatalities.head()
```
Output (first few rows):
| id | name          | date     | manner_of_death | armed | age | gender | race | city     | state | signs_of_mental_illness | threat_level | flee         | body_camera |
|----|---------------|----------|-----------------|-------|-----|--------|------|----------|-------|-------------------------|--------------|--------------|-------------|
| 3  | Tim Elliot    | 02/01/15 | shot            | gun   | 53  | M      | A    | Shelton  | WA    | TRUE                    | attack       | Not fleeing  | FALSE       |
| 4  | Lewis Lee Lembke| 02/01/15| shot           | gun   | 47  | M      | W    | Aloha    | OR    | FALSE                   | attack       | Not fleeing  | FALSE       |
...

---

## Preliminary Data Exploration

We examine the shape, columns, missing values, and duplicates.

```python
print("df_hh_income shape:", df_hh_income.shape)
print("df_pct_poverty shape:", df_pct_poverty.shape)
...
```

**`.shape`** attribute: Returns a tuple (number of rows, number of columns).

**`.columns.tolist()`**: Returns list of column names.

**`.isnull().sum()`**: Counts missing (NaN) values per column.

**`.duplicated().sum()`**: Counts duplicate rows.

**Example Output**:
```
df_hh_income shape: (29331, 3)
df_pct_poverty shape: (29331, 3)
df_pct_completed_hs shape: (29331, 3)
df_share_race_city shape: (29331, 6)
df_fatalities shape: (5116, 14)
```

**Observations**:
- Census data has ~29k cities/towns.
- Fatalities data has ~5k records (from 2015 to present).

---

## Data Cleaning

We handle missing values and prepare for analysis.

```python
# For race shares, fill NaN with 0 (no population of that race)
df_share_race_city.fillna(0, inplace=True)

# Drop rows with missing income, poverty, or HS rate (for state aggregation)
df_hh_income.dropna(subset=['Median Income'], inplace=True)
df_pct_poverty.dropna(subset=['poverty_rate'], inplace=True)
df_pct_completed_hs.dropna(subset=['percent_completed_hs'], inplace=True)

# For fatalities, fill missing race with 'Unknown' and drop rows missing age/gender
df_fatalities['race'].fillna('Unknown', inplace=True)
df_fatalities.dropna(subset=['age', 'gender'], inplace=True)
```

**Methods**:
- **`fillna(value, inplace=True)`**: Replaces NaN with specified value (0) in the DataFrame (modifies original).
- **`dropna(subset=[...])`**: Removes rows where any of the specified columns have NaN. `inplace=True` modifies original.
- **Why**: For census, missing race likely means zero population. For fatalities, age and gender are essential; missing race is kept as 'Unknown'.

**After cleaning**:
```python
df_fatalities.isnull().sum()
```
Output:
```
id                         0
name                       0
date                       0
manner_of_death            0
armed                    220
age                        0
gender                     0
race                       0
city                       0
state                      0
signs_of_mental_illness    0
threat_level             260
flee                     377
body_camera              106
dtype: int64
```
(Some columns still have missing values, but they are not critical for our analysis.)

---

## Charting Poverty Rate by State

**Goal**: Create a bar chart of average poverty rate per state, ranked highest to lowest.

```python
# Calculate average poverty rate by state
poverty_by_state = df_pct_poverty.groupby('Geographic Area')['poverty_rate'].mean().sort_values(ascending=False).reset_index()
poverty_by_state.columns = ['state', 'avg_poverty_rate']
```

**Step-by-step**:
1. **`df_pct_poverty.groupby('Geographic Area')`**: Groups the DataFrame by the state column (Geographic Area). Returns a `DataFrameGroupBy` object.
2. **`['poverty_rate'].mean()`**: Selects the 'poverty_rate' column and computes the mean for each group. Returns a Series with state as index and average poverty as values.
3. **`.sort_values(ascending=False)`**: Sorts the Series in descending order (highest poverty first).
4. **`.reset_index()`**: Converts the Series back to a DataFrame, with state as a column and the average as another column.
5. **Renaming columns**: `.columns = ['state', 'avg_poverty_rate']` for clarity.

**Plotting with Plotly**:
```python
fig = px.bar(poverty_by_state, x='state', y='avg_poverty_rate', 
             title='Average Poverty Rate by US State (2015)',
             labels={'state': 'State', 'avg_poverty_rate': 'Poverty Rate (%)'})
fig.show()
```
**`px.bar`**:
- **Parameters**:
  - `data_frame`: DataFrame (poverty_by_state).
  - `x`: Column name for x-axis (state).
  - `y`: Column name for y-axis (avg_poverty_rate).
  - `title`: Chart title.
  - `labels`: Dictionary to rename axes in hover and labels.
- **Returns**: A Plotly Figure object. Calling `.show()` displays it.

**Output**: Interactive bar chart. Highest poverty state: Mississippi (~22%), lowest: New Hampshire (~9%).

**Alternative with matplotlib**:
```python
plt.figure(figsize=(12,6))
plt.bar(poverty_by_state['state'], poverty_by_state['avg_poverty_rate'])
plt.xticks(rotation=90)
plt.xlabel('State')
plt.ylabel('Poverty Rate (%)')
plt.title('Average Poverty Rate by US State (2015)')
plt.tight_layout()
plt.show()
```
**`plt.bar`** creates a static bar chart. `plt.xticks(rotation=90)` rotates labels to avoid overlap. `plt.tight_layout()` adjusts spacing.

---

## Charting High School Graduation Rate by State

Similar process using `df_pct_completed_hs`.

```python
hs_by_state = df_pct_completed_hs.groupby('Geographic Area')['percent_completed_hs'].mean().sort_values().reset_index()
hs_by_state.columns = ['state', 'avg_hs_rate']
```

**`sort_values()`** defaults to ascending (lowest first). Then plot with `px.bar`.

**Output**: Lowest HS graduation: Texas (~80%), highest: North Dakota (~92%).

---

## Relationship Between Poverty and Education

### Dual-Axis Line Chart

```python
merged = pd.merge(poverty_by_state, hs_by_state, on='state')
merged = merged.sort_values('state')  # or sort by poverty

fig, ax1 = plt.subplots(figsize=(14,6))
ax1.set_xlabel('State')
ax1.set_ylabel('Poverty Rate (%)', color='tab:red')
ax1.plot(merged['state'], merged['avg_poverty_rate'], color='tab:red', marker='o', label='Poverty')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.set_xticklabels(merged['state'], rotation=90)

ax2 = ax1.twinx()
ax2.set_ylabel('HS Graduation Rate (%)', color='tab:blue')
ax2.plot(merged['state'], merged['avg_hs_rate'], color='tab:blue', marker='s', label='HS Graduation')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title('Poverty Rate vs High School Graduation Rate by State')
fig.tight_layout()
plt.show()
```

**Explanation**:
- **`pd.merge(poverty_by_state, hs_by_state, on='state')`**: Joins two DataFrames on the 'state' column. Default is inner join (keeps only states present in both).
- **`plt.subplots()`**: Creates a figure and a single subplot (axes). Returns `(fig, ax)`.
- **`ax1.plot()`**: Plots line on first axis.
- **`ax1.twinx()`**: Creates a second y-axis sharing the same x-axis.
- **`ax2.plot()`**: Plots on second axis.
- **`tick_params()`**: Sets color of tick labels.
- **`set_xticklabels()`**: Assigns rotated state names.

### Jointplot with Seaborn

```python
sns.jointplot(data=merged, x='avg_poverty_rate', y='avg_hs_rate', kind='scatter', marginal_kws=dict(bins=10))
plt.suptitle('Poverty vs HS Graduation Rate (Scatter with Marginals)', y=1.02)
plt.show()
```
**`sns.jointplot`**:
- **Parameters**:
  - `data`: DataFrame.
  - `x`, `y`: Column names.
  - `kind`: Type of plot ('scatter', 'kde', 'hex', etc.).
  - `marginal_kws`: Dictionary of keyword arguments for marginal plots (here, number of bins).
- **Returns**: A `JointGrid` object. The plot includes a scatter plot in the center and histograms (or KDE) on margins.

**KDE version**:
```python
sns.jointplot(data=merged, x='avg_poverty_rate', y='avg_hs_rate', kind='kde', fill=True)
```

### Regression Plot

```python
sns.lmplot(data=merged, x='avg_poverty_rate', y='avg_hs_rate')
plt.xlabel('Average Poverty Rate (%)')
plt.ylabel('Average HS Graduation Rate (%)')
plt.title('Linear Regression: Poverty vs HS Graduation')
plt.show()
```
**`sns.lmplot`**:
- Plots scatter points and fits a linear regression line with confidence interval.
- Returns a `FacetGrid` object. Use `plt.xlabel`/`ylabel` to label.

---

## Racial Demographics by State

We average city-level racial percentages to get state-level estimates.

```python
race_cols = ['share_white', 'share_black', 'share_native_american', 'share_asian', 'share_hispanic']
race_by_state = df_share_race_city.groupby('Geographic area')[race_cols].mean().reset_index()
race_by_state = race_by_state.rename(columns={'Geographic area': 'state'})
```

**`groupby` + mean** on multiple columns gives average share per state.

**Melt for stacked bar**:
```python
race_melted = race_by_state.melt(id_vars='state', value_vars=race_cols, 
                                  var_name='race', value_name='percentage')
```
**`melt`**:
- **Purpose**: Unpivots DataFrame from wide to long format.
- **Parameters**:
  - `id_vars`: Columns to keep as identifiers.
  - `value_vars`: Columns to unpivot.
  - `var_name`: Name for the new variable column (holds original column names).
  - `value_name`: Name for the new value column.
- **Returns**: Long-format DataFrame.

**Plotly stacked bar**:
```python
fig = px.bar(race_melted, x='state', y='percentage', color='race', 
             title='Racial Makeup by State (Average of Cities)',
             labels={'percentage': 'Percentage', 'state': 'State'})
fig.show()
```
**`color='race'`** splits bars by race, creating stacked bars automatically.

---

## Analysis of Fatalities Data

### 10.1 Race Distribution (Donut Chart)

```python
race_counts = df_fatalities['race'].value_counts().reset_index()
race_counts.columns = ['race', 'count']
fig = px.pie(race_counts, values='count', names='race', title='Police Killings by Race',
             hole=0.4)
fig.show()
```
**`value_counts()`**: Returns Series with counts of unique values.
**`px.pie`**:
- `values`: Numerical column for slice sizes.
- `names`: Column for slice labels.
- `hole`: Size of hole (0.4 creates a donut).

**Output**: Largest slice is White (W), then Black (B), Hispanic (H), etc.

### 10.2 Gender Distribution

```python
gender_counts = df_fatalities['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']
fig = px.bar(gender_counts, x='gender', y='count', 
             title='Police Killings by Gender')
fig.show()
```
Shows that males are killed far more often (~95%).

### 10.3 Age and Manner of Death (Box Plot)

```python
plt.figure(figsize=(12,6))
sns.boxplot(data=df_fatalities, x='manner_of_death', y='age', hue='gender')
plt.title('Age Distribution by Manner of Death and Gender')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```
**`sns.boxplot`**:
- `x`: Categorical column for grouping boxes.
- `y`: Numerical column.
- `hue`: Additional categorical grouping (gender).
- Box shows median, quartiles, outliers.

### 10.4 Armed Status

```python
armed_status = df_fatalities['armed'].value_counts()
total = len(df_fatalities)
armed_percent = (armed_status / total * 100).round(2)
print(armed_percent)

# Top 10 weapons
top_weapons = armed_status.head(10).reset_index()
top_weapons.columns = ['weapon', 'count']
fig = px.bar(top_weapons, x='weapon', y='count', title='Top 10 Weapons Carried by Victims')
fig.show()

# Gun vs unarmed
gun_count = armed_status.get('gun', 0)
unarmed_count = armed_status.get('unarmed', 0)
print(f"Armed with gun: {gun_count} ({gun_count/total*100:.2f}%)")
print(f"Unarmed: {unarmed_count} ({unarmed_count/total*100:.2f}%)")
```
**`value_counts()`** returns counts for each unique value in 'armed'. We can then extract specific categories.

### 10.5 Age Distribution (Histogram/KDE)

```python
plt.figure(figsize=(10,6))
sns.histplot(df_fatalities['age'], bins=30, kde=True)
plt.title('Distribution of Ages of People Killed by Police')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()
```
**`sns.histplot`**:
- `bins`: Number of bins.
- `kde=True`: Overlays kernel density estimate.

### 10.6 Age by Race (KDE)

```python
plt.figure(figsize=(12,8))
for race in df_fatalities['race'].unique():
    subset = df_fatalities[df_fatalities['race'] == race]
    sns.kdeplot(subset['age'], label=race, bw_adjust=0.5)
plt.title('Age Distribution by Race')
plt.xlabel('Age')
plt.legend()
plt.show()
```
**`sns.kdeplot`** plots density for each race. `bw_adjust` controls bandwidth.

### 10.7 Mental Illness

```python
mental_illness_counts = df_fatalities['signs_of_mental_illness'].value_counts()
total = len(df_fatalities)
mental_percent = (mental_illness_counts.get(True, 0) / total) * 100
print(f"Percentage of victims with signs of mental illness: {mental_percent:.2f}%")

fig = px.pie(names=['No mental illness', 'Mental illness'], 
             values=[mental_illness_counts.get(False,0), mental_illness_counts.get(True,0)],
             title='Mental Illness Among Victims')
fig.show()
```
**`get(key, default)`** safely retrieves count for True/False.

### 10.8 Top Cities by Killings

```python
city_counts = df_fatalities['city'].value_counts().head(10).reset_index()
city_counts.columns = ['city', 'count']
fig = px.bar(city_counts, x='count', y='city', orientation='h',
             title='Top 10 Cities with Most Police Killings')
fig.show()
```
**`orientation='h'`** makes horizontal bars for easier city name reading.

**Output**: Los Angeles, Phoenix, Houston, etc.

### 10.9 Rate of Death by Race (City-Level)

This is the most complex part, requiring merging fatalities with census data at city level. The steps are split into two cells.

**Cell 1: Prepare Data**
```python
top_cities = city_counts['city'].tolist()
top_cities_fatalities = df_fatalities[df_fatalities['city'].isin(top_cities)]

victim_race_by_city = top_cities_fatalities.groupby(['city', 'race']).size().reset_index(name='victim_count')

def clean_city_name(city):
    import re
    suffixes = r'\s+(city|town|village|cdp|census designated place|municipality|borough)$'
    cleaned = re.sub(suffixes, '', city, flags=re.IGNORECASE).strip()
    return cleaned

df_fatalities['city_clean'] = df_fatalities['city'].apply(clean_city_name)
df_share_race_city['city_clean'] = df_share_race_city['City'].apply(clean_city_name)
df_share_race_city['state'] = df_share_race_city['Geographic area']

top_cities_clean = [clean_city_name(c) for c in top_cities]
top_cities_census = df_share_race_city[df_share_race_city['city_clean'].isin(top_cities_clean)]

total_victims_per_city = top_cities_fatalities.groupby('city').size().reset_index(name='total_victims')
victim_race_pct = pd.merge(victim_race_by_city, total_victims_per_city, on='city')
victim_race_pct['victim_pct'] = victim_race_pct['victim_count'] / victim_race_pct['total_victims'] * 100

city_to_state = df_fatalities[df_fatalities['city'].isin(top_cities)][['city', 'state']].drop_duplicates().set_index('city')['state'].to_dict()
victim_race_pct['state'] = victim_race_pct['city'].map(city_to_state)
victim_race_pct['city_clean'] = victim_race_pct['city'].apply(clean_city_name)
```

**Key Functions**:
- **`.isin()`**: Filters DataFrame to rows where column value is in a list.
- **`re.sub(pattern, replacement, string)`**: Uses regex to remove suffixes. `flags=re.IGNORECASE` makes it case-insensitive.
- **`.apply(function)`**: Applies a function to each element of a Series.
- **`pd.merge()`**: Joins DataFrames.
- **`to_dict()`**: Converts a Series to a dictionary.

**Cell 2: Merge and Display**
```python
race_cols = ['share_white', 'share_black', 'share_native_american', 'share_asian', 'share_hispanic']
census_race = top_cities_census.groupby(['city_clean', 'state'])[race_cols].mean().reset_index()
census_race_melted = census_race.melt(id_vars=['city_clean', 'state'], 
                                      var_name='race_census', value_name='population_pct')
race_map = {'share_white': 'W', 'share_black': 'B', 'share_hispanic': 'H', 
            'share_asian': 'A', 'share_native_american': 'N'}
census_race_melted['race'] = census_race_melted['race_census'].map(race_map)

comparison = pd.merge(victim_race_pct, census_race_melted, 
                      on=['city_clean', 'state', 'race'], how='outer')
comparison = comparison[['city', 'race', 'victim_pct', 'population_pct', 'state']].dropna()

for city in comparison['city'].unique():
    city_data = comparison[comparison['city'] == city]
    print(f"\n{city}:")
    display_df = city_data[['race', 'victim_pct', 'population_pct']].round(2)
    print(display_df.to_string(index=False))
```

**`map(race_map)`**: Replaces census race names with fatality race codes. `how='outer'` keeps all rows even if no match. `.dropna()` removes rows missing population data.

**Output Example**:
```
Los Angeles:
 race  victim_pct  population_pct
    B       30.00            9.20
    H       45.00           48.50
    W       20.00           28.30
```

### 10.10 Choropleth Map by State

```python
state_killings = df_fatalities['state'].value_counts().reset_index()
state_killings.columns = ['state', 'killings']

fig = px.choropleth(state_killings, locations='state', locationmode='USA-states', color='killings',
                     scope='usa', title='Police Killings by State',
                     color_continuous_scale='Reds')
fig.show()
```
**`px.choropleth`**:
- `locations`: Column with state codes.
- `locationmode='USA-states'`: Interprets locations as US state abbreviations.
- `color`: Column determining color intensity.
- `scope='usa'': Restricts map to USA.
- `color_continuous_scale`: Color palette.

### 10.11 Time Series Analysis

**Cell 1: Convert Date**
```python
df_fatalities['date'] = pd.to_datetime(df_fatalities['date'])
df_fatalities['year'] = df_fatalities['date'].dt.year
df_fatalities['month'] = df_fatalities['date'].dt.to_period('M')
```
**`pd.to_datetime`**: Converts string to datetime. `.dt` accessor extracts components. `.to_period('M')` converts to monthly period.

**Cell 2: Monthly Counts and Line Plot**
```python
monthly_counts = df_fatalities.groupby('month').size().reset_index(name='count')
monthly_counts['month'] = monthly_counts['month'].astype(str)
fig = px.line(monthly_counts, x='month', y='count', title='Police Killings Over Time (Monthly)')
fig.show()
```
**`.astype(str)`** ensures x-axis is treated as categorical/string.

**Cell 3: Yearly Bar Plot**
```python
yearly_counts = df_fatalities.groupby('year').size().reset_index(name='count')
fig = px.bar(yearly_counts, x='year', y='count', title='Police Killings by Year')
fig.show()
```

**Cell 4: Rolling Average**
```python
monthly_counts['rolling_avg'] = monthly_counts['count'].rolling(window=6).mean()
```
**`.rolling(window=6).mean()`**: Computes 6-month moving average.

**Cell 5: Plot with Rolling Average**
```python
fig = px.line(monthly_counts, x='month', y=['count', 'rolling_avg'],
              title='Monthly Killings with 6-Month Rolling Average')
fig.show()
```

---

## Epilogue

```python
print("Read the Washington Post analysis at: https://www.washingtonpost.com/graphics/investigations/police-shootings-database/")
```

---

## Appendix: Detailed Function Reference

This appendix provides a comprehensive list of every function/method used, with description, parameters, return value, and example.

### pandas Functions

| Function/Method | Description | Key Parameters | Returns | Example |
|----------------|-------------|----------------|---------|---------|
| `pd.read_csv()` | Read CSV file | `filepath`, `encoding` | DataFrame | `pd.read_csv('data.csv')` |
| `df.shape` | Get dimensions | - | Tuple (rows, cols) | `df.shape` → (5000,14) |
| `df.columns` | Get column names | - | Index | `df.columns` |
| `df.isnull().sum()` | Count missing per column | - | Series | `df.isnull().sum()` |
| `df.duplicated().sum()` | Count duplicate rows | - | int | `df.duplicated().sum()` |
| `df.fillna(value)` | Replace NaN | `value`, `inplace` | DataFrame or None | `df.fillna(0, inplace=True)` |
| `df.dropna()` | Drop missing rows | `subset`, `inplace` | DataFrame or None | `df.dropna(subset=['age'])` |
| `df.groupby(by)` | Group data | Column name(s) | DataFrameGroupBy | `df.groupby('state')` |
| `Series.mean()` | Compute mean of group | - | Series | `grouped['col'].mean()` |
| `Series.sort_values()` | Sort series | `ascending` | Series | `series.sort_values(ascending=False)` |
| `Series.reset_index()` | Reset index to columns | - | DataFrame | `series.reset_index()` |
| `pd.merge(left, right, on)` | Merge DataFrames | `left`, `right`, `on`, `how` | DataFrame | `pd.merge(df1, df2, on='state')` |
| `df.value_counts()` | Count unique values | - | Series | `df['race'].value_counts()` |
| `df.melt()` | Unpivot wide to long | `id_vars`, `value_vars`, `var_name`, `value_name` | DataFrame | `df.melt(id_vars='state', value_vars=['col1','col2'])` |
| `Series.apply(func)` | Apply function element-wise | function | Series | `df['city'].apply(clean_city)` |
| `Series.map(dict)` | Map values using dict | mapping dict | Series | `series.map({'A':1, 'B':2})` |
| `df.rename(columns=dict)` | Rename columns | `columns` dict | DataFrame | `df.rename(columns={'old':'new'})` |
| `df.rolling(window).mean()` | Rolling window mean | `window` | Rolling object then Series | `df['count'].rolling(6).mean()` |
| `pd.to_datetime()` | Convert to datetime | - | DatetimeIndex | `pd.to_datetime(df['date'])` |
| `dt.year` / `dt.month` | Extract datetime components | - | Series | `df['date'].dt.year` |
| `dt.to_period(freq)` | Convert to period | freq string | PeriodIndex | `df['date'].dt.to_period('M')` |
| `Series.astype(str)` | Convert to string | - | Series | `series.astype(str)` |

### Plotly Express Functions

| Function | Description | Key Parameters | Returns | Example |
|----------|-------------|----------------|---------|---------|
| `px.bar()` | Create bar chart | `x`, `y`, `color`, `title`, `labels`, `orientation` | Figure | `px.bar(df, x='state', y='rate')` |
| `px.pie()` | Create pie/donut chart | `values`, `names`, `hole`, `title` | Figure | `px.pie(df, values='count', names='race', hole=0.4)` |
| `px.line()` | Create line chart | `x`, `y`, `title` | Figure | `px.line(df, x='month', y='count')` |
| `px.choropleth()` | Create choropleth map | `locations`, `locationmode`, `color`, `scope`, `color_continuous_scale` | Figure | `px.choropleth(df, locations='state', locationmode='USA-states', color='killings')` |

### Matplotlib Functions

| Function | Description | Key Parameters | Returns | Example |
|----------|-------------|----------------|---------|---------|
| `plt.figure()` | Create new figure | `figsize` | Figure | `plt.figure(figsize=(10,6))` |
| `plt.subplots()` | Create figure and axes | `nrows`, `ncols`, `figsize` | (fig, ax) | `fig, ax = plt.subplots()` |
| `ax.plot()` | Line plot on axes | x, y, `color`, `marker`, `label` | None | `ax.plot(x, y, color='red')` |
| `ax.bar()` | Bar plot on axes | x, height | None | `ax.bar(x, y)` |
| `ax.twinx()` | Create twin axes sharing x | - | Axes | `ax2 = ax.twinx()` |
| `ax.set_xlabel()`, `ax.set_ylabel()` | Set axis labels | label string | None | `ax.set_xlabel('State')` |
| `ax.tick_params()` | Customize ticks | `axis`, `labelcolor`, `rotation` | None | `ax.tick_params(axis='x', rotation=90)` |
| `ax.set_xticklabels()` | Set custom tick labels | labels, rotation | None | `ax.set_xticklabels(states, rotation=90)` |
| `plt.title()` | Set title | string | None | `plt.title('My Plot')` |
| `plt.legend()` | Show legend | - | None | `plt.legend()` |
| `plt.tight_layout()` | Adjust spacing | - | None | `plt.tight_layout()` |
| `plt.show()` | Display plot | - | None | `plt.show()` |

### Seaborn Functions

| Function | Description | Key Parameters | Returns | Example |
|----------|-------------|----------------|---------|---------|
| `sns.jointplot()` | Scatter with marginal distributions | `data`, `x`, `y`, `kind`, `marginal_kws` | JointGrid | `sns.jointplot(data=df, x='a', y='b', kind='scatter')` |
| `sns.lmplot()` | Scatter with regression line | `data`, `x`, `y` | FacetGrid | `sns.lmplot(data=df, x='a', y='b')` |
| `sns.boxplot()` | Box plot | `data`, `x`, `y`, `hue` | Axes | `sns.boxplot(data=df, x='cat', y='num')` |
| `sns.histplot()` | Histogram with optional KDE | `data`, `bins`, `kde` | Axes | `sns.histplot(df['age'], bins=30, kde=True)` |
| `sns.kdeplot()` | Kernel density estimate | `data`, `label`, `bw_adjust` | Axes | `sns.kdeplot(df['age'], label='group')` |

### Python Built-in / Other

| Function | Description | Key Parameters | Returns | Example |
|----------|-------------|----------------|---------|---------|
| `len()` | Get length | object | int | `len(df)` |
| `print()` | Print to console | objects | None | `print("Hello")` |
| `re.sub(pattern, repl, string)` | Regex substitution | pattern, replacement, string, flags | string | `re.sub(r'\s+city', '', city, flags=re.I)` |
| `list.tolist()` | Convert to list | - | list | `series.tolist()` |
| `set()` | Create set | iterable | set | `set(list1) & set(list2)` for intersection |
| `dict.get(key, default)` | Get value with fallback | key, default | value | `counts.get('gun', 0)` |

---

## Complete Algorithm Walkthrough

1. **Load data** → `pd.read_csv()`
2. **Initial exploration** → `.shape`, `.columns`, `.isnull().sum()`, `.duplicated().sum()`
3. **Clean data** → `.fillna()`, `.dropna()`
4. **Poverty by state** → `.groupby()`, `.mean()`, `.sort_values()`, `px.bar()`
5. **HS graduation by state** → same as above
6. **Merge poverty & HS** → `pd.merge()`, plot with `plt.subplots()` and twin axes
7. **Jointplot** → `sns.jointplot()` (scatter + KDE)
8. **Regression** → `sns.lmplot()`
9. **Racial demographics** → `.groupby().mean()`, `.melt()`, `px.bar(color=...)`
10. **Fatalities race donut** → `.value_counts()`, `px.pie(hole=0.4)`
11. **Gender bar** → `.value_counts()`, `px.bar()`
12. **Box plot age vs manner** → `sns.boxplot(hue='gender')`
13. **Armed status** → `.value_counts()`, extract gun/unarmed, `px.bar()`
14. **Age distribution** → `sns.histplot(kde=True)`
15. **Age by race KDE** → loop over unique races, `sns.kdeplot()`
16. **Mental illness pie** → `.value_counts()`, `px.pie()`
17. **Top cities** → `.value_counts().head(10)`, `px.bar(orientation='h')`
18. **Rate of death by race** (complex):
    - Get top cities list.
    - Filter fatalities to those cities.
    - Count victims by city and race.
    - Clean city names (regex).
    - Filter census to those cities (cleaned).
    - Compute victim percentages.
    - Map city to state.
    - Prepare census race percentages, melt, map race codes.
    - Merge on cleaned city, state, race.
    - Display comparison.
19. **Choropleth map** → `px.choropleth(locationmode='USA-states')`
20. **Time series**:
    - Convert date → `pd.to_datetime()`
    - Extract year/month → `.dt.year`, `.dt.to_period('M')`
    - Group by month, count, plot `px.line()`
    - Group by year, count, plot `px.bar()`
    - Compute rolling average → `.rolling().mean()`
    - Plot with `px.line(y=['count','rolling_avg'])`
21. **Epilogue** → print link

---
