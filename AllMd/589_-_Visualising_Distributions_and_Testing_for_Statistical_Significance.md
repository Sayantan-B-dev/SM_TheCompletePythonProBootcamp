## Visualising Distributions and Testing for Statistical Significance

After establishing that handwashing dramatically reduced the average death rate, we now employ more advanced statistical and visual methods to strengthen the argument. This section focuses on:

- Quantifying the reduction in the mean monthly death rate.
- Using box plots to compare distributions before and after handwashing.
- Creating overlapping histograms to visualise the shift in outcomes.
- Applying kernel density estimation (KDE) to smooth the distributions.
- Conducting a t‑test to determine if the difference is statistically significant.

All analyses use the monthly dataset with the `pct_deaths` column and the subsets `before_washing` and `after_washing` defined earlier.

---

### Challenge 1: Calculate the Difference in the Average Monthly Death Rate

We compute the mean of the monthly death proportions (converted to percentages) for the two periods and compare them.

```python
# Average monthly death proportion before handwashing (as percentage)
avg_prob_before = before_washing['pct_deaths'].mean() * 100

# Average monthly death proportion after handwashing (as percentage)
avg_prob_after = after_washing['pct_deaths'].mean() * 100

# Print with three significant digits
print(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')
print(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')

# Absolute reduction in percentage points
mean_diff = avg_prob_before - avg_prob_after
print(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')

# Relative improvement (how many times lower)
times = avg_prob_before / avg_prob_after
print(f'This is a {times:.2}x improvement!')
```

**Output**:
```
Chance of death during childbirth before handwashing: 10.5%.
Chance of death during childbirth AFTER handwashing: 2.11%.
Handwashing reduced the monthly proportion of deaths by 8.4%!
This is a 5.0x improvement!
```

**Explanation**:

- `before_washing['pct_deaths'].mean()` calculates the arithmetic mean of the monthly death proportions. Multiplying by 100 converts the decimal to a percentage.
- The reduction of 8.4 percentage points means that, on average, 8.4 fewer women per 100 gavebirths died after handwashing.
- A five‑fold improvement means the risk was reduced to one‑fifth of its previous level.

---

### Challenge 2: Using Box Plots to Show How the Death Rate Changed

Box plots provide a concise summary of the distribution: median, quartiles, range, and outliers. We first add a categorical column indicating whether handwashing was in effect for each month.

#### Adding the `washing_hands` Column with NumPy's `where()`

```python
import numpy as np

# Create new column: 'No' if date < handwashing_start, else 'Yes'
df_monthly['washing_hands'] = np.where(df_monthly['date'] < handwashing_start, 'No', 'Yes')
```

**Explanation**:

- `np.where(condition, value_if_true, value_if_false)` operates element‑wise. For each row, if the date is before the intervention, assign `'No'`; otherwise assign `'Yes'`.
- This column will be used as the grouping variable in Plotly.

#### Creating the Box Plot with Plotly Express

```python
import plotly.express as px

# Create box plot
box = px.box(df_monthly,
             x='washing_hands',      # categorical variable on x-axis
             y='pct_deaths',          # numeric variable on y-axis
             color='washing_hands',   # colour boxes by category
             title='How Have the Stats Changed with Handwashing?')

# Improve axis labels
box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths')

# Display the plot
box.show()
```

**Detailed Explanation**:

- `px.box()` creates an interactive box plot.
- `x='washing_hands'`: groups the data by the two categories ('No' and 'Yes').
- `y='pct_deaths'`: the variable whose distribution is shown.
- `color='washing_hands'`: colours the boxes differently for each group (Plotly automatically assigns colours).
- `update_layout()`: customises the axis titles.

**Interpretation**:

- **Before handwashing ('No')**: The box extends from about 5% to 15% (first to third quartile), with a median near 10%. There are several high outliers above 20%, including one above 30%. This indicates a wide spread and occasional catastrophic months.
- **After handwashing ('Yes')**: The box is much shorter, spanning roughly 1% to 4%, with a median around 2%. The maximum is below 5%. There are no high outliers. This shows that not only the average but also the variability and worst‑case outcomes improved dramatically.

The box plot succinctly conveys the overall shift in the distribution.

---

### Challenge 3: Use Histograms to Visualise the Monthly Distribution of Outcomes

Histograms show the frequency of different death rate values. Because the two periods have different lengths (76 months before vs. 22 months after), we normalise using `histnorm='percent'` so that the areas of the bars represent percentages rather than raw counts, making them comparable.

```python
# Create overlapping histograms
hist = px.histogram(df_monthly,
                    x='pct_deaths',
                    color='washing_hands',
                    nbins=30,               # number of bins
                    opacity=0.6,             # transparency for overlap visibility
                    barmode='overlay',       # bars drawn on top of each other
                    histnorm='percent',      # normalise to percentages
                    marginal='box')          # add box plot above the histogram

# Label axes
hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Percentage of Months')

# Show the plot
hist.show()
```

**Explanation**:

