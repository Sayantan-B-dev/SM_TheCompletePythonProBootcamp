### step 4 — keeping track of the player’s lives

---

### objective of this step

| item    | description                      |
| ------- | -------------------------------- |
| purpose | reduce lives when guess is wrong |
| input   | guessed letter                   |
| state   | `lives` counter                  |
| output  | updated lives value              |

---

### logic breakdown (only lives logic)

| order | operation                      |
| ----- | ------------------------------ |
| 1     | initialize lives               |
| 2     | assume guess is wrong          |
| 3     | check if letter exists in word |
| 4     | if not found → reduce lives    |
| 5     | show remaining lives           |

---

### pseudocode (strictly this step)

```text
SET lives = 6

INPUT guessed_letter

IF guessed_letter not in word
    lives = lives - 1
ENDIF

PRINT lives
```

---

### python code (isolated step, heavily commented)

```python
import random

# select a random word
word_list = ["apple", "grape", "banana"]
word = random.choice(word_list)

# initialize lives
lives = 6

print("Word chosen (hidden):", word)
print("Initial lives:", lives)

# take user input
guessed_letter = input("Guess a letter: ").lower()

# check if guessed letter is NOT in the word
if guessed_letter not in word:
    lives -= 1  # reduce life for wrong guess
    print("Wrong guess! Life lost.")
else:
    print("Correct guess! No life lost.")

# show remaining lives
print("Remaining lives:", lives)
```

---

### sample output — wrong guess

```
Word chosen (hidden): apple
Initial lives: 6
Guess a letter: z
Wrong guess! Life lost.
Remaining lives: 5
```

---

### sample output — correct guess

```
Word chosen (hidden): apple
Initial lives: 6
Guess a letter: a
Correct guess! No life lost.
Remaining lives: 6
```

---

### key concepts clarified

| concept              | explanation                              |
| -------------------- | ---------------------------------------- |
| `lives` variable     | tracks remaining attempts                |
| `letter not in word` | direct membership test                   |
| decrement (`-=`)     | concise state update                     |
| separation           | lives logic independent of display logic |

This step **only manages penalties** and does not affect word display or win logic.
