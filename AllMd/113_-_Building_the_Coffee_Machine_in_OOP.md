## OOP REFACTORING OF THE COFFEE MACHINE SYSTEM

---

## 1. System Goal (Reframed in OOP Terms)

> Build a coffee machine where **responsibilities are distributed across objects**, not functions and globals.

Each object:

* Owns its data
* Enforces its own rules
* Collaborates with other objects

---

## 2. High-Level Object Decomposition (Bigger Picture)

| Responsibility            | Object                         |
| ------------------------- | ------------------------------ |
| Drink definition          | `MenuItem`                     |
| Menu lookup               | `Menu`                         |
| Resource tracking & usage | `CoffeeMaker`                  |
| Payment & money handling  | `MoneyMachine`                 |
| Application flow          | `CoffeeMachineApp` (or `main`) |

This removes:

* Global state
* Cross-function dependencies
* Tight coupling

---

## 3. Algorithm (Step-by-Step, OOP-Oriented)

```
START
│
├─ Create Menu object
├─ Create CoffeeMaker object
├─ Create MoneyMachine object
│
└─ LOOP while machine is ON
    │
    ├─ Display available drinks (Menu)
    ├─ Ask user for order
    │
    ├─ IF order == "report"
    │   ├─ CoffeeMaker.report()
    │   └─ MoneyMachine.report()
    │
    ├─ ELSE IF order == "off"
    │   └─ STOP machine
    │
    ├─ ELSE
    │   ├─ Menu.find_drink(order)
    │   ├─ IF drink not found → error
    │   │
    │   ├─ CoffeeMaker.is_resource_sufficient(drink)
    │   ├─ IF False → continue
    │   │
    │   ├─ MoneyMachine.make_payment(drink.cost)
    │   ├─ IF False → continue
    │   │
    │   └─ CoffeeMaker.make_coffee(drink)
    │
END
```

---

## 4. Flowchart (Text-Based)

```
        ┌──────────────┐
        │  Start App   │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Show Menu    │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ User Input   │
        └───┬─────┬───┘
            │     │
     ┌──────▼─┐ ┌─▼────────┐
     │ report │ │ off       │
     └──────┬─┘ └────┬─────┘
            │        │
   ┌────────▼───┐    │
   │ print data │    │
   └────────────┘    │
                     │
                ┌────▼─────┐
                │ shutdown │
                └──────────┘

Else (drink selected):
→ find_drink
→ check resources
→ take payment
→ make coffee
```

---

## 5. Pseudocode (Clean, Language-Neutral)

```
menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

while machine_on:
    display menu.get_items()
    choice = input()

    if choice == "report":
        coffee_maker.report()
        money_machine.report()

    else if choice == "off":
        break

    else:
        drink = menu.find_drink(choice)

        if drink is None:
            print("Invalid selection")
            continue

        if not coffee_maker.is_resource_sufficient(drink):
            continue

        if not money_machine.make_payment(drink.cost):
            continue

        coffee_maker.make_coffee(drink)
```

---

## 6. Objects and Their Responsibilities (Final Design)

---

### 6.1 `MenuItem` Class

**Purpose**

* Represents a single drink
* Immutable definition object

**Attributes**

* `name: str`
* `cost: float`
* `ingredients: dict`

```python
class MenuItem:
    """
    Models a drink item.
    Owns its name, cost, and required ingredients.
    """

    def __init__(self, name, cost, ingredients):
        self.name = name
        self.cost = cost
        self.ingredients = ingredients
```

---

### 6.2 `Menu` Class

**Purpose**

* Holds all available drinks
* Performs lookup

**Methods**

* `get_items()`
* `find_drink(order_name)`

```python
class Menu:
    """
    Stores and manages menu items.
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

### 6.3 `CoffeeMaker` Class

**Purpose**

* Owns machine resources
* Controls resource usage

**Methods**

* `report()`
* `is_resource_sufficient(drink)`
* `make_coffee(order)`

```python
class CoffeeMaker:
    """
    Manages resources and coffee preparation.
    """

    def __init__(self):
        self.resources = {
            "water": 1000,
            "milk": 800,
            "coffee": 500
        }

    def report(self):
        for item, amount in self.resources.items():
            print(f"{item.title()}: {amount}")

    def is_resource_sufficient(self, drink):
        for item, amount in drink.ingredients.items():
            if self.resources.get(item, 0) < amount:
                print(f"Sorry, not enough {item}")
                return False
        return True

    def make_coffee(self, order):
        for item, amount in order.ingredients.items():
            self.resources[item] -= amount
        print(f"Here is your {order.name} ☕")
```

---

### 6.4 `MoneyMachine` Class

**Purpose**

* Handles coins
* Tracks profit
* Validates payment

**Methods**

* `report()`
* `make_payment(cost)`

```python
class MoneyMachine:
    """
    Handles payment processing and profit tracking.
    """

    COIN_VALUES = {
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
        total_paid = 0

        for coin, value in self.COIN_VALUES.items():
            count = int(input(f"How many {coin}?: "))
            total_paid += count * value

        if total_paid < cost:
            print("Sorry that's not enough money. Money refunded.")
            return False

        change = total_paid - cost
        if change > 0:
            print(f"Here is ₹{change} in change.")

        self.profit += cost
        return True
```

---

## 7. Final Responsibility Map (Critical Insight)

| Object       | Owns Data        | Makes Decisions     |
| ------------ | ---------------- | ------------------- |
| MenuItem     | Drink definition | No                  |
| Menu         | Menu collection  | Lookup              |
| CoffeeMaker  | Resources        | Resource validation |
| MoneyMachine | Money            | Payment validation  |
| Main loop    | Flow             | Orchestration       |

---

## 8. Why This Design Is Superior

```
Procedural → Shared state → Fragile
OOP        → Owned state  → Stable
```

* Each object guards its own data
* No function knows too much
* Easy to extend (new drinks, new payment types)

---

## 9. Design Rule Lock-In

> If data and logic belong together,
> they must live in the same object.

This refactor converts your working procedural program into a **scalable, professional OOP system** without changing the behavior.
