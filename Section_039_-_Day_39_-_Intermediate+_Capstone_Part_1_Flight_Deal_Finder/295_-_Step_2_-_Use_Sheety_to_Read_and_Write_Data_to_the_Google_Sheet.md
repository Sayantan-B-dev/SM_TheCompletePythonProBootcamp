## Sheety Integration — Conceptual Model and Practical Reuse Pattern

> **Mental shortcut:**
> *Sheety turns a Google Sheet into a strict REST database where each row behaves like an API resource.*

---

## Where Sheety Sits in This Project

```text
Google Sheet  ←→  Sheety REST API  ←→  data_manager.py  ←→  main.py
```

Sheety is **not business logic**, **not storage logic you control**, and **not a database server**.
It is a **translation layer** that exposes spreadsheet rows as HTTP resources.

---

## Google Sheet Structure Assumed by This Project

```text
Sheet Name: prices

| id | departureIata | arrivalIata | airline | flightNumber | lastSeenAt |
|----|---------------|-------------|---------|--------------|------------|
|  1 | DEL           | JFK         |         |              |            |
|  2 | BOM           | LHR         |         |              |            |
```

Important behavioral rule:
**Sheety automatically generates the `id` column and uses it as the REST identifier.**

---

## Environment Configuration — Security and Decoupling

```env
SHEETY_BASE_URL=https://api.sheety.co/<project>/<sheet-name>/prices
SHEETY_BEARER_TOKEN=your_long_lived_secret_token
```

Why this matters for future projects:

* No credentials inside source code
* Environment-based configuration allows reuse across environments
* Token rotation does not require code changes

---

## DataManager — Sheety Client Abstraction

### Purpose of This File

```text
data_manager.py exists to:
• Hide HTTP mechanics from the rest of the application
• Centralize authentication and headers
• Guarantee schema correctness when reading or writing
```

---

## Sheety Session Setup — Explained Line by Line

```python
self.session = requests.Session()
```

This creates a reusable HTTP client, reducing overhead and ensuring consistent headers.

```python
self.session.headers.update({
    "Authorization": f"Bearer {self.sheety_bearer_token}",
    "Content-Type": "application/json"
})
```

Why this matters:

* Sheety requires Bearer authentication for every request
* JSON content type guarantees predictable request parsing
* Session-level headers prevent duplication and mistakes

---

## Reading Data from Google Sheet via Sheety

### Code Example with Deep Commentary

```python
def get_routes(self):
    """
    Fetches all rows from the Google Sheet via Sheety.

    This method assumes:
    • The sheet name is 'prices'
    • Sheety exposes rows under the 'prices' key
    """

    # Perform HTTP GET request to Sheety endpoint
    response = self.session.get(self.sheety_base_url)

    # Immediately fail if HTTP status is not successful
    response.raise_for_status()

    # Convert JSON payload into Python dictionary
    data = response.json()

    # Extract only the rows, ignoring metadata
    return data["prices"]
```

### Actual HTTP Request Being Made

```http
GET /prices HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: application/json
```

### Actual JSON Response from Sheety

```json
{
  "prices": [
    {
      "id": 1,
      "departureIata": "DEL",
      "arrivalIata": "JFK",
      "airline": "",
      "flightNumber": "",
      "lastSeenAt": ""
    }
  ]
}
```

### Output Returned to `main.py`

```python
[
  {
    "id": 1,
    "departureIata": "DEL",
    "arrivalIata": "JFK",
    "airline": "",
    "flightNumber": "",
    "lastSeenAt": ""
  }
]
```

---

## Updating a Single Row — REST Resource Mental Model

### Key Concept for Reuse

```text
Each Google Sheet row == One REST resource == One unique URL
```

Row update URL format:

```text
<base-url>/<row-id>
```

Example:

```text
https://api.sheety.co/project/sheet/prices/1
```

---

## Updating Observation Data — Code with Explanation

```python
def update_route_observation(self, row_id, airline, flight_number):
    """
    Updates a single Google Sheet row using its unique id.

    This performs a partial update, not a full overwrite.
    """

    # Construct URL for specific sheet row
    update_url = f"{self.sheety_base_url}/{row_id}"

    # Payload structure must match Sheety expectations
    payload = {
        "price": {
            "airline": airline,
            "flightNumber": flight_number,
            "lastSeenAt": datetime.utcnow().isoformat()
        }
    }

    # Execute PUT request to update row
    response = self.session.put(update_url, json=payload)

    # Fail immediately if update was rejected
    response.raise_for_status()
```

### Actual HTTP Request

```http
PUT /prices/1 HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: application/json
```

```json
{
  "price": {
    "airline": "Air India",
    "flightNumber": "AI101",
    "lastSeenAt": "2026-02-08T17:12:44.531921"
  }
}
```

---

## Why the Payload Is Nested Under `"price"`

Sheety enforces a strict rule:

```text
Top-level key must equal singular form of sheet name
```

Sheet name: `prices`
Payload wrapper: `price`

This rule is universal across all Sheety projects and reusable everywhere.

---

## End-to-End Execution Output of This Project

### Console Output Produced by Notification Layer

```text
✈️ Flight Observed
Air India flight AI101 from DEL to JFK
```

### Google Sheet After Execution

```text
| id | departureIata | arrivalIata | airline   | flightNumber | lastSeenAt                  |
|----|---------------|-------------|-----------|--------------|-----------------------------|
|  1 | DEL           | JFK         | Air India | AI101        | 2026-02-08T17:12:44.531921  |
```

---

## Universal Sheety Reuse Blueprint for Any Project

```text
1. Design your Google Sheet as a database table
2. Enable Sheety API access for the sheet
3. Treat rows as REST resources identified by id
4. Centralize Sheety logic in a single manager file
5. Never mix Sheety calls with business logic
6. Fail fast on HTTP or schema mismatches
7. Use ISO timestamps for all time-based fields
```

---

## Reusable Data Flow Summary

```text
User-defined data → Google Sheet
Google Sheet → Sheety REST API
Sheety REST API → DataManager
DataManager → Application Logic
Application Logic → DataManager
DataManager → Sheety REST API
Sheety REST API → Google Sheet
```

This pattern scales cleanly from **tiny scripts** to **multi-service automation systems** without architectural changes.
