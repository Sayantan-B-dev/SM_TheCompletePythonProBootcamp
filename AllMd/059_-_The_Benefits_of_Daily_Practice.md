### final combined hangman game (steps 1 → 5 together)

---

### complete logic flow (compressed)

| responsibility | how it works             |
| -------------- | ------------------------ |
| random word    | `random.choice()`        |
| blanks display | list of `_`              |
| guessing       | input one letter         |
| reveal letters | `for` loop over word     |
| lives          | decrease on wrong guess  |
| win check      | `"_" not in display`     |
| UX             | clear prints + ascii art |

---

### ascii art design (logical, single body, lava ground)

**rules followed**

* one head
* one torso
* two arms max
* two legs max
* lava as ground (`~~~~`)
* body grows with mistakes

```text
  +---+
  |   |
      |
      |
      |
      |
~~~~~~~~~~
```

---

### final python code (fully commented, readable)

```python
import random

# -------------------------------
# SETUP
# -------------------------------

# list of possible words
word_list = ["apple", "grape", "banana", "mango"]

# choose a random word
word = random.choice(word_list)

# create blank display
display = ["_"] * len(word)

# track guessed letters
guessed_letters = set()

# total lives
lives = 6

# hangman stages (lava theme)
stages = [
    """
      +---+
      |   |
          |
          |
          |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    ~~~~~~~~~~
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    ~~~~~~~~~~
    """
]

# -------------------------------
# GAME LOOP
# -------------------------------

while lives > 0 and "_" in display:

    # show visual state
    print(stages[6 - lives])
    print("Word :", " ".join(display))
    print("Lives:", lives)
    print("Guessed:", ", ".join(sorted(guessed_letters)))

    # take input
    guess = input("\nGuess a letter: ").lower()

    # validation: already guessed
    if guess in guessed_letters:
        print("You already guessed that letter.\n")
        continue

    guessed_letters.add(guess)

    # assume wrong guess
    is_correct = False

    # reveal letters
    for i in range(len(word)):
        if word[i] == guess:
            display[i] = guess
            is_correct = True

    # life handling
    if not is_correct:
        lives -= 1
        print("Wrong guess! Lava rises 🔥\n")
    else:
        print("Correct guess! Safe for now 😌\n")

# -------------------------------
# GAME END
# -------------------------------

print(stages[6 - lives])
print("Final word:", word)

if "_" not in display:
    print("YOU WIN 🏆 — escaped the lava!")
else:
    print("GAME OVER 💀 — fell into the lava!")
```

---

### sample output (shortened run)

```
  +---+
  |   |
      |
      |
      |
      |
~~~~~~~~~~

Word : _ _ _ _ _
Lives: 6
Guessed:

Guess a letter: a
Correct guess! Safe for now 😌

Word : a _ _ _ _
Lives: 6
Guessed: a
```

```
Guess a letter: z
Wrong guess! Lava rises 🔥

  +---+
  |   |
  O   |
      |
      |
      |
~~~~~~~~~~
```

```
GAME OVER 💀 — fell into the lava!
Final word: apple
```

---

### learning notes & tips (important)

| concept              | takeaway                             |
| -------------------- | ------------------------------------ |
| lists vs strings     | strings can’t be modified, lists can |
| `_` check            | simplest win condition               |
| flags (`is_correct`) | avoid duplicate logic                |
| `set()`              | prevents repeated guesses            |
| separation           | logic, visuals, input kept readable  |
| ascii stages         | index = mistakes made                |
| flow thinking        | each loop = one guess                |

**mental model to keep**

* one loop = one turn
* one responsibility per block
* visuals never control logic
* logic never prints randomly

If you can rewrite this without looking, you truly understood it.
