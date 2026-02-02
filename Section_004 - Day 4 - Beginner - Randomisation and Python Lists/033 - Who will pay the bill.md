```python
"""
Program: Who Pays the Bill?
Author: Professional Python Example
Description:
    This program randomly selects one person from a group
    to pay the bill. It demonstrates clean input handling,
    list usage, randomness, and clear output formatting.
"""

import random


def who_pays_the_bill(names):
    """
    Selects one random person from the list.

    Parameters:
        names (list): List of participant names

    Returns:
        str: Name of the person who pays the bill
    """

    # Defensive check to avoid runtime errors
    if not names:
        raise ValueError("Name list cannot be empty")

    # random.choice picks one element uniformly at random
    selected_person = random.choice(names)

    return selected_person


def main():
    """
    Main driver function.
    Handles user input, processing, and output.
    """

    # Ask user for input
    raw_input_names = input(
        "Enter names separated by commas (e.g. Alice,Bob,Charlie): "
    )

    # Convert input string into a clean list of names
    names = [name.strip() for name in raw_input_names.split(",") if name.strip()]

    # Call business logic
    payer = who_pays_the_bill(names)

    # Professional formatted output
    print("\n💳 Bill Payment Result")
    print("-" * 25)
    print(f"{payer} has been selected to pay the bill.")
    print("Better luck next time! 😄")


# Program entry point
if __name__ == "__main__":
    main()
```

### Example Run (Output)

```text
Enter names separated by commas (e.g. Alice,Bob,Charlie): Alice, Bob, Charlie, David

💳 Bill Payment Result
-------------------------
Charlie has been selected to pay the bill.
Better luck next time! 😄
```

### Key Professional Concepts Used

| Concept            | Explanation              |
| ------------------ | ------------------------ |
| `random.choice()`  | Uniform random selection |
| List comprehension | Clean input parsing      |
| Functions          | Separation of logic      |
| Guard clause       | Prevents empty input     |
| `__main__` check   | Script-safe execution    |
| Clear formatting   | User-friendly output     |

### Notes (Real-world quality)

* Deterministic testing can be added using `random.seed()`
* Easily extendable to weighted probabilities
* Safe input handling
* Interview-acceptable structure
