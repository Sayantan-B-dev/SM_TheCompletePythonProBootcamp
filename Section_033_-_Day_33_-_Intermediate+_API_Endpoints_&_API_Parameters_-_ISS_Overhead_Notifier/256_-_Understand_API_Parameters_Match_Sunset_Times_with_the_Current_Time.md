# Solar Report Application - Complete Documentation

## Overview

This Python application fetches your current location using IP geolocation, retrieves sunrise/sunset data for that location, generates a detailed solar report, and displays it in both a text file and a graphical user interface (GUI).

## Features

1. **Automatic Geolocation**: Uses your IP address to determine your location
2. **Solar Data Retrieval**: Fetches sunrise, sunset, and twilight times from the Sunrise-Sunset API
3. **Formatted Reporting**: Creates a well-structured, human-readable report
4. **File Output**: Saves the report to a UTF-8 encoded text file
5. **GUI Display**: Presents the report in a scrollable Tkinter window

## Dependencies

```python
import requests          # For HTTP requests to APIs
import datetime as dt    # For time formatting and manipulation
import tkinter as tk     # For GUI creation
from tkinter import ttk  # For themed tkinter widgets
```

## API Endpoints

```python
SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"
IPINFO_ENDPOINT = "https://ipinfo.io/json"
```

## Complete Code

