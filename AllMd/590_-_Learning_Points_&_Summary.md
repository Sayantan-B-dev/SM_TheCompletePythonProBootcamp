## Learning Points and Summary

This document summarises the key techniques and concepts demonstrated in the Dr. Semmelweis handwashing analysis. It also recounts the tragic story of Dr. Semmelweis and the historical context of his discovery. The material here consolidates the skills acquired throughout the project and serves as a reference for applying similar methods to other datasets.

---

### Overview of the Project

The analysis replicated Dr. Ignaz Semmelweis’s investigation into the high mortality rate from childbed fever at the Vienna General Hospital in the 1840s. Using historical data on monthly births and deaths, and annual data split by clinic, we:

- Explored the data and calculated baseline mortality rates.
- Visualised trends over time with Matplotlib and Plotly.
- Compared outcomes between Clinic 1 (doctors) and Clinic 2 (midwives).
- Quantified the impact of mandatory handwashing introduced in June 1847.
- Employed statistical graphics and hypothesis testing to confirm the significance of the results.

The following sections detail the specific data‑science skills applied.

---

### 1. Using Histograms to Visualise Distributions

Histograms display the frequency distribution of a continuous variable. In this project, we used histograms to compare the monthly death proportions before and after handwashing.

```python
import plotly.express as px

# Create overlapping histograms with normalisation to percentage
hist = px.histogram(df_monthly,
                    x='pct_deaths',
                    color='washing_hands',
                    nbins=30,
                    opacity=0.6,
                    barmode='overlay',
                    histnorm='percent',
                    marginal='box')

hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Percentage of Months')
hist.show()
```

**Explanation**:

- `nbins=30` divides the data into 30 bins.
- `opacity=0.6` makes bars semi‑transparent so overlapping regions are visible.
- `barmode='overlay'` draws the two histograms on the same axes.
- `histnorm='percent'` normalises each histogram so that bar heights represent percentages, making the two periods comparable despite different lengths.
- `marginal='box'` adds a box plot above the histogram for each group, providing additional summary statistics.

**What we learned**: Histograms reveal the shape, spread, and central tendency of distributions. Overlaying them with transparency and normalising by percent allows fair comparison when sample sizes differ.

---

### 2. Superimposing Histograms

The above code demonstrates superimposing two histograms directly using Plotly’s `barmode='overlay'`. In Matplotlib, one could use `plt.hist()` with `alpha` and `density=True` to achieve a similar effect. However, Plotly’s interactive output and built‑in marginal plots make it particularly effective for exploratory analysis.

---

### 3. Using Kernel Density Estimates (KDE) and the `clip` Parameter

A KDE smooths a histogram into a continuous probability density curve. Seaborn’s `kdeplot()` was used to estimate the underlying distributions of death rates.

#### Basic KDE (with negative tail artifact)

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(dpi=200)
sns.kdeplot(before_washing['pct_deaths'], shade=True)
sns.kdeplot(after_washing['pct_deaths'], shade=True)
plt.title('Estimated Distribution of Monthly Death Rate')
plt.show()
```

**Problem**: The left tail extends below zero, which is impossible for a death rate.

#### Corrected KDE with `clip`

```python
plt.figure(dpi=200)
sns.kdeplot(before_washing['pct_deaths'],
            shade=True,
            clip=(0, 1))          # restrict density to [0,1]
sns.kdeplot(after_washing['pct_deaths'],
            shade=True,
            clip=(0, 1))
plt.title('Estimated Distribution (Clipped to [0,1])')
plt.xlim(0, 0.40)
plt.show()
```

**Explanation**:

- `clip=(0,1)` forces the KDE to consider only the interval between 0 and 1, eliminating the negative tail.
- `plt.xlim(0, 0.40)` focuses on the region where most data lie, improving readability.

**What we learned**: KDEs can produce estimates outside the data’s natural bounds. The `clip` parameter constrains the estimate to a physically meaningful range.

---

### 4. Testing for Statistical Significance with SciPy (p‑values)

A t‑test determines whether the observed difference in means between two independent groups is statistically significant.

```python
from scipy import stats

t_stat, p_value = stats.ttest_ind(a=before_washing['pct_deaths'],
                                   b=after_washing['pct_deaths'])

