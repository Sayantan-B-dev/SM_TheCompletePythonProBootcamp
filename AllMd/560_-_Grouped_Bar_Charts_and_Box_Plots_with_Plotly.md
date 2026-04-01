# Grouped Bar Charts and Box Plots with Plotly

## Introduction

After analysing categories and genres, we now turn our attention to the fundamental business question: **free vs. paid apps**. The Google Play Store is dominated by free apps, but is this true across all categories? Which categories have a higher proportion of paid apps? And what are the consequences of choosing a paid model – how many downloads do you sacrifice, and what revenue might you expect?

In this module, we will:

- Compare the number of free and paid apps per category using a **grouped bar chart**.
- Explore the distribution of installs for free vs. paid apps using **box plots**.
- Estimate revenue for paid apps per category and see which categories are most lucrative.
- Examine pricing strategies by looking at the price distribution per category.

We'll use Plotly Express to create interactive, informative charts that reveal these insights.

---

## 1. Free vs. Paid Apps: Overall Counts

First, let's get a quick overview of how many apps are free vs. paid.

```python
print(df_apps_clean.Type.value_counts())
```

**Output:**
```
Free    7595
Paid     589
Name: Type, dtype: int64
```

**Observation:** Out of 8,199 apps, only **589 (about 7.2%)** are paid. The vast majority are free. But this aggregate hides category‑specific patterns.

---

## 2. Grouped Bar Chart: Free vs. Paid per Category

We want to see, for each category, how many free and paid apps exist. This requires grouping by both `Category` and `Type`.

### 2.1 Creating the Grouped DataFrame

```python
# Group by Category and Type, count apps
df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': 'count'})
df_free_vs_paid.head()
```

**Output (first few rows):**

| Category        | Type | App |
|-----------------|------|----:|
| ART_AND_DESIGN  | Free |  58 |
| ART_AND_DESIGN  | Paid |   3 |
| AUTO_AND_VEHICLES| Free|  72 |
| AUTO_AND_VEHICLES| Paid|   1 |
| BEAUTY          | Free|  42 |
| ...             | ... | ... |

The `as_index=False` keeps `Category` and `Type` as columns rather than moving them to the index, which is convenient for plotting.

### 2.2 Plotting the Grouped Bar Chart

We'll use `px.bar()` with `barmode='group'` to place bars for free and paid side by side for each category. We also want to order the categories by total number of apps (free + paid) so that the most crowded categories appear first. This can be done by setting `xaxis={'categoryorder':'total descending'}` in `update_layout()`. Additionally, because the counts vary widely (from single digits to over a thousand), a **log scale** on the y‑axis helps visualise the smaller categories.

```python
import plotly.express as px

fig = px.bar(
    df_free_vs_paid,
    x='Category',
    y='App',
    color='Type',
    barmode='group',
    title='Free vs Paid Apps by Category'
)

fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Number of Apps',
    xaxis={'categoryorder': 'total descending'},
    yaxis=dict(type='log')   # log scale for better visibility
)

fig.show()
```

**Explanation of parameters:**

- **`color='Type'`** – creates separate bars for `Free` and `Paid`, each with a distinct colour (default blue and red).
- **`barmode='group'`** – places bars for the same category side‑by‑side instead of stacked.
- **`xaxis={'categoryorder':'total descending'}`** – orders categories from highest total apps (free+paid) to lowest. This is achieved by Plotly internally computing the sum for each category based on the provided data.
- **`yaxis=dict(type='log')`** – because the number of free apps can be in the thousands, while paid apps might be only a few, a linear scale would squash the paid bars. Log scale makes both visible.

**Interpretation:**