```python
import requests
import datetime as dt
import tkinter as tk
from tkinter import ttk

# API Endpoints
SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"
IPINFO_ENDPOINT = "https://ipinfo.io/json"

# -------------------------------------------------
# TIME FORMATTER — UTC ISO → HUMAN-FRIENDLY STRING
# -------------------------------------------------
def format_utc_time(iso_utc_str: str) -> str:
    """
    Convert ISO format UTC time string to a human-readable format.
    
    Args:
        iso_utc_str: ISO format UTC time string (e.g., "2024-01-01T12:00:00+00:00")
    
    Returns:
        Formatted string (e.g., "Monday, 01 January 2024 at 12:00:00 PM (UTC)")
    """
    dt_obj = dt.datetime.fromisoformat(iso_utc_str)
    return dt_obj.strftime("%A, %d %B %Y at %I:%M:%S %p (UTC)")

# -------------------------------------------------
# GET LOCATION
# -------------------------------------------------
def get_current_location():
    """
    Fetch current location information using IP geolocation.
    
    Returns:
        Dictionary containing location data:
        - ip: Public IP address
        - city: City name
        - region: State/Region
        - country: Country code
        - latitude: Latitude coordinate
        - longitude: Longitude coordinate
        - timezone: Local timezone
    
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    response = requests.get(IPINFO_ENDPOINT, timeout=5)
    response.raise_for_status()
    data = response.json()
    
    # Extract latitude and longitude from "loc" field (format: "lat,lng")
    lat, lon = data.get("loc", "0,0").split(",")
    
    return {
        "ip": data.get("ip"),
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
        "latitude": float(lat),
        "longitude": float(lon),
        "timezone": data.get("timezone"),
    }

# -------------------------------------------------
# FETCH SOLAR DATA
# -------------------------------------------------
def fetch_solar_data(latitude: float, longitude: float):
    """
    Fetch sunrise/sunset data for given coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    
    Returns:
        Dictionary containing all solar data from the API
    
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    params = {
        "lat": latitude,
        "lng": longitude,
        "formatted": 0,  # Get ISO 8601 formatted times
    }
    
    response = requests.get(SUNRISE_SUNSET_ENDPOINT, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# -------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------
if __name__ == "__main__":
    # Step 1: Get current location
    try:
        my_location = get_current_location()
        print(f"Location detected: {my_location['city']}, {my_location['country']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")
        exit(1)
    
    # Step 2: Fetch solar data
    try:
        solar_data = fetch_solar_data(my_location["latitude"], my_location["longitude"])
        results = solar_data["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching solar data: {e}")
        exit(1)
    
    # Step 3: Organize solar data
    all_data = {
        "sunrise_utc": results["sunrise"],
        "sunset_utc": results["sunset"],
        "solar_noon_utc": results["solar_noon"],
        "day_length": results["day_length"],
        "civil_twilight_begin_utc": results["civil_twilight_begin"],
        "civil_twilight_end_utc": results["civil_twilight_end"],
        "nautical_twilight_begin_utc": results["nautical_twilight_begin"],
        "nautical_twilight_end_utc": results["nautical_twilight_end"],
        "astronomical_twilight_begin_utc": results["astronomical_twilight_begin"],
        "astronomical_twilight_end_utc": results["astronomical_twilight_end"],
    }
    
    # Step 4: Build the report (Single Source of Truth)
    total_info = f"""
========================================================================
LOCATION & SOLAR REPORT
========================================================================

You are currently located at latitude {my_location['latitude']} and
longitude {my_location['longitude']}. Based on IP-derived geolocation,
this corresponds to {my_location['city']}, {my_location['region']},
{my_location['country']}. Your public IP address is {my_location['ip']},
and your local timezone is {my_location['timezone']}.

------------------------------------------------------------------------
SOLAR POSITION & DAYLIGHT INFORMATION (UTC)
------------------------------------------------------------------------

Sunrise:
{format_utc_time(all_data['sunrise_utc'])}

Sunset:
{format_utc_time(all_data['sunset_utc'])}

Solar Noon:
{format_utc_time(all_data['solar_noon_utc'])}

Total Day Length:
{all_data['day_length']}

------------------------------------------------------------------------
TWILIGHT PHASES (UTC)
------------------------------------------------------------------------

Civil Twilight:
{format_utc_time(all_data['civil_twilight_begin_utc'])}
to
{format_utc_time(all_data['civil_twilight_end_utc'])}

Nautical Twilight:
{format_utc_time(all_data['nautical_twilight_begin_utc'])}
to
{format_utc_time(all_data['nautical_twilight_end_utc'])}

Astronomical Twilight:
{format_utc_time(all_data['astronomical_twilight_begin_utc'])}
to
{format_utc_time(all_data['astronomical_twilight_end_utc'])}

========================================================================
"""
    
    # Step 5: Save report to file
    try:
        with open("solar_report.txt", "w", encoding="utf-8") as file:
            file.write(total_info)
        print("Report saved to 'solar_report.txt'")
    except IOError as e:
        print(f"Error saving file: {e}")
    
    # Step 6: Create GUI to display report
    window = tk.Tk()
    window.title("Solar Report Viewer")
    window.geometry("900x650")
    
    # Create main frame
    main_frame = ttk.Frame(window, padding=10)
    main_frame.pack(fill="both", expand=True)
    
    # Create text widget for displaying the report
    text_widget = tk.Text(
        main_frame,
        wrap="word",
        font=("Consolas", 11),
        state="normal"
    )
    text_widget.pack(side="left", fill="both", expand=True)
    
    # Create scrollbar
    scrollbar = ttk.Scrollbar(
        main_frame,
        orient="vertical",
        command=text_widget.yview
    )
    scrollbar.pack(side="right", fill="y")
    
    # Connect scrollbar to text widget
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    # Insert report text
    text_widget.insert("1.0", total_info)
    text_widget.config(state="disabled")  # Make read-only
    
    # Start the GUI event loop
    window.mainloop()
```

## Data Structure

### Location Data (from IPInfo API)
```python
{
    "ip": "192.168.1.1",
    "city": "New York",
    "region": "New York",
    "country": "US",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
}
```

