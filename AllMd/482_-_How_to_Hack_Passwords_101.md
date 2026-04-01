## How to Hack Passwords 101

### 1. Introduction

To build a secure authentication system, you must understand how attackers attempt to compromise passwords. This knowledge allows you to implement defenses that thwart these attacks. This document explores the most common password attack techniques, how they work, and the countermeasures that prevent them.

**What you will learn:**

- The categories of password attacks.
- How attackers obtain password hashes.
- Techniques for cracking hashed passwords.
- Methods to bypass authentication logic.
- Practical prevention strategies for each attack type.

By the end, you will understand why proper password hashing (with salting and slow algorithms) and additional security layers are essential.

---

### 2. Categories of Password Attacks

Password attacks generally fall into two broad categories:

1. **Online Attacks** – The attacker interacts with the live application (e.g., login page) to guess credentials.
2. **Offline Attacks** – The attacker has obtained the password hashes (e.g., from a database breach) and attempts to recover the original passwords without interacting with the application.

Each category includes multiple techniques, which we will examine in detail.

---

### 3. Online Attacks

#### 3.1 Brute Force Attack

**Definition:** The attacker tries every possible combination of characters until the correct password is found.

**How it works:**  
An automated script sends login requests with systematically generated passwords. For a password of length L using a character set of size C, the total number of possibilities is C^L. For example, a 6-character lowercase password (26^6 = 308 million combinations) can be tested relatively quickly if no rate limiting is applied.

**Example (pseudocode):**
```
for each password in generate_all_combinations():
    if login(username, password) == success:
        return password
```

**Vulnerable if:**
- No rate limiting on login attempts.
- Weak password policy (short or simple passwords).
- No account lockout after multiple failures.

**Prevention:**
- **Rate limiting:** Restrict the number of login attempts per IP address or per account within a time window.
- **Account lockout:** Temporarily lock the account after a certain number of failed attempts.
- **CAPTCHA:** Require solving a challenge after a few failures.
- **Strong password policies:** Enforce minimum length and complexity.
- **Multi-factor authentication (MFA):** Even if password is guessed, the second factor blocks access.

---

#### 3.2 Dictionary Attack

**Definition:** A type of brute force that uses a list of likely passwords (a dictionary) instead of trying all possible combinations. The dictionary contains common passwords, leaked passwords from previous breaches, and variations (e.g., adding numbers or symbols).

**How it works:**  
The attacker compiles a wordlist (e.g., "password", "123456", "qwerty", "admin") and tries each one.

**Why it's effective:**  
Users often choose weak, predictable passwords. A dictionary attack can crack a large percentage of accounts with minimal effort.

**Prevention:**
- **Password blacklisting:** Reject passwords that appear in common password lists.
- **Enforce complexity:** Require a mix of character types, but be aware that users may still choose predictable patterns (e.g., "Password123!").
- **Use passphrases:** Encourage longer, memorable phrases instead of short complex strings.

---

#### 3.3 Credential Stuffing

**Definition:** The attacker uses username/password pairs leaked from one service and tries them on other services. This exploits the common practice of password reuse across multiple websites.

**How it works:**  
Large databases of breached credentials are available on the dark web. Attackers automate login attempts across many sites using these lists.

**Prevention:**
- **Encourage unique passwords:** Educate users not to reuse passwords.
- **Check for breached credentials:** Services like Have I Been Pwned offer APIs to check if a password has appeared in breaches.
- **Implement MFA:** Even if credentials are stolen, the second factor prevents account takeover.
- **Monitor for suspicious activity:** Unusual login locations, times, or devices can indicate credential stuffing.

---

#### 3.4 Phishing

**Definition:** The attacker tricks the user into entering their credentials on a fake website that mimics the legitimate one.

**How it works:**  
The attacker sends an email or message with a link to a fraudulent login page. When the user enters their username and password, the attacker captures them and then uses them on the real site.

