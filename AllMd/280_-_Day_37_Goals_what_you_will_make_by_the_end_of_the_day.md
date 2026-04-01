## Pixela — Conceptual Overview and Purpose

Pixela is a lightweight habit-tracking and quantitative self-measurement service designed around the idea of *daily pixels*. Each pixel represents a numeric value associated with a specific date, and these pixels are rendered visually on a graph resembling a GitHub-style contribution chart. The system is intentionally minimalistic, focusing on consistency, temporal data, and visual reinforcement rather than complex analytics or social features.

At its core, Pixela answers a single question repeatedly and reliably: **“What numeric value did you produce today for this habit?”**
This design choice makes Pixela especially suitable for habits such as workouts, study hours, reading pages, commits, meditation minutes, or any activity that can be expressed as a daily integer or float.

---

## Core Architecture of Pixela

Pixela follows a **REST-based client–server model** where all interactions occur through HTTP requests. There is no SDK requirement, no authentication handshake complexity, and no persistent session state maintained by the client.

### Fundamental Concepts

| Concept | Meaning in Pixela                           | How it appears in your project |
| ------- | ------------------------------------------- | ------------------------------ |
| User    | A Pixela account identified by a username   | `PIXELA_USERNAME`              |
| Token   | A secret API token acting as authentication | `PIXELA_TOKEN`                 |
| Graph   | A single habit or metric visualization      | `PIXELA_GRAPH_ID`              |
| Pixel   | One data point for one date                 | Added via `add_pixel`          |
| Date    | The x-axis key for each pixel               | `YYYYMMDD` format              |

Pixela intentionally avoids relational complexity. A user owns graphs, graphs own pixels, and pixels are immutable per date unless explicitly updated or deleted.

---

## Authentication and Security Model

Pixela uses **token-based authentication** via a custom HTTP header.

```text
Header Name: X-USER-TOKEN
Header Value: <your-secret-token>
```

There is no OAuth flow, no refresh token logic, and no user session. This means:

* Every request must include the token
* Token leakage immediately compromises the account
* Environment variables are the correct storage mechanism

Your project correctly enforces this through `.env` loading inside `Config`, ensuring secrets never appear in source code.

---

## Pixela API Lifecycle as Implemented in This Project

### 1. User Creation (Idempotent by Design)

```python
self.client.create_user()
```

This call creates a Pixela user if it does not already exist. Pixela returns an error if the user exists, which your project intentionally ignores.

**Design reasoning:**
User creation is treated as *idempotent setup*, not a runtime operation. Errors are swallowed because an existing user is an acceptable state.

---

### 2. Graph Creation (Habit Definition)

```python
self.client.create_graph(
    graph_id=self.graph_id,
    name="Daily Habit",
    unit="count",
    graph_type="int",
    color="shibafu",
)
```

A graph defines:

* **What is being measured** (`name`)
* **How it is measured** (`unit`, `type`)
* **How it looks visually** (`color`)

Pixela graphs are immutable in structure after creation, which enforces discipline and prevents schema drift.

---

### 3. Pixel Operations (Daily Habit Actions)

Pixela enforces *one pixel per graph per date*. This constraint is central to its philosophy.

#### Add Pixel

```python
add_pixel(graph_id, date, quantity)
```

* Creates a new data point for the given date
* Fails if the pixel already exists

#### Update Pixel

```python
update_pixel(graph_id, date, quantity)
```

* Modifies an existing pixel
* Used when correcting mistakes or revising data

#### Delete Pixel

```python
delete_pixel(graph_id, date)
```

* Removes the pixel entirely
* Leaves the graph visually empty for that date

Your `HabitManager` cleanly abstracts these operations into semantic actions: add, update, delete — without exposing HTTP or Pixela details to the UI layer.

---

## Date Handling Strategy

Pixela requires dates in strict `YYYYMMDD` format.

```python
def _today(self) -> str:
    return datetime.now().strftime("%Y%m%d")
```

This choice ensures:

* No timezone ambiguity within a single local environment
* Predictable daily behavior
* Alignment with Pixela’s backend validation

An important implication is that *habit tracking is local-time dependent*, which is acceptable for personal tracking but relevant if extended to multi-timezone usage.

---

## Error Handling Philosophy in This Project

### Error Taxonomy

Your project defines a clear exception hierarchy:

* `HabitTrackerError` → base domain error
* `PixelaAPIError` → API-level failures
* `NetworkError` → transport or connectivity issues
* `ConfigurationError` → missing environment setup

This separation allows UI logic to respond differently to user errors, API throttling, and misconfiguration.

---

### Pixela Rate Limiting Reality

Pixela’s free tier applies **non-deterministic throttling**, typically manifesting as HTTP `503` responses.

Your UI explicitly handles this:

* Detects status code `503`
* Shows a user-friendly rate-limit warning
* Prevents repeated spamming through a `_rate_warned` guard
* Temporarily blocks UI actions to avoid cascading failures

This is a pragmatic, user-centered solution to an unreliable external constraint.

---

## UI and UX Integration with Pixela

### Graph Visualization Strategy

Pixela does not embed graphs directly. Instead, it exposes a static HTML endpoint:

```text
https://pixe.la/v1/users/<username>/graphs/<graph_id>.html
```

Your project leverages this by:

* Constructing the URL dynamically
* Opening it in the system browser
* Avoiding iframe embedding or HTML parsing

This keeps the desktop application lightweight while still benefiting from Pixela’s visualization engine.

---

## Separation of Responsibilities in the Project

| Layer          | Responsibility                                      |
| -------------- | --------------------------------------------------- |
| `PixelaClient` | Raw HTTP communication and response validation      |
| `HabitManager` | Domain-level habit operations and business intent   |
| `AppWindow`    | UI orchestration, user feedback, blocking, warnings |
| `HabitForm`    | Input capture and button wiring                     |
| `GraphView`    | External visualization access                       |
| `Config`       | Secure configuration loading and validation         |

This mirrors a clean architecture approach, making Pixela replaceable without rewriting UI or business logic.

---

## Why Pixela Works Well for This Use Case

Pixela’s constraints are not limitations; they are design enforcements that align with habit formation principles.

* One value per day enforces consistency
* Visual streaks reinforce behavior
* No analytics avoids over-optimization
* Simple API minimizes maintenance burden

Your project leverages Pixela exactly as intended: as a *visual accountability engine*, not a data warehouse.

---

## Practical Mental Model for Working With Pixela

> A Pixela graph is a calendar.
> Each date can contain exactly one number.
> Your job as a client is simply to decide what that number should be today.

Everything else in the API exists to support that single invariant.
