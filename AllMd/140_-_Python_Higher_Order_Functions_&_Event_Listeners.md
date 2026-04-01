## Higher-Order Functions & Event Listeners in Python (Vanilla → Turtle)

![Image](https://miro.medium.com/1%2ATxDhmsq9LG0p4au_RULnVA.png)

![Image](https://i.sstatic.net/ZWHCF.png)

![Image](https://miro.medium.com/0%2ABdzrHhBRZ9LwBJFe)

![Image](https://i.sstatic.net/IYiGl.png)

---

## 1. Higher-Order Functions — Core Definition

A **higher-order function** is a function that does **at least one** of the following:

* Accepts another function as an argument
* Returns a function as its result

This is not a “functional programming trick”.
It is a **control mechanism** that allows behavior to be injected, delayed, or reused.

---

## 2. Functions as First-Class Objects (Foundation)

In Python:

* Functions are objects
* They can be stored in variables
* They can be passed without calling them
* They can be executed later

### Critical Distinction

| Expression  | Meaning                       |
| ----------- | ----------------------------- |
| `move_up`   | Reference to the function     |
| `move_up()` | Call the function immediately |

Event systems **require references**, not calls.

---

## 3. Vanilla Example — Passing a Function to Another Function

### Concept

* One function controls *when*
* Another function controls *what*

```python
def greet():
    print("Hello from the inner function")

def executor(action):
    """
    action → expected to be a function reference
    executor decides WHEN to execute it
    """
    print("Executor started")
    action()        # Function is called here
    print("Executor finished")

executor(greet)
```

### Expected Output

```
Executor started
Hello from the inner function
Executor finished
```

### Why This Is Higher-Order

* `executor` receives behavior (`greet`)
* Execution is **deferred**
* Logic and behavior are separated

---

## 4. Why This Matters for Events

Event systems **never know**:

* When a key will be pressed
* Which user action will occur
* How many times it will occur

So instead of executing logic immediately, they **store function references** and trigger them later.

This is where higher-order functions become mandatory.

---

## 5. Event Listener — Vanilla Concept (Simplified)

An event listener is:

> A function that registers another function to be executed later when a condition occurs

Pseudo-logic:

```
register(event, function_reference)
wait...
event happens
→ call function_reference
```

---

## 6. Turtle Screen = Real Event Listener System

`turtle.Screen()` is an **event dispatcher**.

It:

* Stores function references internally
* Maps them to user actions
* Calls them when the event fires

---

## 7. Turtle Example — Keyboard Event Listener

### Structure

* `Screen` → event manager
* `onkey` → higher-order function
* `move_up` → callback function

```python
import turtle

# -----------------------------
# SCREEN SETUP
# -----------------------------
screen = turtle.Screen()
screen.setup(600, 600)
screen.title("Higher-Order Functions with Turtle")

# -----------------------------
# PLAYER OBJECT
# -----------------------------
player = turtle.Turtle()
player.shape("turtle")
player.penup()

# -----------------------------
# CALLBACK FUNCTIONS
# -----------------------------
def move_up():
    """
    This function does NOT run immediately.
    It is passed as a reference to onkey().
    """
    player.sety(player.ycor() + 20)

def move_down():
    player.sety(player.ycor() - 20)

# -----------------------------
# EVENT REGISTRATION
# -----------------------------
screen.listen()

# Higher-order functions:
# onkey(callback_function, key)
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")

screen.mainloop()
```

### Expected Output (Behavior)

* Turtle appears at center
* Pressing `Up` moves turtle upward
* Pressing `Down` moves turtle downward
* No movement happens until a key event fires

---

## 8. What `onkey()` Really Is (Mental Model)

```python
def onkey(callback, key):
    store callback in event_table[key]
```

Later:

```python
if key_pressed:
    event_table[key]()
```

### Key Insight

* `onkey()` does **not** call your function
* It **stores** it
* Turtle calls it later when the event occurs

---

## 9. Higher-Order Function with Parameters (Advanced Pattern)

### Problem

Event listeners cannot pass arguments directly.

### Solution

Wrap logic inside another function.

```python
def move(distance):
    player.forward(distance)

def create_mover(distance):
    """
    Returns a function with distance remembered
    """
    def mover():
        move(distance)
    return mover

screen.onkey(create_mover(30), "Right")
screen.onkey(create_mover(-30), "Left")
```

### Expected Output

* Right key moves turtle forward
* Left key moves turtle backward
* Distance is preserved via closure

---

## 10. `ontimer()` — Higher-Order + Game Loop

Timers are event listeners for **time**, not input.

```python
def game_loop():
    player.forward(2)
    screen.ontimer(game_loop, 50)

game_loop()
```

### Expected Output

* Turtle moves continuously
* Movement happens every 50 milliseconds
* This is a real **game loop**

---

## 11. Event Listener vs Normal Function Call

| Aspect    | Normal Call      | Event Listener    |
| --------- | ---------------- | ----------------- |
| Execution | Immediate        | Deferred          |
| Control   | Caller           | Event system      |
| Arguments | Direct           | Usually none      |
| Use case  | Sequential logic | Interactive logic |

---

## 12. Why Turtle Makes This Click Instantly

Because you can **see**:

* When a function is not called
* When it suddenly executes
* What event caused it
* How behavior is decoupled from control

This visual feedback eliminates abstraction confusion.

---

## 13. Core Rule to Remember

> If a function is passed **without parentheses**,
> it is being treated as **data**, not an action.

That single rule explains:

* Higher-order functions
* Event listeners
* Callbacks
* GUI programming
* Game loops
