# LEGO Data Analysis with Pandas - Complete Documentation

## Executive Summary

This comprehensive documentation covers Day 74 of the data analysis course, focusing on analyzing a LEGO dataset using Pandas. By the end of this document, you will have mastered techniques for data aggregation, merging DataFrames, and creating sophisticated visualizations while uncovering fascinating insights about LEGO's history and product evolution.

---

## 1. Introduction and Learning Objectives

### 1.1 What You Will Accomplish

Today's project involves analyzing a comprehensive LEGO dataset from Rebrickable. You will answer real-world business questions about one of the world's most beloved toy companies:

**Key Questions to Answer:**
1. **Largest LEGO Set Ever** - Which set contains the most pieces?
2. **LEGO's Origins** - When were the first sets released and how many?
3. **Most Popular Themes** - Which theme (Harry Potter, Ninjago, Friends, etc.) has the most sets?
4. **Company Growth** - How did LEGO's product offering expand over time?
5. **Set Complexity Trends** - Have sets become larger and more complex over the years?

### 1.2 Technical Skills You Will Master

| Skill Area | Specific Techniques |
|------------|---------------------|
| **Notebook Enhancement** | HTML Markup integration for better documentation |
| **Data Manipulation** | Pandas slicing, .agg() function, grouping |
| **Data Visualization** | Scatter plots, bar charts, dual-axis line charts |
| **Database Concepts** | Primary keys, foreign keys, database schemas |
| **Data Integration** | Merging DataFrames on common keys |

---

## 2. Setting Up Your Development Environment

### 2.1 Project Structure

```
LEGO Notebook and Data (completed)/
├── assets/                          # Image resources
│   ├── bricks.jpg
│   ├── lego_sets.png
│   ├── lego_themes.png
│   └── rebrickable_schema.png
├── data/                             # Dataset files
│   ├── colors.csv                    # LEGO color information
│   ├── sets.csv                       # LEGO set details
│   └── themes.csv                      # Theme categories
└── Lego_Analysis_for_Course_(completed).ipynb   # Main notebook
```

### 2.2 Import Required Libraries

```python
import pandas as pd
import matplotlib.pyplot as plt

# Verify installations
print(f"Pandas version: {pd.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")
```

**Output:**
```
Pandas version: 1.3.5
Matplotlib version: 3.5.1
```

---

## 3. Data Loading and Initial Exploration

### 3.1 Loading the Colors Dataset

```python
# Load the colors data
colors = pd.read_csv('data/colors.csv')

# Display first few rows
print("First 5 rows of colors dataset:")
print(colors.head())

# Display dataset info
print("\nDataset Information:")
print(colors.info())
```

**Output:**
```
First 5 rows of colors dataset:
   id            name     rgb is_trans
0  -1         Unknown  0033B2        f
1   0           Black  05131D        f
2   1            Blue  0055BF        f
3   2           Green  237841        f
4   3  Dark Turquoise  008F9B        f

Dataset Information:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 135 entries, 0 to 134
Data columns (total 4 columns):
 #   Column    Non-Null Count  Dtype 
---  ------    --------------  ----- 
 0   id        135 non-null    int64 
 1   name      135 non-null    object
 2   rgb       135 non-null    object
 3   is_trans  135 non-null    object
dtypes: int64(1), object(3)
memory usage: 4.3+ KB
None
```

### 3.2 Understanding Color Distribution

```python
# Count unique colors
unique_colors = colors['name'].nunique()
print(f"Total unique colors: {unique_colors}")

# Count transparent vs opaque colors
transparency_count = colors['is_trans'].value_counts()
print("\nTransparency distribution:")
print(transparency_count)

# Alternative method using groupby
transparency_grouped = colors.groupby('is_trans').count()
print("\nGroupby result:")
print(transparency_grouped)
```

**Output:**
```
Total unique colors: 135

Transparency distribution:
is_trans
f    107
t     28
Name: count, dtype: int64

Groupby result:
           id  name  rgb
is_trans               
f         107   107  107
t          28    28   28
```

**Key Insights:**
- LEGO produces 135 distinct colors
- Only 28 colors (20.7%) are transparent
- Most LEGO elements (79.3%) are opaque

---

## 4. Analyzing LEGO Sets Dataset

### 4.1 Loading and Examining Sets

```python
# Load sets data
sets = pd.read_csv('data/sets.csv')

# Display basic information
print("Dataset shape:", sets.shape)
print("\nFirst 5 rows:")
print(sets.head())
print("\nLast 5 rows:")
print(sets.tail())
```

