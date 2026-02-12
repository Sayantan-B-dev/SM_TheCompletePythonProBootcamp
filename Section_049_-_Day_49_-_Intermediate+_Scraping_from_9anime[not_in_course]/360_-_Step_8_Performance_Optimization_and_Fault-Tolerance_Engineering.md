# Step 8 — Performance Optimization and Fault-Tolerance Engineering

## 1. Objective of This Step

After implementing durable storage, the next structural layer strengthens runtime robustness and scalability.

This step focuses exclusively on:

* Timeout tuning and adaptive waiting
* Retry mechanisms for transient failures
* Controlled resource cleanup
* Performance optimization without breaking stealth
* Failure recovery architecture

The objective is to transform a working scraper into a resilient scraping system.

---

## 2. Timeout Strategy Optimization

The default:

```python
wait = WebDriverWait(driver, 20)
```

A fixed timeout is safe but inefficient. Instead, implement adaptive timeout control.

### Adaptive Wait Wrapper

```python
from selenium.common.exceptions import TimeoutException


def wait_for_elements(driver, css_selector: str, timeout_seconds: int = 20):
    """
    Waits for elements using explicit wait.
    Allows timeout customization per call.
    """

    wait = WebDriverWait(driver, timeout_seconds)

    try:
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return elements

    except TimeoutException:
        print(f"Timeout while waiting for selector: {css_selector}")
        return []
```

### Why This Matters

Different pages load at different speeds.
Heavy pages may require longer waits.
Light pages should not be penalized with excessive delay.

---

## 3. Retry Logic for Transient Failures

Network instability or rendering race conditions may cause sporadic failures.

### Retry Decorator Implementation

```python
import time


def retry_operation(operation_function, max_retries: int = 3, delay_seconds: int = 2):
    """
    Executes a function with retry logic.
    Useful for unstable operations like navigation or extraction.
    """

    for attempt_number in range(1, max_retries + 1):
        try:
            return operation_function()

        except Exception as error:
            print(f"Attempt {attempt_number} failed: {error}")

            if attempt_number == max_retries:
                raise

            time.sleep(delay_seconds)
```

### Usage Example

```python
retry_operation(lambda: driver.get(next_page_url))
```

This ensures temporary network failures do not collapse the entire session.

---

## 4. Memory and Resource Management

Selenium sessions consume:

* RAM
* CPU
* File descriptors

Always enforce deterministic cleanup.

### Structured Driver Lifecycle

```python
def run_scraper():
    driver = None

    try:
        driver = initialize_browser()
        navigate_to_az_list(driver, BASE_URL)
        traverse_all_pages(driver, paginated_data, visited_titles)

    finally:
        if driver:
            driver.quit()
            print("Driver closed safely.")
```

This guarantees cleanup even if unexpected exceptions occur.

---

## 5. Performance Optimization Techniques

### 5.1 Disable Image Loading (Optional)

Reduces bandwidth and improves load speed.

```python
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
```

Tradeoff:
Images required for scraping must not depend on actual image rendering.

---

### 5.2 Use Page Load Strategy

```python
chrome_options.page_load_strategy = "eager"
```

Options:

| Strategy | Behavior                  |
| -------- | ------------------------- |
| normal   | Wait for full load        |
| eager    | Wait for DOMContentLoaded |
| none     | Do not wait               |

`eager` improves speed while maintaining DOM stability.

---

### 5.3 Reduce Human Delay in Production

For testing:

```python
human_delay(1.8, 3.5)
```

For production:

```python
human_delay(0.8, 1.5)
```

Maintain variability but reduce total runtime.

---

## 6. Defensive State Recovery

If pagination breaks unexpectedly:

```python
current_page = extract_page_number(driver)
print(f"Failure occurred on page {current_page}")
```

Log current state before termination.

Production systems should store:

* Last successful page
* Timestamp
* Error type

This enables resumable scraping.

---

## 7. Logging Strategy

Replace print statements with structured logging.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Page loaded successfully.")
logging.warning("Retrying operation.")
logging.error("Fatal extraction failure.")
```

Benefits:

* Timestamped traceability
* Production debugging
* Clear severity levels

---

## 8. Scaling Considerations

### Vertical Scaling

* Increase system RAM
* Use faster CPU
* Reduce wait time

### Horizontal Scaling

* Split alphabet ranges
* Run multiple instances in parallel
* Use Selenium Grid

Example distributed URL pattern:

```
/az-list?char=A
/az-list?char=B
```

---

## 9. Handling Website Structural Changes

Implement structural validation:

```python
def verify_dom_structure(driver):
    required_selector = "div.anime-block-ul > ul > li"

    if not driver.find_elements(By.CSS_SELECTOR, required_selector):
        raise RuntimeError("DOM structure changed. Scraper requires update.")
```

Fail early rather than producing corrupted dataset.

---

## 10. Headless Production Mode (Optional)

For deployment:

```python
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
```

Best for:

* CI pipelines
* Cloud servers
* Containerized environments

---

## 11. Performance Risk Tradeoffs

| Optimization       | Risk                      |
| ------------------ | ------------------------- |
| Lower delay        | Increased detection       |
| Headless mode      | Higher fingerprint risk   |
| Disable images     | May break dynamic loading |
| Aggressive retries | Potential infinite loop   |

Balance speed with stability.

---

## 12. Architectural Role of Step 8

This layer introduces:

* Runtime fault tolerance
* Retry resilience
* Performance tuning discipline
* Deterministic cleanup
* Production-grade logging

The system now includes:

1. Stealth initialization
2. Deterministic navigation
3. Behavioral entropy
4. Structured data containers
5. Defensive extraction
6. Pagination traversal
7. Persistent serialization
8. Performance and resilience engineering

The scraper is now production-hardened.

---