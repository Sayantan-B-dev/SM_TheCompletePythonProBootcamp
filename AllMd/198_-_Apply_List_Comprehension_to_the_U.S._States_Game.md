## Real-Life Data Fetching in Python — Practical Patterns

> **Data fetching** means *bringing external data into your program*, transforming it, and using it for logic, analysis, or visualization.

Python usually fetches data from:

* Files (`.txt`, `.csv`, `.json`)
* Memory structures
* User input
* APIs (skipped here as you asked file-centric + turtle)

---

# 1. Fetching Data from `.txt` Files (Plain Text)

### Real-Life Scenario

Log files, configuration files, notes, system outputs.

---

## Example 1 — Reading Usernames from a `.txt` File

### File: `users.txt`

```text
asha
ravi
neha
amit
```

---

### Code

```python
# Open the file in read mode
with open("users.txt", "r") as file:
    # Read all lines into a list
    users = file.readlines()

# Clean newline characters and convert to uppercase
clean_users = [user.strip().upper() for user in users]

print(clean_users)
```

### Expected Output

```text
['ASHA', 'RAVI', 'NEHA', 'AMIT']
```

### Explanation

* `readlines()` fetches raw data
* `.strip()` cleans formatting noise
* List comprehension transforms fetched data

---

# 2. Fetching Structured Data from `.csv` Files

### Real-Life Scenario

Excel exports, reports, databases, analytics pipelines.

---

## Example 2 — Reading Student Scores from CSV

### File: `students.csv`

```text
name,score
Asha,85
Ravi,35
Neha,92
```

---

### Code

```python
import csv

students = []

# Open CSV file
with open("students.csv", newline="") as file:
    reader = csv.DictReader(file)

    # Fetch each row as a dictionary
    for row in reader:
        students.append(row)

print(students)
```

### Expected Output

```text
[
 {'name': 'Asha', 'score': '85'},
 {'name': 'Ravi', 'score': '35'},
 {'name': 'Neha', 'score': '92'}
]
```

---

## Example 3 — Filtering CSV Data with List Comprehension

```python
passed_students = [
    student["name"]
    for student in students
    if int(student["score"]) >= 40
]

print(passed_students)
```

### Expected Output

```text
['Asha', 'Neha']
```

### Explanation

* CSV rows → dictionaries
* Filtering + transformation
* Very common in reporting systems

---

# 3. Fetching Numbers from `.txt` and Cleaning Data

### Real-Life Scenario

Sensor data, scraped values, machine logs.

---

## Example 4 — Cleaning Raw Numeric Data

### File: `temperatures.txt`

```text
32
-5
40
error
25
```

---

### Code

```python
with open("temperatures.txt") as file:
    raw_data = file.readlines()

# Keep only valid numeric values
temperatures = [
    int(value.strip())
    for value in raw_data
    if value.strip().lstrip("-").isdigit()
]

print(temperatures)
```

### Expected Output

```text
[32, -5, 40, 25]
```

### Explanation

* Defensive data fetching
* Invalid rows discarded
* Prevents runtime crashes

---

# 4. Fetching Data → Visualizing with `turtle`

### Real-Life Scenario

Educational visualization, simulations, simple dashboards.

---

## Example 5 — Draw Bars from File Data Using Turtle

### File: `scores.txt`

```text
80
50
90
60
```

---

### Code

```python
import turtle

# Fetch data from file
with open("scores.txt") as file:
    scores = [int(line.strip()) for line in file]

# Setup turtle
screen = turtle.Screen()
pen = turtle.Turtle()
pen.speed(0)
pen.left(90)

# Draw bar chart
for score in scores:
    pen.forward(score)
    pen.write(score)
    pen.backward(score)
    pen.right(90)
    pen.forward(30)
    pen.left(90)

screen.mainloop()
```

### Expected Output

```text
Vertical bars drawn for each score with numeric labels
```

### Explanation

* File → list
* List → visual representation
* Turtle acts as a rendering engine for fetched data

---

# 5. CSV → Turtle Visualization (Realistic Pipeline)

### Example 6 — Attendance Visualization

### File: `attendance.csv`

```text
day,present
Mon,40
Tue,35
Wed,45
```

---

### Code

```python
import csv
import turtle

days = []
counts = []

# Fetch CSV data
with open("attendance.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        days.append(row["day"])
        counts.append(int(row["present"]))

# Turtle setup
pen = turtle.Turtle()
pen.left(90)

# Draw bars
for day, count in zip(days, counts):
    pen.forward(count)
    pen.write(f"{day}:{count}")
    pen.backward(count)
    pen.right(90)
    pen.forward(40)
    pen.left(90)

turtle.done()
```

### Expected Output

```text
Attendance bars labeled by day
```

---

# 6. Writing Processed Data Back to Files

### Real-Life Scenario

Reports, exports, logs.

---

## Example 7 — Writing Filtered Results to File

```python
passed = ["Asha", "Neha"]

with open("passed.txt", "w") as file:
    for name in passed:
        file.write(name + "\n")
```

### File Output

```text
Asha
Neha
```

---

# 7. Full Mental Pipeline (Critical)

```text
External Source
   ↓
Fetch (open / read / csv)
   ↓
Clean (strip / convert)
   ↓
Transform (list comprehension)
   ↓
Use (logic / visualization / export)
```

---

# Common Beginner Mistakes (And Fixes)

| Mistake                | Why It Breaks             | Correct Approach          |
| ---------------------- | ------------------------- | ------------------------- |
| Using raw strings      | Newlines cause bugs       | `.strip()`                |
| Trusting file data     | Invalid values crash code | Validate                  |
| Hardcoding indexes     | CSV column order changes  | `DictReader`              |
| Mixing logic + drawing | Hard to debug             | Separate fetch and render |

