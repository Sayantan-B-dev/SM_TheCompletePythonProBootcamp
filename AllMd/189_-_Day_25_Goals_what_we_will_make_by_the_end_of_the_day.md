## Python File Types — Complete Practical Coverage

### 1. Plain Text Files (`.txt`)

Used for logs, notes, configs, simple data storage.

**Common Operations**

* Read entire file
* Read line by line
* Write / append text

```python
# Writing text to a file
with open("notes.txt", "w") as file:
    file.write("Python works with text files\n")
    file.write("Each line is a string\n")

# Reading text from a file
with open("notes.txt", "r") as file:
    content = file.read()
    print(content)
```

**Expected Output**

```
Python works with text files
Each line is a string
```

**Edge Cases**

* File not found → `FileNotFoundError`
* Encoding issues → specify `encoding="utf-8"`

---

### 2. CSV Files (`.csv`)

Used for tabular data (spreadsheets, datasets).

**Key Library**

* `csv`

```python
import csv

# Writing CSV
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", 24])
    writer.writerow(["Bob", 30])

# Reading CSV
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

**Expected Output**

```
['Name', 'Age']
['Alice', 24]
['Bob', 30]
```

**Edge Cases**

* Comma inside text → use quoting
* Newline issues on Windows → `newline=""`

---

### 3. JSON Files (`.json`)

Used for structured data exchange (APIs, configs).

**Key Library**

* `json`

```python
import json

data = {
    "user": "Sayantan",
    "skills": ["Python", "SQL"],
    "active": True
}

# Write JSON
with open("profile.json", "w") as file:
    json.dump(data, file, indent=4)

# Read JSON
with open("profile.json", "r") as file:
    loaded = json.load(file)
    print(loaded)
```

**Expected Output**

```
{'user': 'Sayantan', 'skills': ['Python', 'SQL'], 'active': True}
```

**Edge Cases**

* Only supports basic types
* Dates must be serialized manually

---

### 4. Binary Files (`.bin`, `.dat`)

Used for raw bytes (images, compiled data).

```python
# Writing binary data
with open("raw.bin", "wb") as file:
    file.write(b"\x00\xFF\x10")

# Reading binary data
with open("raw.bin", "rb") as file:
    data = file.read()
    print(data)
```

**Expected Output**

```
b'\x00\xff\x10'
```

**Edge Cases**

* Must use binary mode (`rb`, `wb`)
* No automatic decoding

---

### 5. Image Files (`.jpg`, `.png`)

Used for image processing.

**Key Library**

* `Pillow`

```python
from PIL import Image

image = Image.open("photo.png")
print(image.size)
print(image.format)
```

**Expected Output**

```
(1920, 1080)
PNG
```

**Edge Cases**

* Corrupted image → `OSError`
* Format-dependent metadata

---

### 6. Excel Files (`.xlsx`)

Used for spreadsheets.

**Key Library**

* `openpyxl`

```python
from openpyxl import Workbook, load_workbook

# Create Excel file
wb = Workbook()
sheet = wb.active
sheet["A1"] = "Name"
sheet["B1"] = "Score"
sheet.append(["Alice", 90])
wb.save("scores.xlsx")

# Read Excel file
wb = load_workbook("scores.xlsx")
sheet = wb.active
print(sheet["A2"].value, sheet["B2"].value)
```

**Expected Output**

```
Alice 90
```

**Edge Cases**

* Formula cells need evaluation
* Large files consume memory

---

### 7. PDF Files (`.pdf`)

Used for documents and reports.

**Key Library**

* `PyPDF2`

```python
from PyPDF2 import PdfReader

reader = PdfReader("file.pdf")
print(len(reader.pages))
```

**Expected Output**

```
5
```

**Edge Cases**

* Scanned PDFs are images (no text)
* Encrypted PDFs need password

---

### 8. ZIP Files (`.zip`)

Used for compression and archives.

```python
import zipfile

# Create ZIP
with zipfile.ZipFile("files.zip", "w") as zipf:
    zipf.write("notes.txt")

# Extract ZIP
with zipfile.ZipFile("files.zip", "r") as zipf:
    zipf.extractall("extracted")
```

**Expected Output**

```
(no terminal output; files extracted)
```

---

### 9. Pickle Files (`.pkl`)

Used for Python object serialization.

**Key Library**

* `pickle`

```python
import pickle

data = {"a": 1, "b": 2}

# Save object
with open("data.pkl", "wb") as file:
    pickle.dump(data, file)

# Load object
with open("data.pkl", "rb") as file:
    loaded = pickle.load(file)
    print(loaded)
```

**Expected Output**

```
{'a': 1, 'b': 2}
```

**Edge Cases**

* Not secure for untrusted files
* Python-version dependent

---

### 10. SQLite Database Files (`.db`)

Used for embedded databases.

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT)")
cursor.execute("INSERT INTO users VALUES ('Alice')")

conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()
```

**Expected Output**

```
[('Alice',)]
```

---

### 11. XML Files (`.xml`)

Used for hierarchical structured data.

```python
import xml.etree.ElementTree as ET

tree = ET.parse("data.xml")
root = tree.getroot()

for child in root:
    print(child.tag, child.text)
```

**Expected Output**

```
name Alice
age 24
```

---

### 12. YAML Files (`.yaml`, `.yml`)

Used for configuration files.

**Key Library**

* `pyyaml`

```python
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    print(config)
```

**Expected Output**

```
{'debug': True, 'port': 8000}
```

---

## Summary Table

| File Type | Extension | Primary Use        |
| --------- | --------- | ------------------ |
| Text      | `.txt`    | Logs, notes        |
| CSV       | `.csv`    | Tables             |
| JSON      | `.json`   | APIs, configs      |
| Binary    | `.bin`    | Raw bytes          |
| Image     | `.png`    | Media              |
| Excel     | `.xlsx`   | Spreadsheets       |
| PDF       | `.pdf`    | Documents          |
| ZIP       | `.zip`    | Compression        |
| Pickle    | `.pkl`    | Python objects     |
| Database  | `.db`     | Persistent storage |
| XML       | `.xml`    | Structured markup  |
| YAML      | `.yaml`   | Configuration      |
