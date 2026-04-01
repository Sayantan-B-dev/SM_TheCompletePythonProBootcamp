## Introduction and Project Goals

This documentation covers the analysis of historical medical data collected by Dr. Ignaz Semmelweis at the Vienna General Hospital during the 1840s. The objective is to investigate the high mortality rate from childbed fever (puerperal fever) among women in maternity wards and to evaluate the impact of a handwashing policy introduced in mid-1847.

### Background

In the 19th century, the cause of infectious diseases was unknown. Many believed that illnesses were caused by "bad air" or supernatural forces. Dr. Semmelweis, a Hungarian physician, suspected that something in the hospital procedures was responsible for the alarming number of deaths in the maternity clinics. He collected data on births and deaths across two clinics:

- **Clinic 1**: Staffed by male doctors and medical students who also performed autopsies.
- **Clinic 2**: Staffed by female midwives who did not perform autopsies.

The data spans from 1841 to 1849 and includes monthly and yearly records. This analysis replicates Dr. Semmelweis’s investigation using modern data science tools.

### Learning Objectives

By the end of this analysis, you will be able to:

- Perform exploratory data analysis (EDA) on real-world datasets.
- Create compelling visualizations using Matplotlib, Plotly, and Seaborn.
- Compare distributions using histograms, box plots, and kernel density estimates (KDE).
- Compute rolling averages and highlight time-series segments.
- Conduct statistical significance tests (t-test) and interpret p-values.
- Use NumPy’s `where()` function for conditional column creation.
- Format time-series axes with locators and formatters.

### Dataset

The project uses two CSV files:

- **`monthly_deaths.csv`**: Contains monthly totals of births and deaths from January 1841 to March 1849.
- **`annual_deaths_by_clinic.csv`**: Contains yearly totals of births and deaths, broken down by clinic (clinic 1 and clinic 2).

