from typing import Dict
from network import safe_get
from config import IPINFO_ENDPOINT, REVERSE_GEOCODE_ENDPOINT, USER_AGENT

def get_current_location() -> Dict:
    data = safe_get(IPINFO_ENDPOINT)
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

def reverse_geocode(lat: float, lon: float) -> Dict:
    data = safe_get(
        REVERSE_GEOCODE_ENDPOINT,
        params={"lat": lat, "lon": lon, "format": "json"},
        headers={"User-Agent": USER_AGENT}
    )

    address = data.get("address", {})
    return {
        "city": address.get("city")
                or address.get("town")
                or address.get("village"),
        "state": address.get("state"),
        "country": address.get("country"),
        "type": data.get("type"),
        "name": data.get("name"),
    }

def summarize_location(info: Dict) -> str:
    parts = [info.get("name"), info.get("city"), info.get("country")]
    return ", ".join(p for p in parts if p) or "Unknown location"
