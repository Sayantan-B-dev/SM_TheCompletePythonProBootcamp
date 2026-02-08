class NotificationManager:
    """
    Outputs observed flight information.
    """

    def send(self, message: str):
        print("✈️ Flight Observed")
        print(message)
