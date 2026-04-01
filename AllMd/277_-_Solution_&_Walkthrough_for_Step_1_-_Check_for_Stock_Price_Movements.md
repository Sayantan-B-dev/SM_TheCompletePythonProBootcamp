## STOCK DOMAIN — COMPLETE DATA, WORKFLOW, AND EXECUTION ANALYSIS

---

## 1. External Dependencies and Installed Components Used for STOCK Data

### 1.1 Python Packages Directly Involved

* `requests` is used for synchronous HTTP communication with the Alpha Vantage REST API endpoints, handling query parameter encoding and response retrieval.
* `rich` is used exclusively for structured, human-readable terminal output, not affecting business logic or calculations.
* Standard library modules such as `datetime`, `os`, and `pathlib` are used for time normalization, configuration loading, and filesystem coordination.

### 1.2 External Services and APIs

* **Alpha Vantage API** is the exclusive market data provider for stock price movement.
* The system uses **daily adjusted time series data**, not intraday or real-time streaming feeds.
* Authentication is performed using a static API key loaded from environment variables at runtime.

---

## 2. Alpha Vantage API Usage for STOCK Data

### 2.1 Endpoint and Function Used

* Base endpoint is loaded from environment configuration as `STOCK_ENDPOINT`.
* For STOCK assets, the API function used is:

  ```
  TIME_SERIES_DAILY
  ```

### 2.2 Query Parameters Used

* `function=TIME_SERIES_DAILY` specifies daily OHLC data.
* `symbol=<STOCK_TICKER>` represents the resolved equity ticker symbol.
* `apikey=<API_KEY>` authenticates the request.

### 2.3 Expected API Payload Structure

The code expects the response JSON to contain:

* A top-level key named `"Time Series (Daily)"`
* Each date key mapping to a dictionary containing `"4. close"` values

This expectation is explicitly encoded in a schema map rather than scattered hardcoded strings.

---

## 3. STOCK Asset Resolution Workflow

### 3.1 Entry Point from User Input

* User supplies a keyword using the CLI argument format:

  ```
  news_about=apple
  ```
* `main.py` extracts this keyword using `get_news_topic()`.

### 3.2 Asset Normalization Logic

* `resolve_asset(topic)` in `assets.py` performs keyword normalization.
* It maps human-readable identifiers like `"apple"` to `"AAPL"`.

### 3.3 Asset Type Classification

* STOCK classification occurs when:

  * Symbol contains only alphabetic characters.
  * Symbol length is less than or equal to five characters.
* Output contract:

  ```
  ("STOCK", "AAPL")
  ```

This classification directly controls which Alpha Vantage function is selected later.

---

## 4. STOCK Parameter Construction in main.py

### 4.1 Conditional API Configuration

Once the asset type resolves to STOCK:

```python
function = "TIME_SERIES_DAILY"
stock_params = {
    "function": function,
    "symbol": symbol,
    "apikey": STOCK_API_KEY,
}
```

### 4.2 Why This Construction Is Correct

* Alpha Vantage requires distinct function names for different asset classes.
* The symbol format for stocks does not require base or quote currency splitting.
* Parameters are passed transparently to `requests.get`, avoiding mutation or side effects.

---

## 5. Core STOCK Algorithm — Percentage Change Calculation

### 5.1 Entry Function

* `get_stock_percentage_change(stock_params)` in `stocks.py` is the sole computation function.

### 5.2 Network and Transport Handling

* Uses `requests.get` with a timeout to avoid indefinite blocking.
* `response.raise_for_status()` ensures HTTP-level errors are caught immediately.
* Network exceptions are intercepted and logged, returning `None` to signal failure upstream.

---

## 6. Explicit Alpha Vantage Response State Handling

The function does not assume success and checks **three known Alpha Vantage failure states**.

### 6.1 `"Information"` Response Handling

Triggered when:

* API key is throttled.
* Demo or restricted key is used.
* Backend is temporarily unavailable.

