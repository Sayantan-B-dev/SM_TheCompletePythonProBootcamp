# Investigating Films with Zero Revenue

This document provides a detailed exploration of films that recorded zero revenue in the dataset. The analysis focuses on understanding the distribution of production budgets and worldwide gross revenues, quantifying how many films earned nothing domestically or worldwide, and examining the characteristics of those zero‑revenue films, particularly those with high budgets. The findings reveal important patterns and anomalies that guide subsequent data cleaning and modelling steps.

All operations are performed on the cleaned DataFrame `data` (as established in the previous section), which contains 5,391 films with properly formatted numeric budget and revenue columns, and a datetime release date.

---

## 1. Descriptive Statistics of the Dataset

Before isolating zero‑revenue films, it is essential to obtain a statistical summary of the entire dataset. The `.describe()` method provides key metrics for the numeric columns.

```python
data.describe()
```

**Output:**

| Statistic | Rank | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|-----------|------|------------------------|---------------------|--------------------|
| count     | 5,391.00 | 5,391.00 | 5,391.00 | 5,391.00 |
| mean      | 2,696.00 | 31,113,737.58 | 88,855,421.96 | 41,235,519.44 |
| std       | 1,556.39 | 40,523,796.88 | 168,457,757.00 | 66,029,346.27 |
| min       | 1.00     | 1,100.00      | 0.00          | 0.00          |
| 25%       | 1,348.50 | 5,000,000.00  | 3,865,206.00  | 1,330,901.50  |
| 50%       | 2,696.00 | 17,000,000.00 | 27,450,453.00 | 17,192,205.00 |
| 75%       | 4,043.50 | 40,000,000.00 | 96,454,455.00 | 52,343,687.00 |
| max       | 5,391.00 | 425,000,000.00| 2,783,918,982.00| 936,662,225.00|

**Interpretation:**

- **Mean production budget:** Approximately $31.1 million.
- **Mean worldwide gross:** Approximately $88.9 million, indicating that, on average, films earn about three times their production cost.
- **Minimum values:** The smallest budget is $1,100, and the minimum revenue (both domestic and worldwide) is $0. This suggests some films either never screened or were complete flops.
- **Quartiles:** 
  - The bottom 25% of films have budgets ≤ $5 million and worldwide gross ≤ $3.9 million.
  - The median film costs $17 million and earns $27.5 million worldwide.
  - The top 25% have budgets ≥ $40 million and worldwide gross ≥ $96.5 million.
- **Maximum values:** The most expensive film (*Avatar*) had a budget of $425 million and earned $2.78 billion worldwide.

From these numbers, we can infer that while many films are profitable, a significant portion (especially those in the lower quartile) may not recoup their budgets, as their worldwide gross is often less than their production cost.

### 1.1 Lowest Budget Film

To identify the film with the smallest budget:

```python
data[data.USD_Production_Budget == data.USD_Production_Budget.min()]
```

| Rank | Release_Date | Movie_Title       | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|-------------------|-----------------------|---------------------|--------------------|
| 5391 | 2005-05-08   | My Date With Drew | 1100                  | 181041              | 181041             |

*My Date With Drew* cost only $1,100 to produce and grossed $181,041 worldwide—a remarkable return on investment.

### 1.2 Highest Budget Film

Similarly, the most expensive film:

```python
data[data.USD_Production_Budget == data.USD_Production_Budget.max()]
```

| Rank | Release_Date | Movie_Title | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|-------------|-----------------------|---------------------|--------------------|
| 1    | 2009-12-18   | Avatar      | 425000000             | 2783918982          | 760507625          |

*Avatar* not only had the highest budget but also achieved the highest worldwide gross, suggesting a positive correlation between spending and revenue for blockbusters.

---

## 2. Films with Zero Domestic Revenue

A domestic gross of $0 can occur for several reasons:

- The film was never released in the United States.
- The film was released but earned no reported revenue (e.g., a complete failure).
- The film had not yet been released at the time of data collection (May 1, 2018).

### 2.1 Counting Zero Domestic Films

```python
zero_domestic = data[data.USD_Domestic_Gross == 0]
print(f'Number of films that grossed $0 domestically: {len(zero_domestic)}')
```

**Output:** `Number of films that grossed $0 domestically: 512`

Thus, 512 out of 5391 films (about 9.5%) recorded no domestic revenue.

### 2.2 Highest‑Budget Films with Zero Domestic Gross

To examine which high‑budget films earned nothing in the U.S., sort the subset by production budget descending:

```python
zero_domestic.sort_values('USD_Production_Budget', ascending=False)
```

**Top rows of the sorted output:**

