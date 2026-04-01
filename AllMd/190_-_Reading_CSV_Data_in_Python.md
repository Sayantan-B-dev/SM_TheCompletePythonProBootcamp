## `csv` MODULE — FOUNDATIONS AND INTERNAL MECHANICS

### What `import csv` Actually Provides

The built-in `csv` module is a **low-level text parsing utility** designed to read and write tabular data stored as plain text, where rows are separated by newlines and columns are separated by delimiters (commonly commas).

It does **not** understand data types, schemas, missing values, or relationships. Everything is treated as **strings** unless you manually convert it.

---

## How CSV Data Is Stored (Physically and Logically)

### Physical Representation (Disk Level)

A CSV file is just a text file.

```
day,temp,condition
Monday,21,Sunny
Tuesday,18,Rainy
Wednesday,24,Sunny
```

On disk:

* Each **row** = one line (`\n`)
* Each **column** = separated by delimiter (`,` by default)
* No metadata
* No data types
* No enforced structure

---

### Logical Representation (When Read by `csv.reader`)

```text
[
  ["day", "temp", "condition"],
  ["Monday", "21", "Sunny"],
  ["Tuesday", "18", "Rainy"],
  ["Wednesday", "24", "Sunny"]
]
```

Important:

* Everything is a **string**
* Header row is **not special**
* No automatic conversion
* No column labels

---

## `csv.reader` — LINE-BY-LINE STREAM PARSER

### What `csv.reader` Returns

* An **iterator**
* Each iteration gives **one row as a list of strings**
* Reads sequentially (memory efficient)

---

### Your Original Code — Deep Breakdown

```python
import csv

# Open the CSV file in read mode
with open("weather_data.csv", mode="r") as file:
    
    # csv.reader turns file text into rows (lists of strings)
    data = csv.reader(file)
    
    tempratures = []

    # Loop through each row
    for d in data:
        
        # d is a list like: ["Monday", "21", "Sunny"]
        
        # Skip the header row by checking column name
        if d[1] != "temp":
            
            # Convert string to integer manually
            tempratures.append(int(d[1]))

    print(tempratures)
```

### Expected Output

```
[21, 18, 24]
```

---

## Why `csv.reader` Feels Painful as Data Grows

### Structural Limitations

| Problem                | Why It Happens                  |
| ---------------------- | ------------------------------- |
| Manual type conversion | CSV has no type system          |
| Header handling        | Headers are plain text          |
| Missing values         | Empty strings cause crashes     |
| Column indexing        | `d[3]` is unreadable            |
| No filtering           | Must write loops                |
| No aggregation         | Manual logic required           |
| No validation          | Silent data corruption possible |

---

### Example of CSV Becoming “Too Complicated”

```
date,temp,humidity,city,wind_speed
2024-01-01,21,,Delhi,5.6
2024-01-02,not_available,82,Mumbai,
2024-01-03,24,78,,3.2
```

With `csv.reader`, you must:

* Handle missing values
* Validate numbers
* Parse dates
* Track columns by index
* Guard every conversion

This becomes **error-prone and unreadable**.

---

## WHY PANDAS EXISTS (THE SOLUTION)

### What Pandas Is

Pandas is a **high-level data analysis library** built on top of:

* NumPy (fast arrays)
* C-extensions (performance)
* Vectorized operations (no manual loops)

It treats CSV not as text, but as **structured data**.

---

## CORE CONCEPT: `DataFrame`

A `DataFrame` is:

* A **2D labeled table**
* Columns have names
* Rows have indices
* Columns have inferred data types

Conceptual model:

```
Index | day       | temp | condition
------------------------------------
0     | Monday    | 21   | Sunny
1     | Tuesday   | 18   | Rainy
2     | Wednesday | 24   | Sunny
```

---

## `pd.read_csv()` — WHAT IT DOES INTERNALLY

When you call:

```python
import pandas as pd

data = pd.read_csv("weather_data.csv")
```

Pandas automatically:

* Reads file efficiently (C engine)
* Detects delimiter
* Identifies headers
* Infers data types
* Handles missing values (`NaN`)
* Assigns column labels
* Builds an indexed structure

---

## Your Pandas Code — Line-by-Line Explanation

```python
import pandas as pd

# Read CSV and convert it into a DataFrame
data = pd.read_csv("weather_data.csv")

# Access a single column by label
print(data["temp"])
```

### What `data["temp"]` Is

* A **Series object**
* 1D labeled array
* Vectorized
* Type-aware

---

### Expected Output

```
0    21
1    18
2    24
Name: temp, dtype: int64
```

---

## Why This Is Powerful (Compared to `csv.reader`)

### Same Task Comparison

| Task           | csv.reader    | pandas         |
| -------------- | ------------- | -------------- |
| Read file      | Manual        | One function   |
| Skip header    | Manual        | Automatic      |
| Convert types  | Manual        | Automatic      |
| Missing values | Manual checks | Built-in `NaN` |
| Column access  | Index-based   | Name-based     |
| Filtering      | Loops         | Vectorized     |
| Aggregation    | Complex loops | One method     |

---

## Beginner Pandas Essentials (From Official Docs)

### Reading Data

```python
df = pd.read_csv("weather_data.csv")
```

---

### Inspecting Data

```python
print(df.head())      # First 5 rows
print(df.tail())      # Last 5 rows
print(df.info())      # Structure and dtypes
print(df.describe())  # Statistics
```

---

### Column Access

```python
df["temp"]        # Single column (Series)
df[["temp"]]      # Still DataFrame
```

---

### Filtering Rows

```python
df[df["temp"] > 20]
```

---

### Handling Missing Values

```python
df.dropna()           # Remove rows with missing values
df.fillna(0)          # Replace missing values
```

---

### Aggregations

```python
df["temp"].mean()
df["temp"].max()
df["temp"].min()
```

---

## When to Use What

| Use Case            | Tool     |
| ------------------- | -------- |
| Small scripts       | `csv`    |
| Educational parsing | `csv`    |
| Real datasets       | `pandas` |
| Analytics           | `pandas` |
| Data cleaning       | `pandas` |
| ML pipelines        | `pandas` |

---

## Mental Model Shift (Critical)

* `csv.reader` → **Text processing**
* `pandas` → **Data modeling**

CSV is not data — **it is a storage format**
Pandas turns storage into **meaningful structure**

This is why every real-world data workflow moves to pandas early.
