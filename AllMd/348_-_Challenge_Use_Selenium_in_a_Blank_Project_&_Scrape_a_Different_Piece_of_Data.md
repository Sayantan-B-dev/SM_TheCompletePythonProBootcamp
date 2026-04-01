## WebElement Interaction Methods in Selenium

A **WebElement** represents a live DOM node reference inside the controlled browser session. Interaction methods trigger real user-like behavior through the WebDriver protocol. Each interaction translates into browser-level automation commands, not simulated HTML changes.

---

## 1. Clicking Elements

### Method: `element.click()`

Used for buttons, links, checkboxes, radio buttons, and clickable containers.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")

# Locate button element by ID
submit_button = driver.find_element(By.ID, "submit-btn")

# Perform real click interaction
submit_button.click()

print("Button clicked successfully")

driver.quit()
```

### Expected Output

```
Button clicked successfully
```

### Behavioral Notes

• Fails if element is hidden or covered
• Requires element to be visible and enabled
• Triggers JavaScript click handlers

---

## 2. Sending Keyboard Input

### Method: `element.send_keys()`

Used for typing into input fields, textareas, or simulating key presses.

```python
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://example.com/login")

# Locate input field
email_input = driver.find_element(By.NAME, "email")

# Type text into input
email_input.send_keys("user@example.com")

# Press Enter key
email_input.send_keys(Keys.ENTER)

print("Text entered and Enter pressed")

driver.quit()
```

### Expected Output

```
Text entered and Enter pressed
```

### Supported Special Keys

| Key              | Usage             |
| ---------------- | ----------------- |
| `Keys.ENTER`     | Submit forms      |
| `Keys.TAB`       | Move focus        |
| `Keys.ESCAPE`    | Close dialogs     |
| `Keys.BACKSPACE` | Delete characters |
| `Keys.CONTROL`   | Modifier key      |

---

## 3. Clearing Input Fields

### Method: `element.clear()`

Removes existing text before sending new input.

```python
search_box = driver.find_element(By.ID, "search")

search_box.clear()
search_box.send_keys("New Query")

print("Input field cleared and updated")
```

### Expected Output

```
Input field cleared and updated
```

---

## 4. Submitting Forms

### Method: `element.submit()`

Triggers form submission if element is inside a `<form>` tag.

```python
form_input = driver.find_element(By.NAME, "username")

form_input.send_keys("admin")
form_input.submit()

print("Form submitted")
```

### Expected Output

```
Form submitted
```

### Important Behavior

This works only if element belongs to a form. Modern JavaScript-heavy apps often override default submission.

---

## 5. Reading Element Text

### Property: `element.text`

Extracts visible rendered content.

```python
title = driver.find_element(By.TAG_NAME, "h1")

print(title.text)
```

### Expected Output

```
Welcome Page
```

Hidden elements return empty string.

---

## 6. Getting Attributes

### Method: `element.get_attribute()`

Retrieves any attribute value including dynamic ones.

```python
image = driver.find_element(By.TAG_NAME, "img")

image_source = image.get_attribute("src")

print(image_source)
```

### Expected Output

```
https://example.com/image.jpg
```

---

## 7. Getting CSS Properties

### Method: `element.value_of_css_property()`

Extracts computed style properties.

```python
box = driver.find_element(By.CLASS_NAME, "highlight")

background_color = box.value_of_css_property("background-color")

print(background_color)
```

### Expected Output

```
rgba(255, 0, 0, 1)
```

---

## 8. Checking Element State

### Visibility Check

```python
element = driver.find_element(By.ID, "menu")

print(element.is_displayed())
```

### Expected Output

```
True
```

### Enabled Check

```python
button = driver.find_element(By.ID, "submit")

print(button.is_enabled())
```

### Selected Check

```python
checkbox = driver.find_element(By.ID, "agree")

print(checkbox.is_selected())
```

---

## 9. Mouse Interactions with ActionChains

### Hover Interaction

```python
from selenium.webdriver.common.action_chains import ActionChains

menu = driver.find_element(By.ID, "dropdown")

actions = ActionChains(driver)

# Move mouse to element
actions.move_to_element(menu).perform()

print("Hover performed")
```

### Expected Output

```
Hover performed
```

---

### Right Click (Context Click)

```python
actions.context_click(menu).perform()

print("Right click executed")
```

---

### Double Click

```python
actions.double_click(menu).perform()

print("Double click executed")
```

---

## 10. Drag and Drop

```python
source = driver.find_element(By.ID, "drag-item")
target = driver.find_element(By.ID, "drop-zone")

actions.drag_and_drop(source, target).perform()

print("Drag and drop completed")
```

### Expected Output

```
Drag and drop completed
```

---

## 11. JavaScript Execution Interaction

### Method: `driver.execute_script()`

Used when standard interaction fails.

```python
element = driver.find_element(By.ID, "hidden-btn")

# Force click using JavaScript
driver.execute_script("arguments[0].click();", element)

print("JavaScript click executed")
```

### Expected Output

```
JavaScript click executed
```

---

## 12. Scrolling to Element

```python
element = driver.find_element(By.ID, "footer")

driver.execute_script("arguments[0].scrollIntoView();", element)

print("Scrolled to footer")
```

---

## 13. File Upload Interaction

File inputs can receive local file paths directly.

```python
file_input = driver.find_element(By.ID, "file-upload")

file_input.send_keys("C:/Users/username/Documents/sample.pdf")

print("File uploaded")
```

### Expected Output

```
File uploaded
```

---

## 14. Handling Dropdowns (Select Class)

```python
from selenium.webdriver.support.ui import Select

dropdown = Select(driver.find_element(By.ID, "country"))

# Select by visible text
dropdown.select_by_visible_text("India")

# Select by value attribute
dropdown.select_by_value("IN")

# Select by index
dropdown.select_by_index(1)

print("Dropdown selection completed")
```

### Expected Output

```
Dropdown selection completed
```

---

## 15. Switching Frames

```python
# Switch into iframe
driver.switch_to.frame("frame-name")

print("Switched to iframe")

# Switch back to main document
driver.switch_to.default_content()
```

---

## 16. Handling Alerts

```python
alert = driver.switch_to.alert

print(alert.text)

alert.accept()
```

### Expected Output

```
Are you sure?
```

---

## 17. Window and Tab Handling

```python
# Store current window
main_window = driver.current_window_handle

# Open new tab
driver.execute_script("window.open('https://example.com');")

# Switch to new tab
driver.switch_to.window(driver.window_handles[1])

print("Switched to new tab")
```

---

## Summary of Interaction Categories

| Category           | Methods                               |
| ------------------ | ------------------------------------- |
| Basic Actions      | click, send_keys, clear, submit       |
| State Checks       | is_displayed, is_enabled, is_selected |
| Attribute Access   | get_attribute, text, tag_name         |
| Mouse Actions      | hover, double_click, drag_and_drop    |
| Keyboard Actions   | Keys.ENTER, Keys.TAB, etc.            |
| JavaScript Control | execute_script                        |
| Browser Control    | switch_to.frame, switch_to.window     |
| Special Elements   | Select, alert handling                |