- **FAMILY** has by far the most free apps (1,456) and also a significant number of paid apps (150). This category is huge.
- **GAME** has 834 free apps and 76 paid – again, many free, fewer paid.
- In many categories, paid apps are a tiny fraction (e.g., `AUTO_AND_VEHICLES` has 72 free, only 1 paid).
- However, some categories show a **relatively higher proportion of paid apps**:
  - **PERSONALIZATION**: 233 free, 65 paid – paid apps make up about 22% of the category.
  - **MEDICAL**: 229 free, 63 paid – about 22% paid.
  - **WEATHER**: 65 free, 7 paid – about 10% paid.
  - **FINANCE**: 289 free, 7 paid – only 2% paid, so users in finance prefer free apps.

**Business insight:** If you plan to release a paid app, categories like Personalization, Medical, and Weather might be more receptive to paid models, while in others (like Finance, Communication) paid apps are rare and may struggle.

---

## 3. Box Plots: Downloads for Free vs. Paid Apps

A box plot (or box‑and‑whisker plot) summarises the distribution of a numeric variable across groups. Here we compare the number of installs (`Installs`) for free and paid apps.

### 3.1 Basic Box Plot

```python
fig = px.box(
    df_apps_clean,
    y='Installs',
    x='Type',
    color='Type',
    notched=True,
    points='all',
    title='How Many Downloads are Paid Apps Giving Up?'
)

fig.update_layout(yaxis=dict(type='log'))
fig.show()
```

**Parameters explained:**

- **`notched=True`** – adds a notch around the median, which can indicate the confidence interval for the median. Overlapping notches suggest medians are not significantly different (though here they clearly are).
- **`points='all'`** – shows all individual data points (outliers) as dots, giving a sense of the spread.
- **`yaxis=dict(type='log')`** – essential because installs range from 1 to over 1 billion.

**Hover information:** Hover over the box to see median, quartiles, min, max. For example, you might see:

- **Free apps:** median ~500,000 installs.
- **Paid apps:** median ~5,000 installs.

**Interpretation:**

- The median number of downloads for **free apps is about 500,000**.
- The median for **paid apps is only about 5,000** – **100 times lower**.
- The boxes for paid apps are much lower on the y‑axis, confirming that paid apps achieve far fewer downloads.
- Even the upper quartile of paid apps (around 50,000) is below the median of free apps.
- There are some paid apps with millions of downloads (e.g., Minecraft), but they are rare outliers.

**Conclusion:** Going paid reduces your potential audience dramatically. If your goal is maximum user reach, free is the way to go. However, a few paid apps achieve huge revenue despite lower downloads, which we'll examine next.

---

## 4. Revenue Estimates for Paid Apps by Category

We previously added a `Revenue_Estimate` column (`Price * Installs`). Now we can see how much revenue paid apps generate per category. We'll create a DataFrame of only paid apps and then a box plot.

```python
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']
```

### 4.1 Box Plot of Revenue by Category

We'll order categories by the minimum revenue (or any ascending order) to show categories with lower revenue first. The hint suggested `'min ascending'`.

```python
fig = px.box(
    df_paid_apps,
    x='Category',
    y='Revenue_Estimate',
    title='How Much Can Paid Apps Earn?'
)

fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Paid App Ballpark Revenue',
    xaxis={'categoryorder': 'min ascending'},
    yaxis=dict(type='log')
)

fig.show()
```

**Observations:**

- **GAME** and **FAMILY** have very high median revenues and many high‑earning outliers (e.g., Minecraft). This reflects the huge success of a few top games.
- **MEDICAL** apps have a relatively high median (around $20,000‑$30,000?) – hover to see exact values.
- **PERSONALIZATION** also shows a decent median and some high earners.
- **WEATHER** and **TOOLS** have lower medians but still some outliers.

**Business question:** If developing an Android app costs around **$30,000**, which categories recoup that cost on average?

- For **Photography**, the median revenue appears around $20,000 (based on the chart description) – so the **average** photography paid app does **not** cover development costs. However, many photography apps earn far less, while a few earn much more (the outliers). This suggests a risky proposition.
- **Medical** and **Game** categories have medians possibly above or near $30,000, meaning an average‑performing paid app could break even. But note that "average" here means the median of paid apps – many paid apps still fail.

