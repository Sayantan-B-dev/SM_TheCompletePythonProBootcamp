## FRONTEND–BACKEND CONNECTION MODEL

This application follows a **local client–service architecture**, where the frontend and backend are not network-separated processes but are **logically separated layers** running inside the same Python runtime.
The connection is therefore **function-call based**, not socket-based, but the responsibilities remain cleanly decoupled.

---

## HIGH-LEVEL ARCHITECTURE OVERVIEW

```
┌──────────────────────────┐
│        USER (Human)      │
└────────────┬─────────────┘
             │ keyboard input / terminal output
             ▼
┌──────────────────────────┐
│      FRONTEND LAYER      │
│      TerminalUI          │
│  (ui.py)                 │
└────────────┬─────────────┘
             │ structured data (dict, objects)
             ▼
┌──────────────────────────┐
│     BACKEND ORCHESTRATOR │
│     NutritionEngine      │
│  (engine.py)             │
└────────────┬─────────────┘
             │ outbound HTTP requests
             ▼
┌──────────────────────────┐
│ EXTERNAL SERVICES        │
│ - Nutrition API          │
│ - Sheety API             │
└──────────────────────────┘
```

The frontend never talks directly to external services, and the backend never prints or asks for input.
Their connection exists **only through well-defined method calls and data contracts**.

---

## FRONTEND RESPONSIBILITIES (ui.py)

### Role Definition

The frontend is a **presentation and interaction layer**, not a decision-making layer.
It is intentionally unaware of APIs, authentication, persistence, or business rules.

### What the frontend does

```
TerminalUI
├── get_user_input()
│   Collects raw user input from stdin
│   Normalizes optional values into Python-native types
│   Outputs a dictionary usable by backend without translation
│
├── render_results(results)
│   Accepts backend-produced domain objects
│   Converts structured data into human-readable output
│
├── info(), success(), error()
│   Purely visual feedback methods
│   No branching logic, no retries, no persistence awareness
```

### What the frontend never does

• Never builds HTTP requests
• Never handles authentication
• Never validates business rules
• Never persists data
• Never modifies ExerciseResult objects

This ensures **frontend replaceability**, meaning Tkinter or Web UI can be swapped in without backend changes.

---

## BACKEND RESPONSIBILITIES (engine.py)

### Role Definition

The backend acts as a **service layer and coordinator**, owning all business logic and integrations.

### What the backend does

```
NutritionEngine
├── health_check()
│   Ensures external dependency availability
│   Prevents wasted user interaction on downstream failure
│
├── calculate_exercise()
│   Converts human language into API-compatible payload
│   Handles optional parameter inclusion intelligently
│   Normalizes third-party API response
│   Emits domain objects instead of raw JSON
│
├── log_to_sheet()
│   Enriches data with timestamps
│   Enforces storage schema
│   Delegates persistence responsibility
```

### What the backend never does

• Never prints to terminal
• Never reads from stdin
• Never formats output for humans
• Never stores secrets internally
• Never assumes UI implementation

This ensures **backend portability**, meaning it could later be exposed as a REST API without redesign.

---

## HOW THEY ARE CONNECTED — STEP-BY-STEP FLOW

```
1. User types text into terminal
   ↓
2. TerminalUI.get_user_input()
   ↓
3. main.py passes returned dict to backend
   ↓
4. NutritionEngine.calculate_exercise(**dict)
   ↓
5. Backend returns List[ExerciseResult]
   ↓
6. Frontend renders ExerciseResult data
   ↓
7. Backend persists results via WorkoutSheet
```

**Key detail:**
The frontend does not know *how* exercise data is computed, and the backend does not know *how* results are displayed.

---

## DATA CONTRACT BETWEEN FRONTEND AND BACKEND

### Input Contract (Frontend → Backend)

```
{
    "query"      : str,
    "weight_kg"  : Optional[int],
    "height_cm"  : Optional[int],
    "age"        : Optional[int],
    "gender"     : Optional[str]
}
```

The frontend guarantees **type cleanliness**, so the backend never performs input parsing.

---

### Output Contract (Backend → Frontend)

```
ExerciseResult
├── exercise : str
├── duration : int
└── calories : float
```

The backend guarantees **semantic correctness**, so the frontend never interprets raw numbers.

---

## WHY THIS CONNECTION DESIGN IS CORRECT

> Separation is based on **responsibility**, not files or folders.

• UI changes never affect business logic
• API changes never affect user interaction
• Errors are surfaced centrally
• Testing backend logic requires no UI
• Frontend mocking is trivial

This architecture mirrors professional **MVC / Clean Architecture principles**, adapted for a single-process Python application.

---

## IF THIS WERE A NETWORKED APP (MENTAL MODEL)

```
TerminalUI  →  HTTP Client  →  NutritionEngine API
```

Your current design already matches this model, except the network hop is replaced by a direct function call, which is optimal for local execution and rapid iteration.

---

## FINAL CONNECTION SUMMARY

```
Frontend = asks, shows, formats, reacts
Backend  = decides, computes, validates, persists
Connection = pure Python data structures
Transport = function calls
Direction = unidirectional and explicit
```

No hidden coupling, no circular dependencies, no UI leakage into logic, no business rules leaking into presentation.
