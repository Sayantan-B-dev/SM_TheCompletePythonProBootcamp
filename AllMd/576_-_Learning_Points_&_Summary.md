# Learning Points & Summary

This document provides a comprehensive review of the key concepts, techniques, and insights gained during the analysis of movie budget and revenue data. The project encompassed the entire data science workflow: data cleaning, exploration, visualisation, statistical modelling, and interpretation. By working through this case study, you have acquired practical skills that are directly applicable to a wide range of real‑world datasets.

Below is a detailed summary of each major topic covered, including the relevant code examples, the rationale behind each step, and the conclusions drawn from the analysis.

---

## 1. Data Cleaning and Preparation

The raw dataset (`cost_revenue_dirty.csv`) contained several issues that needed to be addressed before any analysis could be performed.

### 1.1 Inspecting the Data

- **Shape and structure:** Used `data.shape`, `data.head()`, `data.tail()`, and `data.sample()` to understand the number of rows (5,391) and columns (6), and to get a feel for the content.
- **Missing values:** `data.isna().values.any()` confirmed there were no NaN values.
- **Duplicate rows:** `data.duplicated().values.any()` showed no duplicates.
- **Data types:** `data.info()` revealed that monetary columns were stored as objects (strings) and the release date as an object.

### 1.2 Cleaning Monetary Columns

The columns `USD_Production_Budget`, `USD_Worldwide_Gross`, and `USD_Domestic_Gross` contained dollar signs (`$`) and commas. To convert them to numeric values, a nested loop removed these characters:

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

After this, the columns became integers, ready for mathematical operations.

### 1.3 Converting Release Date to Datetime

The `Release_Date` column was converted to a proper datetime type using `pd.to_datetime()`, enabling time‑based filtering and extraction of temporal components.

```python
data.Release_Date = pd.to_datetime(data.Release_Date)
```

---

## 2. Exploratory Data Analysis

With clean data, we performed initial exploration to understand distributions and identify anomalies.

### 2.1 Descriptive Statistics

`data.describe()` provided a quick statistical summary:

- Average production budget: $31.1 million
- Average worldwide gross: $88.9 million
- Minimum budget: $1,100 (the film *My Date With Drew*)
- Maximum budget: $425 million (*Avatar*)
- 25% of films have budgets ≤ $5 million and worldwide gross ≤ $3.9 million, indicating that many low‑budget films do not break even.

### 2.2 Zero Revenue Films

We examined films that earned nothing domestically or worldwide:

- **Zero domestic:** 512 films. Many were international releases or unreleased at the time of data collection.
- **Zero worldwide:** 357 films. The difference (155 films) represents films that earned money internationally but not in the U.S.
- **Highest‑budget zero‑revenue films:** Included *Singularity* ($175M), *Aquaman* ($160M), and others with future release dates. This highlighted the need to remove unreleased films.

---

## 3. Advanced Filtering with Multiple Conditions

We learned two methods to filter DataFrames based on multiple criteria.

### 3.1 Using `.loc[]` with Bitwise Operators

```python
international_releases = data.loc[(data.USD_Domestic_Gross == 0) & 
                                  (data.USD_Worldwide_Gross != 0)]
```

This selects films that had no U.S. revenue but earned money elsewhere. Parentheses are essential because `&` has higher precedence than comparison operators.

### 3.2 Using `.query()`

```python
international_releases = data.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')
```

The `query()` method offers a more readable syntax, especially for complex conditions.

---

## 4. Handling Unreleased Films

We identified films with release dates after the data collection date (May 1, 2018) and removed them to avoid skewing the analysis.

```python
scrape_date = pd.Timestamp('2018-5-1')
future_releases = data[data.Release_Date >= scrape_date]
data_clean = data.drop(future_releases.index)
```

This left 5,384 films in the working dataset.

---

## 5. Quantifying Financial Risk

We calculated the percentage of films that failed to recoup their production budgets:

```python
money_losing = data_clean[data_clean.USD_Production_Budget > data_clean.USD_Worldwide_Gross]
loss_percentage = len(money_losing) / len(data_clean)   # ≈ 37.3%
```

Over one‑third of all released films lose money at the box office – a stark reminder of the industry’s risk.

---

## 6. Data Visualisation with Seaborn

Seaborn was introduced as a high‑level interface for drawing attractive statistical graphics.

### 6.1 Basic Scatter Plot

```python
sns.scatterplot(data=data_clean,
                x='USD_Production_Budget',
                y='USD_Worldwide_Gross')
```

### 6.2 Bubble Charts

By adding `hue` and `size` parameters, we encoded a third variable (worldwide gross) into the colour and size of the points:

```python
sns.scatterplot(data=data_clean,
                x='USD_Production_Budget',
                y='USD_Worldwide_Gross',
                hue='USD_Worldwide_Gross',
                size='USD_Worldwide_Gross')
```

### 6.3 Styling with Seaborn Themes

We used `sns.axes_style()` within a `with` statement to apply themes like `'darkgrid'` and `'whitegrid'` to individual plots.

### 6.4 Budget Over Time Bubble Chart

```python
with sns.axes_style("darkgrid"):
    sns.scatterplot(data=data_clean, 
                    x='Release_Date', 
                    y='USD_Production_Budget',
                    hue='USD_Worldwide_Gross',
                    size='USD_Worldwide_Gross')
```

This chart revealed the explosion in film budgets and output from the 1970s onwards.

---

## 7. Creating a Decade Column with Floor Division

To split the data into meaningful time periods, we converted individual years into decades.

### 7.1 Extracting Years

```python
dt_index = pd.DatetimeIndex(data_clean.Release_Date)
years = dt_index.year
```

### 7.2 Floor Division

Floor division (`//`) discards the remainder, allowing us to group years:

```python
decades = (years // 10) * 10
data_clean['Decade'] = decades
```

Now a film released in 1963 receives a `Decade` value of 1960.

### 7.3 Separating Old and New Films

```python
old_films = data_clean[data_clean.Decade <= 1960]   # pre‑1970
new_films = data_clean[data_clean.Decade > 1960]    # 1970 onward
```

Only 153 films (≈2.8%) belong to the old era; the vast majority are modern.

---

## 8. Regression Plots with Seaborn

`regplot()` combines a scatter plot with a fitted linear regression line and confidence interval.

### 8.1 Old Films

```python
sns.regplot(data=old_films,
            x='USD_Production_Budget',
            y='USD_Worldwide_Gross',
            scatter_kws={'alpha': 0.4},
            line_kws={'color': 'black'})
```

The line was nearly flat and the confidence interval wide – budget had little predictive power.

### 8.2 New Films (Styled)

```python
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

The points clustered around the line, and the confidence interval was narrow – a strong positive relationship.

---

## 9. Linear Regression with scikit‑learn

We moved beyond visualisation to quantitative modelling using `sklearn.linear_model.LinearRegression`.

### 9.1 Fitting the Model for New Films

```python
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

regression = LinearRegression()
regression.fit(X, y)
```

### 9.2 Extracting Coefficients

- **Intercept (θ₀):** `regression.intercept_` ≈ –$8.65 million
- **Slope (θ₁):** `regression.coef_` ≈ 3.12

Each additional dollar in budget is associated with about $3.12 in extra revenue.

### 9.3 R‑squared

```python
regression.score(X, y)   # ≈ 0.558
```

Budget explains 55.8% of the variance in worldwide gross – a moderate but meaningful relationship.

### 9.4 Old Films Regression

Repeating the process for `old_films` yielded:

- Slope: 1.65
- Intercept: $22.8 million
- R²: 0.029

Budget explains almost none of the variation in revenue for pre‑1970 films.

### 9.5 Making Predictions

We used the model to estimate revenue for a hypothetical $350 million film:

```python
budget = 350000000
revenue_estimate = regression.intercept_[0] + regression.coef_[0,0] * budget
print(round(revenue_estimate, -6))   # $600 million (using old‑films model)
```

(For a more realistic estimate, the new‑films model would be used, giving ≈$1.09 billion.)

---

## 10. Key Insights and Conclusions

- **Overall relationship:** For modern films (1970–present), there is a clear positive correlation between production budget and worldwide gross revenue. A $1 increase in budget is associated with a $3.12 increase in revenue on average.
- **Historical shift:** Before 1970, the relationship was very weak (R² ≈ 0.03). The film industry operated differently; low‑budget films could still achieve substantial success.
- **Financial risk:** Despite the positive correlation, 37% of films still lose money. High budgets do not guarantee profitability.
- **Data cleaning is crucial:** Removing unreleased films and correctly formatting columns was essential to avoid misleading conclusions.
- **Visualisation aids interpretation:** Bubble charts and regression plots made the patterns and outliers immediately apparent.

---

## 11. Tools and Libraries Used

- **pandas:** Data manipulation, cleaning, and filtering.
- **matplotlib:** Low‑level plotting and customisation.
- **seaborn:** High‑level statistical visualisations (scatter plots, bubble charts, regression plots).
- **scikit‑learn:** Linear regression modelling and evaluation.
- **Python datetime and pandas datetime:** Handling temporal data.

---

## 12. Further Resources

- Seaborn documentation: [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
- scikit‑learn LinearRegression: [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- Pandas documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- The dataset source: [the‑numbers.com](https://www.the-numbers.com/movie/budgets)
