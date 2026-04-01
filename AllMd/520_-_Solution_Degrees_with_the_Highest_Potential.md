## Solution: Degrees with the Highest Potential and Greatest Spread

This section provides the solutions to the challenges posed in the previous lesson. It includes code to identify majors with the highest earning potential (based on 90th percentile mid‑career salary) and majors with the greatest spread (largest difference between 90th and 10th percentiles). The results are examined, and observations about the overlap between high potential and high variability are discussed. Additionally, an extra credit task is outlined for those interested in updating the analysis with current data from PayScale.

---

### 1. Majors with the Highest Potential

**Potential** is defined here as the 90th percentile mid‑career salary – the earnings achieved by the top 10% of graduates in a given major. To find the majors with the highest potential, we sort the DataFrame by the `'Mid-Career 90th Percentile Salary'` column in descending order.

#### 1.1. Code Implementation

```python
# Sort the DataFrame by the 90th percentile salary in descending order
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)

# Display the top 5 majors with their 90th percentile salaries
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
```

**Expected Output:**

|     | Undergraduate Major | Mid-Career 90th Percentile Salary |
|-----|---------------------|-----------------------------------|
| 17  | Economics           | 181000                            |
| 8   | Chemical Engineering| 162000                            |
| 41  | Finance             | 148000                            |
| 20  | Physics             | 147000                            |
| 1   | Aerospace Engineering | 143000                          |

#### 1.2. Interpretation

- **Economics** tops the list with a 90th percentile salary of $181,000, indicating that the highest‑earning economists command very high salaries.
- **Chemical Engineering** follows closely at $162,000, showing strong earning potential in that field.
- **Finance, Physics, and Aerospace Engineering** round out the top five, all with 90th percentile salaries above $140,000.

These majors are predominantly in the STEM and Business categories, reflecting the market demand for quantitative and technical skills.

---

### 2. Majors with the Greatest Spread in Salaries

**Spread** measures the difference between the 90th percentile and 10th percentile mid‑career salaries. A large spread indicates high earnings inequality within the major – some graduates earn much more than others. To identify these majors, we sort the DataFrame by the `'Spread'` column in descending order.

#### 2.1. Code Implementation

```python
# Sort the DataFrame by the Spread column in descending order
highest_spread = clean_df.sort_values('Spread', ascending=False)

# Display the top 5 majors with their spread values
highest_spread[['Undergraduate Major', 'Spread']].head()
```

**Expected Output:**

|     | Undergraduate Major | Spread |
|-----|---------------------|--------|
| 17  | Economics           | 120600 |
| 8   | Chemical Engineering| 104400 |
| 1   | Aerospace Engineering | 82600 |
| 41  | Finance             | 82500  |
| 20  | Physics             | 82000  |

#### 2.2. Interpretation

- **Economics** again leads, with a spread of $120,600. This means the top 10% of economics graduates earn $120,600 more than the bottom 10%. The field offers high potential but also high risk.
- **Chemical Engineering** has a spread of $104,400, also indicating significant variability.
- **Aerospace Engineering, Finance, and Physics** all have spreads above $80,000, placing them among the most unequal majors in terms of earnings.

---

### 3. Comparison: High Potential vs. High Spread

Notice that **three of the top five majors** appear in both lists: Economics, Chemical Engineering, and Finance. This overlap illustrates a common pattern: degrees that offer the highest earning potential often come with greater uncertainty and a wider range of outcomes. Graduates in these fields can end up either very highly compensated or relatively modestly paid, depending on factors such as industry, location, and individual performance.

The table below summarizes the overlap:

| Major               | 90th Percentile Salary | Spread  | Appears in Both? |
|---------------------|------------------------|---------|------------------|
| Economics           | $181,000               | $120,600| Yes              |
| Chemical Engineering| $162,000               | $104,400| Yes              |
| Finance             | $148,000               | $82,500 | Yes              |
| Physics             | $147,000               | $82,000 | No (only in potential) |
| Aerospace Engineering| $143,000              | $82,600 | No (only in spread) |

**Key Insight:** Majors with the highest median salaries (e.g., Chemical Engineering) may not always have the highest 90th percentile; conversely, some majors with very high 90th percentiles also have large spreads, indicating that while the top earners do extremely well, the typical graduate may not fare as well.

---

### 4. Additional Observations

#### 4.1. The Role of Group Category

Examining the group membership of these top majors:

- **Economics** is classified as a **Business** major in this dataset.
- **Chemical Engineering, Physics, Aerospace Engineering** are **STEM**.
- **Finance** is **Business**.

Thus, both Business and STEM dominate the high‑potential and high‑spread lists, while HASS (Humanities, Arts, Social Science) majors are absent from the top five in both categories. This aligns with the earlier grouping analysis that showed STEM and Business have higher average salaries.

#### 4.2. Visualizing the Relationship

A scatter plot of Spread vs. 90th Percentile Salary would likely show a positive correlation: majors with higher potential tend to have larger spreads. This is a typical risk‑reward trade‑off.

---

### 5. Extra Credit: Updating the Data with Current PayScale Information

The dataset used in this analysis is from a 2008 PayScale survey covering the prior ten years. Since then, economic conditions, industry demands, and salary structures have evolved. The financial crisis of 2008, in particular, may have altered the relative rankings of majors such as Finance and Economics.

#### 5.1. Web Scraping Approach

As covered in Day 45, web scraping can be used to extract current data from PayScale’s website. The PayScale College Salary Report (https://www.payscale.com/college-salary-report) provides up‑to‑date salary information by major. However, scraping modern websites often requires handling JavaScript‑rendered content, pagination, and adherence to robots.txt and terms of service.

A simplified approach might involve:

1. Inspecting the network requests to find an API endpoint that returns data in JSON format.
2. Using `requests` and `BeautifulSoup` to parse static HTML if available.
3. Respecting the website's `robots.txt` and rate limits.

#### 5.2. Example Outline for Scraping

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract table rows containing major names and salary figures
# (This is illustrative; actual implementation depends on page structure)
```

Because PayScale's site is dynamic and may change, a more reliable method is to look for an official API or download the data as a CSV if provided.

#### 5.3. Alternative: Using PayScale’s Data via API

PayScale may offer data access through a paid API. For educational purposes, one could use a publicly available dataset from sources like Kaggle or the US Bureau of Labor Statistics.

#### 5.4. Comparing Results

If updated data is obtained, the analysis can be repeated to see:

- Which majors have risen or fallen in rankings.
- Whether the risk‑reward trade‑off still holds.
- How the average salaries by group (STEM, Business, HASS) have changed over time.

---

### 6. Summary of Solutions

| Challenge                          | Method                                      | Key Takeaway                                                                 |
|------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|
| Highest potential majors           | `sort_values('Mid-Career 90th Percentile Salary', ascending=False).head()` | Economics, Chemical Engineering, Finance, Physics, Aerospace Engineering lead. |
| Greatest spread majors             | `sort_values('Spread', ascending=False).head()` | Same majors appear, indicating high potential often comes with high variability. |
| Overlap analysis                   | Compare the two lists                       | Three majors (Economics, Chemical Engineering, Finance) are in both top fives. |

---

### 7. Next Steps

With these insights, the analysis can move toward grouping by category (STEM, Business, HASS) to compare average salaries and spreads across broad fields. This will provide a higher‑level understanding of which types of degrees offer the best financial outcomes and the least risk.

---

**Resource:**  
- PayScale College Salary Report: [https://www.payscale.com/college-salary-report](https://www.payscale.com/college-salary-report)  
- Day 45 web scraping lessons for techniques to extract current data.