**Prevention:**
- **User education:** Train users to recognize phishing attempts.
- **MFA:** The attacker may capture the password but cannot provide the second factor.
- **Browser protections:** Modern browsers warn users about known phishing sites.
- **Email authentication:** Use SPF, DKIM, and DMARC to prevent email spoofing.

---

#### 3.5 Man-in-the-Middle (MitM) Attack

**Definition:** The attacker intercepts communication between the user and the server, capturing credentials or session tokens.

**How it works:**  
If the user connects over an unencrypted network (e.g., public Wi-Fi without HTTPS), an attacker on the same network can eavesdrop or modify traffic. Even with HTTPS, a misconfigured or compromised certificate can enable interception.

**Prevention:**
- **Enforce HTTPS:** Use TLS for all communication. Redirect HTTP to HTTPS.
- **HSTS (HTTP Strict Transport Security):** Tell browsers to always use HTTPS for your domain.
- **Secure cookies:** Set the `Secure` flag so cookies are only sent over HTTPS.
- **Certificate pinning:** (Advanced) Ensure the client only accepts a specific certificate.

---

#### 3.6 SQL Injection

**Definition:** The attacker injects malicious SQL code into a login form input, potentially bypassing authentication entirely.

**How it works:**  
If the application constructs SQL queries by concatenating user input, an attacker can input something like `' OR '1'='1` as the password. The resulting query might become:

```sql
SELECT * FROM users WHERE email = 'user@example.com' AND password = '' OR '1'='1'
```

Since `'1'='1'` is always true, the query returns a user, and the attacker is logged in without a valid password.

**Prevention:**
- **Use parameterized queries or ORMs:** Never concatenate user input directly into SQL statements.
- **Input validation:** Validate and sanitize all user inputs.
- **Least privilege:** The database user should have minimal necessary permissions.

---

### 4. Offline Attacks (Password Cracking)

Offline attacks occur after an attacker has obtained the password hashes, typically from a data breach. The attacker can then attempt to recover the original passwords at their own pace, without interacting with the live application.

#### 4.1 Obtaining Password Hashes

Attackers can obtain hashes through:

- **Database breaches:** Exploiting vulnerabilities like SQL injection to dump the user table.
- **Insider threats:** Malicious employees with database access.
- **Backup leaks:** Unsecured backups exposed online.
- **Physical theft:** Stolen servers or hard drives.

Once the attacker has the hashes, the goal is to find plaintext passwords that produce the same hash.

---

#### 4.2 Brute Force (Offline)

The attacker tries every possible password, hashes each, and compares to the target hash. This is much faster online because there are no rate limits, and the attacker can use powerful hardware.

**Defense:** Use slow hashing algorithms (bcrypt, Argon2) with a high cost factor to make each guess computationally expensive.

---

#### 4.3 Dictionary Attack (Offline)

Similar to online dictionary attack, but performed against hashes. The attacker hashes each word from a wordlist and compares to the target hash.

**Defense:** Salting ensures that even if two users have the same password, their hashes differ. The attacker would have to hash each dictionary word separately for every salt, multiplying the work.

---

#### 4.4 Rainbow Table Attack

**Definition:** A rainbow table is a precomputed table of hashes for a large set of possible passwords. The attacker can look up a hash in the table and instantly find the corresponding password, if present.

**How it works:**  
Creating a rainbow table is time-consuming, but once built, cracking individual hashes is extremely fast. Tables can cover all combinations up to a certain length for a given hash algorithm.

**Why salting defeats rainbow tables:**  
A salt randomizes the hash. For a salt of length S, the attacker would need a separate rainbow table for each possible salt value, which is infeasible. Therefore, a unique salt per user makes precomputed tables useless.

**Prevention:**
- **Always use a unique, random salt per password.**
- Use a strong hash function with a salt (bcrypt, Argon2 automatically include salt).

---

#### 4.5 GPU and Hardware Acceleration

