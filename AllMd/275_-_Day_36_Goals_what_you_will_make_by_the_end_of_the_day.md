## 1. High-Level System Flowchart (End-to-End Execution)

```
┌──────────────────────────────────────────────┐
│                Program Start                 │
│            python main.py args                │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ Parse CLI arguments                           │
│ get_news_topic() extracts news_about keyword  │
│ Default keyword applied if none provided      │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ Asset Resolution                              │
│ resolve_asset(topic)                          │
│ Maps keyword → asset type and trading symbol  │
└──────────────────────────────────────────────┘
                     │
          ┌──────────┴───────────┐
          │                      │
          ▼                      ▼
┌──────────────────────┐  ┌──────────────────────┐
│ Unknown Asset        │  │ Valid Asset           │
│ Show asset table     │  │ Continue execution    │
│ Exit program         │  └──────────────────────┘
└──────────────────────┘              │
                                      ▼
┌──────────────────────────────────────────────┐
│ Build Alpha Vantage Parameters                │
│ Stock / Crypto / Forex specific configuration │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ Fetch Market Data                             │
│ get_stock_percentage_change(stock_params)    │
│ Handles rate limits, errors, invalid payloads │
└──────────────────────────────────────────────┘
                     │
          ┌──────────┴───────────┐
          │                      │
          ▼                      ▼
┌──────────────────────┐  ┌──────────────────────────────┐
│ Market Data Failure  │  │ Valid Percentage Change      │
│ Print error          │  │ Evaluate change threshold    │
└──────────────────────┘  └──────────────────────────────┘
                                      │
                          ┌───────────┴────────────┐
                          │                        │
                          ▼                        ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│ Change ≤ 5%                  │   │ Change > 5%                  │
│ Print percentage only        │   │ Fetch related news articles  │
│ Show available assets        │   │ Render news panels           │
└──────────────────────────────┘   │ Send WhatsApp alert (cooldown)│
                                   └──────────────────────────────┘
```

---

## 2. Logical Architecture Diagram (Module Interaction View)

```
              ┌───────────────┐
              │   main.py     │
              │ Orchestration │
              └───────┬───────┘
                      │
   ┌──────────────────┼───────────────────┐
   │                  │                   │
   ▼                  ▼                   ▼
┌───────────┐   ┌───────────┐     ┌──────────────┐
│ assets.py │   │ stocks.py │     │   news.py    │
│ keyword → │   │ market    │     │ fetch news   │
│ symbol    │   │ movement  │     │ articles     │
└────┬──────┘   └────┬──────┘     └────┬─────────┘
     │               │                 │
     ▼               ▼                 ▼
┌───────────┐   ┌───────────┐   ┌──────────────┐
│  ui.py    │   │ config.py │   │ article.py   │
│ tables    │   │ env + io  │   │ render panels│
└───────────┘   └───────────┘   └──────────────┘
                                      │
                                      ▼
                             ┌────────────────┐
                             │ whatsapp.py    │
                             │ alert delivery │
                             └────────────────┘
```

---

## 3. Project Tree With Responsibilities and Function-Level Purpose

```
.
├── main.py
│   ├── get_news_topic()
│   │   • Purpose: Parse command-line arguments for news keyword.
│   │   • Parameters: None, reads from sys.argv.
│   │   • Output: String keyword representing asset topic.
│   │
│   ├── Global execution logic
│   │   • Purpose: Central decision engine coordinating all modules.
│   │   • Inputs: CLI args, resolved asset type, API responses.
│   │   • Outputs: Console output, optional WhatsApp notification.
│
├── assets.py
│   ├── ASSET_MAP
│   │   • Purpose: Human-friendly keyword to trading symbol mapping.
│   │   • Structure: Dictionary[str, str].
│   │
│   ├── resolve_asset(topic)
│   │   • Purpose: Identify asset class and normalized trading symbol.
│   │   • Parameters: topic (str user keyword).
│   │   • Output: Tuple(asset_type, symbol) or (None, None).
│
├── stocks.py
│   ├── TIME_SERIES_MAP
│   │   • Purpose: Declarative schema describing Alpha Vantage payloads.
│   │
│   ├── get_stock_percentage_change(stock_params)
│   │   • Purpose: Fetch and compute daily percentage price change.
│   │   • Parameters: stock_params (dict of Alpha Vantage query params).
│   │   • Output: Float percentage value or None on failure.
│   │   • Behavior: Handles throttling, API errors, malformed payloads.
│
├── news.py
│   ├── get_news_data(news_params, render=True, limit=3)
│   │   • Purpose: Retrieve and optionally display news articles.
│   │   • Parameters:
│   │       - news_params (dict query parameters)
│   │       - render (bool controlling output rendering)
│   │       - limit (int maximum number of articles)
│   │   • Output: List of article dictionaries.
│
├── article.py
│   ├── _parse_datetime(iso_str)
│   │   • Purpose: Normalize ISO timestamps into readable UTC strings.
│   │   • Parameters: iso_str (string timestamp from API).
│   │   • Output: Human-readable datetime string.
│   │
│   ├── render_article(article, index=None)
│   │   • Purpose: Visually format a single news article using rich Panel.
│   │   • Parameters:
│   │       - article (dict from News API)
│   │       - index (optional numbering)
│   │   • Output: Printed console panel, no return value.
│
├── ui.py
│   ├── show_available_assets()
│   │   • Purpose: Display all supported asset keywords and symbols.
│   │   • Parameters: None.
│   │   • Output: Rich table printed to console.
│
├── whatsapp.py
│   ├── _can_send()
│   │   • Purpose: Enforce alert cooldown using local timestamp lock.
│   │   • Parameters: None.
│   │   • Output: Boolean permission flag.
│   │
│   ├── _mark_sent()
│   │   • Purpose: Persist last sent timestamp to disk.
│   │   • Parameters: None.
│   │   • Output: Side-effect file write.
│   │
│   ├── send_whatsapp_alert(message)
│   │   • Purpose: Send WhatsApp alert via Twilio with rate limiting.
│   │   • Parameters: message (str).
│   │   • Output: Boolean success or failure state.
│
├── config.py
│   ├── console
│   │   • Purpose: Shared rich Console instance for consistent output.
│   │
│   ├── Environment configuration
│   │   • Purpose: Centralized API keys and endpoint management.
│   │   • Output: Constants consumed by all modules.
```

---

## 4. Conceptual Model Summary (Mental Model View)

```
User Intent
   ↓
Keyword Abstraction Layer (assets.py)
   ↓
Market Data Engine (stocks.py)
   ↓
Decision Threshold Logic (main.py)
   ↓
Information Amplification
   ├── News Context (news.py + article.py)
   └── Alert Channel (whatsapp.py)
   ↓
Human-Readable Terminal UI (rich based rendering)
```

This system behaves as a **reactive market signal amplifier**, where raw numerical movement is only escalated into narrative context and notifications once a defined volatility condition is met, preventing noise while preserving situational awareness.
