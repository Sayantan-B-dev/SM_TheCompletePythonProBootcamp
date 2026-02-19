# Analyzing Nobel Prize Categories and Gender Distribution

## Overview

This section of the analysis focuses on basic categorical questions: the distribution of prizes by category, the representation of women among laureates, and identification of repeat winners. Visualizations are created using Plotly Express, a high-level interface for generating interactive charts.

The following tasks are addressed:

1. Formulating initial exploratory questions.
2. Creating a donut chart to visualize the gender split.
3. Identifying the first three female laureates.
4. Finding laureates who won the prize more than once.
5. Counting prizes per category and displaying with a bar chart.
6. Determining when the Economics prize was first awarded.
7. Splitting the category bar chart by gender to reveal differences.

---

## 1. Formulating Exploratory Questions

Before writing code, it is good practice to think about what the data might reveal. Based on the column names, some initial questions include:

- What percentage of Nobel laureates are women?
- How many prizes have been awarded in each category?
- Are there any individuals or organizations that received the prize more than once?
- How does gender representation vary across categories?
- When was the Economics prize introduced?

These questions guide the subsequent visualizations and analyses.

---

## 2. Gender Distribution: Donut Chart

### Data Preparation

The `sex` column contains three categories: `"Male"`, `"Female"`, and `NaN` (for organizations). To count how many prizes went to men versus women, we use `value_counts()` on the `sex` column. This automatically excludes NaN values.

```python
gender_counts = df_data.sex.value_counts()
print(gender_counts)
```

Typical output:
```
Male      876
Female     58
Name: sex, dtype: int64
```

### Creating the Donut Chart

Plotly Express provides a `pie` function that can create both pie and donut charts. Setting `hole` to a value between 0 and 1 creates a donut (0 for pie, 0.4 for a donut). The `labels` and `values` parameters define the slices.

```python
fig = px.pie(
    labels=gender_counts.index,
    values=gender_counts.values,
    names=gender_counts.index,
    title="Percentage of Male vs. Female Winners",
    hole=0.4
)
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
fig.show()
```

**Explanation**:
- `labels` and `names` are both set to the index (the gender categories) to properly label the slices.
- `hole=0.4` transforms the pie into a donut.
- `update_traces` adjusts the text: placed inside the slices, font size 15, showing percentages.
- The resulting interactive chart displays that only about **6.2%** of Nobel prizes (where the laureate is an individual) have been awarded to women.

---

## 3. First Three Female Nobel Laureates

### Filtering and Sorting

To find the earliest female winners, we filter for `sex == 'Female'` and sort by `year` ascending. Selecting the first three rows gives the answer.

```python
first_women = df_data[df_data.sex == 'Female'].sort_values('year', ascending=True)[:3]
first_women[['year', 'category', 'full_name', 'birth_country', 'organization_name']]
```

**Output** (example):

| year | category  | full_name                     | birth_country_current | organization_name |
|------|-----------|-------------------------------|-----------------------|-------------------|
| 1903 | Physics   | Marie Curie, née Sklodowska   | Poland                | NaN               |
| 1905 | Peace     | Bertha von Suttner            | Czech Republic        | NaN               |
| 1909 | Literature| Selma Lagerlöf                | Sweden                | NaN               |

**Observations**:
- Marie Curie won the Physics prize in 1903 (shared with her husband and Henri Becquerel).
- Bertha von Suttner, an Austrian pacifist, won the Peace prize in 1905.
- Selma Lagerlöf, the first female writer to win the Literature prize, received it in 1909.
- None of these early female winners were affiliated with a research organization at the time of the award (reflecting that Peace and Literature laureates often are not, and Curie’s affiliation was not recorded in this column).

---

## 4. Repeat Winners

### Detecting Multiple Wins

Some laureates have received the Nobel Prize more than once. We can identify them by looking for duplicate names in the `full_name` column. The `duplicated` method with `keep=False` marks all occurrences of duplicated names.

```python
is_duplicate = df_data.duplicated(subset=['full_name'], keep=False)
multiple_winners = df_data[is_duplicate]
print(f"There are {multiple_winners.full_name.nunique()} winners who received the prize more than once.")
```

**Output**: `There are 6 winners who received the prize more than once.`

### Viewing the Repeat Winners

We can inspect a subset of columns to see who they are and in which categories.

```python
cols = ['year', 'category', 'laureate_type', 'full_name']
multiple_winners[cols].sort_values(['full_name', 'year'])
```

The output reveals:

