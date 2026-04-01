### Tip Calculator — Program Documentation

This Python program calculates how much each person should pay when a bill is split among multiple people, including a selected tip percentage. It introduces **user input handling**, **type conversion**, **basic arithmetic**, and **formatted output**.

---

### Program Flow

1. Display a welcome message
2. Ask for the total bill amount
3. Ask for the tip percentage
4. Ask how many people will split the bill
5. Calculate the final amount per person
6. Display the result rounded to two decimal places

---

### Example Interaction

```
Welcome to the tip calculator!
What was the total bill? $
4567
How much tip would you like to give? 10, 12, or 15?
15
How many people to split the bill?
788
Each person should pay: $6.67
```

---

### Formula Used

```text
total_with_tip = bill + (bill × tip_percentage / 100)
amount_per_person = total_with_tip ÷ number_of_people
```

---

### Key Concepts Covered

* `input()` for user interaction
* `float()` and `int()` for type conversion
* Percentage calculations
* Division and rounding
* f-string formatting

---

### Notes

* `round(value, 2)` ensures currency-style output
* Input values must be valid numbers to avoid runtime errors
* This program builds the foundation for calculators, billing systems, and real-world finance logic

This project reinforces **clean data flow**, **basic math logic**, and **user-friendly output**, which are essential early Python skills.
