### STEP 1 — MODEL THE GAME DATA (DECK, CARDS, HAND VALUE)

---

## GOAL OF STEP 1

* Represent cards and deck
* Shuffle deck
* Deal cards
* Calculate hand value correctly
* Handle **Ace (1 or 11)** automatically

No gameplay, no betting, no turns yet.
Only **pure data + logic**.

---

## DESIGN DECISIONS (IMPORTANT)

| Element   | Strategy                                   |
| --------- | ------------------------------------------ |
| Card      | Stored as string (`'A♠'`, `'10♥'`, `'K♦'`) |
| Deck      | List of card strings                       |
| Hand      | List of cards                              |
| Ace logic | Count as 11 first, downgrade to 1 if bust  |
| Deck size | Single 52-card deck                        |

---

## CARD & DECK STRUCTURE

```python
import random

# Suits and ranks define the deck
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
```

---

## FUNCTION 1 — CREATE A DECK

```python
def create_deck():
    """
    Creates a standard 52-card deck.
    Each card is represented as a string like 'A♠' or '10♦'.
    """
    deck = []

    # Loop through each suit
    for suit in SUITS:
        # Loop through each rank
        for rank in RANKS:
            deck.append(f"{rank}{suit}")

    return deck
```

### OUTPUT CHECK

```python
deck = create_deck()
print(len(deck))
print(deck[:5])
```

```
52
['2♠', '3♠', '4♠', '5♠', '6♠']
```

---

## FUNCTION 2 — SHUFFLE DECK

```python
def shuffle_deck(deck):
    """
    Shuffles the deck in-place.
    """
    random.shuffle(deck)
```

### OUTPUT CHECK

```python
shuffle_deck(deck)
print(deck[:5])
```

```
['Q♦', '7♣', 'A♥', '4♠', '10♦']
```

---

## FUNCTION 3 — DEAL A CARD

```python
def deal_card(deck):
    """
    Removes and returns the top card from the deck.
    """
    return deck.pop()
```

### OUTPUT CHECK

```python
card = deal_card(deck)
print(card)
print(len(deck))
```

```
9♣
51
```

---

## FUNCTION 4 — CALCULATE HAND VALUE (CRITICAL LOGIC)

```python
def calculate_hand_value(hand):
    """
    Calculates the total value of a blackjack hand.
    Aces are counted as 11 or 1 automatically.
    """
    total = 0
    ace_count = 0

    for card in hand:
        rank = card[:-1]  # remove suit

        if rank in ['J', 'Q', 'K']:
            total += 10
        elif rank == 'A':
            total += 11
            ace_count += 1
        else:
            total += int(rank)

    # Adjust Aces from 11 to 1 if total exceeds 21
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total
```

---

## HAND VALUE TEST CASES (VERY IMPORTANT)

```python
hand1 = ['A♠', 'K♦']
hand2 = ['A♠', '9♥', 'A♦']
hand3 = ['A♠', '9♥', 'A♦', '5♣']

print(calculate_hand_value(hand1))
print(calculate_hand_value(hand2))
print(calculate_hand_value(hand3))
```

```
21
21
16
```

---

## SIMULATED DEAL (PLAYER & DEALER)

```python
deck = create_deck()
shuffle_deck(deck)

player_hand = [deal_card(deck), deal_card(deck)]
dealer_hand = [deal_card(deck), deal_card(deck)]

print("Player hand:", player_hand)
print("Player total:", calculate_hand_value(player_hand))

print("Dealer hand:", dealer_hand)
print("Dealer total:", calculate_hand_value(dealer_hand))
```

### SAMPLE OUTPUT

```
Player hand: ['10♣', '7♥']
Player total: 17
Dealer hand: ['A♦', '6♠']
Dealer total: 17
```

---

## WHAT STEP 1 ACHIEVES

* Correct deck creation
* Safe shuffling
* Reliable dealing
* **Ace logic fully solved**
* Hand value always accurate

---

## DO NOT MOVE FORWARD UNTIL

* Ace never breaks the game
* Hand values are always correct
* Deck size decreases properly after dealing

