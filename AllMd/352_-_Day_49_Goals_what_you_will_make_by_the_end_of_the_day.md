# Selenium Automation Documentation

**Project:** Automated Anime Metadata Scraper
**Target Website:** 9animetv.to
**Language:** Python
**Libraries:** Selenium, WebDriver Manager, JSON

---

## 1. System Overview

This script automates a Chromium browser instance using Selenium WebDriver to extract paginated anime metadata from the A–Z listing page of **[https://9animetv.to](https://9animetv.to)**.

The program performs the following core operations:

1. Configures a stealth browser session.
2. Navigates to the A–Z anime listing page.
3. Iteratively traverses paginated result pages.
4. Extracts structured metadata:

   * Anime title
   * Poster image URL
   * Anime detail page URL
5. Stores the dataset into a structured JSON file grouped by page.

The output file generated is:

```
anime_data_paginated.json
```

---

## 2. Architectural Flow

### 2.1 Execution Entry Point

```python
if __name__ == "__main__":
    main()
```

The script executes through the `main()` function, which orchestrates driver configuration and data extraction.

---

## 3. Browser Configuration

### 3.1 Chrome Options

The browser is configured to reduce automation detection signals:

| Configuration                                   | Purpose                      |
| ----------------------------------------------- | ---------------------------- |
| `--disable-blink-features=AutomationControlled` | Hides automation fingerprint |
| Remove `enable-automation` switch               | Prevents Selenium banner     |
| Override `navigator.webdriver`                  | Avoid detection by JS        |
| Custom User-Agent                               | Mimics real browser          |
| `--start-maximized`                             | Full viewport rendering      |

This approach improves resilience against bot detection mechanisms.

---

## 4. Functional Components

### 4.1 Human Delay Simulation

```python
def human_delay():
    time.sleep(random.uniform(1.8, 3.5))
```

Introduces randomized delay to simulate natural browsing behavior.

---

### 4.2 Popup Handler

```python
def handle_popups():
```

Responsibilities:

• Close unexpected new browser tabs
• Click modal close buttons
• Prevent scraping interruption

It handles both:

* Multi-window popups
* Modal overlays

---

## 5. Navigation Logic

### 5.1 Initial Page Access

```python
driver.get(BASE_URL)
```

Then navigates to:

```
/az-list
```

via:

```python
a[href="/az-list"]
```

---

## 6. Core Extraction Engine

### 6.1 Method: `get_images()`

This method performs paginated scraping.

---

### 6.2 Data Structures

```python
paginated_data = {}
visited_titles = set()
```

| Structure        | Purpose                               |
| ---------------- | ------------------------------------- |
| `paginated_data` | Stores grouped anime results per page |
| `visited_titles` | Prevents duplicate entries            |

---

### 6.3 Extracted Elements

Each anime entry contains:

| Field | CSS Selector           | Description     |
| ----- | ---------------------- | --------------- |
| Title | `h3.film-name > a`     | Anime name      |
| Image | `img.film-poster-img`  | Poster URL      |
| Link  | `href` of title anchor | Detail page URL |

---

### 6.4 Pagination Logic

The scraper identifies the "Next" button:

```python
div.ap__-btn-next > a:not(.disabled)
```

If present:

1. Extracts `href`
2. Navigates to next page
3. Repeats extraction

If not present:
• Pagination loop terminates.

---

## 7. JSON Output Format

### 7.1 Structure

```json
{
    "page-1": [
        {
            "title": "Naruto",
            "image": "https://image_url.jpg",
            "link": "https://9animetv.to/watch/naruto-xyz"
        },
        ...
    ],
    "page-2": [
        ...
    ]
}
```

### 7.2 Design Characteristics

• Grouped by page number
• No duplicate titles
• UTF-8 encoded
• Indented for readability

---

# 8. Using the Output JSON

The generated JSON file can serve multiple downstream purposes.

---

## 8.1 Web Application Integration

The dataset can power:

• Anime gallery websites
• Card-based UI layouts
• Search and filter systems
• Static site generators

Example JavaScript usage:

```javascript
fetch("anime_data_paginated.json")
  .then(response => response.json())
  .then(data => {
      Object.keys(data).forEach(page => {
          data[page].forEach(anime => {
              console.log(anime.title);
          });
      });
  });
```

---

## 8.2 Backend API Consumption

The JSON file can be:

• Loaded into a Flask / FastAPI server
• Stored in MongoDB
• Indexed in Elasticsearch
• Converted to SQL database rows

Example Python usage:

```python
import json

with open("anime_data_paginated.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

for page, animes in dataset.items():
    for anime in animes:
        print(anime["title"])
```

---

## 8.3 Data Engineering Use Cases

| Use Case              | Description                              |
| --------------------- | ---------------------------------------- |
| Dataset creation      | Build ML training corpus                 |
| Recommendation engine | Use titles for similarity mapping        |
| Metadata indexing     | Create searchable archive                |
| Image dataset         | Poster-based computer vision experiments |

---

## 8.4 Converting to Flat List

If page grouping is unnecessary:

```python
flat_list = [
    anime
    for page in dataset.values()
    for anime in page
]
```

This simplifies usage for APIs or database insertion.

---

## 9. Limitations and Considerations

1. Heavy reliance on CSS selectors
2. Site structure changes may break scraper
3. Anti-bot systems may still detect automation
4. No exception logging implemented
5. No rate limiting beyond sleep delays

---

## 10. Suggested Improvements

| Improvement                            | Benefit                     |
| -------------------------------------- | --------------------------- |
| Add logging                            | Debug visibility            |
| Use headless mode with stealth plugins | Better automation stability |
| Implement retry mechanism              | Improved robustness         |
| Store timestamps                       | Data versioning             |
| Add async scraping                     | Performance optimization    |

---

## 11. Execution Summary

When executed:

1. Browser launches
2. Navigates to A–Z page
3. Iterates through all pages
4. Extracts anime metadata
5. Writes structured JSON
6. Closes browser

---

This script provides a clean, structured dataset extraction pipeline suitable for frontend display systems, backend services, and research workflows.
