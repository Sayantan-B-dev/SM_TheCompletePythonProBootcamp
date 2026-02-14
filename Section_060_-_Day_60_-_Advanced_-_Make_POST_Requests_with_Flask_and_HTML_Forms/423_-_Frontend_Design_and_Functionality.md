## Step 5: Frontend Design and Functionality

The frontend is a single HTML page (`index.html`) located in the `templates/` folder. It serves as the user interface for the contact form, combining visual design with interactive behavior. This step explains the frontend architecture, including the HTML structure, styling with Bootstrap and custom CSS, and JavaScript that handles form submission and user feedback asynchronously.

### 5.1 Overall Structure

The page is built with HTML5 and follows a responsive two-column layout using Bootstrap's grid system. The left panel displays contact information, while the right panel contains the form. All CSS and JavaScript are embedded within the HTML file for simplicity, though in larger projects they would be separated into static files.

#### Document Declaration and Head

```html
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us | Pro Dark Form</title>

    <!-- Bootstrap 5.3 + Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <!-- Google Font (optional) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap" rel="stylesheet">

    <style>
        /* Custom CSS will be discussed later */
    </style>
</head>
```

- `data-bs-theme="dark"` applies Bootstrap's dark theme variant.
- Bootstrap CSS provides base styling and grid system.
- Bootstrap Icons are used for visual enhancements.
- Google Fonts loads the 'Inter' font for a modern look.
- Custom CSS overrides and extends Bootstrap's styles.

### 5.2 HTML Body and Layout

The body contains a container with a row that splits into two columns:

```html
<body>
<div class="container">
    <div class="row g-0 contact-card">
        <!-- LEFT INFO PANEL -->
        <div class="col-lg-5 info-panel">
            <!-- contact details -->
        </div>

        <!-- RIGHT FORM PANEL -->
        <div class="col-lg-7 form-panel">
            <!-- form fields -->
        </div>
    </div>
</div>
```

- `container` centers the content and provides responsive padding.
- `row g-0` removes gutters between columns.
- `col-lg-5` and `col-lg-7` create a 5:7 split on large screens; on smaller screens they stack vertically.
- Custom classes `contact-card`, `info-panel`, `form-panel` add styling.

#### Left Panel – Contact Information

```html
<div class="col-lg-5 info-panel d-flex flex-column">
    <h2 class="section-title">Let’s connect</h2>
    <p class="text-secondary mb-4">Have a project in mind? We’re here to turn ideas into reality.</p>

    <div class="info-item">
        <div class="info-icon"><i class="bi bi-geo-alt-fill"></i></div>
        <div class="info-text">
            <strong>Visit us</strong>
            Barasat, West Bengal, India
        </div>
    </div>
    <!-- similar blocks for phone, email, hours -->
    <div class="mt-auto pt-4">
        <hr class="border-white opacity-25">
        <div class="d-flex gap-3">
            <a href="#" class="text-white opacity-75"><i class="bi bi-twitter-x fs-5"></i></a>
            <a href="#" class="text-white opacity-75"><i class="bi bi-linkedin"></i></a>
            <a href="#" class="text-white opacity-75"><i class="bi bi-github"></i></a>
        </div>
    </div>
</div>
```

- Each contact method is wrapped in `info-item` with an icon and text.
- `mt-auto` pushes the social links to the bottom of the panel (flex column).

#### Right Panel – Form

