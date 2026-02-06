import requests



ipinfo_api_url="https://ipinfo.io/json"
iss_api_url="http://api.open-notify.org/iss-now.json"


def get_current_location():
    """
    Uses IP-based geolocation to determine the user's approximate location.
    Returns a dictionary with city, region, country, latitude, longitude.
    """

    try:
        # Public IP geolocation API
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()

        data = response.json()

        # Latitude and longitude are returned as "lat,long"
        lat, lon = data.get("loc", "0,0").split(",")

        location = {
            "ip": data.get("ip"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "latitude": float(lat),
            "longitude": float(lon),
            "timezone": data.get("timezone")
        }

        return location

    except Exception as e:
        raise RuntimeError(f"Failed to determine location: {e}")

def satellite_position():
    """
    Returns the current position of the ISS.
    """
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        response_data=response.json()
        return response_data
    except Exception as e:
        raise RuntimeError(f"Failed to determine satellite position: {e}")


location = get_current_location()
print("Your Latitude: "+str(location["latitude"]))
print("Your Longitude: "+str(location["longitude"]))

satellite_position = satellite_position()
print("Satellite Latitude: "+str(satellite_position["iss_position"]["latitude"]))
print("Satellite Longitude: "+str(satellite_position["iss_position"]["longitude"]))