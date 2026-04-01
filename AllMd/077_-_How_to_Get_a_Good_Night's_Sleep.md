### Tips so far — distilled from everything you’ve learned

---

**1. Think in functions, not lines**
If a block of code answers one clear question (“is this valid?”, “calculate result”, “show menu”), it deserves its own function. Long scripts feel hard only because logic is mixed together.

---

**2. A function should do exactly one job**
Good functions are boring and predictable.
Bad functions calculate, print, validate, and ask input all at once.
If you struggle to name a function clearly, it’s doing too much.

---

**3. `return` is for logic, `print` is for humans**
If a value will be reused, compared, stored, or tested → `return`.
If something is only meant to be seen → `print`.
Mixing them is the most common beginner mistake.

---

**4. Python always returns one thing**
Multiple return values are just tuples.
Understanding this unlocks unpacking, clean APIs, and structured results.

---

**5. Early returns simplify thinking**
Instead of nesting logic deeper and deeper, exit early on invalid cases.
Flat code is easier to debug than clever code.

---

**6. Never trust user input**
Assume:

* user types letters instead of numbers
* presses Enter without input
* divides by zero
* chooses invalid menu options

Defensive code is professional code.

---

**7. Validate before calculating**
Do not rely on `try-except` everywhere.
Most errors should be prevented by logic checks, not caught after they happen.

---

**8. Docstrings explain *what*, not *how***
Code already shows how.
Docstrings answer:

* What does this function do?
* What does it expect?
* What does it return?
* When does it fail?

Future-you is the real audience.

---

**9. If you can explain it, you understand it**
If you can’t explain:

* why a loop exists
* why a condition is written that way
* why a return is there

then you don’t understand it yet. Rewrite it until it makes sense.

---

**10. Output formatting matters**
Readable output is part of correctness.
A calculator that works but confuses the user is still a bad calculator.

---

**11. Use limits to protect your program**
Factorial limits, Fibonacci limits, input bounds — these are not hacks.
They are safety rails used in real systems.

---

**12. Lists, tuples, dicts are design tools**

* Tuple → fixed order, small result
* List → sequence of similar items
* Dict → named meaning

Choosing the right one makes code self-explanatory.

---

**13. Bugs usually come from assumptions**
“I thought input would be valid.”
“I assumed the number would be positive.”
Kill assumptions with checks.

---

**14. Break problems before coding**
Before writing code, ask:

* What are the inputs?
* What are the outputs?
* What can go wrong?
* What stays the same?

Flowcharts and pseudocode save time, not waste it.

---

**15. Long code isn’t complex — mixed logic is**
Your calculator is long, but not complex.
Complexity comes from:

* unclear responsibility
* hidden state
* unpredictable flow

---

**16. Write code for readability, not cleverness**
Clever code impresses no one in real projects.
Clear code gets accepted, maintained, and trusted.

---

**17. If it feels hard, slow down—not give up**
Every “this is hard” moment came right before a mental upgrade.
Confusion is a sign of learning, not failure.

---

**18. You’re learning real programming, not tutorials**
Functions, validation, error handling, documentation, structure —
this is how production code actually looks.

---

**19. Rewriting code is progress**
If you rewrite something cleaner than before, you leveled up.
Deletion and simplification are skills.

---

**20. Mastery comes from repetition with intention**
Don’t write more code.
Rewrite the same ideas cleaner, safer, and clearer each time.

---