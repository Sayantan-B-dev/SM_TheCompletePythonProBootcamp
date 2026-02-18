## What is Authentication

### 1. Definition of Authentication

Authentication is the process of verifying the identity of a person or system trying to access a protected resource. When a user attempts to log into a website, the system must confirm that the user is who they claim to be before granting access. This verification answers one fundamental question: **"Who are you?"**

The entity requesting access can be:

- A human user entering credentials through a web form
- Another application or service making an API call
- A device attempting to connect to a network
- An automated script or bot

Authentication establishes identity, but it does not determine what the authenticated entity can do. That separate function is called authorization, which we will discuss in detail later.

---

### 2. Authentication Factors

Authentication systems rely on one or more factors to prove identity. These factors fall into three main categories:

#### Something You Know (Knowledge Factors)
This is the most common form of authentication. The user provides information that only they should know.

- Passwords
- Personal Identification Numbers (PINs)
- Answers to security questions
- Passphrases

Example: When you log into your email, you enter a password that you have memorized. The system assumes that anyone who knows this password must be you.

#### Something You Have (Possession Factors)
The user must physically possess an object to authenticate.

- Mobile phones (receiving SMS codes)
- Hardware tokens (like RSA SecurID or YubiKey)
- Smart cards or ID badges
- Authenticator apps (Google Authenticator, Authy)

Example: After entering your password on a banking website, you might receive a text message with a one-time code. Only someone with access to your phone can complete the login.

#### Something You Are (Inherence Factors)
These are biometric characteristics unique to an individual.

- Fingerprint scans
- Facial recognition
- Retina or iris scans
- Voice recognition
- Hand geometry

Example: Unlocking a modern smartphone with your fingerprint or face uses biometric authentication.

#### Additional Factors
Modern systems sometimes consider additional dimensions:

- **Location factors**: Accessing from a recognized location (home or office) may be treated differently than access from an unfamiliar country.
- **Time factors**: Login attempts at unusual hours might trigger additional verification.
- **Behavioral factors**: Typing patterns or mouse movements can be used for continuous authentication.

---

### 3. Multi-Factor Authentication (MFA)

When a system requires two or more different factors, it is called Multi-Factor Authentication. MFA significantly increases security because an attacker would need to compromise multiple independent elements.

#### Examples of MFA Combinations

| Factors Used | Example Scenario |
|--------------|------------------|
| Password + SMS Code | User enters password, then receives and enters a code sent to their phone |
| Password + Fingerprint | User types password, then scans fingerprint on a reader |
| Smart Card + PIN | User inserts card and enters PIN to access a secure facility |
| Password + Authenticator App | User enters password, then generates a time-based code from an app |

#### Why MFA Matters
If an attacker steals your password through phishing or a data breach, they still cannot access your account because they lack the second factor. This is why banks, email providers, and sensitive applications now mandate or strongly encourage MFA.

---

### 4. Authentication vs Authorization

These two terms are often confused, but they serve distinct purposes in security systems.

| Aspect | Authentication | Authorization |
|--------|----------------|---------------|
| Core Question | "Who are you?" | "What are you allowed to do?" |
| Timing | Happens first, before access is granted | Happens after identity is confirmed |
| Dependence | Does not require authorization | Depends on authentication |
| Mechanism | Credentials, factors, tokens | Roles, permissions, policies |
| Example | Logging in with email and password | Accessing the admin dashboard |
| Failure Result | "Access denied" at login | "Forbidden" after login |

#### Real-World Analogy
Think of entering a secure office building:

1. You show your ID badge to the security guard at the front desk. The guard verifies that the photo matches your face and the badge is valid. This is **authentication**.
2. Once inside, you try to enter the server room. The door requires a special keycard that only IT staff have. Checking whether you possess that keycard is **authorization**.

You cannot reach the authorization step without first authenticating. But authentication alone does not grant you access to everything.

#### Example Scenario in Web Applications

