"""
===========================================================
 ROBUST TERMINAL BASED ADVANCED CALCULATOR
===========================================================

GOALS
- Handle ALL possible user errors safely
- Never crash the program
- Clear error messages
- Clean, readable, well-documented code
- Educational + professional structure
"""

# =========================
# STANDARD LIBRARIES
# =========================
import math
import os
import sys

# =========================
# GLOBAL HISTORY
# =========================
history = []

# =========================
# TERMINAL HELPERS
# =========================
def clear_screen():
    """Clear terminal screen safely"""
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass  

def pause():
    """Pause execution"""
    input("\nPress ENTER to continue...")

# =========================
# INPUT SAFETY FUNCTIONS
# =========================
def get_float(prompt):
    """Safely get float input"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid number. Please enter a numeric value.")

def get_int(prompt):
    """Safely get integer input"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Invalid integer. Please enter a whole number.")

# =========================
# ASCII UI
# =========================
def banner():
    print(r"""
╔══════════════════════════════════════╗
║      ADVANCED PYTHON CALCULATOR      ║
║        Safe • Stable • Clean         ║
╚══════════════════════════════════════╝
""")

def menu():
    print("""
[1] Basic Arithmetic
[2] Power / Modulus
[3] Factorial
[4] GCD & LCM
[5] Prime Check
[6] Fibonacci Series
[7] Percentage
[8] Scientific Operations
[9] History
[0] Exit
""")

# =========================
# CORE CALCULATIONS (ERROR SAFE)
# =========================

def basic_arithmetic(a, b, op):
    """Perform basic arithmetic with safety"""
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "❌ Error: Division by zero"
        return a / b
    else:
        return "❌ Error: Invalid operator"

def power_mod(a, b, mode):
    """Power or modulus with validation"""
    if mode == "power":
        return a ** b
    elif mode == "mod":
        if b == 0:
            return "❌ Error: Modulus by zero"
        return a % b
    return "❌ Error: Invalid mode"

def factorial(n):
    """Factorial with domain checking"""
    if n < 0:
        return "❌ Error: Factorial of negative number"
    if n > 1000:
        return "❌ Error: Number too large"
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def gcd_lcm(a, b):
    """GCD & LCM with zero handling"""
    if a == 0 and b == 0:
        return "❌ Error: GCD undefined for both zero", None
    gcd = math.gcd(a, b)
    lcm = abs(a * b) // gcd if gcd != 0 else 0
    return gcd, lcm

def is_prime(n):
    """Prime check with edge cases"""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    """Fibonacci generator with bounds"""
    if n <= 0:
        return "❌ Error: Enter a positive number"
    if n > 100:
        return "❌ Error: Too many terms requested"
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

def percentage(value, percent):
    """Percentage calculation"""
    return (value * percent) / 100

def scientific_ops(n):
    """Scientific calculations with math safety"""
    results = {}

    if n < 0:
        results["square_root"] = "❌ Undefined"
    else:
        results["square_root"] = math.sqrt(n)

    results["log10"] = math.log10(n) if n > 0 else "❌ Undefined"
    results["sine"] = math.sin(n)
    results["cosine"] = math.cos(n)

    return results

# =========================
# HISTORY FUNCTIONS
# =========================
def add_history(entry):
    history.append(entry)

def show_history():
    if not history:
        print("No calculations performed yet.")
        return
    print("\n──── CALCULATION HISTORY ────")
    for i, item in enumerate(history, 1):
        print(f"{i}. {item}")

# =========================
# MAIN LOOP (CRASH-PROOF)
# =========================
while True:
    clear_screen()
    banner()
    menu()

    choice = input("Choose an option: ").strip()

    if choice == "0":
        print("\nExiting calculator safely.")
        sys.exit()

    elif choice == "1":
        a = get_float("Enter first number: ")
        b = get_float("Enter second number: ")
        op = input("Operator (+ - * /): ").strip()
        result = basic_arithmetic(a, b, op)
        print("Result:", result)
        add_history(f"{a} {op} {b} = {result}")

    elif choice == "2":
        a = get_float("Enter base number: ")
        b = get_float("Enter second number: ")
        mode = input("Type 'power' or 'mod': ").lower()
        result = power_mod(a, b, mode)
        print("Result:", result)
        add_history(f"{mode}({a},{b}) = {result}")

    elif choice == "3":
        n = get_int("Enter integer: ")
        result = factorial(n)
        print("Result:", result)
        add_history(f"factorial({n}) = {result}")

    elif choice == "4":
        a = get_int("Enter first integer: ")
        b = get_int("Enter second integer: ")
        result = gcd_lcm(a, b)
        print("Result:", result)
        add_history(f"GCD/LCM({a},{b}) = {result}")

    elif choice == "5":
        n = get_int("Enter number: ")
        result = is_prime(n)
        print("Prime:", result)
        add_history(f"is_prime({n}) = {result}")

    elif choice == "6":
        n = get_int("Enter terms: ")
        result = fibonacci(n)
        print("Result:", result)
        add_history(f"fibonacci({n}) = {result}")

    elif choice == "7":
        value = get_float("Enter value: ")
        percent = get_float("Enter percentage: ")
        result = percentage(value, percent)
        print("Result:", result)
        add_history(f"{percent}% of {value} = {result}")

    elif choice == "8":
        n = get_float("Enter number: ")
        result = scientific_ops(n)
        for k, v in result.items():
            print(f"{k}: {v}")
        add_history(f"scientific_ops({n})")

    elif choice == "9":
        show_history()

    else:
        print("❌ Invalid menu choice.")

    pause()