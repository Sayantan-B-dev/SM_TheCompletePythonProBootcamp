# Step 7 — Persistent Data Serialization and Atomic JSON Storage Strategy

## 1. Objective of This Step

After completing multi-page traversal and building an in-memory structured dataset, the next layer is persistent storage.
Without controlled serialization, the dataset remains volatile and vulnerable to loss or corruption.

This step focuses exclusively on:

* Writing structured JSON safely
* UTF-8 encoding correctness
* Atomic file writing strategy
* Data validation before persistence
* Preventing partial writes

The goal is durable, deterministic storage.

---

## 2. Basic JSON Serialization (Heavily Commented)

```python
import json
import os


def save_to_json_file(paginated_data: dict, output_filename: str = "anime_data_paginated.json"):
    """
    Serializes the in-memory paginated dataset into a formatted JSON file.

    Responsibilities:
    - Ensure correct UTF-8 encoding
    - Use indentation for readability
    - Prevent ASCII escaping issues
    """

    # Defensive validation before writing
    if not isinstance(paginated_data, dict):
        raise TypeError("Expected paginated_data to be a dictionary.")

    # Open file in write mode with UTF-8 encoding.
    # ensure_ascii=False preserves non-English characters.
    with open(output_filename, "w", encoding="utf-8") as output_file:

        json.dump(
            paginated_data,
            output_file,
            indent=4,          # Improves human readability
            ensure_ascii=False # Prevents Unicode escaping
        )

    print(f"Dataset successfully saved to {output_filename}")
```

---

## 3. Expected Output

Console:

```
Dataset successfully saved to anime_data_paginated.json
```

File created:

```
anime_data_paginated.json
```

Readable, structured, properly encoded.

---

## 4. Why `ensure_ascii=False` Is Important

Without:

```python
ensure_ascii=False
```

Unicode characters become escaped:

```
"Pok\u00e9mon"
```

With proper encoding:

```
"Pokémon"
```

This preserves dataset integrity and frontend compatibility.

---

## 5. Atomic Write Strategy (Production-Grade)

Basic writing risks corruption if:

* Script crashes mid-write
* System loses power
* Disk write is interrupted

Safer approach:

```python
def save_json_atomically(paginated_data: dict, output_filename: str):
    """
    Writes JSON using atomic replacement strategy.
    Prevents partial or corrupted file states.
    """

    temporary_filename = output_filename + ".tmp"

    # Write to temporary file first
    with open(temporary_filename, "w", encoding="utf-8") as temp_file:
        json.dump(
            paginated_data,
            temp_file,
            indent=4,
            ensure_ascii=False
        )

    # Replace original file atomically
    os.replace(temporary_filename, output_filename)

    print(f"Atomically saved dataset to {output_filename}")
```

Why this matters:
If crash occurs before `os.replace()`, original file remains intact.

---

## 6. Data Validation Before Writing

Before serialization, validate structure:

```python
def validate_dataset_structure(paginated_data: dict):
    """
    Ensures dataset matches expected schema before writing.
    """

    for page_key, records in paginated_data.items():

        if not page_key.startswith("page-"):
            raise ValueError(f"Invalid page key format: {page_key}")

        if not isinstance(records, list):
            raise TypeError("Page value must be a list.")

        for record in records:

            if not all(key in record for key in ["title", "image", "link"]):
                raise ValueError("Record missing required fields.")
```

Use before writing:

```python
validate_dataset_structure(paginated_data)
save_json_atomically(paginated_data, "anime_data_paginated.json")
```

---

## 7. Alternative Serialization Formats

### Alternative 1 — Flatten Before Writing

If page grouping not required:

```python
flat_data = [
    anime
    for page_records in paginated_data.values()
    for anime in page_records
]

with open("anime_data_flat.json", "w", encoding="utf-8") as f:
    json.dump(flat_data, f, indent=4, ensure_ascii=False)
```

Better for:

* Database ingestion
* API consumption

---

### Alternative 2 — Write Line-Delimited JSON (NDJSON)

Better for large datasets:

```python
with open("anime_data.ndjson", "w", encoding="utf-8") as f:
    for page_records in paginated_data.values():
        for anime in page_records:
            f.write(json.dumps(anime, ensure_ascii=False) + "\n")
```

Advantages:

* Stream processing friendly
* Easier incremental reading

---

### Alternative 3 — Export to CSV

```python
import csv

def save_to_csv(paginated_data):
    with open("anime_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "image", "link"])
        writer.writeheader()

        for page_records in paginated_data.values():
            for anime in page_records:
                writer.writerow(anime)
```

Best for:

* Spreadsheet analysis
* Non-technical stakeholders

---

## 8. Performance Considerations

Memory usage scales with dataset size.

If pages are very large:

* Write incrementally per page
* Avoid storing entire dataset in memory

Streaming example:

```python
def append_page_to_json_file(page_records, file_object):
    for record in page_records:
        file_object.write(json.dumps(record, ensure_ascii=False) + "\n")
```

---

## 9. Best Practices for Persistent Storage

### 9.1 Never Write Inside Pagination Loop

Avoid:

```python
for each page:
    save_to_json()
```

This causes unnecessary disk I/O overhead.

---

### 9.2 Validate Before Persisting

Corrupt in-memory structure propagates into corrupt file.
Validate early.

---

### 9.3 Use Explicit Encoding Always

Never rely on system default encoding.

---

### 9.4 Keep Storage Layer Separate

Do not mix scraping logic and writing logic in same function.
Maintain clean architectural boundaries.

---

## 10. Architectural Role of Step 7

This layer introduces:

* Durable persistence
* Data integrity validation
* Atomic write safety
* Format flexibility

The system now includes:

1. Stealth initialization
2. Deterministic navigation
3. Human behavior simulation
4. Structured state container
5. Defensive extraction
6. Controlled pagination traversal
7. Reliable persistent storage

The dataset is now complete and safely written.

---