```html
<div class="col-lg-7 form-panel">
    <h3 class="section-title">Send a message</h3>
    <p class="text-secondary mb-4">We’ll reply within 24 hours.</p>

    <div id="alert-container"></div>  <!-- Dynamic alerts appear here -->

    <form id="contactForm" class="needs-validation" novalidate>
        <!-- Floating label for Name -->
        <div class="form-floating mb-4">
            <input type="text" class="form-control" id="name" placeholder="Your name" required>
            <label for="name"><i class="bi bi-person me-2"></i>Full name *</label>
            <div class="invalid-feedback">Please enter your name.</div>
        </div>

        <!-- Floating label for Email -->
        <div class="form-floating mb-4">
            <input type="email" class="form-control" id="email" placeholder="name@example.com" required>
            <label for="email"><i class="bi bi-envelope me-2"></i>Email address *</label>
            <div class="invalid-feedback">Valid email required.</div>
        </div>

        <!-- Project type dropdown -->
        <div class="mb-4">
            <label for="project_type" class="form-label"><i class="bi bi-code-slash me-2"></i>Project type *</label>
            <select class="form-select form-select-lg" id="project_type" required>
                <option value="" selected disabled>Select project type</option>
                <option value="Web Development">Web Development</option>
                <option value="Mobile App">Mobile App</option>
                <option value="UI/UX Design">UI/UX Design</option>
                <option value="Consulting">Consulting</option>
                <option value="Other">Other</option>
            </select>
            <div class="invalid-feedback">Please choose a project type.</div>
        </div>

        <!-- Budget dropdown -->
        <div class="mb-4">
            <label for="budget" class="form-label"><i class="bi bi-currency-dollar me-2"></i>Budget range *</label>
            <select class="form-select form-select-lg" id="budget" required>
                <option value="" selected disabled>Select budget</option>
                <option value="Less than $1,000">Less than $1,000</option>
                <option value="$1,000 – $5,000">$1,000 – $5,000</option>
                <option value="$5,000 – $10,000">$5,000 – $10,000</option>
                <option value="$10,000+">$10,000+</option>
            </select>
            <div class="invalid-feedback">Please select a budget range.</div>
        </div>

        <!-- Floating label for Message -->
        <div class="form-floating mb-5">
            <textarea class="form-control" id="message" placeholder="Your message" style="min-height: 140px;" required></textarea>
            <label for="message"><i class="bi bi-chat-dots me-2"></i>Message *</label>
            <div class="invalid-feedback">Please write your message.</div>
        </div>

        <button type="submit" class="btn btn-submit w-100" id="submitBtn">
            <span class="button-text">Send message</span>
            <span class="spinner-border spinner-border-sm d-none" role="status"></span>
        </button>
    </form>
</div>
```

- **Floating labels**: Using Bootstrap's `form-floating` class, labels appear inside the input and float up when the field is focused or has content. This saves space and looks modern.
- **Validation feedback**: Each field includes an `invalid-feedback` div that appears when the `was-validated` class is applied to the form and the field fails browser validation.
- **Submit button**: Contains a text span and a hidden spinner that will be shown during submission to indicate loading.
- **`novalidate`**: Disables the browser's default validation popups; we use Bootstrap's custom validation UI.

### 5.3 Custom CSS Styling

The `<style>` block contains extensive customizations to achieve a dark, professional look while maintaining readability and accessibility.

#### Key Customizations

- **Body background**: `#0b0e14` – a deep dark color.
- **Card styling**: Rounded corners, border, shadow.
- **Info panel**: Slightly darker background with subtle border.
- **Form inputs**: Dark backgrounds with light text, white borders, and glow on focus.
- **Button**: Gradient-like effect with hover animation.

Example of input styling:

```css
.form-floating > .form-control,
.form-floating > .form-select {
    background: #1a212e;
    border: 2px solid rgba(255,255,255,0.1);
    border-radius: 1.2rem;
    height: calc(3.8rem + 2px);
    padding: 1.2rem 1rem 0.4rem;
    color: white;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-floating > .form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 3px rgba(13,110,253,0.25);
    background: #1e2636;
}
```

- The focus state adds a blue glow consistent with Bootstrap's primary color.
- `border-radius: 1.2rem` gives pill-shaped inputs.

#### Responsive Adjustments

```css
@media (max-width: 991px) {
    .info-panel {
        border-right: none;
        border-bottom: 2px solid rgba(255,255,255,0.08);
    }
}
```

- On smaller screens, the left panel loses its right border and gains a bottom border to separate from the form.

### 5.4 JavaScript for Asynchronous Form Submission

