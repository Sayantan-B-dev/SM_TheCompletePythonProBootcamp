## Aviationstack Integration — Conceptual Model and Reusable Mental Pattern

> **Mental shortcut:**
> *Aviationstack is a read-only observation API that answers one question reliably: “What flight data exists right now for these constraints?”*

In this project, Aviationstack is used strictly as an **external truth source**, never as storage, never as business logic, and never as a decision engine.

---

## Where Aviationstack Fits in the Overall System

```text
Real-world flights
        │
        ▼
Aviationstack REST API
        │
        ▼
flight_search.py
        │
        ▼
FlightData (domain object)
        │
        ▼
main.py orchestration logic
```

Aviationstack is queried **per route**, and its response is treated as **optional**, never guaranteed.

---

## Why Aviationstack Is Isolated in `flight_search.py`

```text
flight_search.py exists to:
• Encapsulate external API volatility
• Normalize third-party data into internal objects
• Prevent API-specific assumptions from leaking elsewhere
```

This design ensures that replacing Aviationstack later does **not** require touching persistence, orchestration, or notification logic.

---

## Environment Configuration — API Key Handling

```env
AVIATIONSTACK_API_KEY=your_api_key_here
```

Why this pattern is reusable:

* Prevents accidental key leakage in repositories
* Enables per-environment API usage control
* Allows key rotation without modifying application code

---

## FlightSearch — External Observation Client

### Class Responsibility

```text
FlightSearch represents:
• One configured API client
• One responsibility: observe live flight data
• Zero responsibility for persistence or formatting
```

---

## Initialization Logic — Fail Fast Philosophy

```python
class FlightSearch:
    """
    Retrieves real flight observations from Aviationstack.
    """

    def __init__(self):
        # Read API key from environment for security and portability
        self.api_key = os.getenv("AVIATIONSTACK_API_KEY")

        # Base URL remains constant across all Aviationstack endpoints
        self.base_url = "https://api.aviationstack.com/v1"

        # Immediate failure avoids silent misconfiguration
        if not self.api_key:
            raise RuntimeError("AVIATIONSTACK_API_KEY missing")
```

Why this matters:

* Prevents meaningless HTTP calls
* Makes configuration errors obvious and early
* Avoids partial execution with corrupted assumptions

---

## Observing a Route — Core API Interaction

### Method Purpose

```text
observe_route(departure_iata, arrival_iata)
→ Ask Aviationstack for any live flight matching this route
→ Return exactly one observation or nothing at all
```

---

## Code Example with Line-by-Line Explanation

```python
def observe_route(self, departure_iata: str, arrival_iata: str):
    """
    Queries Aviationstack for live flight data between two airports.

    Returns:
        FlightData instance if data exists
        None if no observable flight is found
    """

    # Query parameters narrow the dataset at the API level
    params = {
        "access_key": self.api_key,        # Authentication token
        "dep_iata": departure_iata,        # Departure airport filter
        "arr_iata": arrival_iata,          # Arrival airport filter
        "limit": 1                         # Reduce payload and API cost
    }

    # Perform HTTP GET request to Aviationstack
    response = requests.get(
        f"{self.base_url}/flights",
        params=params
    )

    # Fail immediately if API responds with error status
    response.raise_for_status()

    # Parse JSON payload into Python structure
    data = response.json().get("data", [])

    # If no flights exist, signal absence explicitly
    if not data:
        return None

    # Select the first matching flight record
    flight = data[0]

    # Normalize third-party data into internal domain object
    return FlightData(
        airline=flight["airline"]["name"],
        flight_number=flight["flight"]["iata"],
        departure_iata=departure_iata,
        arrival_iata=arrival_iata
    )
```

---

## Actual HTTP Request Sent to Aviationstack

```http
GET /v1/flights?access_key=API_KEY&dep_iata=DEL&arr_iata=JFK&limit=1 HTTP/1.1
Host: api.aviationstack.com
```

Key reusable concept:

* **Filtering happens server-side**, not in your code
* Smaller payloads mean lower latency and lower quota usage

---

## Typical Aviationstack JSON Response (Simplified)

```json
{
  "data": [
    {
      "airline": {
        "name": "Air India"
      },
      "flight": {
        "iata": "AI101"
      },
      "departure": {
        "iata": "DEL"
      },
      "arrival": {
        "iata": "JFK"
      }
    }
  ]
}
```

Important observation:

* Aviationstack responses are **deeply nested**
* You must extract only what you need
* Never propagate raw API payloads further downstream

---

## Output of `observe_route()` Method

### When a Flight Exists

```python
FlightData(
    airline="Air India",
    flight_number="AI101",
    departure_iata="DEL",
    arrival_iata="JFK"
)
```

### When No Flight Exists

```python
None
```

This explicit `None` return value is critical for safe control flow.

---

## Why `None` Is Better Than Empty Objects

```text
None clearly signals:
• No observable data exists
• No persistence should occur
• No notification should be sent
```

This avoids:

* Fake updates
* Misleading logs
* Polluted historical records

---

## Downstream Usage in `main.py`

```python
flight = flight_search.observe_route(
    departure_iata=row["departureIata"],
    arrival_iata=row["arrivalIata"]
)

if not flight:
    continue
```

This pattern is reusable across any external read-only API integration.

---

## Final Observable Output of This Project

### Console Output

```text
✈️ Flight Observed
Air India flight AI101 from DEL to JFK
```

### Data Written Elsewhere

* Aviationstack **does not store anything**
* All persistence occurs via Sheety
* Aviationstack is purely observational

---

## Universal Aviationstack Reuse Blueprint

```text
1. Treat Aviationstack as a read-only truth source
2. Always filter aggressively using query parameters
3. Never assume data will exist for a query
4. Convert API responses into internal domain models
5. Return None explicitly when no data exists
6. Never leak raw API payloads into business logic
7. Keep API logic isolated in a single module
```

---

## Reusable External API Mental Model

```text
External API
   ↓
Client Wrapper (flight_search.py)
   ↓
Domain Object (FlightData)
   ↓
Application Logic
   ↓
Persistence / Notification
```

This exact structure applies cleanly to **weather APIs**, **stock APIs**, **maps APIs**, and **any observational service** used in future projects.
