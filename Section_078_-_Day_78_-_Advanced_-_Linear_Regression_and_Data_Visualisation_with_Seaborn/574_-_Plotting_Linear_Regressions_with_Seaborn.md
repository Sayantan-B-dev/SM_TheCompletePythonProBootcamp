# Plotting Linear Regressions with Seaborn

This document provides a comprehensive guide to visualising linear relationships using Seaborn’s `regplot()` function. Building on the cleaned movie dataset and the separation of films into old (pre‑1970) and new (1970 onward) eras, we create scatter plots overlaid with a fitted regression line and confidence interval. These visualisations help assess whether the relationship between production budget and worldwide gross revenue differs between the two time periods.

Key topics:

- Introduction to `regplot()` and its parameters.
- Basic regression plot for old films.
- Customising plot appearance (figure size, transparency, line colour).
- Applying Seaborn themes.
- Styled regression plot for new films with custom colours and axis limits.
- Interpretation of the plots: fit quality, confidence intervals, and practical insights.

All code examples are taken from the completed Jupyter Notebook and assume that the following imports and data preparations have already been performed:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming data_clean, old_films, new_films are already defined
```

---

## 1. Overview of `regplot`

Seaborn’s `regplot()` draws a scatter plot of two variables and fits a linear regression model, displaying the regression line along with a 95% confidence interval for the regression estimate. The confidence interval is shown as a shaded band around the line, indicating the uncertainty in the fitted line.

Basic syntax:

```python
sns.regplot(data=DataFrame, x='column_x', y='column_y')
```

Additional parameters allow fine‑tuning of the scatter points (`scatter_kws`), the regression line (`line_kws`), and overall appearance.

---

## 2. Regression Plot for Old Films

We begin by plotting the relationship between production budget and worldwide gross for films released before 1970.

```python
sns.regplot(data=old_films, 
            x='USD_Production_Budget',
            y='USD_Worldwide_Gross')
```

**Result:** A scatter plot with a regression line and confidence interval. The points are spread widely, and the confidence band is relatively wide, indicating a poor fit.

### 2.1 Improving the Plot with Matplotlib Customisation

To make the chart more suitable for presentation, we increase the figure size and resolution, set a white grid background, and adjust the transparency of the scatter points. We also change the regression line to black for better visibility.

```python
plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style("whitegrid"):
    sns.regplot(data=old_films, 
                x='USD_Production_Budget', 
                y='USD_Worldwide_Gross',
                scatter_kws={'alpha': 0.4},
                line_kws={'color': 'black'})
```

**Explanation:**

- `plt.figure(figsize=(8,4), dpi=200)` creates a figure with width 8 inches, height 4 inches, and 200 dots per inch.
- `with sns.axes_style("whitegrid")` temporarily applies the white grid background.
- `scatter_kws={'alpha': 0.4}` makes the points semi‑transparent, reducing overplotting.
- `line_kws={'color': 'black'}` sets the regression line to black.

**Interpretation:**

- The regression line has a slight positive slope, but many points lie far from it.
- The confidence interval is broad, especially at higher budgets.
- The model does not capture the data well; budget alone is a poor predictor of revenue for old films.

---

## 3. Regression Plot for New Films (Challenge)

Now we create a styled regression plot for the new films (1970 onward). The challenge requires:

- Using a dark grid background.
- Setting axis limits to avoid negative values.
- Labelling axes appropriately: "Revenue in $ billions" and "Budget in $100 millions".
- Using specific HEX colour codes: dark blue (`#2f4b7c`) for the scatter points, orange (`#ff7c43`) for the regression line.
- Interpreting the chart.

### 3.1 Solution Code

```python
plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('darkgrid'):
    ax = sns.regplot(data=new_films,
                     x='USD_Production_Budget',
                     y='USD_Worldwide_Gross',
                     color='#2f4b7c',
                     scatter_kws={'alpha': 0.3},
                     line_kws={'color': '#ff7c43'})
    
    ax.set(ylim=(0, 3000000000),
           xlim=(0, 450000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')
```

**Explanation of parameters:**

- `color='#2f4b7c'` sets the colour of the scatter points (this overrides the default palette).
- `scatter_kws={'alpha': 0.3}` makes the points transparent to better visualise density.
- `line_kws={'color': '#ff7c43'}` colours the regression line orange.
- `ax.set(...)` sets the axis limits and labels. The y‑limit is set to 3 billion, x‑limit to 450 million, which comfortably covers the data range without negative values.

### 3.2 Interpreting the Chart

- **Fit quality:** The data points align much more closely with the regression line than in the old‑films plot. The confidence interval is also much narrower, indicating a more precise estimate of the relationship.
- **Slope:** The line rises steeply, suggesting a strong positive relationship: higher budgets are associated with higher worldwide gross.
- **Predictions:** From the line, a film with a budget of $150 million is estimated to earn slightly under $500 million worldwide.
- **Outliers:** A few points with very high revenue (e.g., *Avatar*) lie above the line, meaning they outperformed the model’s prediction. Points below the line underperformed relative to their budget.

Overall, the regression plot confirms that for modern films, the production budget is a meaningful predictor of worldwide revenue.

---

## 4. Understanding the Components of a Regression Plot

### 4.1 The Regression Line

The line represents the best‑fit linear relationship estimated by ordinary least squares. Its equation is:

```
revenue = θ₀ + θ₁ × budget
```

The slope θ₁ tells us the average change in revenue for a one‑unit (one‑dollar) increase in budget. From the scikit‑learn analysis (covered later), we find that for new films, θ₁ ≈ 3.12, meaning each additional dollar in budget is associated with about $3.12 in additional revenue.

### 4.2 The Confidence Interval

The shaded band around the line is the 95% confidence interval for the regression line. It represents the uncertainty in the estimated mean revenue at each budget level. A narrow interval indicates that the model is relatively certain about the average revenue for a given budget. A wide interval suggests greater uncertainty, often due to sparse data or high variability.

### 4.3 The Scatter Points

The individual points show the actual data. Their spread around the line reflects the residual variance – the part of revenue not explained by budget. In the new‑films plot, while the points cluster around the line, there is still considerable scatter, indicating that other factors (e.g., genre, marketing, release timing) also influence revenue.

---

## 5. Comparison Between Old and New Films

Plotting regressions for the two eras side‑by‑side highlights a dramatic shift:

- **Old films:** The regression line is nearly flat, and the confidence interval is wide. Budget explains very little of the variation in revenue (R² ≈ 0.03). This suggests that in the early days of cinema, a film’s success was not closely tied to its production cost.
- **New films:** The regression line has a clear upward slope, and the confidence interval is narrow. Budget explains about 56% of the variance in revenue (R² ≈ 0.56). This supports the hypothesis that since the 1970s, bigger budgets tend to lead to bigger box office returns, likely due to the rise of blockbuster filmmaking, extensive marketing, and global distribution.

---

## 6. Summary

In this section, we have:

- Used Seaborn’s `regplot()` to visualise linear relationships.
- Customised the appearance of regression plots using Matplotlib parameters and Seaborn themes.
- Produced styled plots for both old and new films, following a specific challenge.
- Interpreted the plots to assess the strength of the relationship between budget and revenue.
- Observed a marked difference between the two eras, motivating further quantitative analysis with scikit‑learn.

