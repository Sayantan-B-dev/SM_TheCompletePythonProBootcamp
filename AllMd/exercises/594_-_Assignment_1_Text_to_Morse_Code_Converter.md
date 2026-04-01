# Morse Code Converter – Full Documentation

This document provides a complete explanation of the text‑based Morse code converter program. The program takes any string input from the user and outputs the equivalent Morse code. It supports letters (A–Z), digits (0–9), common punctuation, and spaces (converted to a forward slash `/`). Unsupported characters are replaced with a question mark (`?`).

---

## 1. Complete Code with Comments

Below is the full source code, with detailed inline comments explaining each section.

```python
# Morse Code Converter
# A text-based program that converts a string into Morse code.

# ----------------------------------------------------------------------
# 1. Morse code mapping dictionary
#    Maps each character (uppercase letter, digit, punctuation, space)
#    to its corresponding Morse code representation.
# ----------------------------------------------------------------------
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'   # space becomes slash
}

# ----------------------------------------------------------------------
# 2. Conversion function
#    Accepts a string and returns its Morse code equivalent.
# ----------------------------------------------------------------------
def text_to_morse(text):
    """
    Convert a plain text string to Morse code.

    Steps:
    - Convert the input to uppercase (dictionary keys are uppercase).
    - For each character, look up its Morse code in the dictionary.
    - If the character is not found, replace it with a '?'.
    - Join all Morse symbols with a single space to form the output.
    """
    text = text.upper()                 # Normalise to uppercase
    morse_parts = []                     # List to hold Morse symbols

    for char in text:                    # Iterate through each character
        if char in morse_code_dict:       # Check if character is supported
            morse_parts.append(morse_code_dict[char])
        else:
            # Unsupported character – use a placeholder
            morse_parts.append('?')

    return ' '.join(morse_parts)          # Combine symbols with spaces

# ----------------------------------------------------------------------
# 3. Main program loop
#    Handles user interaction: prompts for input, displays result,
#    and allows multiple conversions until the user types 'exit'.
# ----------------------------------------------------------------------
def main():
    """Run the interactive Morse code converter."""
    print("Welcome to the Morse Code Converter!")
    print("Enter your message (letters, numbers, and basic punctuation).")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your message: ").strip()   # Get input, remove extra spaces
        if user_input.lower() == 'exit':                # Exit condition
            print("Goodbye!")
            break
        if user_input == "":                             # Empty input – ask again
            print("Please enter a message.")
            continue

        morse_output = text_to_morse(user_input)         # Perform conversion
        print(f"Morse Code: {morse_output}\n")           # Display result

# ----------------------------------------------------------------------
# 4. Entry point
#    Ensures the main() function runs only when the script is executed
#    directly (not imported as a module).
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
```

---

## 2. Detailed Explanation of Each Part

### 2.1. Morse Code Dictionary

```python
morse_code_dict = { ... }
```

- **Purpose**: Provides a lookup table that maps each supported character to its Morse code sequence.
- **Keys**: All uppercase letters (`A`–`Z`), digits (`0`–`9`), and various punctuation marks. The space character `' '` is mapped to a forward slash `/` to visually separate words in the output.
- **Values**: Strings composed of dots (`.`) and dashes (`-`), as defined by the International Morse Code standard.
- **Why uppercase?** By storing keys in uppercase, we can easily normalise user input (convert to uppercase) before lookup, making the conversion case‑insensitive.

### 2.2. Conversion Function – `text_to_morse(text)`

```python
def text_to_morse(text):
    text = text.upper()
    morse_parts = []
    for char in text:
        if char in morse_code_dict:
            morse_parts.append(morse_code_dict[char])
        else:
            morse_parts.append('?')
    return ' '.join(morse_parts)
```

