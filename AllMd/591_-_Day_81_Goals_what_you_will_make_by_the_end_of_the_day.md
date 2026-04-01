## Multivariable Regression and Valuation Model – Complete Documentation

This document provides an **extremely detailed** walkthrough of the Boston housing project, explaining every line of code, function, method, and concept. Use this as a future reference for multivariable regression, data exploration, model evaluation, and data transformation.

---

### 1. Project Overview

**Goal:** Build a regression model to estimate the median value of owner-occupied homes in Boston (1970s) based on 13 features.  
**Dataset:** Boston house prices (506 samples, 13 features + target).  
**Steps:**  
- Load and explore data  
- Visualise relationships  
- Split into training/testing sets  
- Fit linear regression  
- Evaluate coefficients and residuals  
- Apply log transformation to improve model  
- Compare models and predict a new property’s value  

---

### 2. Environment Setup

#### Cell: Upgrade plotly (optional for Google Colab)
```python
# %pip install --upgrade plotly
```
- **Purpose:** Ensures the latest version of `plotly` is installed (uncomment if running in Google Colab).  
- **Why:** Older Colab versions may have an outdated plotly; upgrading guarantees compatibility with the code.

#### Cell: Import Statements
```python
import pandas as pd
import numpy as np

import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
```
- **pandas (`pd`)** : Data manipulation and analysis (DataFrames).  
- **numpy (`np`)** : Numerical operations (arrays, mathematical functions).  
- **seaborn (`sns`)** : Statistical data visualization (built on matplotlib).  
- **plotly.express (`px`)** : High‑level interface for creating interactive plots.  
- **matplotlib.pyplot (`plt`)** : Base plotting library.  
- **sklearn.linear_model.LinearRegression** : Ordinary least squares linear regression.  
- **sklearn.model_selection.train_test_split** : Splits arrays/matrices into random train and test subsets.

#### Cell: Notebook Presentation
```python
pd.options.display.float_format = '{:,.2f}'.format
```
- **Purpose:** Sets pandas to display floating-point numbers with two decimal places and thousand separators.  
- **Effect:** Makes printed tables cleaner and easier to read (e.g., `12345.6789` → `12,345.68`).

---

### 3. Data Loading

#### Cell: Load the Data
```python
data = pd.read_csv('boston.csv', index_col=0)
```
- **`pd.read_csv()`** : Reads a CSV file into a DataFrame.  
  - `'boston.csv'` : filename (assumed in same directory).  
  - `index_col=0` : Use the first column (row numbers) as the DataFrame index.  
- **Result:** `data` is a DataFrame with 506 rows and 14 columns (13 features + target `PRICE`).

---

### 4. Preliminary Data Exploration

#### Cell: Check shape
```python
data.shape
```
- **Output:** `(506, 14)`  
- **Explanation:** `DataFrame.shape` returns a tuple (rows, columns). Confirms 506 samples and 14 variables.

#### Cell: Check column names
```python
data.columns
```
- **Output:** `Index(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'PRICE'], dtype='object')`  
- **Explanation:** Lists all feature names and the target `PRICE`.

#### Cell: View first few rows
```python
data.head()
```
- **Output:** First 5 rows (as a table).  
- **Explanation:** `.head()` shows a quick preview to verify data loaded correctly.

#### Cell: View last few rows
```python
data.tail()
```
- **Output:** Last 5 rows.  
- **Explanation:** Useful to check for consistency at the end.

#### Cell: Count non‑null values
```python
data.count()
```
- **Output:** Series with counts per column (all 506).  
- **Explanation:** Verifies no missing values.

#### Cell: Check for NaN values
```python
print(f'Any NaN values? {data.isna().values.any()}')
```
- **`data.isna()`** : Returns boolean DataFrame where True indicates missing.  
- **`.values.any()`** : Flattens to 1D array and checks if any True exists.  
- **Output:** `Any NaN values? False` → confirms no missing data.

