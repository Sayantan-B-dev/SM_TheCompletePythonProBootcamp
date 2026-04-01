# Step 5 — Defensive Element Extraction and Selector Stability Strategy

## 1. Objective of This Step

With structured data containers in place, the next layer is controlled element extraction.
This is the stage where the scraper transitions from page-level awareness to individual DOM element parsing.

This step focuses exclusively on:

* Stable CSS selector usage
* Defensive element access
* Fallback attribute retrieval
* Exception containment without silent corruption
* Clean separation between discovery and parsing

The goal is deterministic, resilient extraction.

---

## 2. Core Extraction Loop (Heavily Commented)

```python
from selenium.webdriver.common.by import By


def extract_anime_items(driver, paginated_data, visited_titles):
    """
    Extracts anime metadata from the current page.

    Responsibilities:
    - Locate anime listing blocks
    - Parse title, image, and link safely
    - Insert into structured data container
    - Avoid crashes from partial DOM inconsistencies
    """

    # Locate all anime list item containers on the page.
    anime_item_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "div.anime-block-ul > ul > li"
    )

    # Extract current page number using previously built helper
    page_number = extract_page_number(driver)

    # Ensure the page bucket exists
    page_key = initialize_page_bucket(paginated_data, page_number)

    for anime_item in anime_item_elements:

        try:
            # Locate the title anchor element inside the list item
            title_anchor = anime_item.find_element(
                By.CSS_SELECTOR,
                "h3.film-name > a"
            )

            # Extract text and clean whitespace
            anime_title = title_anchor.text.strip()

            # Extract href attribute for detail page link
            anime_link = title_anchor.get_attribute("href")

            # Locate image element
            image_element = anime_item.find_element(
                By.CSS_SELECTOR,
                "img.film-poster-img"
            )

            # Attempt to extract standard image source
            image_url = image_element.get_attribute("src")

            # Fallback to lazy-loaded attribute if src is empty
            if not image_url:
                image_url = image_element.get_attribute("data-src")

            # Insert record into structured container
            insert_anime_record(
                paginated_data,
                visited_titles,
                page_key,
                anime_title,
                image_url,
                anime_link
            )

        except Exception:
            # Skip malformed entries without stopping execution
            continue
```

---

## 3. Expected Output Behavior

No textual output is required.
Internally, each anime record is appended to:

```
paginated_data["page-X"]
```

Each record contains:

```
{
    "title": "...",
    "image": "...",
    "link": "..."
}
```

---

## 4. Selector Strategy Explained

### 4.1 Container Selector

```python
div.anime-block-ul > ul > li
```

Reasoning:

* Anchors extraction to semantic structure
* Avoids overly fragile nth-child selectors
* Minimizes dependency on styling classes

---

### 4.2 Title Selector

```python
h3.film-name > a
```

Benefits:

* Direct access to clickable anchor
* Avoids scanning unnecessary DOM depth
* Extracts both text and link from same element

---

### 4.3 Image Selector

```python
img.film-poster-img
```

Handles both:

* Standard image loading (`src`)
* Lazy loading (`data-src`)

Lazy-loading fallback is critical in modern web apps.

---

## 5. Defensive Extraction Principles

### 5.1 Isolate Each Item in try/except

If one item fails:

* Do not abort entire page
* Skip only malformed entries
* Continue iteration

This preserves page-level completeness.

---

### 5.2 Avoid Nested try/except Blocks Excessively

Keep try-block scope minimal:

```python
for anime_item in anime_item_elements:
    try:
        ...
```

Do not wrap entire function in one try-block.
Granular failure isolation improves observability.

---

### 5.3 Always Strip Text

```python
anime_title = title_anchor.text.strip()
```

Prevents:

* Hidden whitespace duplication
* False-negative deduplication mismatches

---

## 6. Alternative Extraction Strategies

### Alternative 1 — Use `.get_attribute("innerText")`

```python
anime_title = title_anchor.get_attribute("innerText")
```

Useful if:

* Text includes hidden spans
* Styling affects `.text` output

---

### Alternative 2 — Pre-Validate Element Presence

Instead of exception-based control:

```python
title_elements = anime_item.find_elements(By.CSS_SELECTOR, "h3.film-name > a")

if title_elements:
    title_anchor = title_elements[0]
```

Avoids exception cost, but slightly more verbose.

---

### Alternative 3 — Extract via JavaScript

```python
anime_data = driver.execute_script("""
    return Array.from(document.querySelectorAll("div.anime-block-ul > ul > li"))
        .map(item => ({
            title: item.querySelector("h3.film-name > a")?.innerText,
            link: item.querySelector("h3.film-name > a")?.href,
            image: item.querySelector("img.film-poster-img")?.src
        }));
""")
```

Advantages:

* Faster batch extraction
* Single DOM traversal

Tradeoff:

* Harder debugging
* Less granular control

---

## 7. Best Practices for Element Extraction

### 7.1 Minimize DOM Traversals

Use `find_element` relative to parent item:

```python
anime_item.find_element(...)
```

Not:

```python
driver.find_element(...)
```

This prevents cross-container contamination.

---

### 7.2 Avoid Hardcoded Indexes

Never use:

```python
anime_item_elements[0]
```

Assume list size may vary.

---

### 7.3 Validate Critical Fields Before Insertion

Ensure:

* Title is not empty
* Link is valid
* Image URL exists

Optional validation example:

```python
if anime_title and anime_link:
    insert_anime_record(...)
```

---

### 7.4 Log Failures in Production Systems

Instead of silent continue:

```python
except Exception as error:
    logger.warning(f"Failed to parse item: {error}")
```

Silent skipping is acceptable in controlled experimentation, not production pipelines.

---

## 8. Architectural Role of Step 5

This layer introduces:

* Selector stability discipline
* Defensive parsing architecture
* Lazy-load handling
* Item-level failure isolation

The system now includes:

1. Stealth browser configuration
2. Deterministic navigation
3. Human interaction pacing
4. Structured data containers
5. Safe element-level extraction

At this stage, the scraper can reliably parse one page.

---