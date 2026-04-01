# Preliminary Exploration: The Highest Ratings, Most Reviews, and Largest Size

## Introduction

Now that our dataset is clean (free of missing values and duplicates), we can begin exploring it to uncover initial patterns. Preliminary exploration is like getting to know a new friend – we ask simple questions to understand their personality, quirks, and extremes. In this module, we will investigate three basic aspects of the apps:

1.  **Highest Rated Apps:** Which apps have perfect or near‑perfect ratings? Is a high rating always a reliable indicator of quality?
2.  **Largest Apps:** How big can an Android app be? Is there a size limit imposed by the Google Play Store?
3.  **Most Reviewed Apps:** Which apps have received the most user feedback? Do any paid apps make it into the top tier of reviews?

These questions will help us validate our data, discover potential outliers, and form hypotheses for deeper analysis.

---

## 1. Highest Rated Apps

### Challenge

> **Challenge:** Identify which apps are the highest rated. What problem might you encounter if you rely exclusively on ratings alone to determine the quality of an app?

### Solution

We can use the `.sort_values()` method to order the DataFrame by the `Rating` column in descending order and then look at the top rows.

```python
# Sort by Rating from highest to lowest and show the top 5
df_apps_clean.sort_values('Rating', ascending=False).head()
```

**Output:**

|     | App                    | Category     | Rating | Reviews | Size_MBs | Installs | Type | Price | Content_Rating | Genres     |
|----:|:-----------------------|:-------------|-------:|--------:|---------:|:---------|:-----|:------|:---------------|:-----------|
| 21  | KBA-EZ Health Guide    | MEDICAL      | 5.0    | 4       | 25.0     | 1        | Free | 0     | Everyone       | Medical    |
| 1230| Sway Medical           | MEDICAL      | 5.0    | 3       | 22.0     | 100      | Free | 0     | Everyone       | Medical    |
| 1227| AJ Men's Grooming      | LIFESTYLE    | 5.0    | 2       | 22.0     | 100      | Free | 0     | Everyone       | Lifestyle  |
| 1224| FK Dedinje BGD         | SPORTS       | 5.0    | 36      | 2.6      | 100      | Free | 0     | Everyone       | Sports     |
| 1223| CB VIDEO VISION        | PHOTOGRAPHY  | 5.0    | 13      | 2.6      | 100      | Free | 0     | Everyone       | Photography|

### Interpretation

At first glance, it seems wonderful that so many apps have a perfect 5‑star rating. However, a closer look reveals a crucial detail: **these apps have very few reviews** (between 1 and 36). Apps with a handful of ratings can easily achieve a perfect score if all those ratings are positive – often from friends, family, or the developers themselves. Such apps may not have been tested by the broader public and could be low‑quality or even non‑functional.

**The Problem with Relying Solely on Ratings:**

- **Low‑review bias:** A high average rating based on a small number of votes is not statistically meaningful. The rating could change dramatically with just one or two additional reviews.
- **Popularity not considered:** An app with a 4.8 rating from 10 million users is far more credible and indicative of widespread quality than an app with a 5.0 from 10 users.
- **Missing context:** Ratings alone don't tell you about the app's features, stability, or whether it meets user needs.

**Why This Matters:** In later analyses, we will often need to consider both rating and the number of reviews together to gauge true popularity and user satisfaction. For now, this exercise teaches us to be cautious with simple aggregates.

---

## 2. Largest Apps (by Size in MB)

### Challenge

> **Challenge:** What's the size in megabytes (MB) of the largest Android apps in the Google Play Store? Based on the data, do you think there could be a limit in place or can developers make apps as large as they please?

### Solution

We sort the DataFrame by the `Size_MBs` column in descending order.

```python
df_apps_clean.sort_values('Size_MBs', ascending=False).head()
```

**Output:**

|      | App                                 | Category              | Rating | Reviews | Size_MBs | Installs    | Type | Price | Content_Rating | Genres                 |
|-----:|:------------------------------------|:----------------------|-------:|--------:|---------:|:------------|:-----|:------|:---------------|:-----------------------|
| 9942 | Talking Babsy Baby: Baby Games      | LIFESTYLE             | 4.0    | 140,995 | 100.0    | 10,000,000  | Free | 0     | Everyone       | Lifestyle;Pretend Play |
| 10687| Hungry Shark Evolution              | GAME                  | 4.5    | 6,074,334| 100.0    | 100,000,000 | Free | 0     | Teen           | Arcade                 |
| 9943 | Miami crime simulator               | GAME                  | 4.0    | 254,518 | 100.0    | 10,000,000  | Free | 0     | Mature 17+     | Action                 |
| 9944 | Gangster Town: Vice District        | FAMILY                | 4.3    | 65,146  | 100.0    | 10,000,000  | Free | 0     | Mature 17+     | Simulation             |
| 3144 | Vi Trainer                          | HEALTH_AND_FITNESS    | 3.6    | 124     | 100.0    | 5,000       | Free | 0     | Everyone       | Health & Fitness       |

