# Numeric Type Conversions for the Installations & Price Data

## Introduction

After cleaning our DataFrame and removing duplicates, we now have a clean dataset of **8,199 unique apps**. However, two important columns – `Installs` and `Price` – are still stored as text (object) data types. This prevents us from performing numerical calculations such as summing installs, averaging prices, or estimating revenue. In this module, we will:

- Convert the `Installs` column to a proper numeric format.
- Explore the distribution of installs (e.g., how many apps have over 1 billion installs? How many have just one install?).
- Convert the `Price` column to numeric.
- Identify the most expensive apps and remove extreme outliers (apps costing more than $250) that are likely gimmicks.
- Create a new `Revenue_Estimate` column (price × installs) and find the top‑grossing paid apps.

By the end, our DataFrame will be fully numeric where appropriate, ready for advanced analysis and visualisation.

---

## 1. Examining the Installs Column

### Challenge

> **Challenge:** How many apps had over 1 billion installations? How many apps just had a single install?
> 
> Check the datatype of the `Installs` column.
> 
> Count the number of apps at each level of installations.
> 
> Convert the number of installations (the `Installs` column) to a numeric data type. Hint: this is a 2‑step process. You'll have to make sure you remove non‑numeric characters first.

### Solution

#### 1.1 Check the Data Type

We can use `.info()` or `.describe()` to see the data type of the `Installs` column.

```python
df_apps_clean.info()
```

**Output:**
```
<class 'pandas.core.frame.DataFrame'>
Int64Index: 8199 entries, 21 to 10835
Data columns (total 10 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   App             8199 non-null   object 
 1   Category        8199 non-null   object 
 2   Rating          8199 non-null   float64
 3   Reviews         8199 non-null   int64  
 4   Size_MBs        8199 non-null   float64
 5   Installs        8199 non-null   object 
 6   Type            8199 non-null   object 
 7   Price           8199 non-null   object 
 8   Content_Rating  8199 non-null   object 
 9   Genres          8199 non-null   object 
dtypes: float64(2), int64(1), object(7)
```

The `Installs` column is of type **object** (string). The `.describe()` method confirms this:

```python
df_apps_clean.Installs.describe()
```

**Output:**
```
count          8199
unique           19
top       1,000,000
freq           1417
Name: Installs, dtype: object
```

We see that the most common value is `"1,000,000"` and there are 19 unique install strings. The presence of commas (and possibly a trailing `+` in the original data, though it seems the `+` was removed in the pre‑processed version) prevents these from being interpreted as numbers.

#### 1.2 Count Apps by Install Level (Before Conversion)

We can group by the current string values to see the distribution.

```python
df_apps_clean[['App', 'Installs']].groupby('Installs').count()
```

**Output:**

| Installs        | App |
|----------------|-----|
| 1              | 3   |
| 1,000          | 698 |
| 1,000,000      | 1417|
| 1,000,000,000  | 20  |
| 10             | 69  |
| 10,000         | 988 |
| 10,000,000     | 933 |
| 100            | 303 |
| 100,000        | 1096|
| 100,000,000    | 189 |
| 5              | 9   |
| 5,000          | 425 |
| 5,000,000      | 607 |
| 50             | 56  |
| 50,000         | 457 |
| 50,000,000     | 202 |
| 500            | 199 |
| 500,000        | 504 |
| 500,000,000    | 24  |

From this we can already answer the first part of the challenge:

- **Apps with over 1 billion installs:** The value `"1,000,000,000"` appears 20 times. So **20 apps** have crossed the billion‑download mark.
- **Apps with a single install:** The value `"1"` appears 3 times. So **3 apps** have only one install.

#### 1.3 Convert Installs to Numeric

To convert, we first remove the commas (`,`) from the strings, then convert the entire column to integers using `pd.to_numeric()`.

```python
# Remove commas
df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', '')

# Convert to numeric (integers)
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
```

Now let's verify the conversion and see the new distribution.

```python
df_apps_clean[['App', 'Installs']].groupby('Installs').count()
```

**Output (numeric order):**

