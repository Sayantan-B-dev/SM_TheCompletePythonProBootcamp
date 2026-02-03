class MenuItem:
    """
    Represents a single drink item.
    Immutable definition of a coffee.
    """

    def __init__(self, name, cost, ingredients):
        # Name of the drink (e.g. espresso)
        self.name = name

        # Cost in rupees
        self.cost = cost

        # Required ingredients dictionary
        # Example: {"water": 50, "coffee": 18}
        self.ingredients = ingredients