```python
# Pseudocode demonstrating the flow
def login_route():
    # Step 1: Authentication
    email = request.form['email']
    password = request.form['password']
    
    user = find_user_by_email(email)
    if user and verify_password(password, user.hashed_password):
        # Authentication successful
        login_user(user)  # Creates session
        return redirect('/dashboard')
    else:
        # Authentication failed
        return "Invalid credentials", 401

def admin_route():
    # Step 2: Authorization (after authentication)
    if not current_user.is_authenticated:
        return redirect('/login')
    
    if current_user.role != 'admin':
        # User is authenticated but not authorized
        return "Forbidden", 403
    
    return render_template('admin_panel.html')
```

In this example, both authentication and authorization checks are necessary for complete security.

---

### 5. Secure Password Handling Principles

When implementing authentication, passwords must be handled with extreme care. The following principles are non-negotiable in any production system.

#### Never Store Plaintext Passwords
Storing passwords in their original form is catastrophic. If an attacker gains access to your database, they immediately have all user credentials. Since many people reuse passwords across sites, a single breach can compromise users' accounts elsewhere.

#### Always Hash Passwords
Hashing transforms a password into a fixed-length string using a one-way mathematical function. From the hash, it is computationally infeasible to recover the original password.

#### Use Per-User Unique Salts
A salt is random data added to the password before hashing. Each user gets a different salt, ensuring that identical passwords produce different hashes. This prevents attackers from using precomputed lookup tables (rainbow tables).

#### Choose Adaptive Hashing Algorithms
Not all hash functions are suitable for passwords. General-purpose hashes like SHA-256 are designed to be fast, which actually makes them poor choices for passwords because attackers can try billions of combinations per second. Password-specific algorithms are intentionally slow and resource-intensive.

**Recommended algorithms:**

- **bcrypt**: The most widely used password hashing algorithm. It automatically handles salting and includes a cost factor that can be increased over time.
- **Argon2**: Winner of the Password Hashing Competition (2015). It is memory-hard, making it resistant to GPU-based attacks.
- **scrypt**: Another memory-hard algorithm designed to resist hardware brute-force attacks.

#### Enforce Strong Password Policies
Guide users toward creating passwords that are resistant to guessing and brute-force attacks.

- Minimum length (at least 12 characters recommended)
- Require a mix of character types (uppercase, lowercase, numbers, symbols)
- Check against lists of commonly used passwords
- Prevent passwords that are too similar to the username or email

#### Implement Rate Limiting
Limit the number of login attempts from a single IP address or for a specific account. This slows down automated attacks.

```python
# Example rate limiting concept
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic here
```

#### Use HTTPS for All Authentication Traffic
All communication between the client and server must be encrypted. Without HTTPS, passwords and session tokens can be intercepted by anyone on the same network.

---

### 6. Password Hashing in Python with bcrypt

The `bcrypt` library is the recommended tool for password hashing in Python applications. It implements the bcrypt algorithm with automatic salt generation and embedding.

#### Installation

```bash
pip install bcrypt
```

#### Basic Hashing and Verification

```python
import bcrypt

def hash_password(plain_password):
    """
    Hash a plaintext password using bcrypt.
    
    Args:
        plain_password (str): The password entered by the user
        
    Returns:
        bytes: The bcrypt hash string (includes salt and cost factor)
    """
    # Convert string to bytes (bcrypt works with bytes)
    password_bytes = plain_password.encode('utf-8')
    
    # Generate salt with default cost factor (12)
    # gensalt() automatically creates a cryptographically secure random salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    # The salt is automatically embedded in the returned hash
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

def verify_password(plain_password, stored_hash):
    """
    Verify that a plaintext password matches a stored bcrypt hash.
    
    Args:
        plain_password (str): The password attempt from login
        stored_hash (bytes): The hash retrieved from the database
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    password_bytes = plain_password.encode('utf-8')
    
    # checkpw extracts the salt from the stored hash,
    # re-hashes the input with that salt, and compares
    return bcrypt.checkpw(password_bytes, stored_hash)

# Example usage
if __name__ == "__main__":
    # User registration
    user_password = "MySecurePassword123!"
    hashed = hash_password(user_password)
    print(f"Stored hash: {hashed}")
    
    # User login attempt
    login_attempt = "MySecurePassword123!"
    is_correct = verify_password(login_attempt, hashed)
    print(f"Login successful: {is_correct}")
    
    # Wrong password attempt
    wrong_attempt = "WrongPassword"
    is_correct = verify_password(wrong_attempt, hashed)
    print(f"Login successful: {is_correct}")
```

