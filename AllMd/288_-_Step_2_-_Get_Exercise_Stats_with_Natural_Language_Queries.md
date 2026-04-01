## WHAT THIS NLP API ACTUALLY IS

This is **not a generic chatbot NLP API** and not a language model like GPT.
It is a **domain-specific Natural Language Understanding service** focused exclusively on **exercise and nutrition intent extraction**.

The API’s core job is **semantic parsing**, not conversation.
It converts **free-form human workout descriptions** into **structured physiological metrics**.

---

## WHAT PROBLEM THIS API SOLVES INTERNALLY

Humans describe workouts like this:

> “I ran for 30 minutes and did 20 minutes of cycling”

Machines require this instead:

```
[
  { "exercise": "running", "duration": 30, "calories": 240 },
  { "exercise": "cycling", "duration": 20, "calories": 180 }
]
```

This API sits **between language and physiology**, performing:

• intent detection
• entity extraction
• activity classification
• duration inference
• metabolic estimation

---

## INTERNAL NLP PIPELINE (CONCEPTUAL MODEL)

```
Raw Human Text
   ↓
Text Normalization
   ↓
Intent Classification
   ↓
Exercise Entity Extraction
   ↓
Duration Resolution
   ↓
MET Lookup & Metabolic Modeling
   ↓
Calorie Estimation
   ↓
Structured JSON Output
```

You never see these stages directly, but the behavior matches this pipeline.

---

## STEP 1 — REQUEST CONSTRUCTION (YOUR SIDE)

### Endpoint Used

```
POST /v1/nutrition/natural/exercise
```

This endpoint explicitly signals **natural language processing**, meaning the API expects **unstructured human text**, not predefined exercise IDs.

---

### HTTP HEADERS — WHY EACH EXISTS

```
{
  "Content-Type": "application/json",
  "x-app-id": "...",
  "x-app-key": "..."
}
```

• `Content-Type` tells the server how to decode your payload
• `x-app-id` identifies your application
• `x-app-key` authorizes quota usage and billing

No OAuth flow exists here because this API is **service-to-service**, not user-to-user.

---

### PAYLOAD — THE SINGLE MOST IMPORTANT FIELD

```
{
  "query": "ran for 30 minutes and cycled for 20 minutes"
}
```

This `query` string is passed **verbatim** into their NLP engine.
No preprocessing is required or recommended on your side.

---

### OPTIONAL METABOLIC MODIFIERS (WHY THEY MATTER)

```
{
  "weight_kg": 70,
  "height_cm": 175,
  "age": 24,
  "gender": "male"
}
```

These parameters **do not affect language parsing**.
They affect **calorie calculation precision**.

Internally, the API adjusts MET values based on:

• basal metabolic rate
• body mass
• age-dependent efficiency
• gender-dependent energy models

If omitted, **population averages** are used.

---

## STEP 2 — WHAT THE API DOES WITH YOUR TEXT

### NLP TASKS PERFORMED INTERNALLY

#### 1. Tokenization and Normalization

The text is cleaned, lower-cased, and split into semantic tokens.

```
"ran for 30 minutes"
→ ["run", "30", "minute"]
```

---

#### 2. Exercise Intent Recognition

The engine matches verbs and nouns against an **exercise ontology**.

Examples it understands:

• running
• jogging
• sprinting
• cycling
• walking uphill
• swimming freestyle
• weight lifting
• yoga

Synonyms are aggressively mapped.

---

#### 3. Duration Extraction

Numbers combined with temporal units are bound to exercises.

```
"ran for 30 minutes"
→ duration = 30
```

If no duration is present, it attempts inference or rejects ambiguity.

---

#### 4. Activity Segmentation

Multiple activities in one sentence are split automatically.

```
"ran for 20 minutes and lifted weights for 15 minutes"
→ two independent exercise objects
```

---

#### 5. MET Assignment

Each exercise maps to a **MET (Metabolic Equivalent of Task)** value.

This is a **scientific standard**, not an AI guess.

Example:

• running ≈ 7.5 MET
• cycling ≈ 6.8 MET

---

#### 6. Calorie Computation

Calories are calculated roughly as:

```
Calories = MET × weight_kg × duration_hours
```

Adjusted by age and gender when provided.

---

## STEP 3 — RESPONSE STRUCTURE (WHAT YOU RECEIVE)

### RAW RESPONSE FORMAT

```
{
  "exercises": [
    {
      "name": "running",
      "duration_min": 30,
      "nf_calories": 245.7
    }
  ]
}
```

### IMPORTANT CHARACTERISTICS

• `name` is always lowercase and normalized
• `duration_min` is always numeric
• `nf_calories` is a float, not rounded

The API intentionally returns **raw scientific values**, leaving rounding decisions to you.

---

## STEP 4 — HOW YOUR CODE CONSUMES THIS RESPONSE

### Where the NLP Result Enters Your System

```python
for item in response.json()["exercises"]:
```

You are explicitly trusting:

• response schema stability
• consistent key naming
• list-based output

This is correct and expected for this API.

---

### Why You Convert It into `ExerciseResult`

```
ExerciseResult(
    exercise=item["name"].title(),
    duration=item["duration_min"],
    calories=item["nf_calories"],
)
```

This transformation achieves:

• UI-friendly formatting
• decoupling from vendor schema
• protection against API changes
• domain-specific typing

This is **good architecture**, not cosmetic.

---

## ERROR BEHAVIOR — WHAT HAPPENS WHEN NLP FAILS

### Typical Failure Causes

• Completely ambiguous text
• Unsupported activity description
• Missing duration with no inferable context
• Invalid authentication

### API Behavior

• Returns HTTP 4xx or 5xx
• Includes human-readable error message
• No partial success is returned

Your `raise_for_status()` is correct because partial NLP results are unsafe.

---

## HOW TO THINK ABOUT THIS API WITHOUT DOCUMENTATION

### Mental Model

> “This API is a **translator from human exercise language to physiology math**.”

You should always ask:

• Is the sentence something a human trainer would understand
• Does it clearly contain a duration
• Does it describe physical activity, not intention

If yes, the API will almost always succeed.

---

## HOW TO APPROACH THIS API PROFESSIONALLY

### Before Sending Requests

• Treat `query` as unstructured human speech
• Do not try to pre-structure or sanitize aggressively
• Always pass real numbers for body metrics

---

### When Debugging Issues

1. Log raw query string
2. Test the same query in isolation
3. Remove optional parameters to isolate issues
4. Inspect returned `exercises` list length
5. Never assume single exercise output

---

### When Extending Usage

• Accept free-form paragraphs
• Support multiple exercises per request
• Persist raw calories, round only at display time
• Store original query for audit and replay

---

## FINAL INTERNAL TRUTH ABOUT THIS API

• It is **NLP-powered**, but **domain-constrained**
• It is **deterministic**, not conversational
• It is **ontology-driven**, not generative
• It is **mathematically grounded**, not heuristic
• It expects **human language**, not structured commands

If you treat it like a language translator rather than a chatbot, everything about its behavior becomes predictable and reliable.
