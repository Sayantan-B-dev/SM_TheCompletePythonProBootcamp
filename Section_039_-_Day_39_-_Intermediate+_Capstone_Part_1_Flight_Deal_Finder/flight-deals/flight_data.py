class FlightData:
    """
    Represents a single observed flight instance.
    """

    def __init__(
        self,
        airline: str,
        flight_number: str,
        departure_iata: str,
        arrival_iata: str
    ):
        self.airline = airline
        self.flight_number = flight_number
        self.departure_iata = departure_iata
        self.arrival_iata = arrival_iata

    def __str__(self):
        return (
            f"{self.airline} flight {self.flight_number} "
            f"from {self.departure_iata} to {self.arrival_iata}"
        )
