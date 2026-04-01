## Required Imports for Advanced Interaction Workflows

Robust automation scripts require explicit imports covering element location, keyboard simulation, waits, dropdown handling, and complex mouse interactions.

```python
# Core WebDriver import for launching and controlling browser instances
from selenium import webdriver

# Provides all official locator strategies such as ID, NAME, XPATH, CSS_SELECTOR
from selenium.webdriver.common.by import By

# Enables keyboard simulation including ENTER, TAB, ESCAPE and modifier keys
from selenium.webdriver.common.keys import Keys

# Supports advanced mouse interactions such as hover, drag-and-drop, right-click
from selenium.webdriver.common.action_chains import ActionChains

# Provides explicit wait functionality for synchronization control
from selenium.webdriver.support.ui import WebDriverWait

# Provides expected conditions used together with explicit waits
from selenium.webdriver.support import expected_conditions as EC

# Supports dropdown selection handling
from selenium.webdriver.support.ui import Select
```

---

## Using `By.LINK_TEXT` and `By.PARTIAL_LINK_TEXT`

`By.LINK_TEXT` matches exact visible anchor text.
`By.PARTIAL_LINK_TEXT` matches substring inside anchor text.

### Example: Clicking a Navigation Link

```python
# Initialize Chrome driver
driver = webdriver.Chrome()

# Navigate to target website
driver.get("https://example.com")

# Locate link by exact visible text and click
login_link = driver.find_element(By.LINK_TEXT, "Login")
login_link.click()

print("Login link clicked successfully")

driver.quit()
```

### Expected Output

```
Login link clicked successfully
```

### Partial Link Text Example

```python
driver = webdriver.Chrome()
driver.get("https://example.com")

# Locate link using partial match
register_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Regis")
register_link.click()

print("Partial link matched and clicked")

driver.quit()
```

---

## Automating Form Filling with `send_keys()`

### Dummy HTML Form Structure Assumption

```html
<form id="loginForm">
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">Sign In</button>
</form>
```

---

## Complete Dummy Login Automation Script

```python
# Import required Selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create browser instance
driver = webdriver.Chrome()

# Open dummy login page
driver.get("https://example.com/login")

# Wait explicitly until username input becomes available
wait = WebDriverWait(driver, 15)
username_input = wait.until(
    EC.presence_of_element_located((By.NAME, "username"))
)

# Locate password input
password_input = driver.find_element(By.NAME, "password")

# Clear fields in case of pre-filled values
username_input.clear()
password_input.clear()

# Send login credentials to respective fields
username_input.send_keys("test_user")
password_input.send_keys("secure_password")

# Submit form using ENTER key instead of clicking button
password_input.send_keys(Keys.ENTER)

print("Login form filled and submitted successfully")

driver.quit()
```

### Expected Output

```
Login form filled and submitted successfully
```

---

## Submitting via Button Click Instead of ENTER

```python
# Locate sign-in button by text using XPath
submit_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")

# Click button explicitly
submit_button.click()

print("Form submitted using button click")
```

---

## Advanced Example: Full Registration Form Automation

### Assumed Form Fields

• First Name
• Last Name
• Email
• Password
• Gender Dropdown
• Terms Checkbox

---

### Automation Script

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://example.com/register")

# Fill text fields
driver.find_element(By.NAME, "first_name").send_keys("John")
driver.find_element(By.NAME, "last_name").send_keys("Doe")
driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
driver.find_element(By.NAME, "password").send_keys("StrongPassword123")

# Handle dropdown using Select class
gender_dropdown = Select(driver.find_element(By.ID, "gender"))
gender_dropdown.select_by_visible_text("Male")

# Click checkbox if not already selected
terms_checkbox = driver.find_element(By.ID, "terms")
if not terms_checkbox.is_selected():
    terms_checkbox.click()

# Submit form using ENTER key on last input
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

print("Registration form automated successfully")

driver.quit()
```

### Expected Output

```
Registration form automated successfully
```

---

## Powerful Interaction Patterns

### 1. Waiting Before Interacting

```python
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
element.click()
```

Prevents clicking invisible or disabled elements.

---

### 2. Triggering JavaScript Events Manually

```python
element = driver.find_element(By.ID, "hidden-button")

# Force click even if element is hidden or overlayed
driver.execute_script("arguments[0].click();", element)

print("JavaScript forced click executed")
```

---

### 3. Simulating Keyboard Navigation

```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# Press TAB twice then ENTER
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.ENTER)
actions.perform()

print("Keyboard navigation simulated")
```

---

## Handling Multi-Step Login Flow

Some websites require:

1. Enter username
2. Click Next
3. Enter password
4. Click Sign In

```python
driver.get("https://example-multistep-login.com")

# Step 1: Enter username
driver.find_element(By.ID, "identifier").send_keys("test_user")

# Step 2: Click Next
driver.find_element(By.ID, "next-btn").click()

# Step 3: Wait for password field to appear
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

password_field.send_keys("secure_password")

# Step 4: Submit using ENTER
password_field.send_keys(Keys.ENTER)

print("Multi-step login automated successfully")
```

---

## Comparing Submission Strategies

| Strategy                | Mechanism                   | Best Use Case                    |
| ----------------------- | --------------------------- | -------------------------------- |
| `click()`               | Triggers button event       | Standard button-based forms      |
| `send_keys(Keys.ENTER)` | Submits via keyboard event  | Forms listening for Enter key    |
| `submit()`              | Submits parent form element | Traditional HTML forms           |
| `execute_script()`      | Forces event via JS         | Overlays or blocked interactions |

---

## Edge Case Considerations

• Always clear inputs before reusing fields
• Always use explicit waits for dynamic websites
• Never rely on `time.sleep()` in production automation
• Handle potential `ElementNotInteractableException`
• Confirm successful navigation after submission by checking URL or page element

---

## Automating Sign-In with Post-Login Validation

```python
# After submitting login form
WebDriverWait(driver, 10).until(
    EC.url_contains("dashboard")
)

print("User successfully logged in and redirected")
```

### Expected Output

```
User successfully logged in and redirected
```