#### Cell: Check for duplicates
```python
print(f'Any duplicates? {data.duplicated().values.any()}')
```
- **`data.duplicated()`** : Returns boolean Series indicating duplicate rows (first occurrence marked False, subsequent duplicates True).  
- **`.values.any()`** : Checks if any duplicate exists.  
- **Output:** `Any duplicates? False` → no duplicate rows.

---

### 5. Descriptive Statistics

#### Cell: Generate summary statistics
```python
data.describe()
```
- **Output:** Table with count, mean, std, min, 25%, 50%, 75%, max for each numeric column.  
- **Interpretation:**  
  - `PTRATIO` (pupil‑teacher ratio) average ≈ 18.46.  
  - `PRICE` average ≈ 22.53 ($22,530).  
  - `CHAS` (Charles River dummy) min=0, max=1, mean=0.07 → only 7% of homes are next to river.  
  - `RM` (rooms) ranges from 3.56 to 8.78, average 6.28.

---

### 6. Data Visualisation

#### Markdown: Visualise the Features
- Instructions to create distribution plots for `PRICE`, `DIS`, `RM`, `RAD`.

#### Cell: House Prices (PRICE)
```python
sns.displot(data['PRICE'], 
            bins=50, 
            aspect=2,
            kde=True, 
            color='#2196f3')

plt.title(f'1970s Home Values in Boston. Average: ${(1000*data.PRICE.mean()):.6}')
plt.xlabel('Price in 000s')
plt.ylabel('Nr. of Homes')

plt.show()
```
- **`sns.displot()`** : Figure‑level interface for distribution plots (histogram + KDE).  
  - `bins=50` : number of histogram bins.  
  - `aspect=2` : width/height ratio (makes plot wider).  
  - `kde=True` : overlay kernel density estimate.  
  - `color='#2196f3'` : fill colour.  
- **`plt.title()`** : Adds title; uses f‑string to display average price (in dollars).  
- **`plt.xlabel()`**, `plt.ylabel()` : axis labels.  
- **Observation:** Right tail spike at $50,000 → possible data censoring.

#### Cell: Distance to Employment (DIS)
```python
sns.displot(data.DIS, 
            bins=50, 
            aspect=2,
            kde=True, 
            color='darkblue')

plt.title(f'Distance to Employment Centres. Average: {(data.DIS.mean()):.2}')
plt.xlabel('Weighted Distance to 5 Boston Employment Centres')
plt.ylabel('Nr. of Homes')

plt.show()
```
- Similar to above; shows most homes are within ~3.8 miles.

#### Cell: Number of Rooms (RM)
```python
sns.displot(data.RM, 
            aspect=2,
            kde=True, 
            color='#00796b')

plt.title(f'Distribution of Rooms in Boston. Average: {data.RM.mean():.2}')
plt.xlabel('Average Number of Rooms')
plt.ylabel('Nr. of Homes')

plt.show()
```
- Distribution roughly normal, centered around 6.28 rooms.

#### Cell: Access to Highways (RAD)
```python
plt.figure(figsize=(10, 5), dpi=200)

plt.hist(data['RAD'], 
         bins=24, 
         ec='black', 
         color='#7b1fa2', 
         rwidth=0.5)

plt.xlabel('Accessibility to Highways')
plt.ylabel('Nr. of Houses')
plt.show()
```
- **`plt.figure(figsize=(10,5), dpi=200)`** : Creates a new figure with specific size and resolution.  
- **`plt.hist()`** : Plots a histogram.  
  - `bins=24` : 24 bins (RAD ranges from 1 to 24).  
  - `ec='black'` : edge colour of bars.  
  - `rwidth=0.5` : relative width of bars (0.5 leaves gaps).  
- Shows that RAD is not continuous; there are gaps in the index.

#### Cell: Next to the River (CHAS) – bar chart with plotly
```python
river_access = data['CHAS'].value_counts()

bar = px.bar(x=['No', 'Yes'],
             y=river_access.values,
             color=river_access.values,
             color_continuous_scale=px.colors.sequential.haline,
             title='Next to Charles River?')

bar.update_layout(xaxis_title='Property Located Next to the River?', 
                  yaxis_title='Number of Homes',
                  coloraxis_showscale=False)
bar.show()
```
- **`data['CHAS'].value_counts()`** : Counts occurrences of 0 and 1. Returns Series with index=0,1.  
- **`px.bar()`** : Creates an interactive bar chart.  
  - `x=['No','Yes']` : custom x‑axis labels.  
  - `y=river_access.values` : counts for each category.  
  - `color` : colour bars based on the counts.  
  - `color_continuous_scale` : colour palette.  
