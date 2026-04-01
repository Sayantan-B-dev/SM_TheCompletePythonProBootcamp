## GOOGLE SHEETS — WHAT IT ACTUALLY IS UNDER THE HOOD

**Google Sheets** is not just a grid UI; it is a **cloud-hosted, transactional document service** backed by Google’s distributed storage and exposed through the **Google Sheets API**.
Your app never touches the spreadsheet UI; it interacts indirectly through Sheety, which itself calls the Google Sheets API.

---

## THE REAL STORAGE MODEL (NOT A CSV, NOT A DATABASE)

```
Spreadsheet (Document Container)
└── Sheet / Tab (Logical Table)
    ├── Header Row (Schema Definition)
    ├── Row 2..N (Records)
    └── Cell (Atomic Value, always string-backed)
```

Key implications that affect your app’s behavior:

• There is **no enforced data type** at storage level
• Every cell is stored as a **string with metadata**
• Ordering matters visually but not semantically
• Rows are addressable by index, not primary keys

---

## HOW A SPREADSHEET BECOMES “AN API”

Google exposes spreadsheets through a **document-centric API**, not a database protocol.

```
Your App
   ↓
Sheety REST API
   ↓
Google Sheets API
   ↓
Spreadsheet Document
```

Sheety translates REST semantics into Google’s document operations.

---

## GOOGLE SHEETS API — OPERATIONAL VIEW

### What the API Actually Does

When Sheety sends a request, Google performs **document mutations**, not SQL-style inserts.

```
POST row → appendCells()
GET rows → readGridRange()
```

These operations are **transactional at document level**, meaning:

• Each request is atomic
• No partial row writes occur
• No multi-row transaction support exists

---

## SCHEMA DEFINITION — WHY HEADER ROW IS CRITICAL

Your spreadsheet header row:

```
Date | Time | Exercise | Duration | Calories
```

This row is treated as:

• Column name mapping
• JSON key reference
• Ordering guide

If you rename a header column, **Sheety breaks instantly**.
There is no schema registry elsewhere.

---

## WHAT HAPPENS WHEN YOUR APP SAVES A WORKOUT

### FULL WRITE PIPELINE — STEP BY STEP

```
1. engine.log_to_sheet()
2. WorkoutSheet.add(workout_dict)
3. HTTP POST to Sheety
4. Sheety validates bearer token
5. Sheety resolves spreadsheet + tab
6. Sheety maps JSON keys → column headers
7. Google Sheets API appendCells()
8. New row added at bottom
9. Row index assigned implicitly
10. Sheety returns created row as JSON
```

Nothing here resembles a database insert.
This is **document editing**.

---

## ROW ID — WHAT IT REALLY IS

Sheety returns:

```
"id": 12
```

This is **not a primary key**.

It represents:

• internal row index at insertion time
• unstable if rows are deleted
• unsafe to rely on long-term

Your app correctly **ignores it**, which avoids future corruption.

---

## HOW READS WORK (GET ALL)

```
WorkoutSheet.get_all()
   ↓
Sheety GET request
   ↓
Google readGridRange()
   ↓
Entire tab serialized to JSON
```

Important behavior:

• Always returns full dataset
• No server-side filtering
• No pagination guarantees
• Ordering equals sheet order

This is why Google Sheets is unsuitable for large datasets.

---

## WHY GOOGLE SHEETS FEELS “SLOW” SOMETIMES

Because operations involve:

• document locking
• revision tracking
• permission validation
• UI synchronization

Google Sheets is optimized for **collaboration**, not throughput.

Your app’s low write frequency fits this model perfectly.

---

## AUTHENTICATION — WHAT REALLY HAPPENS

You do **not** authenticate with Google directly.

```
Your App → Sheety (Bearer Token)
Sheety → Google (OAuth Service Account)
```

Sheety owns:

• OAuth tokens
• refresh cycles
• spreadsheet permissions

Your bearer token only controls **Sheety access**, not Google access.

---

## DATA TYPE REALITY — WHY YOU ROUND CALORIES

Even if you send:

```
"calories": 245
```

Google stores it as:

```
"245"
```

Type interpretation is **UI-level**, not storage-level.

This explains:

• lack of numeric constraints
• formatting inconsistencies
• necessity of explicit normalization

Your backend correctly enforces formatting before persistence.

---

## CONCURRENCY MODEL — WHAT IF TWO REQUESTS ARRIVE

Google Sheets uses **last-write-wins** per row append.

• Two inserts never overwrite each other
• Ordering depends on arrival time
• No locking for logical conflicts

For logging apps, this is acceptable.

---

## WHAT THIS MEANS FOR YOUR APP DESIGN

### Why This Works Well

• Append-only workload
• Low write frequency
• Human-readable audit trail
• Zero infrastructure management

### Why This Would Fail at Scale

• No indexing
• Full-table reads only
• No joins or aggregation
• No access control per row

---

## HOW TO THINK ABOUT GOOGLE SHEETS CORRECTLY

> “Google Sheets is a **collaborative document**, not a database.”

If you treat it like:

• PostgreSQL → you will fight it
• MongoDB → you will hit limits
• CSV storage → you will underestimate it

Your current usage treats it correctly as:

**append-only, schema-light, human-visible storage**

---

## COMPLETE SYSTEM VIEW — END TO END

```
Human Input
   ↓
TerminalUI
   ↓
NutritionEngine
   ↓
Sheety REST API
   ↓
Google Sheets API
   ↓
Spreadsheet Document
   ↓
Persistent Cloud Storage
```

Each layer adds value without leaking responsibility.

---

## WHY THIS ARCHITECTURE IS SOUND

• UI unaware of persistence
• Engine unaware of storage implementation
• Sheety isolates Google complexity
• Spreadsheet remains inspectable and editable
• Migration path remains open

This app works not because Google Sheets is powerful, but because your design **respects its constraints** and uses it exactly where it excels.