#### Understanding the bcrypt Hash Format

A bcrypt hash looks like this:

```
$2b$12$e9WQ9JX1vX6qzK3P0n0F8eL6sC6V6nX3bZQ5WZlYl1VY5ZlJ8X8W2
```

This string encodes several pieces of information:

| Component | Value in Example | Meaning |
|-----------|------------------|---------|
| Algorithm | `$2b$` | The bcrypt algorithm version |
| Cost | `12` | 2^12 = 4096 iterations |
| Salt | `e9WQ9JX1vX6qzK3P0n0F8e` | 16-byte salt (base64 encoded) |
| Hash | `L6sC6V6nX3bZQ5WZlYl1VY5ZlJ8X8W2` | The actual password hash |

The salt is not stored separately – it is part of the hash string itself. This is why `bcrypt.checkpw()` only needs the plain password and the stored hash.

---

### 7. Types of Authentication Systems

Different applications require different authentication approaches. Understanding the options helps you choose the right method for your use case.

#### Password-Based Authentication
The traditional method where users authenticate with a username/email and password.

**Strengths:**
- Simple to implement
- Familiar to users
- No additional hardware or software required

**Weaknesses:**
- Vulnerable to phishing
- Susceptible to brute-force attacks
- Users choose weak passwords or reuse them

**Best for:**
- Low-risk applications
- Internal tools with strong password policies
- Applications where simplicity is prioritized

#### Token-Based Authentication
Instead of maintaining session state on the server, the client presents a token with each request. JSON Web Tokens (JWT) are the most common implementation.

**How it works:**
1. User logs in with credentials
2. Server validates credentials and issues a signed token
3. Client stores the token (typically in localStorage or a cookie)
4. Client includes the token in the Authorization header of subsequent requests
5. Server verifies the token's signature and grants access

**Strengths:**
- Stateless – no session storage on server
- Scales well across multiple servers
- Can include claims (like user role) directly in the token

**Weaknesses:**
- Token revocation is difficult (tokens are valid until expiration)
- Token size can become large
- Must be transmitted securely (HTTPS only)

**Example JWT Structure:**

```
Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"user_id": 123, "role": "admin", "exp": 1625097600}
Signature: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```

