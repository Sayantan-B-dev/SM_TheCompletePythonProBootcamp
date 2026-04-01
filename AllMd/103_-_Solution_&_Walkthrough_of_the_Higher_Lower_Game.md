BLOCK 1 — GAME GOAL & RULE DEFINITION
Decide exactly what the game is and what ends it.
• Player compares two items: A and B
• Player guesses whether B is higher or lower than A
• One wrong answer ends the game
• Score = number of consecutive correct guesses
This block fixes the win/lose condition and prevents scope creep later.

BLOCK 2 — DATA DESIGN
Define what a single game item looks like.
Each item must have:
• name (string)
• description (string)
• value (number used for comparison)

Example mental model (not code yet):
Item = { name, info, hidden_value }

Decide source of data:
• Hardcoded list (best for first version)
• All values must be comparable on the same scale

BLOCK 3 — RANDOM SELECTION LOGIC
Plan how items are chosen.
• Pick random item A
• Pick random item B
• Ensure A ≠ B
This avoids unfair repeats and keeps the game feeling fresh.

BLOCK 4 — DISPLAY STRATEGY
Decide what the player sees.
• Show name + description of A
• Show name + description of B
• Do NOT show numeric values
• Clearly label “Compare A vs B”
This block controls information asymmetry (core fun mechanic).

BLOCK 5 — INPUT HANDLING
Define how guesses are entered.
• Accept only higher / lower (or h / l)
• Convert input to lowercase
• Reject invalid input and re-ask
This block prevents crashes and player frustration.

BLOCK 6 — COMPARISON ENGINE
Isolate the logic that decides truth.
• Compare B.value with A.value
• Determine correct answer internally
• Do not mix this logic with input or printing
This makes the game predictable and testable.

BLOCK 7 — SCORING SYSTEM
Plan score behavior.
• Start score at 0
• Increment score only on correct guess
• Score persists across rounds
• Score resets only when game ends
This block creates progression and tension.

BLOCK 8 — GAME LOOP
Tie everything together in a loop.
Each iteration does:

1. Select B
2. Display A and B
3. Get guess
4. Check correctness
5. If correct → score++, set A = B
6. If wrong → break loop
   This is the backbone of the game.

BLOCK 9 — FEEDBACK MECHANISM
Decide what feedback appears after each guess.
• If correct → show updated score
• If wrong → reveal both values + final score
Immediate feedback reinforces learning and replay.

BLOCK 10 — GAME TERMINATION
Define clean ending behavior.
• Print “Game Over”
• Show final score
• Stop execution cleanly
Optional later: ask for replay (but not now).

BLOCK 11 — EDGE CASE HANDLING
Plan for failure points.
• Same item selected twice
• Invalid input
• Empty or broken data
• Non-numeric values
Handling this early prevents silent bugs.

BLOCK 12 — CODE STRUCTURE PLANNING
Before writing code, decide structure.
• data section
• helper functions (random pick, compare)
• main game loop
• execution guard (main)
This keeps the file readable and scalable.

BLOCK 13 — ADDICTIVENESS CHECK
Verify the loop satisfies these conditions:
• Short rounds
• Immediate consequence
• Increasing pressure
• No safety net
If yes, the design is complete.

BLOCK 14 — READY FOR IMPLEMENTATION
At this point, you can write code line by line without confusion.
No logic decisions remain—only translation into Python.
