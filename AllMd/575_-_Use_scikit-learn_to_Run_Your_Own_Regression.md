# Using scikit‑learn to Run Your Own Regression

This document provides a detailed, step‑by‑step guide to performing linear regression using the scikit‑learn library. Building on the exploratory visualisations from Seaborn, we now quantify the relationship between a film’s production budget and its worldwide gross revenue. We will fit a univariate linear regression model, extract its coefficients, evaluate its fit with the R‑squared metric, and use the model to make predictions. The analysis is performed separately for the “new” films (released from 1970 onward) and the “old” films (pre‑1970), allowing us to compare the strength of the relationship across different eras.

All code examples assume that the necessary imports have been made and that the cleaned data (`data_clean`) as well as the subsets `old_films` and `new_films` are already defined, as established in previous sections.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
```

---

## 1. The Linear Regression Model

A univariate linear regression models the relationship between a single explanatory variable (feature) and a continuous response variable (target). In our case:

- **Feature (X):** Production budget (`USD_Production_Budget`)
- **Target (y):** Worldwide gross revenue (`USD_Worldwide_Gross`)

The model assumes a linear relationship of the form:

```
y = θ₀ + θ₁·X
```

where:

- **θ₀ (intercept):** the predicted revenue when the budget is zero.
- **θ₁ (slope):** the change in revenue for a one‑unit (one‑dollar) increase in budget.

The goal of linear regression is to find the values of θ₀ and θ₁ that minimise the sum of squared differences between the observed and predicted values – the ordinary least squares (OLS) solution.

---

## 2. Preparing the Data for scikit‑learn

scikit‑learn’s `LinearRegression` expects the feature(s) and target to be provided as two‑dimensional arrays or DataFrames. While a pandas Series could be used, it is safer and more consistent to pass DataFrames.

For the **new films** (post‑1970), we create:

```python
# Explanatory variable (feature)
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])

# Response variable (target)
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
```

- `X` is a DataFrame with a single column: the production budget.
- `y` is a DataFrame with a single column: the worldwide gross.

---

## 3. Creating and Fitting the Model

We instantiate a `LinearRegression` object and then call its `.fit()` method, passing the feature and target DataFrames.

```python
# Create the regression object
regression = LinearRegression()

# Fit the model to the data
regression.fit(X, y)
```

During fitting, scikit‑learn computes the optimal θ₀ and θ₁ using the entire dataset. The fitted model is stored in the `regression` object.

---

## 4. Extracting the Model Coefficients

After fitting, we can access the estimated intercept and slope via the attributes `intercept_` and `coef_`.

```python
# Intercept (θ₀)
print(regression.intercept_)

# Slope (θ₁)
print(regression.coef_)
```

**Typical output (for new_films):**

```
[-8650768.00661027]
[[3.12259592]]
```

- **Intercept:** approximately –$8.65 million. This would be the predicted revenue for a film with a zero budget. A negative revenue is not realistic; it simply reflects the mathematical best‑fit line extended leftwards beyond the range of the data. In practice, we should not interpret the intercept literally because no film has a zero budget.
- **Slope:** approximately 3.12. This means that, on average, each additional dollar spent on production is associated with an increase of about $3.12 in worldwide gross revenue.

The slope confirms the visual impression from the regression plot: higher budgets tend to yield higher revenues, and the relationship is economically meaningful – a $1 investment is associated with a $3.12 return.

---

## 5. Evaluating Model Fit with R‑squared

The coefficient of determination, **R²**, measures the proportion of variance in the target variable that is explained by the feature(s). It ranges from 0 to 1, with higher values indicating a better fit.

```python
r_squared = regression.score(X, y)
print(r_squared)
```

**Output:** `0.5577032617720403`

- Approximately **55.8%** of the variation in worldwide gross revenue among new films can be explained by their production budgets.
- This is a moderately strong relationship, especially considering that a single variable (budget) cannot capture all the complexities of box office performance (e.g., genre, cast, marketing, release timing).

The R² value aligns with the visual impression from the regression plot: the points cluster reasonably well around the line, but there is still considerable scatter.

---

## 6. Running a Regression on Old Films (Challenge)

Now we repeat the process for the old films (pre‑1970). This allows us to compare how well budget predicts revenue in an earlier era.

```python
# Prepare data for old films
X_old = pd.DataFrame(old_films, columns=['USD_Production_Budget'])
y_old = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])

# Fit a new regression model (reusing the same object or creating a new one)
regression.fit(X_old, y_old)

