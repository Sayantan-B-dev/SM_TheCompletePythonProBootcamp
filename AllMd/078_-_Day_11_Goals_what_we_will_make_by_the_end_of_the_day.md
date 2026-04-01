![Image](https://images.openai.com/static-rsc-3/qE6nnF73c7sp7j_4BQot9TqmUO7lqT6O-rK_tONkVbfKYleHJKs6OnGd_PkahebWYYhIm971ULdT0yg9stTm4BKn6SZi76xdt_oaYZstW4o?purpose=fullsize)

![Image](https://blackjackdoc.com/img/value.png)

![Image](https://www.888casino.com/blog/sites/newblog.888casino.com/files/inline-images/Hand-1.jpg)

![Image](https://www.pagat.com/images/banking/bjbasic.jpg)

### BLACKJACK (21) — COMPLETE RULE SET (TERMINAL-FRIENDLY)

---

## 1. Objective

* Beat the **dealer**, not other players.
* Win by:

  * Getting a hand value **closer to 21** than the dealer without exceeding 21, or
  * Dealer **busts** (goes over 21).

---

## 2. Card Values

| Card Type           | Value                                          |
| ------------------- | ---------------------------------------------- |
| Number cards (2–10) | Face value                                     |
| Jack (J)            | 10                                             |
| Queen (Q)           | 10                                             |
| King (K)            | 10                                             |
| Ace (A)             | 1 **or** 11 (whichever is better for the hand) |

**Ace rule**

* If counting Ace as 11 causes total > 21 → Ace becomes 1 automatically.

---

## 3. Game Setup

* Standard **52-card deck** (can use multiple decks, but terminal games usually use 1).
* One **dealer**, one or more **players**.
* Each round:

  * Player places a **bet**
  * Dealer and player receive cards

---

## 4. Dealing Cards

* Player gets **2 cards**
* Dealer gets **2 cards**

  * One card **face up** (visible)
  * One card **face down** (hidden)

Example:

```
Player:  K  7   → Total = 17
Dealer:  9  ?   → One card hidden
```

---

## 5. Player Turn Rules

The player acts **first**.

### Player options:

| Action               | Meaning                                  |
| -------------------- | ---------------------------------------- |
| Hit                  | Take one more card                       |
| Stand                | Take no more cards                       |
| Double Down          | Double bet, take **one** final card      |
| Split                | Split two identical cards into two hands |
| Surrender (optional) | Forfeit half bet, end hand               |

---

### Hit

* Player takes another card.
* Can hit **multiple times**.
* If total > 21 → **Bust (lose immediately)**.

---

### Stand

* Player ends turn.
* Dealer plays next.

---

### Double Down

Conditions:

* Usually allowed only on first move.
  Rules:
* Bet is doubled.
* Player receives **exactly one card**.
* Turn ends.

---

### Split

Conditions:

* First two cards must have **same value** (e.g., 8 & 8, K & Q).
  Rules:
* Split into **two separate hands**.
* Each hand gets a new card.
* Each hand plays independently.
* Requires an **extra bet** equal to the original.

---

## 6. Dealer Rules (Fixed, No Choice)

Dealer plays **after all players finish**.

Dealer must:

* **Hit** until total is **17 or more**
* **Stand** on 17 or higher

Common rule:

* Dealer **hits on soft 16**
* Dealer **stands on soft 17** (Ace + 6)

Dealer **cannot**:

* Double down
* Split
* Surrender

---

## 7. Bust Rules

| Situation          | Result                           |
| ------------------ | -------------------------------- |
| Player busts (>21) | Player loses                     |
| Dealer busts (>21) | All remaining players win        |
| Both bust          | Player loses (player bust first) |

---

## 8. Blackjack (Natural 21)

* Ace + 10-value card as **first two cards**
* Beats all hands **except dealer blackjack**

### Payout:

* Standard win → 1 : 1
* Blackjack win → **3 : 2**

Example:

```
Bet: $10
Blackjack payout: $15
```

If both player and dealer have blackjack → **Push**

---

## 9. Comparing Hands (After Dealer Plays)

| Condition       | Outcome                  |
| --------------- | ------------------------ |
| Player > Dealer | Player wins              |
| Player < Dealer | Player loses             |
| Equal total     | Push (tie, bet returned) |
| Dealer busts    | Player wins              |
| Player busts    | Player loses             |

---

## 10. Push (Tie)

* Player total == Dealer total
* No one wins or loses
* Bet is returned

---

## 11. Insurance (Optional Rule)

* Offered when dealer’s visible card is **Ace**
* Player bets **half** of original bet
* If dealer has blackjack → insurance pays **2 : 1**
* If not → insurance bet lost

(Usually avoided in learning projects)

---

## 12. Typical Round Flow (Terminal Logic)

```text
1. Player places bet
2. Deal 2 cards to player
3. Deal 2 cards to dealer (1 hidden)
4. Check for blackjack
5. Player turn (hit / stand / double / split)
6. Dealer reveals hidden card
7. Dealer hits until >=17
8. Compare hands
9. Payout or loss
```

---

## 13. Common Simplifications for Terminal Games

Recommended for learning:

* Single deck
* No insurance
* No surrender
* One player vs dealer
* Simple ASCII card display

---

## 14. Key Rules to Enforce in Code

* Ace auto-adjusts (11 → 1)
* Player bust ends turn immediately
* Dealer logic is **automatic**
* Blackjack check happens **before** player actions
* Split hands tracked independently

---

## 15. Win/Loss Summary Table

| Situation          | Player Result |
| ------------------ | ------------- |
| Blackjack          | Win (3:2)     |
| Higher than dealer | Win           |
| Dealer bust        | Win           |
| Same total         | Push          |
| Lower than dealer  | Lose          |
| Player bust        | Lose          |

---

These rules are sufficient to build a **fully correct blackjack terminal game** with betting, turns, and payout logic.
