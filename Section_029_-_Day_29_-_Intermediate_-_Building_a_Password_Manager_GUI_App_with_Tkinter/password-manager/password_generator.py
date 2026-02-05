# password_generator.py

import secrets
import string

# Safe symbols explicitly chosen to avoid shell / file issues
SAFE_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

def generate_strong_password(length=16):
    """
    Generates a cryptographically secure password.

    Why this function exists:
    - Centralizes password logic
    - Keeps UI free from security logic
    - Easy to test independently

    Security guarantees:
    - Uses `secrets` (not random)
    - Ensures at least:
        • one letter
        • one digit
        • one symbol
    """

    # Enforce minimum length for security
    if length < 12:
        raise ValueError("Password length should be at least 12")

    # Character pools
    letters = string.ascii_letters
    digits = string.digits
    symbols = SAFE_SYMBOLS

    # Force minimum complexity first
    password_chars = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Combine all pools for remaining characters
    all_chars = letters + digits + symbols

    # Fill remaining length with random secure choices
    for _ in range(length - 3):
        password_chars.append(secrets.choice(all_chars))

    # Shuffle to remove predictable positions
    secrets.SystemRandom().shuffle(password_chars)

    # Convert list of characters to string
    return ''.join(password_chars)
