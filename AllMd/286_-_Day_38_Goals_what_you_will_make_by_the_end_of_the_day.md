## SYSTEM DATA FLOW — ASCII TREE DIAGRAM

Business logic, control flow, functions, variables, parameters, inputs, outputs, and side effects are represented explicitly and hierarchically.
Every line maintains semantic density and avoids fragmentary wording.

```
MAIN PROCESS ENTRYPOINT
└── main.py : main()
    ├── Purpose
    │   Orchestrates configuration loading, dependency wiring, execution order,
    │   user interaction, error handling, and lifecycle management.
    │
    ├── Environment Initialization
    │   ├── load_dotenv()
    │   │   Loads runtime secrets and configuration from .env file
    │   │   Input  : .env file on disk
    │   │   Output : OS environment variables populated
    │
    ├── UI Layer Construction
    │   ├── ui = TerminalUI()
    │   │   Purpose : Handles all user-facing input and output concerns
    │   │   Output  : UI abstraction instance
    │
    ├── Persistence Layer Construction
    │   ├── sheet = WorkoutSheet(base_url, bearer_token)
    │   │   Inputs
    │   │     - SHEETY_BASE_URL   : API base endpoint
    │   │     - SHEETY_BEARER_TOKEN : Authorization credential
    │   │
    │   │   Internal State
    │   │     - self.endpoint : Full REST endpoint to workouts collection
    │   │     - self.headers  : Authorization and content-type headers
    │   │
    │   │   Responsibility
    │   │     - Persist structured workout records
    │   │     - Retrieve historical workout data
    │
    ├── Business Engine Construction
    │   ├── engine = NutritionEngine(app_id, api_key, sheet)
    │   │   Inputs
    │   │     - NUTRITION_APP_ID  : API application identifier
    │   │     - NUTRITION_API_KEY : API authentication secret
    │   │     - sheet            : Persistence dependency injection
    │   │
    │   │   Internal State
    │   │     - self.headers : Authenticated API request headers
    │   │     - self.sheet   : Reference to persistence layer
    │
    │   │   Responsibility
    │   │     - External API communication
    │   │     - Domain computation and normalization
    │   │     - Delegated persistence orchestration
    │
    ├── Health Verification Phase
    │   ├── engine.health_check()
    │   │   Purpose
    │   │     - Verifies upstream API availability before user interaction
    │   │
    │   │   Input
    │   │     - HEALTH_ENDPOINT (constant)
    │   │
    │   │   Output
    │   │     - None on success
    │   │     - Raises exception on failure
    │
    ├── User Input Acquisition
    │   ├── user_data = ui.get_user_input()
    │   │   Collected Parameters
    │   │     - query      : Natural language exercise description
    │   │     - weight_kg  : Optional numeric user weight
    │   │     - height_cm  : Optional numeric user height
    │   │     - age        : Optional numeric user age
    │   │     - gender     : Optional string gender identifier
    │   │
    │   │   Output
    │   │     - Dictionary suitable for direct API payload usage
    │
    ├── Exercise Computation Phase
    │   ├── results = engine.calculate_exercise(**user_data)
    │   │
    │   │   FUNCTION: calculate_exercise()
    │   │   ├── Input Parameters
    │   │   │     - query      : Required textual exercise description
    │   │   │     - weight_kg  : Optional metabolic modifier
    │   │   │     - height_cm  : Optional metabolic modifier
    │   │   │     - age        : Optional metabolic modifier
    │   │   │     - gender     : Optional metabolic modifier
    │   │
    │   │   ├── Payload Construction Logic
    │   │   │     - Always includes "query"
    │   │   │     - Conditionally includes optional parameters only if present
    │   │
    │   │   ├── External API Call
    │   │   │     - Endpoint : /v1/nutrition/natural/exercise
    │   │   │     - Method   : POST
    │   │   │     - Headers  : Application authentication
    │   │
    │   │   ├── Response Parsing
    │   │   │     - Iterates over response["exercises"]
    │   │   │     - Normalizes capitalization and numeric types
    │   │
    │   │   ├── Output Transformation
    │   │   │     - Maps raw JSON into ExerciseResult dataclass instances
    │   │
    │   │   └── Output
    │   │         - List[ExerciseResult]
    │
    ├── Result Presentation
    │   ├── ui.render_results(results)
    │   │   Purpose
    │   │     - Displays computed exercise data in human-readable form
    │   │
    │   │   Input
    │   │     - List of ExerciseResult objects
    │
    ├── Persistence Loop
    │   ├── for each ExerciseResult in results
    │   │
    │   │   ├── engine.log_to_sheet(result)
    │   │   │
    │   │   │   FUNCTION: log_to_sheet()
    │   │   │   ├── Input
    │   │   │   │     - ExerciseResult instance
    │   │   │   │
    │   │   │   ├── Internal Data Enrichment
    │   │   │   │     - date     : Current system date
    │   │   │   │     - time     : Current system time
    │   │   │   │     - calories : Rounded integer for storage consistency
    │   │   │   │
    │   │   │   ├── Delegation
    │   │   │   │     - Calls sheet.add(workout_row)
    │   │   │   │
    │   │   │   └── Output
    │   │   │         - Dictionary representing persisted spreadsheet row
    │
    │   │   └── ui.success("Saved")
    │
    └── Error Boundary
        ├── Catches any unhandled exception in execution path
        └── Delegates formatted error display to UI layer
```

---

## DATA OBJECT DEFINITIONS — STRUCTURAL VIEW

```
ExerciseResult (dataclass)
├── exercise : str
│   Human-readable normalized exercise name
├── duration : int
│   Duration in minutes as computed by nutrition API
└── calories : float
    Raw calorie expenditure value before rounding
```

---

## PERSISTENCE LAYER — SHEETY INTERACTION FLOW

```
WorkoutSheet
├── add(workout: Dict)
│   ├── Input
│   │     - workout dictionary with strict schema mapping
│   ├── HTTP Method
│   │     - POST
│   ├── Side Effect
│   │     - Persists a new row in remote spreadsheet
│   └── Output
│         - Created workout row returned by API
│
└── get_all()
    ├── HTTP Method
    │     - GET
    ├── Purpose
    │     - Retrieve full workout history
    └── Output
          - List of workout dictionaries
```

---

## CONTROL FLOW SUMMARY — LINEAR VIEW

```
User Input
   ↓
TerminalUI.get_user_input
   ↓
NutritionEngine.calculate_exercise
   ↓
ExerciseResult objects
   ↓
TerminalUI.render_results
   ↓
NutritionEngine.log_to_sheet
   ↓
WorkoutSheet.add
   ↓
Remote Spreadsheet Persistence
```
