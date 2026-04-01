## Encryption and Hashing

### 1. Introduction

In authentication systems, protecting user passwords is paramount. Two fundamental cryptographic concepts are often discussed: **encryption** and **hashing**. While they may seem similar, they serve entirely different purposes and have distinct properties. Understanding these differences is critical for building secure systems.

- **Encryption** is a two-way function: data that is encrypted can be decrypted back to its original form using a key.
- **Hashing** is a one-way function: data that is hashed cannot be reversed to its original form.

Authentication systems primarily rely on **hashing** for password storage, and **encryption** is used for protecting data in transit (e.g., HTTPS) or at rest (e.g., encrypted databases). This documentation explains why these choices are made, how hashing works internally, and the best practices for secure password handling.

---

### 2. Encryption vs Hashing

| Property               | Encryption                                      | Hashing                                        |
|------------------------|-------------------------------------------------|------------------------------------------------|
| **Reversibility**      | Yes – data can be decrypted with the correct key. | No – it is computationally infeasible to reverse a hash. |
| **Purpose**            | Protect confidentiality of data.                | Verify integrity or store passwords without revealing original. |
| **Key Required**       | Yes – encryption key.                           | No key is used; hashing is keyless.            |
| **Output Size**        | Same as input size (or slightly larger).        | Fixed-length output regardless of input size.  |
| **Collisions**         | Not applicable.                                 | Two different inputs should never produce the same hash (collision resistance). |
| **Example Algorithms** | AES, RSA, ChaCha20                              | SHA-256, bcrypt, Argon2                        |

**Key Takeaway:**  
Encryption is used when you need to recover the original data (e.g., sending a message). Hashing is used when you only need to verify that the data hasn't changed or to check if a provided password matches a stored value without storing the password itself.

---

### 3. Why Not Encrypt Passwords?

A common mistake is to encrypt passwords instead of hashing them. This approach has critical flaws:

- **Key Storage Problem:** The encryption key must be stored somewhere. If an attacker gains access to the database and the key (often stored in configuration files or environment variables), they can decrypt all passwords.
- **Reversibility:** If the encryption is reversible, anyone with the key can retrieve the original passwords. This exposes users to risk if the system is compromised.
- **No Salting:** Encryption alone does not incorporate salting, so identical passwords would encrypt to identical ciphertexts, revealing which users share passwords.

Hashing avoids these issues because:
- No key is stored alongside the hash.
- The original password cannot be derived from the hash (one-way property).
- With salting, identical passwords produce different hashes.

**Therefore, password hashing is the industry standard and a mandatory security practice.**

---

### 4. Hashing in Depth

A cryptographic hash function takes an input (or "message") and returns a fixed-size string of bytes, typically a digest. The output appears random, but the same input always produces the same output.

#### 4.1 Required Properties of a Secure Hash Function

1. **Deterministic:** The same input always yields the same hash.
2. **Fast Computation:** Given an input, the hash should be quick to compute (though for passwords, we intentionally slow it down).
3. **Preimage Resistance:** Given a hash, it should be infeasible to find any input that produces that hash.
4. **Second Preimage Resistance:** Given an input, it should be infeasible to find a different input that produces the same hash.
5. **Collision Resistance:** It should be infeasible to find any two different inputs that produce the same hash.
6. **Avalanche Effect:** A small change in input (e.g., changing one bit) should produce a drastically different hash.

#### 4.2 How Hashing Works Internally

Hash functions process input in blocks. A typical construction (like SHA-256) follows these steps:

1. **Preprocessing:** The input message is converted to binary.
2. **Padding:** The message is padded to ensure its length is a multiple of the block size (e.g., 512 bits for SHA-256). Padding includes the original message length.
3. **Block Decomposition:** The padded message is split into fixed-size blocks.
4. **Initialization:** A set of initial hash values (constants) is loaded.
5. **Compression Function:** Each block is processed through a compression function that mixes the block with the current hash state using bitwise operations, modular additions, and logical functions. This updates the internal state.
6. **Final Output:** After all blocks are processed, the final hash state is output as the digest.

The compression function is designed to be one-way and to produce the avalanche effect.

#### 4.3 Example: SHA-256 Simplified

SHA-256 processes 512-bit blocks and outputs a 256-bit digest. It uses 64 rounds of operations on a 256-bit state (8 32-bit words). Each round involves:

- Bitwise rotations and shifts
- XOR operations
- Modular addition
- Choice and majority functions

The complexity ensures that even a tiny change in input flips about half of the output bits.

---

### 5. Types of Hash Functions

#### 5.1 General-Purpose Cryptographic Hashes

