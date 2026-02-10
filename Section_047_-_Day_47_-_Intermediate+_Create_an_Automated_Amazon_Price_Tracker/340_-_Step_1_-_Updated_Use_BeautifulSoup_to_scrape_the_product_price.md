## Step 1 — **Input Acquisition, Request Strategy, and HTML Caching Layer**

### 1.1 Purpose of This Step in the Overall System

This step is responsible for **obtaining raw HTML content** from Amazon search results while minimizing unnecessary network requests and avoiding repeated scraping operations. The logic ensures that the project behaves deterministically during development and debugging, which is essential for beginners who need reproducible results. Instead of fetching live data every time, the system first checks for an existing cached HTML file and only performs a network request if the cache does not exist.

---

### 1.2 File Responsible for This Step

> **`main.py`**
> This file acts as the **orchestrator** of the entire project lifecycle, and Step 1 begins here.

---

### 1.3 Configuration and Constants Definition

```python
PRODUCT_URL = "https://www.amazon.in/s?k=ram+8gb+ddr4"
CACHE_FILE = "data/input/productpage.html"
CSV_FILE = "data/output/products.csv"
HTML_FILE = "data/output/products.html"
```

**Explanation of each variable and its role**

* `PRODUCT_URL` defines the Amazon search endpoint that returns HTML containing product listings.
* `CACHE_FILE` defines the local storage path where fetched HTML is persisted for reuse.
* `CSV_FILE` defines the structured data output destination after parsing.
* `HTML_FILE` defines the final visual dashboard output destination.

These constants centralize configuration, allowing future changes without modifying logic scattered across multiple files.

---

### 1.4 HTTP Request Identity and Anti-Blocking Strategy

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}
```

**Why headers are mandatory for real-world scraping**

* Amazon blocks requests that do not resemble a real browser.
* `User-Agent` simulates a legitimate Chrome browser running on Windows.
* `Accept-Language` ensures content is returned in English with Indian localization.
* Without these headers, the request may return CAPTCHA pages or HTTP 503 errors.

---

### 1.5 Cache-First Decision Flow

```python
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        html = f.read()
```

**Behavioral explanation**

* The program first checks whether the cached HTML already exists.
* If present, the system **skips the network entirely**, improving speed and stability.
* This enables offline debugging and prevents repeated hits to Amazon servers.
* This approach protects against IP throttling and accidental rate-limit violations.

---

### 1.6 Live Fetch Fallback Mechanism

```python
else:
    r = requests.get(PRODUCT_URL, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(r.status_code)
    html = r.text
```

**Why this fallback is critical**

* If no cache exists, a live HTTP request is executed.
* A timeout of fifteen seconds prevents the program from hanging indefinitely.
* Explicit status code validation ensures only valid HTML responses are accepted.
* Any non-200 response immediately fails fast, avoiding corrupted downstream logic.

---

### 1.7 Persisting the HTML for Deterministic Reuse

```python
with open(CACHE_FILE, "w", encoding="utf-8") as f:
    f.write(html)
```

**Why writing raw HTML to disk matters**

* The cached HTML becomes a **static snapshot** of Amazon’s page at that moment.
* Parsing logic can be tested repeatedly without re-fetching live content.
* Beginners can inspect the HTML file manually to understand DOM structure.
* This step decouples network variability from parsing complexity.

---

### 1.8 Output of Step 1

> **Guaranteed Output**

* A fully populated `productpage.html` file containing Amazon search HTML.
* A Python variable `html` holding the exact same HTML content in memory.

This output becomes the **sole input** for Step 2, which focuses exclusively on HTML parsing and product block extraction.
