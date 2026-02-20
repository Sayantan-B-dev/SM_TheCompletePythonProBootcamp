// js/main.js
async function loadData() {
  const response = await fetch('data/data.json');
  return await response.json();
}

function renderTemplate(html, data) {
  return html.replace(/\{\{(\w+\.?\w*)\}\}/g, (match, key) => {
    const keys = key.split('.');
    let value = data;
    for (const k of keys) {
      value = value?.[k];
      if (value === undefined) break;
    }
    return value !== undefined ? value : match;
  });
}

function buildSidebar(data, activePage) {
  const contactIcons = `
    <div class="contact-icons flex justify-center gap-4 text-xl my-4">
      <a href="mailto:{{contact.email}}" title="{{contact.email}}"><i class="fas fa-envelope"></i></a>
      <a href="https://{{contact.linkedin}}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
      <a href="https://{{contact.github}}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
      <span title="{{location}}"><i class="fas fa-map-marker-alt"></i></span>
    </div>
  `;

  const navLinks = [
    { href: 'index.html', icon: 'fa-home', label: 'Summary', page: 'summary' },
    { href: 'projects.html', icon: 'fa-code', label: 'Projects', page: 'projects' },
    { href: 'education.html', icon: 'fa-graduation-cap', label: 'Education', page: 'education' },
    { href: 'skills.html', icon: 'fa-cogs', label: 'Skills', page: 'skills' },
    { href: 'languages.html', icon: 'fa-language', label: 'Languages', page: 'languages' },
    { href: 'certifications.html', icon: 'fa-certificate', label: 'Certifications', page: 'certifications' },
    { href: 'experience.html', icon: 'fa-briefcase', label: 'Experience', page: 'experience' }
  ];

  const navHtml = navLinks.map(link => `
    <a href="${link.href}" class="nav-link ${activePage === link.page ? 'active' : ''}">
      <i class="fas ${link.icon} w-6"></i>
      <span class="nav-label">${link.label}</span>
    </a>
  `).join('');

  return `
    <div class="sidebar-header flex flex-col items-center text-center">
        <img 
            src="https://avatars.githubusercontent.com/u/181269757?v=4"
            alt="abstract profile avatar"
            class="w-24 h-24 rounded-full object-cover border-2 border-gray-200 dark:border-gray-700"
        >
        <h2 class="text-2xl font-medium mt-4">
            {{name}}
        </h2>
        <p class="text-gray-600 dark:text-gray-400 text-sm break-words">
            {{title}}
        </p>
    </div>


    ${contactIcons}
    <nav class="mt-6 flex flex-col space-y-2">
      ${navHtml}
    </nav>
    <div class="mt-auto pt-6 flex justify-between items-center">
      <button id="toggle-sidebar" class="text-gray-500 hover:text-black dark:hover:text-white">
        <i class="fas fa-chevron-left"></i>
      </button>
    </div>
  `;
}

async function initPage(activePage) {
  const data = await loadData();
  const sidebarHtml = buildSidebar(data, activePage);
  document.getElementById('sidebar').innerHTML = renderTemplate(sidebarHtml, data);

  // Replace placeholders in main content if any
  const mainEl = document.querySelector('main');
  if (mainEl) {
    mainEl.innerHTML = renderTemplate(mainEl.innerHTML, data);
  }

  setupSidebarToggle();
  setupThemeToggle();
}

function setupSidebarToggle() {
  const btn = document.getElementById('toggle-sidebar');
  if (!btn) return;
  const sidebar = document.getElementById('sidebar');
  const main = document.querySelector('main');
  btn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    main?.classList.toggle('expanded');
    const icon = btn.querySelector('i');
    if (icon) {
      icon.classList.toggle('fa-chevron-left');
      icon.classList.toggle('fa-chevron-right');
    }
  });
}

function setupThemeToggle() {
  const html = document.documentElement;
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.classList.toggle('dark', savedTheme === 'dark');

  btn.addEventListener('click', () => {
    html.classList.toggle('dark');
    localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
  });
}