- **`update_layout()`** : Adjusts axis titles and hides colour scale.  
- **Output:** Shows 471 homes not next to river, 35 next to it.

---

### 7. Understanding Relationships – Pair Plot

#### Cell: Pair Plot
```python
sns.pairplot(data)
plt.show()
```
- **`sns.pairplot()`** : Creates a matrix of scatter plots for every pair of columns, with histograms on the diagonal.  
- **Purpose:** Quickly visualise relationships (linear, nonlinear, outliers) between all variables.  
- **Observation:** For example, `NOX` vs `DIS` shows negative correlation; `RM` vs `PRICE` positive; `LSTAT` vs `PRICE` negative.

#### Markdown: Predictions before joint plots
- Prompts user to hypothesise relationships.

#### Cell: Jointplot – DIS vs NOX
```python
with sns.axes_style('darkgrid'):
  sns.jointplot(x=data['DIS'], 
                y=data['NOX'], 
                height=8, 
                kind='scatter',
                color='deeppink', 
                joint_kws={'alpha':0.5})
plt.show()
```
- **`sns.axes_style('darkgrid')`** : Temporarily sets seaborn style.  
- **`sns.jointplot()`** : Combines scatter plot with marginal histograms.  
  - `height=8` : size of the figure.  
  - `kind='scatter'` : type of joint plot.  
  - `joint_kws={'alpha':0.5}` : transparency of points.  
- **Interpretation:** As distance to employment increases, pollution decreases (negative correlation).

#### Cell: Jointplot – NOX vs INDUS
```python
with sns.axes_style('darkgrid'):
  sns.jointplot(x=data.NOX, 
                y=data.INDUS, 
                height=7, 
                color='darkgreen',
                joint_kws={'alpha':0.5})
plt.show()
```
- Shows strong positive correlation: more industry → higher pollution.

#### Cell: Jointplot – LSTAT vs RM
```python
with sns.axes_style('darkgrid'):
  sns.jointplot(x=data['LSTAT'], 
                y=data['RM'], 
                height=7, 
                color='orange',
                joint_kws={'alpha':0.5})
plt.show()
```
- Negative correlation: lower % lower status (wealthier areas) tend to have more rooms.

#### Cell: Jointplot – LSTAT vs PRICE
```python
with sns.axes_style('darkgrid'):
  sns.jointplot(x=data.LSTAT, 
                y=data.PRICE, 
                height=7, 
                color='crimson',
                joint_kws={'alpha':0.5})
plt.show()
```
- Strong negative correlation: poverty reduces home prices.

#### Cell: Jointplot – RM vs PRICE
```python
with sns.axes_style('whitegrid'):
  sns.jointplot(x=data.RM, 
                y=data.PRICE, 
                height=7, 
                color='darkblue',
                joint_kws={'alpha':0.5})
plt.show()
```
- Positive correlation: more rooms → higher price.

---

### 8. Train‑Test Split

#### Cell: Create train/test subsets
```python
target = data['PRICE']
features = data.drop('PRICE', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, 
                                                    target, 
                                                    test_size=0.2, 
                                                    random_state=10)
```
- **`target`** : Series containing the dependent variable.  
- **`features`** : DataFrame of independent variables (drop `PRICE` column, axis=1 for column removal).  
- **`train_test_split()`** :  
  - `features`, `target` : input data.  
  - `test_size=0.2` : 20% for testing, 80% for training.  
  - `random_state=10` : seed for reproducibility (ensures same split each run).  
- **Returns:** 4 subsets: `X_train` (features train), `X_test` (features test), `y_train` (target train), `y_test` (target test).