Handling strategy:

* User-visible explanation is printed.
* Function returns `None` to prevent downstream logic from executing incorrectly.

### 6.2 `"Note"` Response Handling

Triggered by:

* Rate limit violations.
* Excessive request frequency.

Handling strategy:

* Explicit warning is printed.
* Function returns `None` to avoid invalid calculations.

### 6.3 `"Error Message"` Response Handling

Triggered by:

* Invalid symbols.
* Unsupported function parameters.

Handling strategy:

* Error content is printed verbatim.
* Execution halts for this asset.

This explicit handling prevents silent failures and undefined behavior.

---

## 7. STOCK Time Series Parsing Logic

### 7.1 Schema-Driven Parsing

* `TIME_SERIES_MAP` defines:

  * The expected top-level series key.
  * The expected closing price field name.

For STOCK:

```python
{
  "series": "Time Series (Daily)",
  "close": "4. close"
}
```

### 7.2 Validation of Payload Shape

* Confirms the series key exists before accessing it.
* Logs actual payload keys if mismatch occurs, aiding debugging.

### 7.3 Date Ordering Assumption

* Alpha Vantage returns daily series with most recent date first.
* The function relies on dictionary key order preservation, valid in Python 3.7+.

---

## 8. Percentage Change Calculation Algorithm

### 8.1 Data Selection

* Extracts the two most recent trading days:

  * `dates[0]` → latest close
  * `dates[1]` → previous close

### 8.2 Mathematical Formula

```
percentage_change = ((latest - previous) / previous) * 100
```

### 8.3 Safety and Type Handling

* Values are cast to `float` explicitly.
* `KeyError` and `ValueError` are caught if expected fields are missing or malformed.
* Result is rounded to two decimal places for stable presentation.

---

## 9. Threshold-Based Decision Logic in main.py

### 9.1 Output Branching

* If percentage change is `None`, execution stops for STOCK logic.
* If percentage change is greater than `5%`:

  * STOCK movement is considered significant.
  * News retrieval workflow is activated.
* Otherwise:

  * Only numerical movement is displayed.
  * Asset list is shown for exploration.

### 9.2 Why This Works Correctly

* Numerical computation and contextual enrichment are decoupled.
* News API is never called unless market movement justifies it.
* Prevents unnecessary API usage and alert fatigue.

---

## 10. STOCK-Specific Variables and Their Scope

### 10.1 Configuration-Level Variables

* `STOCK_ENDPOINT` defined in `config.py`
* `STOCK_API_KEY` loaded from environment

### 10.2 Runtime Variables

* `symbol` resolved in `main.py`
* `stock_params` constructed dynamically per asset
* `change` storing computed percentage movement

Each variable has a single responsibility and clear ownership.

---

## 11. Edge Cases Explicitly Handled for STOCK Workflow

* Network timeouts or DNS failures.
* API throttling and cooldown responses.
* Invalid or unsupported ticker symbols.
* Missing or insufficient trading day data.
* Payload schema changes or partial responses.
* Non-trading days resulting in insufficient time series entries.

Each edge case returns control safely to the orchestrator without corrupting state.

---

## 12. Why the STOCK Workflow Is Correct and Stable

* API contracts are validated before computation.
* All external dependencies are isolated behind explicit functions.
* No hidden global state influences calculations.
* Failure states are surfaced early and clearly.
* Business logic remains deterministic and reproducible.

---

## 13. Mental Model of STOCK Data Flow

```
User Keyword
   ↓
Asset Resolution (STOCK)
   ↓
Alpha Vantage Parameter Construction
   ↓
Daily Time Series Fetch
   ↓
Schema Validation
   ↓
Two-Day Price Delta Computation
   ↓
Threshold Evaluation
   ↓
Context Expansion or Silent Exit
```

This workflow ensures STOCK-related logic remains **accurate, explainable, resilient, and bounded**, even under degraded network or API conditions.
