### Python Code

```python
print("Welcome to the tip calculator!")

bill = float(input("What was the total bill? $"))
tip = int(input("How much tip would you like to give? 10, 12, or 15? "))
people = int(input("How many people to split the bill? "))

total_with_tip = bill * (1 + tip / 100)
amount_per_person = total_with_tip / people

final_amount = round(amount_per_person, 2)

print(f"Each person should pay: ${final_amount}")
```
