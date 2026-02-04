## Step 1 — Evaluation of Understanding: How the Game Will Work

---

## 1. Core Objective (What the Player Is Trying to Do)

> Move a turtle character from the **bottom of the screen** to the **top of the screen**
> without colliding with horizontally moving cars.

This objective never changes.
Everything else in the game exists to **support or obstruct** this goal.

---

## 2. Static vs Dynamic Elements (Mental Separation)

### Static Elements (Do Not Move)

| Element             | Purpose          |
| ------------------- | ---------------- |
| Screen boundaries   | Define play area |
| Finish line (top Y) | Win condition    |
| Scoreboard text     | Player feedback  |

These elements define **rules and limits**, not gameplay motion.

---

### Dynamic Elements (Continuously Change)

| Element         | Behavior                       |
| --------------- | ------------------------------ |
| Turtle (player) | Moves only on user input       |
| Cars            | Move automatically every frame |
| Difficulty      | Increases after success        |

Dynamic elements are updated **inside the game loop**.

---

## 3. Time-Based Thinking (Frame Mental Model)

The game runs in **discrete frames**, not continuously.

```
Frame 1 → Update positions → Check rules → Draw
Frame 2 → Update positions → Check rules → Draw
Frame 3 → ...
```

Each loop iteration represents **one snapshot in time**.

**Key implication**

> Nothing “just happens” — every movement and check must occur inside the loop.

---

## 4. Player Control Model (Event-Driven)

### Input Behavior

| Action       | Trigger        |
| ------------ | -------------- |
| Move forward | Key press only |
| Stop         | Default state  |

Important understanding:

* Player movement is **not automatic**
* Player moves only when an **event occurs**
* Cars move **even if the player does nothing**

This creates tension and risk.

---

## 5. Car Behavior Model (Autonomous Obstacles)

Cars operate independently of the player.

### Conceptual Rules

```
Cars:
    spawn occasionally
    move left every frame
    disappear when off-screen
```

Cars do not:

* React to player
* Change direction
* Stop moving

They exist purely as **constraints**.

---

## 6. Interaction Model (Cause → Effect)

### Collision Interaction

```
IF turtle touches any car:
    game ends immediately
```

### Success Interaction

```
IF turtle reaches top boundary:
    level increases
    turtle resets
    cars move faster
```

Only **two outcomes** exist:

* Success (progress)
* Failure (termination)

---

## 7. Difficulty Progression Logic (Implicit Understanding)

Difficulty increases by:

* Faster cars
* Possibly more frequent spawns

It **does not** increase by:

* Smaller turtle
* Less control
* Random penalties

This keeps difficulty **fair and predictable**.

---

## 8. Responsibility Awareness (Who Does What)

At this stage, understanding should be:

| Component  | Responsibility    |
| ---------- | ----------------- |
| Player     | Movement only     |
| Cars       | Obstruction only  |
| Scoreboard | Information only  |
| Main loop  | Coordination only |

No component should “know too much”.

---

## 9. Failure & End-State Understanding

When the game ends:

* No movement continues
* No input is processed
* A message is displayed
* The loop stops

This is a **hard stop**, not a pause.

---

## 10. Conceptual Flow (Human Language Algorithm)

```
Game starts
Player waits
Cars move continuously
Player tries to cross
IF collision → game over
IF success → harder level
Repeat until failure
```

---

## Step 1 Completion Criteria (Self-Check)

You fully understand Step 1 if you can clearly answer:

* Who moves automatically?
* Who moves only by input?
* What ends the game?
* What increases difficulty?
* What happens in every frame?