These are designed for integrity checks, digital signatures, and general use. They are **fast** – which makes them unsuitable for password storage.

- **MD5** (128-bit output) – Broken; collision attacks possible. Do not use.
- **SHA-1** (160-bit output) – Deprecated; collision attacks demonstrated.
- **SHA-2** family (SHA-224, SHA-256, SHA-384, SHA-512) – Still secure for general use, but too fast for passwords.
- **SHA-3** – Latest standard; based on Keccak sponge construction. Also fast.

#### 5.2 Password Hashing Functions

These are designed to be **slow**, **memory-hard**, and **adaptable** to resist brute-force attacks.

- **bcrypt** – Based on Blowfish cipher; includes a cost factor (work factor) that can be increased over time. Automatically handles salting.
- **scrypt** – Memory-hard; requires a significant amount of memory to compute, making it harder to accelerate with GPUs or ASICs.
- **Argon2** – Winner of the Password Hashing Competition (2015). Highly configurable (memory, time, parallelism). Recommended for new applications.

| Algorithm | Suitable for Passwords? | Why |
|-----------|-------------------------|-----|
| MD5, SHA-1, SHA-2 | No | Too fast; attackers can try billions of hashes per second. |
| bcrypt | Yes | Slow, salted, cost adjustable. |
| scrypt | Yes | Memory-hard, resistant to GPU attacks. |
| Argon2 | Yes | Modern, memory-hard, highly configurable. |

---

### 6. Secure Password Hashing

Secure password hashing combines three essential elements:

1. **Slow Hash Function:** Deliberately slow to increase the time required for brute-force attempts.
2. **Unique Salt per User:** Prevents precomputed attacks (rainbow tables) and hides identical passwords.
3. **Adaptable Cost:** The work factor can be increased over time as hardware improves.

#### 6.1 bcrypt in Practice

bcrypt is the most widely adopted password hashing algorithm. In Python, the `bcrypt` library provides an easy interface.

**Installation:**

```bash
pip install bcrypt
```

**Hashing a Password:**

```python
import bcrypt

def hash_password(plain_password: str) -> bytes:
    # Convert password to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Generate a salt with a cost factor (default is 12)
    salt = bcrypt.gensalt(rounds=12)
    
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed

# Example usage
hashed_pw = hash_password("MySecureP@ssw0rd")
print(hashed_pw)
# Output: b'$2b$12$e9WQ9JX1vX6qzK3P0n0F8eL6sC6V6nX3bZQ5WZlYl1VY5ZlJ8X8W2'
```

**Verifying a Password:**

```python
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

# Verify the previously hashed password
is_correct = verify_password("MySecureP@ssw0rd", hashed_pw)
print(is_correct)  # True
is_correct = verify_password("WrongPassword", hashed_pw)
print(is_correct)  # False
```

**How bcrypt Works Internally:**

- bcrypt uses the Blowfish cipher's key schedule to derive a hash. The cost factor (`rounds`) determines the number of key expansion iterations: 2^rounds iterations. This makes it exponentially slower as the cost increases.
- The salt is randomly generated and stored as part of the output hash string. When verifying, bcrypt extracts the salt from the stored hash and repeats the process.

#### 6.2 Salting Explained

A **salt** is a random value added to the password before hashing. It ensures that even if two users have the same password, their hashes will be different. Salts also defeat rainbow tables – precomputed tables of hashes for common passwords.

**Without salt:**
```
hash("password123") → abc123...
hash("password123") → abc123...   (same for all users)
```

**With salt:**
```
hash("password123" + random_salt1) → xyz789...
hash("password123" + random_salt2) → pqr456...
```

**Salt Requirements:**
- Must be cryptographically random.
- Must be unique per user.
- Should be long enough (at least 16 bytes).
- Does not need to be secret; it is stored alongside the hash.

bcrypt automatically generates a random salt and embeds it in the output hash, so you don't need to manage salt separately.

#### 6.3 Pepper – An Extra Layer

A **pepper** is a secret value (similar to a salt) that is **not stored in the database**. It is typically a hard-coded string or a key stored in a secure environment variable. The pepper is combined with the password and salt before hashing. If an attacker obtains the database, they still need the pepper to crack the hashes.

**Example using bcrypt with pepper:**

```python
import bcrypt
import os

PEPPER = os.environ.get('PASSWORD_PEPPER', 'default-pepper-change-me')

def hash_with_pepper(plain_password: str) -> bytes:
    # Combine password with pepper before hashing
    peppered_password = plain_password + PEPPER
    return bcrypt.hashpw(peppered_password.encode('utf-8'), bcrypt.gensalt())

def verify_with_pepper(plain_password: str, hashed: bytes) -> bool:
    peppered = plain_password + PEPPER
    return bcrypt.checkpw(peppered.encode('utf-8'), hashed)
```

