## Improvement Areas — Reliability, Resilience, and User Experience Enhancement

---

## 1. Error Handling Strategy — Centralized, Predictable, and Explicit

### Current State Limitation

The current implementation relies heavily on implicit exception propagation, which is acceptable for prototypes but fragile for production-grade automation systems where partial failures are expected.

### Recommended Error Handling Layers

```text
Layered Error Handling Model
• Configuration errors handled at startup
• Network and API errors handled at integration boundaries
• Data validation errors handled before persistence
• Notification failures handled without blocking core flow
```

---

## 2. Improved `FlightSearch` — Defensive External API Consumption

### Failure Scenarios to Handle Explicitly

```text
• API quota exceeded
• Network timeout or DNS failure
• Malformed or partial API response
• Missing nested keys in JSON payload
```

### Improved `observe_route()` with Try/Except and Validation

```python
def observe_route(self, departure_iata: str, arrival_iata: str):
    """
    Safely queries Aviationstack and returns normalized flight data.

    All external API risks are contained inside this method to avoid
    polluting upstream orchestration logic.
    """

    params = {
        "access_key": self.api_key,
        "dep_iata": departure_iata,
        "arr_iata": arrival_iata,
        "limit": 1
    }

    try:
        # Network request with timeout to prevent hanging execution
        response = requests.get(
            f"{self.base_url}/flights",
            params=params,
            timeout=10
        )

        # Explicit HTTP status validation
        response.raise_for_status()

        # Parse JSON safely
        payload = response.json()
        flights = payload.get("data", [])

        # No observable flights is a valid, expected state
        if not flights:
            return None

        flight = flights[0]

        # Defensive extraction to avoid KeyError crashes
        airline_name = flight.get("airline", {}).get("name")
        flight_iata = flight.get("flight", {}).get("iata")

        if not airline_name or not flight_iata:
            return None

        return FlightData(
            airline=airline_name,
            flight_number=flight_iata,
            departure_iata=departure_iata,
            arrival_iata=arrival_iata
        )

    except requests.exceptions.Timeout:
        return None

    except requests.exceptions.RequestException:
        return None

    except ValueError:
        return None
```

### Expected Behavior

```text
• External API failures do not crash the program
• Missing or corrupted data results in safe route skipping
• Core loop continues processing remaining routes
```

---

## 3. Improved `DataManager` — Persistence Safety and Idempotency

### Failure Scenarios to Handle

```text
• Sheety authentication failure
• Row not found due to stale id
• Partial updates leaving inconsistent data
• Timestamp overwrite collisions
```

### Improved Update Method with Explicit Exception Handling

```python
def update_route_observation(self, row_id: int, airline: str, flight_number: str):
    """
    Updates a Google Sheet row safely and predictably.

    Persistence failures are isolated here to prevent cascading errors.
    """

    update_url = f"{self.sheety_base_url}/{row_id}"

    payload = {
        "price": {
            "airline": airline,
            "flightNumber": flight_number,
            "lastSeenAt": datetime.utcnow().isoformat()
        }
    }

    try:
        response = self.session.put(update_url, json=payload, timeout=10)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise RuntimeError("Sheety update timed out")

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"Sheety rejected update: {error}")

    except requests.exceptions.RequestException:
        raise RuntimeError("Unexpected Sheety communication failure")
```

### Why This Matters

```text
• Data corruption risks are minimized
• Errors are raised with semantic meaning
• Observability improves during debugging
```

---

## 4. Main Orchestration — Fail Soft, Not Fail Fast

### Improved Loop-Level Error Isolation

```python
for row in routes:
    try:
        flight = flight_search.observe_route(
            departure_iata=row["departureIata"],
            arrival_iata=row["arrivalIata"]
        )

        if not flight:
            continue

        data_manager.update_route_observation(
            row_id=row["id"],
            airline=flight.airline,
            flight_number=flight.flight_number
        )

        notifier.send(str(flight))

    except Exception as error:
        # Log error and continue processing remaining routes
        print(f"Route processing failed for row {row['id']}: {error}")
```

### Resulting Behavior

```text
• One failing route does not block all others
• System degrades gracefully under partial failure
• Debugging information remains visible
```

---

## 5. UX Improvement — Replacing Console Output with Twilio Notifications

### Why Messaging Improves UX Significantly

```text
Console output requires active monitoring.
Messages deliver value asynchronously and immediately.
```

---

## 6. Twilio Integration — NotificationManager Upgrade

### Environment Configuration

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890
TWILIO_TO_NUMBER=+919xxxxxxxxx
```

---

### Enhanced NotificationManager Using Twilio SMS

```python
from twilio.rest import Client
import os

class NotificationManager:
    """
    Sends flight observation notifications via SMS.
    """

    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )

        self.from_number = os.getenv("TWILIO_FROM_NUMBER")
        self.to_number = os.getenv("TWILIO_TO_NUMBER")

    def send(self, message: str):
        """
        Sends message asynchronously and isolates failures.
        """

        try:
            self.client.messages.create(
                body=f"✈️ Flight Observed\n{message}",
                from_=self.from_number,
                to=self.to_number
            )

        except Exception as error:
            print(f"Notification failed: {error}")
```

---

### Expected User-Facing Output

```text
SMS Received on Phone

✈️ Flight Observed
Air India flight AI101 from DEL to JFK
```

---

## 7. Optional Enhancements for Advanced Robustness

### Rate Limiting Protection

```text
• Add sleep delays between API calls
• Cache recent observations to avoid duplicate alerts
```

### Observability Improvements

```text
• Structured logging using logging module
• Error counters per integration
• Timestamped audit logs
```

### Architecture-Level Improvements

```text
• Replace Sheety with database when scale increases
• Introduce retry with exponential backoff
• Add health-check endpoint for cron monitoring
```

---

## 8. Reusable Improvement Blueprint for Any Automation Project

```text
1. Wrap all external API calls in try/except
2. Normalize data immediately into domain objects
3. Isolate persistence logic in one module
4. Never let notification failure block core flow
5. Prefer asynchronous user notifications
6. Log errors, continue execution, preserve data integrity
```

This approach transforms a working script into a **production-grade, user-friendly, and fault-tolerant automation system** without changing its core architecture.