Modern graphics processing units (GPUs) can perform billions of hash calculations per second for fast algorithms like MD5 or SHA-256. Attackers use specialized hardware (GPUs, FPGAs, ASICs) to accelerate cracking.

**Defense:** Use memory-hard algorithms (scrypt, Argon2) that require large amounts of memory, making GPU acceleration less effective because memory bandwidth becomes the bottleneck.

---

#### 4.6 Hash Collision Attacks

If an attacker can find two different inputs that produce the same hash (a collision), they might be able to log in without knowing the actual password. This is a theoretical concern for modern hash functions; practical collision attacks have been demonstrated against MD5 and SHA-1 but not yet against SHA-256 or bcrypt.

**Defense:** Use collision-resistant hash functions (SHA-256, SHA-3, bcrypt).

---

### 5. Cracking Examples with Code

To understand the attacker's perspective, consider a simple Python script that attempts to crack a SHA-256 hash using a dictionary. **This is for educational purposes only.**

```python
import hashlib

# Example hash of "password123" (unsalted SHA-256)
target_hash = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"

# Load a dictionary of common passwords (one per line)
with open('rockyou.txt', 'r', encoding='latin-1') as f:
    for line in f:
        password = line.strip()
        # Compute SHA-256 hash of the password
        computed = hashlib.sha256(password.encode()).hexdigest()
        if computed == target_hash:
            print(f"Password found: {password}")
            break
```

If the password is in the dictionary, this script will find it quickly. If a salt were used, the attacker would need to know the salt and incorporate it.

---

### 6. JWT and Token-Based Attacks

JSON Web Tokens (JWT) are commonly used for authentication in modern web apps. Attackers exploit JWT vulnerabilities.

#### 6.1 Weak Secret

If the JWT is signed with a weak secret (e.g., "secret"), the attacker can brute-force the secret and forge tokens.

**Prevention:** Use a strong, random secret (at least 256 bits) stored securely.

#### 6.2 Algorithm Confusion

Some JWT libraries allow the `alg` header to be set to `none`, which means no signature. If the server accepts tokens with `alg: none`, the attacker can create arbitrary tokens without a signature.

**Prevention:** Configure the JWT library to reject tokens with `alg: none` and to only accept a specific algorithm (e.g., HS256 or RS256).

#### 6.3 Token Theft (XSS)

If the JWT is stored in `localStorage` or a non-HttpOnly cookie, an XSS vulnerability can allow an attacker to steal the token.

**Prevention:**
- Store tokens in **HttpOnly, Secure, SameSite cookies** to prevent JavaScript access.
- Use Content Security Policy (CSP) to mitigate XSS.

---

### 7. Defensive Measures Summary

| Attack Type | Primary Defenses |
|-------------|------------------|
| Brute Force (online) | Rate limiting, account lockout, CAPTCHA, MFA |
| Dictionary (online) | Password blacklisting, strong password policy, MFA |
| Credential Stuffing | MFA, breached password detection, unique password enforcement |
| Phishing | User education, MFA, browser warnings |
| MitM | HTTPS, HSTS, secure cookies |
| SQL Injection | Parameterized queries, input validation |
| Rainbow Tables | Unique salts per password |
| GPU Cracking | Slow, memory-hard hashing (bcrypt, Argon2) |
| JWT Weakness | Strong secret, reject alg:none, secure token storage |

---

### 8. Conclusion

Understanding how passwords are attacked is the first step in building robust authentication. A well-designed system incorporates multiple layers of defense:

- **Strong password hashing** (bcrypt/Argon2 with salt)
- **Rate limiting** to slow online attacks
- **MFA** to render stolen passwords useless
- **Secure coding** to prevent injection and XSS
- **HTTPS** to protect data in transit

By implementing these measures, you make it significantly harder for attackers to compromise user accounts, even if they obtain the password hashes. In the next lesson, you will learn about **salting** in detail and how it integrates with hashing.