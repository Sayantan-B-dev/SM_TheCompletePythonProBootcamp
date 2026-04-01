### ✅ BEST FREE WAY (ZERO SERVER, ZERO BILL): **GitHub + GitHub Actions**

Runs **once per day**, fully free, reliable, no VM, no Docker, no credit card.

---

## OPTION 1 — GITHUB ACTIONS (RECOMMENDED)

### WHY THIS IS IDEAL

* Free forever (public repo)
* Built-in scheduler (cron)
* Perfect for small Python jobs
* No server management
* Secure secrets handling

---

## STEP 1 — PUSH PROJECT TO GITHUB

Project root **must look like this**:

```
.
├── data/
├── logic/
├── mail/
├── templates/
├── main.py
├── requirements.txt
```

Create `requirements.txt`:

```
pandas
python-dotenv
```

---

## STEP 2 — REMOVE `.env` FROM CLOUD USAGE

GitHub **will NOT use `.env`**

Instead:

* EMAIL and PASSWORD go into **GitHub Secrets**

⚠️ Your code is already correct — it reads from environment variables.

---

## STEP 3 — ADD GITHUB SECRETS

Go to:

```
Repo → Settings → Secrets and variables → Actions
```

Add secrets:

| Name       | Value        |
| ---------- | ------------ |
| `EMAIL`    | your gmail   |
| `PASSWORD` | app password |

⚠️ Use **Gmail App Password**, not real password.

---

## STEP 4 — ADD SCHEDULER FILE

Create file:

```
.github/workflows/birthday.yml
```

```yaml
name: Birthday Email Scheduler

on:
  schedule:
    # Runs every day at 00:00 UTC
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  run-birthday-bot:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run birthday script
        env:
          EMAIL: ${{ secrets.EMAIL }}
          PASSWORD: ${{ secrets.PASSWORD }}
        run: |
          python main.py
```

---

## STEP 5 — TIMEZONE (IMPORTANT)

GitHub cron runs in **UTC**

If you are in India (IST = UTC+5:30):

| Desired IST Time | Cron         |
| ---------------- | ------------ |
| 5:30 AM IST      | `0 0 * * *`  |
| 6:00 AM IST      | `30 0 * * *` |
| 9:00 AM IST      | `30 3 * * *` |

Example (9 AM IST):

```
30 3 * * *
```

---

## STEP 6 — TEST MANUALLY

Click:

```
Actions → Birthday Email Scheduler → Run workflow
```

Check logs:

* Emails sent
* Or "No birthdays today"

---

## WHAT HAPPENS DAILY (IN CLOUD)

1. GitHub spins up a Linux machine
2. Installs Python
3. Installs dependencies
4. Runs `main.py`
5. Machine is destroyed
6. Cost = ₹0

---

## SECURITY MODEL (VERY IMPORTANT)

* Secrets are encrypted
* Not visible in logs
* Not in repo
* Not accessible to forks

---

## OPTION 2 — PythonAnywhere (FREE)

### How it works

* Upload files
* Add scheduled task (daily)
* Free tier allows daily jobs

### Downsides

* Manual setup
* Less automation
* Limited CPU

---

## OPTION 3 — Railway / Render

❌ NOT IDEAL

* Free tier expires
* Credit card often required
* Sleep policies break schedulers

---

## RECOMMENDED FINAL ARCHITECTURE

```
GitHub Repo
 └── GitHub Actions (cron)
      └── Python VM (temporary)
           └── Run main.py
                ├── Read CSV
                ├── Filter birthdays
                ├── Build email
                └── Send SMTP
```

---

## COMMON PITFALLS (READ CAREFULLY)

1. Gmail blocks login → use **App Password**
2. Wrong cron timezone
3. Forgetting `requirements.txt`
4. `.env` not used in cloud
5. Public repo exposing email list (use private if needed)

---

## IF YOU WANT NEXT

* Add logging to file
* Add retry logic
* Add WhatsApp / Telegram alerts
* Add birthday images
* Add Google Sheets instead of CSV
* Add unit tests
* Convert to Docker (optional)

Say which one you want next.
