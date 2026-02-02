### breaking a complex problem into smaller problems (systematic method)

**core idea**: convert a vague goal into a sequence of deterministic decisions and actions. every box in a flowchart must answer only one question or perform only one action.

---

### step 1: define the problem clearly (single sentence)

| item              | description                                          |
| ----------------- | ---------------------------------------------------- |
| goal              | user guesses a hidden word letter by letter          |
| success condition | user guesses all letters before running out of lives |
| failure condition | lives reach zero                                     |
| inputs            | word to guess, user letter input                     |
| outputs           | win / lose message, current word state               |

---

### step 2: identify major phases (top-level decomposition)

| phase          | responsibility                   |
| -------------- | -------------------------------- |
| initialization | setup word, lives, empty guesses |
| game loop      | keep asking for guesses          |
| validation     | check input correctness          |
| update state   | reveal letters or reduce lives   |
| termination    | win or lose                      |

Each **phase becomes a flowchart block group**.

---

### step 3: break each phase into atomic actions

**initialization**

* choose word
* set lives
* create display (underscores)

**game loop**

* show current state
* ask for input
* check win/lose

**validation**

* single letter?
* already guessed?

**update**

* correct → update display
* wrong → lose life

---

### step 4: translate into flowchart logic (decision-driven)

![Image](https://inventwithpython.com/invent4thed/images/00081.jpeg)

![Image](https://inventwithpython.com/invent4thed/images/00089.jpeg)

**mental rule while drawing**

* rectangle → action
* diamond → yes/no question
* arrows → flow of control
* only ONE decision per diamond

---

### step 5: hangman flowchart logic (written form)

| order | type     | description                     |
| ----- | -------- | ------------------------------- |
| 1     | start    | begin program                   |
| 2     | process  | select random word              |
| 3     | process  | set lives = 6                   |
| 4     | process  | display underscores             |
| 5     | decision | lives > 0 AND word not guessed? |
| 6     | input    | ask user for letter             |
| 7     | decision | letter already guessed?         |
| 8     | decision | letter in word?                 |
| 9a    | process  | reveal letter                   |
| 9b    | process  | lives -= 1                      |
| 10    | decision | word fully revealed?            |
| 11a   | output   | win                             |
| 11b   | output   | lose                            |
| 12    | end      | stop program                    |

---

### step 6: convert flowchart → pseudocode (1-to-1 mapping)

```text
START
SET word = random word
SET lives = 6
SET guessed_letters = empty set
SET display = "_" for each letter in word

WHILE lives > 0 AND display contains "_"
    SHOW display
    INPUT letter

    IF letter in guessed_letters
        SHOW "Already guessed"
        CONTINUE LOOP
    ENDIF

    ADD letter to guessed_letters

    IF letter in word
        FOR each position in word
            IF word[position] == letter
                display[position] = letter
            ENDIF
        ENDFOR
    ELSE
        lives = lives - 1
    ENDIF
ENDWHILE

IF "_" not in display
    SHOW "You win"
ELSE
    SHOW "You lose"
ENDIF
END
```

---

### step 7: python implementation (directly from pseudocode)

```python
import random

# initialization
word = random.choice(["apple", "banana", "grape"])
lives = 6
guessed_letters = set()
display = ["_"] * len(word)

# game loop
while lives > 0 and "_" in display:
    print("Word:", " ".join(display))
    print("Lives:", lives)
    letter = input("Guess a letter: ").lower()

    # validation
    if letter in guessed_letters:
        print("Already guessed\n")
        continue

    guessed_letters.add(letter)

    # update state
    if letter in word:
        for i in range(len(word)):
            if word[i] == letter:
                display[i] = letter
        print("Correct!\n")
    else:
        lives -= 1
        print("Wrong!\n")

# termination
if "_" not in display:
    print("You win! Word was:", word)
else:
    print("You lose! Word was:", word)
```

---

### sample output (example run)

```
Word: _ _ _ _ _
Lives: 6
Guess a letter: a
Correct!

Word: a _ _ _ _
Lives: 6
Guess a letter: z
Wrong!

Word: a _ _ _ _
Lives: 5
Guess a letter: p
Correct!

Word: a p p _ _
Lives: 5
Guess a letter: l
Correct!

Word: a p p l _
Lives: 5
Guess a letter: e
Correct!

You win! Word was: apple
```

---

### step 8: universal rule to break any complex problem

| rule | explanation                |
| ---- | -------------------------- |
| 1    | write goal in one sentence |
| 2    | split into phases          |
| 3    | each phase → small actions |
| 4    | actions → decisions        |
| 5    | decisions → flowchart      |
| 6    | flowchart → pseudocode     |
| 7    | pseudocode → code          |

This exact pipeline works for games, APIs, backend systems, AI pipelines, anything.
