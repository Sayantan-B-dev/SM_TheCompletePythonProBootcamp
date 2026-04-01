## Salting Passwords

### 1. Fundamental Concept of Salting

Salting is the process of adding **random data** to a password before hashing it. The primary purpose is to prevent attackers from using precomputed attacks and to ensure that identical passwords do not produce identical hashes.

Without salt:

```
hash("password123") → abc123...
hash("password123") → abc123...
```

With salt:

```
hash("password123" + salt1) → X9F2...
hash("password123" + salt2) → P0L8...
```

Even though the password is identical, the hashes are different because the salt differs. Salting does not make hashing reversible; it only strengthens resistance against large‑scale attacks.

---

### 2. Why Salting Is Required

#### 2.1 Problem Without Salt

If multiple users choose the same password:

| Username | Password  | Hash (No Salt) |
|----------|-----------|----------------|
| Alice    | secret123 | H1             |
| Bob      | secret123 | H1             |

An attacker seeing identical hashes instantly knows both users share the same password. Additionally, attackers use **rainbow tables** — precomputed hash lookup tables — to reverse common hashes instantly. With no salt, one rainbow table suffices for all users.

#### 2.2 With Salt

| Username | Password  | Salt | Hash |
|----------|-----------|------|------|
| Alice    | secret123 | S1   | H1   |
| Bob      | secret123 | S2   | H2   |

Now hashes differ even for identical passwords. Rainbow tables become useless because the attacker would need a unique table per salt – an infeasible task.

---

### 3. Properties of a Secure Salt

A salt must satisfy strict properties:

| Property          | Explanation                                               |
|-------------------|-----------------------------------------------------------|
| Random            | Must be generated using a cryptographically secure pseudo‑random number generator (CSPRNG). |
| Unique            | Each user must have a different salt.                      |
| Sufficient length | Minimum 16 bytes recommended; longer is better.           |
| Public            | Salt does **not** need to be secret; it is stored alongside the hash. |
| Stored with hash  | Must be retrievable during verification.                   |

Salt does not require confidentiality. It prevents mass attacks, not targeted brute force.

---

### 4. Deep Technical View: How Salt Works Internally

At the lowest level, the hash is computed as:

```
H = hash(password || salt)
```

where `||` denotes concatenation. The hash function processes the combined byte sequence.

If the password is 8 bytes and the salt is 16 bytes, the total input is 24 bytes. This input is padded and processed block‑by‑block inside the hash function (e.g., SHA‑256 or bcrypt). The randomness injected by the salt changes the entire compression output due to the **avalanche effect** – even a 1‑bit change produces a completely different digest.

---

### 5. Where Is Salt Stored?

#### 5.1 Traditional Hashing (Manual Salt)

In older or custom implementations, the database stores:

| user_id | salt | hashed_password |
|---------|------|-----------------|

The salt must be stored because verification requires it: during login, the system retrieves the salt, concatenates it with the entered password, hashes, and compares.

#### 5.2 bcrypt / Argon2 (Modern Approach)

Modern password hashing libraries like bcrypt automatically embed the salt inside the hash string. Example bcrypt hash:

```
$2b$12$e9WQ9JX1vX6qzK3P0n0F8eL6sC6V6nX3bZQ5WZlYl1VY5ZlJ8X8W2
```

Breakdown:

- `$2b$` → algorithm identifier
- `12` → cost factor (2^12 iterations)
- `e9WQ9JX1vX6qzK3P0n0F8e` → 16‑byte salt (base64 encoded)
- Remaining characters → actual hash output

With bcrypt, you do **not** store the salt separately; it is part of the stored hash string. During verification, bcrypt extracts the salt automatically.

---

### 6. Salt Generation in Python (Manual Example)

For demonstration purposes only, here is how you could manually generate a salt and hash a password using SHA‑256. **Do not use this in production** – always use a dedicated password hashing library.