- **Marie Curie** (Physics 1903, Chemistry 1911)
- **Linus Pauling** (Chemistry 1954, Peace 1962)
- **John Bardeen** (Physics 1956, Physics 1972)
- **Frederick Sanger** (Chemistry 1958, Chemistry 1980)
- **International Committee of the Red Cross** (Peace 1917, 1944, 1963)
- **Office of the United Nations High Commissioner for Refugees** (Peace 1954, 1981)

Note that only four of the six are individuals; two are organizations. This shows that while rare, it is possible to be recognized multiple times, either in the same field or different ones.

### Alternative Approach Using `groupby`

An alternative method uses `groupby` to filter groups with count >= 2:

```python
multiple_winners = df_data.groupby('full_name').filter(lambda x: x['year'].count() >= 2)
```

This yields the same result.

---

## 5. Number of Prizes per Category

### Counting Categories

First, we check how many distinct categories exist:

```python
df_data.category.nunique()
```
**Output**: `6`

### Bar Chart of Prize Counts

To visualize the distribution, we compute the frequency of each category and create a vertical bar chart.

```python
prizes_per_category = df_data.category.value_counts()
fig = px.bar(
    x=prizes_per_category.index,
    y=prizes_per_category.values,
    color=prizes_per_category.values,
    color_continuous_scale='Aggrnyl',
    title='Number of Prizes Awarded per Category'
)
fig.update_layout(
    xaxis_title='Nobel Prize Category',
    yaxis_title='Number of Prizes',
    coloraxis_showscale=False
)
fig.show()
```

**Explanation**:
- `color=prizes_per_category.values` maps the bar colors to the count values, using the `Aggrnyl` color scale.
- `coloraxis_showscale=False` hides the color bar because it is redundant here.
- The chart shows that **Medicine** has the most prizes (222), followed closely by Physics (216) and Chemistry (186). Economics has the fewest (86), reflecting its later establishment.

### Why Does Economics Have Fewer Prizes?

Looking at the earliest Economics laureates:

```python
df_data[df_data.category == 'Economics'].sort_values('year').head(3)
```

| year | category  | full_name       | motivation... |
|------|-----------|-----------------|---------------|
| 1969 | Economics | Jan Tinbergen   | ...           |
| 1969 | Economics | Ragnar Frisch   | ...           |
| 1970 | Economics | Paul Samuelson  | ...           |

The first Economics prize was awarded in **1969**, nearly 70 years after the other categories. This explains its lower total count.

---

## 6. Gender Breakdown by Category

### Grouping Data by Category and Sex

To see how many men and women have won in each category, we group by both `category` and `sex` and count the number of prizes. We use `agg` with `pd.Series.count` on the `prize` column (any column would work since we just need counts).

```python
cat_gender = df_data.groupby(['category', 'sex'], as_index=False).agg({'prize': 'count'})
cat_gender.sort_values('prize', ascending=False, inplace=True)
```

The resulting DataFrame has three columns: `category`, `sex`, and `prize` (the count). Sorting by prize helps to see the largest groups first.

### Stacked Bar Chart

We can now create a bar chart where the color distinguishes gender. Because the x-axis is category, the bars will be grouped by gender within each category.

```python
fig = px.bar(
    x=cat_gender.category,
    y=cat_gender.prize,
    color=cat_gender.sex,
    title='Number of Prizes Awarded per Category split by Men and Women'
)
fig.update_layout(
    xaxis_title='Nobel Prize Category',
    yaxis_title='Number of Prizes'
)
fig.show()
```

**Observations**:
- In **Physics**, women have won only 4 prizes compared to 212 for men.
- In **Chemistry**, women have 7 prizes; men 179.
- In **Medicine**, women have 12; men 210.
- The gap is narrower in **Literature** (16 women, 101 men) and **Peace** (17 women, 90 men).
- **Economics** has the fewest women (only 2) and 84 men.

This split bar chart reveals that while overall female representation is low, it varies considerably by discipline, with Literature and Peace being relatively more inclusive.

---

## Summary of Findings

- Only **6.2%** of individual Nobel laureates are women.
- The first three female winners were Marie Curie (Physics 1903), Bertha von Suttner (Peace 1905), and Selma Lagerlöf (Literature 1909).
- Six laureates (four individuals, two organizations) have won the prize more than once.
- Medicine is the most awarded category, Economics the least, due to its later start in 1969.
- Gender imbalance persists across all categories but is most extreme in Physics, Chemistry, and Economics, and least in Literature and Peace.
