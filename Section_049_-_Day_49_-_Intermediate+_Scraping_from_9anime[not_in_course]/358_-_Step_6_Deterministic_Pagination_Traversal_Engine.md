# Step 6 — Deterministic Pagination Traversal Engine

## 1. Objective of This Step

With reliable single-page extraction implemented, the next structural layer is controlled pagination traversal.

This step focuses exclusively on:

* Detecting the existence of a next page
* Extracting the correct navigation URL
* Preventing infinite loops
* Ensuring state synchronization before continuing
* Safely terminating when pagination ends

The objective is to convert page-level scraping into full dataset traversal.

---

## 2. Core Pagination Loop (Heavily Commented)

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def traverse_all_pages(driver, paginated_data, visited_titles):
    """
    Controls pagination traversal until no further pages exist.

    Responsibilities:
    - Extract current page data
    - Detect next-page availability
    - Navigate safely
    - Prevent infinite loops
    """

    wait = WebDriverWait(driver, 20)

    while True:

        # Step 1: Extract data from the current page
        extract_anime_items(driver, paginated_data, visited_titles)

        # Step 2: Handle popups before attempting navigation
        handle_popups(driver)

        try:
            # Step 3: Locate the next-page navigation button
            next_button = driver.find_element(
                By.CSS_SELECTOR,
                "div.ap__-btn-next > a:not(.disabled)"
            )

            # Extract the URL of the next page
            next_page_url = next_button.get_attribute("href")

            # Defensive check: ensure URL exists
            if not next_page_url:
                break

            # Navigate directly using URL
            driver.get(next_page_url)

            # Wait for URL change confirmation
            wait.until(EC.url_contains("page="))

            # Wait for page content to load
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.anime-block-ul > ul > li")
                )
            )

            # Simulate human delay after navigation
            human_delay()

        except Exception:
            # If next button does not exist or is disabled,
            # pagination has reached its end.
            break
```

---

## 3. Expected Behavior

The function:

* Extracts page 1
* Navigates to page 2
* Extracts page 2
* Continues until last page
* Terminates safely when no next button exists

The final `paginated_data` dictionary contains all pages grouped correctly.

---

## 4. Pagination Selector Explained

```python
div.ap__-btn-next > a:not(.disabled)
```

This selector ensures:

* The anchor tag exists
* It is not disabled
* It belongs to the "next" pagination container

Using `:not(.disabled)` prevents attempts to click inactive navigation controls.

---

## 5. Why Direct URL Navigation Is Used

Instead of:

```python
next_button.click()
```

We use:

```python
driver.get(next_page_url)
```

Advantages:

* Reduces dependency on click interaction
* Avoids interception by popups
* More deterministic navigation
* Clear URL-based state tracking

---

## 6. Infinite Loop Prevention Strategy

The loop breaks under these conditions:

1. Next button not found
2. Next button disabled
3. No `href` attribute
4. URL fails to update

This ensures no uncontrolled iteration occurs.

---

## 7. Alternative Pagination Strategies

### Alternative 1 — Click-Based Navigation

```python
next_button.click()
```

Pros:

* Simulates real user interaction

Cons:

* More vulnerable to overlay interruption
* More sensitive to timing issues

---

### Alternative 2 — Pre-Calculate Total Pages

If total page count is available in DOM:

```python
total_pages = int(driver.find_element(...).text)

for page_index in range(1, total_pages + 1):
    driver.get(f"https://site/az-list?page={page_index}")
```

Advantages:

* Eliminates next-button detection
* Faster traversal

Tradeoff:

* Requires reliable total-page element

---

### Alternative 3 — Crawl Until Duplicate Page Detected

Track page content hash:

```python
previous_titles = set()
current_titles = set()

if current_titles == previous_titles:
    break
```

Useful if pagination button is unreliable.

---

## 8. Best Practices for Pagination Traversal

### 8.1 Always Extract Before Navigating

Do not navigate before extracting current page.
Otherwise first page may be skipped.

---

### 8.2 Validate URL Change

Always confirm navigation:

```python
wait.until(EC.url_contains("page="))
```

Prevents race conditions.

---

### 8.3 Use Clear Loop Exit Conditions

Avoid ambiguous logic like:

```python
while next_button:
```

Explicit break conditions are safer.

---

### 8.4 Keep Traversal Stateless Beyond Data Containers

Pagination loop should not mutate unrelated state variables.
Contain logic within controlled scope.

---

## 9. Performance Considerations

Pagination traversal time grows linearly with number of pages.

Performance factors:

* Network latency
* DOM rendering time
* Human delay settings
* Popup frequency

Optimizing delay windows can significantly reduce runtime without increasing detection risk.

---

## 10. Architectural Role of Step 6

This layer transforms:

Single-page scraper → Multi-page dataset crawler

The system now includes:

1. Stealth browser configuration
2. Deterministic navigation
3. Behavioral simulation
4. Structured data architecture
5. Defensive extraction
6. Controlled pagination traversal

The scraper now covers the entire dataset surface.

---
