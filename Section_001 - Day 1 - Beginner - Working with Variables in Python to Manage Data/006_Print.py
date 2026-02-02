import logging
from pprint import pprint

# Configure logging to display section headers
logging.basicConfig(level=logging.INFO, format='%(message)s')

def log_header(title):
    logging.info(f"\n--- {title} ---")

log_header("Basic Printing")
print("Hello, World")
print(10)
print(3.14)

log_header("Variables")
name, age = "Alex", 25
print(f"Name: {name}, Age: {age}")

log_header("Print Formatting (sep/end)")
print("2026", "02", "01", sep="-")
print("Loading", end="...")
print("done")

log_header("String Formatting")
price = 49.5
print(f"Total price: ₹{price:.2f}")
print("Score: {} / {}".format(8, 10))

log_header("Special Characters & Raw Strings")
print("Line1\nLine2")
print("Column1\tColumn2")
print(r"C:\new_folder\test")

log_header("Data Structures")
print([1, 2, 3])
pprint({"a": 1, "b": {"x": 10, "y": 20}})

log_header("Functions & Logic")
def add(a, b):
    return a + b

result = add(2, 3)
print(f"Addition Result: {result}")

log_header("Iteration")
for i in range(3):
    print(f"Iteration: {i}")
