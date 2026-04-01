## 1. Caesar Cipher → Decryption (shift back)

```python
def caesar_decrypt(cipher_text, shift):
    decrypted = ""
    for ch in cipher_text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            decrypted += chr((ord(ch) - base - shift) % 26 + base)
        else:
            decrypted += ch
    return decrypted


cipher = "KHOOR"
plain = caesar_decrypt(cipher, 3)
print(plain)
```

**Output**

```
HELLO
```

How it works

* Encryption: shift forward
* Decryption: shift backward
* Same logic, reverse direction

---

## 2. XOR encryption → Decryption (same function)

XOR is **self-reversible**.

```python
def xor_decrypt(cipher_text, key):
    result = ""
    for ch in cipher_text:
        result += chr(ord(ch) ^ key)
    return result


cipher = xor_decrypt("HELLO", 42)
plain = xor_decrypt(cipher, 42)

print(plain)
```

**Output**

```
HELLO
```

Why this works

* `A ^ B ^ B = A`
* Same function encrypts and decrypts

---

## 3. Hashing → ❌ No decryption possible

### SHA-256 (cannot be decrypted)

```python
import hashlib

hash_value = hashlib.sha256("password".encode()).hexdigest()
print(hash_value)
```

**Output**

```
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

❌ You **cannot** decrypt this.

Correct way to verify:

```python
def verify_password(input_password, stored_hash):
    return hashlib.sha256(input_password.encode()).hexdigest() == stored_hash


print(verify_password("password", hash_value))
```

**Output**

```
True
```

Key rule

* Hashing is **one-way**
* Verification ≠ decryption

---

## 4. Salted hashing → ❌ No decryption (verification only)

```python
import hashlib

def verify_password(password, salt, stored_hash):
    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )
    return new_hash == stored_hash
```

Why decryption is impossible

* Hash output destroys original structure
* Only comparison is allowed

---

## 5. Symmetric encryption (AES / Fernet) → Decryption

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

encrypted = cipher.encrypt(b"Secret message")
decrypted = cipher.decrypt(encrypted)

print(decrypted)
```

**Output**

```
b'Secret message'
```

Rules

* Same key encrypts & decrypts
* If key is lost → data lost

---

## 6. Asymmetric encryption (RSA) → Decryption

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

cipher = public_key.encrypt(
    b"HELLO",
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

plain = private_key.decrypt(
    cipher,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(plain)
```

**Output**

```
b'HELLO'
```

Rules

* Public key → encrypt
* Private key → decrypt
* One-way relationship

---

## 7. Hybrid encryption → Decryption flow (conceptual)

```text
Sender:
- RSA encrypts AES key
- AES encrypts message

Receiver:
- RSA decrypts AES key
- AES decrypts message
```

This is exactly how HTTPS works.

---

## 8. End-to-End Encryption → Decryption logic

At receiver side:

* Use private key to unwrap session key
* Use symmetric key to decrypt message
* Server never sees plaintext

No single function — it’s a **protocol**, not a function.

---

## 9. One-to-one mapping table (important)

| Encryption type | Decryptable | How            |
| --------------- | ----------- | -------------- |
| Caesar          | ✅           | Reverse shift  |
| XOR             | ✅           | Same operation |
| Hashing         | ❌           | Not possible   |
| Salted hashing  | ❌           | Not possible   |
| AES (Fernet)    | ✅           | Same key       |
| RSA             | ✅           | Private key    |
| Hybrid          | ✅           | Multi-step     |
| E2EE            | ✅           | Client keys    |

---

## 10. Mental model (this matters)

* Encryption → reversible **with key**
* Hashing → irreversible **by design**
* Symmetric → same key both sides
* Asymmetric → key pair
* Security = math + protocol + discipline

If you want next:

* build a login system (hash + verify)
* write your own Fernet file encryptor
* visualize how HTTPS decrypts data
* compare AES vs RSA performance
