# Converting Years to Decades Using Floor Division

This document provides a detailed explanation of how to transform individual release years into decade groupings using floor division (integer division) in Python with pandas. Creating a decade column allows for temporal segmentation of the data, enabling comparative analysis between different eras—in this case, comparing films released before 1970 with those released from 1970 onward. This step is crucial for understanding how the relationship between budget and revenue has changed over time.

The analysis uses the cleaned DataFrame `data_clean`, which contains 5,384 films after removing unreleased titles. The `Release_Date` column is already in datetime format, making it straightforward to extract year information.

---

## 1. Motivation for Creating a Decade Column

The bubble chart showing movie budgets over time revealed a dramatic shift starting in the 1970s:

- Prior to 1970, films were relatively few, budgets were modest, and the industry operated differently.
- From 1970 onwards, the number of films exploded, budgets escalated rapidly, and the correlation between budget and revenue appeared much stronger.

To formally test whether the relationship between budget and revenue differs between these two periods, we need to split the dataset into two groups: "old" films (pre‑1970) and "new" films (1970 and later). Creating a `Decade` column simplifies this segmentation.

---

## 2. Extracting Years from the Release Date

The first step is to extract the year from each film's release date. Pandas provides a convenient way to do this by creating a `DatetimeIndex` object from the `Release_Date` column and then accessing its `.year` property.

```python
# Create a DatetimeIndex from the Release_Date column
dt_index = pd.DatetimeIndex(data_clean.Release_Date)

# Extract the year from each date
years = dt_index.year
```

**What happens:**

- `pd.DatetimeIndex(data_clean.Release_Date)` converts the Series of datetime objects into a specialized index that offers date-related attributes.
- `.year` retrieves the year component for each element, returning a NumPy array or pandas Series of integers.

For example, if a film was released on `1963-12-06`, the corresponding year would be `1963`.

---

## 3. Converting Years to Decades with Floor Division

To convert a year like 1963 into the decade 1960, we use floor division (also called integer division). Floor division is performed with the `//` operator in Python.

### 3.1 How Floor Division Works

Floor division divides two numbers and rounds the result down to the nearest integer (towards negative infinity). It discards the fractional part.

**Examples:**

```python
# Regular division
5 / 2    # returns 2.5

# Floor division
5 // 2   # returns 2

1999 // 10   # returns 199
199 * 10     # returns 1990
```

### 3.2 Applying to Years

To get the decade of a year:

1. Perform floor division by 10 to remove the last digit (the units place).
2. Multiply the result by 10 to restore a full decade number.

For a year `y`, the decade is `(y // 10) * 10`.

**Examples:**

- 1963 → 1963 // 10 = 196 → 196 × 10 = 1960
- 1999 → 1999 // 10 = 199 → 199 × 10 = 1990
- 2005 → 2005 // 10 = 200 → 200 × 10 = 2000

This works because floor division effectively truncates the year to the nearest lower multiple of 10.

### 3.3 Creating the Decade Column

We apply this transformation to the entire `years` Series:

```python
decades = (years // 10) * 10
data_clean['Decade'] = decades
```

Now `data_clean` has a new integer column `Decade` that indicates the decade of release (e.g., 1960, 1970, 1980, ...). Films released between 1960 and 1969 all receive a value of 1960; films from 1970 to 1979 get 1970, and so on.

---

## 4. Separating Old and New Films

With the `Decade` column in place, we can create two subsets:

- **Old films**: all films released before 1970 (i.e., `Decade ≤ 1960`).
- **New films**: all films released from 1970 onward (i.e., `Decade > 1960`).

The cutoff at 1960 in the `Decade` column includes films from 1960–1969, which is exactly what we want for pre‑1970 films.

```python
old_films = data_clean[data_clean.Decade <= 1960]
new_films = data_clean[data_clean.Decade > 1960]
```

### 4.1 Verifying the Split

Check the size of each subset:

```python
print(f'Number of old films (pre‑1970): {len(old_films)}')
print(f'Number of new films (1970‑present): {len(new_films)}')
```

**Output:**

```
Number of old films (pre‑1970): 153
Number of new films (1970‑present): 5231
```

