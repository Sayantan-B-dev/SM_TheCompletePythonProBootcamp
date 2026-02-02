REQUIREMENTS (FUNCTIONAL + NON-FUNCTIONAL)

Functional requirements
• A predefined dataset of entities with numeric attributes (example: celebrities with follower counts).
• Random selection of two distinct entities: A and B.
• Display partial information (name, description, country) but hide the numeric value.
• Player input: guess whether B is higher or lower than A.
• Validation of input (only “higher / lower” or h / l).
• Score tracking that increments on every correct guess.
• Immediate loss on the first incorrect guess.
• Reveal correct values after each round.
• Continuous gameplay loop until failure.
• Final score display and game reset option.

Non-functional requirements
• Runs entirely in terminal (no GUI dependency).
• Fast feedback loop (no unnecessary delays).
• Deterministic logic, nondeterministic data order.
• Simple I/O so beginners can understand the flow.
• Clean separation of data, logic, and game loop.

────────────────────────────────────────────

CORE GAME ALGORITHM (LOGIC VIEW)

1. Initialize score = 0
2. Load dataset into memory
3. Randomly pick entity A
4. Randomly pick entity B (must not equal A)
5. Display entity A info
6. Display entity B info
7. Ask player for guess
8. Compare values
9. If correct
   • score += 1
   • B becomes new A
   • repeat loop
10. Else
    • end game
    • show final score

This loop structure is the heart of the game’s addictiveness.

────────────────────────────────────────────

PSEUDOCODE (LANGUAGE-AGNOSTIC)

START GAME
score ← 0
data ← load_entities

A ← random_choice(data)

WHILE True
B ← random_choice(data)
WHILE B == A
B ← random_choice(data)

```
DISPLAY A.name, A.description  
DISPLAY B.name, B.description  

guess ← USER_INPUT("Higher or Lower?")  

IF B.value > A.value  
    correct_answer ← "higher"  
ELSE  
    correct_answer ← "lower"  

IF guess == correct_answer  
    score ← score + 1  
    DISPLAY "Correct! Current score:", score  
    A ← B  
ELSE  
    DISPLAY "Wrong!"  
    DISPLAY "Final score:", score  
    BREAK  
```

END GAME

────────────────────────────────────────────

FLOW CHART (LOGIC FLOW)

START
↓
Initialize score
↓
Pick random A
↓
Pick random B (≠ A)
↓
Display A & B
↓
Player guess
↓
Compare values
↓
Is guess correct?
┌───────────────┐
│ YES           │ NO
│               │
score +1         Game Over
│               │
B becomes A      Show score
│               │
Repeat loop      END

────────────────────────────────────────────

GAME PLANNING (DECOMPOSITION STRATEGY)

Step 1: Data Design
• Decide entity structure
{ name, description, value }
• Store as list of dictionaries

Step 2: Random Selection Logic
• Use randomness but enforce uniqueness
• Avoid repetition frustration

Step 3: Comparison Engine
• Single responsibility function
• Takes two values → returns “higher” or “lower”

Step 4: Input Handling
• Normalize input (lowercase, strip spaces)
• Reject invalid guesses

Step 5: Game Loop
• Infinite loop with controlled break
• Score persistence inside loop

Step 6: Feedback System
• Immediate correctness feedback
• Reveal hidden values every round

────────────────────────────────────────────

FEATURES THAT MAKE IT ADDICTIVE (DESIGN PSYCHOLOGY)

• Binary decision making
Reduces cognitive load → faster engagement

• Immediate feedback
Dopamine loop: guess → result → score

• Escalating tension
Every correct answer increases loss aversion

• No recovery after failure
One mistake = reset → “just one more try” effect

• Familiar information, hidden truth
Humans love testing intuition against facts

• Short rounds
Perfect for rapid replay loops

• Progressive difficulty illusion
Difficulty feels higher as score increases, even if logic stays constant

────────────────────────────────────────────

WHY IT’S A “PERFECT” TERMINAL GAME

• Minimal rules, maximum replayability
• Pure logic, no graphics dependency
• Teaches conditionals, loops, randomness, state
• Scales easily (add difficulty, streaks, hints)
• Clear win/lose conditions
• Beginner-friendly yet psychologically engaging

────────────────────────────────────────────

EXTENSION IDEAS (FOR LATER EVOLUTION)

• Streak bonuses
• Timed mode
• Difficulty tiers (close numbers vs far apart)
• Leaderboard (file persistence)
• Hint system with score penalty
• Category selection

Everything above maps cleanly into Python without complexity inflation.
