# Data Preparation and Exploration

## Upgrading Plotly in Google Colab

Google Colaboratory comes with many Python packages pre-installed, including Plotly. However, the version of Plotly available by default may be outdated and might not support certain modern features, such as sunburst charts used later in this analysis. To ensure all visualizations work correctly, it is necessary to upgrade Plotly to the latest version.

Execute the following command in a code cell. The line is commented out initially; uncomment it, run the cell, and then comment it again to avoid re‑running unnecessarily.

```python
# %pip install --upgrade plotly
```

After upgrading, if prompted, restart the runtime so that the new version is loaded.

---

## Preliminary Data Exploration

Before any cleaning or transformation, it is essential to understand the structure and contents of the dataset. The data is stored in a CSV file named `nobel_prize_data.csv`. After loading it into a pandas DataFrame (`df_data`), we examine its basic properties.

```python
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
df_data = pd.read_csv('nobel_prize_data.csv')
```

### Shape of the Dataset

```python
df_data.shape
```
**Output:** `(962, 16)`

This tells us that the dataset contains 962 rows (each representing a Nobel laureate or a prize awarded to an organization) and 16 columns.

### Column Names and Sample Data

```python
df_data.head()
df_data.tail()
```

From the first and last few rows we can see the following columns:

- `year`: year the prize was awarded.
- `category`: prize category (Chemistry, Literature, Medicine, Peace, Physics, Economics).
- `prize`: full name of the prize.
- `motivation`: citation text (may be missing).
- `prize_share`: fractional share of the prize (e.g., `"1/1"`, `"1/2"`, `"1/3"`).
- `laureate_type`: `"Individual"` or `"Organization"`.
- `full_name`: name of the laureate or organization.
- `birth_date`: date of birth (string format).
- `birth_city`: city of birth.
- `birth_country`: country of birth as it existed at the time (some are historical names).
- `birth_country_current`: modern name of the birth country.
- `sex`: gender (`Male`, `Female`, or `NaN` for organizations).
- `organization_name`: affiliated institution (if any).
- `organization_city`: city of the institution.
- `organization_country`: country of the institution.
- `ISO`: three‑letter ISO code for `birth_country_current`.

### First and Last Years

The first Nobel prizes were awarded in **1901**, as shown in the head. The tail shows that the dataset extends to **2020**, the latest year included.

---

## Missing Data Analysis

### Checking for Duplicates

Duplicates could distort counts and aggregations. We check for any completely duplicated rows:

```python
print(f'Any duplicates? {df_data.duplicated().values.any()}')
```
**Output:** `False`

No full duplicates exist, so each row is unique.

### Identifying NaN Values

Many real‑world datasets contain missing values. First, we see if any NaNs are present:

```python
print(f'Any NaN values among the data? {df_data.isna().values.any()}')
```
**Output:** `True`

Then we count NaNs per column:

```python
df_data.isna().sum()
```

| Column                 | NaN Count |
|------------------------|-----------|
| year                   | 0         |
| category               | 0         |
| prize                  | 0         |
| motivation             | 88        |
| prize_share            | 0         |
| laureate_type          | 0         |
| full_name              | 0         |
| birth_date             | 28        |
| birth_city             | 31        |
| birth_country          | 28        |
| birth_country_current  | 28        |
| sex                    | 28        |
| organization_name      | 255       |
| organization_city      | 255       |
| organization_country   | 254       |
| ISO                    | 28        |

### Why Are There Missing Values?

#### Birth‑related Columns (birth_date, birth_city, etc.)

Filtering rows where `birth_date` is NaN reveals that these rows correspond to **organizations** rather than individuals. Organizations do not have a birth date, birth city, or gender.

```python
col_subset = ['year','category', 'laureate_type', 'birth_date','full_name', 'organization_name']
df_data.loc[df_data.birth_date.isna(), col_subset]
```

All such entries are of `laureate_type = Organization`, for example the Red Cross, UN agencies, etc. This explains the 28 missing values in `birth_date` and the corresponding 28 in `sex`, `birth_country`, and `ISO`.

#### Organization‑related Columns (organization_name, city, country)

Many prizes, especially in Literature and Peace, are awarded to individuals who were not affiliated with a university or research institute. For these rows, the organization columns are left blank. This accounts for the 255 missing values in `organization_name`.

```python
col_subset = ['year','category', 'laureate_type','full_name', 'organization_name']
df_data.loc[df_data.organization_name.isna(), col_subset]
```

The output shows a mix of Literature laureates, Peace laureates, and also some individuals in other categories who worked independently.

#### Motivation Column

`motivation` is missing for 88 rows, almost exclusively for Peace Prize laureates (both individuals and organizations), where the motivation text is often not provided.

---

## Data Type Conversions

To enable time‑based analysis and numerical calculations, two columns need type conversion:

1. **`birth_date`** – currently strings; convert to pandas `datetime` objects.
2. **`prize_share`** – currently strings like `"1/2"`; convert to a floating‑point percentage.

### Converting `birth_date` to Datetime

```python
df_data.birth_date = pd.to_datetime(df_data.birth_date)
```

Now `birth_date` has type `datetime64[ns]`, allowing extraction of year, month, etc.

### Creating a Percentage Share Column

The `prize_share` column contains fractions such as `"1/1"` (full prize) or `"1/3"` (shared among three). To perform arithmetic, we split the string, convert to numbers, and compute the division.

```python
separated_values = df_data.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denominator = pd.to_numeric(separated_values[1])
df_data['share_pct'] = numerator / denominator
```

This adds a new column `share_pct` with values like `1.0`, `0.5`, `0.333`, etc.

---

## Verifying the Changes

After these transformations, we can inspect the DataFrame’s info to confirm the new data types:

```python
df_data.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 962 entries, 0 to 961
Data columns (total 17 columns):
 #   Column                 Non-Null Count  Dtype         
---  ------                 --------------  -----         
 0   year                   962 non-null    int64         
 1   category               962 non-null    object        
 2   prize                  962 non-null    object        
 3   motivation             874 non-null    object        
 4   prize_share            962 non-null    object        
 5   laureate_type          962 non-null    object        
 6   full_name              962 non-null    object        
 7   birth_date             934 non-null    datetime64[ns]
 8   birth_city             931 non-null    object        
 9   birth_country          934 non-null    object        
 10  birth_country_current  934 non-null    object        
 11  sex                    934 non-null    object        
 12  organization_name      707 non-null    object        
 13  organization_city      707 non-null    object        
 14  organization_country   708 non-null    object        
 15  ISO                    934 non-null    object        
 16  share_pct              962 non-null    float64       
dtypes: datetime64[ns](1), float64(1), int64(1), object(14)
memory usage: 127.9+ KB
```

- `birth_date` is now `datetime64[ns]`.
- `share_pct` is `float64`.
- All other columns retain their original types.

The data is now clean and properly typed, ready for exploratory analysis and visualization.

---

## Summary of Key Steps

1. **Upgraded Plotly** to ensure compatibility with advanced charts.
2. **Explored the dataset** using `shape`, `head`, `tail` to understand its dimensions and contents.
3. **Identified missing values** and reasoned about their origins:
   - Organizations cause missing birth‑related fields.
   - Literature and Peace laureates often lack organizational affiliations.
4. **Converted data types**:
   - `birth_date` to datetime.
   - `prize_share` to a numeric percentage column `share_pct`.
5. **Verified the changes** with `info()`.