As expected, the vast majority of films in the dataset (over 97%) were released after 1970, confirming the visual impression from the bubble chart.

---

## 5. Exploring the Old Films Subset

Now we can examine the characteristics of the old films in more detail.

### 5.1 Summary Statistics

```python
old_films.describe()
```

**Output:**

| Statistic | Rank | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross | Decade |
|-----------|------|------------------------|---------------------|--------------------|--------|
| count     | 153.00 | 153.00 | 153.00 | 153.00 | 153.00 |
| mean      | 4,274.77 | 4,611,297.65 | 30,419,634.38 | 22,389,473.87 | 1,949.15 |
| std       | 742.14 | 5,713,648.85 | 54,931,828.93 | 32,641,752.41 | 12.72 |
| min       | 1,253.00 | 100,000.00 | 0.00 | 0.00 | 1,910.00 |
| 25%       | 3,973.00 | 1,250,000.00 | 5,273,000.00 | 5,000,000.00 | 1,940.00 |
| 50%       | 4,434.00 | 2,900,000.00 | 10,000,000.00 | 10,000,000.00 | 1,950.00 |
| 75%       | 4,785.00 | 5,000,000.00 | 33,208,099.00 | 28,350,000.00 | 1,960.00 |
| max       | 5,299.00 | 42,000,000.00 | 390,525,192.00 | 198,680,470.00 | 1,960.00 |

**Observations:**

- The average production budget for old films is about $4.6 million, far lower than the overall average of $31 million.
- The maximum budget is $42 million (for *Cleopatra*), which was extraordinarily high for its time.
- The average worldwide gross is $30.4 million, meaning that on average these films earned about 6.6 times their budget—a higher multiple than modern films, but with much smaller absolute numbers.
- The oldest films in this subset date back to the 1910s (Decade = 1910).

### 5.2 Most Expensive Old Film

To identify the highest‑budget film prior to 1970:

```python
old_films.sort_values('USD_Production_Budget', ascending=False).head()
```

**Top result:**

| Rank | Release_Date | Movie_Title | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross | Decade |
|------|--------------|-------------|-----------------------|---------------------|--------------------|--------|
| 1253 | 1963-12-06   | Cleopatra   | 42,000,000            | 71,000,000          | 57,000,000         | 1960   |

*Cleopatra* (1963) had a production budget of $42 million, which, adjusted for inflation, would be even more staggering today. It grossed $71 million worldwide, a respectable return but not as high as some later blockbusters. This film is an outlier in the old‑films dataset and will be influential in the regression analysis.

---

## 6. Implications for Regression Analysis

Splitting the data into old and new films allows us to build separate linear regression models for each era. The expectation is that:

- For old films, the relationship between budget and revenue will be weak (low R²) because the industry was different, and many low‑budget films could still achieve high revenue.
- For new films, the relationship will be much stronger (higher R²), reflecting the modern blockbuster dynamic where higher spending tends to yield higher returns.

This hypothesis will be tested in the next phase using Seaborn's `regplot` and scikit‑learn's `LinearRegression`.

---

## 7. Complete Code Block

For reference, here is the complete code to add the `Decade` column and create the two subsets:

```python
# Extract years from Release_Date
dt_index = pd.DatetimeIndex(data_clean.Release_Date)
years = dt_index.year

# Convert years to decades using floor division
decades = (years // 10) * 10
data_clean['Decade'] = decades

# Split into old and new films
old_films = data_clean[data_clean.Decade <= 1960]
new_films = data_clean[data_clean.Decade > 1960]

# Verify counts
print(f'Old films (pre‑1970): {len(old_films)}')
print(f'New films (1970‑present): {len(new_films)}')
```

---

## 8. Summary

In this section, we have:

- Created a `Decade` column by extracting years from the release date and applying floor division.
- Understood the mechanics of floor division (`//`) and why it is useful for binning continuous data into discrete categories.
- Separated the dataset into old films (pre‑1970) and new films (1970 onward), discovering that only 153 films (about 2.8%) belong to the old era.
- Examined the summary statistics for old films and identified *Cleopatra* as the most expensive film of that period.
- Set the stage for comparative regression analysis between the two eras.

