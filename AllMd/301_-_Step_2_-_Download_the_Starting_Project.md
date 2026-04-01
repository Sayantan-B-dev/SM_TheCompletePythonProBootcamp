## STEP 2 — DATA ENRICHMENT AND CONTROLLED ORCHESTRATION (CODE-FIRST)

### 2.1 What STEP 2 Is Responsible For

STEP 2 takes the **clean flight dictionaries produced by STEP 1** and performs **controlled, deterministic enrichment** before persistence.
This step **does not fetch external data**, **does not modify structure**, and **does not perform I/O side effects beyond logging**.

Its only responsibilities are:

* Iterating over normalized flight records
* Adding contextual, non-critical metadata
* Maintaining strict execution observability

---

### 2.2 Code Location and Ownership

```
main.py
fun_facts.py
notification.py
```

`main.py` orchestrates
`fun_facts.py` enriches
`notification.py` observes

---

### 2.3 Entry Point Into STEP 2

```python
flights = fetch_live_flights(limit=15)
```

Explanation
At this moment, STEP 1 has already completed successfully.
`flights` is guaranteed to be a `list[dict]` with a stable schema.

---

### 2.4 Controlled Iteration Over Flight Records

```python
for index, flight in enumerate(flights, start=1):
    log(f"Processing flight {index} with IATA code {flight.get('flight_iata')}")
```

Explanation

* `enumerate(..., start=1)` provides human-friendly indexing for logs
* Logging before mutation ensures traceability even if later steps fail
* `flight` is treated as a mutable working object

Expected behavior
Each iteration represents **exactly one logical unit of work**.

---

### 2.5 Enrichment Logic — Adding Non-Critical Metadata

```python
from fun_facts import random_aviation_fact

flight["fun_fact"] = random_aviation_fact()
```

Explanation
This line performs **pure enrichment**:

* No existing keys are modified
* No required fields are overwritten
* The added key is optional and non-fatal

Design intent
If enrichment fails, the system could still persist flight data without breaking integrity.

---

### 2.6 Inside the Enrichment Function (Pure Function)

```python
def random_aviation_fact() -> str:
    return random.choice(FACTS)
```

Explanation

* No parameters → no external coupling
* No side effects → deterministic behavior per call
* Returns a simple string → storage-safe and human-readable

This function is deliberately isolated so enrichment can be:

* Disabled
* Replaced
* Expanded later

---

### 2.7 Data Shape Before vs After STEP 2

Before enrichment:

```python
{
  "flight_iata": "AI302",
  "altitude": 36000,
  "speed": 820
}
```

After enrichment:

```python
{
  "flight_iata": "AI302",
  "altitude": 36000,
  "speed": 820,
  "fun_fact": "Planes fly more efficiently at higher altitudes due to thinner air."
}
```

Explanation
The core telemetry remains untouched.
STEP 2 strictly **augments**, never mutates meaning.

---

### 2.8 What STEP 2 Explicitly Does NOT Do

* No API calls
* No Google Sheet writes
* No retries or error recovery
* No schema validation

STEP 2 assumes STEP 1 succeeded and STEP 3 will handle persistence guarantees.

---

### 2.9 Failure Characteristics of STEP 2

If STEP 2 fails:

* No external systems are affected
* No partial writes occur
* Logs clearly show the last processed flight index

This makes STEP 2 **safe, reversible, and easy to reason about**, which is exactly why enrichment is isolated here instead of being merged into ingestion or persistence.
