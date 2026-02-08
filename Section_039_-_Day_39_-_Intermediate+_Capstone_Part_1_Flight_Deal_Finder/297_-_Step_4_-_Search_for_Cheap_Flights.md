## Core Interaction Model — How `FlightSearch`, `FlightData`, and `DataManager` Work Together

```text
GOAL
Observe real-world flight data, normalize it, and persist the observation safely.

RULE
Each component owns exactly one responsibility and never overlaps concerns.
```

---

## High-Level Data Flow Overview

```text
Route definition (Google Sheet)
        │
        ▼
FlightSearch  ── observes reality ──► FlightData
        │                                │
        │                                ▼
        └──────────────► DataManager ── persists observation
```

This flow is **one-directional**, **explicit**, and **non-circular**, which is why it scales well to other projects.

---

## `FlightSearch` — External Reality Reader

### What `FlightSearch` Is Responsible For

```text
• Talking to Aviationstack
• Asking precise questions about flights
• Returning either real data or explicit absence
• Never storing anything permanently
```

### What `FlightSearch` Does NOT Do

```text
• Does not update Google Sheets
• Does not format output messages
• Does not decide business rules
```

### Input → Output Contract

```text
INPUT
  departure_iata : string
  arrival_iata   : string

PROCESS
  Query Aviationstack with filters applied at API level

OUTPUT
  FlightData instance OR None
```

### Internal Logic Flow

```text
observe_route()
  ├─ Build query parameters
  ├─ Send HTTP GET request
  ├─ Parse JSON response
  ├─ If no data exists → return None
  └─ If data exists → create FlightData object
```

---

## `FlightData` — Domain Representation Layer

### Why `FlightData` Exists

```text
APIs return messy, deeply nested JSON.
Applications need clean, meaningful objects.
```

`FlightData` is the **translation boundary** between external data chaos and internal clarity.

### What `FlightData` Contains

```text
• airline name
• flight number
• departure airport code
• arrival airport code
```

### What `FlightData` Does NOT Know

```text
• Where the data came from
• How the data will be stored
• Who will read the data
```

### Constructor Contract

```text
INPUT
  airline         : string
  flight_number   : string
  departure_iata  : string
  arrival_iata    : string

OUTPUT
  Immutable domain object representing one observed flight
```

### Why `__str__()` Matters

```text
FlightData → string conversion is centralized.

Result
  • No duplicate formatting logic
  • Consistent human-readable output
  • Safe reuse across logging and notifications
```

---

## `DataManager` — Persistence and State Authority

### What `DataManager` Owns

```text
• Google Sheet persistence
• Sheety API communication
• Authentication and headers
• Timestamp consistency
```

### What `DataManager` Does NOT Do

```text
• Does not fetch flight data
• Does not interpret flight meaning
• Does not decide when updates happen
```

### Input → Output Contract

```text
INPUT
  row_id         : integer
  airline        : string
  flight_number  : string

PROCESS
  Update exactly one Google Sheet row

OUTPUT
  None, but persistent state is modified
```

---

## How All Three Work Together — Step-by-Step

```text
1. main.py retrieves route rows from DataManager
2. For each route, FlightSearch is asked to observe
3. FlightSearch queries Aviationstack
4. Aviationstack returns live data or nothing
5. FlightSearch converts raw data into FlightData
6. FlightData travels back to main.py
7. main.py passes FlightData fields to DataManager
8. DataManager updates the corresponding sheet row
```

---

## Interaction Diagram — ASCII Tree View

```text
main.py
 ├─ calls DataManager.get_routes()
 │    └─ returns list of route dictionaries
 │
 ├─ loop over each route
 │    ├─ calls FlightSearch.observe_route(dep, arr)
 │    │    ├─ queries Aviationstack API
 │    │    ├─ if no data → returns None
 │    │    └─ if data → returns FlightData
 │    │
 │    ├─ FlightData object received
 │    │    ├─ airline
 │    │    ├─ flight_number
 │    │    ├─ departure_iata
 │    │    └─ arrival_iata
 │    │
 │    └─ calls DataManager.update_route_observation()
 │         ├─ builds Sheety PUT request
 │         ├─ updates Google Sheet row
 │         └─ stores timestamped observation
 │
 └─ notification emitted using FlightData.__str__()
```

---

## Why This Separation Is Architecturally Correct

```text
FlightSearch answers: “What exists right now?”
FlightData answers:   “What does this data mean?”
DataManager answers: “Where does this data live permanently?”
```

No class answers more than one question.

---

## Reusable Pattern for Any Future Project

```text
External API Client     →   Domain Object     →   Persistence Manager
(read-only, volatile)      (clean, stable)       (stateful, controlled)
```

### Example Replacements Without Code Restructuring

```text
Aviationstack → Weather API
FlightData    → WeatherData
Sheety        → PostgreSQL or Firebase
```

The interaction pattern remains unchanged, which is the key long-term benefit of this design.
