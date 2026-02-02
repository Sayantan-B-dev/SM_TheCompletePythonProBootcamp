import random

# =========================
# CONSTANTS
# =========================

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# =========================
# STEP 1 — DATA & UTILITIES
# =========================

def create_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append(f"{rank}{suit}")
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    total = 0
    ace_count = 0

    for card in hand:
        rank = card[:-1]
        if rank in ['J', 'Q', 'K']:
            total += 10
        elif rank == 'A':
            total += 11
            ace_count += 1
        else:
            total += int(rank)

    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total

# =========================
# STEP 2 — PLAYER TURN
# =========================

def show_player_state(hand):
    print("\nYour hand:", hand)
    print("Your total:", calculate_hand_value(hand))

def player_turn(deck, hand, balance, bet):
    has_doubled = False

    while True:
        show_player_state(hand)

        if calculate_hand_value(hand) > 21:
            print("You busted!")
            return bet, "bust"

        if len(hand) == 2 and balance >= bet and not has_doubled:
            print("Choose action: [hit / stand / double]")
        else:
            print("Choose action: [hit / stand]")

        choice = input("> ").strip().lower()

        if choice == "hit":
            hand.append(deal_card(deck))
            print("You draw a card.")

        elif choice == "stand":
            print("You stand.")
            return bet, "stand"

        elif choice == "double" and len(hand) == 2 and balance >= bet:
            bet *= 2
            hand.append(deal_card(deck))
            print("You double down.")
            show_player_state(hand)

            if calculate_hand_value(hand) > 21:
                print("You busted after doubling!")
                return bet, "bust"

            return bet, "stand"

        else:
            print("Invalid action.")

# =========================
# STEP 3 — DEALER TURN
# =========================

def show_dealer_state(hand, hide_first=False):
    if hide_first:
        print("\nDealer hand: ['?',", hand[1], "]")
    else:
        print("\nDealer hand:", hand)
        print("Dealer total:", calculate_hand_value(hand))

def dealer_turn(deck, hand):
    print("\nDealer reveals hidden card.")
    show_dealer_state(hand)

    while calculate_hand_value(hand) < 17:
        print("Dealer hits.")
        hand.append(deal_card(deck))
        show_dealer_state(hand)

    print("Dealer stands.")

# =========================
# STEP 4 — RESOLUTION
# =========================

def resolve_round(player_hand, dealer_hand, bet, status):
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    if status == "bust":
        return "lose", -bet

    if dealer_total > 21:
        return "win", bet

    if player_total > dealer_total:
        return "win", bet
    elif player_total < dealer_total:
        return "lose", -bet
    else:
        return "push", 0

# =========================
# STEP 5 — GAME LOOP
# =========================

def blackjack_game():
    balance = 100

    print("=== BLACKJACK TERMINAL GAME ===")
    print("Starting balance:", balance)

    while balance > 0:
        print("\n----------------------------")
        print("Current balance:", balance)

        # Bet input
        while True:
            try:
                bet = int(input("Place your bet: "))
                if 0 < bet <= balance:
                    break
                print("Invalid bet amount.")
            except ValueError:
                print("Enter a number.")

        # Setup round
        deck = create_deck()
        shuffle_deck(deck)

        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        show_player_state(player_hand)
        show_dealer_state(dealer_hand, hide_first=True)

        # Player phase
        bet, status = player_turn(deck, player_hand, balance, bet)

        # Dealer phase
        if status != "bust":
            dealer_turn(deck, dealer_hand)

        # Resolve
        outcome, balance_change = resolve_round(
            player_hand, dealer_hand, bet, status
        )

        balance += balance_change

        print("\n=== ROUND RESULT ===")
        print("Outcome:", outcome.upper())
        print("Balance change:", balance_change)
        print("New balance:", balance)

        if balance <= 0:
            print("You are out of money.")
            break

        again = input("\nPlay another round? (y/n): ").lower()
        if again != 'y':
            break

    print("\nGame over. Final balance:", balance)

# =========================
# RUN GAME
# =========================

blackjack_game()
