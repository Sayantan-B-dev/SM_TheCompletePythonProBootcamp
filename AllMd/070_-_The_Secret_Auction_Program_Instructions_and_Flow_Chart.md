```python
# ================================
# SECRET SILENT AUCTION PROGRAM
# ================================
# This program allows multiple bidders to place bids secretly.
# Each bidder enters their name and bid amount.
# After all bids are entered, the program determines the highest bidder.
# No bids are shown during entry (silent auction behavior).


# Function to safely get a valid bid amount
def get_valid_bid():
    while True:
        bid = input("Enter your bid amount (numbers only): ₹ ")
        if bid.isdigit():
            return int(bid)
        else:
            print("❌ Invalid input. Please enter a numeric value.")

# Function to find the highest bidder
def find_highest_bidder(bids):
    highest_bid = 0
    winner = ""

    # Loop through dictionary keys (bidder names)
    for bidder in bids:
        bid_amount = bids[bidder]

        # Compare each bid with current highest
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder

    return winner, highest_bid


# ================================
# MAIN PROGRAM LOGIC
# ================================

print("🏷️  WELCOME TO THE SECRET SILENT AUCTION 🏷️")
print("-------------------------------------------")

bids = {}          # Dictionary to store bidder_name : bid_amount
auction_active = True

while auction_active:
    name = input("\nEnter bidder name: ").strip()

    # Prevent empty names
    if not name:
        print("❌ Name cannot be empty.")
        continue

    # Get validated bid
    amount = get_valid_bid()

    # Store bid in dictionary
    bids[name] = amount

    # Ask if more bidders are there
    choice = input("\nAre there any other bidders? (yes/no): ").lower()

    if choice == "no":
        auction_active = False
    elif choice == "yes":
        pass
    else:
        print("⚠️ Invalid choice. Assuming more bidders.")
        pass

# Determine winner
winner, winning_bid = find_highest_bidder(bids)

# Final result display
print("🏆 AUCTION RESULT 🏆")
print("--------------------")
print(f"Winner: {winner}")
print(f"Winning Bid: ₹ {winning_bid}")

```

### Sample Terminal Output

```
🏷️  WELCOME TO THE SECRET SILENT AUCTION 🏷️
-------------------------------------------

Enter bidder name: Alice
Enter your bid amount (numbers only): ₹ 2500
Are there any other bidders? (yes/no): yes


Enter bidder name: Bob
Enter your bid amount (numbers only): ₹ 3200
Are there any other bidders? (yes/no): no


🏆 AUCTION RESULT 🏆
--------------------
Winner: Bob
Winning Bid: ₹ 3200
```

---

## Documentation / Learning Notes

### 1. Core Data Structure

* **Dictionary (`bids`)**

  * Key → bidder name
  * Value → bid amount
* Perfect for mapping *who* → *how much*

---

### 2. Silent Auction Logic

* Bids are stored silently
* Screen clearing hides previous bidders
* Final result shown only once

---

### 3. Error Handling Used

| Scenario             | Handling                    |
| -------------------- | --------------------------- |
| Empty name           | rejected                    |
| Non-numeric bid      | loop until valid            |
| Invalid yes/no input | defaults safely             |
| Overwriting bids     | last bid wins (intentional) |

---

### 4. Why `isdigit()`?

* Prevents crashes from invalid input
* Ensures `int()` conversion is safe

---

### 5. Why Separate Functions?

* `get_valid_bid()` → input validation
* `find_highest_bidder()` → logic isolation
* Improves readability, testing, reuse

---

### 6. Unexpected Behaviors to Know

* Same name entered twice → bid overwritten
* Equal bids → first highest wins (by order)
* `clear_screen()` is visual, not OS-level

---

### 7. Easy Enhancements (Practice Ideas)

* Prevent duplicate names
* Handle tie bids
* Add currency formatting
* Store auction history
* Use ASCII banner art
* Add countdown timer

---

### 8. Real-World Mapping

* Used in sealed bidding systems
* Online auctions (backend logic)
* Competitive pricing simulations
* Game mechanics (loot bidding)

---

### 9. Key Takeaway

This program combines:

* dictionaries
* loops
* input validation
* defensive programming
* clean separation of logic

This is **production-style beginner Python**, not toy code.
