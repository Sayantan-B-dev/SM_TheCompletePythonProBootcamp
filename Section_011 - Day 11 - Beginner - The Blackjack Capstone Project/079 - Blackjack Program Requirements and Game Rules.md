### BLACKJACK — HIGH-LEVEL STRATEGY ONLY (NO CODE)

---

## A) PSEUDOCODE (LOGIC FLOW, LANGUAGE-AGNOSTIC)

```
START GAME
SET player_balance

WHILE player_balance > 0 AND player_wants_to_continue

    ASK player for bet
    VALIDATE bet <= player_balance

    CREATE and SHUFFLE deck
    DEAL 2 cards to player
    DEAL 2 cards to dealer (1 hidden)

    CALCULATE hand values (Ace = 11 or 1 automatically)

    IF player has blackjack AND dealer has blackjack
        RESULT = push
        RETURN bet
        CONTINUE round

    IF player has blackjack
        PAY 3:2
        CONTINUE round

    IF dealer has blackjack
        PLAYER loses bet
        CONTINUE round

    ---- PLAYER TURN ----
    WHILE player chooses action
        SHOW player cards and visible dealer card
        ASK action (hit / stand / double)

        IF hit
            DEAL 1 card to player
            RECALCULATE hand value
            IF value > 21
                PLAYER busts
                PLAYER loses bet
                END player turn

        IF double
            DOUBLE bet
            DEAL 1 card
            RECALCULATE
            END player turn

        IF stand
            END player turn

    IF player busted
        CONTINUE round

    ---- DEALER TURN ----
    REVEAL dealer hidden card
    WHILE dealer total < 17
        DEAL 1 card to dealer
        RECALCULATE dealer total

    ---- COMPARE HANDS ----
    IF dealer busts
        PLAYER wins bet
    ELSE IF player > dealer
        PLAYER wins bet
    ELSE IF player < dealer
        PLAYER loses bet
    ELSE
        PUSH (return bet)

END WHILE

END GAME
```

---

## B) 5 STRATEGIC STEPS TO BUILD IT AS A PYTHON TERMINAL GAME

---

### STEP 1 — MODEL THE GAME DATA (FOUNDATION)

Focus: **data representation, not gameplay**

Strategy:

* Decide how cards, deck, and hands are stored
* Cards as strings or tuples
* Deck as a list
* Hand as a list of cards

Decisions to lock early:

* How Ace adjustment works
* How totals are calculated
* Single deck or multiple deck

Outcome of this step:

* You can create, shuffle, deal cards
* You can calculate hand value correctly every time

---

### STEP 2 — PLAYER INTERACTION LOOP

Focus: **input, validation, turn logic**

Strategy:

* One clear loop for player decisions
* Restrict actions based on game state
* Validate every input (no crashes)

Design principles:

* Player turn ends immediately on bust
* Player cannot act after stand/double
* Always show clear state before asking input

Outcome of this step:

* Player can hit, stand, double safely
* Invalid input never breaks the game

---

### STEP 3 — DEALER AUTOMATION (NO CHOICES)

Focus: **fixed rules, zero interaction**

Strategy:

* Dealer logic must be deterministic
* No user input here
* Follow casino rules strictly

Dealer behavior rules:

* Hit until total >= 17
* Stop immediately at 17+
* Ace logic auto-adjusted

Outcome of this step:

* Dealer plays correctly every time
* No duplicated logic from player turn

---

### STEP 4 — ROUND RESOLUTION & PAYOUT

Focus: **comparison logic and money flow**

Strategy:

* Compare only after dealer finishes
* Resolve outcomes in strict order
* Keep payout logic isolated (clean, readable)

Resolution priority:

1. Player bust
2. Dealer bust
3. Higher total wins
4. Equal total → push

Outcome of this step:

* Correct win/loss every round
* Balance updates accurately

---

### STEP 5 — GAME LOOP & UX POLISH

Focus: **playability and structure**

Strategy:

* Wrap everything in a game loop
* Allow replay without restarting program
* Clear screen or spacing for readability
* Minimal ASCII for cards and separators

Quality checks:

* Balance never goes negative
* Game exits cleanly
* Each round feels distinct

Outcome of this step:

* Fully playable terminal blackjack
* Easy to extend later (split, insurance, stats)

---

### CORE DESIGN PRINCIPLE

Blackjack is **state-driven**, not animation-driven.
If state transitions are correct (deal → player → dealer → resolve), the game will always be correct even in a plain terminal.

Next step after strategy: implement **Step 1 only** (deck + hand value) before touching gameplay.