print(f'p-value: {p_value:.10f}')   # extremely small
print(f't-statistic: {t_stat:.4f}')
```

**Explanation**:

- `ttest_ind()` performs an independent two‑sample t‑test (Welch’s t‑test is the default when variances are unequal).
- The null hypothesis is that the two samples come from populations with the same mean.
- A small p‑value (typically < 0.01) indicates strong evidence against the null, meaning the difference is unlikely due to chance.
- In our case, `p_value ≈ 3e-7`, far below 0.01, so we conclude handwashing had a statistically significant effect.

**What we learned**: p‑values quantify the probability of observing the data if the null hypothesis were true. A low p‑value allows us to reject the null with confidence.

---

### 5. Highlighting Different Parts of a Time Series Chart in Matplotlib

We created a multi‑line plot that distinguishes three periods: before handwashing, after handwashing, and the 6‑month moving average before handwashing.

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up date locators
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim([df_monthly['date'].min(), df_monthly['date'].max()])

plt.grid(color='grey', linestyle='--', alpha=0.3)

# Plot three lines
ma_line, = plt.plot(roll_df.index, roll_df['pct_deaths'],
                    color='crimson', linewidth=3, linestyle='--',
                    label='6m Moving Average (before)')
bw_line, = plt.plot(before_washing['date'], before_washing['pct_deaths'],
                    color='black', linewidth=1, linestyle='--',
                    label='Before Handwashing')
aw_line, = plt.plot(after_washing['date'], after_washing['pct_deaths'],
                    color='skyblue', linewidth=3, marker='o',
                    label='After Handwashing')

plt.legend(handles=[ma_line, bw_line, aw_line], fontsize=18)
plt.show()
```

**Explanation**:

- Different line styles, colours, and markers visually separate the three data series.
- The `label` parameter inside each `plot()` call is used to generate the legend.
- The legend is added with `plt.legend()`, explicitly listing the handles to control order.

**What we learned**: Customising line appearance and adding a legend makes complex time‑series charts interpretable. The `handles` argument in `legend()` allows precise control over which items appear and in what order.

---

### 6. Adding and Configuring a Legend in Matplotlib

The legend was configured using the `handles` parameter, as shown above. Additional customisations (e.g., font size, location) can be applied:

```python
plt.legend(handles=[ma_line, bw_line, aw_line],
           fontsize=18,
           loc='upper right',
           frameon=False)
```

**Explanation**:

- `fontsize` sets the text size.
- `loc` positions the legend (e.g., 'upper right', 'lower left').
- `frameon=False` removes the box around the legend for a cleaner look.

---

### 7. Using NumPy’s `where()` Function for Conditional Column Creation

NumPy’s `where()` provides a vectorised way to create a new column based on a condition.

```python
import numpy as np

# Add a column indicating whether handwashing was in effect
df_monthly['washing_hands'] = np.where(df_monthly['date'] < handwashing_start,
                                        'No', 'Yes')
```

**Explanation**:

- `np.where(condition, x, y)` returns an array with elements from `x` where `condition` is True, and from `y` where False.
- Here, if the date is before the handwashing start date, assign `'No'`; otherwise assign `'Yes'`.
- This column was then used to colour box plots and histograms.

**What we learned**: Vectorised operations like `where()` are efficient and concise for adding categorical columns based on thresholds.

---

### The Tragic Story of Dr. Semmelweis

Despite the overwhelming evidence from his own data, Dr. Ignaz Semmelweis’s handwashing mandate was rejected by the medical establishment. Several factors contributed to this tragic outcome:

- **Scientific context**: In the mid‑19th century, the germ theory of disease had not yet been established. Most physicians believed that diseases were caused by “miasma” (bad air) or imbalances in the body’s humors. The idea that invisible particles on doctors’ hands could cause illness was radical and counterintuitive.
- **Presentation of data**: Semmelweis published his findings in long tables of raw numbers, without any graphical visualisations. The pattern of declining deaths after handwashing was not immediately apparent to readers, and the sheer volume of numbers made the argument difficult to grasp.
- **Tactlessness**: Semmelweis was reportedly confrontational and accused other doctors of causing the deaths of their patients. This alienated potential allies and created powerful enemies.
- **Political opposition**: His hypothesis implied that doctors themselves were carriers of disease, an accusation that many found insulting. His superiors at the Vienna hospital, already sceptical, eventually dismissed him.
- **Later life**: After losing his position, Semmelweis grew increasingly frustrated and erratic. He may have suffered from early‑onset dementia or syphilis. In 1865, at age 47, he was committed to a mental asylum, where he died within two weeks, reportedly from sepsis—the very type of infection he had fought to prevent.

It was not until the 1880s, after Louis Pasteur’s work on germ theory and Joseph Lister’s introduction of antiseptic surgery, that handwashing became widely accepted. Semmelweis’s data, once dismissed, were posthumously recognised as a landmark in epidemiology.

**Modern parallel**: The tragic story underscores the importance of clear data communication and the need for scientific humility. Visualisations like those in this project would have made Semmelweis’s case far more compelling.

---

### Conclusion

This project demonstrated a complete data‑analysis workflow: from loading and exploring data, through visualisation and statistical testing, to drawing conclusions. The techniques learned—histograms, KDE, p‑values, time‑series highlighting, and conditional column creation—are applicable to countless real‑world problems. The story of Dr. Semmelweis serves as a powerful reminder that data alone is not enough; it must be presented effectively and persuasively to drive change.