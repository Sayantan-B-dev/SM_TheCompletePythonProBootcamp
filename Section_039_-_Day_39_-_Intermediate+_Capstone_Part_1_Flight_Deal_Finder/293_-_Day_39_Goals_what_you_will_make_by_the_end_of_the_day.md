## Overall Architectural Role Separation and Runtime Flow

This codebase is structured as a **linear observation pipeline** where each module has a single, non-overlapping responsibility, and orchestration occurs exclusively inside `main.py`.
The execution model is synchronous, deterministic, and state-light, relying on external services for persistence and observation.

> **Core execution principle:**
> *Fetch configured routes → observe live flight data → persist observation → notify output.*

---

## Module Responsibility Matrix

| Module Name               | Primary Responsibility                    | External Dependency | Mutable State             | Failure Surface                 |
| ------------------------- | ----------------------------------------- | ------------------- | ------------------------- | ------------------------------- |
| `data_manager.py`         | Google Sheet persistence and row updates  | Sheety REST API     | Requests session headers  | Network errors, schema mismatch |
| `flight_search.py`        | Real-time flight observation lookup       | Aviationstack API   | None beyond configuration | API quota, empty datasets       |
| `flight_data.py`          | Domain model for flight observations      | None                | Instance attributes only  | Invalid upstream data           |
| `notification_manager.py` | Output and notification abstraction       | Stdout only         | None                      | None                            |
| `main.py`                 | Control flow orchestration and sequencing | All modules         | Loop-local variables      | Propagated exceptions           |

---

## `DataManager` — Persistence and External State Control

### Purpose and Design Rationale

The `DataManager` class exists to **isolate all Google Sheet related concerns** from the rest of the system.
This avoids tight coupling between business logic and storage mechanisms, enabling future replacement without refactoring consumers.

### Initialization Flow and Safety Guarantees

* Environment variables are validated immediately during instantiation.
* Failure is explicit and early, preventing partial runtime execution.
* A persistent `requests.Session` is used to avoid redundant header reconfiguration.

```python
self.session.headers.update({
    "Authorization": f"Bearer {self.sheety_bearer_token}",
    "Content-Type": "application/json"
})
```

This ensures **authentication correctness** and **payload consistency** across all requests.

### `get_routes()` Behavioral Contract

* Performs a `GET` request to the Sheety endpoint.
* Assumes the response schema contains a top-level `prices` key.
* Raises immediately on HTTP failure, avoiding silent corruption.

> **Important implicit dependency:**
> The Google Sheet tab name **must** be `prices`, otherwise this method will raise a `KeyError`.

### `update_route_observation()` Update Semantics

* Constructs a row-specific URL using `row_id`.
* Updates only observation-related fields, preserving unrelated sheet data.
* Uses UTC ISO 8601 timestamps for timezone-safe auditing.

```python
"lastSeenAt": datetime.utcnow().isoformat()
```

This choice avoids locale ambiguity and ensures sortable timestamps inside Google Sheets.

---

## `FlightSearch` — External Observation Boundary

### Purpose and Data Ownership

`FlightSearch` is responsible for **reading external reality**, not storing or transforming long-term state.
Its sole responsibility is to return the **most recent observable flight** for a route.

### API Interaction Strategy

* Uses `limit=1` to reduce payload size and API cost.
* Filters by departure and arrival IATA codes directly at query level.
* Performs no retries, preserving deterministic execution time.

### `observe_route()` Edge Case Handling

| Scenario                      | Behavior              | Reasoning                                |
| ----------------------------- | --------------------- | ---------------------------------------- |
| API returns empty `data` list | Returns `None`        | Indicates no active or observable flight |
| API key missing               | Raises `RuntimeError` | Configuration error must fail fast       |
| Network or HTTP error         | Exception propagates  | Prevents partial updates                 |

This method explicitly **does not fabricate data**, ensuring downstream persistence reflects reality only.

---

## `FlightData` — Domain Model and Human Readability

### Role Within the System

`FlightData` represents a **pure domain object**, holding no persistence or transport logic.
Its primary value lies in semantic clarity and safe encapsulation of flight attributes.

### Why `__str__` Matters

```python
return (
    f"{self.airline} flight {self.flight_number} "
    f"from {self.departure_iata} to {self.arrival_iata}"
)
```

This allows the same object to be:

* Logged consistently
* Printed by notification layers
* Reused without formatting duplication

This is a **low-level design choice** that reduces string logic scattering.

---

## `NotificationManager` — Output Abstraction Layer

### Intentional Simplicity

The notification layer currently outputs to standard output only.
This abstraction exists **not for current complexity**, but for **future extensibility**.

Potential future replacements include:

* Email delivery
* SMS gateways
* Push notification services
* Messaging queues

Because consumers call only `send(message: str)`, no upstream code must change.

---

## `main.py` — Deterministic Orchestration Engine

### Execution Sequence Breakdown

1. Load environment variables before any object instantiation.
2. Construct all service objects eagerly to validate configuration.
3. Fetch all configured routes from the Google Sheet.
4. Iterate routes sequentially, avoiding concurrency complexity.
5. For each route:

   * Observe live flight data.
   * Skip silently if no observation exists.
   * Persist observation metadata.
   * Emit notification output.

### Control Flow Guarantees

* Each route is processed independently.
* A failure in one route does not implicitly skip others unless exception propagates.
* No shared mutable state exists across iterations.

---

## End-to-End Data Flow Trace

```
Google Sheet (routes)
        │
        ▼
DataManager.get_routes()
        │
        ▼
for each route row
        │
        ▼
FlightSearch.observe_route()
        │
        ├── None returned → route skipped safely
        │
        ▼
FlightData instance created
        │
        ▼
DataManager.update_route_observation()
        │
        ▼
NotificationManager.send()
        │
        ▼
Human-readable output emitted
```

This pipeline is **single-pass, side-effect controlled, and externally observable**, making it suitable for cron execution and auditability.
