# storage.py

# Centralized file path
DATA_FILE = "data/passwords.txt"

def save_credentials(website, username, password):
    """
    Saves credentials to a local file.

    Design choice:
    - Plain text for learning clarity
    - Easy to migrate to encryption or database later
    """

    # Append mode ensures no overwriting
    with open(DATA_FILE, "a") as file:
        file.write(f"{website} | {username} | {password}\n")
