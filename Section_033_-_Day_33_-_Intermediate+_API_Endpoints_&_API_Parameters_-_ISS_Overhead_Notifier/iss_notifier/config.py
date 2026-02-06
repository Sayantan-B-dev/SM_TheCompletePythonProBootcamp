import os
from dotenv import load_dotenv

load_dotenv()

# =======================
# EMAIL CONFIG
# =======================

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# =======================
# API ENDPOINTS
# =======================

SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"
IPINFO_ENDPOINT = "https://ipinfo.io/json"
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"
REVERSE_GEOCODE_ENDPOINT = "https://nominatim.openstreetmap.org/reverse"

# =======================
# GENERAL SETTINGS
# =======================

REQUEST_TIMEOUT = 5
ISS_PROXIMITY_DEGREES = 5
USER_AGENT = "python-iss-tracker"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
