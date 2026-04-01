# Step 4 — Structured Data Architecture and Stateful Deduplication Engine

## 1. Objective of This Step

With browser initialization, navigation control, and behavioral simulation in place, the next structural layer is data architecture.
Scraping without structured state management leads to duplication, memory bloat, and inconsistent datasets.

This step focuses exclusively on:

* Designing the data container model
* Implementing page-level grouping
* Preventing duplicate entries
* Managing runtime state during pagination

This layer transforms raw extraction into deterministic structured data.

---

## 2. Core Data Structures

Two central structures define this layer:

```python
paginated_data = {}
visited_titles = set()
```

### 2.1 `paginated_data` — Hierarchical Container

```python
paginated_data = {}
```

Purpose:

* Groups anime entries by page
* Preserves pagination metadata
* Enables downstream analysis per page

Structure:

```python
{
    "page-1": [...],
    "page-2": [...],
}
```

---

### 2.2 `visited_titles` — Deduplication Guard

```python
visited_titles = set()
```

Purpose:

* Prevent duplicate anime entries
* Maintain dataset integrity
* Protect against pagination overlap or re-render duplication

Sets provide:

* O(1) average lookup time
* Guaranteed uniqueness

---

## 3. Structured Pagination Tracking Logic

### 3.1 Extract Current Page Number

```python
from urllib.parse import urlparse, parse_qs


def extract_page_number(driver):
    """
    Extracts the current page number from the URL query string.
    Defaults to page 1 if no 'page' parameter exists.
    """

    current_url = driver.current_url

    # Parse the URL into components
    parsed_url = urlparse(current_url)

    # Extract query parameters into dictionary form
    query_parameters = parse_qs(parsed_url.query)

    # Attempt to retrieve page number, defaulting to '1'
    page_number = query_parameters.get("page", ["1"])[0]

    return page_number
```

Why this matters:

* URL-based state tracking is more reliable than DOM inference.
* Pagination buttons may be dynamically disabled.
* URL always reflects authoritative page state.

---

## 4. Core Data Insertion Engine (Heavily Commented)

```python
def initialize_page_bucket(paginated_data: dict, page_number: str):
    """
    Ensures a page bucket exists inside the master container.
    Prevents KeyError during data insertion.
    """

    page_key = f"page-{page_number}"

    # Create page bucket only if not already initialized.
    if page_key not in paginated_data:
        paginated_data[page_key] = []

    return page_key



def insert_anime_record(
    paginated_data: dict,
    visited_titles: set,
    page_key: str,
    title: str,
    image_url: str,
    anime_link: str
):
    """
    Inserts an anime record into the correct page bucket,
    while preventing duplicate entries across pages.
    """

    # Deduplication check.
    # If title already processed, skip insertion.
    if title in visited_titles:
        return False

    # Add title to visited registry.
    visited_titles.add(title)

    # Construct structured record.
    anime_record = {
        "title": title,
        "image": image_url,
        "link": anime_link
    }

    # Append record to appropriate page bucket.
    paginated_data[page_key].append(anime_record)

    return True
```

---

## 5. Expected Data Structure Output

After scraping two pages, JSON-like structure:

```json
{
    "page-1": [
        {
            "title": "Naruto",
            "image": "https://image1.jpg",
            "link": "https://9animetv.to/watch/naruto"
        }
    ],
    "page-2": [
        {
            "title": "Bleach",
            "image": "https://image2.jpg",
            "link": "https://9animetv.to/watch/bleach"
        }
    ]
}
```

Characteristics:

* Page-indexed grouping
* No duplicate titles
* Structured key-value schema

---

## 6. Alternative Data Architecture Designs

### Alternative 1 — Flat Dataset

```python
flat_data = []
```

Structure:

```json
[
    { "title": "...", "image": "...", "link": "..." }
]
```

Advantages:

* Simpler structure
* Easier database insertion

Tradeoff:

* Loses pagination context

---

### Alternative 2 — Indexed by Title

```python
anime_data = {
    "Naruto": {
        "image": "...",
        "link": "..."
    }
}
```

Advantages:

* Fast lookup by title
* No need for visited set

Tradeoff:

* Does not preserve page order
* Cannot store duplicate titles if variants exist

---

### Alternative 3 — Add Metadata Layer

Extended design:

```python
paginated_data = {
    "metadata": {
        "total_pages": 24,
        "scraped_at": "timestamp"
    },
    "pages": {
        "page-1": [...],
        "page-2": [...]
    }
}
```

Best for:

* Production systems
* Version tracking
* Dataset auditing

---

## 7. Best Practices for Data Architecture

### 7.1 Separate State and Storage

Do not mix navigation logic with storage logic.
Keep data insertion isolated in dedicated functions.

---

### 7.2 Deduplicate Using Stable Keys

Title-based deduplication works only if titles are unique.
For higher reliability:

```python
unique_key = anime_link
```

Links are more stable than titles.

---

### 7.3 Avoid Implicit Page Detection

Never infer page index from button position.
Always use URL query parameters as authoritative source.

---

### 7.4 Keep Data Immutable After Insertion

Do not modify records after insertion.
If transformation is needed, apply it before storing.

---

## 8. Architectural Role of Step 4

This layer introduces:

* Deterministic dataset structure
* State-aware pagination grouping
* O(1) duplicate protection
* Separation of extraction and storage logic

At this stage, the scraper now has:

1. Stealth browser initialization
2. Deterministic navigation control
3. Human interaction simulation
4. Structured data architecture

The system is now prepared for controlled element-level extraction from each page.

---
