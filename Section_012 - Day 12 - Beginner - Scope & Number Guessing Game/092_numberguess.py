"""
===========================================================
MULTIPLAYER NUMBER GUESSING GAME (TERMINAL BASED)
===========================================================

FEATURES
--------
✔ Multiple difficulty levels (range + guesses)
✔ Multiplayer (turn-based)
✔ Score keeping
✔ Guess history per player
✔ Fun ASCII art and texts
✔ Clean scope usage (NO bad globals)
✔ Fully documented & commented

DIFFICULTY LEVELS
-----------------
Easy    : 1–10    | 5 guesses | x1 score
Medium  : 1–50    | 7 guesses | x2 score
Hard    : 1–100   | 10 guesses| x3 score
Extreme : 1–500   | 12 guesses| x5 score
"""

import random

# ---------------------------------------------------------
# ASCII ARTS
# ---------------------------------------------------------

TITLE_ART = """
╔══════════════════════════════════════╗
║     🎯 NUMBER GUESSING GAME 🎯       ║
╚══════════════════════════════════════╝
"""

WIN_ART = """
 ██████╗ ██╗   ██╗███████╗███████╗
██╔════╝ ██║   ██║██╔════╝██╔════╝
██║  ███╗██║   ██║█████╗  ███████╗
██║   ██║██║   ██║██╔══╝  ╚════██║
╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""

LOSE_ART = """
 ☠ ☠ ☠ GAME OVER ☠ ☠ ☠
 The number escaped you...
"""

# ---------------------------------------------------------
# DIFFICULTY CONFIGURATION (READ-ONLY GLOBAL CONSTANT)
# ---------------------------------------------------------

DIFFICULTIES = {
    "1": {"name": "Easy", "range": 10, "guesses": 5, "multiplier": 1},
    "2": {"name": "Medium", "range": 50, "guesses": 7, "multiplier": 2},
    "3": {"name": "Hard", "range": 100, "guesses": 10, "multiplier": 3},
    "4": {"name": "Extreme", "range": 500, "guesses": 12, "multiplier": 5},
}

# ---------------------------------------------------------
# PLAYER SETUP
# ---------------------------------------------------------

def create_players():
    """
    Creates player profiles with score and history.

    Returns:
        list: List of player dictionaries
    """
    players = []
    count = int(input("Enter number of players: "))

    for i in range(count):
        name = input(f"Enter name for Player {i+1}: ")
        players.append({
            "name": name,
            "score": 0,
            "history": []
        })
    return players

# ---------------------------------------------------------
# DIFFICULTY SELECTION
# ---------------------------------------------------------

def select_difficulty():
    """
    Displays difficulty menu and returns selected config.

    Returns:
        dict: Difficulty configuration
    """
    print("\nChoose Difficulty:")
    for key, value in DIFFICULTIES.items():
        print(f"{key}. {value['name']} (1–{value['range']}, {value['guesses']} guesses)")

    choice = input("Enter choice: ")
    return DIFFICULTIES.get(choice, DIFFICULTIES["1"])

# ---------------------------------------------------------
# SINGLE PLAYER TURN
# ---------------------------------------------------------

def player_turn(player, secret, max_guesses, multiplier):
    """
    Handles a single player's guessing turn.

    Updates score and history.

    Args:
        player (dict): Player data
        secret (int): Secret number
        max_guesses (int): Allowed guesses
        multiplier (int): Score multiplier
    """
    guesses_left = max_guesses
    guesses = []
    success = False

    while guesses_left > 0:
        try:
            print(f"\n{player['name']} | Guesses left: {guesses_left}")
            guess = int(input("Enter your guess: "))

            guesses.append(guess)
            guesses_left -= 1

            if guess == secret:
                print(WIN_ART)
                score_gain = guesses_left * multiplier
                player["score"] += score_gain
                success = True
                break
            elif guess < secret:
                print("Too LOW 🔽")
            else:
                print("Too HIGH 🔼")

        except ValueError:
            print("Invalid input! Enter a number.")

    if not success:
        print(LOSE_ART)

    # Store round history
    player["history"].append({
        "guesses": guesses,
        "success": success
    })

# ---------------------------------------------------------
# ROUND SUMMARY
# ---------------------------------------------------------

def show_round_summary(players, round_no):
    """
    Displays round summary table.

    Args:
        players (list): Player list
        round_no (int): Current round number
    """
    print(f"\n📊 ROUND {round_no} SUMMARY")
    print("-" * 40)
    for p in players:
        last = p["history"][-1]
        print(
            f"{p['name']} | "
            f"Guesses: {last['guesses']} | "
            f"Success: {last['success']} | "
            f"Score: {p['score']}"
        )

# ---------------------------------------------------------
# FINAL SCOREBOARD & HISTORY
# ---------------------------------------------------------

def show_final_results(players):
    """
    Displays final scores and full history.
    """
    print("\n🏆 FINAL SCOREBOARD")
    print("=" * 40)
    for p in players:
        print(f"{p['name']} → Score: {p['score']}")
        for i, h in enumerate(p["history"], 1):
            print(f"  Round {i}: {h['guesses']} | Success: {h['success']}")

# ---------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------

def play_game():
    """
    Main game controller.
    """
    print(TITLE_ART)
    players = create_players()
    round_no = 1

    while True:
        difficulty = select_difficulty()
        secret = random.randint(1, difficulty["range"])

        print(
            f"\n🎲 ROUND {round_no} | "
            f"Range: 1–{difficulty['range']} | "
            f"Max guesses: {difficulty['guesses']}"
        )

        for player in players:
            player_turn(
                player,
                secret,
                difficulty["guesses"],
                difficulty["multiplier"]
            )

        show_round_summary(players, round_no)

        again = input("\nPlay another round? (y/n): ").lower()
        if again != "y":
            break

        round_no += 1

    show_final_results(players)

# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------

play_game()
