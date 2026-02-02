### BMI Calculator — Python Program

A **BMI (Body Mass Index) calculator** estimates whether a person is underweight, normal, overweight, or obese based on **height and weight**. This is a classic beginner project that combines **input**, **type conversion**, **math operations**, and **conditional logic**.

---

## BMI Formula

```
BMI = weight (kg) / (height (m) ** 2)
```

---

## BMI Categories (Standard)

| BMI Value   | Category      |
| ----------- | ------------- |
| < 18.5      | Underweight   |
| 18.5 – 24.9 | Normal weight |
| 25 – 29.9   | Overweight    |
| ≥ 30        | Obese         |

---

## Basic BMI Calculator Code

```python
print("Welcome to the BMI Calculator")

height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in kilograms: "))

bmi = weight / (height ** 2)
bmi = round(bmi, 2)

print(f"Your BMI is {bmi}")
```

---

## BMI Calculator with Category

```python
print("Welcome to the BMI Calculator")

height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in kilograms: "))

bmi = round(weight / (height ** 2), 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal weight"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print(f"Your BMI is {bmi}")
print(f"Category: {category}")
```

---

## Example Run

```
Welcome to the BMI Calculator
Enter your height in meters: 1.75
Enter your weight in kilograms: 70
Your BMI is 22.86
Category: Normal weight
```

---

## Key Concepts Used

* `input()` for user interaction
* `float()` for decimal values
* `**` for exponentiation
* Arithmetic operators
* `round()` for clean output
* `if / elif / else` conditions

---

## Common Beginner Mistakes

* Using height in **cm instead of meters**
* Forgetting to convert input to `float`
* Writing `height * height` instead of `height ** 2`
* Not rounding the final value

---

## Professional Improvement (Validation)

```python
try:
    height = float(input("Height (m): "))
    weight = float(input("Weight (kg): "))

    if height <= 0 or weight <= 0:
        print("Height and weight must be positive numbers.")
    else:
        bmi = round(weight / (height ** 2), 2)
        print(f"Your BMI is {bmi}")

except ValueError:
    print("Please enter valid numeric values.")
```

---

### Core Learning Outcome

This project teaches how **real-world formulas translate into code**, how to handle user input safely, and how to make decisions based on numeric ranges—skills you’ll reuse constantly in larger applications.
