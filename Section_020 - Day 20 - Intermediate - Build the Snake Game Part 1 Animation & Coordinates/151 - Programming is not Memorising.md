## TIPS ON SO-FAR LEARNING (SNAKE GAME — DAY 1)

---

## 1. THINK IN SYSTEMS, NOT LINES OF CODE

> Games are **loops + state + events**, not sequential scripts.

* The program never “finishes”
* The loop runs forever
* Each frame:

  * Reads current state
  * Applies logic
  * Renders output

**Mental shift**

* Stop thinking: “What runs next?”
* Start thinking: “What changes every frame?”

---

## 2. SEPARATE RESPONSIBILITIES EARLY

| Responsibility  | Where it belongs             |
| --------------- | ---------------------------- |
| Screen setup    | `main.py`                    |
| Game loop       | `main.py`                    |
| Snake creation  | `Snake` class                |
| Snake movement  | `Snake.move()`               |
| Direction rules | `Snake.up/down/left/right()` |

**Why this matters**

* Prevents tangled logic
* Makes debugging surgical
* Enables reuse (reset, restart, AI snake)

---

## 3. DATA STRUCTURES DRIVE BEHAVIOR

> The snake works because of **ordered data**, not graphics.

* `segments` list order = movement logic
* Index `0` always means **head**
* Reverse iteration avoids overwriting positions

**Key realization**

* Visual motion is a **side-effect**
* The real logic is list manipulation

---

## 4. BACKWARD ITERATION IS A GAME PATTERN

```text
Tail ← Body ← Neck ← Head
```

**Why this pattern appears often**

* Snake
* Train cars
* Particle chains
* Follow cameras

**Rule**

> When something follows something else, iterate backward.

---

## 5. CONSTANTS ARE NOT OPTIONAL

| Constant             | Why it exists       |
| -------------------- | ------------------- |
| `MOVE_DISTANCE`      | Grid alignment      |
| `STARTING_POSITIONS` | Reset capability    |
| Direction angles     | Logical constraints |

**Avoid**

* Magic numbers inside methods
* Hardcoded values in logic

---

## 6. INPUT SHOULD CHANGE STATE, NOT POSITION

**What you did right**

* Key press → changes heading
* Game loop → applies movement

**Why this is professional**

* Smooth animation
* No stuttering
* No frame skipping

**Anti-pattern**

> Moving objects directly inside key handlers

---

## 7. PREVENT INVALID STATES EARLY

Direction checks:

```text
UP    cannot go DOWN
LEFT  cannot go RIGHT
```

**Why this matters**

* Prevents impossible states
* Simplifies collision logic later
* Avoids edge-case bugs

> Good code prevents bugs instead of fixing them later.

---

## 8. TURTLE IS A TOOL, NOT THE LOGIC

* Turtle only:

  * Draws
  * Moves
  * Rotates
* **Your logic decides**:

  * When
  * Where
  * Why

**Key insight**

> You are not “programming turtle”
> You are using turtle to visualize your logic.

---

## 9. OOP IS ABOUT OWNERSHIP

Ask this question constantly:

> “Who owns this behavior?”

| Behavior       | Owner               |
| -------------- | ------------------- |
| Move snake     | Snake               |
| Listen to keys | Screen              |
| Run loop       | Main                |
| Track score    | Scoreboard (future) |

If ownership feels unclear → design issue.

---

## 10. DEBUGGING STRATEGY FOR GAMES

**When something breaks**

1. Print segment positions
2. Check list order
3. Verify heading before movement
4. Slow down `sleep()` to observe frames

**Golden rule**

> If you can’t explain what happens in one frame, you don’t understand the bug.

---

## 11. WHAT YOU SHOULD FEEL RIGHT NOW

* The snake feels **mechanical**, not magical
* Movement feels predictable
* Code feels readable

That’s correct.

Games feel simple **only after** the foundation is solid.

---

## 12. READY FOR NEXT PHASE BECAUSE

You now understand:

* Frame-based animation
* Event-driven input
* Object responsibility
* Movement algorithms

Which means:

* Food spawning
* Collision detection
* Growth logic
* Scoring

will feel **logical**, not overwhelming.