# Display coefficients and R‑squared
print(f'Slope: {regression.coef_[0][0]}')
print(f'Intercept: {regression.intercept_[0]}')
print(f'R‑squared: {regression.score(X_old, y_old)}')
```

**Typical output:**

```
Slope: 1.64771314
Intercept: 22821538.635080386
R‑squared: 0.02937258620576877
```

- **Slope (θ₁):** 1.65 – each dollar spent is associated with only $1.65 in revenue, a much lower multiplier than for new films.
- **Intercept (θ₀):** $22.8 million – the predicted revenue for a zero‑budget film is positive and substantial, which is nonsensical and highlights the poor fit.
- **R‑squared:** only **2.9%** – the budget explains almost none of the variance in revenue for old films.

These numbers confirm what we saw in the regression plot: the linear model is inappropriate for the pre‑1970 era. The relationship, if any, is very weak.

---

## 7. Making Predictions with the Model

Once a model is fitted, we can use it to predict revenue for any given budget. For example, we might ask: what worldwide gross does the model (fitted on old films) predict for a film with a budget of $350 million?

Using the coefficients from the old‑films model (the last one fitted), we can compute the prediction manually:

```python
budget = 350000000
revenue_estimate = regression.intercept_[0] + regression.coef_[0, 0] * budget
print(f'Estimated revenue for a $350M film: ${revenue_estimate:.0f}')
```

**Output:** `Estimated revenue for a $350M film: $599521137`

Alternatively, we can use the model’s `.predict()` method:

```python
# Create a DataFrame for the new budget (must have the same column name as X)
new_budget = pd.DataFrame({'USD_Production_Budget': [350000000]})
prediction = regression.predict(new_budget)
print(prediction[0][0])
```

Both methods give the same result: approximately **$600 million**.

It is important to note that this prediction uses the model built on **old films**. Because that model has a very low R², its predictions are highly uncertain and should be treated with caution. For a more reliable estimate, we would use the model fitted on new films, which yields:

```
revenue_new_model = -8650768 + 3.1226 * 350000000 ≈ 1,085,000,000  (approx. $1.09 billion)
```

(Calculated from the new‑films coefficients.)

The large discrepancy between the two predictions underscores how much the industry has changed over time. Predictions should always be made using a model trained on data representative of the scenario to which it is applied.

---

## 8. Interpretation and Caveats

### 8.1 Interpreting the Intercept

The intercept (θ₀) is often not meaningful in a univariate regression when the range of the feature does not include zero. In the new‑films model, the intercept is negative, which would imply a film with zero budget loses money – an impossibility. In the old‑films model, the intercept is a large positive number, suggesting that even with no budget a film would earn $22.8 million – equally absurd. These intercepts are merely mathematical artifacts of extending the regression line leftwards beyond the data. Their primary purpose is to enable the line to fit the data optimally within the observed range.

### 8.2 The Slope as an Average Effect

The slope (θ₁) represents the average change in revenue for a unit increase in budget, assuming the linear model is correct. It does not imply causation; we cannot conclude that increasing a film’s budget *causes* higher revenue, only that they are correlated. Other factors (e.g., star power, marketing) may influence both.

### 8.3 R‑squared and Model Limitations

R‑squared tells us how much of the variance is explained by the feature. For new films, 56% is a respectable value for a simple model, but it also means 44% of the variation is unexplained. This residual variance could be due to omitted variables, measurement error, or inherent randomness in box office performance.

### 8.4 Extrapolation Danger

Predicting for a budget of $350 million using the old‑films model is an extrapolation far beyond the range of the training data (old films had budgets up to $42 million). Such predictions are highly unreliable and should be avoided in practice. The new‑films model is trained on budgets up to $425 million, so a $350 million prediction is within its range and more credible.

---

## 9. Summary of Steps

1. **Prepare the data:** Create feature DataFrame `X` and target DataFrame `y` from the relevant subset.
2. **Instantiate the model:** `regression = LinearRegression()`.
3. **Fit the model:** `regression.fit(X, y)`.
4. **Extract coefficients:** `intercept_` and `coef_`.
5. **Evaluate fit:** `regression.score(X, y)` gives R².
6. **Make predictions:** Use `.predict()` or the equation manually.

We have applied this workflow to both new and old films, confirming that budget is a meaningful predictor only for the modern era. This quantitative analysis complements the visual insights from Seaborn and provides concrete numbers that can be used for decision‑making or further study.

---

## 10. Additional Resources

- scikit‑learn documentation on [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- An introduction to [ordinary least squares](https://en.wikipedia.org/wiki/Ordinary_least_squares)
- For a deeper dive into regression diagnostics, see [Statsmodels](https://www.statsmodels.org/stable/index.html)

