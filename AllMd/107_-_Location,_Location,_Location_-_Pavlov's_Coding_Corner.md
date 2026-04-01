1. Always design the data model before writing logic. Clearly separating configuration data (like `MENU`) from mutable runtime state (like `resources` and `money_earned`) makes the system predictable and easier to reason about.

2. Think in terms of real-world behavior first, then translate it into code. The rule “no money without resources, no resources without money” is a domain rule, not a programming trick. When domain rules are clear, the code structure naturally improves.

3. Avoid deep nesting. Nested `if` blocks quickly reduce readability and increase bug risk. Prefer early exits (`continue`, `return`) and flat control flow to make logic easier to follow and debug.

4. Aggregate before validating. When dealing with multiple selections (a cart), always compute total requirements first, then validate once. This avoids partial checks and prevents inconsistent states.

5. Separate responsibilities strictly. A function should do one thing only: checking resources, taking payment, deducting ingredients, or printing UI. Mixed responsibilities are the fastest way to introduce subtle bugs.

6. Treat money and resources as critical state. Update them only at well-defined points, and only after all validations succeed. This mirrors transactional thinking used in real systems.

7. Prefer data-driven design over hard-coded logic. Looping over dictionaries (`MENU`, `coins`, `cart`) is more scalable and less error-prone than writing special cases for each product or coin.

8. Design for failure, not success. Most real bugs happen in error paths. Handle insufficient resources, invalid input, empty carts, and payment failure explicitly and early.

9. Keep user input at the edges. Collect input in the main loop, then pass clean data (like a cart or total cost) into functions. This makes functions easier to test and reuse.

10. Use clear, consistent naming. Names like `check_resources`, `make_order`, and `take_payment` communicate intent immediately, reducing the need for comments and lowering cognitive load.

11. Maintain a predictable execution order. Input → validation → payment → state mutation → confirmation. If this order is ever violated, logic errors almost always appear.

12. Avoid global mutation inside functions when possible. Return values that describe outcomes and apply state changes in one controlled place, usually in the main loop.

13. Design your UI for humans, not just machines. Simple separators, consistent menus, and clean output formatting dramatically improve usability, even in terminal programs.

14. Build extensibility into the first version. A structure that supports multiple products, quantities, and single-payment flow is much easier to extend than one that handles only one item at a time.

15. Treat this as a system, not a script. Thinking in terms of states, transitions, and invariants prepares you for larger applications, APIs, and real production code later.
