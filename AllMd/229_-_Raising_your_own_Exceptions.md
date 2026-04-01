## Custom Exceptions — from **simple** to **industrial-grade**, all realistic and intentional

---

## 1. What a custom exception really is (definition)

A **custom exception** is a domain-specific signal that communicates **meaning**, not mechanics.

> Built-in exceptions describe *what failed technically*
> Custom exceptions describe *what failed logically or business-wise*

They:

* Express intent
* Separate technical failure from business rules
* Make APIs predictable
* Are heavily used in high-paying backend roles

---

## 2. Rules professionals follow (important)

| Rule                      | Why                         |
| ------------------------- | --------------------------- |
| Inherit from `Exception`  | Avoid catching system exits |
| Name ends with `Error`    | Convention                  |
| One concept per exception | Precision                   |
| Raise early               | Fail fast                   |
| Chain lower errors        | Debuggability               |

---

## 3. SIMPLE custom exceptions (beginner → solid)

### 3.1 ValidationError (classic)

```python
class ValidationError(Exception):
    pass
```

#### Use

```python
def set_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
    return age
```

**Expected output**

```
ValidationError: Age cannot be negative
```

---

### 3.2 NotFoundError

```python
class NotFoundError(Exception):
    pass
```

```python
def get_user(users, user_id):
    if user_id not in users:
        raise NotFoundError("User does not exist")
    return users[user_id]
```

---

## 4. MODERATE custom exceptions (realistic backend)

### 4.1 Base domain exception (best practice)

```python
class DomainError(Exception):
    pass
```

All domain exceptions inherit from this.

---

### 4.2 Business rule violation

```python
class BusinessRuleError(DomainError):
    pass
```

```python
def withdraw(balance, amount):
    if amount > balance:
        raise BusinessRuleError("Insufficient balance")
    return balance - amount
```

---

### 4.3 AuthorizationError

```python
class AuthorizationError(DomainError):
    pass
```

```python
def delete_record(is_admin):
    if not is_admin:
        raise AuthorizationError("Admin privileges required")
```

---

## 5. CLASSIC INDUSTRIAL PATTERN (layered)

### Base exception

```python
class ApplicationError(Exception):
    pass
```

### Technical layer

```python
class DatabaseError(ApplicationError):
    pass

class CacheError(ApplicationError):
    pass
```

### Business layer

```python
class OrderError(ApplicationError):
    pass

class PaymentError(OrderError):
    pass

class InventoryError(OrderError):
    pass
```

---

## 6. REALISTIC INDUSTRIAL EXAMPLES (multiple domains)

---

### 6.1 Data Pipeline (ETL / ML / Analytics)

```python
class DataPipelineError(Exception):
    pass

class DataSourceMissing(DataPipelineError):
    pass

class DataFormatInvalid(DataPipelineError):
    pass

class DataConsistencyError(DataPipelineError):
    pass
```

```python
def load_data(data):
    if data is None:
        raise DataSourceMissing("Data source returned nothing")
    if not isinstance(data, dict):
        raise DataFormatInvalid("Expected dict data")
    if "id" not in data:
        raise DataConsistencyError("Missing primary key")
```

---

### 6.2 Payments system (fintech)

```python
class PaymentError(Exception):
    pass

class CardExpired(PaymentError):
    pass

class InsufficientFunds(PaymentError):
    pass

class PaymentGatewayDown(PaymentError):
    pass
```

```python
def charge(card_valid, balance, amount):
    if not card_valid:
        raise CardExpired("Card expired")
    if amount > balance:
        raise InsufficientFunds("Not enough balance")
```

---

### 6.3 Authentication / Security

```python
class AuthError(Exception):
    pass

class InvalidCredentials(AuthError):
    pass

class AccountLocked(AuthError):
    pass

class TokenExpired(AuthError):
    pass
```

```python
def login(password, locked):
    if locked:
        raise AccountLocked("Account is locked")
    if password != "secret":
        raise InvalidCredentials("Wrong password")
```

---

### 6.4 APIs / Microservices

```python
class ServiceError(Exception):
    pass

class ServiceUnavailable(ServiceError):
    pass

class Timeout(ServiceError):
    pass

class BadRequest(ServiceError):
    pass
```

```python
def call_service(response_time):
    if response_time > 5:
        raise Timeout("Service timeout")
```

---

## 7. Raising custom exceptions **compactly** (professional style)

### 7.1 Inline raise (short, expressive)

```python
age = -1
age >= 0 or raise ValueError("Age must be positive")
```

(Not commonly used — readable but risky)

---

### 7.2 Guard clause (preferred)

```python
def create_user(age):
    if age < 18:
        raise BusinessRuleError("User must be adult")
```

---

### 7.3 Raise with context (best)

```python
if amount <= 0:
    raise ValidationError(f"Invalid amount: {amount}")
```

---

## 8. Exception chaining (critical for production)

```python
class FileProcessingError(Exception):
    pass
```

```python
try:
    open("missing.txt")
except FileNotFoundError as e:
    raise FileProcessingError("Failed to load config") from e
```

**Why**

* Keeps root cause
* Enables tracing
* Mandatory in large systems

---

## 9. Wrapping low-level errors into domain errors

```python
class UserServiceError(Exception):
    pass
```

```python
def fetch_user():
    try:
        int("abc")
    except ValueError as e:
        raise UserServiceError("User parsing failed") from e
```

---

## 10. Custom exception + logging (industry standard)

```python
import logging

class OrderProcessingError(Exception):
    pass

try:
    raise OrderProcessingError("Order failed")
except OrderProcessingError:
    logging.exception("Critical failure in order pipeline")
```

---

## 11. When NOT to create custom exceptions

| Situation          | Use instead  |
| ------------------ | ------------ |
| Index out of range | `IndexError` |
| Wrong type         | `TypeError`  |
| Invalid value      | `ValueError` |
| Parsing failure    | `ValueError` |

Custom exceptions are for **meaning**, not duplication.

---

## 12. Interview-level mental model

> Built-in exceptions describe **how** code failed
> Custom exceptions describe **why** the system failed

---

## 13. Final compact hierarchy example (perfect answer quality)

```python
class AppError(Exception): pass
class ValidationError(AppError): pass
class AuthError(AppError): pass
class PaymentError(AppError): pass
class InsufficientFunds(PaymentError): pass
class CardExpired(PaymentError): pass
```

This is **clean**, **scalable**, and **industry-approved**.

---

If you can design, name, raise, and chain custom exceptions like this, you are already writing **production-grade Python**.