```python
import os
import hashlib
import base64

def hash_password_with_manual_salt(plain_password):
    # Generate 16-byte cryptographically secure salt
    salt = os.urandom(16)
    
    # Combine password and salt
    password_bytes = plain_password.encode('utf-8')
    combined = password_bytes + salt
    
    # Hash using SHA-256 (demonstration only)
    hash_digest = hashlib.sha256(combined).digest()
    
    # Encode for storage
    salt_encoded = base64.b64encode(salt).decode('utf-8')
    hash_encoded = base64.b64encode(hash_digest).decode('utf-8')
    
    return salt_encoded, hash_encoded

# Example usage
salt, hashed = hash_password_with_manual_salt("SecurePass123")
print("Salt:", salt)
print("Hash:", hashed)
```

**Expected output (example):**
```
Salt: random_base64_value
Hash: random_hash_value
```

This code illustrates the principle: a unique salt is generated, combined with the password, and hashed. Both salt and hash must be stored to verify later.

---

### 7. Salting with bcrypt (Recommended)

The `bcrypt` library is the industry standard for password hashing in Python. It handles salt generation, embedding, and verification automatically.

**Installation:**

```bash
pip install bcrypt
```

**Hashing a password:**

```python
import bcrypt

def hash_password(password):
    password_bytes = password.encode('utf-8')
    
    # Generate salt with cost factor 12
    salt = bcrypt.gensalt(rounds=12)
    
    # Hash password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

# Example
stored_hash = hash_password("StrongPassword123")
print("Stored Hash:", stored_hash)
```

**Verifying a password:**

```python
def verify_password(password, stored_hash):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        stored_hash
    )

print("Verification:", verify_password("StrongPassword123", stored_hash))
# Output: Verification: True
```

**Key points:**

- `bcrypt.gensalt()` automatically creates a random salt each time.
- The salt is embedded in the returned hash string.
- `bcrypt.checkpw()` extracts the salt from the stored hash, re‑hashes the input password, and securely compares.

---

### 8. Salt Rounds (Cost Factor)

In bcrypt, the cost factor determines how many iterations of the key derivation function are performed:

```
gensalt(rounds=12)   # 2^12 = 4096 iterations
```

- `rounds=12` → 4096 iterations
- `rounds=14` → 16384 iterations

Higher rounds make hashing slower, which directly increases the time required for an attacker to brute‑force passwords. However, it also increases CPU load on your server during login and registration.

**Recommended:** Start with 12 and benchmark. Adjust based on your server’s performance and security requirements. The cost factor can be increased over time as hardware improves.

---

### 9. Extreme Deep‑Level Explanation: bcrypt Internals

bcrypt is based on the Blowfish cipher. Internally:

1. The password and salt are fed into Blowfish’s key expansion routine.
2. The key schedule is repeatedly expanded – the number of expansions is 2^rounds.
3. This expensive key setup creates computational hardness.
4. The final output is a 192‑bit value encoded in a specific format.

Because bcrypt:

- Uses an adaptive cost factor.
- Is intentionally CPU‑intensive.
- Incorporates the salt into the key setup.

It effectively prevents:

- Rainbow table attacks (due to unique salts).
- Fast GPU cracking (to a large extent, though GPU‑based bcrypt cracking is still possible with enough resources; memory‑hard algorithms like Argon2 offer even stronger GPU resistance).

---

### 10. What Salt Does NOT Protect Against

Salting is essential, but it is **not** a silver bullet. It does **not**:

- Prevent brute‑force attacks on a single user (the attacker can still try many passwords against that user’s hash).
- Protect weak passwords (a dictionary attack against a salted hash is still feasible if the password is common).
- Replace rate limiting (online attacks must still be throttled).
- Replace multi‑factor authentication (MFA).

Salting specifically protects against **mass hash cracking** – i.e., an attacker trying to crack many user hashes simultaneously with precomputed tables.

---

### 11. Advanced Concepts: Pepper vs Salt

| Feature         | Salt                   | Pepper                 |
|-----------------|------------------------|------------------------|
| Unique per user | Yes                    | No (same for all)      |
| Stored in DB    | Yes                    | No (kept secret)       |
| Secret          | No                     | Yes                    |
| Purpose         | Prevent rainbow tables | Add extra secret layer |

