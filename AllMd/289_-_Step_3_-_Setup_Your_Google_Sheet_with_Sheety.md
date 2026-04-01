## WHAT SHEETY IS IN THIS PROJECT

**Sheety** is acting as a **Backend-as-a-Service layer** that exposes a Google Spreadsheet as a **RESTful JSON API**, allowing your Python application to persist and retrieve structured data without managing a database, server, or ORM.

In your project, Sheety is not an auxiliary tool.
It **is the database layer**, abstracted behind HTTP.

---

## WHY SHEETY EXISTS (THE PROBLEM IT SOLVES)

Traditional persistence requires:

• database setup
• schema migrations
• authentication handling
• hosting and backups
• CRUD boilerplate code

Sheety replaces all of that by:

> Turning a spreadsheet into a secure, authenticated REST endpoint.

For small to medium projects, logging systems, trackers, prototypes, and learning architectures, this is an **extremely pragmatic backend choice**.

---

## SHEETY’S CORE CONCEPTUAL MODEL

```
Google Spreadsheet
   ↓
Sheet (tab)
   ↓
Row (record)
   ↓
Column (field)
   ↓
JSON Object
   ↓
REST Endpoint
```

Sheety performs a **lossless mapping** between spreadsheet rows and JSON documents.

---

## HOW SHEETY IS USED IN *YOUR* PROJECT

### Spreadsheet Schema (Source of Truth)

```
Date | Time | Exercise | Duration | Calories
```

This schema is **authoritative**.
Sheety dynamically builds its API behavior directly from this header row.

There is no separate schema definition anywhere else.

---

## ENDPOINT STRUCTURE USED BY YOUR APP

```
{SHEETY_BASE_URL}/myWorkouts(sayantan)/workouts
```

### Decomposed Meaning

```
SHEETY_BASE_URL        → Your Sheety project base
myWorkouts(sayantan)  → Spreadsheet name
workouts              → Sheet (tab) name
```

Sheety internally resolves this path to a specific Google Sheet and tab.

---

## AUTHENTICATION MODEL USED

### Bearer Token Authentication

```
Authorization: Bearer <TOKEN>
```

This is **service-level authentication**, not user-level authentication.

### Implications

• Every request is trusted equally
• No per-user permission model exists
• Token grants full access to the sheet
• Token leakage equals full compromise

This is acceptable for:

• personal tools
• learning projects
• internal utilities

Not suitable for multi-tenant public apps.

---

## WORKOUTSHEET CLASS — WHY IT EXISTS

### Architectural Role

`WorkoutSheet` is a **persistence adapter**, not business logic.

It isolates:

• endpoint construction
• authentication headers
• HTTP request details
• response parsing

From the rest of the system.

This prevents Sheety-specific logic from leaking into your engine or UI.

---

## ADD OPERATION — FULL DATA FLOW

### Step-by-step Breakdown

```
engine.log_to_sheet()
   ↓
WorkoutSheet.add(workout)
   ↓
HTTP POST request
   ↓
Sheety API
   ↓
Google Spreadsheet row insertion
```

### Payload Sent

```json
{
  "workout": {
    "date": "07/02/2026",
    "time": "21:45:12",
    "exercise": "Running",
    "duration": 30,
    "calories": 245
  }
}
```

### Why the `workout` Wrapper Exists

Sheety requires the **root object key** to match the sheet name in singular form.

```
Sheet name : workouts
Root key   : workout
```

This is how Sheety maps JSON keys to spreadsheet columns.

---

## RESPONSE FROM SHEETY — WHAT IT RETURNS

```json
{
  "workout": {
    "id": 12,
    "date": "07/02/2026",
    "time": "21:45:12",
    "exercise": "Running",
    "duration": 30,
    "calories": 245
  }
}
```

### Important Observations

• Sheety injects an `id` field automatically
• Column order does not matter
• Data types are loosely enforced
• All values are stored as strings internally

Your code correctly ignores the `id`, which keeps your domain clean.

---

## GET OPERATION — FULL DATA FLOW

### Step-by-step Breakdown

```
WorkoutSheet.get_all()
   ↓
HTTP GET request
   ↓
Sheety API
   ↓
Spreadsheet row serialization
   ↓
JSON list returned
```

### Response Shape

```json
{
  "workouts": [
    { "date": "...", "time": "...", "exercise": "...", ... },
    { "date": "...", "time": "...", "exercise": "...", ... }
  ]
}
```

This allows:

• building history views
• analytics
• charts
• audits

Without any schema translation.

---

## WHAT SHEETY DOES INTERNALLY (ABSTRACT VIEW)

```
HTTP Request
   ↓
Authentication Check
   ↓
Endpoint → Sheet Resolution
   ↓
JSON ↔ Column Mapping
   ↓
Google Sheets API Call
   ↓
Response Normalization
```

Sheety is effectively a **proxy and transformer** over Google Sheets.

---

## LIMITATIONS YOU MUST UNDERSTAND

### Data Integrity Limitations

• No strict typing enforcement
• No transactions
• No foreign keys
• No constraints or indexes

This is why your backend rounds calories and formats dates explicitly.

---

### Performance Limitations

• Not suitable for high-frequency writes
• Latency depends on Google Sheets API
• No batch insert optimization

Acceptable for logging, not for analytics-heavy workloads.

---

### Security Limitations

• Single bearer token access
• No row-level permissions
• No user authentication

Mitigation requires putting a real backend in front of Sheety.

---

## WHY YOUR CURRENT USAGE IS CORRECT

Your project uses Sheety **exactly as intended**:

• as a persistence backend
• with strict schema discipline
• behind an abstraction layer
• without leaking vendor logic

This keeps future migration trivial.

---

## HOW TO THINK ABOUT SHEETY WITHOUT DOCUMENTATION

### Correct Mental Model

> “Sheety is a REST façade over Google Sheets, not a database engine.”

If you treat it like:

• PostgreSQL → you will break things
• Firebase → you will overestimate features
• CSV storage → you will underutilize it

---

## HOW YOU WOULD MIGRATE AWAY LATER

Because of your architecture, replacing Sheety would require:

```
Replace WorkoutSheet
Keep NutritionEngine
Keep UI
```

No refactor of business logic or frontend required.

That alone proves the design choice was sound.

---

## FINAL ROLE SUMMARY IN YOUR PROJECT

```
TerminalUI     → Human interaction
NutritionEngine → Business logic and computation
WorkoutSheet   → Persistence abstraction
Sheety         → External storage service
Spreadsheet    → Actual data store
```

Sheety is not “just saving data”.
It is functioning as a **stateless, schema-driven backend service**, and your code is already treating it with the correct level of respect and isolation.
