### DOCUMENTATION — MULTIPLAYER NUMBER GUESSING GAME (TERMINAL)

---

## 1. PURPOSE OF THE PROGRAM

This program implements a **terminal-based multiplayer number guessing game** designed to demonstrate:

* Clean scope management (no unsafe globals)
* State-driven game logic
* Turn-based multiplayer flow
* Difficulty-based constraints
* History tracking and scoring
* Readable, maintainable Python structure

The game is intentionally structured the way **real-world terminal games and CLI tools** are written.

---

## 2. HIGH-LEVEL ARCHITECTURE

The program follows a **controller + helper-functions** architecture.

```
play_game()
 ├── create_players()
 ├── select_difficulty()
 ├── player_turn()
 ├── show_round_summary()
 └── show_final_results()
```

Each function:

* Has a single responsibility
* Uses local scope safely
* Communicates only via arguments and return values

---

## 3. GLOBALS USED (AND WHY THEY ARE SAFE)

Only **read-only configuration and ASCII art** are global.

| Global Name    | Purpose          | Mutability |
| -------------- | ---------------- | ---------- |
| `DIFFICULTIES` | Difficulty rules | Read-only  |
| `TITLE_ART`    | UI display       | Read-only  |
| `WIN_ART`      | UI display       | Read-only  |
| `LOSE_ART`     | UI display       | Read-only  |

No game state (scores, players, secret numbers) is stored globally.

---

## 4. PLAYER DATA MODEL

Each player is represented as a dictionary.

```
player = {
    "name": str,
    "score": int,
    "history": list
}
```

### History structure (per round)

```
{
    "guesses": [int, int, ...],
    "success": bool
}
```

This allows:

* Full round-by-round replay
* Score auditing
* Easy extension (timestamps, penalties, etc.)

---

## 5. GAME FLOW (DETAILED)

### Step 1 — Game start

* `play_game()` prints the title ASCII
* Calls `create_players()`
* Initializes round counter

---

### Step 2 — Player creation (`create_players`)

* Asks for number of players
* Collects player names
* Initializes:

  * score = 0
  * history = empty list

No globals are modified.

---

### Step 3 — Difficulty selection (`select_difficulty`)

* Displays difficulty menu
* Reads user choice
* Returns a difficulty dictionary:

```
{
  "name": "Easy",
  "range": 10,
  "guesses": 5,
  "multiplier": 1
}
```

Difficulty affects:

* Secret number range
* Allowed guesses
* Score multiplier

---

### Step 4 — Round setup

Inside `play_game()`:

* Generates secret number using `random.randint`
* Displays round metadata
* Iterates through players in turn order

---

### Step 5 — Player turn (`player_turn`)

This is the core gameplay loop.

For each player:

1. Initialize:

   * guesses_left
   * guesses list
   * success flag

2. Loop while guesses remain:

   * Prompt user for guess
   * Validate input
   * Store guess in local list
   * Compare with secret number
   * Print feedback (Too High / Too Low / Win)

3. If guessed correctly:

   * Score awarded = guesses_left × multiplier
   * Success flag set

4. If guesses run out:

   * Failure ASCII shown

5. Store round result in player's history

This function:

* Mutates only the passed-in `player` object
* Has no hidden side effects
* Is deterministic given inputs

---

## 6. SCORING SYSTEM

```
score_gain = remaining_guesses × difficulty_multiplier
```

This design:

* Rewards efficiency
* Rewards harder difficulty
* Prevents score inflation

Example:

* Hard mode (×3)
* 4 guesses left
* Score gained = 12

---

## 7. ROUND SUMMARY (`show_round_summary`)

After all players finish:

* Displays per-player:

  * Guess history
  * Success / failure
  * Current total score

This reinforces:

* Transparency
* Multiplayer fairness
* Debug-friendly output

---

## 8. CONTINUATION LOGIC

At end of each round:

* User is asked whether to continue
* If yes:

  * round number increments
  * new difficulty can be selected
* If no:

  * game exits gracefully

---

## 9. FINAL RESULTS (`show_final_results`)

Displays:

* Final scores for all players
* Full guess history per player per round

This acts as:

* End-game scoreboard
* Audit log
* Learning feedback

---

## 10. ERROR HANDLING STRATEGY

Handled safely:

* Non-integer input → caught with `try/except`
* Invalid difficulty choice → defaults safely
* Guess input does not crash game

Not handled intentionally:

* Malicious inputs (out of scope for terminal demo)

---

## 11. SCOPE & DESIGN PRINCIPLES USED

| Principle             | How it’s applied            |
| --------------------- | --------------------------- |
| No global state       | All state passed explicitly |
| Function scope        | Each function isolated      |
| Single responsibility | One task per function       |
| Predictable mutation  | Only player object updated  |
| Extensible design     | Easy to add modes/features  |

---

## 12. HOW THIS SCALES PROFESSIONALLY

This design can be extended to:

* Save/load game state (JSON)
* Add AI players
* Add leaderboard persistence
* Convert to GUI or web app
* Add timers or penalties
* Multiplayer networking

Without changing core logic.

---

## 13. SUMMARY (IMPORTANT)

* Globals are **configuration only**
* State flows explicitly
* Game logic is deterministic
* Scope rules are respected
* Code is readable and maintainable

This is the same structural thinking used in **real production CLI tools and games**, just applied to a learning-friendly terminal project.





```python
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
```

```
SAMPLE TERMINAL FLOW (ABBREVIATED)

╔══════════════════════════════════════╗
║     🎯 NUMBER GUESSING GAME 🎯       ║
╚══════════════════════════════════════╝

Enter number of players: 2
Enter name for Player 1: Alex
Enter name for Player 2: Sam

Choose Difficulty:
1. Easy (1–10, 5 guesses)
2. Medium (1–50, 7 guesses)
3. Hard (1–100, 10 guesses)
4. Extreme (1–500, 12 guesses)
Enter choice: 1

🎲 ROUND 1 | Range: 1–10 | Max guesses: 5

Alex | Guesses left: 5
Enter your guess: 5
Too LOW 🔽

Sam | Guesses left: 5
Enter your guess: 7
██████╗ ██╗   ██╗███████╗███████╗

📊 ROUND 1 SUMMARY
Alex | Guesses: [5] | Success: False | Score: 0
Sam  | Guesses: [7] | Success: True  | Score: 4
```
