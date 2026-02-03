from menu_item import MenuItem


class Menu:
    """
    Stores all available drinks and
    handles drink lookup.
    """

    def __init__(self):
        # Menu is a collection of MenuItem objects
        self.menu = [
            MenuItem("espresso", 120, {"water": 50, "coffee": 18}),
            MenuItem("latte", 180, {"water": 200, "milk": 150, "coffee": 24}),
            MenuItem("cappuccino", 200, {"water": 250, "milk": 100, "coffee": 24}),
        ]

    def get_items(self):
        """
        Returns all drink names as a single string.
        Used for user display.
        """
        return "/".join(item.name for item in self.menu)

    def find_drink(self, order_name):
        """
        Searches for a drink by name.
        Returns MenuItem if found, else None.
        """
        for item in self.menu:
            if item.name == order_name:
                return item
        return None
