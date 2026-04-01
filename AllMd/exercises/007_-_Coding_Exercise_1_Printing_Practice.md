Here’s a dynamic version of the a that avoids hard-coded values and makes the instructions reusable and easy to update. Instead of writing multiple `print()` statements, the data is stored separately and injected into the text at runtime.

```python
steps = [
    "Mix {flour}g of flour, {yeast}g yeast and {water}ml water in a bowl.",
    "Knead the dough for {knead_time} minutes.",
    "Add {salt}g of salt.",
    "Leave to rise for {rise_time} hours.",
    "Bake at {temp}°C for {bake_time} minutes."
]

ingredients = {
    "flour": 500,
    "yeast": 10,
    "water": 300,
    "knead_time": 10,
    "salt": 3,
    "rise_time": 2,
    "temp": 200,
    "bake_time": 30
}

for index, step in enumerate(steps, start=1):
    print(f"{index}. {step.format(**ingredients)}")
```

This approach is more professional because it separates **logic**, **data**, and **output**, making the code cleaner, scalable, and easier to maintain or reuse.
