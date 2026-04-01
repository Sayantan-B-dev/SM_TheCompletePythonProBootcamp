# Step 3 — Human Interaction Simulation and Behavioral Anti-Detection Layer

## 1. Objective of This Step

After deterministic navigation control, the next structural layer is behavioral realism.
Modern websites do not rely solely on static fingerprint detection; they analyze interaction patterns, timing consistency, and behavioral entropy.

This step focuses exclusively on:

* Randomized delay injection
* Behavioral timing variability
* Structured interaction pacing
* Popup and window anomaly handling

The goal is not randomness for its own sake, but statistically human-like temporal behavior.

---

## 2. Core Human Simulation Functions (Heavily Commented)

```python
import time
import random
from selenium.webdriver.common.by import By


def human_delay(minimum_seconds: float = 1.8, maximum_seconds: float = 3.5):
    """
    Introduces a randomized delay between actions.

    Why this exists:
    - Humans do not act at deterministic intervals.
    - Fixed delays create detectable timing signatures.
    - Random jitter reduces behavioral predictability.

    Parameters:
    minimum_seconds: Lower bound of delay window.
    maximum_seconds: Upper bound of delay window.
    """

    # Generate a floating-point random number within the specified range.
    randomized_sleep_duration = random.uniform(minimum_seconds, maximum_seconds)

    # Suspend execution for the generated duration.
    time.sleep(randomized_sleep_duration)



def handle_popups(driver):
    """
    Handles unexpected browser behaviors such as:
    - Ad popups opening new tabs
    - Modal overlays blocking interaction
    - Close buttons that obstruct scraping

    This function improves scraper robustness.
    """

    try:
        # Check if multiple browser windows exist.
        # Many ad networks open new tabs silently.
        if len(driver.window_handles) > 1:

            # The first handle is considered the main window.
            main_window_handle = driver.window_handles[0]

            # Iterate over all open window handles.
            for window_handle in driver.window_handles:

                # Close any window that is not the primary one.
                if window_handle != main_window_handle:
                    driver.switch_to.window(window_handle)
                    driver.close()

            # Switch back to main window.
            driver.switch_to.window(main_window_handle)

    except Exception:
        # Silently ignore window handling errors to avoid interruption.
        pass

    try:
        # Attempt to locate modal close buttons.
        close_button_elements = driver.find_elements(
            By.CSS_SELECTOR,
            ".close, .btn-close, .modal-close"
        )

        # Attempt to click each close button safely.
        for close_button in close_button_elements:
            try:
                close_button.click()
            except Exception:
                continue

    except Exception:
        # Ignore modal handling exceptions.
        pass
```

---

## 3. Expected Behavioral Output

There is no visible textual output from these functions.
Instead, the browser behaves more organically:

* Pauses between actions
* Avoids rapid-fire clicks
* Recovers from popup interruptions
* Maintains session continuity

---

## 4. Why Behavioral Simulation Matters

### 4.1 Timing Signature Detection

Bots often perform actions in exact intervals:

```
Action → 2.000 seconds → Action → 2.000 seconds
```

Humans exhibit:

```
Action → 2.37 seconds → Action → 3.12 seconds → Action → 1.94 seconds
```

Uniform timing is statistically anomalous.

---

### 4.2 Popup Handling as Stability Layer

Without popup handling:

* Scraper switches to wrong window
* Clicks target wrong DOM
* NoSuchElementException occurs
* Execution halts unpredictably

Popup control acts as fault-tolerance middleware.

---

## 5. Alternative Human Simulation Techniques

### Alternative 1 — Gaussian Delay Distribution

More natural than uniform randomness.

```python
def gaussian_delay(mean: float = 2.5, standard_deviation: float = 0.7):
    """
    Uses normal distribution to simulate more realistic delay.
    """
    delay_value = max(0.5, random.gauss(mean, standard_deviation))
    time.sleep(delay_value)
```

Why superior:
Human reaction time clusters around a mean, not uniform distribution.

---

### Alternative 2 — Scroll Simulation

Simulate reading behavior.

```python
def simulate_scroll(driver):
    """
    Scrolls gradually to simulate human reading behavior.
    """
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    for scroll_position in range(0, scroll_height, 300):
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(random.uniform(0.3, 0.8))
```

Use when:

* Website monitors scroll behavior
* Lazy-loaded content exists

---

### Alternative 3 — Mouse Movement Simulation

```python
from selenium.webdriver.common.action_chains import ActionChains

def simulate_mouse_movement(driver, element):
    """
    Moves mouse cursor to an element before clicking.
    """
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
```

Helps reduce click anomaly detection.

---

## 6. Best Practices for Behavioral Realism

### 6.1 Randomize Within Logical Bounds

Avoid extreme ranges such as:

```python
random.uniform(0.1, 10)
```

Large delays degrade performance.
Extremely small delays look robotic.

---

### 6.2 Keep Behavior Consistent Across Session

Random does not mean chaotic.
Maintain a stable behavioral profile.

---

### 6.3 Handle Windows Before Scraping

Always call:

```python
handle_popups(driver)
```

Before extracting elements or navigating pages.

---

### 6.4 Avoid Excessive Complexity

Behavior simulation should improve stealth, not complicate architecture.
Over-engineering introduces new failure vectors.

---

## 7. Architectural Role of Step 3

This layer introduces:

* Behavioral entropy
* Runtime fault tolerance
* Interaction pacing realism
* Session continuity protection

At this stage, the automation system now includes:

1. Stable browser configuration
2. Deterministic navigation control
3. Human-like interaction pacing

The scraper is now prepared to enter structured data extraction safely.

---
