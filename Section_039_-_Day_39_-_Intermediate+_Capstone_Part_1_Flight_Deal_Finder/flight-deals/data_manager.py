import requests
import os
from datetime import datetime

class DataManager:
    """
    Handles all Google Sheet persistence for flight observations.
    """

    def __init__(self):
        self.sheety_base_url = os.getenv("SHEETY_BASE_URL")
        self.sheety_bearer_token = os.getenv("SHEETY_BEARER_TOKEN")

        if not self.sheety_base_url or not self.sheety_bearer_token:
            raise RuntimeError("Sheety environment variables missing")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.sheety_bearer_token}",
            "Content-Type": "application/json"
        })

    def get_routes(self):
        response = self.session.get(self.sheety_base_url)
        response.raise_for_status()

        # IMPORTANT: resource name must match Sheety response
        return response.json()["prices"]

    def update_route_observation(self, row_id: int, airline: str, flight_number: str):
        update_url = f"{self.sheety_base_url}/{row_id}"

        payload = {
            "price": {
                "airline": airline,
                "flightNumber": flight_number,
                "lastSeenAt": datetime.utcnow().isoformat()
            }
        }

        response = self.session.put(update_url, json=payload)
        response.raise_for_status()