**Note:** Pepper is an additional defense-in-depth measure. It is not a replacement for proper salting and hashing.

---

### 7. Why Different Hashing Methods Exist

Different cryptographic problems require different solutions. The existence of multiple hash functions reflects:

- **Security Strength:** As attacks improve, older algorithms become obsolete. MD5 and SHA-1 are now considered broken for collision resistance.
- **Performance Trade-offs:** General-purpose hashes prioritize speed; password hashes prioritize slowness.
- **Hardware Evolution:** Algorithms like scrypt and Argon2 are designed to resist attacks using GPUs, FPGAs, and ASICs by requiring large amounts of memory.
- **Regulatory Compliance:** Some standards mandate specific algorithms (e.g., FIPS 140-2 requires SHA-2 family).

---

### 8. The Avalanche Effect in Detail

The avalanche effect is a desirable property of cryptographic hash functions: a tiny change in input should produce a drastically different output. For example, hashing "password" vs "passwore" (one character changed) yields:

```
SHA-256("password") = 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
SHA-256("passwore") = 0b14d7f4a5f9c0c7b5f5d5e5a5f5c5d5e5f5c5d5e5f5c5d5e5f5c5d5e5f5c5d5
```

(Note: The second hash is fabricated for illustration, but the point stands that they are completely different.)

This property ensures that attackers cannot predict the hash of similar passwords and must attempt each possibility individually.

---

### 9. Hashing vs Encryption in Authentication Systems

| Use Case | Appropriate Mechanism |
|----------|----------------------|
| Storing passwords | Hashing (bcrypt, Argon2) |
| Transmitting data (e.g., login form) | Encryption (HTTPS/TLS) |
| Storing sensitive user data (e.g., addresses) | Encryption (AES) |
| Verifying file integrity | Hashing (SHA-256) |
| Digital signatures | Hashing + encryption (RSA, ECDSA) |

In a complete authentication system:

- Passwords are **hashed** before storage.
- All communication between client and server is **encrypted** using TLS.
- Session cookies or tokens may be **encrypted** or signed.
- Database backups may be **encrypted** at rest.

---

### 10. Common Pitfalls and How to Avoid Them

| Pitfall | Why It's Dangerous | Correct Approach |
|---------|--------------------|------------------|
| Storing plaintext passwords | Immediate compromise if database leaked | Hash with bcrypt/Argon2 |
| Using fast hashes (SHA-256) for passwords | Easily brute-forced | Use slow, adaptive hash |
| No salt | Rainbow tables reveal identical passwords | Generate unique salt per user |
| Reusing salt | Same as no salt | Always random per user |
| Weak salt generation | Predictable salt reduces security | Use `os.urandom()` or bcrypt's `gensalt()` |
| Not increasing cost over time | As hardware improves, older hashes become weaker | Periodically increase cost factor and rehash |
| Rolling your own crypto | Extremely high risk of vulnerabilities | Use well-audited libraries |

---

### 11. Practical Implementation Steps for Flask

In the upcoming lessons, you will implement secure password handling using Werkzeug's `generate_password_hash` and `check_password_hash`. These functions use `pbkdf2:sha256` with a salt by default, which is acceptable for many applications, though bcrypt is recommended for higher security.

**Example with Werkzeug (built into Flask):**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing a password
hashed_password = generate_password_hash('mypassword', method='pbkdf2:sha256', salt_length=8)

# Verifying a password
check_password_hash(hashed_password, 'mypassword')  # Returns True
```

Werkzeug automatically stores the salt and method in the hash string, similar to bcrypt.

---

### 12. Summary

- **Encryption is reversible; hashing is not.** Use encryption for confidentiality, hashing for password verification.
- **Never store passwords in plaintext.** Always hash them with a strong, slow, salted algorithm.
- **Use bcrypt, Argon2, or scrypt** for password hashing. Avoid MD5, SHA-1, and plain SHA-2.
- **Salting is mandatory** to prevent rainbow table attacks and hide identical passwords.
- **Pepper adds an extra layer** but is not a substitute for proper hashing.
- **Understand the internal workings** of hash functions to appreciate why they are secure.
- **Always use well-tested libraries** and never implement cryptographic primitives yourself.

In the next lesson, you will learn about common password hacking techniques and how proper hashing defends against them. This knowledge will solidify why the practices described here are essential.