| Installs    | App |
|------------|-----|
| 1          | 3   |
| 5          | 9   |
| 10         | 69  |
| 50         | 56  |
| 100        | 303 |
| 500        | 199 |
| 1000       | 698 |
| 5000       | 425 |
| 10000      | 988 |
| 50000      | 457 |
| 100000     | 1096|
| 500000     | 504 |
| 1000000    | 1417|
| 5000000    | 607 |
| 10000000   | 933 |
| 50000000   | 202 |
| 100000000  | 189 |
| 500000000  | 24  |
| 1000000000 | 20  |

The numbers are now properly ordered, and we can perform arithmetic operations on them.

---

## 2. Examining and Converting the Price Column

### Challenge

> **Challenge:** Convert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset.
>
> Remove all apps that cost more than $250 from the `df_apps_clean` DataFrame.
>
> Add a column called `'Revenue_Estimate'` to the DataFrame. This column should hold the price of the app times the number of installs. What are the top 10 highest‑grossing paid apps according to this estimate? Out of the top 10, how many are games?

### Solution

#### 2.1 Convert Price to Numeric

The `Price` column contains dollar signs (`$`). We need to remove them before conversion.

```python
# Remove dollar signs
df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', '')

# Convert to numeric (float, because prices can have cents)
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
```

#### 2.2 Find the Top 20 Most Expensive Apps

Now we can sort by price in descending order.

```python
df_apps_clean.sort_values('Price', ascending=False).head(20)
```

**Output (first 20 rows):**

|     | App                                 | Category     | Rating | Reviews | Size_MBs | Installs | Type | Price | Content_Rating | Genres         |
|----:|:------------------------------------|:-------------|-------:|--------:|---------:|---------:|:-----|------:|:---------------|:---------------|
| 3946| I'm Rich - Trump Edition            | LIFESTYLE    | 3.6    | 275     | 7.3      | 10000    | Paid | 400.00| Everyone       | Lifestyle      |
| 2461| I AM RICH PRO PLUS                  | FINANCE      | 4.0    | 36      | 41.0     | 1000     | Paid | 399.99| Everyone       | Finance        |
| 4606| I Am Rich Premium                   | FINANCE      | 4.1    | 1867    | 4.7      | 50000    | Paid | 399.99| Everyone       | Finance        |
| 3145| I am rich(premium)                  | FINANCE      | 3.5    | 472     | 0.94     | 5000     | Paid | 399.99| Everyone       | Finance        |
| 3554| 💎 I'm rich                         | LIFESTYLE    | 3.8    | 718     | 26.0     | 10000    | Paid | 399.99| Everyone       | Lifestyle      |
| 5765| I am rich                           | LIFESTYLE    | 3.8    | 3547    | 1.8      | 100000   | Paid | 399.99| Everyone       | Lifestyle      |
| 1946| I am rich (Most expensive app)      | FINANCE      | 4.1    | 129     | 2.7      | 1000     | Paid | 399.99| Teen           | Finance        |
| 2775| I Am Rich Pro                       | FAMILY       | 4.4    | 201     | 2.7      | 5000     | Paid | 399.99| Everyone       | Entertainment  |
| 3221| I am Rich Plus                      | FAMILY       | 4.0    | 856     | 8.7      | 10000    | Paid | 399.99| Everyone       | Entertainment  |
| 3114| I am Rich                           | FINANCE      | 4.3    | 180     | 3.8      | 5000     | Paid | 399.99| Everyone       | Finance        |
| 1331| most expensive app (H)              | FAMILY       | 4.3    | 6       | 1.5      | 100      | Paid | 399.99| Everyone       | Entertainment  |
| 2394| I am Rich!                          | FINANCE      | 3.8    | 93      | 22.0     | 1000     | Paid | 399.99| Everyone       | Finance        |
| 3897| I Am Rich                           | FAMILY       | 3.6    | 217     | 4.9      | 10000    | Paid | 389.99| Everyone       | Entertainment  |
| 2193| I am extremely Rich                 | LIFESTYLE    | 2.9    | 41      | 2.9      | 1000     | Paid | 379.99| Everyone       | Lifestyle      |
| 3856| I am rich VIP                       | LIFESTYLE    | 3.8    | 411     | 2.6      | 10000    | Paid | 299.99| Everyone       | Lifestyle      |
| 2281| Vargo Anesthesia Mega App           | MEDICAL      | 4.6    | 92      | 32.0     | 1000     | Paid | 79.99 | Everyone       | Medical        |
| 1407| LTC AS Legal                        | MEDICAL      | 4.0    | 6       | 1.3      | 100      | Paid | 39.99 | Everyone       | Medical        |
| 2629| I am Rich Person                    | LIFESTYLE    | 4.2    | 134     | 1.8      | 1000     | Paid | 37.99 | Everyone       | Lifestyle      |
| 2481| A Manual of Acupuncture             | MEDICAL      | 3.5    | 214     | 68.0     | 1000     | Paid | 33.99 | Everyone       | Medical        |
| 4264| Golfshot Plus: Golf GPS             | SPORTS       | 4.1    | 3387    | 25.0     | 50000    | Paid | 29.99 | Everyone       | Sports         |

