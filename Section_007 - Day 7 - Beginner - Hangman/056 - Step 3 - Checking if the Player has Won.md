### step 3 — checking if the player has won

---

### objective of this step

| item      | description                   |
| --------- | ----------------------------- |
| condition | no `_` left in display        |
| meaning   | all letters guessed correctly |
| output    | win / not yet won             |

---

### logic breakdown (only win-check logic)

| order | operation                |
| ----- | ------------------------ |
| 1     | inspect the display list |
| 2     | check if `_` exists      |
| 3     | decide win or continue   |

---

### pseudocode (strictly this step)

```text
IF "_" not in display
    PRINT "Player wins"
ELSE
    PRINT "Game continues"
ENDIF
```

---

### python code (isolated step, fully commented)

```python
# example display states
display = ['a', 'p', 'p', 'l', 'e']   # all letters guessed
# display = ['a', '_', 'p', 'l', '_'] # not yet complete

# win check
if "_" not in display:
    # no blanks means all letters are revealed
    print("Player wins")
else:
    # at least one blank still exists
    print("Game continues")
```

---

### sample output — win case

```
Player wins
```

---

### sample output — not yet won case

```
Game continues
```

---

### key concept explained

| concept              | explanation                         |
| -------------------- | ----------------------------------- |
| `"_" not in display` | checks completion in one expression |
| list membership      | fast and readable win condition     |
| separation of logic  | win-check does not modify state     |

This step **only answers one question**: *is the word fully revealed or not?*