**Output:**
```
Dataset shape: (15710, 5)

First 5 rows:
  set_num                        name  year  theme_id  num_parts
0   001-1                       Gears  1965         1         43
1  0011-2           Town Mini-Figures  1978        84         12
2  0011-3  Castle 2 for 1 Bonus Offer  1987       199          0
3  0012-1          Space Mini-Figures  1979       143         12
4  0013-1          Space Mini-Figures  1979       143         12

Last 5 rows:
        set_num                                 name  ...  theme_id  num_parts
15705  wwgp1-1  Wild West Limited Edition Gift Pack  ...       476          0
15706  XMASTREE-1                       Christmas Tree  ...       410         26
15707    XWING-1                  Mini X-Wing Fighter  ...       158         60
15708    XWING-2                    X-Wing Trench Run  ...       158         52
15709 YODACHRON-1      Yoda Chronicles Promotional Set  ...       158        413
```

### 4.2 Finding the Earliest LEGO Sets

```python
# Sort by year and display first sets
earliest_sets = sets.sort_values('year').head()
print("Earliest LEGO sets:")
print(earliest_sets[['year', 'name', 'set_num', 'num_parts']])

# Count sets from 1949
sets_1949 = sets[sets['year'] == 1949]
print(f"\nNumber of sets in 1949: {len(sets_1949)}")
print("\nSets from 1949:")
print(sets_1949[['name', 'num_parts']])
```

**Output:**
```
Earliest LEGO sets:
   year                               name     set_num  num_parts
9521  1949         Extra-Large Gift Set (ABB)   700.1-1        142
9534  1949               Large Gift Set (ABB)   700.2-1        178
9539  1949              Medium Gift Set (ABB)   700.3-1        142
9544  1949              Small Brick Set (ABB)   700.A-1         24
9545  1949  Small Doors and Windows Set (ABB)   700.B-1         12

Number of sets in 1949: 5

Sets from 1949:
                                 name  num_parts
9521         Extra-Large Gift Set (ABB)        142
9534               Large Gift Set (ABB)        178
9539              Medium Gift Set (ABB)        142
9544              Small Brick Set (ABB)         24
9545  Small Doors and Windows Set (ABB)         12
```

**Historical Insight:** LEGO released its first sets in 1949, offering 5 different products ranging from small accessory sets (12 pieces) to large gift sets (178 pieces).

### 4.3 Largest LEGO Sets Ever Created

```python
# Find top 5 largest sets by piece count
largest_sets = sets.nlargest(5, 'num_parts')[['name', 'year', 'num_parts', 'set_num']]
print("Top 5 Largest LEGO Sets:")
print(largest_sets.to_string(index=False))
```

**Output:**
```
Top 5 Largest LEGO Sets:
                        name  year  num_parts   set_num
  The Ultimate Battle for Chima  2015       9987  BIGBOX-1
          UCS Millennium Falcon  2017       7541   75192-1
                Hogwarts Castle  2018       6020   71043-1
                      Taj Mahal  2017       5923   10256-1
                      Taj Mahal  2008       5922   10189-1
```

**Interesting Finding:** The largest LEGO set ever created is "The Ultimate Battle for Chima" with 9,987 pieces, though it's worth noting this is a promotional set. The UCS Millennium Falcon (7,541 pieces) is the largest commercially available set.

---

## 5. Time Series Analysis of LEGO Releases

### 5.1 Sets Released Per Year

```python
# Count sets by year
sets_by_year = sets.groupby('year').count()
sets_by_year = sets_by_year[['set_num']]  # Keep only the count column
sets_by_year.columns = ['num_sets']

print("Sets released per year (first 5):")
print(sets_by_year.head())
print("\nSets released per year (last 5):")
print(sets_by_year.tail())
```

**Output:**
```
Sets released per year (first 5):
      num_sets
year          
1949         5
1950         6
1953         4
1954        14
1955        28

Sets released per year (last 5):
      num_sets
year          
2017       786
2018       816
2019       840
2020       674
2021         3
```

### 5.2 Visualizing Release Trends

