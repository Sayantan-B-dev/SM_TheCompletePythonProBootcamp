### step 1 — pick a random word and check letters using a `for` loop

---

### goal of this step

| item   | meaning                                                               |
| ------ | --------------------------------------------------------------------- |
| task   | select a random word and compare each character with a guessed letter |
| input  | a single guessed letter                                               |
| output | whether the letter exists and where                                   |

---

### logic breakdown (micro-steps)

| order | operation                                  |
| ----- | ------------------------------------------ |
| 1     | store words in a list                      |
| 2     | pick one word randomly                     |
| 3     | take one letter as input                   |
| 4     | loop through each character in the word    |
| 5     | compare guessed letter with each character |
| 6     | print match positions                      |

---

### pseudocode (only this step)

```text
SET word_list
SELECT random word from word_list
INPUT guessed_letter

FOR each index in word
    IF word[index] == guessed_letter
        PRINT "Match found at index"
    ENDIF
ENDFOR
```

---

### python code (isolated step only)

```python
import random

# 1. list of possible words
word_list = ["apple", "banana", "grape"]

# 2. pick a random word
word = random.choice(word_list)

# 3. user guesses a letter
guessed_letter = input("Guess a letter: ").lower()

# 4. check each letter using for loop
found = False

for index in range(len(word)):
    if word[index] == guessed_letter:
        print(f"Match found at position {index}")
        found = True

# 5. result if not found
if not found:
    print("No match found")

# debug visibility
print("Selected word was:", word)
```

---

### sample output

```
Guess a letter: a
Match found at position 0
Selected word was: apple
```

```
Guess a letter: z
No match found
Selected word was: grape
```

---

### key concept clarified

| concept            | explanation                            |
| ------------------ | -------------------------------------- |
| `random.choice()`  | selects one random element from a list |
| `range(len(word))` | gives index access to each character   |
| `word[index]`      | retrieves a single letter              |
| `found` flag       | tracks whether any match occurred      |

This is the **lowest atomic unit** of hangman logic: word selection + letter scanning.