| Rank | Release_Date | Movie_Title                  | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|------------------------------|-----------------------|---------------------|--------------------|
| 96   | 2020-12-31   | Singularity                  | 175000000             | 0                   | 0                  |
| 126  | 2018-12-18   | Aquaman                      | 160000000             | 0                   | 0                  |
| 321  | 2018-09-03   | A Wrinkle in Time            | 103000000             | 0                   | 0                  |
| 366  | 2018-10-08   | Amusement Park               | 100000000             | 0                   | 0                  |
| 556  | 2015-12-31   | Don Gato, el inicio de la pandilla | 80000000        | 4547660             | 0                  |
| ...  | ...          | ...                          | ...                   | ...                 | ...                |

**Observations:**

- Films like *Singularity*, *Aquaman*, and *A Wrinkle in Time* have release dates **after** the data collection date (May 1, 2018). They had not been released yet, hence the zero domestic gross.
- *Don Gato, el inicio de la pandilla* (an animated Mexican film) was released in 2015, earned money worldwide ($4.5 million), but nothing in the U.S.—a clear example of an international release that never played in American theaters.
- Many other films with smaller budgets also show zero domestic gross, likely for similar reasons (international releases or unreleased status).

### 2.3 Why the Difference Between Domestic and Worldwide Zero Counts?

The fact that there are 512 films with zero domestic gross but only 357 with zero worldwide gross (as we will see) indicates that 155 films (512 − 357) earned money **outside** the U.S. but nothing domestically. These are the international releases that did not get a U.S. release.

---

## 3. Films with Zero Worldwide Revenue

Now we examine films that generated no revenue anywhere in the world. A worldwide gross of $0 typically means the film was either:

- Never released (or its release date is after the data collection).
- A complete flop with no box office earnings reported.

### 3.1 Counting Zero Worldwide Films

```python
zero_worldwide = data[data.USD_Worldwide_Gross == 0]
print(f'Number of films that grossed $0 worldwide: {len(zero_worldwide)}')
```

**Output:** `Number of films that grossed $0 worldwide: 357`

### 3.2 Highest‑Budget Films with Zero Worldwide Gross

Sorting by budget descending:

```python
zero_worldwide.sort_values('USD_Production_Budget', ascending=False)
```

**Top rows:**

| Rank | Release_Date | Movie_Title                  | USD_Production_Budget | USD_Worldwide_Gross | USD_Domestic_Gross |
|------|--------------|------------------------------|-----------------------|---------------------|--------------------|
| 96   | 2020-12-31   | Singularity                  | 175000000             | 0                   | 0                  |
| 126  | 2018-12-18   | Aquaman                      | 160000000             | 0                   | 0                  |
| 321  | 2018-09-03   | A Wrinkle in Time            | 103000000             | 0                   | 0                  |
| 366  | 2018-10-08   | Amusement Park               | 100000000             | 0                   | 0                  |
| 880  | 2015-11-12   | The Ridiculous 6             | 60000000              | 0                   | 0                  |
| ...  | ...          | ...                          | ...                   | ...                 | ...                |

Again, many of the highest‑budget entries are films with future release dates (post‑May 2018). *The Ridiculous 6* (a 2015 Netflix film) had no theatrical release, hence zero box office gross.

### 3.3 Comparison with Zero Domestic

The key difference: 512 films had zero domestic gross, but only 357 had zero worldwide gross. The extra 155 films are those that earned money internationally but not in the U.S. This subset can be extracted using a multi‑condition filter, as shown in later sections.

---

## 4. Implications for Further Analysis

The presence of unreleased films (those with release dates after May 1, 2018) in the zero‑revenue groups is problematic because they artificially inflate the count of films with zero revenue and could distort any analysis of financial performance. These films should be removed before building models or drawing conclusions about the relationship between budget and revenue.

The next steps in the project (covered in subsequent files) will address this by:

- Creating a subset of films released **on or before** the data collection date.
- Re‑examining zero‑revenue counts without the unreleased films.
- Calculating the percentage of films that actually lost money (budget > worldwide gross) among released films.

---

## 5. Summary

Through this investigation, we have:

- Calculated summary statistics revealing average budgets and revenues, and identified the lowest and highest budget films.
- Discovered that 512 films earned nothing domestically, while 357 earned nothing worldwide.
- Observed that many high‑budget zero‑revenue films have future release dates, indicating they are not yet released.
- Recognised that the difference between domestic and worldwide zero counts arises from international films that never screened in the U.S.

These findings highlight the need to clean the data further by removing unreleased films before proceeding with regression analysis. They also underscore the risky nature of film financing: over one‑third of all films in the dataset do not recoup their production budgets, as we will quantify later.

---
