## STEP 1 — DATA INGESTION FROM AVIATIONSTACK (CODE-FIRST, PRACTICAL EXPLANATION)

### 1.1 What STEP 1 Is Responsible For

STEP 1 exists only to **pull live flight data from Aviationstack and normalize it into clean Python dictionaries**.
No enrichment, no persistence, no business logic pollution happens here.
If this step fails, the entire pipeline must stop immediately.

---

### 1.2 Core Function Involved

```
aviation_client.fetch_live_flights(limit: int) -> list[dict]
```

This function performs **four concrete actions**, always in the same order.

---

### 1.3 Action 1 — Build Request Parameters

```python
params = {
    "access_key": AVIATIONSTACK_API_KEY,  # API authentication
    "limit": limit                        # Max number of flights requested
}
```

Explanation
The API key authenticates the request, while `limit` controls payload size to avoid quota exhaustion and unnecessary network cost.
Nothing else is requested intentionally to keep the response predictable and small.

---

### 1.4 Action 2 — Perform the HTTP Request Safely

```python
response = requests.get(
    AVIATIONSTACK_BASE_URL,
    params=params,
    timeout=15
)

response.raise_for_status()
```

Explanation
A timeout is mandatory to avoid hanging processes.
`raise_for_status()` ensures that **HTTP 4xx or 5xx failures stop execution immediately**, preventing invalid data from entering the system.

Expected behavior

* HTTP 200 → continue
* HTTP 401 / 403 → invalid API key
* HTTP 429 → quota exceeded
* HTTP 5xx → upstream failure

---

### 1.5 Action 3 — Parse and Inspect Raw API Payload

```python
payload = response.json()
raw_flights = payload.get("data", [])

log(f"Aviationstack returned {len(raw_flights)} raw flight records")
```

Explanation
The Aviationstack API nests all flight records inside the `data` array.
Using `.get("data", [])` guarantees safe iteration even if the response shape changes or becomes partial.

---

### 1.6 Action 4 — Normalize API Chaos Into Stable Python Objects

```python
flights = []

for item in raw_flights:
    live_data = item.get("live") or {}

    flights.append({
        "airline_name": (item.get("airline") or {}).get("name"),
        "flight_iata": (item.get("flight") or {}).get("iata"),
        "departure_airport": (item.get("departure") or {}).get("airport"),
        "departure_iata": (item.get("departure") or {}).get("iata"),
        "arrival_airport": (item.get("arrival") or {}).get("airport"),
        "arrival_iata": (item.get("arrival") or {}).get("iata"),
        "aircraft_model": (item.get("aircraft") or {}).get("icao"),
        "flight_status": item.get("flight_status"),
        "altitude": live_data.get("altitude"),
        "speed": live_data.get("speed_horizontal")
    })
```

Explanation
The Aviationstack response is deeply nested and inconsistent.
This step flattens the structure into a **stable internal contract** that downstream code can trust.

Key design choices

* `.get()` everywhere prevents KeyErrors
* Missing `live` telemetry does **not crash ingestion**
* Internal field names are decoupled from API naming

---

### 1.7 Expected Output of STEP 1

```python
[
  {
    "airline_name": "IndiGo",
    "flight_iata": "6E204",
    "departure_airport": "Netaji Subhas Chandra Bose International",
    "departure_iata": "CCU",
    "arrival_airport": "Chhatrapati Shivaji International",
    "arrival_iata": "BOM",
    "aircraft_model": "A320",
    "flight_status": "active",
    "altitude": 35000,
    "speed": 780
  },
  ...
]
```

This output is **guaranteed clean, flat, and predictable**, even when the API response is not.

---

### 1.8 What STEP 1 Explicitly Does NOT Do

* No Google Sheets interaction
* No retries or backoff logic
* No user-facing formatting
* No mutation beyond normalization

STEP 1’s only job is **trustworthy data ingestion**, nothing more, nothing less.
