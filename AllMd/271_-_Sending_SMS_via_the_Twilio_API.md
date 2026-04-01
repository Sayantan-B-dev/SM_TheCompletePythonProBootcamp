## Twilio Role Within Application Architecture

Twilio functions as the outbound messaging transport layer for weather notifications.
It is exclusively responsible for SMS and WhatsApp message delivery.
No weather computation or decision logic exists inside Twilio-related modules.
Twilio is treated as an external side-effect system.

The application uses Twilio only after weather data analysis completes.
All messages are derived from the normalized weather summary object.
Twilio never receives raw API responses or forecast JSON structures.

---

## Twilio Integration Location and Module Responsibility

The Twilio integration exists entirely inside `app/services/reminder.py`.
No other module imports or depends on Twilio directly.
This enforces strict separation between business logic and infrastructure concerns.

The reminder service acts as a delivery adapter.
It converts summary data into transport-specific message formats.

---

## Environment Configuration and Credential Management

Twilio credentials are loaded exclusively from environment variables.
Hardcoded secrets are intentionally avoided for security reasons.

The required environment variables include the following values:

* `TWILIO_ACCOUNT_SID` identifying the Twilio account
* `TWILIO_AUTH_TOKEN` acting as the secret authentication credential
* `TWILIO_PHONE_NUMBER` used as the SMS sender number
* `TWILIO_WHATSAPP_NUMBER` used as the WhatsApp sender identity
* `MY_PHONE_NUMBER` representing the recipient destination

The dotenv loader initializes these values at runtime.
Missing or incorrect values will cause runtime authentication failures.

---

## Twilio Client Initialization and Lifecycle

The Twilio REST client is instantiated once at module import time.
The client is created using account SID and authentication token.

```python
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
```

This client object is reused across all message-sending functions.
No client pooling or reconnection logic is implemented.

---

## Daily Message Deduplication Strategy

Twilio message sending is guarded by a filesystem-based daily lock.
This mechanism prevents duplicate weather notifications within a single day.

The file `data/txt/last_sms.txt` stores the last successful send date.
Dates are stored in ISO format using the local system timezone.

If the stored date equals today’s date, sending is skipped.
This logic applies equally to SMS and WhatsApp messages.

---

## SMS Message Sending Workflow

The SMS sending function performs a strict sequence of steps.

First, it checks whether a message was already sent today.
Second, it constructs a compact plain-text weather summary message.
Third, it dispatches the message using the Twilio client.
Fourth, it records the successful send date locally.

```python
client.messages.create(
    body=message_body,
    from_=TWILIO_PHONE_NUMBER,
    to=MY_PHONE_NUMBER
)
```

The function returns a boolean indicating send success or suppression.

---

## WhatsApp Message Sending Workflow

The WhatsApp sending function mirrors the SMS logic structure.
The primary difference lies in message formatting and sender address.

WhatsApp messages use markdown-style emphasis and emoji symbols.
The sender number must be prefixed with `whatsapp:`.

```python
client.messages.create(
    body=message_body,
    from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
    to=f"whatsapp:{MY_PHONE_NUMBER}"
)
```

Twilio routes the message through its WhatsApp Business integration.

---

## Message Content Composition Rules

Message bodies are derived from the analyzed weather summary only.
No live API calls occur during message composition.

Included data fields typically include:

* Location name and forecast date
* Current condition description and vibe classification
* Temperature range and feels-like temperature
* Rain probability and UV risk classification
* Outdoor suitability indicator
* Sunrise and sunset times

Formatting differs between SMS and WhatsApp for readability.

---

## Execution Control and Mode Selection

The messaging functionality is triggered through `APP_MODE=sms`.
An additional environment variable `SMS_MODE` selects transport type.

Valid SMS_MODE values include:

* `sms` for standard text messaging
* `whatsapp` for WhatsApp delivery

Invalid values raise a runtime exception immediately.

---

## Step-by-Step Twilio Setup Guide

### Step One: Create a Twilio Account

Visit the Twilio console website and create a new account.
Verify email address and phone number during onboarding.

### Step Two: Retrieve Account Credentials

Navigate to the Twilio dashboard console.
Copy the Account SID and Auth Token securely.

Never expose these credentials inside source code repositories.

### Step Three: Purchase or Activate Phone Numbers

Purchase an SMS-capable phone number from the Twilio console.
Enable messaging capabilities for the selected number.

For WhatsApp usage, activate the Twilio WhatsApp sandbox.

### Step Four: Configure WhatsApp Sandbox

Join the Twilio WhatsApp sandbox using provided instructions.
Send the join code from your phone to the sandbox number.

Confirm successful sandbox connection inside the Twilio console.

### Step Five: Configure Environment Variables

Create a `.env` file in the project root directory.
Add all required Twilio credentials and phone numbers.

Example configuration format:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=+14155238886
MY_PHONE_NUMBER=+919XXXXXXXXX
```

Ensure country codes are included in all phone numbers.

### Step Six: Install Required Dependencies

Install the Twilio Python SDK using pip.

```bash
pip install twilio
```

Ensure dotenv is installed for environment loading.

### Step Seven: Validate Messaging Execution

Run the application with `APP_MODE=sms`.
Set `SMS_MODE` to either `sms` or `whatsapp`.

Observe console output confirming send status.

---

## Error Handling and Operational Constraints

Twilio errors propagate as runtime exceptions by default.
No retry or exponential backoff logic is implemented.
Network failures will interrupt execution immediately.

Daily deduplication relies entirely on local filesystem state.
Deleting the lock file will re-enable message sending.

---

## Architectural Intent and Design Boundaries

Twilio integration is intentionally minimal and explicit.
The system favors predictability over abstraction complexity.
All Twilio logic remains isolated from weather computation layers.

This design allows easy replacement of Twilio with another provider.
