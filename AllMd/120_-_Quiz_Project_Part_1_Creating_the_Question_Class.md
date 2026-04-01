## STEP 1 — Define the **Question Model** (Foundation of the Game)

> If the **Question** class is weak, the entire quiz game collapses.
> Step 1 is about modeling **one perfect question object**.

No game loop.
No player.
No quiz flow.
Only **one question, done right**.

---

## 1. Purpose of Step 1

This step answers only these questions:

* What data does *one question* need?
* What behavior should *one question* control by itself?
* How do we **test a question in isolation**?

If this step feels solid, later steps become trivial.

---

## 2. Responsibilities of the `Question` Class

> A `Question` object must **know everything about itself**.

### It MUST:

* store the question text
* store multiple options
* know which option is correct
* display itself cleanly
* validate an answer

### It MUST NOT:

* track score
* ask for user input
* control game flow

---

## 3. Attributes Planning (Data Inside the Object)

| Attribute       | Type        | Why it exists           |
| --------------- | ----------- | ----------------------- |
| `text`          | `str`       | The question itself     |
| `options`       | `list[str]` | Possible answers        |
| `correct_index` | `int`       | Correct option position |

> Store the **index**, not the text — indexes are stable and fast to compare.

---

## 4. Methods Planning (Behavior)

| Method               | Purpose                 |
| -------------------- | ----------------------- |
| `display()`          | Show question + options |
| `is_correct(choice)` | Validate answer         |

These methods operate only on **this question’s data**.

---

## 5. Implementing Step 1 — Code

```python
class Question:
    def __init__(self, text, options, correct_index):
        # Store the question text
        self.text = text

        # Store list of answer options
        self.options = options

        # Store index of correct option (1-based for user friendliness)
        self.correct_index = correct_index

    def display(self):
        """
        Displays the question and its options.
        This method does NOT take input.
        It only presents data.
        """
        print(self.text)

        for index, option in enumerate(self.options, start=1):
            print(f"{index}. {option}")

    def is_correct(self, user_choice):
        """
        Checks whether the user's choice matches
        the correct option index.

        Returns:
            True  -> if correct
            False -> if wrong
        """
        return user_choice == self.correct_index
```

---

## 6. Testing the Question in Isolation (Critical Discipline)

> Never trust a class until you test it alone.

```python
q = Question(
    "Which data type is immutable?",
    ["list", "dict", "tuple", "set"],
    3
)

q.display()

answer = 3
print(q.is_correct(answer))
```

---

## 7. Expected Output

```
Which data type is immutable?
1. list
2. dict
3. tuple
4. set
True
```

---

## 8. Why Step 1 Is Complete (Checklist)

* Question data is encapsulated
* Behavior belongs to the question
* No external dependencies
* No premature abstraction
* Fully testable in isolation

If **any future step breaks**, you come back here.

---

## 9. Mental Lock-In for Step 1

> “A Question object is a self-contained unit of knowledge.”