The data was originally published by Dr. Semmelweis in 1861. The English translation of his work is available [here](http://graphics8.nytimes.com/images/blogs/freakonomics/pdf/the%20etiology,%20concept%20and%20prophylaxis%20of%20childbed%20fever.pdf).

### Setup Instructions

1. Download the project ZIP file containing the two CSV files and the Jupyter notebook.
2. Upload the notebook to Google Colab or open it locally with Jupyter.
3. Ensure the CSV files are placed in the same directory as the notebook.
4. Install required libraries if necessary (pandas, numpy, plotly, seaborn, matplotlib, scipy). In Google Colab, you may need to upgrade plotly:
   ```python
   %pip install --upgrade plotly
   ```

The analysis is structured in sequential steps, each building upon the previous. The following sections document every stage in detail, with code examples and explanations.

---

## Preliminary Data Exploration

In this first phase, we load the data, inspect its structure, check for missing values or duplicates, and compute basic statistics. This step is crucial to understand the scope and quality of the dataset.

### Loading the Data

We use pandas to read the CSV files. For the monthly data, we parse the `date` column as datetime to facilitate time-series operations.

```python
import pandas as pd
import numpy as np

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])
```

### Examining the DataFrames

#### Yearly Data

```python
print(df_yearly.shape)   # (12, 4)
df_yearly.head()
```

Output shows 12 rows and 4 columns: `year`, `births`, `deaths`, `clinic`. The data covers 1841–1846 (only six years, but two clinics each year, hence 12 rows). We see that clinic 1 consistently has more births and deaths than clinic 2.

#### Monthly Data

```python
print(df_monthly.shape)   # (98, 3)
df_monthly.tail()
```

The monthly data has 98 rows and 3 columns: `date`, `births`, `deaths`. It spans from January 1841 to March 1849. The last few rows show data up to March 1849.

### Checking for Missing Values and Duplicates

```python
print(df_yearly.info())
print(df_monthly.info())
```

Both DataFrames have no null values. Alternatively, we can use:

```python
print(f'Any yearly NaN values? {df_yearly.isna().values.any()}')
print(f'Any monthly NaN values? {df_monthly.isna().values.any()}')
```

Duplicate checks:

```python
print(f'Any yearly duplicates? {df_yearly.duplicated().values.any()}')
print(f'Any monthly duplicates? {df_monthly.duplicated().values.any()}')
```

Both return `False`, confirming the data is clean.

### Descriptive Statistics

```python
df_yearly.describe()
df_monthly.describe()
```

**Yearly stats**:
- Average births per year: 3153
- Average deaths per year: 223
- Minimum deaths: 66 (clinic 2, 1844)
- Maximum deaths: 518 (clinic 1, 1842)

**Monthly stats**:
- Average births per month: 267
- Average deaths per month: 22.47
- Minimum deaths: 0 (some months had no deaths)
- Maximum deaths: 75

These initial numbers already hint at the severity of the problem.

### Overall Mortality Rate

We calculate the total percentage of women who died in childbirth over the entire period (1841–1846, as yearly data stops at 1846).

```python
prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')
```

Output: `7.08%`. This is an extremely high rate compared to modern statistics (e.g., 0.018% in the US in 2013). The data confirms that childbirth was indeed very dangerous.

### Visualizing Births and Deaths Over Time

We create a twin‑axis plot to show monthly births and deaths together. This helps spot any trends or sudden changes.

First, we set up locators for the x‑axis to display years and months clearly:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
```

Now the plot:

```python
plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.plot(df_monthly.date, df_monthly.births, color='skyblue', linewidth=3)
ax2.plot(df_monthly.date, df_monthly.deaths, color='crimson', linewidth=2, linestyle='--')

plt.show()
```

**Observations**:
- Births gradually increase over the years.
- Deaths fluctuate but show a notable drop after mid‑1847, despite rising births. This coincides with the introduction of handwashing.

The visualization clearly reveals an anomaly that warrants further investigation.

---

## Analysing the Yearly Data Split by Clinic

The yearly data provides a breakdown by clinic, allowing us to compare outcomes between the two wards. This step is essential to understand whether the difference in death rates is consistent and which clinic has a higher risk.

### Births and Deaths by Clinic (Line Charts)

We use Plotly Express to create interactive line charts.

#### Births

```python
import plotly.express as px

line = px.line(df_yearly, x='year', y='births', color='clinic',
               title='Total Yearly Births by Clinic')
line.show()
```

**Findings**:
- Clinic 1 consistently has more births than clinic 2.
- Both clinics show an upward trend in births, indicating the hospital became busier over time.

#### Deaths

```python
line = px.line(df_yearly, x='year', y='deaths', color='clinic',
               title='Total Yearly Deaths by Clinic')
line.show()
```

**Findings**:
- Clinic 1 also has more deaths, but raw numbers are not directly comparable because the patient volumes differ. We need to look at proportions.

### Calculating Proportion of Deaths per Clinic

We add a column `pct_deaths` to the yearly DataFrame, representing the death rate per clinic per year.

```python
df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births
df_yearly
```

Now we can compute the average death rate over the entire period for each clinic.

```python
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_c1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100
print(f'Average death rate in clinic 1 is {avg_c1:.3}%.')   # 9.92%

clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
print(f'Average death rate in clinic 2 is {avg_c2:.3}%.')   # 3.88%
```

Clinic 1 has a death rate more than twice that of clinic 2. This is a striking difference and the core puzzle Dr. Semmelweis faced.

### Visualising Yearly Proportions

```python
line = px.line(df_yearly, x='year', y='pct_deaths', color='clinic',
               title='Proportion of Yearly Deaths by Clinic')
line.show()
```

**Observations**:
- The proportion of deaths in clinic 1 is consistently higher than in clinic 2 every year.
- The worst year was 1842, where clinic 1 reached ~16% mortality, while clinic 2 peaked at ~7.6%.
- Both clinics show a general downward trend after 1842, but clinic 1 remains more dangerous.

These findings reinforce the suspicion that something specific to clinic 1 (e.g., doctors performing autopsies) was causing the excess deaths.

---

## The Effect of Handwashing

In June 1847, Dr. Semmelweis mandated handwashing with a chlorine solution for all medical staff. The monthly data allows us to quantify the impact of this intervention.

### Adding a Monthly Death Proportion Column

We add `pct_deaths` to the monthly DataFrame similarly.

```python
df_monthly['pct_deaths'] = df_monthly.deaths / df_monthly.births
```

### Defining the Intervention Date

```python
handwashing_start = pd.to_datetime('1847-06-01')
```

### Splitting the Data

```python
before_washing = df_monthly[df_monthly.date < handwashing_start]
after_washing = df_monthly[df_monthly.date >= handwashing_start]
```

### Calculating Overall Death Rates Before and After

```python
bw_rate = before_washing.deaths.sum() / before_washing.births.sum() * 100
aw_rate = after_washing.deaths.sum() / after_washing.births.sum() * 100
print(f'Average death rate before 1847 was {bw_rate:.4}%')   # 10.53%
print(f'Average death rate AFTER 1847 was {aw_rate:.3}%')    # 2.15%
```

The death rate dropped from 10.53% to 2.15% – a dramatic reduction.

### Rolling Average of Death Rate Before Handwashing

To smooth out monthly fluctuations and better visualize the trend before the intervention, we compute a 6‑month rolling average.

```python
roll_df = before_washing.set_index('date')
roll_df = roll_df.rolling(window=6).mean()
```

The resulting DataFrame contains the moving average for births, deaths, and death proportion.

### Enhanced Time‑Series Plot with Handwashing Highlight

We modify the earlier twin‑axis plot to show the death proportion over time, with separate lines for before, after, and the moving average.

```python
plt.figure(figsize=(14,8), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])

