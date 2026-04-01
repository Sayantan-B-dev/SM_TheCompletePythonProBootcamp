## SMS Message Construction And Practical Limitations Demonstration

SMS messages in this project must remain compact and aggressively summarized.
The following example demonstrates how information density is reduced.

```python
message_body = (
    f"Weather {summary['location']} {summary['date']}\n"
    f"Cond: {summary['current_condition']}\n"
    f"Temp: {summary['temp_min']}-{summary['temp_max']} C\n"
    f"Rain: {summary['rain_chance']}%\n"
    f"UV: {summary['uv_index']} {summary['uv_risk']}\n"
    f"Outdoor: {'Good' if summary['good_outdoor_day'] else 'Careful'}"
)
```

This structure forces abbreviation of descriptive context.
Vibe classification and astronomy details are omitted entirely.
Formatting is limited to raw line breaks without emphasis.

---

## SMS Transport Invocation And Its Constraints

SMS dispatch relies on numeric sender identification only.
Carrier routing may split messages silently if length thresholds exceed limits.

```python
client.messages.create(
    body=message_body,
    from_=TWILIO_PHONE_NUMBER,
    to=MY_PHONE_NUMBER
)
```

No delivery confirmation is consumed by the application.
Failures may occur without granular error categorization.

---

## WhatsApp Message Construction With Expanded Expressiveness

WhatsApp messaging enables expressive formatting without length restrictions.
The same weather summary can be delivered with semantic richness preserved.

```python
message_body = (
    f"🌤 *Today's Weather – {summary['location']} ({summary['date']})*\n\n"
    f"*Condition:* {summary['current_condition']}\n"
    f"*Vibe:* {summary['vibe']}\n"
    f"*Temp:* {summary['temp_min']}°C → {summary['temp_max']}°C\n"
    f"*Feels like:* {summary['feels_like_now']}°C\n"
    f"*Rain chance:* {summary['rain_chance']}%\n"
    f"*UV Index:* {summary['uv_index']} ({summary['uv_risk']})\n"
    f"*Outdoor:* {'Good to go 👍' if summary['good_outdoor_day'] else 'Be careful ⚠️'}\n\n"
    f"🌅 Sunrise: {summary['sunrise']} | 🌇 Sunset: {summary['sunset']}"
)
```

This format preserves narrative clarity and visual scanning efficiency.
Astronomical context is retained without sacrificing readability.

---

## WhatsApp Transport Invocation And Addressing Rules

WhatsApp delivery requires explicit protocol prefixing for routing.
Twilio internally distinguishes WhatsApp traffic using this prefix.

```python
client.messages.create(
    body=message_body,
    from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
    to=f"whatsapp:{MY_PHONE_NUMBER}"
)
```

This mechanism bypasses SMS carrier constraints entirely.
Delivery occurs over internet-based WhatsApp infrastructure.

---

## Shared Daily Deduplication Logic Across Transports

Both SMS and WhatsApp share identical send-once-per-day enforcement.
This prevents duplicate notifications regardless of chosen transport.

```python
def already_sent_today():
    if not os.path.exists(LAST_SENT_FILE):
        return False

    with open(LAST_SENT_FILE, "r") as f:
        last_date = f.read().strip()

    return last_date == datetime.date.today().isoformat()
```

Transport-specific logic is never duplicated unnecessarily.
Message suppression remains transport-agnostic and deterministic.

---

## Transport Selection Control Using Environment Configuration

Delivery channel selection occurs entirely through environment variables.
No code modification is required to switch messaging behavior.

```python
SMS_MODE = os.getenv("SMS_MODE", "whatsapp")

if SMS_MODE == "whatsapp":
    send_daily_weather_status_whatsapp(summary)
elif SMS_MODE == "sms":
    send_daily_weather_status(summary)
```

This design cleanly isolates transport concerns from business logic.
Weather analysis remains unchanged regardless of output channel.

---

## Practical Comparison Through Code Responsibility Separation

SMS functions prioritize brevity due to transport limitations.
WhatsApp functions prioritize clarity due to expanded capabilities.

```python
def send_daily_weather_status(summary):
    # concise transport, limited expressiveness
    pass

def send_daily_weather_status_whatsapp(summary):
    # rich transport, expressive formatting
    pass
```

Each function optimizes content for its respective medium.
This avoids compromising one channel to accommodate another.

---

## Architectural Outcome Of WhatsApp Preference

WhatsApp eliminates truncation risk present in SMS delivery.
Formatting improves user comprehension of weather conditions.
Expanded payload capacity allows inclusion of contextual insights.

The WhatsApp module therefore resolves SMS transport limitations cleanly.
