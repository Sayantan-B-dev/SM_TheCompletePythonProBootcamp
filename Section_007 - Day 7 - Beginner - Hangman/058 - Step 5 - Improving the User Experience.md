### step 5 — improving the user experience (clarity + feedback only)

---

### objective of this step

| aspect     | improvement                     |
| ---------- | ------------------------------- |
| visibility | show current word state clearly |
| feedback   | tell user correct / wrong guess |
| awareness  | show remaining lives            |
| context    | show guessed letters            |

No game-loop logic, no win/lose logic added here — only **presentation and feedback**.

---

### logic breakdown (UX-focused)

| order | operation                          |
| ----- | ---------------------------------- |
| 1     | display word with spaces           |
| 2     | show remaining lives               |
| 3     | show guessed letters so far        |
| 4     | print feedback message after guess |

---

### pseudocode (only UX layer)

```text
PRINT display word with spaces
PRINT lives remaining
PRINT guessed letters list

IF guess correct
    PRINT "Correct guess"
ELSE
    PRINT "Wrong guess"
ENDIF
```

---

### python code (isolated UX enhancement, fully commented)

```python
import random

# setup data (from previous steps)
word = random.choice(["apple", "grape"])
display = ["a", "_", "_", "l", "_"]   # example partially guessed word
lives = 5
guessed_letters = ["a", "l", "z"]

# show current game state clearly
print("\nCurrent word : ", " ".join(display))
print("Lives left   : ", lives)
print("Guessed so far:", ", ".join(guessed_letters))

# simulate a new guess
guessed_letter = input("\nGuess a letter: ").lower()

# UX feedback only (no state changes here)
if guessed_letter in word:
    print("Feedback: Correct guess 👍")
else:
    print("Feedback: Wrong guess ❌")
```

---

### sample output — correct guess

```
Current word :  a _ _ l _
Lives left   :  5
Guessed so far: a, l, z

Guess a letter: e
Feedback: Correct guess 👍
```

---

### sample output — wrong guess

```
Current word :  a _ _ l _
Lives left   :  5
Guessed so far: a, l, z

Guess a letter: x
Feedback: Wrong guess ❌
```

---

### UX principles applied

| principle          | explanation                        |
| ------------------ | ---------------------------------- |
| immediate feedback | user knows result instantly        |
| state visibility   | player sees progress clearly       |
| reduced confusion  | guessed letters prevent repetition |
| separation         | UX does not modify core logic      |

This step **only improves how the game feels to the player**, without changing the underlying mechanics.
