# Portfolio Website Documentation

## Overview

This is a single‑page application (SPA) like portfolio website built with vanilla HTML, CSS, and JavaScript. It uses **Tailwind CSS** for utility‑first styling and **Font Awesome** for icons. Content is dynamically loaded from a central JSON file (`data/data.json`), making the site easy to update without touching the HTML structure.

The site features:

- A collapsible sidebar with profile info, navigation, and contact icons.
- Seven content pages: Summary, Projects, Education, Skills, Languages, Certifications, Experience.
- Dark/light mode toggle (persisted in `localStorage`).
- Responsive design (mobile‑friendly with flexbox).
- Background image with overlay on the main content area.

## File Structure

```
.
├── index.html               # Summary page
├── projects.html            # Projects page
├── education.html           # Education page
├── skills.html              # Skills page
├── languages.html           # Languages page
├── certifications.html      # Certifications page
├── experience.html          # Experience page
├── css/
│   └── style.css            # Custom styles (sidebar toggle, background, animations)
├── js/
│   └── main.js              # Core logic: data loading, templating, sidebar, theme
└── data/
    └── data.json            # All content data (not provided in the snippet)
```

## How It Works

### 1. Data Management (`data/data.json`)

All textual content, lists, and URLs are stored in a single JSON file. Example structure:

```json
{
  "name": "Sayantan",
  "title": "Developer & Designer",
  "contact": {
    "email": "sayantan@example.com",
    "linkedin": "linkedin.com/in/sayantan",
    "github": "github.com/sayantan"
  },
  "location": "City, Country",
  "summary": "...",
  "projects": [ ... ],
  "education": { ... },
  "skills": { ... },
  "languages": [ ... ],
  "certifications": [ ... ],
  "experience": [ ... ]
}
```

### 2. Core JavaScript (`js/main.js`)

- **`loadData()`** – Fetches and parses `data/data.json`.
- **`renderTemplate(html, data)`** – Replaces `{{key}}` or `{{nested.key}}` placeholders with corresponding values from the data object.
- **`buildSidebar(data, activePage)`** – Generates the sidebar HTML using data and marks the current page’s navigation link as active.
- **`initPage(activePage)`** – Called on every page:
  1. Loads data.
  2. Injects the rendered sidebar into the `<aside>`.
  3. Replaces any placeholders in the main content (e.g., `{{summary}}`).
  4. Sets up sidebar toggle and theme toggle listeners.
- **`setupSidebarToggle()`** – Handles collapsing/expanding the sidebar and toggling the chevron icon.
- **`setupThemeToggle()`** – Manages dark/light mode based on user preference stored in `localStorage`.

### 3. Page Initialization

Each HTML page includes a `<script>` block that calls `initPage()` with the page identifier. For pages that display lists (projects, certifications, etc.), additional DOM manipulation is performed after `initPage` to populate the container with dynamic content from the JSON.

Example from `projects.html`:

```javascript
document.addEventListener('DOMContentLoaded', async () => {
  await initPage('projects');
  const data = await loadData();
  const container = document.getElementById('projects-container');
  container.innerHTML = data.projects.map(proj => `...`).join('');
});
```

### 4. Styling (`css/style.css`)

- **Sidebar Collapse** – When the `.collapsed` class is added, navigation labels, profile name/title, and contact text are hidden; the avatar shrinks.
- **Background Overlay** – The `<main>` element has a background image with a dark overlay (opacity changes slightly in dark mode). The overlay is created with a `::before` pseudo‑element.
- **Animations** – A simple fade‑in on page load (`.fade-in`).
- **Responsive** – On mobile, the sidebar becomes full width and the layout stacks vertically.

### 5. Dark / Light Mode

A theme toggle button is injected into the sidebar (via `buildSidebar`). Clicking it toggles the `dark` class on the `<html>` element. Tailwind’s dark mode variant (`dark:`) is used throughout the HTML. The current theme is saved to `localStorage` and restored on page load.

## Customization

### Changing Content

1. Open `data/data.json`.
2. Update the relevant fields (strings, arrays, objects).
3. Ensure the structure matches what each page expects (see the HTML files for placeholder names).

### Adding a New Page

1. Create a new HTML file (e.g., `awards.html`).
2. Copy the basic structure from an existing page (like `certifications.html`).
3. Replace the main content area with appropriate markup and placeholders.
4. In the script section, call `initPage('awards')` and then populate any dynamic containers.
5. Add a corresponding entry in the `navLinks` array inside `buildSidebar()` in `main.js`.

### Modifying the Sidebar

The sidebar is built dynamically by `buildSidebar()`. To change its layout or add new sections, edit that function. The profile image is currently hardcoded to a GitHub avatar – replace the `src` with your own image path or URL.

### Changing the Background Image

The background image is set in `css/style.css`:

```css
main {
  background-image: url('https://images.pexels.com/photos/247671/pexels-photo-247671.jpeg');
  ...
}
```

Replace the URL with your own image. Adjust the overlay opacity in the `main::before` rule.

### Styling Adjustments

- Tailwind classes are used extensively – you can override them in `style.css` or by adding custom classes.
- For global style changes, edit `css/style.css`.

## Dependencies

- **Tailwind CSS** – Loaded via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- **Font Awesome 6** – Loaded via CDN: `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">`

No build tools or package managers are required.

## Setup

1. Clone or download the repository.
2. Ensure the file structure is preserved.
3. Create/edit `data/data.json` with your own content.
4. Open any `.html` file in a modern web browser.

All pages share the same sidebar and theme logic, so navigating between them feels seamless.

## Browser Support

Works in all modern browsers (Chrome, Firefox, Safari, Edge). Internet Explorer is not supported.

---

