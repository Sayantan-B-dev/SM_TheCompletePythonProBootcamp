```python
"""
===========================================================
TERMINAL-BASED MULTI-LEVEL ENCRYPTION / DECRYPTION SYSTEM
(USER CHOOSES ENCRYPT OR DECRYPT)
===========================================================

This program allows the user to:
1. Choose whether to ENCRYPT or DECRYPT
2. Choose a security level (1–5)
3. Enter message and key (if required)
4. See the result in the terminal

-----------------------------------------------------------
SECURITY LEVELS
-----------------------------------------------------------
1 → Caesar Cipher        (educational)
2 → XOR Cipher           (educational symmetric)
3 → Base64 Encoding      (NOT encryption)
4 → AES (Fernet)         (real symmetric encryption)
5 → RSA                  (real asymmetric encryption)

-----------------------------------------------------------
REQUIREMENTS
-----------------------------------------------------------
Python 3.8+
pip install cryptography
===========================================================
"""

# =========================
# STANDARD LIBRARIES
# =========================

import base64      # For Base64 encode/decode
import sys         # For clean program exit

# =========================
# CRYPTOGRAPHY LIBRARY
# =========================

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


# =========================================================
# LEVEL 1: CAESAR CIPHER
# =========================================================

def caesar_encrypt(text, shift):
    encrypted = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            encrypted += chr((ord(ch) - base + shift) % 26 + base)
        else:
            encrypted += ch
    return encrypted


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# =========================================================
# LEVEL 2: XOR CIPHER
# =========================================================

def xor_cipher(text, key):
    result = ""
    for ch in text:
        result += chr(ord(ch) ^ key)
    return result


# =========================================================
# LEVEL 3: BASE64 (ENCODING)
# =========================================================

def base64_encrypt(text):
    return base64.b64encode(text.encode()).decode()


def base64_decrypt(text):
    return base64.b64decode(text.encode()).decode()


# =========================================================
# LEVEL 4: AES (FERNET)
# =========================================================

fernet_key = Fernet.generate_key()   # Secret key for this session
fernet = Fernet(fernet_key)

def aes_encrypt(text):
    return fernet.encrypt(text.encode()).decode()


def aes_decrypt(text):
    return fernet.decrypt(text.encode()).decode()


# =========================================================
# LEVEL 5: RSA
# =========================================================

rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

rsa_public_key = rsa_private_key.public_key()

def rsa_encrypt(text):
    encrypted_bytes = rsa_public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_bytes).decode()


def rsa_decrypt(text):
    decrypted_bytes = rsa_private_key.decrypt(
        base64.b64decode(text),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_bytes.decode()


# =========================================================
# MAIN TERMINAL INTERFACE
# =========================================================

def main():
    print("\n🔐 MULTI-LEVEL SECURITY SYSTEM 🔐\n")

    while True:
        # Ask user what they want to do
        print("Choose operation:")
        print("1 → Encrypt")
        print("2 → Decrypt")
        print("0 → Exit")

        operation = input("\nEnter choice: ")

        if operation == "0":
            print("Exiting program...")
            sys.exit()

        if operation not in ("1", "2"):
            print("Invalid choice!\n")
            continue

        # Ask security level
        print("\nChoose Security Level:")
        print("1 → Caesar Cipher")
        print("2 → XOR Cipher")
        print("3 → Base64")
        print("4 → AES")
        print("5 → RSA")

        level = input("\nEnter level: ")

        message = input("\nEnter your message: ")

        # =========================
        # ENCRYPTION
        # =========================

        if operation == "1":

            if level == "1":
                shift = int(input("Enter shift value: "))
                result = caesar_encrypt(message, shift)

            elif level == "2":
                key = int(input("Enter numeric key: "))
                result = xor_cipher(message, key)

            elif level == "3":
                result = base64_encrypt(message)

            elif level == "4":
                result = aes_encrypt(message)

            elif level == "5":
                result = rsa_encrypt(message)

            else:
                print("Invalid level!\n")
                continue

            print("\nEncrypted Message:")
            print(result)

        # =========================
        # DECRYPTION
        # =========================

        else:

            if level == "1":
                shift = int(input("Enter shift value: "))
                result = caesar_decrypt(message, shift)

            elif level == "2":
                key = int(input("Enter numeric key: "))
                result = xor_cipher(message, key)

            elif level == "3":
                result = base64_decrypt(message)

            elif level == "4":
                result = aes_decrypt(message)

            elif level == "5":
                result = rsa_decrypt(message)

            else:
                print("Invalid level!\n")
                continue

            print("\nDecrypted Message:")
            print(result)

        print("\n" + "=" * 50 + "\n")


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
```

---

### How the control flow works (clear mental model)

```
Start
↓
User chooses Encrypt / Decrypt
↓
User chooses Security Level
↓
Message + Key (if needed)
↓
Correct function is called
↓
Result printed
↓
Loop repeats
```

---

### Important learning points

* Same algorithm ≠ same direction
* XOR uses one function both ways
* Base64 is reversible but NOT secure
* AES needs the same secret key
* RSA uses public ↔ private key pair
* User choice controls logic path

---

### Common mistakes this design avoids

* Mixing encrypt/decrypt logic
* Forgetting key reuse
* Printing instead of controlling flow
* Assuming Base64 is encryption
* Hardcoding behavior

If you want next:

* persistent keys (save/load)
* password-based AES
* encrypted file system
* attack demo on Caesar/XOR
* refactor using OOP
