### Band Name Generator — Python Program

This is a beginner-friendly Python program that generates a band name by **combining user input**. It demonstrates core concepts like `input()`, variables, string concatenation, and output formatting.

---

### How It Works

* Ask the user for two inputs
* Store them in variables
* Combine them to form a band name
* Display the result

---

### Python Code

```python
print("Welcome to the Band Name Generator 🎸")

city = input("What's the name of the city you grew up in?\n")
pet = input("What's the name of your pet?\n")

band_name = city + " " + pet

print("Your band name could be:", band_name)
```

---

### Example Run

```text
Welcome to the Band Name Generator 🎸
What's the name of the city you grew up in?
Delhi
What's the name of your pet?
Tiger
Your band name could be: Delhi Tiger
```

---

### Concepts Used

* `input()` for user interaction
* Variables to store data
* String concatenation using `+`
* `print()` for output

---

### Professional Improvement (Optional)

Using f-strings:

```python
print(f"Your band name could be: {band_name}")
```

This project is simple by design and acts as a **foundation for interactive programs**, preparing you for more complex logic, conditions, and real-world applications later.
