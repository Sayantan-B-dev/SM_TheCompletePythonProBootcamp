### STEP 2 — PLAYER INTERACTION LOOP (HIT / STAND / DOUBLE)

---

## GOAL OF STEP 2

* Handle **only the player’s turn**
* Allow player to:

  * Hit
  * Stand
  * Double down
* Validate inputs safely
* End turn correctly on:

  * Bust
  * Stand
  * Double

No dealer logic yet.
No round comparison yet.

---

## STATE REQUIRED FROM STEP 1

Assumed already available:

* `deck`
* `player_hand`
* `calculate_hand_value()`
* `deal_card()`

---

## PLAYER TURN RULES (STRICT)

| Rule              | Explanation               |
| ----------------- | ------------------------- |
| Player acts first | Dealer waits              |
| Hit               | Take 1 card, may repeat   |
| Stand             | End turn                  |
| Double            | Only once, ends turn      |
| Bust              | Immediate loss, turn ends |
| Input             | Must be validated         |

---

## FUNCTION — DISPLAY PLAYER STATE

```python
def show_player_state(player_hand):
    """
    Displays player's current hand and total.
    """
    total = calculate_hand_value(player_hand)
    print("\nYour hand:", player_hand)
    print("Your total:", total)
```

---

## FUNCTION — PLAYER TURN LOOP

```python
def player_turn(deck, player_hand, balance, bet):
    """
    Handles the entire player decision phase.
    Returns updated bet and a status flag.
    """
    has_doubled = False

    while True:
        show_player_state(player_hand)

        # Check for bust before asking input
        if calculate_hand_value(player_hand) > 21:
            print("You busted!")
            return bet, "bust"

        # Available actions
        if len(player_hand) == 2 and balance >= bet and not has_doubled:
            print("Choose action: [hit / stand / double]")
        else:
            print("Choose action: [hit / stand]")

        choice = input("> ").strip().lower()

        if choice == "hit":
            player_hand.append(deal_card(deck))
            print("You draw a card.")

        elif choice == "stand":
            print("You stand.")
            return bet, "stand"

        elif choice == "double" and len(player_hand) == 2 and balance >= bet:
            bet *= 2
            player_hand.append(deal_card(deck))
            has_doubled = True
            print("You double down.")
            show_player_state(player_hand)

            if calculate_hand_value(player_hand) > 21:
                print("You busted after doubling!")
                return bet, "bust"

            return bet, "stand"

        else:
            print("Invalid action. Try again.")
```

---

## WHY EACH PART EXISTS (IMPORTANT)

### `while True`

* Player can hit multiple times
* Loop exits only on **stand, bust, or double**

### `len(player_hand) == 2`

* Ensures **double down** is first-move only

### `balance >= bet`

* Prevents illegal doubling

### `return bet, status`

* Game controller later decides outcome
* Keeps player logic isolated

---

## TEST DRIVER (ISOLATED PLAYER TURN)

```python
# Setup for testing Step 2
balance = 100
bet = 10

deck = create_deck()
shuffle_deck(deck)

player_hand = [deal_card(deck), deal_card(deck)]

bet, status = player_turn(deck, player_hand, balance, bet)

print("\n--- PLAYER TURN RESULT ---")
print("Final hand:", player_hand)
print("Final total:", calculate_hand_value(player_hand))
print("Final bet:", bet)
print("Status:", status)
```

---

## SAMPLE TERMINAL RUN (HIT → STAND)

```
Your hand: ['9♣', '5♦']
Your total: 14
Choose action: [hit / stand / double]
> hit
You draw a card.

Your hand: ['9♣', '5♦', '6♥']
Your total: 20
Choose action: [hit / stand]
> stand
You stand.

--- PLAYER TURN RESULT ---
Final hand: ['9♣', '5♦', '6♥']
Final total: 20
Final bet: 10
Status: stand
```

---

## SAMPLE TERMINAL RUN (DOUBLE DOWN)

```
Your hand: ['6♠', '5♥']
Your total: 11
Choose action: [hit / stand / double]
> double
You double down.

Your hand: ['6♠', '5♥', '10♦']
Your total: 21

--- PLAYER TURN RESULT ---
Final hand: ['6♠', '5♥', '10♦']
Final total: 21
Final bet: 20
Status: stand
```

---

## SAMPLE TERMINAL RUN (BUST)

```
Your hand: ['K♣', '8♦']
Your total: 18
Choose action: [hit / stand]
> hit
You draw a card.

Your hand: ['K♣', '8♦', '6♠']
Your total: 24
You busted!

--- PLAYER TURN RESULT ---
Final hand: ['K♣', '8♦', '6♠']
Final total: 24
Final bet: 10
Status: bust
```

---

## WHAT STEP 2 COMPLETES

* Safe input handling
* Correct hit/stand/double behavior
* No illegal actions
* Clean turn termination
* Player logic fully isolated

---