- `nbins=30`: divides the range of death proportions into 30 equal‑width bins.
- `opacity=0.6`: makes bars semi‑transparent so overlapping regions are visible.
- `barmode='overlay'`: draws the two histograms on the same axes, one in front of the other.
- `histnorm='percent'`: the height of each bar represents the percentage of months in that category falling into that bin, not the raw count. This compensates for the unequal sample sizes.
- `marginal='box'`: adds a miniature box plot above the histogram for each group, providing an additional visual summary.

**Interpretation**:

- Before handwashing (blue), the distribution is spread widely, with many months in the 10–15% range and a long right tail extending beyond 25%.
- After handwashing (red), the distribution is sharply peaked near 0–2%, with almost all months below 5%. There is very little overlap between the two histograms.
- The box plots at the top reinforce the same message.

The histogram makes it clear that the entire distribution shifted leftwards after handwashing.

---

### Challenge 4: Use a Kernel Density Estimate (KDE) to Visualise a Smooth Distribution

Histograms can be sensitive to bin width. KDE provides a smooth estimate of the probability density function. We use Seaborn’s `kdeplot()`.

#### Default KDE (with negative tail problem)

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(dpi=200)
sns.kdeplot(before_washing['pct_deaths'], shade=True)
sns.kdeplot(after_washing['pct_deaths'], shade=True)
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.show()
```

**Problem**: The left tail of the before‑handwashing distribution extends below zero. A negative death rate is impossible. This artifact occurs because the KDE uses Gaussian kernels that can assign probability mass outside the data range.

#### Corrected KDE with `clip` Parameter

We restrict the estimate to the physically meaningful range [0, 1] (death proportion cannot be negative or exceed 1). We also set the x‑axis limit to 0–40% for a focused view.

```python
plt.figure(dpi=200)
sns.kdeplot(before_washing['pct_deaths'],
            shade=True,
            clip=(0, 1))          # constrain density to [0,1]
sns.kdeplot(after_washing['pct_deaths'],
            shade=True,
            clip=(0, 1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)                 # zoom in on relevant range
plt.show()
```

**Explanation**:

- `clip=(0,1)` tells the KDE to only consider the density within that interval; any density outside is ignored. This eliminates the impossible negative tail.
- `shade=True` fills the area under the curve.
- `plt.xlim(0, 0.40)` restricts the x‑axis to 0–40%, where all meaningful data lie.

**Interpretation**:

- The before curve (blue) peaks around 10–12% and has a long right tail.
- The after curve (orange) peaks near 2% and decays quickly; almost all its mass is below 5%.
- The two curves have minimal overlap, visually confirming that the distributions are fundamentally different.

---

### Challenge 5: Use a T‑Test to Show Statistical Significance

A t‑test assesses whether the observed difference in means could be due to random chance. The null hypothesis is that the two samples come from populations with the same mean. A low p‑value (typically < 0.01) indicates strong evidence against the null.

We use SciPy’s `ttest_ind()` for independent samples.

```python
from scipy import stats

# Perform two-sample t-test (assuming unequal variances, Welch's t-test)
t_stat, p_value = stats.ttest_ind(a=before_washing['pct_deaths'],
                                   b=after_washing['pct_deaths'])

print(f'p-value is {p_value:.10f}')   # p-value with 10 decimal places
print(f't-statistic is {t_stat:.4}')  # t-statistic with 4 significant digits
```

**Output**:
```
p-value is 0.0000002985
t-statistic is 5.512
```

**Explanation**:

- `stats.ttest_ind()` calculates the t‑statistic and the two‑tailed p‑value. By default, it assumes equal variances; however, the test is robust to moderate violations, and we can also set `equal_var=False` for Welch’s test (which we might add for completeness).
- The p‑value is approximately 3 × 10⁻⁷, far below 0.01. Therefore, we can reject the null hypothesis with 99% confidence.
- This means the probability of observing such a large difference (or larger) by random chance is less than 0.0001%. The reduction in death rate is statistically significant.

**Conclusion**: Handwashing had a genuine, non‑random effect.

---

### Summary of Statistical and Visual Findings

- The average monthly death rate dropped from 10.5% to 2.1%, a five‑fold improvement.
- Box plots show the entire distribution shifted: median, quartiles, and maximum all decreased.
- Histograms reveal that before handwashing, death rates were spread widely; after, they clustered near zero.
- KDE smooths the distributions and, after clipping, confirms the separation without the artifact of negative rates.
- A t‑test yields a p‑value of 0.0000003, confirming that the change is highly statistically significant.

Together, these analyses provide overwhelming evidence that handwashing with chlorine caused a substantial and enduring reduction in maternal mortality at the Vienna General Hospital. This modern re‑analysis of Dr. Semmelweis’s data vindicates his hypothesis, even though his contemporaries rejected it.

---

### Additional Notes

- The `clip` parameter in `kdeplot` is essential when the data have natural bounds, to avoid misleading extrapolation.
- Using `histnorm='percent'` in histograms is crucial when comparing groups of unequal size.
- The t‑test p‑value should always be reported with enough precision; values below 0.001 are often given in scientific notation or with many decimal places to convey their magnitude.
- These techniques are widely applicable to any before‑and‑after intervention study.