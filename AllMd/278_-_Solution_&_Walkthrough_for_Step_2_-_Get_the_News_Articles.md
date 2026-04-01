## NEWS DOMAIN — COMPLETE DATA FLOW, ARCHITECTURE, AND EXECUTION ANALYSIS

---

## 1. External Dependencies and Installed Components for NEWS Handling

### 1.1 Python Libraries Involved in NEWS Workflow

* `requests` is used as the HTTP client for synchronous REST communication with the News API endpoint, handling query serialization, response retrieval, and timeout control.
* `rich` is used for structured terminal rendering, specifically `Panel` components, ensuring readable presentation of article metadata without affecting business logic.
* Standard library modules such as `json` handling through `requests`, and basic Python data structures are relied upon for safe parsing and iteration.

These dependencies ensure the NEWS workflow remains lightweight, synchronous, deterministic, and transparent in behavior.

---

## 2. External NEWS Service and API Configuration

### 2.1 News API Provider

* The project uses **NewsAPI.org** as the sole provider of news content.
* NewsAPI is a REST-based aggregation service sourcing articles from publishers, blogs, and news outlets.
* Authentication is handled via a static API key supplied through environment variables.

### 2.2 Endpoint Used

* The endpoint is loaded dynamically from environment configuration:

  ```
  NEWS_ENDPOINT
  ```
* In typical usage, this corresponds to:

  ```
  https://newsapi.org/v2/top-headlines
  ```

### 2.3 API Authentication

* Authentication is handled using:

  ```
  apiKey=<NEWS_API_KEY>
  ```
* The key is injected into every request and validated server-side by NewsAPI.

---

## 3. NEWS Configuration and Parameter Construction

### 3.1 Where Configuration Lives

* `config.py` is the single source of truth for:

  * `NEWS_ENDPOINT`
  * `NEWS_API_KEY`
* These values are loaded from `.env` at startup using `python-dotenv`.

This ensures secrets are never hardcoded and can be rotated without code changes.

---

## 4. NEWS Trigger Conditions Within the System

### 4.1 Conditional Invocation

* NEWS data fetching is **not unconditional**.
* It is triggered only when:

  ```
  stock_percentage_change > 5
  ```
* This decision is made in `main.py`.

### 4.2 Why This Conditional Design Exists

* Prevents unnecessary News API calls.
* Avoids exhausting API quotas.
* Reduces noise by only surfacing news when market movement is meaningful.
* Couples narrative context strictly to significant numerical signals.

---

## 5. NEWS Parameter Assembly in main.py

### 5.1 Query Parameter Dictionary

```python
news_params = {
    "q": topic,
    "apiKey": NEWS_API_KEY,
    "country": "us",
    "pageSize": 3,
}
```

### 5.2 Parameter Semantics

* `q` defines the keyword search term derived from the asset topic.
* `country` restricts results to a specific geographic news market.
* `pageSize` caps the number of returned articles, limiting payload size and rendering cost.

This explicit parameter construction ensures predictable response sizes and relevance.

---

## 6. Primary NEWS Fetch Function

### 6.1 Function Entry Point

* Function name:

  ```
  get_news_data()
  ```
* Defined in:

  ```
  news.py
  ```

### 6.2 Function Signature and Contract

```python
get_news_data(news_params, render=True, limit=3)
```

**Parameters**

* `news_params`: dictionary of API query parameters.
* `render`: boolean flag controlling console rendering behavior.
* `limit`: maximum number of articles to process.

**Output**

* Always returns a list of article dictionaries.
* Returns an empty list on any failure condition.

---

## 7. Network-Level Error Handling in NEWS Workflow

### 7.1 Transport Failure Handling

```python
requests.get(..., timeout=10)
```

* Network errors such as DNS failures, connection resets, or timeouts are caught via `RequestException`.
* A structured error panel is printed using `rich`.
* Function exits early, returning an empty list.

This prevents partial execution or corrupted state propagation.

---

## 8. HTTP Response Validation Logic

### 8.1 Non-200 Status Code Handling