#### Cell: Print percentages
```python
train_pct = 100*len(X_train)/len(features)
print(f'Training data is {train_pct:.3}% of the total data.')

test_pct = 100*X_test.shape[0]/features.shape[0]
print(f'Test data makes up the remaining {test_pct:0.3}%.')
```
- **`len(X_train)`** : number of training samples (404).  
- **`len(features)`** : total samples (506).  
- **`X_test.shape[0]`** : number of test samples (102).  
- **Output:** ~79.8% train, 20.2% test.

---

### 9. First Multivariable Regression

#### Cell: Fit linear regression on training data
```python
regr = LinearRegression()
regr.fit(X_train, y_train)
rsquared = regr.score(X_train, y_train)

print(f'Training data r-squared: {rsquared:.2}')
```
- **`LinearRegression()`** : Creates a linear regression model object.  
- **`.fit(X_train, y_train)`** : Estimates coefficients using ordinary least squares.  
- **`.score(X_train, y_train)`** : Returns R‑squared (coefficient of determination) for the training data.  
  - R² = 1 – (sum of squared residuals / total sum of squares).  
- **Output:** R² ≈ 0.75 → 75% of variance explained.

#### Cell: Display coefficients
```python
regr_coef = pd.DataFrame(data=regr.coef_, index=X_train.columns, columns=['Coefficient'])
regr_coef
```
- **`regr.coef_`** : Array of fitted coefficients (one per feature).  
- **`pd.DataFrame()`** : Wraps coefficients in a DataFrame with feature names as index.  
- **Output:** Table with coefficients.  
  - `RM` positive (3.11) → extra room adds ~$3,110.  
  - `LSTAT` negative (-0.58) → poverty reduces price.  
  - Signs match expectations.

#### Cell: Premium for extra room
```python
premium = regr_coef.loc['RM'].values[0] * 1000
print(f'The price premium for having an extra room is ${premium:.5}')
```
- Extracts RM coefficient and multiplies by 1000 (since price is in $1000s).  
- **Output:** `$3108.5`.

#### Cell: Compute predictions and residuals
```python
predicted_vals = regr.predict(X_train)
residuals = (y_train - predicted_vals)
```
- **`.predict(X_train)`** : Generates predicted prices for training data.  
- **Residuals** = actual – predicted (errors).

#### Cell: Scatter plots – Actual vs Predicted & Residuals vs Predicted
```python
plt.figure(dpi=100)
plt.scatter(x=y_train, y=predicted_vals, c='indigo', alpha=0.6)
plt.plot(y_train, y_train, color='cyan')
plt.title(f'Actual vs Predicted Prices: $y _i$ vs $\hat y_i$', fontsize=17)
plt.xlabel('Actual prices 000s $y _i$', fontsize=14)
plt.ylabel('Prediced prices 000s $\hat y _i$', fontsize=14)
plt.show()

plt.figure(dpi=100)
plt.scatter(x=predicted_vals, y=residuals, c='indigo', alpha=0.6)
plt.title('Residuals vs Predicted Values', fontsize=17)
plt.xlabel('Predicted Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()
```
- First plot: points should lie near the diagonal line (perfect predictions).  
- Second plot: residuals should be randomly scattered around zero (no pattern).  
- **Observation:** Some pattern may exist, indicating possible non‑linearity.

#### Cell: Distribution of residuals
```python
resid_mean = round(residuals.mean(), 2)
resid_skew = round(residuals.skew(), 2)

sns.displot(residuals, kde=True, color='indigo')
plt.title(f'Residuals Skew ({resid_skew}) Mean ({resid_mean})')
plt.show()
```
- **`.mean()`** : average residual (should be near zero).  
- **`.skew()`** : measure of asymmetry (0 = symmetric).  
- **Output:** Skew ≈ 1.46 → residuals are right‑skewed, not ideal.

---

### 10. Data Transformation – Log Prices

#### Markdown: Why log transform?
- Target `PRICE` is right‑skewed; log transformation can make distribution more normal and improve model fit.

#### Cell: Check skew of original prices
```python
tgt_skew = data['PRICE'].skew()
sns.displot(data['PRICE'], kde='kde', color='green')
plt.title(f'Normal Prices. Skew is {tgt_skew:.3}')
plt.show()
```
- Skew ≈ 1.11 (positive skew).