- **Input**: A string (the user’s message).
- **Process**:
  1. `text.upper()` – Converts the entire string to uppercase so that every character matches the dictionary keys (e.g., `'a'` becomes `'A'`).
  2. `morse_parts = []` – Initialises an empty list that will hold the Morse symbols for each character.
  3. `for char in text:` – Loops through each character in the normalised string.
  4. `if char in morse_code_dict:` – Checks whether the character exists in the dictionary. If yes, the corresponding Morse code is appended to the list.
  5. `else:` – If the character is not supported (e.g., `%`, `#`), a question mark `'?'` is appended as a placeholder.
  6. `return ' '.join(morse_parts)` – Joins all the Morse symbols together with a single space between them. This creates a readable output where each character’s code is clearly separated.
- **Output**: A string containing the Morse code representation of the input.

### 2.3. Main Program Loop – `main()`

```python
def main():
    print("Welcome to the Morse Code Converter!")
    print("Enter your message (letters, numbers, and basic punctuation).")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your message: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        if user_input == "":
            print("Please enter a message.")
            continue
        morse_output = text_to_morse(user_input)
        print(f"Morse Code: {morse_output}\n")
```

- **Purpose**: Provides an interactive interface for the user. It runs continuously until the user decides to quit.
- **Steps**:
  1. Prints a welcome message and brief instructions.
  2. Enters an infinite loop (`while True`).
  3. `input("Your message: ")` – Prompts the user to type a message. `.strip()` removes any leading/trailing whitespace.
  4. **Exit condition**: If the user types `'exit'` (case‑insensitive), the program prints a farewell message and `break`s out of the loop, ending the program.
  5. **Empty input check**: If the user just presses Enter (empty string), it prints a reminder and uses `continue` to restart the loop (ask again).
  6. **Conversion**: Calls `text_to_morse(user_input)` to get the Morse code.
  7. **Output**: Prints the result in the format `Morse Code: ...` followed by a blank line for readability.
  8. The loop then repeats, allowing another conversion.

### 2.4. Entry Point Guard

```python
if __name__ == "__main__":
    main()
```

- **Purpose**: This common Python idiom ensures that `main()` is called only when the script is run directly, not when it is imported as a module in another program.
- **How it works**: The special variable `__name__` is set to `"__main__"` when the script is executed. If the script is imported elsewhere, `__name__` becomes the module’s name, and the `main()` function is not called automatically. This allows the code to be reused without side effects.

---

## 3. Program Flow Summary

1. The script starts and the dictionary is created.
2. The `if __name__ == "__main__":` guard triggers the `main()` function.
3. The welcome message is displayed.
4. The program enters an interactive loop:
   - It asks the user for a message.
   - If the user types `exit`, the loop ends.
   - If the input is empty, it prompts again.
   - Otherwise, it converts the message using `text_to_morse()` and prints the result.
5. The loop continues until the user chooses to exit.

---

## 4. Example Run

```
Welcome to the Morse Code Converter!
Enter your message (letters, numbers, and basic punctuation).
Type 'exit' to quit.

Your message: Hello World 123
Morse Code: .... . .-.. .-.. --- / .-- --- .-. .-.. -.. / .---- ..--- ...--

Your message: SOS
Morse Code: ... --- ...

Your message: How are you?
Morse Code: .... --- .-- / .- .-. . / -.-- --- ..- ..--..

Your message: Test@123
Morse Code: - . ... - ? .---- ..--- ...--

Your message: exit
Goodbye!
```

- **Spaces** in the input become `/` in the output.
- **Unsupported character** `@` is replaced with `?`.

---

## 5. Potential Enhancements

Although the current program meets the assignment requirements, here are some ideas for future improvements:

- **Add reverse conversion** – Allow the user to input Morse code and get plain text.
- **Play sounds** – Use a library like `winsound` (Windows) or `pygame` to play the Morse code as beeps.
- **File input/output** – Read from a text file and write the Morse code to another file.
- **Better error handling** – Provide a list of supported characters when an unsupported one is encountered.
- **Command‑line arguments** – Accept a string directly from the command line for quick conversions (e.g., `python morse_converter.py "hello"`).

---

## 6. Conclusion

This Morse code converter is a simple yet complete example of a text‑based Python program. It demonstrates:

- Use of dictionaries for mapping.
- String manipulation (upper‑case conversion, joining).
- Interactive loops with user input validation.
- Modular code structure with separate functions.
- The importance of handling edge cases (empty input, unsupported characters).
