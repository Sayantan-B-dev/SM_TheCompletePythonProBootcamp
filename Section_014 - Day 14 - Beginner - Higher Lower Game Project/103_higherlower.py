# ============================================================
# HIGHER–LOWER GAME (SINGLE PLAYER + HISTORY ORIENTED)
# ============================================================
# • Dataset loaded from 103_dataset.py (same directory)
# • Single-player only
# • Full round-by-round history tracking
# • Clearer, well-separated terminal UI
# • Explicit comparison prompts to avoid confusion
# • Robust error handling
# ============================================================

import random
import sys
from datetime import datetime

# =========================
# DATASET IMPORT
# =========================
try:
    from dataset import DATASET
except ImportError:
    print("\n[ERROR] Dataset file not found.")
    print("Expected: 103_dataset.py with a variable named DATASET\n")
    sys.exit(1)

if not isinstance(DATASET, list) or len(DATASET) < 2:
    print("\n[ERROR] DATASET must be a list with at least 2 items.\n")
    sys.exit(1)

# =========================
# GAME HISTORY STORAGE
# =========================
GAME_HISTORY = []

# =========================
# UTILITY FUNCTIONS
# =========================

def divider(char="=", width=50):
    """Print a visual divider."""
    print(char * width)


def get_random_item(exclude=None):
    """Return a random dataset item different from exclude."""
    try:
        item = random.choice(DATASET)
        while exclude is not None and item == exclude:
            item = random.choice(DATASET)
        return item
    except IndexError:
        raise RuntimeError("Dataset is empty or corrupted")


def normalize_guess(user_input):
    """Normalize and validate user guess."""
    cleaned = user_input.strip().lower()
    if cleaned in ("higher", "h"):
        return "higher"
    if cleaned in ("lower", "l"):
        return "lower"
    return None


def compare_items(item_a, item_b):
    """Return correct answer based on hidden values."""
    try:
        return "higher" if item_b["value"] > item_a["value"] else "lower"
    except KeyError:
        raise KeyError("Each dataset item must contain a 'value' key")

# =========================
# GAME LOGIC
# =========================

def play_game(player_name):
    score = 0
    rounds = []

    item_a = get_random_item()

    divider()
    print(f"PLAYER: {player_name}")
    print("GAME STARTED")
    divider()

    while True:
        item_b = get_random_item(exclude=item_a)

        print("\nCURRENT COMPARISON")
        divider("-")

        print("ITEM A (REFERENCE)")
        print(f"Name        : {item_a['name']}")
        print(f"Description : {item_a['description']}")

        divider("~")

        print("ITEM B (TO COMPARE)")
        print(f"Name        : {item_b['name']}")
        print(f"Description : {item_b['description']}")

        divider("-")

        print(
            f"\nQUESTION:\n"
            f"Do you think **{item_b['name']}** has a HIGHER or LOWER value\n"
            f"than **{item_a['name']}**?"
        )
        print("Type: higher / lower (or h / l)")

        guess = None
        while guess is None:
            user_input = input("Your choice → ")
            guess = normalize_guess(user_input)
            if guess is None:
                print("Invalid input. Please respond clearly.")

        correct_answer = compare_items(item_a, item_b)

        round_record = {
            "A": item_a["name"],
            "B": item_b["name"],
            "A_value": item_a["value"],
            "B_value": item_b["value"],
            "guess": guess,
            "correct": guess == correct_answer
        }

        if guess == correct_answer:
            score += 1
            print("\nRESULT: ✔ CORRECT")
            print(f"{item_b['name']} = {item_b['value']}M")
            print(f"Current Score → {score}")
            rounds.append(round_record)
            item_a = item_b
        else:
            print("\nRESULT: ✘ WRONG")
            print("REVEAL:")
            print(f"{item_a['name']} = {item_a['value']}M")
            print(f"{item_b['name']} = {item_b['value']}M")
            rounds.append(round_record)
            break

    divider()
    print("GAME OVER")
    print(f"FINAL SCORE: {score}")
    divider()

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "player": player_name,
        "score": score,
        "rounds": rounds
    }

# =========================
# HISTORY DISPLAY
# =========================

def show_history():
    if not GAME_HISTORY:
        print("\nNo game history available.")
        return

    divider()
    print("GAME HISTORY")
    divider()

    for idx, game in enumerate(GAME_HISTORY, start=1):
        print(f"\nGAME #{idx}")
        print(f"Date   : {game['timestamp']}")
        print(f"Player : {game['player']}")
        print(f"Score  : {game['score']}")
        print("Rounds:")
        for i, r in enumerate(game["rounds"], start=1):
            status = "✔" if r["correct"] else "✘"
            print(
                f"  {i}. {r['A']} ({r['A_value']}M)  vs  "
                f"{r['B']} ({r['B_value']}M) "
                f"| Guess: {r['guess']} {status}"
            )

# =========================
# MAIN MENU
# =========================

def main():
    divider()
    print("WELCOME TO THE HIGHER–LOWER GAME")
    divider()

    player_name = input("Enter your name: ").strip() or "Player"

    while True:
        print("\nMAIN MENU")
        divider("-")
        print("1. Play Game")
        print("2. View History")
        print("3. Exit")
        divider("-")

        choice = input("Select an option (1/2/3): ").strip()

        if choice == "1":
            result = play_game(player_name)
            GAME_HISTORY.append(result)
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("\nThanks for playing. Goodbye.")
            sys.exit(0)
        else:
            print("Invalid menu choice.")

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Exiting safely.")
        sys.exit(0)
    except Exception as e:
        print("\nUnexpected error occurred:", str(e))
        sys.exit(1)
