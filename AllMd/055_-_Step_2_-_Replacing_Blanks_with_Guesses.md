### step 2 — show blanks (`_`), take guess, replace correctly matched letters

---

### objective of this step

| item           | description                          |
| -------------- | ------------------------------------ |
| input          | a guessed letter                     |
| internal state | word, display list (`_ _ _`)         |
| output         | updated display after checking guess |

---

### logic breakdown (strictly this step)

| order | operation                             |
| ----- | ------------------------------------- |
| 1     | create a display list filled with `_` |
| 2     | take guessed letter                   |
| 3     | loop through word characters          |
| 4     | if match → replace `_` with letter    |
| 5     | show updated display                  |

---

### pseudocode (focused only on this step)

```text
SET word
SET display as list of "_" same length as word

INPUT guessed_letter

FOR each index in word
    IF word[index] == guessed_letter
        display[index] = guessed_letter
    ENDIF
ENDFOR

PRINT display
```

---

### python code (isolated step only, heavily commented)

```python
import random

# predefined word list
word_list = ["apple", "grape", "banana"]

# pick a random word
word = random.choice(word_list)

# create display with blanks
display = ["_"] * len(word)

print("Initial display:", " ".join(display))

# take user input
guessed_letter = input("Guess a letter: ").lower()

# check and replace blanks
for i in range(len(word)):
    # compare each character of word with guessed letter
    if word[i] == guessed_letter:
        display[i] = guessed_letter  # replace blank with letter

# show updated display
print("Updated display:", " ".join(display))

# debug visibility
print("Actual word was:", word)
```

---

### sample output — correct guess

```
Initial display: _ _ _ _ _
Guess a letter: a
Updated display: a _ _ _ _
Actual word was: apple
```

---

### sample output — incorrect guess

```
Initial display: _ _ _ _ _
Guess a letter: z
Updated display: _ _ _ _ _
Actual word was: apple
```

---

### important concepts clarified

| concept                       | explanation                         |
| ----------------------------- | ----------------------------------- |
| `["_"] * len(word)`           | creates blank placeholders          |
| `display[i] = guessed_letter` | replaces only matched positions     |
| `display` as list             | lists are mutable (strings are not) |
| `" ".join(display)`           | formats output cleanly              |

This step **only handles visual state update** — no lives, no win/lose, no repetition handling.