### Interpretation

Notice that several apps have a size of exactly **100.0 MB**. This is not a coincidence. A quick search or prior knowledge reveals that **the Google Play Store imposes a maximum APK file size of 100 MB**. If an app needs to be larger, developers must use **APK expansion files** (OBB files), which can host additional assets (up to 2 GB). However, the core APK itself cannot exceed 100 MB.

- **Evidence of a limit:** The presence of multiple apps at exactly 100.0 MB strongly suggests a hard limit. If there were no limit, we would expect to see a continuous range of sizes beyond 100 MB. Instead, 100.0 MB appears to be a ceiling.
- **Practical implication:** Developers of large games must carefully manage assets and often require users to download additional data after installation. This can affect user experience, especially on metered connections.

**Why This Matters:** Understanding the size constraint helps us interpret the distribution of app sizes and explains why we see this clustering at 100 MB. It also informs discussions about app complexity and target devices.

---

## 3. Most Reviewed Apps

### Challenge

> **Challenge:** Which apps have the highest number of reviews? Are there any paid apps among the top 50?

### Solution

We sort by the `Reviews` column in descending order and examine the top 50 rows. Because there are many apps, we'll display the top 10 first, but the challenge asks for the top 50.

```python
# Get top 50 most reviewed apps
top_50_reviews = df_apps_clean.sort_values('Reviews', ascending=False).head(50)
top_50_reviews[['App', 'Category', 'Reviews', 'Type', 'Price']]
```

**Output (first 10 rows shown):**

|       | App                                      | Category          | Reviews   | Type | Price |
|------:|:-----------------------------------------|:------------------|----------:|:-----|:------|
| 10805 | Facebook                                 | SOCIAL            | 78,158,306| Free | 0     |
| 10785 | WhatsApp Messenger                       | COMMUNICATION     | 69,119,316| Free | 0     |
| 10806 | Instagram                                | SOCIAL            | 66,577,313| Free | 0     |
| 10784 | Messenger – Text and Video Chat for Free | COMMUNICATION     | 56,642,847| Free | 0     |
| 10650 | Clash of Clans                           | GAME              | 44,891,723| Free | 0     |
| 10744 | Clean Master- Space Cleaner & Antivirus  | TOOLS             | 42,916,526| Free | 0     |
| 10835 | Subway Surfers                            | GAME              | 27,722,264| Free | 0     |
| 10828 | YouTube                                  | VIDEO_PLAYERS     | 25,655,305| Free | 0     |
| 10746 | Security Master - Antivirus, VPN, AppLock| TOOLS             | 24,900,999| Free | 0     |
| 10584 | Clash Royale                             | GAME              | 23,133,508| Free | 0     |

### Interpretation

- **Top Apps are Household Names:** The list is dominated by global giants: Facebook, WhatsApp, Instagram, Messenger, YouTube. These are apps with billions of users, so the number of reviews is naturally enormous.
- **No Paid Apps in Top 50:** Scanning the entire top 50 (which we have done but not fully printed here) reveals that **every single one of the top 50 most‑reviewed apps is free**. This is a powerful observation. It suggests that paid apps, no matter how good, simply cannot achieve the same level of widespread adoption and user feedback as free apps.

**Why This Matters:**

- **User acquisition:** Free apps remove the barrier to entry, allowing for massive download numbers, which in turn generate many reviews. Paid apps have a much smaller potential audience.
- **Monetisation trade‑off:** Developers face a clear choice: go free and hope to earn through ads/in‑app purchases, or go paid and accept a smaller, but possibly more dedicated, user base. The data shows that paid apps are almost invisible in terms of raw popularity metrics.

This insight will be crucial later when we estimate revenue and compare free vs. paid app performance.

---

## Summary of Preliminary Findings

| Exploration          | Key Insight                                                                                                 |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| Highest Rated Apps   | Perfect ratings often come from apps with very few reviews. Ratings must be considered alongside review count. |
| Largest Apps         | The Google Play Store imposes a 100 MB limit on APK files. Many apps hit this exact maximum.               |
| Most Reviewed Apps   | The top 50 most‑reviewed apps are all free. Paid apps do not achieve comparable levels of user engagement. |

These early observations already give us valuable business intelligence:

- If you want a high rating quickly, target a niche audience and get a few positive reviews – but that rating won't reflect true market acceptance.
- If you're building a large game, plan for expansion files and manage user expectations about initial download size.
- If you're considering a paid‑only model, understand that you will likely never reach the audience size of a free app.