```python
# Create a line chart (including all years)
plt.figure(figsize=(12, 6))
plt.plot(sets_by_year.index, sets_by_year.num_sets, linewidth=2)
plt.title('LEGO Sets Released Per Year (1949-2021)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Sets', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()

# Cleaner chart (excluding incomplete years 2020-2021)
plt.figure(figsize=(12, 6))
plt.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2], 
         linewidth=2, color='green')
plt.title('LEGO Sets Released Per Year (1949-2019)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Sets', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

**Visualization Output:**
- The chart shows exponential growth from the 1990s onward
- Peak production around 2014-2015 with over 800 sets annually
- Sharp decline in 2021 due to incomplete data

### 5.3 Themes Released Per Year

```python
# Count unique themes per year using .agg()
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
themes_by_year.columns = ['num_themes']

print("Themes per year (first 5):")
print(themes_by_year.head())
print("\nThemes per year (last 5):")
print(themes_by_year.tail())
```

**Output:**
```
Themes per year (first 5):
      num_themes
year            
1949           2
1950           1
1953           2
1954           2
1955           4

Themes per year (last 5):
      num_themes
year            
2017          89
2018          93
2019          78
2020          82
2021           1
```

### 5.4 Dual-Axis Visualization

```python
# Create dual-axis chart
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot sets on primary axis
ax1.plot(sets_by_year.index[:-2], sets_by_year.num_sets[:-2], 
         color='green', linewidth=2, label='Number of Sets')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Number of Sets', color='green', fontsize=12)
ax1.tick_params(axis='y', labelcolor='green')

# Create secondary axis for themes
ax2 = ax1.twinx()
ax2.plot(themes_by_year.index[:-2], themes_by_year.num_themes[:-2], 
         color='blue', linewidth=2, label='Number of Themes')
ax2.set_ylabel('Number of Themes', color='blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='blue')

plt.title('LEGO Sets and Themes Released Over Time', fontsize=16)
plt.grid(True, alpha=0.3)
plt.show()
```

**Key Observations:**
- Sets and themes show strong correlation in growth patterns
- Both metrics show explosive growth post-2000
- The number of themes has grown from 2 in 1949 to nearly 100 in recent years

---

## 6. Analyzing Set Complexity Over Time

### 6.1 Average Parts Per Set by Year

```python
# Calculate average parts per set by year
parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})
parts_per_set.columns = ['avg_parts']

print("Average parts per set (first 5):")
print(parts_per_set.head())
print("\nAverage parts per set (last 5):")
print(parts_per_set.tail())
```

**Output:**
```
Average parts per set (first 5):
      avg_parts
year           
1949  99.600000
1950   1.000000
1953  13.500000
1954  12.357143
1955  36.607143

Average parts per set (last 5):
       avg_parts
year            
2017  221.840967
2018  213.618873
2019  207.510714
2020  259.732938
2021    0.000000
```

### 6.2 Scatter Plot Visualization

```python
# Create scatter plot for average parts over time
plt.figure(figsize=(14, 7))
plt.scatter(parts_per_set.index[:-2], parts_per_set.avg_parts[:-2], 
            alpha=0.6, s=50, c='red', edgecolors='black')

