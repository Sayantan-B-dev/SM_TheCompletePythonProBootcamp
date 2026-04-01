## STEP 3 — DATA PERSISTENCE VIA SHEETY (WRITE PATH, CODE-FIRST)

### 3.1 What STEP 3 Is Responsible For

STEP 3 takes **one fully enriched flight dictionary** and performs **exactly one irreversible side effect**:
persisting that record as a new row inside a Google Sheet using the Sheety REST API.

This step is intentionally isolated because **writes are the most dangerous operation** in any data pipeline.

---

### 3.2 Code Ownership and Execution Boundary

```
sheet_writer.py
```

Only this file is allowed to:

* Know Sheety endpoints
* Handle authentication headers
* Decide success or failure of persistence

---

### 3.3 Entry Point Function

```python
def write_flight_record(record: dict) -> None:
```

Explanation

* Input must already be validated and enriched
* Function returns nothing because persistence is a side effect
* Any failure must be observable and loud

---

### 3.4 Authorization and Transport Setup

```python
HEADERS = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}",
    "Content-Type": "application/json"
}
```

Explanation
Bearer authentication prevents accidental public exposure.
Headers are defined once to avoid duplication and inconsistency.

---

### 3.5 Payload Construction (Schema Translation)

```python
payload = {
    "sheet1": {
        "recorded_at_utc": datetime.utcnow().isoformat(),
        "airline_name": record.get("airline_name"),
        "flight_iata_code": record.get("flight_iata"),
        "departure_airport_name": record.get("departure_airport"),
        "departure_iata_code": record.get("departure_iata"),
        "arrival_airport_name": record.get("arrival_airport"),
        "arrival_iata_code": record.get("arrival_iata"),
        "aircraft_model": record.get("aircraft_model"),
        "flight_status": record.get("flight_status"),
        "altitude_feet": record.get("altitude"),
        "ground_speed_kmh": record.get("speed"),
        "fun_fact": record.get("fun_fact")
    }
}
```

Explanation
This is a **translation layer**, not business logic.
Internal field names are mapped explicitly to spreadsheet column names to prevent tight coupling.

Design choice
Missing values remain `null` instead of crashing the request.

---

### 3.6 HTTP Write Operation

```python
response = requests.post(
    SHEETY_BASE_URL,
    json=payload,
    headers=HEADERS,
    timeout=10
)
```

Explanation

* POST is used because each call creates a new row
* Timeout prevents stalled writes
* JSON encoding ensures predictable serialization

---

### 3.7 Correct Success Detection (Critical)

```python
if 200 <= response.status_code < 300:
    log(
        f"Row inserted successfully | "
        f"flight={record.get('flight_iata')} | "
        f"status={response.status_code}"
    )
```

Explanation
Sheety may return **200, 201, or 204** depending on configuration.
Checking a range prevents false negatives.

---

### 3.8 Failure Escalation Path

```python
else:
    error(
        f"Sheety request failed | "
        f"status={response.status_code} | "
        f"body={response.text}"
    )
    response.raise_for_status()
```

Explanation

* Error is logged before raising
* Full response body is preserved for debugging
* Exception propagation stops downstream corruption

Expected failures

* 401 → invalid token
* 403 → sheet permissions
* 429 → rate limiting
* 5xx → Sheety outage

---

### 3.9 Expected External Result of STEP 3

Google Sheet receives a new row:

```
| recorded_at_utc | airline_name | flight_iata_code | altitude_feet | ground_speed_kmh | fun_fact |
|-----------------|--------------|------------------|---------------|------------------|----------|
| 2026-02-09T...  | IndiGo       | 6E204            | 35000         | 780              | Planes...|
```

Each successful POST maps to **exactly one new row**, no updates, no overwrites.

---

### 3.10 What STEP 3 Explicitly Does NOT Do

* No retries or exponential backoff
* No batching
* No deduplication
* No validation of STEP 1 or STEP 2 assumptions

STEP 3 trusts upstream steps and focuses solely on **durable persistence with visibility**.
