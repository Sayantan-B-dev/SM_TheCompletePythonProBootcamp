### STEP 3 — DEALER AUTOMATION (FORCED RULES, NO INPUT)

---

## GOAL OF STEP 3

* Implement **dealer behavior only**
* Dealer has **no choices**
* Dealer follows casino rules strictly
* No player logic, no betting logic

Dealer logic must be:

* Deterministic
* Automatic
* Reusable

---

## DEALER RULES (FIXED)

| Rule                       | Explanation                 |
| -------------------------- | --------------------------- |
| Dealer reveals hidden card | Happens before dealer plays |
| Dealer hits                | Total < 17                  |
| Dealer stands              | Total ≥ 17                  |
| Dealer hits on soft 16     | Required                    |
| Dealer stands on soft 17   | Standard                    |

---

## FUNCTION — DISPLAY DEALER STATE

```python
def show_dealer_state(dealer_hand, hide_first=False):
    """
    Displays dealer hand.
    If hide_first=True, hides the first card.
    """
    if hide_first:
        print("\nDealer hand: ['?',", *dealer_hand[1:], "]")
    else:
        print("\nDealer hand:", dealer_hand)
        print("Dealer total:", calculate_hand_value(dealer_hand))
```

---

## FUNCTION — DEALER TURN LOGIC

```python
def dealer_turn(deck, dealer_hand):
    """
    Handles dealer's automatic play.
    Dealer hits until total >= 17.
    Returns final dealer total.
    """
    print("\nDealer reveals hidden card.")
    show_dealer_state(dealer_hand)

    while calculate_hand_value(dealer_hand) < 17:
        print("Dealer hits.")
        dealer_hand.append(deal_card(deck))
        show_dealer_state(dealer_hand)

    print("Dealer stands.")
    return calculate_hand_value(dealer_hand)
```

---

## WHY THIS WORKS

* Dealer never asks for input
* Loop condition enforces rules
* Ace logic handled automatically by `calculate_hand_value`
* Stops immediately at valid stand condition

---

## TEST DRIVER (ISOLATED DEALER TURN)

```python
deck = create_deck()
shuffle_deck(deck)

dealer_hand = [deal_card(deck), deal_card(deck)]

print("Initial dealer state (one card hidden):")
show_dealer_state(dealer_hand, hide_first=True)

final_total = dealer_turn(deck, dealer_hand)

print("\n--- DEALER TURN RESULT ---")
print("Final dealer hand:", dealer_hand)
print("Final dealer total:", final_total)
```

---

## SAMPLE TERMINAL RUN (DEALER HITS)

```
Initial dealer state (one card hidden):
Dealer hand: ['?', 7♦ ]

Dealer reveals hidden card.
Dealer hand: ['5♣', '7♦']
Dealer total: 12
Dealer hits.

Dealer hand: ['5♣', '7♦', '6♥']
Dealer total: 18
Dealer stands.

--- DEALER TURN RESULT ---
Final dealer hand: ['5♣', '7♦', '6♥']
Final dealer total: 18
```

---

## SAMPLE TERMINAL RUN (DEALER STANDS IMMEDIATELY)

```
Initial dealer state (one card hidden):
Dealer hand: ['?', K♠ ]

Dealer reveals hidden card.
Dealer hand: ['A♦', 'K♠']
Dealer total: 21
Dealer stands.

--- DEALER TURN RESULT ---
Final dealer hand: ['A♦', 'K♠']
Final dealer total: 21
```

---

## EDGE CASES HANDLED

* Dealer busts (>21)
* Soft hand Ace adjustment
* Correct stop at 17+

---

## WHAT STEP 3 COMPLETES

* Fully automatic dealer logic
* Clean separation from player code
* Deterministic behavior
* No user input dependency

---