A **pepper** is a secret value stored separately from the database (e.g., in an environment variable or a hardware security module). It is combined with the password and salt before hashing. If an attacker obtains the database but not the pepper, cracking becomes significantly harder.

**Example with pepper:**

```python
import os
import bcrypt

PEPPER = os.environ.get('PASSWORD_PEPPER', 'default-pepper-change-me')

def hash_with_pepper(password):
    peppered = password + PEPPER
    return bcrypt.hashpw(peppered.encode('utf-8'), bcrypt.gensalt(12))

def verify_with_pepper(password, stored_hash):
    peppered = password + PEPPER
    return bcrypt.checkpw(peppered.encode('utf-8'), stored_hash)
```

**Important:** Pepper is an additional layer of defense‑in‑depth, not a substitute for proper salting.

---

### 12. Attack Scenario Analysis

Consider an attacker who has obtained the password hashes from your database.

#### Database Only (bcrypt hashes with embedded salt)

- The attacker sees hashes like `$2b$12$...`. Each hash contains its own unique salt.
- To recover a password, the attacker must brute‑force each hash individually. With a high cost factor (e.g., 12), each guess is slow. This makes cracking a large set of hashes computationally expensive.

#### Database + Source Code

- The attacker now knows the algorithm and cost factor, but that does not help reverse the hash. They still must brute‑force each hash individually. If a pepper was used, and it is not in the source code (e.g., stored in a separate secure location), the attacker cannot even begin to guess without the pepper.

#### Database + Pepper Compromised

- If the pepper is also stolen (e.g., from an exposed environment variable), the system is fully compromised. Defense‑in‑depth requires protecting all layers.

---

### 13. Common Mistakes

- **Reusing the same salt for all users** – identical passwords still produce identical hashes; rainbow tables become effective again.
- **Generating predictable salts** – using weak random sources (e.g., `random.random()` instead of `os.urandom`).
- **Using too short a salt** – less than 8 bytes is insufficient.
- **Using SHA‑256 + salt without iterations** – fast hashing allows rapid brute‑force.
- **Setting too low a bcrypt cost factor** – e.g., rounds=4 (16 iterations) provides almost no protection.
- **Storing plaintext passwords temporarily** – even for a short time in logs or memory, they can be exposed.

---

### 14. Full Lifecycle of a Password with Salt

1. **User registration:** The user submits a password.
2. **Salt generation:** A unique, random salt is generated (e.g., by bcrypt).
3. **Hashing:** The password and salt are processed through a slow, adaptive hash function (bcrypt).
4. **Storage:** The resulting hash (which includes the salt) is stored in the database.
5. **User login:** The user submits their password.
6. **Hash retrieval:** The stored hash is fetched from the database.
7. **Salt extraction:** bcrypt extracts the salt from the stored hash.
8. **Re‑hashing:** The submitted password is combined with the extracted salt and hashed using the same algorithm and cost factor.
9. **Comparison:** The newly computed hash is compared to the stored hash using a constant‑time comparison (to prevent timing attacks). If they match, login succeeds.

Throughout this process, the plaintext password is never stored, and the salt ensures that even if two users have the same password, their stored hashes differ.

---

### 15. Highest‑Level Security Architecture

For a production‑grade authentication system, incorporate:

- **bcrypt or Argon2** with a unique salt per user.
- **Cost factor** benchmarked and increased periodically.
- **Optional pepper** stored separately.
- **Rate limiting** on login endpoints.
- **Multi‑factor authentication** (MFA).
- **TLS encryption** for all communication.
- **Secure secret management** (environment variables, vaults, HSMs).

Salting is foundational, but it is only one layer in a properly designed authentication security model.

---

### Next Steps

Now that you understand the theory behind salting and secure password hashing, the next lesson will guide you through implementing these concepts in your Flask application using Werkzeug’s built‑in functions (`generate_password_hash` and `check_password_hash`). You will replace the plaintext password storage in the registration and login routes with properly salted and hashed passwords, following the principles covered here.