**Observations:**

- The top 15 entries are variations of the "I am Rich" app, priced at $300 or more (some as high as $400). These apps are notorious for doing nothing except displaying a gemstone, a gimmick that originated in 2008. Their high price is not reflective of genuine commercial apps.
- The install numbers for these apps are relatively low (mostly in the thousands), but some have tens of thousands of installs, possibly due to temporary free promotions or fake reviews.
- Including these apps would skew any analysis of paid app pricing and revenue. Therefore, we should filter them out.

#### 2.3 Remove Apps Priced Above $250

We will keep only apps with a price less than $250.

```python
df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
df_apps_clean.sort_values('Price', ascending=False).head(5)
```

**Output (top 5 after filtering):**

|      | App                           | Category | Rating | Reviews | Size_MBs | Installs | Type | Price | Content_Rating | Genres  |
|-----:|:------------------------------|:---------|-------:|--------:|---------:|---------:|:-----|------:|:---------------|:--------|
| 2281 | Vargo Anesthesia Mega App     | MEDICAL  | 4.6    | 92      | 32.0     | 1000     | Paid | 79.99 | Everyone       | Medical |
| 1407 | LTC AS Legal                  | MEDICAL  | 4.0    | 6       | 1.3      | 100      | Paid | 39.99 | Everyone       | Medical |
| 2629 | I am Rich Person              | LIFESTYLE| 4.2    | 134     | 1.8      | 1000     | Paid | 37.99 | Everyone       | Lifestyle|
| 2481 | A Manual of Acupuncture       | MEDICAL  | 3.5    | 214     | 68.0     | 1000     | Paid | 33.99 | Everyone       | Medical |
| 2463 | PTA Content Master            | MEDICAL  | 4.2    | 64      | 41.0     | 1000     | Paid | 29.99 | Everyone       | Medical |

Now the most expensive "real" apps are mostly **medical apps**, priced around $30–$80. This makes sense: specialised professional apps often command higher prices.

#### 2.4 Add Revenue Estimate Column and Find Top‑Grossing Paid Apps

We estimate revenue by multiplying the price by the number of installs. This is a rough estimate because it assumes every install happened at the current price (ignoring discounts or promotions). Nevertheless, it gives a ballpark figure.

```python
df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
df_apps_clean.sort_values('Revenue_Estimate', ascending=False).head(10)
```

**Output (top 10):**

