• **Default to local scope**
Treat every variable as local unless you have a strong reason otherwise. Most bugs you faced came from accidentally sharing state.

• **Understand the assignment rule deeply**
The moment you assign to a name inside a function, Python marks it as local. This single rule explains `UnboundLocalError`, shadowing, and many “why is this broken?” moments.

• **Memorize LEGB, not as theory but as a debugger**
When a name behaves oddly, mentally trace: Local → Enclosing → Global → Built-in. Every scope bug resolves with this model.

• **Functions are the real scope boundary in Python**
`if`, `for`, `while` do not protect variables. Only `def`, `class`, `lambda`, and modules do. Design with this fact, not against it.

• **Avoid `global` in logic, tolerate it in configuration**
Globals are acceptable for constants, flags, and config. They are a design smell for scores, balances, user data, or game state.

• **Professional fix = return values, not mutation**
If a function needs to change something, return the new value and reassign outside. This keeps data flow visible and testable.

• **`nonlocal` is rare for a reason**
Use it only when writing closures intentionally. If you need it often, your design likely wants a class instead.

• **Late binding in loops is not a bug, it’s a rule**
Lambdas capture names, not values. If you want the value frozen, pass it explicitly (`i=i`). This applies everywhere, not just lambdas.

• **History-first design improves debugging**
Storing guesses, rounds, and outcomes made your game easier to reason about. This pattern scales to logs, audits, and analytics in real systems.

• **Score systems reveal design maturity**
Multipliers, remaining attempts, and difficulty-based rewards force you to think in constraints instead of ad-hoc increments.

• **Separate configuration from state**
Difficulty tables and ASCII art stayed global and safe because they never changed. Game state stayed local and controlled.

• **Comments explain “why”, not “what”**
Your best comments justified decisions (boundaries, rules, constraints), not obvious syntax. That’s professional commenting.

• **Docstrings are contracts, not decoration**
A good docstring tells what a function owns, what it mutates, and what it returns. If that’s unclear, the function is too big.

• **Terminal UX still follows software design rules**
Even ASCII art and fun text benefited from structure. UI chaos usually reflects logic chaos underneath.

• **When logic feels hard, it’s usually scope or state**
If a problem feels “mentally heavy”, check:
– Who owns the data?
– Who is allowed to change it?
– How far does it live?

• **You’re moving from syntax to systems thinking**
Writing code that runs is beginner level. Designing flow, constraints, and scope is the real skill you’ve been building.

If you can now explain *why* a variable lives where it lives and *who* is allowed to touch it, you’re no longer just learning Python—you’re learning software design.
