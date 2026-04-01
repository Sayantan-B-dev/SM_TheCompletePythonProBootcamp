## Data Source Definition and External Dependency Contracts

The application fetches weather data from a third-party HTTP weather service defined by the environment variable `API_ENDPOINT`.
Authentication is performed using an API key loaded from environment variables under `API_KEY`.
The API response is expected to follow a fixed hierarchical JSON schema with `location`, `current`, and `forecast` root keys.
All downstream logic assumes the presence of forecast data for exactly one day.

The request parameters explicitly request a single forecast day using `"days": 1`.
The city name string acts as the primary query identifier for location resolution.
Any deviation in API schema will propagate errors unless explicitly guarded.

---

## Data Retrieval Flow and Network Layer Responsibilities

### Request Construction Logic

The `build_params` function constructs a dictionary containing authentication and query parameters.
This dictionary is passed directly to the HTTP client without transformation or validation.

```python
{
    "key": API_KEY,
    "q": city,
    "days": 1
}
```

The responsibility of request correctness is entirely delegated to environment configuration.

### Network Fetch Execution

The `fetch_weather` function performs a synchronous HTTP GET request using `requests.get`.
A strict timeout of ten seconds is enforced to prevent indefinite blocking behavior.
HTTP status validation is enforced through `raise_for_status`, aborting execution on non-success responses.

The returned payload is assumed to be valid JSON and parsed immediately.

---

## Data Caching Strategy and Temporal Validation

### Cache Storage Model

Weather data is cached as a JSON file located at `data/json/weather.json`.
Each cache entry stores two top-level keys: `weather_data` and `timestamp`.

The timestamp is recorded using ISO-8601 local datetime serialization.

### Cache Validation Logic

Cache validity is evaluated by comparing the current local time against the stored timestamp.
A cache entry is considered valid if the elapsed duration is less than one hour.

```python
datetime.datetime.now() - cached_timestamp < CACHE_TTL
```

If validation fails, the cache is discarded silently without raising exceptions.

### Cache Usage Policy

If valid cached data exists, no API request is performed.
If cached data is missing or expired, a fresh API call is executed and persisted.

This ensures network efficiency while maintaining reasonable data freshness.

---

## Core Data Decomposition and Semantic Extraction

### Location Metadata Extraction

From `weather_data["location"]`, the following fields are extracted and propagated:

* City name
* Administrative region
* Country

These values are treated as immutable identifiers for display and messaging contexts.

### Current Conditions Extraction

From `weather_data["current"]`, the system extracts:

* Current condition text
* Feels-like temperature in Celsius
* Wind direction
* Visibility in kilometers

These values represent real-time conditions at execution time.

### Forecast Day Extraction

Only the first element of `forecast.forecastday` is processed.
All future extensibility beyond single-day forecasting is intentionally excluded.

From `forecastday[0]["day"]`, the system extracts:

* Minimum, maximum, and average temperatures
* Maximum wind speed
* Average visibility
* Rain probability and rain presence flag
* UV index
* Condition code and descriptive text

From `forecastday[0]["astro"]`, astronomical data is extracted.

---

## Derived Logical Evaluations and Environmental Classification

### Thermal Comfort Classification

Comfort flags are derived using deterministic temperature thresholds:

* Comfortable temperature range defined between eighteen and twenty-eight degrees Celsius
* Heat stress defined at or above thirty-two degrees Celsius
* Cold stress defined at or below ten degrees Celsius

These flags are mutually independent and may overlap logically.

### Outdoor Usability Determination

Outdoor suitability is calculated using compound boolean logic requiring:

* No rain forecast
* Wind speed below twenty-five kilometers per hour
* Visibility equal to or greater than eight kilometers

Failure of any condition results in a cautionary classification.

### Rain Interpretation Logic

Rain probability is converted into human-readable messaging using fixed thresholds.

Zero probability yields a definitive no-rain message.
Low probability yields a mild caution message.
Higher probability yields a rain-likely message.

### Visibility Interpretation Logic

Visibility below five kilometers is classified as fog or mist conditions.
Higher visibility yields a clear conditions message.

### Weather Vibe Classification

A qualitative “vibe” is inferred using symbolic heuristics:

* Clear sky condition code yields a positive classification
* Mist keywords yield a calm classification
* All other cases yield an unsettled classification

This classification is purely descriptive and non-meteorological.

---

## Summary Object Normalization and Structural Guarantees

The analysis phase returns a normalized dictionary containing:

* Location and date identifiers
* Raw and derived weather conditions
* Risk and comfort flags
* Wind, visibility, and UV information
* Outdoor suitability boolean
* Astronomical timings and moon metadata

This summary object becomes the single source of truth for all presentation layers.

---

## Presentation Adaptation for Different Delivery Channels

### CLI Presentation Formatting

The CLI renderer formats the summary into a structured multiline string.
Visual emphasis is provided using `rich.Panel` with consistent ordering.
No additional logic is introduced at this stage beyond string formatting.

### GUI Adaptation Layer

The UI adapter transforms raw summary values into GUI-friendly strings.
Color codes are derived from comfort flags for immediate visual feedback.
Composite strings are created for temperature ranges, UV risk, wind, and rain.

No GUI component accesses raw weather data directly.

### Graphical Rendering Layer

The Tkinter GUI renders labels sequentially using preformatted adapter values.
All widgets are stateless and read-only after creation.
No user interaction modifies underlying data structures.

---

## Messaging and Notification Validation Logic

### Daily Send Enforcement

A filesystem-based lock mechanism prevents duplicate daily messages.
The current date is persisted in a text file after successful delivery.

If the stored date matches today’s date, message sending is skipped.

### Message Content Construction

SMS and WhatsApp messages are derived from the same summary object.
Formatting differs between plain text and markdown-styled WhatsApp messages.

No additional weather calculations occur during messaging.

### External Messaging Transport

Messages are dispatched using the Twilio REST client.
Transport configuration is entirely environment-driven.

---

## Entry Point Routing and Mode Selection

The application execution path is selected using the `APP_MODE` environment variable.
Only one execution mode is active per runtime invocation.

CLI, GUI, and messaging modes all share the same data pipeline.

---

## Data Integrity Assumptions and Implicit Constraints

The application assumes consistent API schema stability.
Missing or malformed fields may raise runtime exceptions.
Timezone normalization is not explicitly handled.
All datetime comparisons use local system time.

The system prioritizes clarity and determinism over defensive abstraction.
