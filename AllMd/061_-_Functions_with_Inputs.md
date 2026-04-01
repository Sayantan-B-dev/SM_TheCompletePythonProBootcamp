### 1. Functions without inputs (no parameters)

These functions do not take any external data. They run the same way every time they are called.

```python
def greet():
    print("Hello, welcome to Python functions!")

greet()
```

**Output**

```
Hello, welcome to Python functions!
```

Explanation

* `greet` has no parameters.
* Parentheses `()` are empty.
* Data is hardcoded inside the function.

---

### 2. Functions with single input (parameter)

A parameter allows the function to receive data from outside.

```python
def greet_user(name):
    print("Hello", name)

greet_user("Sayantan")
```

**Output**

```
Hello Sayantan
```

Explanation

* `name` is a parameter.
* `"Sayantan"` is an argument.
* The function behavior changes based on input.

---

### 3. Functions with multiple inputs

Functions can take more than one parameter.

```python
def add_numbers(a, b):
    result = a + b
    print("Sum:", result)

add_numbers(10, 20)
```

**Output**

```
Sum: 30
```

Explanation

* `a` and `b` are parameters.
* Inputs are positional by default.
* Order matters unless specified otherwise.

---

### 4. Functions with input() inside them

Here, the function itself asks the user for input.

```python
def get_name_and_greet():
    name = input("Enter your name: ")
    print("Hello", name)

get_name_and_greet()
```

**Output (example user input)**

```
Enter your name: Rahul
Hello Rahul
```

Explanation

* `input()` always returns a string.
* The function controls user interaction.
* Useful for CLI-based programs.

---

### 5. Functions with input() and type conversion

Since `input()` returns a string, numeric operations require conversion.

```python
def add_two_numbers():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    print("Sum:", a + b)

add_two_numbers()
```

**Output (example user input)**

```
Enter first number: 5
Enter second number: 7
Sum: 12
```

Explanation

* `int()` converts string to integer.
* Without conversion, `+` would concatenate strings.

---

### 6. Functions with parameters AND input() together

Some inputs come from arguments, some from user input.

```python
def calculate_total(price):
    quantity = int(input("Enter quantity: "))
    total = price * quantity
    print("Total cost:", total)

calculate_total(50)
```

**Output (example user input)**

```
Enter quantity: 3
Total cost: 150
```

Explanation

* `price` comes from function call.
* `quantity` comes from user input.
* Mixed input sources are common in real apps.

---

### 7. Functions with default inputs

Default values are used if no argument is provided.

```python
def greet(name="Guest"):
    print("Hello", name)

greet()
greet("Amit")
```

**Output**

```
Hello Guest
Hello Amit
```

Explanation

* `"Guest"` is a default value.
* Default parameters must come after required ones.

---

### 8. Functions with variable number of inputs (*args)

Used when you don’t know how many inputs will be passed.

```python
def add_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    print("Total:", total)

add_all(1, 2, 3, 4)
```

**Output**

```
Total: 10
```

Explanation

* `*numbers` packs arguments into a tuple.
* Useful for flexible input sizes.

---

### 9. Functions with keyword inputs (**kwargs)

Used for named inputs.

```python
def show_profile(**details):
    for key, value in details.items():
        print(key, ":", value)

show_profile(name="Sayantan", age=22, skill="Python")
```

**Output**

```
name : Sayantan
age : 22
skill : Python
```

Explanation

* `**kwargs` stores inputs as a dictionary.
* Order does not matter.
* Keys must be strings.

---

### 10. Comparison table

| Function type  | Input source      | Example           |
| -------------- | ----------------- | ----------------- |
| No input       | None              | `greet()`         |
| Single input   | Argument          | `greet_user("A")` |
| Multiple input | Arguments         | `add(1,2)`        |
| input() inside | User              | `input()`         |
| Mixed input    | Argument + user   | `price + input()` |
| Default input  | Optional argument | `name="Guest"`    |
| *args          | Many values       | `(1,2,3)`         |
| **kwargs       | Named values      | `key=value`       |

---

### 11. Key rules to remember

* `input()` always returns `str`
* Convert input explicitly (`int`, `float`)
* Parameters ≠ arguments
* Logic should stay inside functions
* User interaction can be inside or outside functions depending on design
