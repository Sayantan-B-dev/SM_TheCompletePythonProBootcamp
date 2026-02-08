## Project Data Flow — Memory-Friendly, Reusable Mental Model

```text
PROJECT: Flight Observation and Logging Pipeline
PURPOSE: Observe live flights, persist observations, and notify results

┌─ main.py
│  PURPOSE
│    Central orchestrator controlling application startup and execution order
│
│  RESPONSIBILITY
│    Coordinates data retrieval, observation, persistence, and notification
│
│  FUNCTIONS
│    main()
│      PARAMETERS
│        None, relies entirely on environment configuration and imports
│
│      FLOW
│        1. Initialize DataManager for sheet persistence handling
│        2. Initialize FlightSearch for external flight observation
│        3. Initialize NotificationManager for output delivery
│        4. Retrieve configured routes from Google Sheet
│        5. Loop through each route deterministically
│        6. Observe live flight data for the route
│        7. Persist observation back into the sheet
│        8. Send human-readable notification message
│
│      OUTPUT
│        No return value, side effects include API calls, sheet updates, console output
│
├─ data_manager.py
│  PURPOSE
│    Acts as persistence boundary for Google Sheets using Sheety API
│
│  CLASS: DataManager
│
│  ├─ __init__()
│  │    PARAMETERS
│  │      None, reads SHEETY_BASE_URL and SHEETY_BEARER_TOKEN from environment
│  │
│  │    INTERNAL STATE
│  │      requests.Session with authorization and JSON headers
│  │
│  │    OUTPUT
│  │      Initialized DataManager instance or runtime failure if config missing
│
│  ├─ get_routes()
│  │    PARAMETERS
│  │      None, uses preconfigured session and base URL
│  │
│  │    INPUT SOURCE
│  │      Google Sheet rows exposed via Sheety endpoint
│  │
│  │    OUTPUT
│  │      List of route dictionaries representing sheet rows
│
│  ├─ update_route_observation(row_id, airline, flight_number)
│  │    PARAMETERS
│  │      row_id         → integer sheet row identifier
│  │      airline        → string airline name from observed flight
│  │      flight_number  → string flight IATA code
│  │
│  │    SIDE EFFECT
│  │      Updates airline, flightNumber, and lastSeenAt fields in Google Sheet
│  │
│  │    OUTPUT
│  │      None, raises exception if update fails
│
├─ flight_search.py
│  PURPOSE
│    External data acquisition layer for real-world flight observations
│
│  CLASS: FlightSearch
│
│  ├─ __init__()
│  │    PARAMETERS
│  │      None, reads AVIATIONSTACK_API_KEY from environment
│  │
│  │    OUTPUT
│  │      Initialized search client or runtime failure if key missing
│
│  ├─ observe_route(departure_iata, arrival_iata)
│  │    PARAMETERS
│  │      departure_iata → string IATA airport code for departure
│  │      arrival_iata   → string IATA airport code for arrival
│  │
│  │    INPUT SOURCE
│  │      Aviationstack REST API live flight data
│  │
│  │    DECISION LOGIC
│  │      If no flight data exists, returns None to signal safe skip
│
│  │    OUTPUT
│  │      FlightData instance representing a single observed flight
│
├─ flight_data.py
│  PURPOSE
│    Domain model representing a single flight observation
│
│  CLASS: FlightData
│
│  ├─ __init__(airline, flight_number, departure_iata, arrival_iata)
│  │    PARAMETERS
│  │      airline         → airline name string
│  │      flight_number   → IATA flight code string
│  │      departure_iata  → origin airport code string
│  │      arrival_iata    → destination airport code string
│  │
│  │    OUTPUT
│  │      Immutable domain object holding flight identity
│
│  ├─ __str__()
│  │    PURPOSE
│  │      Convert flight object into consistent human-readable message
│  │
│  │    OUTPUT
│  │      Formatted descriptive string used by notification layer
│
├─ notification_manager.py
│  PURPOSE
│    Notification abstraction layer for observed flight output
│
│  CLASS: NotificationManager
│
│  ├─ send(message)
│  │    PARAMETERS
│  │      message → string describing observed flight
│  │
│  │    CURRENT IMPLEMENTATION
│  │      Prints message to console with contextual label
│  │
│  │    FUTURE EXTENSIBILITY
│  │      Can be replaced with email, SMS, push, or logging services
│  │
│  │    OUTPUT
│  │      None, side effect is message delivery
│
└─ ENVIRONMENT VARIABLES (Implicit Input Layer)
   PURPOSE
     Secure configuration injection without code changes

   REQUIRED KEYS
     SHEETY_BASE_URL
     SHEETY_BEARER_TOKEN
     AVIATIONSTACK_API_KEY

   FAILURE MODE
     Missing variables cause immediate runtime termination
```