|      | App                               | Category  | Rating | Reviews  | Size_MBs | Installs  | Type | Price | Content_Rating | Genres                     | Revenue_Estimate |
|-----:|:----------------------------------|:----------|-------:|---------:|---------:|----------:|:-----|------:|:---------------|:---------------------------|-----------------:|
| 9220 | Minecraft                         | FAMILY    | 4.5    | 2,376,564| 19.0     | 10,000,000| Paid | 6.99  | Everyone 10+   | Arcade;Action & Adventure  |     69,900,000.00|
| 8825 | Hitman Sniper                     | GAME      | 4.6    | 408,292  | 29.0     | 10,000,000| Paid | 0.99  | Mature 17+     | Action                     |      9,900,000.00|
| 7151 | Grand Theft Auto: San Andreas     | GAME      | 4.4    | 348,962  | 26.0     |  1,000,000| Paid | 6.99  | Mature 17+     | Action                     |      6,990,000.00|
| 7477 | Facetune - For Free               | PHOTOGRAPHY| 4.4   | 49,553   | 48.0     |  1,000,000| Paid | 5.99  | Everyone       | Photography                |      5,990,000.00|
| 7977 | Sleep as Android Unlock           | LIFESTYLE | 4.5    | 23,966   | 0.85     |  1,000,000| Paid | 5.99  | Everyone       | Lifestyle                  |      5,990,000.00|
| 6594 | DraStic DS Emulator                | GAME      | 4.6    | 87,766   | 12.0     |  1,000,000| Paid | 4.99  | Everyone       | Action                     |      4,990,000.00|
| 6082 | Weather Live                      | WEATHER   | 4.5    | 76,593   | 4.75     |    500,000| Paid | 5.99  | Everyone       | Weather                    |      2,995,000.00|
| 7954 | Bloons TD 5                       | FAMILY    | 4.6    | 190,086  | 94.0     |  1,000,000| Paid | 2.99  | Everyone       | Strategy                   |      2,990,000.00|
| 7633 | Five Nights at Freddy's            | GAME      | 4.6    | 100,805  | 50.0     |  1,000,000| Paid | 2.99  | Teen           | Action                     |      2,990,000.00|
| 6746 | Card Wars - Adventure Time         | FAMILY    | 4.3    | 129,603  | 23.0     |  1,000,000| Paid | 2.99  | Everyone 10+   | Card;Action & Adventure    |      2,990,000.00|

**Key Insights:**

- **Minecraft** leads by a huge margin with nearly $70 million in estimated revenue. Interestingly, it's categorised as **FAMILY**, not GAME.
- **Games dominate** the top 10: if we include Minecraft, Hitman Sniper, GTA: San Andreas, DraStic DS Emulator, Five Nights at Freddy's, and Card Wars – that's **7 out of 10** (or 6 if we strictly count only those listed under GAME category, but Minecraft is effectively a game). This underscores the commercial success of mobile gaming.
- Other categories that make an appearance: Photography (Facetune), Lifestyle (Sleep as Android), and Weather (Weather Live) – but these are exceptions.
- The revenue estimates are rough, but they highlight which paid apps have generated the most income.

---

## 3. Summary of Type Conversions and New Columns

| Column              | Original Type | Conversion Applied                      | New Type | Purpose                                  |
|---------------------|---------------|-----------------------------------------|----------|------------------------------------------|
| `Installs`          | object        | Remove commas → `pd.to_numeric()`       | int64    | Enable sum, average, etc.                |
| `Price`             | object        | Remove `$` → `pd.to_numeric()`          | float64  | Enable arithmetic for revenue estimation |
| `Revenue_Estimate`  | n/a (new)     | `Installs` × `Price`                     | float64  | Rough estimate of total revenue           |

After filtering out apps > $250, our DataFrame size remains **8,199** (since only a handful of extremely expensive apps were removed). All paid‑app analyses from now on will be based on this cleaned, numeric‑ready DataFrame.

---

## 4. Important Caveats

- **Installs are approximate:** The Play Store reports installs as ranges (e.g., "1,000,000+"), and we've taken the lower bound. Actual installs could be higher.
- **Revenue estimate assumes full‑price purchases:** In reality, many installs may have occurred during sales, promotions, or price changes. The estimate is a ballpark.
- **Category flexibility:** Some apps (like Minecraft) are placed in categories that may not match our intuition. This affects genre‑based analysis.

Nevertheless, these transformations give us a solid foundation for deeper visualisations and insights.

---

## 5. What We Learned

- How to detect non‑numeric columns (`.info()`, `.describe()`).
- How to clean strings and convert them to numbers (`.str.replace()`, `pd.to_numeric()`).
- How to spot and remove extreme outliers that distort analysis (the "I am Rich" apps).
- How to create a new calculated column and use it to rank apps.
- Real‑world business insight: games are the top earners among paid apps, and specialised professional apps (medical) command higher prices.

With the data now fully numeric, we are ready to create bar charts, scatter plots, and box plots to explore the app market in depth. The next modules will focus on **Plotly visualisations** to answer our original business questions.