#### Cell: Apply log transform
```python
y_log = np.log(data['PRICE'])
sns.displot(y_log, kde=True)
plt.title(f'Log Prices. Skew is {y_log.skew():.3}')
plt.show()
```
- **`np.log()`** : natural logarithm.  
- New skew ≈ 0.12 → much closer to zero.

#### Cell: Visualise mapping
```python
plt.figure(dpi=150)
plt.scatter(data.PRICE, np.log(data.PRICE))
plt.title('Mapping the Original Price to a Log Price')
plt.ylabel('Log Price')
plt.xlabel('Actual $ Price in 000s')
plt.show()
```
- Shows compression of high prices.

---

### 11. Regression with Log Prices

#### Cell: Train/test split with log target
```python
new_target = np.log(data['PRICE'])
features = data.drop('PRICE', axis=1)

X_train, X_test, log_y_train, log_y_test = train_test_split(features, 
                                                    new_target, 
                                                    test_size=0.2, 
                                                    random_state=10)

log_regr = LinearRegression()
log_regr.fit(X_train, log_y_train)
log_rsquared = log_regr.score(X_train, log_y_train)

log_predictions = log_regr.predict(X_train)
log_residuals = (log_y_train - log_predictions)

print(f'Training data r-squared: {log_rsquared:.2}')
```
- **`new_target`** : log‑transformed prices.  
- Same random_state ensures comparable split.  
- **Output:** R² ≈ 0.79 → improvement from 0.75.

#### Cell: Display coefficients
```python
df_coef = pd.DataFrame(data=log_regr.coef_, index=X_train.columns, columns=['coef'])
df_coef
```
- Coefficients now represent the change in **log(price)** per unit change in feature.  
  - Interpretation: e.g., `CHAS` = 0.08 → being next to river increases log price by 0.08, i.e., price multiplied by exp(0.08) ≈ 1.083 (8.3% increase).  
  - Signs remain consistent.

#### Cell: Compare side‑by‑side plots
```python
# Graph of Actual vs. Predicted Log Prices
plt.scatter(x=log_y_train, y=log_predictions, c='navy', alpha=0.6)
plt.plot(log_y_train, log_y_train, color='cyan')
plt.title(f'Actual vs Predicted Log Prices: $y _i$ vs $\hat y_i$ (R-Squared {log_rsquared:.2})', fontsize=17)
plt.xlabel('Actual Log Prices $y _i$', fontsize=14)
plt.ylabel('Prediced Log Prices $\hat y _i$', fontsize=14)
plt.show()

# Original Regression of Actual vs. Predicted Prices
plt.scatter(x=y_train, y=predicted_vals, c='indigo', alpha=0.6)
plt.plot(y_train, y_train, color='cyan')
plt.title(f'Original Actual vs Predicted Prices: $y _i$ vs $\hat y_i$ (R-Squared {rsquared:.3})', fontsize=17)
plt.xlabel('Actual prices 000s $y _i$', fontsize=14)
plt.ylabel('Prediced prices 000s $\hat y _i$', fontsize=14)
plt.show()

# Residuals vs Predicted values (Log prices)
plt.scatter(x=log_predictions, y=log_residuals, c='navy', alpha=0.6)
plt.title('Residuals vs Fitted Values for Log Prices', fontsize=17)
plt.xlabel('Predicted Log Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# Residuals vs Predicted values (Original)
plt.scatter(x=predicted_vals, y=residuals, c='indigo', alpha=0.6)
plt.title('Original Residuals vs Fitted Values', fontsize=17)
plt.xlabel('Predicted Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()
```
- Plots allow visual comparison: log model shows tighter clustering around diagonal and more random residuals.