* Explicit check:

  ```
  if response.status_code != 200
  ```
* The response body and status code are printed verbosely for diagnostics.
* Execution is terminated safely.

This avoids assuming API success purely based on JSON parsing.

---

## 9. JSON Payload Parsing and Validation

### 9.1 Expected Payload Structure

The function expects the JSON payload to contain:

```
{
  "articles": [ { article_object }, ... ]
}
```

### 9.2 Article Extraction Logic

```python
articles = data.get("articles", [])[:limit]
```

* Uses `.get()` to avoid `KeyError`.
* Slices explicitly to enforce upper bounds on processing.
* Ensures predictable rendering behavior.

---

## 10. No-Data and Empty Response Handling

### 10.1 Empty Article List

If no articles are returned:

* A warning panel is displayed explaining likely causes.
* The function returns an empty list.

### 10.2 Common Causes Covered

* Invalid query keywords.
* Misconfigured endpoint parameters.
* Geographic restrictions without proper `country` or `sources`.
* API quota exhaustion returning empty payloads.

This makes failure reasons visible instead of silent.

---

## 11. Rendering Layer Separation

### 11.1 Rendering Delegation

* NEWS fetching logic does **not** format articles directly.
* Rendering is delegated to:

  ```
  render_article()
  ```

  defined in `article.py`.

This ensures clean separation between data retrieval and presentation.

---

## 12. Article Rendering Workflow

### 12.1 Rendering Function

```python
render_article(article: dict, index: int | None)
```

### 12.2 Fields Extracted

* `title`
* `source.name`
* `description`
* `url`
* `publishedAt`

Each field is accessed defensively using `.get()` with fallback values.

---

## 13. Datetime Normalization Logic

### 13.1 Timestamp Parser

```python
_parse_datetime(iso_str)
```

### 13.2 Algorithm Details

* Handles missing timestamps gracefully.
* Converts ISO-8601 strings into UTC-readable format.
* Converts trailing `Z` into explicit UTC offset.
* Uses `datetime.fromisoformat` for strict parsing.
* Returns `"Unknown date"` on any parsing failure.

This ensures malformed or missing timestamps never crash rendering.

---

## 14. Presentation Guarantees

### 14.1 Rich Panel Formatting

* Each article is rendered in a rounded panel.
* Index-based numbering ensures clear article ordering.
* Visual hierarchy highlights title, source, time, summary, and link.

Presentation is consistent regardless of data quality.

---

## 15. NEWS-Specific Variables and Their Scope

### 15.1 Configuration Variables

* `NEWS_ENDPOINT` defined in `config.py`
* `NEWS_API_KEY` loaded from environment

### 15.2 Runtime Variables

* `news_params` created in `main.py`
* `articles` list created in `news.py`
* Individual `article` dictionaries passed to renderer

Each variable is scoped tightly to its responsibility.

---

## 16. Edge Cases Explicitly Handled in NEWS Workflow

* Network failures and timeouts.
* HTTP error responses.
* Empty or missing `articles` payload.
* Missing article fields.
* Malformed timestamps.
* Over-fetching prevention via slicing.
* Rendering disabled scenarios using `render` flag.

All edge cases terminate safely without cascading failures.

---

## 17. Why the NEWS Workflow Is Correct and Robust

* External API usage is bounded and validated.
* No assumptions are made about payload completeness.
* Rendering is decoupled from retrieval.
* Failures never crash the program.
* API quotas are respected by conditional invocation.

---

## 18. Mental Model of NEWS Data Flow

```
Market Signal Trigger
   ↓
Query Parameter Assembly
   ↓
NewsAPI HTTP Request
   ↓
Transport Validation
   ↓
HTTP Status Validation
   ↓
Payload Shape Validation
   ↓
Article Limiting
   ↓
Defensive Field Extraction
   ↓
Datetime Normalization
   ↓
Structured Terminal Rendering
```

This NEWS subsystem acts as a **contextual amplification layer**, converting raw market movement into human-readable narrative only when justified, while remaining resilient against malformed data, unreliable networks, and external API volatility.
