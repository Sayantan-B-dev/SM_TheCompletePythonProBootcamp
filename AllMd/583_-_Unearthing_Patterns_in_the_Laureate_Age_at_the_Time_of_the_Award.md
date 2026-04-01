# Analysis of Laureate Age at the Time of Award

This section investigates the age of Nobel laureates when they received the prize. The analysis includes calculating the age, identifying extremes, examining the overall distribution, and exploring how age varies by category and over time. Both descriptive statistics and visualizations are used to uncover patterns.

---

## 1. Calculating the Winning Age

The `birth_date` column was previously converted to datetime. To compute the age at the time of the award, we subtract the birth year from the award year.

```python
# Extract birth year from the datetime column
birth_years = df_data.birth_date.dt.year

# Calculate age at the time of the award
df_data['winning_age'] = df_data.year - birth_years
```

- `birth_years` is a Series of integers (or NaN for organizations).
- The new column `winning_age` contains floating‑point numbers (ages in years).

**Note**: For individuals with unknown exact birth dates (three cases, substituted with July 2), the calculated age is approximate.

---

## 2. Oldest and Youngest Winners

We use `nlargest` and `nsmallest` to find the extremes.

```python
display(df_data.nlargest(n=1, columns='winning_age'))
display(df_data.nsmallest(n=1, columns='winning_age'))
```

**Output** (simplified):

- **Oldest**: John Goodenough, Chemistry 2019, age **97** (born 1922‑07‑25). He was born in Germany to American parents; the dataset counts this as a German birth, even though he is a US citizen – a caveat when interpreting birth‑country data.
- **Youngest**: Malala Yousafzai, Peace 2014, age **17** (born 1997‑07‑12). She is the youngest Nobel laureate ever.

**Observations**:
- The age range is remarkably wide: from a teenager to a nonagenarian.
- The oldest winner’s case illustrates that birth country does not necessarily reflect nationality.

---

## 3. Descriptive Statistics and Histogram

### Summary Statistics

```python
df_data.winning_age.describe()
```

| Statistic | Value |
|-----------|-------|
| count     | 934.00 |
| mean      | 59.95 |
| std       | 12.62 |
| min       | 17.00 |
| 25%       | 51.00 |
| 50%       | 60.00 |
| 75%       | 69.00 |
| max       | 97.00 |

- The mean age is about **60 years**.
- The median is also 60, indicating a symmetric distribution around the center.
- 75% of laureates are younger than 69; the interquartile range (51–69) spans 18 years.

### Histogram of Winning Ages

A histogram visualizes the distribution. Seaborn’s `histplot` allows easy binning.

```python
plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data, x='winning_age', bins=30)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')
plt.show()
```

- The distribution peaks in the late 50s and early 60s, with a long right tail extending to the 90s.
- The left tail is shorter (few winners under 30).
- Varying the number of bins (e.g., 10, 20, 30, 50) can reveal finer detail; 30 bins provides a good balance.

---

## 4. Age Over Time (All Categories)

Has the typical winning age changed over the decades? A scatter plot with a smoothed trend line answers this.

### Regression Plot with LOWESS

Seaborn’s `regplot` can fit a linear regression, but setting `lowess=True` applies a locally weighted scatterplot smoothing (LOESS), which captures non‑linear trends.

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(
        data=df_data,
        x='year',
        y='winning_age',
        lowess=True,
        scatter_kws={'alpha': 0.4},
        line_kws={'color': 'black'}
    )
plt.show()
```

- Each point is a laureate’s age at a given year.
- The black line is the LOWESS trend, showing the moving average of age.

**Interpretation**:
- From 1900 to about 1950, the average age hovered around **55**.
- After 1950, it began a steady climb, reaching approximately **70** by 2020.
- The spread also increased: in recent decades, we see more very young (e.g., Malala) and very old (e.g., Goodenough) winners.

---

## 5. Age Differences by Category

A box plot compares the distribution of ages across the six prize categories.

### Seaborn Boxplot

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data, x='category', y='winning_age')
plt.show()
```

- Boxes show median (center line), interquartile range (box), and whiskers (typically 1.5× IQR). Points beyond are outliers.

**Observations**:
- **Physics** and **Chemistry** have similar median ages (~60), but Physics has a slightly longer upper whisker.
- **Medicine** has a higher median (closer to 65) and a compact distribution.
- **Literature** has the highest median (around 65) and a wide spread, including many older winners.
- **Peace** has the longest whiskers (from very young to very old) and a median around 65.
- **Economics**, the newest category, has a median around 67 and a relatively narrow range (few very young winners).

**Key findings**:
- Average winners are oldest in **Literature** and **Peace**.
- Average winners are youngest in **Physics** and **Chemistry** (though still around 60).

### Alternative: Plotly Boxplot

For an interactive version, Plotly Express can be used:

```python
fig = px.box(
    df_data,
    x='category',
    y='winning_age',
    title='How old are the Winners?'
)
fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Age at time of Award',
    xaxis={'categoryorder':'mean ascending'}
)
fig.show()
```

This orders categories by mean age, making comparisons easier.

---

## 6. Age Trends by Category Over Time

The box plot aggregates all years, potentially hiding trends within each category. Using `lmplot` with the `row` parameter creates separate panels for each category, each with its own LOWESS trend.

### Faceted LOWESS Plots

```python
with sns.axes_style('whitegrid'):
    sns.lmplot(
        data=df_data,
        x='year',
        y='winning_age',
        row='category',
        lowess=True,
        aspect=2,
        scatter_kws={'alpha': 0.6},
        line_kws={'color': 'black'}
    )
plt.show()
```

- Six subplots, one per category.
- Each shows the raw data points and the smoothed trend.

**Category‑specific trends**:
- **Physics**: Clear upward trend – from ~50 in early years to ~70 recently.
- **Chemistry**: Also increasing, but less steep.
- **Medicine**: Upward trend, similar to Chemistry.
- **Literature**: Slight increase, but with considerable scatter.
- **Peace**: Slight **decrease** over time – winners are getting younger on average (driven by activists like Malala and young human rights advocates).
- **Economics**: Relatively stable since 1969, hovering around 65–70.

### Combined Plot with Hue

To see all trends on one chart, use the `hue` parameter:

```python
with sns.axes_style("whitegrid"):
    sns.lmplot(
        data=df_data,
        x='year',
        y='winning_age',
        hue='category',
        lowess=True,
        aspect=2,
        scatter_kws={'alpha': 0.5},
        line_kws={'linewidth': 5}
    )
plt.show()
```

- Each category gets a different colored line.
- This clearly shows the divergence: Physics, Chemistry, Medicine trend up; Peace trends down; Literature and Economics are intermediate.

**Contrast with Boxplot**:
The boxplot (aggregated over time) suggested Peace laureates are among the oldest, but the time‑series reveals that this is because most Peace laureates in the first half of the 20th century were older; in recent decades, they have become younger. Similarly, Physics laureates are now older than they used to be, so their median in the boxplot is pulled up by recent years. Thus, static and dynamic views can tell different stories – both are important.

---

## 7. Summary of Age Analysis

- The average Nobel laureate is about **60 years old**, but this varies by category and has increased over time.
- **John Goodenough** (Chemistry, 2019) is the oldest at **97**; **Malala Yousafzai** (Peace, 2014) is the youngest at **17**.
- Overall, winners have been getting older, especially in Physics, Chemistry, and Medicine.
- Peace Prize winners, conversely, have become younger on average.
- Economics, the newest category, shows a stable age profile.
- The static boxplot and dynamic time‑series plots complement each other, revealing how aggregating data can mask trends.
