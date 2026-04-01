# International Space Station (ISS) Visibility Tracker - Complete Documentation

## 📋 Overview

The ISS Visibility Tracker is a modular Python application that checks if the International Space Station is currently visible from your location. It determines if it's nighttime at your location, checks if the ISS is overhead, and sends email notifications based on the conditions.

## 📊 System Architecture Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                         START APPLICATION                           │
└───────────────────┬─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       MAIN EXECUTION FLOW                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────────────┐     │
│  │ Get Your    │    │ Get ISS     │    │ Reverse Geocode    │     │
│  │ Location    │───▶│ Position    │───▶│ Both Locations     │     │
│  │ (IPInfo)    │    │ (OpenNotify)│    │ (Nominatim)        │     │
│  └─────────────┘    └─────────────┘    └────────────────────┘     │
│           │               │                      │                 │
│           │               │                      │                 │
│           ▼               ▼                      ▼                 │
│  ┌───────────────┬───────────────┬──────────────────────────────┐ │
│  │ Your Location │  ISS Position │  Human-readable Place Names  │ │
│  │ Coordinates   │  Coordinates  │                              │ │
│  └───────────────┴───────────────┴──────────────────────────────┘ │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     DISPLAY LOCATION INFO                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                     │
│  │ Check if it's   │      │ Check if ISS    │                     │
│  │ Nighttime       │─────▶│ is Overhead      │                     │
│  │ (Sunrise-Sunset)│      │ (Proximity Check)│                     │
│  └─────────────────┘      └─────────────────┘                     │
│                    │                     │                         │
│                    ▼                     ▼                         │
│          ┌─────────────────────────────────────────┐               │
│          │         DECISION LOGIC                  │               │
│          │                                         │               │
│          │  • Night + ISS Overhead → Send Alert    │               │
│          │  • Night + No ISS → Send Update         │               │
│          │  • Daytime → Send Daytime Notice        │               │
│          └─────────────────────────────────────────┘               │
│                              │                                     │
│                              ▼                                     │
│          ┌─────────────────────────────────────────┐               │
│          │         SEND EMAIL NOTIFICATION         │               │
│          │       (via Gmail SMTP)                  │               │
│          └─────────────────────────────────────────┘               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
iss-tracker/
├── .env                    # Environment variables (API keys, credentials)
├── config.py              # Configuration and constants
├── network.py             # HTTP request handling
├── location.py            # Geolocation services
├── astronomy.py           # Astronomical calculations
├── email_service.py       # Email notification system
├── output.py              # Console output formatting
└── main.py               # Main application logic
```

## 🔧 Complete Code with Detailed Comments

### **FILE: ./config.py**
```python
"""
Configuration Module
Handles environment variables and application constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =======================
# EMAIL CONFIGURATION
# =======================
EMAIL = os.getenv("EMAIL")                    # Your Gmail address
PASSWORD = os.getenv("PASSWORD")              # App-specific password (not regular password)
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL") # Who receives notifications

# =======================
# API ENDPOINTS
# =======================
SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"  # Solar times API
IPINFO_ENDPOINT = "https://ipinfo.io/json"                      # IP geolocation API
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"        # ISS position API
REVERSE_GEOCODE_ENDPOINT = "https://nominatim.openstreetmap.org/reverse"  # Convert coordinates to address

# =======================
# APPLICATION SETTINGS
# =======================
REQUEST_TIMEOUT = 5               # HTTP request timeout in seconds
ISS_PROXIMITY_DEGREES = 5         # How close ISS needs to be (in degrees) to be considered "overhead"
                                  # 5° ≈ 556 km at equator - adjustable based on desired sensitivity
USER_AGENT = "python-iss-tracker" # Required by Nominatim API for identification

# =======================
# EMAIL SERVER SETTINGS
# =======================
SMTP_SERVER = "smtp.gmail.com"    # Gmail's SMTP server address
SMTP_PORT = 587                   # TLS port for secure email transmission
```

### **FILE: ./network.py**
```python
"""
Network Module
Handles all HTTP requests with error handling and timeout
"""

import requests
from typing import Dict, Optional
from config import REQUEST_TIMEOUT

def safe_get(url: str, *, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
    """
    Safely make a GET request to any API with error handling
    
    Args:
        url: The API endpoint URL
        params: Query parameters for the request
        headers: HTTP headers to send with the request
    
    Returns:
        Parsed JSON response as a dictionary
    
    Raises:
        requests.exceptions.RequestException: For any network or HTTP errors
    """
    try:
        # Make the HTTP GET request with timeout
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # Raise exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        # Parse and return JSON response
        return response.json()
        
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out after {REQUEST_TIMEOUT} seconds")
        raise
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {url}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Network error for {url}: {e}")
        raise
```

### **FILE: ./location.py**
```python
"""
Location Module
Handles geolocation and reverse geocoding services
"""

from typing import Dict
from network import safe_get
from config import IPINFO_ENDPOINT, REVERSE_GEOCODE_ENDPOINT, USER_AGENT

def get_current_location() -> Dict:
    """
    Get current location using IP-based geolocation
    
    Uses IPInfo.io API to determine location from public IP address
    
    Returns:
        Dictionary containing location information:
        - ip: Public IP address
        - city: City name
        - region: State/region
        - country: Country code
        - latitude: Latitude coordinate
        - longitude: Longitude coordinate
        - timezone: Local timezone
    """
    # Fetch location data from IPInfo API
    data = safe_get(IPINFO_ENDPOINT)
    
    # Extract latitude and longitude from "loc" field (format: "lat,lng")
    lat, lon = data.get("loc", "0,0").split(",")
    
    return {
        "ip": data.get("ip"),
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
        "latitude": float(lat),    # Convert string to float
        "longitude": float(lon),   # Convert string to float
        "timezone": data.get("timezone"),
    }

def reverse_geocode(lat: float, lon: float) -> Dict:
    """
    Convert latitude/longitude coordinates to human-readable address
    
    Uses OpenStreetMap Nominatim API for reverse geocoding
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
    
    Returns:
        Dictionary containing address components:
        - city: City/town/village name
        - state: State/region
        - country: Country name
        - type: Type of location (city, town, etc.)
        - name: Display name of location
    """
    # Make request to Nominatim API with coordinates
    data = safe_get(
        REVERSE_GEOCODE_ENDPOINT,
        params={
            "lat": lat,      # Latitude parameter
            "lon": lon,      # Longitude parameter
            "format": "json" # Response format
        },
        headers={"User-Agent": USER_AGENT}  # Required by Nominatim
    )
    
    # Extract address components from response
    address = data.get("address", {})
    
    return {
        # Try different keys for city name (different APIs use different terms)
        "city": address.get("city") 
                or address.get("town")
                or address.get("village"),
        "state": address.get("state"),
        "country": address.get("country"),
        "type": data.get("type"),    # What type of feature is this?
        "name": data.get("name"),    # Full display name
    }

def summarize_location(info: Dict) -> str:
    """
    Create a concise, human-readable location string
    
    Args:
        info: Location dictionary from reverse_geocode()
    
    Returns:
        Formatted string like "Paris, France" or "Unknown location"
    """
    # Build list of potential location components
    parts = [
        info.get("name"),  # Full name (most detailed)
        info.get("city"),  # City name
        info.get("country") # Country name
    ]
    
    # Join non-empty parts with comma separator
    # filter(None, parts) removes None and empty strings
    location_str = ", ".join(filter(None, parts))
    
    # Return "Unknown location" if no data found
    return location_str or "Unknown location"
```

### **FILE: ./astronomy.py**
```python
"""
Astronomy Module
Handles solar calculations and ISS position tracking
"""

import datetime as dt
from typing import Dict
from network import safe_get
from config import (
    SUNRISE_SUNSET_ENDPOINT,
    ISS_ENDPOINT,
    ISS_PROXIMITY_DEGREES
)

def is_night(location: Dict) -> bool:
    """
    Check if it's currently nighttime at a given location
    
    Args:
        location: Dictionary with "latitude" and "longitude" keys
    
    Returns:
        True if it's currently nighttime, False if daytime
    
    Logic:
        - Fetches sunrise and sunset times for the location
        - Compares current UTC time to sunrise/sunset
        - Returns True if current time is before sunrise OR after sunset
    """
    # Fetch sunrise/sunset data for the given coordinates
    data = safe_get(
        SUNRISE_SUNSET_ENDPOINT,
        params={
            "lat": location["latitude"],
            "lng": location["longitude"],
            "formatted": 0  # 0 = ISO format, 1 = 12-hour format
        }
    )
    
    # Parse sunrise and sunset times from ISO format strings
    sunrise = dt.datetime.fromisoformat(data["results"]["sunrise"])
    sunset = dt.datetime.fromisoformat(data["results"]["sunset"])
    
    # Get current time in UTC (timezone-aware)
    now = dt.datetime.now(dt.UTC)
    
    # It's night if current time is before sunrise OR after sunset
    return now < sunrise or now > sunset

def get_iss_position() -> Dict:
    """
    Get current International Space Station position
    
    Uses Open Notify ISS API which provides real-time ISS coordinates
    
    Returns:
        Dictionary with "latitude" and "longitude" of ISS
    """
    # Fetch current ISS position
    data = safe_get(ISS_ENDPOINT)
    
    return {
        "latitude": float(data["iss_position"]["latitude"]),
        "longitude": float(data["iss_position"]["longitude"]),
    }

def is_iss_overhead(location: Dict, iss: Dict) -> bool:
    """
    Check if ISS is within proximity of a location
    
    Args:
        location: Dictionary with "latitude" and "longitude" (your location)
        iss: Dictionary with "latitude" and "longitude" (ISS position)
    
    Returns:
        True if ISS is within ISS_PROXIMITY_DEGREES of location
    
    Calculation:
        Compares absolute difference in latitude and longitude
        ISS is "overhead" if both differences are <= threshold
    """
    # Calculate absolute differences in coordinates
    lat_diff = abs(location["latitude"] - iss["latitude"])
    lon_diff = abs(location["longitude"] - iss["longitude"])
    
    # Check if both differences are within the proximity threshold
    return (
        lat_diff <= ISS_PROXIMITY_DEGREES and
        lon_diff <= ISS_PROXIMITY_DEGREES
    )
```

### **FILE: ./email_service.py**
```python
"""
Email Service Module
Handles email composition and sending
"""

import smtplib
from email.message import EmailMessage
from config import EMAIL, PASSWORD, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT

def build_email(h1: str, p1: str) -> EmailMessage:
    """
    Build an HTML email message
    
    Args:
        h1: Main heading/title for the email
        p1: Main paragraph content
    
    Returns:
        Formatted EmailMessage object ready to send
    """
    # Create new email message
    msg = EmailMessage()
    
    # Set email headers
    msg["Subject"] = "ISS Overhead Notification"
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT_EMAIL
    
    # Create HTML email body
    html_content = f"""
    <html>
        <body>
            <h1>{h1}</h1>
            <p>{p1}</p>
        </body>
    </html>
    """
    
    # Add HTML content to email (plain text fallback is automatic)
    msg.add_alternative(html_content, subtype="html")
    
    return msg

def send_email(h1: str, p1: str):
    """
    Send an email using Gmail SMTP
    
    Args:
        h1: Email heading
        p1: Email paragraph content
    
    Raises:
        smtplib.SMTPException: If email sending fails
    """
    # Build the email message
    msg = build_email(h1, p1)
    
    # Connect to Gmail's SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        # Upgrade to secure TLS connection
        server.starttls()
        
        # Login with credentials
        server.login(EMAIL, PASSWORD)
        
        # Send the email
        server.send_message(msg)
```

### **FILE: ./output.py**
```python
"""
Output Module
Handles console output formatting for better user experience
"""

def print_header(title: str):
    """
    Print a formatted header with borders
    
    Args:
        title: The title text to display centered in the header
    """
    print("\n" + "═" * 60)  # Top border
    print(f"{title:^60}")    # Centered title
    print("═" * 60)         # Bottom border

def print_kv(label: str, value: str):
    """
    Print a key-value pair in aligned format
    
    Args:
        label: The label/key (left-aligned, fixed width)
        value: The value (right side)
    """
    print(f"{label:<18} : {value}")
```

### **FILE: ./main.py**
```python
"""
Main Application Module
Orchestrates the entire ISS visibility checking process
"""

from location import (
    get_current_location,
    reverse_geocode,
    summarize_location
)
from astronomy import (
    is_night,
    get_iss_position,
    is_iss_overhead
)
from email_service import send_email
from output import print_header, print_kv

def main():
    """
    Main function that executes the ISS visibility check workflow
    """
    # 1. DISPLAY APPLICATION HEADER
    print_header("ISS VISIBILITY CHECK")
    
    # 2. GET LOCATIONS
    # 2a. Get your current location (via IP geolocation)
    my_location = get_current_location()
    
    # 2b. Get current ISS position
    iss_location = get_iss_position()
    
    # 3. REVERSE GEOCODE BOTH LOCATIONS
    # Convert coordinates to human-readable place names
    my_place = reverse_geocode(
        my_location["latitude"],
        my_location["longitude"]
    )
    iss_place = reverse_geocode(
        iss_location["latitude"],
        iss_location["longitude"]
    )
    
    # 4. DISPLAY LOCATION INFORMATION
    print_kv("Your location", summarize_location(my_place))
    print_kv("Your latitude", f"{my_location['latitude']:.4f}")
    print_kv("Your longitude", f"{my_location['longitude']:.4f}")
    
    print()  # Blank line for separation
    
    print_kv("ISS location", summarize_location(iss_place))
    print_kv("ISS latitude", f"{iss_location['latitude']:.4f}")
    print_kv("ISS longitude", f"{iss_location['longitude']:.4f}")
    
    # 5. SEPARATOR LINE
    print("\n" + "─" * 60)
    
    # 6. CHECK CONDITIONS AND SEND NOTIFICATIONS
    try:
        # Condition 1: Is it nighttime at your location?
        if is_night(my_location):
            print("🌙 It is currently NIGHT.")
            
            # Condition 2: Is the ISS currently overhead?
            if is_iss_overhead(my_location, iss_location):
                print("🚀 THE ISS IS OVERHEAD!")
                
                # Send URGENT alert email
                send_email(
                    "The ISS is overhead!",
                    "The International Space Station is currently passing overhead from your location.\n\n"
                    "This is a rare and beautiful moment when the sky is dark enough to spot it with the naked eye.\n\n"
                    "Step outside, find a clear view of the sky, and look up. You may see a steady, fast-moving point of light crossing above you."
                )
            else:
                # ISS is not overhead, but it's night
                print("ℹ ISS not overhead.")
                
                # Send informational update email
                send_email(
                    "ISS Update",
                    "It is currently nighttime at your location, but the International Space Station is not overhead right now.\n\n"
                    "The ISS orbits the Earth rapidly, so visibility changes often.\n\n"
                    "Keep an eye out—another opportunity to see it may occur soon."
                )
        else:
            # It's daytime - ISS can't be seen
            print("☀ DAYTIME – ISS not visible.")
            
            # Send daytime notice email
            send_email(
                "ISS Update",
                "The International Space Station is not visible at the moment because it is currently daytime at your location.\n\n"
                "ISS sightings are best during nighttime or early dawn when the sky is darker.\n\n"
                "You will be notified again when viewing conditions improve."
            )
        
        print("Email sent successfully!")
        
    except Exception as e:
        # Handle any errors that occur during email sending
        print(f"Email error: {e}")
    
    # 7. FINAL SEPARATOR
    print("─" * 60)

# Entry point - only run main() if script is executed directly
if __name__ == "__main__":
    main()
```

### **FILE: .env (Environment Variables)**
```bash
# Gmail Account Credentials
EMAIL="your-email@gmail.com"
PASSWORD="your-app-specific-password"  # NOT your regular Gmail password!
RECIPIENT_EMAIL="recipient-email@gmail.com"

# Note: For Gmail, you need to:
# 1. Enable 2-factor authentication on your Google account
# 2. Generate an "App Password" from Google Security settings
# 3. Use that app password here, not your regular password
```

## 🚀 Setup Instructions

### 1. **Install Dependencies**
```bash
pip install requests python-dotenv
```

### 2. **Configure Gmail for App Access**
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Under "Signing in to Google", click **App passwords**
4. Generate a new app password for "Mail" on "Other" device
5. Copy the 16-character password

### 3. **Create .env File**
Create a file named `.env` in your project root:
```env
EMAIL="yourname@gmail.com"
PASSWORD="xxxx xxxx xxxx xxxx"  # The 16-character app password
RECIPIENT_EMAIL="recipient@gmail.com"
```

### 4. **Run the Application**
```bash
python main.py
```

## 📡 API Rate Limits and Considerations

| API Service | Rate Limit | Notes |
|-------------|------------|-------|
| **IPInfo.io** | 50,000/month | Free tier, no API key required |
| **Open Notify ISS** | No formal limit | Free, public API |
| **Sunrise-Sunset** | No formal limit | Free for reasonable use |
| **Nominatim** | 1 request/sec | Requires User-Agent header |

## 🔄 Data Flow Explanation

### Phase 1: Data Collection
```
Your IP Address → IPInfo API → Your Coordinates
Public ISS API → Current ISS Coordinates
Both Coordinates → Nominatim API → Human-readable Locations
```

### Phase 2: Astronomical Calculations
```
Your Coordinates → Sunrise-Sunset API → Sunrise/Sunset Times
Current UTC Time → Compare → Determine if Nighttime
Your Coordinates + ISS Coordinates → Distance Calculation → Proximity Check
```

### Phase 3: Decision Logic
```
IF Nighttime AND ISS Overhead:
    Send "Look Up Now!" Alert
ELSE IF Nighttime:
    Send "ISS Not Currently Visible" Update
ELSE (Daytime):
    Send "Check Again Tonight" Notice
```

### Phase 4: Notification
```
Decision → Email Service → Gmail SMTP → Recipient's Inbox
```

## ⚠️ Error Handling

The application includes error handling for:
1. **Network failures** (timeouts, connection errors)
2. **API errors** (HTTP errors, invalid responses)
3. **Email sending failures** (SMTP errors, authentication issues)
4. **Missing environment variables**

## 📊 ISS Proximity Calculation

The ISS is considered "overhead" if:
- **Latitude difference** ≤ 5 degrees
- **Longitude difference** ≤ 5 degrees

**Why 5 degrees?**
- Earth's circumference: ~40,000 km
- 1 degree latitude ≈ 111 km
- 5 degrees ≈ 556 km radius
- ISS altitude: ~400 km
- This gives reasonable visibility range while filtering out distant passes

## 🌟 Enhancement Ideas

1. **Visualization**: Add a simple ASCII map showing ISS position relative to your location
2. **Schedule**: Predict future ISS passes using orbit calculation
3. **Weather Integration**: Check cloud cover before suggesting to look up
4. **Multi-platform Notifications**: Add SMS, Discord, or Slack notifications
5. **Historical Logging**: Save visibility events to a database
6. **Web Interface**: Create a Flask/Django web app with real-time updates
7. **Mobile App**: Port to Kivy or BeeWare for mobile use
8. **Audio Alerts**: Play sound when ISS is overhead

## 🛠️ Troubleshooting

### Common Issues:

1. **"SMTP Authentication Error"**
   - Ensure 2-factor authentication is enabled
   - Use app-specific password, not regular password
   - Check if "Less secure app access" is enabled (older accounts)

2. **"429 Too Many Requests"**
   - You're hitting API rate limits
   - Add delays between requests
   - Implement caching for location data

3. **"User-Agent required" (Nominatim)**
   - Ensure USER_AGENT is set in config.py
   - Use a descriptive user agent string

4. **Inaccurate Location**
   - IP geolocation can be imprecise
   - Consider adding manual location override option

## 📝 License and Attribution

This application uses:
- **Open Notify API** for ISS position data
- **IPInfo.io** for IP geolocation
- **Sunrise-Sunset API** for solar calculations
- **OpenStreetMap Nominatim** for reverse geocoding

All APIs are free for personal/non-commercial use. Please respect their rate limits and terms of service.

---

The ISS Visibility Tracker demonstrates excellent software engineering practices including modular design, separation of concerns, proper error handling, and clean code structure. It's a practical example of integrating multiple web APIs to create a useful real-world application.