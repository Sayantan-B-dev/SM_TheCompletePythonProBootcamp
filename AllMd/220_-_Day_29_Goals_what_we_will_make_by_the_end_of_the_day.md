# PASSWORDS — COMPLETE, PRACTICAL, SECURITY-FIRST GUIDE

---

## 1. What a Password **Is**

A **password** is a *shared secret* used to verify identity.
Security depends on **entropy**, **storage method**, **transmission**, and **user behavior** — not secrecy of rules.

> A password is only as strong as:
> **how unpredictable it is + how it is stored + how it is used**

---

## 2. Core Security Principles

### 2.1 Entropy (Unpredictability)

Entropy measures how hard a password is to guess.

| Password Type | Example                        | Approx. Entropy |
| ------------- | ------------------------------ | --------------- |
| Weak          | `password123`                  | Very low        |
| Medium        | `Hello@2024`                   | Low             |
| Strong        | `kQ9!fZ7#R2`                   | High            |
| Passphrase    | `correct horse battery staple` | Very high       |

> Length beats complexity.
> 16 random characters > 8 complex characters.

---

### 2.2 Attack Models

| Attack Type         | How It Works         | Defense          |
| ------------------- | -------------------- | ---------------- |
| Brute Force         | Try all combinations | Long passwords   |
| Dictionary          | Common words & leaks | Randomness       |
| Credential Stuffing | Reused passwords     | Unique passwords |
| Phishing            | Trick user           | Awareness + MFA  |
| Keylogging          | Capture keystrokes   | Secure OS        |

---

## 3. Password Storage (CRITICAL)

### 3.1 NEVER Store Passwords As

* Plain text
* Encrypted text with reversible key
* Base64 encoded text

### 3.2 Correct Storage Flow

```
User Password
   ↓
Salt (random)
   ↓
Hash Function
   ↓
Stored Hash
```

> Servers must **never** know the original password.

---

## 4. Hashing vs Encryption vs Encoding

| Concept    | Reversible | Purpose              |
| ---------- | ---------- | -------------------- |
| Hashing    | No         | Password storage     |
| Encryption | Yes        | Secure data transfer |
| Encoding   | Yes        | Data formatting      |

---

## 5. Secure Hashing Algorithms

| Algorithm | Use                      |
| --------- | ------------------------ |
| bcrypt    | Recommended              |
| argon2    | Best (modern)            |
| scrypt    | Memory-hard              |
| SHA-256   | ❌ Too fast for passwords |

> Password hashing must be **slow** to resist brute force.

---

## 6. Salting (Why It Matters)

* Salt = random value added before hashing
* Prevents rainbow table attacks
* Each password gets its own salt

> Same password ≠ same hash

---

## 7. Password Rules (User-Side)

### 7.1 Good Rules

* Minimum 14–16 characters
* Random or passphrase-based
* One password per service
* Use a password manager

### 7.2 Bad Rules

* Mandatory periodic changes
* Forced symbols without length
* Security questions with real answers

---

## 8. Password Managers

| Feature             | Reason           |
| ------------------- | ---------------- |
| Generates passwords | High entropy     |
| Stores securely     | Encrypted vault  |
| Autofill            | Prevent phishing |
| Sync                | Device safety    |

> One strong master password + MFA is safer than memorizing many.

---

## 9. Multi-Factor Authentication (MFA)

### 9.1 Types

| Factor     | Example             |
| ---------- | ------------------- |
| Knowledge  | Password            |
| Possession | Phone, hardware key |
| Inherence  | Fingerprint         |

### 9.2 Priority Order

1. Hardware key (best)
2. Authenticator app
3. SMS (last resort)

---

## 10. Password Policies (System Design)

| Rule             | Why                         |
| ---------------- | --------------------------- |
| Rate limiting    | Stops brute force           |
| Lockout delay    | Slows attackers             |
| Hash cost factor | Hardware-resistant          |
| Breach detection | Credential stuffing defense |

---

## 11. Password Generation (Python)

```python
import secrets
import string

# Character pool with high entropy
characters = string.ascii_letters + string.digits + string.punctuation

# Generate a cryptographically secure password
password = ''.join(secrets.choice(characters) for _ in range(16))

print(password)
```

### Expected Output

```
Qx7!m@9F#Zp2R^L$
```

**Why this works**

* `secrets` is cryptographically secure
* Random selection
* Sufficient length
* Full character space

---

## 12. Password Hashing (Python – bcrypt)

```python
import bcrypt

# User password input (bytes required)
password = b"VeryStrongPassword123!"

# Generate salt automatically
salt = bcrypt.gensalt()

# Hash password
hashed_password = bcrypt.hashpw(password, salt)

print(hashed_password)
```

### Expected Output

```
b'$2b$12$uE3y5...hashed_value...'
```

**Why bcrypt**

* Adaptive cost
* Slow by design
* Resistant to GPU attacks

---

## 13. Password Verification

```python
# Check password during login
is_valid = bcrypt.checkpw(password, hashed_password)

print(is_valid)
```

### Expected Output

```
True
```

**Key Point**

* Original password is never stored or compared directly

---

## 14. Common Password Mistakes

| Mistake         | Risk                   |
| --------------- | ---------------------- |
| Reuse           | Total account takeover |
| Short passwords | Fast brute force       |
| Human patterns  | Predictable            |
| No MFA          | Single failure point   |
| SMS-only MFA    | SIM swap attacks       |

---

## 15. Passwords vs Passphrases

| Aspect       | Password | Passphrase |
| ------------ | -------- | ---------- |
| Memorability | Low      | High       |
| Length       | Short    | Long       |
| Entropy      | Medium   | High       |
| User Errors  | High     | Low        |

---

## 16. Modern Reality

> Passwords alone are **no longer sufficient**.

Best practice today:

```
Strong Unique Password
+ Password Manager
+ MFA
+ Secure Hashing
```

Anything less is legacy security.
