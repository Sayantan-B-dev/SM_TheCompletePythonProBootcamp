## COFFEE MACHINE — OBJECT-ORIENTED PROJECT

**Complete Technical Documentation**

---

## 1. Project Overview

This project simulates a **multi-product coffee vending machine** using **Object-Oriented Programming (OOP)** principles in Python.

The system:

* Offers multiple coffee types
* Checks ingredient availability
* Handles coin-based payments
* Tracks machine resources and profit
* Separates responsibilities into well-defined objects

The design intentionally avoids:

* Global variables
* Procedural coupling
* Hard-to-extend logic

---

## 2. Design Philosophy

### Core Principles Applied

| Principle             | How It’s Applied                                   |
| --------------------- | -------------------------------------------------- |
| Encapsulation         | Each class owns and protects its data              |
| Single Responsibility | One job per class                                  |
| Loose Coupling        | Objects interact via methods, not shared state     |
| High Cohesion         | Related logic stays together                       |
| Extensibility         | New drinks or features added without breaking code |

---

## 3. Project Directory Structure

```
coffee_machine/
│
├── main.py
├── menu_item.py
├── menu.py
├── coffee_maker.py
└── money_machine.py
```

Each file contains **one primary class or role**.

---

## 4. System Architecture (High-Level)

```
User
 ↓
Menu  →  MenuItem
 ↓
CoffeeMaker
 ↓
MoneyMachine
```

* `Menu` handles *what can be ordered*
* `CoffeeMaker` handles *whether it can be made*
* `MoneyMachine` handles *whether it can be paid for*
* `main.py` orchestrates collaboration

---

## 5. File-by-File Documentation

---

## 5.1 `menu_item.py`

### Purpose

Represents a **single drink definition**.

### Why It Exists

* Centralizes drink data
* Prevents scattered ingredient logic
* Allows drinks to be treated as objects

### Class: `MenuItem`

#### Attributes

| Attribute     | Type   | Description          |
| ------------- | ------ | -------------------- |
| `name`        | `str`  | Drink name           |
| `cost`        | `int`  | Price in rupees      |
| `ingredients` | `dict` | Required ingredients |

#### Code

```python
class MenuItem:
    """
    Represents a single drink item.
    Immutable definition of a coffee.
    """

    def __init__(self, name, cost, ingredients):
        self.name = name
        self.cost = cost
        self.ingredients = ingredients
```

---

## 5.2 `menu.py`

### Purpose

Stores and manages all available drinks.

### Why It Exists

* Abstracts menu lookup logic
* Avoids hard-coded dictionaries in `main.py`
* Returns `MenuItem` objects instead of raw data

### Class: `Menu`

#### Methods

| Method             | Description                           |
| ------------------ | ------------------------------------- |
| `get_items()`      | Returns all drink names               |
| `find_drink(name)` | Returns matching `MenuItem` or `None` |

#### Code

```python
from menu_item import MenuItem


class Menu:
    """
    Stores all available drinks and
    handles drink lookup.
    """

    def __init__(self):
        self.menu = [
            MenuItem("espresso", 120, {"water": 50, "coffee": 18}),
            MenuItem("latte", 180, {"water": 200, "milk": 150, "coffee": 24}),
            MenuItem("cappuccino", 200, {"water": 250, "milk": 100, "coffee": 24}),
        ]

    def get_items(self):
        return "/".join(item.name for item in self.menu)

    def find_drink(self, order_name):
        for item in self.menu:
            if item.name == order_name:
                return item
        return None
```

---

## 5.3 `coffee_maker.py`

### Purpose

Manages machine ingredients and coffee preparation.

### Why It Exists

* Central authority for resource state
* Prevents invalid coffee preparation
* Owns all inventory logic

### Class: `CoffeeMaker`

#### Internal State

| Resource | Unit |
| -------- | ---- |
| Water    | ml   |
| Milk     | ml   |
| Coffee   | g    |

#### Methods

| Method                          | Responsibility         |
| ------------------------------- | ---------------------- |
| `report()`                      | Prints resource status |
| `is_resource_sufficient(drink)` | Validates availability |
| `make_coffee(drink)`            | Deducts resources      |

#### Code

```python
class CoffeeMaker:
    """
    Manages machine resources and coffee preparation.
    """

    def __init__(self):
        self.resources = {
            "water": 1000,
            "milk": 800,
            "coffee": 500
        }

    def report(self):
        print("Water :", self.resources["water"], "ml")
        print("Milk  :", self.resources["milk"], "ml")
        print("Coffee:", self.resources["coffee"], "g")

    def is_resource_sufficient(self, drink):
        for item, amount in drink.ingredients.items():
            if self.resources.get(item, 0) < amount:
                print(f"Sorry, not enough {item}.")
                return False
        return True

    def make_coffee(self, drink):
        for item, amount in drink.ingredients.items():
            self.resources[item] -= amount
        print(f"Here is your {drink.name}. Enjoy ☕")
```

---

## 5.4 `money_machine.py`

### Purpose

Handles all payment logic and profit tracking.

### Why It Exists

* Isolates financial responsibility
* Makes payment system replaceable
* Tracks earnings safely

### Class: `MoneyMachine`

#### Coin System

| Coin  | Value |
| ----- | ----- |
| 10rs  | ₹10   |
| 20rs  | ₹20   |
| 50rs  | ₹50   |
| 100rs | ₹100  |

#### Methods

| Method               | Description       |
| -------------------- | ----------------- |
| `report()`           | Prints profit     |
| `make_payment(cost)` | Validates payment |

#### Code

```python
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
        self.profit = 0

    def report(self):
        print(f"Money: ₹{self.profit}")

    def make_payment(self, cost):
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
```

---

## 5.5 `main.py`

### Purpose

Controls **program flow** and object collaboration.

### Why It Exists

* Keeps logic readable
* Avoids mixing UI with business logic
* Acts as the application controller

### Execution Flow

```
Initialize objects
↓
Ask user input
↓
Validate choice
↓
Check resources
↓
Process payment
↓
Make coffee
```

#### Code

```python
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


def line():
    print("=" * 40)


def main():
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
            "Type 'report' or 'off':\n"
        ).lower()

        line()

        if choice == "off":
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


if __name__ == "__main__":
    main()
```

---

## 6. Error Handling & Edge Cases

| Case                   | Handling             |
| ---------------------- | -------------------- |
| Invalid drink          | Menu returns `None`  |
| Insufficient resources | Coffee blocked       |
| Insufficient payment   | Refund issued        |
| Change required        | Calculated correctly |
| Shutdown               | Clean exit           |

---

## 7. Extensibility Guide

### Add a New Drink

* Add a `MenuItem` in `Menu.__init__`

### Add New Resource

* Extend `CoffeeMaker.resources`
* Update drink ingredient dictionaries

### Change Payment System

* Modify `MoneyMachine` only
* No changes required elsewhere

---

## 8. Key Takeaway Architecture Rule

> **No object knows more than it needs to.**

This keeps the system:

* Predictable
* Testable
* Maintainable
* Professional-grade

---

This documentation fully explains the **design, structure, logic, and extensibility** of the OOP coffee machine project.