The three parts are concatenated with dots to form:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInJvbGUiOiJhZG1pbiIsImV4cCI6MTYyNTA5NzYwMH0.sQk7Q7YqX5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q
```

#### OAuth 2.0 and OpenID Connect
OAuth is an authorization framework that allows third-party applications to access user resources without sharing passwords. OpenID Connect adds an authentication layer on top of OAuth 2.0.

**Common providers:**
- Login with Google
- Login with Facebook
- Login with GitHub
- Login with Microsoft

**Flow (simplified):**
1. User clicks "Login with Google" on your site
2. Your site redirects to Google's authentication page
3. User authenticates with Google (enters password, uses 2FA, etc.)
4. Google asks the user to grant your site certain permissions
5. User approves, and Google redirects back with an authorization code
6. Your server exchanges the code for an access token
7. Your server can now request user information from Google's API

**Strengths:**
- No password storage required on your servers
- Users can use existing, trusted accounts
- Reduced registration friction

**Weaknesses:**
- Dependency on third-party providers
- Complex implementation
- Users must have accounts with the provider

#### Certificate-Based Authentication
Uses digital certificates and public-key cryptography to authenticate.

**Common in:**
- Enterprise internal systems
- Mutual TLS (mTLS) for API-to-API communication
- Smart card logins

**Strengths:**
- Very strong security
- Resistant to phishing (certificates are not easily stolen)
- No shared secrets transmitted

**Weaknesses:**
- Complex to set up and manage
- Requires certificate infrastructure
- User experience can be cumbersome

#### Biometric Authentication
Uses unique physical characteristics for authentication.

**Common implementations:**
- Fingerprint scanners on laptops and phones
- Facial recognition systems
- Iris scanners for high-security areas

**Strengths:**
- Convenient for users
- Difficult to forge (though not impossible)
- Cannot be forgotten or lost

**Weaknesses:**
- Biometric data cannot be changed if compromised
- Requires specialized hardware
- Privacy concerns around biometric data storage

---

### 8. Choosing the Right Authentication Method

The choice of authentication method depends on several factors:

| Application Type | Recommended Approach | Reasoning |
|-----------------|----------------------|-----------|
| Public blog or content site | Password only | Low sensitivity, simplicity prioritized |
| E-commerce site | Password + optional 2FA | Balance of security and convenience |
| Banking application | MFA required | High security necessary |
| Internal company tool | SSO via corporate identity provider | Centralized user management |
| Public API | Token-based (JWT or OAuth) | Stateless, scalable |
| Microservice communication | mTLS or API keys | Secure machine-to-machine |

For this Flask tutorial series, we will implement **password-based authentication** with secure hashing (bcrypt) and session management (Flask-Login). This gives you a solid foundation that you can later extend with OAuth or token-based methods.

---

### 9. Authentication in Web Applications: The Big Picture

A complete authentication system involves multiple components working together:

#### Frontend (Browser)
- Login/registration forms that collect user credentials
- Storage of session identifiers (typically in cookies)
- Conditional rendering based on authentication status

#### Backend (Server)
- Routes to handle login, registration, and logout
- Password hashing and verification logic
- Session creation and management
- Protected routes that check authentication before serving content

#### Database
- User table storing user profiles and password hashes
- Optional session storage (if not using token-based methods)
- Audit logs of authentication events

#### Security Infrastructure
- HTTPS encryption for all traffic
- Rate limiting to prevent brute-force attacks
- Input validation and sanitization
- Secure cookie configuration (HttpOnly, Secure, SameSite)

---

### 10. Common Authentication Vulnerabilities

Understanding potential attacks helps you build defenses against them.

#### Brute Force Attacks
Automated scripts try thousands of password combinations until they find the correct one.

**Mitigation:**
- Rate limiting
- Account lockout after multiple failures
- CAPTCHA after repeated attempts
- Strong password policies

#### Credential Stuffing
Attackers use username/password pairs leaked from other sites, assuming users reuse passwords.

**Mitigation:**
- Encourage or enforce unique passwords
- Monitor for suspicious login patterns
- Implement 2FA

#### Phishing
Users are tricked into entering credentials on a fake login page controlled by attackers.

**Mitigation:**
- User education
- 2FA (the attacker gets the password but cannot use the second factor)
- Browser-based protection features

#### Session Hijacking
Attackers steal a user's session cookie and impersonate them.

**Mitigation:**
- Use HttpOnly and Secure flags on cookies
- Regenerate session IDs after login
- Implement session expiration
- Use HTTPS exclusively

#### SQL Injection
Attackers inject malicious SQL through login forms to bypass authentication.

**Mitigation:**
- Use parameterized queries or ORMs
- Never concatenate user input directly into SQL strings

#### Timing Attacks
Attackers measure response time differences to infer password correctness.

**Mitigation:**
- Use constant-time comparison functions (bcrypt.checkpw does this automatically)

---

### 11. What You Will Implement in This Module

Now that you understand the theory behind authentication, here is how it will be applied in the practical exercises:

1. **User Registration** – Collect name, email, and password. Hash the password using Werkzeug's `generate_password_hash` and store it in the database.

2. **User Login** – Retrieve the user by email, verify the password using `check_password_hash`, and create a session using Flask-Login.

3. **Session Management** – Configure Flask-Login to handle user sessions, including the `@login_required` decorator to protect routes.

4. **Logout** – End the user's session and clear the login state.

5. **Conditional Templates** – Modify HTML templates to show different content based on whether the user is authenticated.

6. **Flash Messages** – Provide user feedback for failed login attempts, duplicate registrations, and other edge cases.

7. **File Download Protection** – Ensure that the secret PDF can only be downloaded by authenticated users.

By the end of this module, you will have a complete, functional authentication system that you can reuse in any future Flask project. More importantly, you will understand the security principles behind each component, enabling you to adapt and extend the system as your applications grow.