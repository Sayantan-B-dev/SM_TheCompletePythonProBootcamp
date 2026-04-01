```python
# A dictionary that stores student names as keys
# and their corresponding scores as values
student_scores = {
    'Harry': 88,
    'Ron': 78,
    'Hermione': 95,
    'Draco': 75,
    'Neville': 60
}

# Function that takes a numeric score as input
# and returns a grade string based on score range
def check_grade(score):

    # If score is between 91 and 100 (inclusive)
    # return the highest grade
    if 91 <= score <= 100:
        return "Outstanding"

    # If score is between 81 and 90 (inclusive)
    # return second highest grade
    if 81 <= score <= 90:
        return "Exceeds Expectations"

    # If score is between 71 and 80 (inclusive)
    # return acceptable performance
    if 71 <= score <= 80:
        return "Acceptable"

    # If score is 70 or below
    # return fail
    if score <= 70:
        return "Fail"

# Empty dictionary to store final results
# keys   -> student names
# values -> grade strings returned by check_grade()
student_grades = {}

# Looping through the dictionary student_scores
# By default, iterating over a dictionary gives KEYS
for student in student_scores:

    # student            -> current key (student name)
    # student_scores[student] -> value (score of that student)

    # Pass the score to check_grade()
    # Store returned grade in student_grades dictionary
    student_grades[student] = check_grade(student_scores[student])

# Print the final dictionary containing grades
print(student_grades)
```

Output:

```
{
 'Harry': 'Exceeds Expectations',
 'Ron': 'Acceptable',
 'Hermione': 'Outstanding',
 'Draco': 'Acceptable',
 'Neville': 'Fail'
}
```

---

### Important behavior notes (logic-level)

* `for student in student_scores:`
  iterates over **keys**, not values.
* `student_scores[student]`
  fetches the score using the key.
* `check_grade()`
  returns **exactly one string** because only one condition matches.
* Dictionary assignment
  `student_grades[student] = value`
  creates a new key if it doesn’t exist, updates if it does.
* Order of output
  follows **insertion order of student_scores** (Python 3.7+).
