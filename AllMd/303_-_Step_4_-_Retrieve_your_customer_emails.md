## STEP 4 — SYSTEM GUARANTEES, FAILURE MODES, AND DESIGN CONTRACTS (PRACTICAL)

### 4.1 What STEP 4 Actually Represents

STEP 4 is **not a code execution step**.
It is the **implicit contract** that governs how the system behaves when things go right, go wrong, or go partially wrong.

Think of STEP 4 as the **rules of survival** for the pipeline.

---

### 4.2 Guaranteed Execution Order (Non-Negotiable)

```
STEP 1 → STEP 2 → STEP 3
```

Explanation

* STEP 1 must succeed before anything else is allowed
* STEP 2 assumes STEP 1 produced valid structures
* STEP 3 assumes STEP 2 finished enrichment

There is **no parallelism, no branching, no shortcuts**.

---

### 4.3 Configuration Failure Guarantee (Fail Fast)

```python
if not all([AVIATIONSTACK_API_KEY, SHEETY_BASE_URL, SHEETY_BEARER_TOKEN]):
    raise RuntimeError("One or more required environment variables are missing")
```

Behavior

* Application crashes immediately on startup
* No HTTP calls are attempted
* No partial state is created

Why this matters
A misconfigured pipeline must **never appear to work**.

---

### 4.4 Observability Guarantee (Nothing Is Silent)

```python
log("Application startup initiated")
log(f"Processing flight {index} with IATA code {flight.get('flight_iata')}")
log("Application execution completed successfully")
```

Guarantee
Every meaningful action emits a timestamped signal.

You can always answer:

* What happened
* When it happened
* Which flight caused it

---

### 4.5 Partial Data Tolerance Guarantee (Soft Failures)

```python
live_data = item.get("live") or {}
```

Behavior

* Missing telemetry does not crash ingestion
* Flights without altitude or speed still persist
* Warnings are logged instead of fatal errors

Why this matters
External APIs are unreliable, but your pipeline must remain predictable.

---

### 4.6 Hard Failure Escalation Guarantee (Writes Are Sacred)

```python
if 200 <= response.status_code < 300:
    log("Row inserted successfully")
else:
    error("Sheety request failed")
    response.raise_for_status()
```

Behavior

* Any failed write stops execution immediately
* No silent data loss
* No pretending persistence succeeded

This guarantees **data integrity over availability**.

---

### 4.7 No Hidden State Guarantee

* No global mutable caches
* No background threads
* No implicit retries
* No deferred writes

Each flight record is:

* Fetched once
* Enriched once
* Written once

If the program exits, everything stops.

---

### 4.8 Idempotency Reality Check (Important Limitation)

Current behavior

* Re-running the script inserts duplicate rows
* No deduplication by flight IATA
* No update semantics

This is **intentional**, not accidental.

Why
Idempotency requires identifiers, versioning, or reconciliation logic, which is outside the scope of a simple ingestion pipeline.

---

### 4.9 What STEP 4 Explicitly Does NOT Promise

* No retry guarantees
* No exactly-once delivery
* No transactional rollback
* No SLA on external APIs

STEP 4 promises **clarity, correctness, and debuggability**, not magic.

---

### 4.10 Mental Model to Remember Forever

```
STEP 1 = Trust nothing from outside
STEP 2 = Change nothing essential
STEP 3 = Treat writes as irreversible
STEP 4 = Fail loudly, never silently
```

If you apply this model to any future project, the architecture will remain same even as complexity grows.
