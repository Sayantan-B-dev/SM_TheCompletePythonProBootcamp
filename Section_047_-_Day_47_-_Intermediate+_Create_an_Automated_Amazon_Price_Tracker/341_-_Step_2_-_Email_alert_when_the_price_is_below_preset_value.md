## Step 2 — **HTML Parsing, DOM Traversal, and Product Block Extraction**

### 2.1 Purpose of This Step in the Overall System

This step is responsible for **transforming raw HTML text into structured, navigable objects** and isolating only those sections of the document that represent individual product listings. Instead of dealing with unreadable HTML strings, the system converts the document into a tree-like structure that can be queried precisely and safely. This separation ensures that data extraction logic operates only on valid product containers and ignores unrelated page elements such as headers, footers, ads, and scripts.

---

### 2.2 Files Responsible for This Step

> **`scraper.py`**
> This file encapsulates all HTML parsing and product-level data extraction logic, ensuring clean separation between network operations and parsing behavior.

---

### 2.3 Converting Raw HTML into a Navigable DOM Tree

```python
from bs4 import BeautifulSoup

def parse_products(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.find_all("div", attrs={"data-component-type": "s-search-result"})
```

**Explanation of parsing mechanics and library choice**

* `BeautifulSoup` converts the raw HTML string into a structured DOM tree.
* The `"lxml"` parser is chosen because it is faster, more forgiving, and handles malformed HTML better than default parsers.
* The resulting `soup` object allows hierarchical traversal similar to a browser DOM.
* This transformation is mandatory because string-based HTML parsing is unreliable and error-prone.

---

### 2.4 Identifying Product Containers Reliably

**Why `data-component-type="s-search-result"` is critical**

* Amazon wraps every product listing inside a `<div>` with this attribute.
* This attribute remains more stable than CSS class names, which change frequently.
* Using semantic attributes reduces the likelihood of parser breakage.
* Each returned `<div>` corresponds to exactly one visible product card.

---

### 2.5 Output Structure of `parse_products`

```python
return soup.find_all("div", attrs={"data-component-type": "s-search-result"})
```

**What this function returns**

* A Python list containing multiple BeautifulSoup `Tag` objects.
* Each object represents a single product block.
* No data is extracted yet; only product boundaries are identified.
* This list becomes the controlled input for granular extraction logic.

---

### 2.6 Extracting Core Product Fields Safely

```python
def get_each_product_info(product_div):
```

This function operates on **one product container at a time**, ensuring that failures in one product do not affect others.

---

### 2.7 Title and Subtitle Extraction Logic

```python
h2 = product_div.find("h2")
if h2 and h2.find("span"):
    title = h2.find("span").get_text(strip=True)
```

**Behavioral reasoning**

* Product titles are nested inside `<h2><span>` structures.
* Defensive checks prevent `NoneType` errors when elements are missing.
* `strip=True` ensures removal of invisible whitespace and formatting noise.

```python
long_title_h2 = product_div.find(
    "h2",
    class_="a-size-base-plus a-spacing-none a-color-base a-text-normal"
)
```

**Why subtitle extraction exists**

* Amazon often duplicates titles in extended formats.
* When subtitle equals title, redundancy is replaced with a placeholder.
* This normalization improves downstream presentation clarity.

---

### 2.8 Product URL, Sponsored Links, and ASIN Resolution

```python
a_tag = product_div.find("a", href=True)
```

**Link parsing logic explanation**

* Amazon uses multiple link formats for organic and sponsored products.
* Sponsored products use `/sspa/click` redirection URLs.
* Query string decoding is required to retrieve the real product URL.
* ASIN extraction relies on detecting `/dp/{ASIN}` path segments.

This logic ensures **canonical URLs** regardless of sponsorship status.

---

### 2.9 Image, Price, Rating, and Sponsored Flag Detection

```python
img = product_div.find("img", class_="s-image")
price_tag = product_div.find("span", class_="a-offscreen")
rating_tag = product_div.find("span", class_="a-icon-alt")
```

**Key extraction guarantees**

* Image URLs are retrieved directly from `src` attributes.
* Prices use visually hidden spans to preserve accessibility formatting.
* Ratings are normalized into numeric-friendly `X/5` format.
* Sponsored status is inferred from visible label text rather than layout assumptions.

---

### 2.10 Normalized Data Output Contract

```python
return [
    title,
    subtitle,
    link,
    asin,
    image_url,
    sponsored,
    price,
    rating,
]
```

**Why list ordering matters**

* This list aligns exactly with CSV headers defined later.
* Consistent ordering prevents column misalignment.
* Missing values remain `None`, allowing clean downstream handling.

---

### 2.11 Output of Step 2

> **Guaranteed Output**

* A list of product containers from `parse_products`.
* A normalized list of extracted fields per product via `get_each_product_info`.
* Zero side effects outside memory, ensuring safe progression to storage.

This output becomes the **exclusive input** for Step 3, which focuses on structured persistence and CSV generation.
