## Step 5: Client-Side Interactivity and Theme Management

While Flask handles server-side logic and HTML generation, the user experience is greatly enhanced by client-side JavaScript. The FlaskBlog application includes a custom `main.js` file that adds interactivity, animations, and user preference persistence. This step explores each JavaScript feature, how it integrates with the HTML templates, and the overall client-server interaction.

### 5.1 The Structure of `main.js`

The script is wrapped in a `DOMContentLoaded` event listener to ensure the DOM is fully loaded before any manipulations occur. It initializes several features:

- AOS (Animate on Scroll) library
- Preloader removal
- Theme toggling with local storage
- Back to top button behavior
- Navbar background change on scroll
- Smooth scrolling for anchor links
- Auto-dismissal of flash messages
- Newsletter form demo submission
- Active navigation link highlighting

### 5.2 AOS Initialization

```javascript
AOS.init({
    duration: 800,
    once: true,
    offset: 100
});
```

AOS (Animate on Scroll) is a library that triggers animations when elements enter the viewport. The configuration sets:
- `duration: 800` – animation duration in milliseconds.
- `once: true` – animation occurs only once.
- `offset: 100` – offset (in pixels) from the original trigger point.

In templates, elements are given `data-aos` attributes (e.g., `data-aos="fade-up"`) to define the animation. This integration provides smooth scroll-based animations without heavy custom code.

### 5.3 Preloader

```javascript
const preloader = document.getElementById('preloader');
if (preloader) {
    window.addEventListener('load', function() {
        preloader.classList.add('hidden');
    });
}
```

The preloader is a full-screen overlay with a spinner, defined in `base.html`. It is hidden once the `load` event fires (i.e., all resources like images are loaded). The `hidden` class (defined in CSS) fades out the preloader and removes it from visibility.

### 5.4 Theme Toggle with Local Storage

The theme system uses CSS custom properties (variables) and a `data-theme` attribute on the `<html>` element. JavaScript toggles this attribute and stores the user’s preference in `localStorage`.

**HTML element in `base.html`:** No initial `data-theme`; defaults to light theme.

**JavaScript:**

```javascript
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') || 'light';

if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
}

themeToggle.addEventListener('click', function() {
    let theme = document.documentElement.getAttribute('data-theme');
    if (theme === 'dark') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
});
```

- On page load, it checks `localStorage` for a saved theme. If `'dark'`, it sets the `data-theme` attribute and changes the toggle icon to a sun (indicating light mode is available).
- Clicking the toggle button toggles the attribute and updates both `localStorage` and the icon.
- The CSS file contains rules like `[data-theme="dark"] { --primary-color: ... }` that override the CSS variables, causing the entire page to recolor.

**CSS variable example:**
```css
:root {
    --primary-color: #4361ee;
    --text-dark: #212529;
    /* ... */
}
[data-theme="dark"] {
    --primary-color: #6c63ff;
    --text-dark: #c0c5ce;
    /* ... */
}
```

This approach allows for a seamless theme switch without reloading the page.

### 5.5 Back to Top Button

```javascript
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});

backToTop.addEventListener('click', function(e) {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
```

- The button (fixed at bottom right) is initially hidden via CSS (`opacity: 0; visibility: hidden;`). When the user scrolls past 300px, the `show` class makes it visible.
- Clicking triggers a smooth scroll back to the top using `window.scrollTo` with `behavior: 'smooth'`.

### 5.6 Navbar Background Change on Scroll

```javascript
const navbar = document.getElementById('mainNav');
window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(0, 0, 0, 0.8)';
        navbar.style.backdropFilter = 'blur(15px)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.15)';
        navbar.style.backdropFilter = 'blur(10px)';
    }
});
```

This enhances the glassmorphism effect: when the page is scrolled down, the navbar becomes darker and more blurred to improve readability over varying backgrounds.

### 5.7 Smooth Scrolling for Anchor Links

```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
```

Any link with an `href` starting with `#` (e.g., `#section`) gets a smooth scroll behavior. This enhances navigation within a page (though the current site has few such links, it's a reusable feature).

### 5.8 Auto-Dismissal of Flash Messages

```javascript
const flashMessages = document.querySelectorAll('.alert');
flashMessages.forEach(msg => {
    setTimeout(() => {
        msg.classList.remove('show');
        setTimeout(() => msg.remove(), 300);
    }, 5000);
});
```

Flash messages are Bootstrap alerts that appear in the `flash-container`. This script automatically hides them after 5 seconds. First, it removes the `show` class (Bootstrap uses this to display alerts), then after a short delay (allowing fade-out transition), it removes the element from the DOM.

### 5.9 Newsletter Form Demo

```javascript
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        if (email) {
            alert('Thanks for subscribing! (Demo)');
            this.reset();
        }
    });
}
```

The newsletter form in the footer is a static demo. JavaScript intercepts the submit, prevents the actual form submission, shows an alert, and resets the field. No data is sent to the server.

### 5.10 Active Navigation Link Highlighting

```javascript
const currentLocation = window.location.pathname;
const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
navLinks.forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
        link.classList.add('active');
    }
});
```

This dynamically adds the `active` class to the navigation link corresponding to the current page. It matches the `href` attribute (which contains the URL path, e.g., `/blogs`) against `window.location.pathname`. This provides visual feedback to the user about their current location.

### 5.11 Integration with Templates

All JavaScript functionality relies on specific HTML elements and classes defined in the templates:

- `id="preloader"` in `base.html`
- `id="themeToggle"` in the navbar
- `id="backToTop"` button
- `id="mainNav"` for the navbar
- `class="alert"` for flash messages
- `class="newsletter-form"` for the footer form
- `class="navbar-nav .nav-link"` for navigation links

The script assumes these elements exist; if they are missing, it gracefully handles `null` checks (e.g., `if (preloader)`). This makes the script robust against template variations.

### 5.12 Performance Considerations

- The scroll event listeners are not debounced; in a high‑traffic site, they could cause performance issues. For this demo, it's acceptable.
- All operations are lightweight and do not block the main thread.
- External libraries (AOS) are loaded via CDN, and their initialization occurs after the DOM is ready.

### 5.13 Client-Server Interaction Summary

The JavaScript enhances the server‑rendered HTML without altering the core data flow. All dynamic content (blogs, search results) is generated on the server and delivered as complete HTML. JavaScript adds:

- Visual effects (animations, theme switching)
- UI conveniences (back to top, smooth scroll, auto‑dismiss)
- Client‑side persistence (theme preference)
- Demo interactions (newsletter)

This pattern keeps the application simple and SEO‑friendly while providing a modern, interactive user experience.

---

**Key Takeaways from Step 5:**
- JavaScript enhances the user experience with animations, theme switching, and UI behaviors.
- Theme switching uses CSS variables and `data-theme` attribute, with `localStorage` for persistence.
- Event listeners for scroll, click, and load trigger various features.
- The script integrates with specific IDs and classes defined in the templates.
- All client‑side code is contained in `main.js` and loaded at the end of `base.html`.
- The design follows progressive enhancement: the site remains functional even if JavaScript is disabled (except theme toggle and animations).