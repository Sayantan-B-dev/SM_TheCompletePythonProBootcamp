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