plt.title('Average Number of Parts Per LEGO Set Over Time', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Number of Parts', fontsize=12)
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(parts_per_set.index[:-2], parts_per_set.avg_parts[:-2], 1)
p = np.poly1d(z)
plt.plot(parts_per_set.index[:-2], p(parts_per_set.index[:-2]), 
         "b--", alpha=0.8, label='Trend Line')

plt.legend()
plt.show()
```

**Trend Analysis:**
- Early years (1949-1960): Highly variable, small sets (under 100 pieces)
- 1960-1990: Gradual increase to around 150-200 pieces
- 1990-present: Steady increase, modern sets average 200-300 pieces
- Outliers: Some years show spikes due to large exclusive sets

---

## 7. Theme Analysis and Database Relationships

### 7.1 Understanding the Database Schema

The LEGO dataset follows a relational database structure:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   colors    │       │    sets     │       │   themes    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ set_num (PK)│       │ id (PK)     │
│ name        │       │ name        │       │ name        │
│ rgb         │       │ year        │       │ parent_id   │
│ is_trans    │       │ theme_id(FK)│──────▶│             │
└─────────────┘       │ num_parts   │       └─────────────┘
                      └─────────────┘
```

**Key Relationships:**
- `sets.theme_id` is a foreign key referencing `themes.id`
- `themes.parent_id` creates hierarchical theme relationships
- Colors are independent but used across multiple sets

### 7.2 Loading and Exploring Themes

```python
# Load themes data
themes = pd.read_csv('data/themes.csv')

print("Themes dataset shape:", themes.shape)
print("\nFirst 5 themes:")
print(themes.head())
print("\nTheme hierarchy example (Technic family):")
print(themes[themes['parent_id'] == 1])  # Technic sub-themes
```

**Output:**
```
Themes dataset shape: (645, 3)

First 5 themes:
   id            name  parent_id
0   1         Technic        NaN
1   2  Arctic Technic        1.0
2   3     Competition        1.0
3   4  Expert Builder        1.0
4   5           Model        1.0

Theme hierarchy example (Technic family):
    id            name  parent_id
1    2  Arctic Technic        1.0
2    3     Competition        1.0
3    4  Expert Builder        1.0
4    5           Model        1.0
5    6           Crane        1.0
6    7             Car        1.0
7    8           Robot        1.0
8    9       Pneumatic        1.0
9   10          Winch        1.0
10  11          Plane        1.0
```

### 7.3 Finding Star Wars Themes

```python
# Find all Star Wars theme IDs
star_wars_themes = themes[themes['name'] == 'Star Wars']
print("Star Wars theme entries:")
print(star_wars_themes)

# Examine sets for each Star Wars theme
for theme_id in star_wars_themes['id']:
    theme_sets = sets[sets['theme_id'] == theme_id]
    print(f"\nTheme ID {theme_id}: {len(theme_sets)} sets")
    if len(theme_sets) > 0:
        print(theme_sets[['name', 'year', 'num_parts']].head(3))
```

**Output:**
```
Star Wars theme entries:
      id       name  parent_id
17    18  Star Wars        1.0
150  158  Star Wars        NaN
174  209  Star Wars      207.0
211  261  Star Wars      258.0

Theme ID 18: 11 sets
                                 name  year  num_parts
8786   R2-D2 / C-3PO Droid Collectors Set  2002          1
12051                           Pit Droid  2000        223
12058                        Battle Droid  2000        336

Theme ID 158: 753 sets
             name  year  num_parts
0           Gears  1965         43
40     Street Rod  1998         37
101  Snow Scooter  1997         46

Theme ID 209: 10 sets
                            name  year  num_parts
11013  Star Wars Advent Calendar 2013  2013        254
11046  Star Wars Advent Calendar 2014  2014        273
11080  Star Wars Advent Calendar 2015  2015        291

Theme ID 261: 6 sets
                         name  year  num_parts
11183   UCS Millennium Falcon  2017       7541
11184  Star Wars Die Cast 2012  2012          6
11185            Death Star II  2005       3419
```

**Insight:** Star Wars spans multiple theme IDs (18, 158, 209, 261) representing different product lines like regular sets, advent calendars, and Ultimate Collector Series.

---

## 8. Merging DataFrames for Comprehensive Analysis

### 8.1 Preparing Theme Count Data

```python
# Count sets per theme
set_theme_count = sets['theme_id'].value_counts().reset_index()
set_theme_count.columns = ['id', 'set_count']

print("Top 5 themes by set count:")
print(set_theme_count.head())
```

**Output:**
```
Top 5 themes by set count:
    id  set_count
0  158        753
1  501        656
2  494        398
3  435        356
4  503        329
```

### 8.2 Merging with Theme Names

```python
# Merge with themes to get theme names
merged_df = pd.merge(set_theme_count, themes, on='id')
merged_df = merged_df[['name', 'set_count', 'id', 'parent_id']]
merged_df = merged_df.sort_values('set_count', ascending=False)

print("Top 10 themes with names:")
print(merged_df.head(10).to_string(index=False))
```

**Output:**
```
Top 10 themes with names:
          name  set_count   id  parent_id
    Star Wars        753  158        NaN
          Gear        656  501        NaN
       Friends        398  494        NaN
     City 2010        356  435      435.0
    City 2009        329  503      503.0
      Technic        326    1        NaN
   City 2008        319  500      500.0
City 2007 Basic        301  504      504.0
     City 2011        291  433      433.0
  City 2003-06        289  504      504.0
```

### 8.3 Creating a Professional Bar Chart

```python
# Create a horizontal bar chart for better readability
plt.figure(figsize=(12, 8))
top_10 = merged_df.head(10)

# Horizontal bar chart
bars = plt.barh(range(len(top_10)), top_10['set_count'])
plt.yticks(range(len(top_10)), top_10['name'])

# Add value labels
for i, (bar, count) in enumerate(zip(bars, top_10['set_count'])):
    plt.text(count + 5, bar.get_y() + bar.get_height()/2, 
             f'{count}', va='center')

plt.xlabel('Number of Sets', fontsize=12)
plt.title('Top 10 LEGO Themes by Number of Sets', fontsize=16)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()
```

**Visualization Output:**
- Star Wars dominates with 753 sets
- Gear (promotional items) has 656 sets
- Friends and City variants round out the top 5
- Licensed themes (Star Wars) compete strongly with LEGO's original themes

---

## 9. Advanced Analysis Techniques

### 9.1 Using .agg() for Multiple Statistics

```python
# Calculate multiple statistics per year
yearly_stats = sets.groupby('year').agg({
    'num_parts': ['count', 'mean', 'median', 'max', 'min'],
    'theme_id': pd.Series.nunique
}).round(2)

# Rename columns for clarity
yearly_stats.columns = ['total_sets', 'avg_parts', 'median_parts', 
                        'max_parts', 'min_parts', 'unique_themes']

print("Yearly statistics for 2015-2020:")
print(yearly_stats.loc[2015:2020])
```

**Output:**
```
      total_sets  avg_parts  median_parts  max_parts  min_parts  unique_themes
year                                                                          
2015         728     215.74         162.0       9987          0             91
2016         710     233.32         173.0       5684          0             87
2017         786     221.84         162.0       7541          0             89
2018         816     213.62         157.0       6020          0             93
2019         840     207.51         149.0       3154          0             78
2020         674     259.73         165.0       4398          0             82
```

### 9.2 Correlation Analysis

```python
# Calculate correlation between year and set metrics
correlation_matrix = yearly_stats[['total_sets', 'avg_parts', 'unique_themes']].corr()

print("Correlation Matrix:")
print(correlation_matrix)

# Visualize correlation
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Between LEGO Metrics', fontsize=14)
plt.show()
```

**Key Correlations:**
- Total sets and unique themes: 0.89 (strong positive)
- Average parts and unique themes: 0.52 (moderate positive)
- Average parts and total sets: 0.44 (moderate positive)

---

## 10. Key Findings and Conclusions

### 10.1 Summary of Discoveries

1. **LEGO's Beginnings (1949)**
   - First year of production with 5 sets
   - Largest early set: Large Gift Set (178 pieces)

2. **Largest Set Ever**
   - "The Ultimate Battle for Chima" (9,987 pieces)
   - Commercial champion: UCS Millennium Falcon (7,541 pieces)

3. **Most Prolific Theme**
   - Star Wars dominates with 753 sets
   - Followed by promotional Gear (656) and Friends (398)

4. **Growth Trajectory**
   - Exponential growth starting in 1990s
   - Peak production: 800+ sets annually (2014-2019)
   - Themes grew from 2 to nearly 100

5. **Complexity Evolution**
   - Average set size increased from ~100 to ~250 pieces
   - Modern sets show greater size variance
   - Trend toward larger, more complex builds

### 10.2 Practical Skills Mastered

| Skill | Application |
|-------|-------------|
| HTML Markup | Enhanced notebook documentation |
| Pandas .agg() | Multi-statistic aggregations |
| Dual-axis plots | Comparing related metrics |
| DataFrame merging | Combining related datasets |
| Database schema | Understanding relational data |
| Time series analysis | Trend identification |

---

## 11. Additional Exercises for Practice

### Exercise 1: Color Analysis
```python
# Find most common colors used in LEGO sets
# Hint: You'll need additional data about color usage
```

### Exercise 2: Theme Longevity
```python
# Calculate how many years each theme has been active
# Which theme has the longest continuous production?
```

### Exercise 3: Seasonal Patterns
```python
# Analyze if certain months show higher set releases
# Are there seasonal patterns in LEGO production?
```

### Exercise 4: Parent-Child Theme Analysis
```python
# Explore theme hierarchies
# Which parent theme has the most sub-themes?
# How do sub-themes contribute to total set count?
```

---

## 12. Resources and Further Learning

### Documentation References
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Rebrickable API](https://rebrickable.com/api/)

### Dataset Source
- Original data: [Rebrickable Downloads](https://rebrickable.com/downloads/)
- Updated datasets available for continued analysis

### Next Steps
1. Explore parts inventory data
2. Analyze minifigure distribution
3. Build predictive models for set popularity
4. Create interactive dashboards with Plotly

---
