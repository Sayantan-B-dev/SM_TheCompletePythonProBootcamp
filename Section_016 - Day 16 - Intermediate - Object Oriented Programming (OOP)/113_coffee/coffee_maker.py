class CoffeeMaker:
    """
    Manages machine resources and coffee preparation.
    """

    def __init__(self):
        # Initial machine resources
        self.resources = {
            "water": 1000,
            "milk": 800,
            "coffee": 500
        }

    def report(self):
        """
        Prints current resource status.
        """
        print("Water :", self.resources["water"], "ml")
        print("Milk  :", self.resources["milk"], "ml")
        print("Coffee:", self.resources["coffee"], "g")

    def is_resource_sufficient(self, drink):
        """
        Checks whether enough resources exist for the drink.
        Returns True if possible, False otherwise.
        """
        for item, amount in drink.ingredients.items():
            if self.resources.get(item, 0) < amount:
                print(f"Sorry, not enough {item}.")
                return False
        return True

    def make_coffee(self, drink):
        """
        Deducts ingredients and prepares coffee.
        """
        for item, amount in drink.ingredients.items():
            self.resources[item] -= amount

        print(f"Here is your {drink.name}. Enjoy ☕")
