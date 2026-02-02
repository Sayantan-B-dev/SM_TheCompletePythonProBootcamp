### Pizza Order Practice Program (Python)

This program demonstrates conditional flow, data types, input validation, error handling, and clean professional structure.

---

### Problem Rules (Business Logic)

| Item           | Condition  | Price (₹) |
| -------------- | ---------- | --------- |
| Pizza Size     | Small (S)  | 150       |
|                | Medium (M) | 200       |
|                | Large (L)  | 250       |
| Extra Cheese   | Yes        | +40       |
| Extra Toppings | Yes        | +60       |
| Delivery       | Yes        | +50       |
| Tax            | GST        | 5%        |

---

### Data Types Used

| Variable         | Type    | Purpose              |
| ---------------- | ------- | -------------------- |
| `size`           | `str`   | Pizza size selection |
| `extra_cheese`   | `bool`  | Cheese add-on        |
| `extra_toppings` | `bool`  | Toppings add-on      |
| `delivery`       | `bool`  | Delivery option      |
| `base_price`     | `int`   | Pizza base cost      |
| `total`          | `float` | Final bill amount    |

---

### Professional Python Implementation

```python
def get_yes_no(prompt: str) -> bool:
    """Safely get yes/no input from user"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("yes", "y"):
            return True
        elif choice in ("no", "n"):
            return False
        else:
            print("Invalid input. Please enter Yes or No.")


def calculate_pizza_price(size: str, cheese: bool, toppings: bool, delivery: bool) -> float:
    """Calculate total pizza price based on selections"""

    prices = {
        "s": 150,
        "m": 200,
        "l": 250
    }

    if size not in prices:
        raise ValueError("Invalid pizza size selected")

    total = prices[size]

    if cheese:
        total += 40

    if toppings:
        total += 60

    if delivery:
        total += 50

    tax = total * 0.05
    return total + tax


def main():
    print("🍕 Welcome to Python Pizza 🍕")

    try:
        size = input("Choose pizza size (S/M/L): ").strip().lower()
        extra_cheese = get_yes_no("Add extra cheese? (Yes/No): ")
        extra_toppings = get_yes_no("Add extra toppings? (Yes/No): ")
        delivery = get_yes_no("Home delivery? (Yes/No): ")

        final_price = calculate_pizza_price(
            size=size,
            cheese=extra_cheese,
            toppings=extra_toppings,
            delivery=delivery
        )

        print("\n--- Order Summary ---")
        print(f"Pizza size       : {size.upper()}")
        print(f"Extra cheese     : {extra_cheese}")
        print(f"Extra toppings   : {extra_toppings}")
        print(f"Home delivery    : {delivery}")
        print(f"Total payable ₹  : {round(final_price, 2)}")

    except ValueError as e:
        print(f"Order Error: {e}")
    except Exception:
        print("Unexpected error occurred. Please try again.")


if __name__ == "__main__":
    main()
```

---

### Conditional Flow Used

| Condition               | Purpose           |
| ----------------------- | ----------------- |
| `if size not in prices` | Input validation  |
| `if cheese:`            | Add cheese cost   |
| `if toppings:`          | Add toppings cost |
| `if delivery:`          | Add delivery fee  |
| `try / except`          | Error handling    |

---

### Concepts Demonstrated

| Concept                | Usage                          |
| ---------------------- | ------------------------------ |
| Conditional statements | Pricing logic                  |
| Boolean logic          | Add-on decisions               |
| Dictionaries           | Price mapping                  |
| Functions              | Modular design                 |
| Error handling         | Robust input validation        |
| Data typing            | Clean and predictable behavior |

---

### Practice Extensions

| Task                  | Difficulty |
| --------------------- | ---------- |
| Add multiple pizzas   | Medium     |
| Apply discount coupon | Medium     |
| Student discount      | Easy       |
| Order history         | Hard       |
| File-based receipt    | Hard       |

---

This mirrors real-world billing systems and is suitable for interviews, beginners-to-intermediate practice, and professional Python standards.