#### Cell: Residual distribution for log model
```python
log_resid_mean = round(log_residuals.mean(), 2)
log_resid_skew = round(log_residuals.skew(), 2)

sns.displot(log_residuals, kde=True, color='navy')
plt.title(f'Log price model: Residuals Skew ({log_resid_skew}) Mean ({log_resid_mean})')
plt.show()

sns.displot(residuals, kde=True, color='indigo')
plt.title(f'Original model: Residuals Skew ({resid_skew}) Mean ({resid_mean})')
plt.show()
```
- Log model residuals skew ≈ 0.09 (near zero), mean ≈ 0.00.  
- Original model skew ≈ 1.46. Log transformation greatly improved normality.

---

### 12. Out‑of‑Sample Performance

#### Cell: Compare test set R²
```python
print(f'Original Model Test Data r-squared: {regr.score(X_test, y_test):.2}')
print(f'Log Model Test Data r-squared: {log_regr.score(X_test, log_y_test):.2}')
```
- **Output:** Original ≈ 0.67, Log ≈ 0.74.  
- Log model performs better on unseen data.  
- Test R² is lower than training R² (expected due to overfitting).

---

### 13. Predict a New Property Value

#### Cell: Create average property stats
```python
features = data.drop(['PRICE'], axis=1)
average_vals = features.mean().values
property_stats = pd.DataFrame(data=average_vals.reshape(1, len(features.columns)), 
                              columns=features.columns)
property_stats
```
- **`features.mean()`** : mean of each feature (as Series).  
- **`.values`** : convert to numpy array.  
- **`.reshape(1, len(features.columns))`** : make it a single row.  
- **`pd.DataFrame()`** : wrap with original column names.  
- **Result:** DataFrame with one row of average feature values.

#### Cell: Predict average property price
```python
log_estimate = log_regr.predict(property_stats)[0]
print(f'The log price estimate is ${log_estimate:.3}')

dollar_est = np.e**log_estimate * 1000
# or use
dollar_est = np.exp(log_estimate) * 1000
print(f'The property is estimated to be worth ${dollar_est:.6}')
```
- **`log_regr.predict(property_stats)`** : returns array of predictions (here one value).  
- **`[0]`** : extract the scalar.  
- **`np.exp(log_estimate)`** : reverse log transformation. Multiply by 1000 because prices are in $1000s.  
- **Output:** ~$20,700.

#### Cell: Define custom property characteristics
```python
next_to_river = True
nr_rooms = 8
students_per_classroom = 20 
distance_to_town = 5
pollution = data.NOX.quantile(q=0.75) # high
amount_of_poverty =  data.LSTAT.quantile(q=0.25) # low
```
- Set desired values.  
- **`quantile(q=0.75)`** : 75th percentile (high pollution).  
- **`quantile(q=0.25)`** : 25th percentile (low poverty).

#### Cell: Modify property_stats with new values
```python
property_stats['RM'] = nr_rooms
property_stats['PTRATIO'] = students_per_classroom
property_stats['DIS'] = distance_to_town

if next_to_river:
    property_stats['CHAS'] = 1
else:
    property_stats['CHAS'] = 0

property_stats['NOX'] = pollution
property_stats['LSTAT'] = amount_of_poverty
```
- Overwrites the average values with the custom ones.

#### Cell: Predict custom property
```python
log_estimate = log_regr.predict(property_stats)[0]
print(f'The log price estimate is ${log_estimate:.3}')

dollar_est = np.e**log_estimate * 1000
print(f'The property is estimated to be worth ${dollar_est:.6}')
```
- **Output:** ~$25,800.  
- This matches intuition: more rooms, better location (river, low poverty) increase price despite higher pollution.

---

### Summary of Key Concepts

- **Multivariable Linear Regression** : Models relationship between multiple features and a continuous target.  
- **R‑squared** : Proportion of variance explained by model.  
- **Coefficients** : Magnitude and sign indicate direction and strength of each feature's effect.  
- **Residuals** : Errors; should be randomly distributed with mean 0.  
- **Skewness** : Measure of asymmetry; log transformation can reduce skew and improve model fit.  
- **Train‑Test Split** : Essential for evaluating out‑of‑sample performance.  
- **`sklearn`** : Provides `LinearRegression`, `train_test_split`.  
- **Visualisation** : `seaborn` (displot, jointplot, pairplot), `plotly` (interactive bar), `matplotlib` (hist, scatter).

