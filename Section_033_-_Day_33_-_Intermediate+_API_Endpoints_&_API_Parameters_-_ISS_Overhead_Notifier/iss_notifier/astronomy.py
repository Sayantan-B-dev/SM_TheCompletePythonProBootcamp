import datetime as dt
from typing import Dict
from network import safe_get
from config import (
    SUNRISE_SUNSET_ENDPOINT,
    ISS_ENDPOINT,
    ISS_PROXIMITY_DEGREES
)

def is_night(location: Dict) -> bool:
    data = safe_get(
        SUNRISE_SUNSET_ENDPOINT,
        params={
            "lat": location["latitude"],
            "lng": location["longitude"],
            "formatted": 0
        }
    )

    sunrise = dt.datetime.fromisoformat(data["results"]["sunrise"])
    sunset = dt.datetime.fromisoformat(data["results"]["sunset"])
    now = dt.datetime.now(dt.UTC)

    return now < sunrise or now > sunset

def get_iss_position() -> Dict:
    data = safe_get(ISS_ENDPOINT)
    return {
        "latitude": float(data["iss_position"]["latitude"]),
        "longitude": float(data["iss_position"]["longitude"]),
    }

def is_iss_overhead(location: Dict, iss: Dict) -> bool:
    return (
        abs(location["latitude"] - iss["latitude"]) <= ISS_PROXIMITY_DEGREES and
        abs(location["longitude"] - iss["longitude"]) <= ISS_PROXIMITY_DEGREES
    )