The JavaScript code is placed just before the closing `</body>` tag. It handles:
- Intercepting form submission.
- Performing Bootstrap's client-side validation.
- Collecting data and sending it to the server via Fetch API.
- Displaying success/error messages in the alert container.
- Managing the button state (disable, show spinner) during the request.

#### 5.4.1 DOM Element References

```javascript
const form = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const spinner = submitBtn.querySelector('.spinner-border');
const buttonText = submitBtn.querySelector('.button-text');
const alertContainer = document.getElementById('alert-container');
```

#### 5.4.2 Helper Function to Show Alerts

```javascript
function showAlert(message, type) {
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    if (type === 'success') {
        setTimeout(() => {
            const alert = document.querySelector('.alert');
            if (alert) bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 5000);
    }
}
```

- Creates a Bootstrap alert dynamically.
- Uses different icons based on success/error.
- Success alerts auto-dismiss after 5 seconds using Bootstrap's Alert API.

#### 5.4.3 Form Submit Event Listener

```javascript
form.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Check browser validation
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    form.classList.remove('was-validated');
```

- `e.preventDefault()` stops the page from reloading.
- `form.checkValidity()` triggers the browser's built-in validation (based on `required` attributes and `type="email"`). If invalid, `was-validated` class is added to show the validation messages, and submission stops.

#### 5.4.4 Collecting Form Data

```javascript
const payload = {
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    project_type: document.getElementById('project_type').value,
    budget: document.getElementById('budget').value,
    message: document.getElementById('message').value.trim()
};
```

- Values are trimmed to avoid sending whitespace-only fields.
- The phone field is omitted because it's not present in this version (though backend supports it).

#### 5.4.5 Disabling Button and Showing Spinner

```javascript
submitBtn.disabled = true;
spinner.classList.remove('d-none');
buttonText.classList.add('opacity-75');
```

- Disables the button to prevent double submission.
- Removes the `d-none` class from the spinner to make it visible.
- Adds opacity to the button text for visual feedback.

#### 5.4.6 Sending the Request with Fetch

```javascript
try {
    const response = await fetch('/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (data.success) {
        showAlert(data.message, 'success');
        form.reset();
    } else {
        showAlert(data.message || 'Something went wrong.', 'danger');
    }
} catch (error) {
    console.error('Fetch error:', error);
    showAlert('Network error. Please try again.', 'danger');
} finally {
    submitBtn.disabled = false;
    spinner.classList.add('d-none');
    buttonText.classList.remove('opacity-75');
}
```

- **`fetch`**: Sends a POST request with JSON payload.
- **`await`**: Waits for the response and then parses JSON.
- **Success path**: Displays success alert and resets the form.
- **Error path**: Displays error alert with message from server or a generic network error.
- **`finally`**: Always re-enables the button and hides the spinner, regardless of outcome.

### 5.5 How Client-Side Validation Complements Server-Side Validation

- **Client-side validation** (HTML5 attributes + Bootstrap) provides instant feedback and reduces unnecessary server requests.
- **Server-side validation** (in `app.py`) is the ultimate gatekeeper; it ensures data integrity even if client-side checks are bypassed.
- Both layers work together: the frontend catches common mistakes early, while the backend enforces security and completeness.

### 5.6 Responsive Behavior

- On large screens, the two panels sit side by side.
- On tablets and phones, the panels stack vertically, with the form appearing below the contact info.
- Inputs and buttons scale appropriately due to Bootstrap's responsive utilities.

### 5.7 Accessibility Considerations

- All form inputs have associated `<label>` elements.
- Icons are decorative and used with screen reader text (though not explicitly marked, they are within labels).
- The button includes a spinner with `role="status"` to indicate loading.
- Alerts are dismissible and have appropriate ARIA roles.

### 5.8 Summary

The frontend is a self-contained, modern contact form that communicates with the backend via asynchronous JavaScript. It provides a polished user experience with immediate validation, loading states, and clear feedback messages. The design is fully responsive and adheres to current web standards. By embedding CSS and JS within the template, the project remains simple to deploy, yet it demonstrates key frontend concepts such as DOM manipulation, event handling, AJAX, and dynamic UI updates.