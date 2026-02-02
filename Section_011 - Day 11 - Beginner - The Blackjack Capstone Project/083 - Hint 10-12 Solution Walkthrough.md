### STEP 4 — ROUND RESOLUTION & OUTCOME COMPARISON

---

## GOAL OF STEP 4

* Decide **win / lose / push**
* Apply **bet outcome**
* Keep resolution logic **isolated**
* No user input
* No game loop yet

This step runs **after**:

* Player turn is finished
* Dealer turn is finished (unless player busted)

---

## OUTCOME PRIORITY (VERY IMPORTANT)

| Priority | Condition                   | Result       |
| -------- | --------------------------- | ------------ |
| 1        | Player busts                | Player loses |
| 2        | Dealer busts                | Player wins  |
| 3        | Player total > Dealer total | Player wins  |
| 4        | Player total < Dealer total | Player loses |
| 5        | Equal totals                | Push         |

---

## FUNCTION — RESOLVE ROUND

```python
def resolve_round(player_hand, dealer_hand, bet, status):
    """
    Determines the outcome of the round.
    Returns outcome string and balance change.
    """
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    # Player already busted in Step 2
    if status == "bust":
        return "lose", -bet

    # Dealer busts
    if dealer_total > 21:
        return "win", bet

    # Compare totals
    if player_total > dealer_total:
        return "win", bet
    elif player_total < dealer_total:
        return "lose", -bet
    else:
        return "push", 0
```

---

## WHY THIS STRUCTURE IS CLEAN

* No side effects
* No printing inside logic
* Easily testable
* Game controller decides how to display results

---

## FUNCTION — DISPLAY ROUND RESULT

```python
def show_round_result(outcome, balance_change):
    """
    Displays the final round outcome.
    """
    print("\n=== ROUND RESULT ===")

    if outcome == "win":
        print("You win!")
        print(f"Balance change: +{balance_change}")
    elif outcome == "lose":
        print("You lose.")
        print(f"Balance change: {balance_change}")
    else:
        print("Push. Bet returned.")
        print("Balance change: 0")
```

---

## TEST DRIVER (FULL ROUND SIMULATION)

```python
balance = 100
bet = 10

deck = create_deck()
shuffle_deck(deck)

player_hand = [deal_card(deck), deal_card(deck)]
dealer_hand = [deal_card(deck), deal_card(deck)]

print("Player hand:", player_hand)
print("Player total:", calculate_hand_value(player_hand))

print("Dealer hand:", dealer_hand)
print("Dealer total:", calculate_hand_value(dealer_hand))

# Simulate a completed turn
status = "stand"  # try "bust" to test losing case

outcome, balance_change = resolve_round(
    player_hand,
    dealer_hand,
    bet,
    status
)

show_round_result(outcome, balance_change)

balance += balance_change
print("Updated balance:", balance)
```

---

## SAMPLE OUTPUT — PLAYER WINS

```
Player hand: ['9♥', '8♣']
Player total: 17
Dealer hand: ['6♠', '9♦']
Dealer total: 15

=== ROUND RESULT ===
You win!
Balance change: +10
Updated balance: 110
```

---

## SAMPLE OUTPUT — DEALER BUSTS

```
Player hand: ['10♣', '7♦']
Player total: 17
Dealer hand: ['9♠', '8♥', '7♣']
Dealer total: 24

=== ROUND RESULT ===
You win!
Balance change: +10
Updated balance: 110
```

---

## SAMPLE OUTPUT — PUSH

```
Player hand: ['10♠', '7♦']
Player total: 17
Dealer hand: ['9♣', '8♥']
Dealer total: 17

=== ROUND RESULT ===
Push. Bet returned.
Balance change: 0
Updated balance: 100
```

---

## WHAT STEP 4 COMPLETES

* Correct outcome determination
* Clean win/lose logic
* Proper bet resolution
* No duplicated comparisons

---
