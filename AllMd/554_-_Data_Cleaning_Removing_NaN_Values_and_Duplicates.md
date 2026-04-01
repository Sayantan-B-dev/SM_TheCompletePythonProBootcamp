# Data Cleaning: Removing NaN Values and Duplicates

## Introduction

Data cleaning is the cornerstone of any data analysis project. Before we can derive any meaningful insights or create stunning visualizations, we must first ensure that our dataset is accurate, consistent, and free from errors. In this section, we will perform the initial cleaning steps on our Google Play Store dataset (`apps.csv`). Our goal is to:

- Understand the structure of the data (rows, columns, data types).
- Remove columns that are irrelevant to our analysis.
- Handle missing values (`NaN`) appropriately.
- Identify and remove duplicate entries.

By the end of this module, you will have a clean, reliable DataFrame ready for exploration and visualization.

---

## 1. Preliminary Data Exploration

Before we start cleaning, we need to get a feel for the data. What are we working with? How many rows and columns? What kind of information is stored? What are the data types? Are there any obvious issues?

### Challenge

> **Challenge:** How many rows and columns does `df_apps` have? What are the column names? Look at a random sample of 5 different rows with [`.sample()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html).

### Solution

Let's load the data and perform initial exploration.

```python
import pandas as pd

# Load the dataset
df_apps = pd.read_csv('apps.csv')

# Check the shape (rows, columns)
print("DataFrame shape:", df_apps.shape)
```

**Output:**
```
DataFrame shape: (10841, 12)
```

Our dataset contains **10,841 rows** and **12 columns**. That's a decent size – not huge, but enough to perform meaningful analysis.

Next, let's list the column names:

```python
print("Column names:")
print(df_apps.columns.tolist())
```

**Output:**
```
Column names:
['App', 'Category', 'Rating', 'Reviews', 'Size_MBs', 'Installs', 'Type', 'Price', 'Content_Rating', 'Genres', 'Last_Updated', 'Android_Ver']
```

Now, let's take a peek at a random sample of 5 rows to see what the data actually looks like. The `.sample()` method is excellent for this because it gives you a random subset, reducing the chance of bias.

```python
# Show 5 random rows
df_apps.sample(5)
```

**Sample Output (your exact rows may vary):**

|    | App                                        | Category          | Rating | Reviews | Size_MBs | Installs    | Type  | Price  | Content_Rating | Genres                       | Last_Updated | Android_Ver       |
|---:|:-------------------------------------------|:------------------|-------:|--------:|---------:|:------------|:------|:-------|:----------------|:-----------------------------|:-------------|:------------------|
| 156| "Mein Kampf" Audio Book                    | BOOKS_AND_REFERENCE| 4.3    | 85      | 16.0     | 10,000+     | Free  | 0      | Mature 17+      | Books & Reference            | July 20, 2018 | 4.0.3 and up      |
| 2397| Photo Editor & Collage Maker               | PHOTOGRAPHY       | 4.6    | 104,741 | 14.0     | 10,000,000+ | Free  | 0      | Everyone        | Photography                  | August 1, 2018 | 4.1 and up        |
| 521| Learn English Listening                     | EDUCATION         | 4.7    | 2,819   | 21.0     | 500,000+    | Free  | 0      | Everyone        | Education                    | July 29, 2018 | 4.1 and up        |
| 10234| Viber Messenger                            | COMMUNICATION     | 4.3    | 11,334,799 | 3.5      | 500,000,000+| Free  | 0      | Everyone        | Communication                | July 31, 2018 | Varies with device|
| 0| Ak Parti Yardım Toplama                     | SOCIAL            | NaN    | 0       | 8.7      | 0           | Paid  | $13.99 | Teen            | Social                       | July 28, 2017 | 4.1 and up        |

### Observations from the Sample

Looking at this sample, we immediately spot several data quality issues:

1.  **Missing Values (NaN):** The `Rating` column for the first app is `NaN`. This is a problem if we want to analyze ratings.
2.  **Inconsistent Data Types:** The `Installs` column contains strings with commas and plus signs (e.g., "10,000+", "500,000,000+"). This will prevent us from doing numerical calculations (like summing total installs).
3.  **Special Characters in Numeric Columns:** The `Price` column has a dollar sign (`$`) in front of the number, making it a string. We need to convert this to a float.
4.  **Irrelevant Columns:** Columns like `Last_Updated` and `Android_Ver` might not be useful for our specific analysis (we're focusing on app categories, ratings, installs, and pricing).

Our cleaning steps must address these issues.

---

## 2. Dropping Unused Columns

The columns `Last_Updated` and `Android_Ver` are not essential for answering our business questions about app categories, popularity, and pricing. Keeping them would just clutter our DataFrame, so we'll remove them.

### Challenge

> **Challenge:** Remove the columns called `Last_Updated` and `Android_Version` from the DataFrame. We will not use these columns.

### Solution

We can use the `.drop()` method in Pandas. The syntax is:

```python
df_apps.drop(columns=['col1', 'col2'], inplace=True)
```

Alternatively, you can use `axis=1` to indicate columns. We'll do this in-place to modify the original DataFrame.

```python
# Drop the two columns
df_apps.drop(['Last_Updated', 'Android_Ver'], axis=1, inplace=True)

# Verify they are gone
print(df_apps.columns.tolist())
```

**Output:**
```
['App', 'Category', 'Rating', 'Reviews', 'Size_MBs', 'Installs', 'Type', 'Price', 'Content_Rating', 'Genres']
```

Great! We now have a more focused DataFrame with only the columns we care about.

---

## 3. Handling Missing Values (NaN) in the Rating Column

The `Rating` column is critical for assessing app quality. Rows with missing ratings cannot be used in any analysis that involves ratings. Let's find out how many such rows exist.

### Challenge

> **Challenge:** How many rows have a NaN value (not-a-number) in the Rating column? Create a DataFrame called `df_apps_clean` that does not include these rows.

### Solution

We can filter the DataFrame to see only rows where `Rating` is NaN.

```python
# Find rows with NaN in Rating
nan_rating_rows = df_apps[df_apps.Rating.isna()]
print("Number of rows with missing rating:", nan_rating_rows.shape[0])
nan_rating_rows.head()
```

**Output:**
```
Number of rows with missing rating: 1474
```

|    | App                                        | Category          | Rating | Reviews | Size_MBs | Installs | Type  | Price  | Content_Rating | Genres     |
|---:|:-------------------------------------------|:------------------|-------:|--------:|---------:|:---------|:------|:-------|:----------------|:-----------|
| 0  | Ak Parti Yardım Toplama                    | SOCIAL            | NaN    | 0       | 8.7      | 0        | Paid  | $13.99 | Teen            | Social     |
| 1  | Ain Arabic Kids Alif Ba ta                  | FAMILY            | NaN    | 0       | 33.0     | 0        | Paid  | $2.99  | Everyone        | Education  |
| 2  | Popsicle Launcher for Android P 9.0 launcher| PERSONALIZATION   | NaN    | 0       | 5.5      | 0        | Paid  | $1.49  | Everyone        | Personalization|
| 3  | Command & Conquer: Rivals                  | FAMILY            | NaN    | 0       | 19.0     | 0        | NaN   | 0      | Everyone 10+    | Strategy   |
| 4  | CX Network                                 | BUSINESS          | NaN    | 0       | 10.0     | 0        | Free  | 0      | Everyone        | Business   |

**Observation:** All these apps have zero reviews and zero installs. It makes sense that an app with no user engagement would not have a rating. For our analysis, we will simply remove these rows, as they don't contribute any information about ratings.

To create a clean DataFrame without these rows, we use `.dropna()`.

```python
df_apps_clean = df_apps.dropna()
print("Shape after dropping NaN rows:", df_apps_clean.shape)
```

**Output:**
```
Shape after dropping NaN rows: (9367, 10)
```

We have eliminated 1,474 rows, leaving us with **9,367 entries**. This is a reasonable loss – the remaining data is now complete in terms of the `Rating` column.

> **Important Note:** Dropping rows with missing values is appropriate when the missing data is not recoverable and the number of missing rows is not too large relative to the dataset. In our case, we are comfortable with this approach.

---

## 4. Finding and Removing Duplicate Rows

Duplicates can skew our analysis. An app may appear more than once in the dataset for various reasons (e.g., scraping errors, multiple versions). We need to detect and remove these duplicates.

### Challenge

> **Challenge:** Are there any duplicates in the data? Check for duplicates using the [`.duplicated()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html) function. How many entries can you find for the "Instagram" app? Use [`.drop_duplicates()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html) to remove any duplicates from `df_apps_clean`.

### Solution

First, let's see how many duplicate rows exist.

```python
# Find duplicate rows
duplicated_rows = df_apps_clean[df_apps_clean.duplicated()]
print("Number of duplicate rows:", duplicated_rows.shape[0])
duplicated_rows.head()
```

**Output:**
```
Number of duplicate rows: 476
```

|     | App                             | Category | Rating | Reviews | Size_MBs | Installs    | Type | Price | Content_Rating | Genres     |
|----:|:--------------------------------|:---------|-------:|--------:|---------:|:------------|:-----|:------|:---------------|:-----------|
| 946 | 420 BZ Budeze Delivery          | MEDICAL  | 5.0    | 2       | 11.0     | 100         | Free | 0     | Mature 17+     | Medical    |
| 1133| MouseMingle                     | DATING   | 2.7    | 3       | 3.9      | 100         | Free | 0     | Mature 17+     | Dating     |
| 1196| Cardiac diagnosis (heart rate, arrhythmia) | MEDICAL  | 4.4    | 8       | 6.5      | 100         | Paid | $12.99| Everyone       | Medical    |
| 1231| Sway Medical                    | MEDICAL  | 5.0    | 3       | 22.0     | 100         | Free | 0     | Everyone       | Medical    |
| 1247| Chat Kids - Chat Room For Kids  | DATING   | 4.7    | 6       | 4.9      | 100         | Free | 0     | Mature 17+     | Dating     |

We have 476 duplicate rows. But are they exact duplicates? Let's examine a specific popular app, Instagram, to understand the nature of the duplication.

```python
# Look for all entries with the app name 'Instagram'
df_apps_clean[df_apps_clean.App == 'Instagram']
```

**Output:**

|       | App       | Category | Rating | Reviews   | Size_MBs | Installs      | Type | Price | Content_Rating | Genres |
|------:|:----------|:---------|-------:|----------:|---------:|:--------------|:-----|:------|:---------------|:-------|
| 10806 | Instagram | SOCIAL   | 4.5    | 66,577,313| 5.3      | 1,000,000,000+| Free | 0     | Teen           | Social |
| 10808 | Instagram | SOCIAL   | 4.5    | 66,577,446| 5.3      | 1,000,000,000+| Free | 0     | Teen           | Social |
| 10809 | Instagram | SOCIAL   | 4.5    | 66,577,313| 5.3      | 1,000,000,000+| Free | 0     | Teen           | Social |
| 10810 | Instagram | SOCIAL   | 4.5    | 66,509,917| 5.3      | 1,000,000,000+| Free | 0     | Teen           | Social |

Here we see **four** entries for Instagram. Notice that the `Reviews` numbers are slightly different for some rows, but the app name, category, size, and installs are identical. These are not exact duplicates across all columns, but they are duplicate entries for the same app. If we simply called `.drop_duplicates()` without any arguments, it would keep one of each unique row, but because the `Reviews` numbers differ, all four would be retained. That's not what we want.

We need to decide which columns define a duplicate. In this case, we likely want to consider an app duplicate if it has the same `App`, `Type`, and `Price` (since these should uniquely identify a version of an app). So we will use the `subset` parameter to specify these columns.

```python
# Remove duplicates based on 'App', 'Type', and 'Price'
df_apps_clean = df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'])

# Check Instagram again
df_apps_clean[df_apps_clean.App == 'Instagram']
```

**Output:**

|       | App       | Category | Rating | Reviews   | Size_MBs | Installs      | Type | Price | Content_Rating | Genres |
|------:|:----------|:---------|-------:|----------:|---------:|:--------------|:-----|:------|:---------------|:-------|
| 10806 | Instagram | SOCIAL   | 4.5    | 66,577,313| 5.3      | 1,000,000,000+| Free | 0     | Teen           | Social |

Perfect! Now we have only one entry for Instagram. The number of rows in our cleaned DataFrame is now:

```python
print("Shape after removing duplicates:", df_apps_clean.shape)
```

**Output:**
```
Shape after removing duplicates: (8199, 10)
```

We have successfully reduced the dataset from 9,367 to **8,199 unique apps**. That's a significant reduction, but now we can be confident that each row represents a distinct app.

---

## 5. Summary of Data Cleaning

Let's recap what we've accomplished:

- **Loaded the dataset** with 10,841 rows and 12 columns.
- **Dropped two irrelevant columns** (`Last_Updated`, `Android_Ver`).
- **Removed 1,474 rows** with missing ratings (`.dropna()`).
- **Identified and removed 1,168 duplicate entries** (using a custom subset of columns).

Our final cleaned DataFrame, `df_apps_clean`, has **8,199 rows and 10 columns**. It is now ready for further exploration and visualization.

### What's Next?

We still have some data type issues to resolve (e.g., `Installs` and `Price` columns are stored as strings). We'll tackle those in the next module as we prepare for numerical analysis and charting.

---

## 6. Important Notes on the Dataset

Before we move on, it's crucial to understand the limitations and characteristics of this dataset. As an analyst, you should always be aware of how the data was collected and what assumptions are being made.

- **Sample Representativeness:** This dataset is a sample of Android apps scraped from the Google Play Store around 2017–2018. It is not a complete list of all apps (there are millions). The sample may be biased based on the geographic location and search behavior of the person who scraped it (Lavanya Gupta). We will assume it is representative for the purpose of this analysis, but this is a simplifying assumption.

- **Pricing Data:** The prices are in USD and reflect the value at the time of scraping. Developers can change prices or run promotions, so this is a snapshot.

- **Size Conversion:** The `Size` column was originally in various units (e.g., "Varies with device", "k", "M"). It has been pre-processed and converted to a float representing megabytes (MB). Missing values were filled with the average size for that category.

- **Installs Approximation:** Google Play reports installs as a range (e.g., "100,000+", "500,000+"). The `Installs` column in this dataset has been converted to an integer by removing the '+' and commas. For example, "1,000,000+" becomes 1,000,000. This is an approximation, but it's the best we have.

Understanding these nuances will help us interpret our visualizations and conclusions correctly.

---

## 7. Key Takeaways

- **Always start with a preliminary exploration:** Use `.shape`, `.columns`, `.sample()`, and `.info()` to get a feel for the data.
- **Drop irrelevant columns early:** It simplifies the DataFrame and reduces clutter.
- **Handle missing values thoughtfully:** Dropping is appropriate when missing data is not recoverable and doesn't represent a large portion.
- **Duplicates are not always exact:** You must decide which columns define a duplicate. Use the `subset` parameter in `.drop_duplicates()` to specify them.
- **Document your assumptions:** Understanding how the data was collected and pre-processed is essential for accurate analysis.

