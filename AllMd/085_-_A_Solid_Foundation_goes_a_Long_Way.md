1. Always separate **game state** from **game flow**.
   In blackjack, cards, hands, totals, balance, and bets are *state*. Turns, rounds, and decisions are *flow*. Mixing them causes bugs that are hard to trace. Your clean separation into Step 1–5 is exactly how real games are engineered.

2. Ace handling is a classic hidden trap.
   The “count as 11 first, downgrade later” strategy is the safest pattern. Never decide Ace’s value upfront. Let the total overflow first, then fix it. This pattern appears again in inventory limits, stamina systems, and RPG stat caps.

3. Prefer **pure functions** whenever possible.
   `calculate_hand_value`, `resolve_round`, and `dealer_turn` work best because they depend only on inputs and return outputs. Fewer side effects = easier debugging, easier testing, easier extensions.

4. Control loops decide game correctness.
   Most bugs in games are loop bugs, not math bugs.
   You used:

* `while True` for player decisions
* conditional breaks for stand/bust/double
  This ensures the loop exits only when the game state demands it.

5. Always validate user input at the boundary.
   The terminal is hostile. Users will press Enter, type words, type symbols, or negative numbers. Input validation should happen immediately, before logic consumes it. You handled this correctly in betting and action selection.

6. Design rules as code, not comments.
   Dealer logic is a perfect example:
   “Dealer hits until total >= 17”
   That rule is embedded directly into the `while` condition. When rules are encoded structurally, they can’t be “forgotten” later.

7. Return **status flags**, not assumptions.
   Using `"bust"`, `"stand"`, `"win"`, `"lose"` avoids guessing what happened. Flags make control flow explicit and readable. This is the same pattern used in real engines and APIs.

8. Build vertically, not horizontally.
   You finished one *complete* feature path (deal → play → resolve → loop) before adding extras like split or blackjack payout. This prevents half-built systems and keeps motivation high.

9. Terminal UX still matters.
   Even without graphics:

* Clear spacing
* Explicit messages (“Dealer reveals hidden card”)
* Predictable prompts
  These reduce cognitive load and make logic easier to verify while testing.

10. If a feature touches more than one step, pause.
    Split, insurance, and blackjack payouts all affect:

* Step 2 (player options)
* Step 4 (resolution)
* Step 5 (balance update)
  That’s your signal to refactor before adding complexity.

11. Debug by printing **state snapshots**, not guesses.
    When something feels wrong, print:

* Hands
* Totals
* Bet
* Status flags
  Games are state machines; seeing the state reveals the bug immediately.

12. This blackjack project already teaches:

* Data modeling
* Loop control
* Deterministic AI behavior
* Input validation
* Modular design
* State transitions

That’s not “just a game”; it’s a compressed software engineering lesson.
