from dotenv import load_dotenv
load_dotenv()

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

def main():
    data_manager = DataManager()
    flight_search = FlightSearch()
    notifier = NotificationManager()

    routes = data_manager.get_routes()

    for row in routes:
        flight = flight_search.observe_route(
            departure_iata=row["departureIata"],
            arrival_iata=row["arrivalIata"]
        )

        if not flight:
            continue

        data_manager.update_route_observation(
            row_id=row["id"],
            airline=flight.airline,
            flight_number=flight.flight_number
        )

        notifier.send(str(flight))

if __name__ == "__main__":
    main()