### Solar Data (from Sunrise-Sunset API)
```python
{
    "sunrise_utc": "2024-01-01T12:00:00+00:00",
    "sunset_utc": "2024-01-01T22:00:00+00:00",
    "solar_noon_utc": "2024-01-01T17:00:00+00:00",
    "day_length": 36000,
    "civil_twilight_begin_utc": "2024-01-01T11:30:00+00:00",
    "civil_twilight_end_utc": "2024-01-01T22:30:00+00:00",
    "nautical_twilight_begin_utc": "2024-01-01T11:00:00+00:00",
    "nautical_twilight_end_utc": "2024-01-01T23:00:00+00:00",
    "astronomical_twilight_begin_utc": "2024-01-01T10:30:00+00:00",
    "astronomical_twilight_end_utc": "2024-01-01T23:30:00+00:00"
}
```

## Installation and Usage

### Prerequisites
1. Python 3.6 or higher
2. Required packages: `requests`

### Installation
```bash
# Install required package
pip install requests

# Save the code to a file (e.g., solar_report.py)
# Run the application
python solar_report.py
```

### Output Files
1. **Console Output**: Shows progress and any errors
2. **solar_report.txt**: Text file containing the full solar report
3. **GUI Window**: Interactive window displaying the report

## Twilight Definitions

The application provides three types of twilight times:

1. **Civil Twilight**: When the sun is 6° below the horizon
   - Bright enough for outdoor activities without artificial light
   
2. **Nautical Twilight**: When the sun is 12° below the horizon
   - Horizon is still visible at sea for navigation
   
3. **Astronomical Twilight**: When the sun is 18° below the horizon
   - Sky is dark enough for astronomical observations

## Error Handling

The application includes basic error handling for:
- Network connectivity issues
- API availability problems
- File write permissions
- Invalid data formats

## Customization Options

### Modify Time Format
Change the `format_utc_time` function to use different datetime formatting:
```python
# Example: 24-hour format
return dt_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
```

### Add Local Time Conversion
```python
import pytz  # Requires: pip install pytz

def format_local_time(iso_utc_str: str, timezone_str: str):
    dt_utc = dt.datetime.fromisoformat(iso_utc_str.replace('Z', '+00:00'))
    local_tz = pytz.timezone(timezone_str)
    dt_local = dt_utc.astimezone(local_tz)
    return dt_local.strftime("%I:%M %p %Z")
```

### Customize GUI Appearance
```python
# Change fonts, colors, or window size
text_widget = tk.Text(
    main_frame,
    wrap="word",
    font=("Arial", 12),
    bg="black",
    fg="white",
    state="normal"
)
```

## Limitations

1. **IP Geolocation Accuracy**: May not be precise (typically city-level)
2. **UTC Times Only**: All times are shown in UTC, not local time
3. **No Caching**: Makes API calls every time the program runs
4. **Internet Dependency**: Requires active internet connection

## Extensions Ideas

1. **Add Caching**: Store location data to reduce API calls
2. **Historical Data**: Add date parameter for past/future solar data
3. **Local Time Display**: Convert UTC times to local timezone
4. **Visualization**: Add sunrise/sunset charts using matplotlib
5. **Multiple Locations**: Allow manual entry of coordinates
6. **Export Formats**: Add PDF or HTML export options
7. **Notifications**: Set alerts for specific solar events
8. **Dark/Light Theme**: Add theme toggle to the GUI

## API Rate Limits

- **Sunrise-Sunset API**: Free, no API key required, reasonable use expected
- **IPInfo API**: Free tier with 50,000 requests per month

## Troubleshooting

1. **No Internet Connection**: Application will fail with connection error
2. **API Changes**: If APIs update, endpoints or response formats may need adjustment
3. **Timezone Issues**: Ensure your system clock is accurate for proper time calculations
4. **Firewall Restrictions**: Some networks may block API requests

## License and Attribution

This application uses:
- **Sunrise-Sunset API**: Free API for solar data
- **IPInfo API**: Free geolocation service
- **Tkinter**: Python's standard GUI library

Always check API terms of service for usage restrictions and consider providing attribution as required.