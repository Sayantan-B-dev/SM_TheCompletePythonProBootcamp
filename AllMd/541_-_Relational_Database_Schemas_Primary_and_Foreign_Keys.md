# Relational Database Schemas – Primary and Foreign Keys

## Overview

Until now, we've analysed the `sets.csv` in isolation. However, the real power of relational databases comes from linking tables via keys. In this lesson, we'll:

- Understand the concept of **database schemas**.
- Explore the `themes.csv` file and its relationship to `sets.csv`.
- Learn the difference between **primary keys** and **foreign keys**.
- Use these keys to find the actual names of LEGO themes (e.g., Star Wars) and see which sets belong to them.
- Embed an image of the database schema in the notebook.

---

## 1. The Problem: Unknown Theme Names

When we counted sets per theme using `.value_counts()` on `theme_id`, we got numbers but no names:

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')
set_theme_count = sets['theme_id'].value_counts()
print(set_theme_count.head())
```

**Output:**
```
158    753
501    656
494    398
435    356
503    329
Name: theme_id, dtype: int64
```

We see that theme ID `158` has 753 sets, but we don't know what theme that is. We need to link to the `themes.csv` file.

---

## 2. Database Schema Overview

A **database schema** is the structure that defines how data is organised into tables and how they relate. Our LEGO dataset has three tables:

- `colors.csv`
- `sets.csv`
- `themes.csv`

They are linked through keys:

- In `sets.csv`, `theme_id` is a **foreign key** that references the `id` column in `themes.csv`.
- In `themes.csv`, `id` is the **primary key** (unique for each theme).

This is a classic one-to-many relationship: one theme can have many sets.

---

## 3. Embedding the Schema Image in the Notebook

To visualise the schema, we can insert the provided image using an HTML `<img>` tag in a Markdown cell.

```html
<img src="https://i.imgur.com/Sg4lcjx.png" width="600">
```

If you're running the notebook locally with the assets folder, you can also use:

```html
<img src="assets/rebrickable_schema.png" width="600">
```

This will display the schema diagram, making the relationships clear.

---

## 4. Exploring `themes.csv`

Let's load and examine the themes data.

```python
themes = pd.read_csv('data/themes.csv')
print(themes.head())
```

**Output:**

| id | name            | parent_id |
|----|-----------------|-----------|
| 1  | Technic         | NaN       |
| 2  | Arctic Technic  | 1.0       |
| 3  | Competition     | 1.0       |
| 4  | Expert Builder  | 1.0       |
| 5  | Model           | 1.0       |

- `id`: primary key (unique).
- `name`: theme name (not necessarily unique).
- `parent_id`: optional reference to another theme's `id`, creating a hierarchy (e.g., "Arctic Technic" is a sub‑theme of "Technic").

---

## 5. Finding All Star Wars Themes

Because theme names can repeat (different IDs may have the same name, possibly for different product lines or eras), we search for all rows where `name == 'Star Wars'`.

```python
star_wars_themes = themes[themes['name'] == 'Star Wars']
print(star_wars_themes)
```

**Output:**

|     | id | name       | parent_id |
|-----|----|------------|-----------|
| 17  | 18 | Star Wars  | 1.0       |
| 150 | 158| Star Wars  | NaN       |
| 174 | 209| Star Wars  | 207.0     |
| 211 | 261| Star Wars  | 258.0     |

So there are **four different theme IDs** associated with "Star Wars". This makes sense because LEGO produces multiple distinct Star Wars lines (regular sets, advent calendars, UCS, etc.).

---

## 6. Retrieving Sets for a Specific Theme ID

Now we can use these IDs to filter the `sets` DataFrame and see what kind of sets belong to each theme.

### Example: Theme ID 18

```python
sets_18 = sets[sets['theme_id'] == 18]
print(sets_18[['name', 'year', 'num_parts']].head(10))
```

**Output (first few rows):**

| name                          | year | num_parts |
|-------------------------------|------|-----------|
| R2-D2 / C-3PO Droid Collectors Set | 2002 | 1         |
| Pit Droid                     | 2000 | 223       |
| Battle Droid                  | 2000 | 336       |
| Destroyer Droid               | 2000 | 567       |
| C-3PO                         | 2001 | 339       |
| Stormtrooper                  | 2001 | 360       |
| R2-D2                         | 2002 | 239       |
| Darth Vader                   | 2002 | 388       |
| Jango Fett                    | 2002 | 425       |
| Super Battle Droid            | 2002 | 378       |

These appear to be character-focused sets from the early 2000s.

### Example: Theme ID 209

```python
sets_209 = sets[sets['theme_id'] == 209]
print(sets_209[['name', 'year', 'num_parts']].head(10))
```

**Output:**

| name                          | year | num_parts |
|-------------------------------|------|-----------|
| Star Wars Advent Calendar 2013 | 2013 | 254       |
| Star Wars Advent Calendar 2014 | 2014 | 273       |
| Star Wars Advent Calendar 2015 | 2015 | 291       |
| Star Wars Advent Calendar 2016 | 2016 | 282       |
| Star Wars Advent Calendar 2017 | 2017 | 309       |
| Star Wars Advent Calendar 2018 | 2018 | 307       |
| Star Wars Advent Calendar 2019 | 2019 | 280       |
| Star Wars Advent Calendar 2020 | 2020 | 312       |
| Star Wars Advent Calendar 2011 | 2011 | 267       |
| Star Wars Advent Calendar 2012 | 2012 | 235       |

All are Advent Calendars – a consistent product line.

---

## 7. Complete Code for This Section

```python
import pandas as pd

sets = pd.read_csv('data/sets.csv')
themes = pd.read_csv('data/themes.csv')

# Find all Star Wars theme IDs
star_wars = themes[themes['name'] == 'Star Wars']
print("Star Wars theme entries:")
print(star_wars)

# For each ID, show a few sets
for tid in star_wars['id']:
    print(f"\n--- Theme ID {tid} ---")
    theme_sets = sets[sets['theme_id'] == tid]
    print(theme_sets[['name', 'year', 'num_parts']].head(3))
```

**Output:** (as shown above)

---

## 8. Key Takeaways

- **Primary key**: a column (or combination) that uniquely identifies each row in a table (e.g., `id` in `themes.csv`).
- **Foreign key**: a column that references a primary key in another table (e.g., `theme_id` in `sets.csv` references `themes.id`).
- This relational structure allows us to **join** tables and enrich our analysis with meaningful names.
- The same theme name can appear multiple times in the `themes` table if it represents different product lines or eras.
- Embedding images (like the schema) in Markdown cells enhances documentation and understanding.

---

## 9. Next Steps

Now that we understand how the tables are linked, the next lesson will show how to **merge** DataFrames to combine theme names with set counts, and create a bar chart of the most popular themes.

---

