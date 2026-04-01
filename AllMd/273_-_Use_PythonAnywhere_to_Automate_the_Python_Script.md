## Deployment Goal And Execution Model Definition

The project is designed as a batch-style execution application.
It performs weather data retrieval, analysis, optional notification dispatch, then exits.
There is no requirement for a continuously running server process.
This enables cost-efficient cloud deployment using scheduled execution models.

---

## Supported Cloud Execution Patterns Overview

The application can be deployed using multiple cloud paradigms.
Each paradigm satisfies different operational and cost constraints.

The most suitable patterns include the following options:

* Scheduled CI runner based execution
* Serverless function with time-based trigger
* Lightweight virtual machine with cron scheduler

The choice depends on cost tolerance, persistence needs, and operational control.

---

## Option One: GitHub Actions Scheduled Execution Model

### Architectural Fit And Operational Characteristics

GitHub Actions is suitable for short-lived scheduled tasks.
It provides managed Python runtime environments automatically.
Secrets management is integrated and secure by default.
No infrastructure provisioning or billing setup is required.

Filesystem state does not persist between executions.
Daily deduplication must rely on external storage or messaging idempotency.

---

### Repository Structure Requirements

The repository must contain a dependency declaration file.
This file ensures deterministic environment setup during execution.

```txt
requests
python-dotenv
twilio
rich
```

All application modules must be committed to the repository.
Environment-specific values must remain excluded from version control.

---

### Secrets And Environment Variable Configuration

Secrets must be defined using repository-level configuration.
Each secret maps directly to a runtime environment variable.

Required secrets include the following values:

* API_KEY used for weather service authentication
* API_ENDPOINT defining the weather service endpoint
* TWILIO_ACCOUNT_SID for Twilio account identification
* TWILIO_AUTH_TOKEN for secure Twilio authentication
* TWILIO_PHONE_NUMBER used for SMS sending
* TWILIO_WHATSAPP_NUMBER used for WhatsApp sending
* MY_PHONE_NUMBER defining the message recipient
* APP_MODE controlling execution entrypoint
* SMS_MODE selecting SMS or WhatsApp transport

These secrets are injected automatically during job execution.

---

### Scheduled Workflow Definition Example

Create a workflow file located at `.github/workflows/weather.yml`.

```yaml
name: Daily Weather Automation

on:
  schedule:
    - cron: "0 6 * * *"

jobs:
  run-weather:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python runtime
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Execute weather application
        env:
          API_KEY: ${{ secrets.API_KEY }}
          API_ENDPOINT: ${{ secrets.API_ENDPOINT }}
          TWILIO_ACCOUNT_SID: ${{ secrets.TWILIO_ACCOUNT_SID }}
          TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
          TWILIO_PHONE_NUMBER: ${{ secrets.TWILIO_PHONE_NUMBER }}
          TWILIO_WHATSAPP_NUMBER: ${{ secrets.TWILIO_WHATSAPP_NUMBER }}
          MY_PHONE_NUMBER: ${{ secrets.MY_PHONE_NUMBER }}
          APP_MODE: sms
          SMS_MODE: whatsapp
        run: |
          python main.py
```

This workflow executes daily at a fixed UTC time.
The application terminates automatically after completion.

---

## Option Two: AWS Lambda With EventBridge Scheduler

### Architectural Fit And Execution Characteristics

AWS Lambda supports event-driven execution with strict runtime limits.
The application runtime must complete within the Lambda timeout window.
Ephemeral filesystem storage is available under the `/tmp` directory.

Daily deduplication must be implemented using persistent storage such as S3.

---

### Code Adaptation Requirements For Lambda

The entrypoint must be converted into a handler function.
Environment variables are injected through Lambda configuration.

```python
def lambda_handler(event, context):
    from app.entrypoints.sms import main
    main()
    return {"status": "completed"}
```

The application logic remains unchanged internally.

---

### EventBridge Scheduled Trigger Configuration

An EventBridge rule defines the execution schedule.
Cron expressions control invocation timing precisely.

```text
cron(0 6 * * ? *)
```

This rule invokes the Lambda function daily.
Timezones must be configured explicitly if required.

---

## Option Three: Cloud Virtual Machine With Cron Scheduler

### Architectural Fit And Persistence Characteristics

A virtual machine provides full filesystem persistence.
Daily cache and lock files persist across executions naturally.
This model offers maximum control at higher operational cost.

---

### VM Setup And Runtime Configuration

Install Python and system dependencies manually.
Clone the application repository onto the server.
Configure environment variables using a `.env` file.

```bash
export APP_MODE=sms
export SMS_MODE=whatsapp
```

---

### Cron Job Configuration Example

Configure cron to execute the application daily.

```bash
0 6 * * * /usr/bin/python3 /home/app/main.py >> weather.log 2>&1
```

This ensures predictable execution with persistent logging.

---

## Comparative Summary Of Deployment Approaches

GitHub Actions offers simplicity and zero cost for public repositories.
AWS Lambda offers scalability and managed scheduling with some complexity.
Virtual machines offer persistence and control with higher maintenance.

The application architecture supports all three without refactoring.
Deployment choice depends on persistence requirements and cost sensitivity.
