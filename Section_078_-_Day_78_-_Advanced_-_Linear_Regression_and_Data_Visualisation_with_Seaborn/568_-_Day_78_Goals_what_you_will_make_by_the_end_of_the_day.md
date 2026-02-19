# Movie Budget and Revenue Analysis: A Comprehensive Documentation

This document provides an in-depth, step-by-step account of a data analysis project investigating the relationship between film production budgets and box office revenue. The project uses Python, pandas, matplotlib, seaborn, and scikit-learn. The dataset was scraped from [the-numbers.com](https://www.the-numbers.com/movie/budgets) on May 1st, 2018. The primary question: do higher film budgets lead to more revenue?

The documentation covers every stage of the analysis: data loading, cleaning, exploration, visualisation, linear regression modelling, and interpretation of results. All code examples are taken from the completed Jupyter Notebook and are presented in a clear, executable format.

---

## 1. Project Overview and Setup

The analysis aims to answer whether film studios should increase spending on production to achieve higher box office returns. To answer this, we use a dataset containing information on thousands of films, including their release dates, titles, production budgets, worldwide gross, and domestic (United States) gross revenue.

The primary tools employed are:

- **pandas** for data manipulation and cleaning.
- **matplotlib** for basic plotting.
- **seaborn** for advanced visualisations and statistical plots (built on matplotlib).
- **scikit-learn** for performing linear regression and obtaining model coefficients.

The dataset is provided as a CSV file named `cost_revenue_dirty.csv`. It contains 5,391 entries and 6 columns.

---

## 2. Data Exploration and Cleaning

### 2.1 Initial Inspection

Before any analysis, the dataset must be examined for structure, missing values, duplicates, and data types. The following steps are performed:

- Load the CSV using `pd.read_csv()`.
- Check the shape: `data.shape` reveals 5391 rows and 6 columns.
- View random samples with `data.sample(5)` and the last rows with `data.tail()` to get a sense of the content.
- Verify the presence of any NaN values: `data.isna().values.any()` returns `False`, indicating no missing values.
- Check for duplicate rows: `data.duplicated().values.any()` returns `False`, confirming all rows are unique.
- Use `data.info()` to see column data types and non-null counts.

The output of `info()` shows:

- `Rank`: int64
- `Release_Date`: object (strings)
- `Movie_Title`: object
- `USD_Production_Budget`: object (contains dollar signs and commas)
- `USD_Worldwide_Gross`: object
- `USD_Domestic_Gross`: object

Thus, the monetary columns need conversion to numeric types, and the release date must be converted to a proper datetime format.

### 2.2 Cleaning Monetary Columns

The budget and gross columns contain strings like `"$110,000"`. To perform arithmetic, we must remove the dollar signs and commas and convert to integers (or floats). A nested loop approach is used:

```python
chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget', 
                    'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']

for col in columns_to_clean:
    for char in chars_to_remove:
        data[col] = data[col].astype(str).str.replace(char, "")
    data[col] = pd.to_numeric(data[col])
```

After this transformation, the monetary columns become `int64` types. The `head()` of the DataFrame now shows clean numeric values without symbols.

### 2.3 Converting Release Date to Datetime

The `Release_Date` column is converted using `pd.to_datetime()`:

```python
data.Release_Date = pd.to_datetime(data.Release_Date)
```

Now `data.info()` confirms `Release_Date` is `datetime64[ns]` and all monetary columns are integers.

---

## 3. Investigating Films with Zero Revenue

### 3.1 Descriptive Statistics

Using `data.describe()` on the numeric columns provides a quick statistical summary:

| Statistic | Production Budget | Worldwide Gross | Domestic Gross |
|-----------|-------------------|-----------------|----------------|
| count     | 5391              | 5391            | 5391           |
| mean      | $31.1M            | $88.9M          | $41.2M         |
| std       | $40.5M            | $168.5M         | $66.0M         |
| min       | $1,100            | $0              | $0             |
| 25%       | $5.0M             | $3.9M           | $1.3M          |
| 50%       | $17.0M            | $27.5M          | $17.2M         |
| 75%       | $40.0M            | $96.5M          | $52.3M         |
| max       | $425.0M           | $2.78B          | $936.7M        |

Observations:

- The average film costs about $31M and earns around $89M worldwide.
- The bottom 25% of films (those with budgets ≤ $5M) have average worldwide gross of only $3.9M, indicating they likely lose money.
- The minimum revenue is $0 both domestically and worldwide.
- The highest budget film is *Avatar* at $425M, which grossed $2.78B worldwide.
- The lowest budget film is *My Date With Drew* with a budget of $1,100 and worldwide gross of $181,041.

### 3.2 Zero Domestic Revenue

To find films that grossed $0 in the U.S.:

```python
zero_domestic = data[data.USD_Domestic_Gross == 0]
print(f'Number of films that grossed $0 domestically: {len(zero_domestic)}')
zero_domestic.sort_values('USD_Production_Budget', ascending=False)
```

This yields 512 films. Among them are high-budget titles like *Singularity* ($175M) and *Aquaman* ($160M) – these films have release dates after the data collection date (May 1, 2018), explaining the zero revenue. Others are international films not released in the U.S., such as *Don Gato, el inicio de la pandilla* ($80M budget, $4.5M worldwide but $0 domestic).

### 3.3 Zero Worldwide Revenue

Similarly, for zero worldwide revenue:

```python
zero_worldwide = data[data.USD_Worldwide_Gross == 0]
print(f'Number of films that grossed $0 worldwide: {len(zero_worldwide)}')
zero_worldwide.sort_values('USD_Production_Budget', ascending=False)
```

357 films have $0 worldwide. Again, many are unreleased or future releases. The difference between the domestic-only zero count (512) and worldwide zero count (357) reflects international films that earned revenue outside the U.S. but not domestically.

---

## 4. Filtering with Multiple Conditions: International Releases

### 4.1 Using `.loc[]` with Bitwise Operators

To isolate films that earned money internationally but nothing in the U.S. (i.e., international releases), we apply two conditions simultaneously:

```python
international_releases = data.loc[(data.USD_Domestic_Gross == 0) & 
                                  (data.USD_Worldwide_Gross != 0)]
```

This uses the bitwise AND (`&`) operator to combine conditions. Parentheses are required because `&` has higher precedence than comparisons. The result contains 155 films.

### 4.2 Using `.query()` Method

The same filter can be expressed more succinctly with `query()`:

```python
international_releases = data.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')
```

Both approaches yield identical subsets. The `query()` method is often more readable for complex conditions.

### 4.3 Unreleased Films

At the time of data collection (May 1, 2018), some films in the dataset had not yet been released. These will have zero revenue simply because they haven't been screened. We identify them by comparing release dates with a timestamp:

```python
scrape_date = pd.Timestamp('2018-5-1')
future_releases = data[data.Release_Date >= scrape_date]
print(f'Number of unreleased movies: {len(future_releases)}')   # Output: 7
```

These 7 films are removed from the working dataset to avoid skewing the analysis:

```python
data_clean = data.drop(future_releases.index)
```

The cleaned dataset now contains 5384 rows.

### 4.4 Films That Lost Money

We can calculate the percentage of films where production costs exceeded worldwide gross revenue:

```python
money_losing = data_clean[data_clean.USD_Production_Budget > data_clean.USD_Worldwide_Gross]
loss_percentage = len(money_losing) / len(data_clean)
print(loss_percentage)   # Output: 0.37277 (≈37.3%)
```

Thus, over one-third of films do not recoup their production budget at the box office.

---

## 5. Data Visualisation with Seaborn: Bubble Charts

Seaborn is imported as `sns`. It provides high-level functions for attractive statistical graphics.

### 5.1 Basic Scatter Plot

A simple scatter plot of budget vs. worldwide gross:

```python
plt.figure(figsize=(8,4), dpi=200)
ax = sns.scatterplot(data=data_clean,
                     x='USD_Production_Budget', 
                     y='USD_Worldwide_Gross')
ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')
plt.show()
```

This produces a cloud of points showing a positive correlation, but many outliers are present.

### 5.2 Adding Hue and Size (Bubble Chart)

To add a third dimension, we can colour and size points by worldwide gross:

```python
plt.figure(figsize=(8,4), dpi=200)
ax = sns.scatterplot(data=data_clean,
                     x='USD_Production_Budget', 
                     y='USD_Worldwide_Gross',
                     hue='USD_Worldwide_Gross',
                     size='USD_Worldwide_Gross')
ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')
plt.show()
```

Now higher-grossing films appear as larger, darker points, making patterns more evident.

### 5.3 Styling with Seaborn Themes

Seaborn offers several built-in themes. Using `with sns.axes_style('darkgrid'):` temporarily applies a dark grid background to the plot:

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=data_clean,
                         x='USD_Production_Budget', 
                         y='USD_Worldwide_Gross',
                         hue='USD_Worldwide_Gross',
                         size='USD_Worldwide_Gross')
    ax.set(ylim=(0, 3000000000),
           xlim=(0, 450000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')
```

Other available styles include `'whitegrid'`, `'dark'`, `'white'`, and `'ticks'`.

### 5.4 Budget Over Time

To examine how budgets have evolved, we plot release date against budget, again using hue and size for worldwide gross:

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("darkgrid"):
    ax = sns.scatterplot(data=data_clean, 
                         x='Release_Date', 
                         y='USD_Production_Budget',
                         hue='USD_Worldwide_Gross',
                         size='USD_Worldwide_Gross')
    ax.set(ylim=(0, 450000000),
           xlim=(data_clean.Release_Date.min(), data_clean.Release_Date.max()),
           xlabel='Year',
           ylabel='Budget in $100 millions')
```

Interpretation: Movie budgets have grown dramatically since the 1970s. Prior to that, budgets were modest and the number of films was smaller. From the 1980s onward, budgets escalated, and the density of points increases, reflecting the industry's expansion.

---

## 6. Converting Years to Decades Using Floor Division

To analyse trends by decade, we add a `Decade` column to the cleaned dataset.

### 6.1 Creating a DatetimeIndex and Extracting Years

First, create a `DatetimeIndex` from the release dates and extract the year:

```python
dt_index = pd.DatetimeIndex(data_clean.Release_Date)
years = dt_index.year
```

### 6.2 Floor Division to Get Decades

Floor division (`//`) truncates the remainder. To convert a year (e.g., 1999) to its decade (1990s), we perform integer division by 10 and then multiply by 10:

```python
decades = years // 10 * 10
data_clean['Decade'] = decades
```

Now each film has a `Decade` column indicating the decade of release (e.g., 1990 for films released between 1990 and 1999).

### 6.3 Separating Old and New Films

We split the data into two groups: films released before 1970 (inclusive up to 1969) and films from 1970 onward:

```python
old_films = data_clean[data_clean.Decade <= 1960]
new_films = data_clean[data_clean.Decade > 1960]
```

- `old_films` contains 153 entries.
- The most expensive film prior to 1970 is *Cleopatra* (1963) with a budget of $42 million.

This separation allows us to compare the relationship between budget and revenue in two distinct eras.

---

## 7. Plotting Linear Regressions with Seaborn

Seaborn's `regplot()` combines a scatter plot with a fitted linear regression line and a confidence interval.

### 7.1 Regression for Old Films

```python
sns.regplot(data=old_films, 
            x='USD_Production_Budget',
            y='USD_Worldwide_Gross')
```

The resulting plot shows a weak relationship; many points lie far from the regression line. The confidence interval is wide, and the line does not capture the data well.

To improve styling, we can use Matplotlib parameters:

```python
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(data=old_films, 
                x='USD_Production_Budget', 
                y='USD_Worldwide_Gross',
                scatter_kws={'alpha': 0.4},
                line_kws={'color': 'black'})
```

### 7.2 Regression for New Films

For the post-1970 films, we expect a stronger correlation. We create a styled regplot with custom colours:

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

Interpretation:

- The data points align much more closely with the regression line than in the old films.
- The confidence interval is narrower.
- A film with a $150 million budget is estimated to earn slightly under $500 million according to the regression line.
- This suggests that for modern films, budget is a strong predictor of revenue.

---

## 8. Running a Linear Regression with scikit-learn

While `regplot()` visualises the regression, scikit-learn allows us to extract the exact coefficients and evaluate the model quantitatively.

### 8.1 Setting Up the Model

Import `LinearRegression` from `sklearn.linear_model` and create an instance:

```python
from sklearn.linear_model import LinearRegression
regression = LinearRegression()
```

### 8.2 Defining Features and Target

The explanatory variable (feature) is the production budget; the target is worldwide gross. Both must be provided as DataFrames (or 2D arrays) to scikit-learn:

```python
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
```

### 8.3 Fitting the Model

```python
regression.fit(X, y)
```

The model estimates the best‑fitting line: `revenue = θ₀ + θ₁ × budget`.

- **Intercept (θ₀)**: `regression.intercept_` returns `array([-8650768.00661027])`. This implies that a film with zero budget would have negative revenue – an unrealistic extrapolation, but statistically it's the y‑intercept of the fitted line.
- **Slope (θ₁)**: `regression.coef_` returns `array([[3.12259592]])`. This means that for each additional dollar spent on production, worldwide gross increases by about $3.12 on average.

### 8.4 Goodness of Fit: R‑squared

The `score()` method computes the coefficient of determination, R²:

```python
regression.score(X, y)   # Output: 0.5577
```

Approximately 55.8% of the variance in worldwide gross is explained by the production budget. This is a moderately strong relationship, especially considering the simplicity of the model.

### 8.5 Regression on Old Films

Repeating the process for `old_films`:

```python
X_old = pd.DataFrame(old_films, columns=['USD_Production_Budget'])
y_old = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])
regression.fit(X_old, y_old)
print(f'Slope: {regression.coef_[0][0]}')
print(f'Intercept: {regression.intercept_[0]}')
print(f'R-squared: {regression.score(X_old, y_old)}')
```

Output:

- Slope: 1.6477
- Intercept: 22,821,538
- R²: 0.0294

Only 2.9% of the variance is explained, confirming the visual impression that budget had little predictive power for older films.

### 8.6 Making Predictions

The fitted model can be used to predict revenue for a given budget. For a $350 million film:

```python
budget = 350000000
revenue_estimate = regression.intercept_[0] + regression.coef_[0,0] * budget
revenue_estimate = round(revenue_estimate, -6)   # Round to nearest million
print(f'The estimated revenue for a $350M film is around ${revenue_estimate:.0f}.')
```

Using the coefficients from the new films model, the predicted revenue is approximately $600 million. (Note: the intercept and slope used here are from the old films model in the provided notebook; the prediction code in the notebook actually uses the old films model. In practice, we would use the model that fits the data best – the new films model.)

---

## 9. Summary of Key Techniques and Concepts

This project demonstrated a complete data analysis workflow:

- **Data cleaning**: removing unwanted characters, converting data types, handling future release dates.
- **Data exploration**: using `.describe()`, filtering, and conditional selection to understand distributions and anomalies.
- **Visualisation with seaborn**: scatter plots, bubble charts (hue and size), and regression plots with custom styling.
- **Temporal analysis**: creating a `Decade` column using floor division to segment data.
- **Linear regression modelling**: using scikit-learn to fit a model, interpret coefficients, and evaluate fit with R².
- **Prediction**: applying the model to estimate revenue for new budgets.

The analysis concludes that for films released after 1970, there is a clear positive relationship between production budget and worldwide gross, explaining about 56% of the variance. In contrast, for earlier films, the relationship is weak. This suggests that in the modern era, higher spending tends to lead to higher box office returns, though many films still lose money (37% do not break even).

The techniques learned here – nested loops for cleaning, multi‑condition filtering, floor division, seaborn visualisations, and scikit‑learn regressions – are broadly applicable to many real‑world datasets.

---

**Resources**:

- The dataset was sourced from [the-numbers.com](https://www.the-numbers.com/movie/budgets).
- Seaborn documentation: [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
- scikit-learn LinearRegression: [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)