plt.grid(color='grey', linestyle='--')

ma_line, = plt.plot(roll_df.index, roll_df.pct_deaths,
                    color='crimson', linewidth=3, linestyle='--',
                    label='6m Moving Average')
bw_line, = plt.plot(before_washing.date, before_washing.pct_deaths,
                    color='black', linewidth=1, linestyle='--',
                    label='Before Handwashing')
aw_line, = plt.plot(after_washing.date, after_washing.pct_deaths,
                    color='skyblue', linewidth=3, marker='o',
                    label='After Handwashing')

plt.legend(handles=[ma_line, bw_line, aw_line], fontsize=18)
plt.show()
```

**Key Insight**: The plot vividly illustrates the sharp decline in death rates immediately after June 1847. The moving average confirms that the downward trend was already present but the drop is sustained and pronounced post‑intervention.

---

## Visualising Distributions and Testing for Statistical Significance

To strengthen the argument, we examine the distribution of monthly death rates before and after handwashing using various statistical graphics and perform a hypothesis test.

### Difference in Average Monthly Death Rate

We compute the mean monthly death proportion (as a percentage) for each period.

```python
avg_prob_before = before_washing.pct_deaths.mean() * 100
avg_prob_after = after_washing.pct_deaths.mean() * 100

print(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')   # 10.5%
print(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')    # 2.11%

mean_diff = avg_prob_before - avg_prob_after
print(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')       # 8.4%

times = avg_prob_before / avg_prob_after
print(f'This is a {times:.2}x improvement!')                                            # 5.0x
```

Handwashing reduced the average monthly death rate by 8.4 percentage points, a five‑fold improvement.

### Box Plots Before and After Handwashing

Box plots provide a concise summary of the distribution (median, quartiles, outliers). We first create a categorical column indicating whether handwashing was in effect.

```python
df_monthly['washing_hands'] = np.where(df_monthly.date < handwashing_start, 'No', 'Yes')
```

Then generate the box plot with Plotly.

```python
box = px.box(df_monthly, x='washing_hands', y='pct_deaths', color='washing_hands',
             title='How Have the Stats Changed with Handwashing?')
box.update_layout(xaxis_title='Washing Hands?', yaxis_title='Percentage of Monthly Deaths')
box.show()
```

**Observations**:
- Before handwashing, the median death rate is around 10%, with a wide interquartile range and several high outliers (e.g., >25%).
- After handwashing, the median drops to about 2%, the spread is much narrower, and the maximum is below 5% (except one month at ~5%).
- The reduction is not only in the average but also in the variability and worst‑case outcomes.

### Histograms of Monthly Death Rates

Histograms show the frequency distribution. Because the two periods have different lengths, we normalize using `histnorm='percent'` to make them comparable.

```python
hist = px.histogram(df_monthly, x='pct_deaths', color='washing_hands',
                    nbins=30, opacity=0.6, barmode='overlay',
                    histnorm='percent', marginal='box')
hist.update_layout(xaxis_title='Proportion of Monthly Deaths', yaxis_title='Count')
hist.show()
```

**Insights**:
- The before‑handwashing distribution is spread out, with many months having death rates above 10%.
- The after‑handwashing distribution is tightly clustered near zero, with most months below 5%.
- The overlaid box plots at the top confirm the dramatic shift.

### Kernel Density Estimation (KDE)

KDE smooths the histogram into a continuous probability density curve, providing a clearer picture of the underlying distribution.

First, we create a basic KDE plot (which may include negative values due to estimation artifacts).

```python
import seaborn as sns

plt.figure(dpi=200)
sns.kdeplot(before_washing.pct_deaths, shade=True)
sns.kdeplot(after_washing.pct_deaths, shade=True)
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.show()
```

This shows a left tail extending below zero – an impossibility because death rates cannot be negative. We correct by clipping the estimate to the [0,1] range.

```python
plt.figure(dpi=200)
sns.kdeplot(before_washing.pct_deaths, shade=True, clip=(0,1))
sns.kdeplot(after_washing.pct_deaths, shade=True, clip=(0,1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)
plt.show()
```

Now the two distributions are clearly separated: the before curve peaks around 10%, while the after curve peaks near 2%. There is very little overlap, indicating a fundamental change.

### Statistical Significance: t‑Test

We use an independent two‑sample t‑test to assess whether the observed difference in means is statistically significant or could have occurred by chance.

```python
import scipy.stats as stats

t_stat, p_value = stats.ttest_ind(a=before_washing.pct_deaths,
                                  b=after_washing.pct_deaths)
print(f'p-value is {p_value:.10f}')   # 0.0000002985
print(f't-statistic is {t_stat:.4}')   # 5.512
```

The p‑value is far below 0.01 (1%). Therefore, we can reject the null hypothesis that the two samples have the same mean. The difference is highly statistically significant at the 99% confidence level. This provides strong evidence that handwashing caused the reduction in death rates.

---

## Learning Points and Summary

Through this analysis, we have demonstrated the following skills and concepts:

- **Data exploration**: Inspecting shape, columns, missing values, duplicates, and summary statistics.
- **Data visualization**:
  - Twin‑axis plots in Matplotlib with time formatting.
  - Line charts, box plots, and histograms in Plotly.
  - Kernel density estimation in Seaborn.
- **Statistical thinking**:
  - Comparing means and distributions.
  - Using rolling averages to smooth time series.
  - Performing a t‑test and interpreting p‑values.
- **Conditional column creation** with NumPy’s `where()`.
- **Highlighting time periods** in Matplotlib charts.
- **Handling date axes** with locators and formatters.

### The Tragic Story of Dr. Semmelweis

Despite the overwhelming evidence from his data, Dr. Semmelweis’s ideas were rejected by the medical establishment. His findings contradicted the prevailing theories of the time, and his confrontational style alienated many colleagues. He published his results as long tables without visualizations, making the pattern difficult to grasp. He eventually lost his position and died in a mental asylum, ironically from an infection similar to the one he fought to prevent. It was not until two decades later, with Louis Pasteur’s germ theory, that handwashing became accepted.

### Final Remarks

This project underscores the importance of data visualization and statistical reasoning in making compelling arguments. By presenting the same data in clear charts and rigorous tests, we can communicate insights that might otherwise be overlooked. The techniques learned here are applicable to countless real‑world problems where we need to compare outcomes before and after an intervention.