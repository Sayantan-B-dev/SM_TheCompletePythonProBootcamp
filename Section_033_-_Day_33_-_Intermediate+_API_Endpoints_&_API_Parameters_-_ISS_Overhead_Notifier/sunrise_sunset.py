import requests
import datetime as dt
import tkinter as tk
from tkinter import ttk
# If tkinter is not installed, run: pip install tk
# If requests is not installed, run: pip install requests

SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"
IPINFO_ENDPOINT = "https://ipinfo.io/json"


# -------------------------------------------------
# TIME FORMATTER — UTC ISO → HUMAN-FRIENDLY STRING
# -------------------------------------------------
def format_utc_time(iso_utc_str: str) -> str:
    dt_obj = dt.datetime.fromisoformat(iso_utc_str)
    return dt_obj.strftime("%A, %d %B %Y at %I:%M:%S %p (UTC)")


# -------------------------------------------------
# GET LOCATION
# -------------------------------------------------
def get_current_location():
    response = requests.get(IPINFO_ENDPOINT, timeout=5)
    response.raise_for_status()
    data = response.json()

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
# FETCH DATA
# -------------------------------------------------
my_location = get_current_location()

params = {
    "lat": my_location["latitude"],
    "lng": my_location["longitude"],
    "formatted": 0,
}

response = requests.get(SUNRISE_SUNSET_ENDPOINT, params=params, timeout=10)
response.raise_for_status()
data = response.json()

all_data = {
    "sunrise_utc": data["results"]["sunrise"],
    "sunset_utc": data["results"]["sunset"],
    "solar_noon_utc": data["results"]["solar_noon"],
    "day_length": data["results"]["day_length"],
    "civil_twilight_begin_utc": data["results"]["civil_twilight_begin"],
    "civil_twilight_end_utc": data["results"]["civil_twilight_end"],
    "nautical_twilight_begin_utc": data["results"]["nautical_twilight_begin"],
    "nautical_twilight_end_utc": data["results"]["nautical_twilight_end"],
    "astronomical_twilight_begin_utc": data["results"]["astronomical_twilight_begin"],
    "astronomical_twilight_end_utc": data["results"]["astronomical_twilight_end"],
}


# -------------------------------------------------
# BUILD REPORT (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------
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


# -------------------------------------------------
# SAVE REPORT TO FILE (UTF-8 SAFE)
# -------------------------------------------------
with open("solar_report.txt", "w", encoding="utf-8") as file:
    file.write(total_info)


# -------------------------------------------------
# TKINTER UI — DISPLAY REPORT
# -------------------------------------------------
window = tk.Tk()
window.title("Solar Report Viewer")
window.geometry("900x650")

main_frame = ttk.Frame(window, padding=10)
main_frame.pack(fill="both", expand=True)

text_widget = tk.Text(
    main_frame,
    wrap="word",
    font=("Consolas", 11),
    state="normal"
)
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(
    main_frame,
    orient="vertical",
    command=text_widget.yview
)
scrollbar.pack(side="right", fill="y")

text_widget.configure(yscrollcommand=scrollbar.set)

text_widget.insert("1.0", total_info)
text_widget.config(state="disabled")

window.mainloop()