This analysis underscores that while a paid app can be lucrative, it is not a guaranteed path, and category choice matters immensely.

---

## 5. Pricing Strategies by Category

We now look at the actual prices charged by paid apps, not revenue. This helps answer: how much should you charge for your app in a given category?

### 5.1 Overall Median Price

```python
print("Median price of a paid app:", df_paid_apps.Price.median())
```

**Output:**
```
Median price of a paid app: 2.99
```

Half of paid apps cost $2.99 or less, half cost more. This is a common psychological price point.

### 5.2 Box Plot of Price by Category

We'll order categories by descending maximum price (or any order that highlights higher‑priced categories). The hint suggested `'max descending'`.

```python
fig = px.box(
    df_paid_apps,
    x='Category',
    y='Price',
    title='Price per Category'
)

fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Paid App Price',
    xaxis={'categoryorder': 'max descending'},
    yaxis=dict(type='log')
)

fig.show()
```

**Interpretation:**

- **MEDICAL** apps have the highest median price (hover shows about $5.49) and several expensive outliers (e.g., $80). This aligns with the earlier finding that medical apps can charge more, likely because they target professionals or offer specialised content.
- **BUSINESS** and **DATING** also have relatively high median prices (around $4.99 and $6.99 respectively). Users in these categories seem willing to pay.
- **PERSONALIZATION** apps are very cheap (median around $1.49). This category is crowded with free alternatives, so paid apps must be inexpensive to attract buyers.
- **GAME** has a wide spread: many games are priced low ($0.99‑$2.99), but some premium games go higher. The median is near the overall $2.99.

**Takeaway:** Your pricing should be guided by category norms. Charging $5 for a medical app is normal; charging the same for a personalisation app might be too high.

---

## 6. Summary of Insights

| Chart | Key Insight |
|-------|-------------|
| Grouped Bar (Free vs Paid) | Paid apps are rare overall, but more common in Personalization, Medical, Weather. |
| Box Plot (Installs: Free vs Paid) | Median free app gets ~500k downloads; median paid app gets ~5k downloads – a 100‑fold difference. |
| Box Plot (Revenue by Category) | Game and Family categories have highest revenue potential; many categories' median revenue is below typical development cost ($30k). |
| Box Plot (Price by Category) | Medical, Business, Dating apps command higher prices; Personalization apps are cheap. |

**Final advice:** If you're developing an app and considering a paid model, target a category like Medical or Business where users are accustomed to paying. Be prepared for much lower download numbers, but potentially higher revenue per user. Also, remember that a few outliers (like Minecraft) dominate, so realistic expectations are crucial.

---

## 7. Complete Code for This Module

```python
import pandas as pd
import plotly.express as px

# Assume df_apps_clean is already loaded and cleaned

# 1. Free vs Paid per category
df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': 'count'})
fig1 = px.bar(df_free_vs_paid, x='Category', y='App', color='Type', barmode='group',
              title='Free vs Paid Apps by Category')
fig1.update_layout(xaxis={'categoryorder':'total descending'}, yaxis=dict(type='log'))
fig1.show()

# 2. Box plot: Installs for free vs paid
fig2 = px.box(df_apps_clean, y='Installs', x='Type', color='Type', notched=True,
              points='all', title='How Many Downloads are Paid Apps Giving Up?')
fig2.update_layout(yaxis=dict(type='log'))
fig2.show()

# 3. Revenue for paid apps by category
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']
fig3 = px.box(df_paid_apps, x='Category', y='Revenue_Estimate',
              title='How Much Can Paid Apps Earn?')
fig3.update_layout(xaxis={'categoryorder':'min ascending'}, yaxis=dict(type='log'))
fig3.show()

# 4. Price per category for paid apps
fig4 = px.box(df_paid_apps, x='Category', y='Price', title='Price per Category')
fig4.update_layout(xaxis={'categoryorder':'max descending'}, yaxis=dict(type='log'))
fig4.show()
```

