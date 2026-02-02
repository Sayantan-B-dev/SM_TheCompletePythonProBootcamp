### NUMBER GUESSING GAME — DESIGN PHASE ONLY

(multiplayer • difficulty-based • scoring • history • terminal UX)

---

## GAME FEATURES (DESIGN CONSTRAINTS)

* Terminal based
* Multiple difficulty levels

  * difficulty controls **number range** + **max guesses**
* Multiplayer (2+ players, turn-based)
* Score keeping across rounds
* Guess history (per player + per round)
* Fun ASCII + text feedback
* No global mutation abuse (state-driven design)

---

## DIFFICULTY MODEL

| Difficulty | Range | Max Guesses | Score Multiplier |
| ---------- | ----- | ----------- | ---------------- |
| Easy       | 1–10  | 5           | ×1               |
| Medium     | 1–50  | 7           | ×2               |
| Hard       | 1–100 | 10          | ×3               |
| Extreme    | 1–500 | 12          | ×5               |

---

## CORE DATA STRUCTURES (CONCEPTUAL)

```
players = [
  {
    name,
    score,
    history = [
        { round, guesses, success }
    ]
  }
]

game_state = {
  current_round,
  difficulty,
  secret_number,
  max_guesses,
  current_player_index,
  round_active
}
```

---

## HIGH-LEVEL GAME FLOW (TEXT FLOWCHART)

```
START
  ↓
SHOW ASCII TITLE
  ↓
INPUT number_of_players
  ↓
INPUT player_names
  ↓
INITIALIZE scores = 0
  ↓
WHILE player_wants_to_continue
  ↓
  SELECT difficulty
  ↓
  SET range & max_guesses
  ↓
  GENERATE secret_number
  ↓
  RESET round history
  ↓
  FOR each player (turn-based)
      ↓
      WHILE guesses_left AND not guessed
          ↓
          INPUT guess
          ↓
          VALIDATE guess
          ↓
          STORE guess in history
          ↓
          COMPARE guess
              → too high
              → too low
              → correct
      END WHILE
      ↓
      UPDATE score
      ↓
      SAVE round history
  END FOR
  ↓
  SHOW round summary
END WHILE
  ↓
SHOW FINAL SCOREBOARD
  ↓
END
```

---

## DETAILED ALGORITHM (STEP-BY-STEP)

---

### STEP 1 — GAME INITIALIZATION

```
DISPLAY game title ASCII
ASK for number of players
FOR each player
    ASK for name
    SET score = 0
    SET history = empty
END FOR
SET round = 1
```

---

### STEP 2 — DIFFICULTY SELECTION

```
DISPLAY difficulty menu
INPUT difficulty_choice

IF choice == Easy
    range = 1–10
    max_guesses = 5
    multiplier = 1
ELIF Medium
    range = 1–50
    max_guesses = 7
    multiplier = 2
ELIF Hard
    range = 1–100
    max_guesses = 10
    multiplier = 3
ELIF Extreme
    range = 1–500
    max_guesses = 12
    multiplier = 5
ELSE
    REPEAT selection
```

---

### STEP 3 — ROUND SETUP

```
GENERATE random secret_number within range
RESET round_history
DISPLAY round intro ASCII
```

---

### STEP 4 — PLAYER TURN LOGIC

```
FOR each player
    SET guesses_left = max_guesses
    SET player_guesses = empty list
    SET success = False

    WHILE guesses_left > 0 AND success == False
        DISPLAY guesses_left
        INPUT guess

        IF guess invalid
            DISPLAY error
            CONTINUE

        ADD guess to player_guesses
        guesses_left -= 1

        IF guess == secret_number
            DISPLAY success ASCII
            CALCULATE score += guesses_left * multiplier
            success = True
        ELSE IF guess < secret_number
            DISPLAY "Too Low"
        ELSE
            DISPLAY "Too High"
    END WHILE

    STORE player round history:
        round_number
        guesses
        success
END FOR
```

---

### STEP 5 — ROUND SUMMARY

```
DISPLAY round summary table
FOR each player
    SHOW name
    SHOW guesses
    SHOW success/fail
    SHOW score
END FOR
```

---

### STEP 6 — CONTINUE OR END

```
ASK "Play another round?"
IF yes
    round += 1
    GO TO difficulty selection
ELSE
    SHOW final scoreboard
    SHOW full history
    END GAME
```

---

## SCORING LOGIC (CLEAR RULE)

```
IF player guessed correctly
    score += guesses_left * difficulty_multiplier
ELSE
    score += 0
```

Optional penalty extension:

```
IF player fails
    score -= 1 (optional)
```

---

## GUESS HISTORY STRUCTURE (PER PLAYER)

```
history = [
  {
    round: 1,
    guesses: [12, 18, 20],
    success: True
  },
  {
    round: 2,
    guesses: [50, 40, 30],
    success: False
  }
]
```

---

## ASCII ART IDEAS (TERMINAL)

### TITLE

```
╔══════════════════════════════╗
║   🎯 NUMBER GUESSING GAME   ║
╚══════════════════════════════╝
```

### SUCCESS

```
  ██████╗  ██████╗ ██████╗ 
  ██╔══██╗██╔═══██╗██╔══██╗
  ██████╔╝██║   ██║██████╔╝
  ██╔═══╝ ██║   ██║██╔═══╝ 
  ██║     ╚██████╔╝██║     
```

### FAILURE

```
  ☠ GAME OVER ☠
  The number escaped...
```

---

## DESIGN PRINCIPLES USED

* No hidden global mutation
* State passed explicitly
* Deterministic scoring
* Extendable difficulty system
* History-first design
* Multiplayer-safe
* Terminal UX focused

---

Next step (when you ask):
👉 **convert this exact design into clean, commented Python terminal code**
(no logic changes, only implementation).
