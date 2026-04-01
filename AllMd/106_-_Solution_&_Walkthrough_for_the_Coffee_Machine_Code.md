# ☕ COFFEE MACHINE — MULTI PRODUCT, SINGLE PAYMENT SYSTEM

***Terminal-Based Simulation | Professional Documentation***

---

## 📌 Overview

This program simulates a **realistic coffee vending machine** in a terminal environment.
It allows users to:

• Select **multiple different coffee products**
• Select **one product multiple times**
• View the **total cost before paying**
• Make a **single consolidated payment**
• Receive **change if applicable**
• View a **live machine resource report**
• Safely shut down the machine

The design strictly follows **real-world vending machine logic**:

> *No payment is accepted unless the machine can fulfill the entire order.*

---

## 🎯 Design Goals

✔ Clean procedural architecture
✔ Clear separation of concerns
✔ Fail-safe transaction handling
✔ Easily extendable (new drinks, discounts, persistence)
✔ Human-readable terminal UI

---

## 🧱 Core Data Structures

### 🔹 MENU (Immutable Configuration)

```text
MENU
 ├── espresso
 │    ├── ingredients → water, milk, coffee
 │    └── cost → ₹120
 ├── latte
 │    ├── ingredients → water, milk, coffee
 │    └── cost → ₹180
 └── cappuccino
      ├── ingredients → water, milk, coffee
      └── cost → ₹200
```

**Purpose**
• Single source of truth for all products
• Adding a new coffee requires *only one entry*

---

### 🔹 resources (Mutable Runtime State)

```text
resources
 ├── water  → 1000 ml
 ├── milk   → 800 ml
 └── coffee → 500 g
```

**Purpose**
• Tracks live ingredient availability
• Updated **only after successful payment**

---

### 🔹 coins (Payment System)

```text
coins
 ├── 10rs  → 10
 ├── 20rs  → 20
 ├── 50rs  → 50
 └── 100rs → 100
```

**Purpose**
• Models real coin-based input
• Easily extensible to notes or digital payments

---

### 🔹 money_earned

```text
money_earned → integer (₹)
```

**Purpose**
• Tracks total revenue collected by the machine

---

### 🔹 machine_on

```text
machine_on → Boolean
```

**Purpose**
• Controls the main execution loop
• Enables graceful shutdown

---

## 🧩 Functional Architecture

### 🔸 UI Helpers

#### `line()`

```text
Prints a visual separator for terminal readability
```

Used to:
• Separate sections
• Improve user experience
• Maintain clean output layout

---

#### `show_menu()`

```text
Displays all available coffee items with prices
```

Responsibilities:
• Reads directly from `MENU`
• Avoids hard-coded product names
• Ensures consistency across UI

---

### 🔸 Resource Management

#### `check_resources(cart)`

```text
Input : cart → { drink_name : quantity }
Output: (Boolean, missing_ingredient | None)
```

**What it does**

1. Aggregates total ingredient demand across the entire cart
2. Compares required quantities with available resources
3. Fails fast if *any* ingredient is insufficient

**Why this matters**
• Prevents partial orders
• Matches real vending machine behavior

---

#### `make_order(cart)`

```text
Deducts ingredients from resources after payment success
```

**Key Rule**

> ⚠️ This function is **never called** unless payment succeeds.

---

### 🔸 Payment Handling

#### `take_payment(total_cost)`

```text
Input : total_cost (₹)
Output: (Boolean, amount_earned)
```

**Flow**

1. Displays total payable amount
2. Accepts coin quantities from user
3. Calculates total paid
4. Validates payment
5. Returns change if applicable

**Fail-Safe Behavior**
• Insufficient payment → full refund
• No resource or money mutation occurs

---

## 🔁 Main Program Flow

### 🟢 Startup

```text
WELCOME MESSAGE
↓
Display Main Menu
↓
Enter Control Loop
```

---

### 🛒 Order Flow (Option 1)

```text
Create empty cart
↓
User selects products + quantities
↓
User types "done"
↓
Display order summary
↓
Check aggregated resources
↓
If sufficient → take payment
↓
If payment successful:
    → deduct resources
    → add money
    → serve coffee
```

---

### 📊 Report Flow (Option 2)

Displays:
• Remaining water
• Remaining milk
• Remaining coffee
• Total money earned

No state mutation occurs.

---

### 🔌 Shutdown Flow (Option 3)

```text
machine_on = False
↓
Exit loop
↓
Program terminates cleanly
```

---

## 🧠 Transaction Integrity Rules

✔ No payment without resources
✔ No resource deduction without payment
✔ No partial fulfillment
✔ One payment per order
✔ All failures revert safely

---

## 🧾 Example Order Scenario

```text
User selects:
- espresso x2
- latte x1

Total cost: ₹420

Machine checks:
✓ water
✓ milk
✓ coffee

User pays ₹500
Change returned: ₹80

Resources updated
Money earned updated
Coffee served ☕
```

---

## 🧩 Extensibility Points

This architecture supports:

• Adding new drinks
• Discount systems
• Combo offers
• Persistent storage (save/load machine state)
• OOP refactor (`CoffeeMachine`, `Order`, `Payment`)
• GUI front-ends

---

## ✅ Summary

This program is a **production-grade terminal simulation** with:

✔ Clean logic
✔ Realistic constraints
✔ Strong separation of concerns
✔ Scalable architecture
✔ Human-friendly interaction

It is suitable as:
• A learning project
• A system-design exercise
• A base for OOP refactoring
• A portfolio-quality terminal application

If you want the **next step**, ask for:
• OOP refactor
• UML diagrams
• Persistence layer
• Testing strategy
• Feature expansion
