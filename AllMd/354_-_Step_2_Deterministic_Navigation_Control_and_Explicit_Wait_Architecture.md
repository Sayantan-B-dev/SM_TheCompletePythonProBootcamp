# Step 2 — Deterministic Navigation Control and Explicit Wait Architecture

## 1. Objective of This Step

After stable browser initialization, the next structural layer is deterministic navigation.
Automation fails most often not because of selectors, but because the DOM is not ready when elements are accessed.

This step focuses exclusively on:

* Controlled navigation flow
* Explicit wait mechanisms
* URL synchronization
* Reliable DOM readiness detection

This ensures the scraper interacts only when the page state is stable and predictable.

---

## 2. Core Navigation and Wait Architecture

```python
# Import required Selenium modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navigate_to_az_list(driver, base_url: str):
    """
    Navigates to the base URL and then to the A–Z listing page.
    Uses explicit waits to guarantee DOM readiness.
    """

    # Create an explicit wait instance with a timeout of 20 seconds.
    # This prevents premature element access.
    wait = WebDriverWait(driver, 20)

    # Step 1: Navigate to the homepage.
    driver.get(base_url)

    # Wait until the page body is fully present.
    # This ensures the initial DOM has been constructed.
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    print("Homepage loaded successfully.")

    # Step 2: Wait for the A–Z list navigation link to be clickable.
    # element_to_be_clickable ensures:
    # 1. Element exists in DOM
    # 2. Element is visible
    # 3. Element is enabled
    az_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/az-list"]'))
    )

    # Click the A–Z link safely after readiness confirmation.
    az_link.click()

    # Step 3: Confirm navigation by waiting for URL change.
    # This ensures we are actually on the expected route.
    wait.until(
        EC.url_contains("/az-list")
    )

    # Step 4: Wait for anime listing container to load.
    # This ensures the dynamic content has been rendered.
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.anime-block-ul > ul > li")
        )
    )

    print("A–Z listing page loaded successfully.")
```

---

## 3. Expected Output

```
Homepage loaded successfully.
A–Z listing page loaded successfully.
```

Additionally, the browser navigates reliably to:

```
https://9animetv.to/az-list
```

with anime list elements present in the DOM.

---

## 4. Why Explicit Waits Are Critical

### 4.1 The Problem with `time.sleep()`

Using:

```python
time.sleep(3)
```

creates nondeterministic behavior:

* Too short → NoSuchElementException
* Too long → Performance degradation
* Network speed dependent

Explicit waits solve this by waiting conditionally instead of blindly.

---

## 5. Types of Explicit Wait Conditions Used

### 5.1 `presence_of_element_located`

Waits until the element exists in the DOM.
Does not guarantee visibility.

Used for:

```python
EC.presence_of_element_located((By.TAG_NAME, "body"))
```

---

### 5.2 `element_to_be_clickable`

Ensures:

* Element exists
* Element is visible
* Element is enabled

Used for interactive elements like navigation links.

---

### 5.3 `url_contains`

Ensures navigation completion before proceeding.
Prevents race conditions between click and DOM load.

---

### 5.4 `presence_of_all_elements_located`

Ensures a list of elements exists before scraping begins.

Used for:

```python
div.anime-block-ul > ul > li
```

---

## 6. Alternative Navigation Strategies

### Alternative 1 — Direct URL Navigation

Instead of clicking:

```python
driver.get("https://9animetv.to/az-list")
```

Advantages:

* Faster execution
* Fewer interaction points

Tradeoff:

* May bypass cookie initialization
* Some sites require landing page session setup

---

### Alternative 2 — Wait for JavaScript Readiness

```python
wait.until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)
```

Ensures full page load including subresources.

Use when:

* Heavy JavaScript rendering
* SPA (Single Page Applications)

---

### Alternative 3 — Wait for Specific Network-Triggered Content

If content loads via AJAX, wait for a unique selector tied to dynamic data rather than general container.

Example:

```python
wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, "film-name"))
)
```

---

## 7. Best Practices for Navigation Control

### 7.1 Never Mix Implicit and Explicit Waits

Avoid:

```python
driver.implicitly_wait(10)
```

Mixing implicit and explicit waits creates unpredictable timeout stacking.

---

### 7.2 Always Validate URL State After Click

Click does not guarantee navigation.
Always confirm using:

```python
EC.url_contains()
```

---

### 7.3 Use Stable Selectors

Avoid fragile selectors like:

```python
div:nth-child(4) > a
```

Prefer semantic attributes:

```python
a[href="/az-list"]
```

---

### 7.4 Fail Fast When Page Structure Changes

If:

```python
presence_of_all_elements_located
```

times out, it likely indicates:

* DOM structure change
* Anti-bot redirection
* Site update

Treat this as a structural failure, not as a random error.

---

## 8. Architectural Role of Step 2

This layer guarantees:

* Correct page state before scraping
* DOM stability
* Reduced race conditions
* Deterministic navigation

At this point:

• Browser is stealth-configured
• Navigation is deterministic
• Page readiness is validated

The system is now safe to begin controlled human-like interaction logic.

---