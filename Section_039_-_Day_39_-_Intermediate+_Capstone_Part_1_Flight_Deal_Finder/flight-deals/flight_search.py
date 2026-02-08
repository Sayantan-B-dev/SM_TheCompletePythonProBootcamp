import requests
import os
from flight_data import FlightData

class FlightSearch:
    """
    Retrieves real flight observations from Aviationstack.
    """

    def __init__(self):
        self.api_key = os.getenv("AVIATIONSTACK_API_KEY")
        self.base_url = "https://api.aviationstack.com/v1"

        if not self.api_key:
            raise RuntimeError("AVIATIONSTACK_API_KEY missing")

    def observe_route(self, departure_iata: str, arrival_iata: str):
        params = {
            "access_key": self.api_key,
            "dep_iata": departure_iata,
            "arr_iata": arrival_iata,
            "limit": 1
        }

        response = requests.get(f"{self.base_url}/flights", params=params)
        response.raise_for_status()

        data = response.json().get("data", [])
        if not data:
            return None

        flight = data[0]

        return FlightData(
            airline=flight["airline"]["name"],
            flight_number=flight["flight"]["iata"],
            departure_iata=departure_iata,
            arrival_iata=arrival_iata
        )
