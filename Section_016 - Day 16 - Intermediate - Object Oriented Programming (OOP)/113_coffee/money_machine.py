class MoneyMachine:
    """
    Handles payment logic and profit tracking.
    """

    COINS = {
        "10rs": 10,
        "20rs": 20,
        "50rs": 50,
        "100rs": 100
    }

    def __init__(self):
        # Total money earned
        self.profit = 0

    def report(self):
        """
        Prints total profit.
        """
        print(f"Money: ₹{self.profit}")

    def make_payment(self, cost):
        """
        Processes coin input.
        Returns True if payment is successful.
        """
        print(f"Please pay ₹{cost}")
        total_paid = 0

        for coin, value in self.COINS.items():
            count = int(input(f"How many {coin}?: "))
            total_paid += count * value

        if total_paid < cost:
            print("Sorry, insufficient payment. Money refunded.")
            return False

        change = total_paid - cost
        if change > 0:
            print(f"Here is ₹{change} in change.")

        self.profit += cost
        return True
