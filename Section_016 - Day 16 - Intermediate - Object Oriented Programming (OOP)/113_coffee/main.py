from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


def line():
    print("=" * 40)


def main():
    # Object construction
    menu = Menu()
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()

    machine_on = True

    print("WELCOME TO THE COFFEE MACHINE")
    line()

    while machine_on:
        options = menu.get_items()
        choice = input(
            f"What would you like? ({options})\n"
            "Type 'report' to view status or 'off' to turn off:\n"
        ).lower()

        line()

        if choice == "off":
            print("Turning off machine.")
            machine_on = False

        elif choice == "report":
            coffee_maker.report()
            money_machine.report()

        else:
            drink = menu.find_drink(choice)

            if drink is None:
                print("Invalid selection.")
                continue

            if not coffee_maker.is_resource_sufficient(drink):
                continue

            if not money_machine.make_payment(drink.cost):
                continue

            coffee_maker.make_coffee(drink)

        line()


# Program entry point
if __name__ == "__main__":
    main()
