// data.js is loaded before this file, providing specific variables
// Variable 'projects' is available globally

// ============================================
// THEME SYSTEM
// ============================================

const THEMES = ['brutalist', 'luxury', 'scientific', 'chaos'];

function initTheme() {
    // Check for saved theme or randomize
    let savedTheme = localStorage.getItem('portfolioTheme');

    if (!savedTheme || !THEMES.includes(savedTheme)) {
        // Random theme on first visit
        savedTheme = THEMES[Math.floor(Math.random() * THEMES.length)];
        localStorage.setItem('portfolioTheme', savedTheme);
    }

    setTheme(savedTheme);
    setupThemeButtons();
}

function setTheme(themeName) {
    document.body.setAttribute('data-theme', themeName);
    localStorage.setItem('portfolioTheme', themeName);

    // Update active button
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === themeName);
    });

    // Switch 3D effect for this theme
    if (typeof switchThemeEffect === 'function') {
        switchThemeEffect(themeName);
    }

    // Recreate particles for theme-specific styling (legacy, now handled by effects.js)
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        particlesContainer.innerHTML = '';
    }
}

function setupThemeButtons() {
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.theme;
            setTheme(theme);
        });
    });
}

// ============================================
// MAIN APP
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme FIRST
    initTheme();

    // Check availability of projects data with polling
    let retries = 0;

    function checkDataAndInit() {
        if (typeof window.projects !== 'undefined' && Array.isArray(window.projects)) {
            // Data loaded!
            init();
        } else {
            console.log("Waiting for portfolio_data.js...");
            retries++;
            if (retries < 20) {
                // First 2 seconds: silent wait
                setTimeout(checkDataAndInit, 100);
            } else if (retries < 100) {
                // Next 8 seconds: keep waiting
                setTimeout(checkDataAndInit, 100);
            } else {
                // Timeout after 10 seconds: Show visible error
                const err = document.getElementById('emptyState');
                if (err) {
                    err.classList.remove('hidden');
                    err.innerHTML = "<h3>Connection Slow</h3><p>Projects data could not be loaded. <br> <button onclick='location.reload()'>Reload Page</button></p>";
                }
            }
        }
    }

    checkDataAndInit();

    const projectsGrid = document.getElementById('projectsGrid');
    const searchInput = document.getElementById('searchInput');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const emptyState = document.getElementById('emptyState');

    // Stats elements
    const totalEl = document.getElementById('totalProjects');
    const webEl = document.getElementById('webProjects');
    const pythonEl = document.getElementById('pythonProjects');
    const cppEl = document.getElementById('cppProjects');
    const aimlEl = document.getElementById('aimlProjects');
    const gamesEl = document.getElementById('gamesProjects');
    const appsEl = document.getElementById('appsProjects');

    // Modal elements
    const modal = document.getElementById('demoModal');
    const closeModalBtn = document.getElementById('closeModal');
    const demoFrame = document.getElementById('demoFrame');
    const modalTitle = document.getElementById('modalTitle');
    const modalExternalLink = document.getElementById('modalExternalLink');

    // State
    let currentCategory = 'all';
    let searchQuery = '';

    // Initialize
    // init() is now called by checkDataAndInit
    // init();

    function init() {
        createParticles();
        renderStats();
        renderProjects();
        setupEventListeners();
        animateCounters();
    }

    function setupEventListeners() {
        // Search
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase();
            renderProjects();
        });

        // Filter Buttons
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentCategory = btn.dataset.category;
                renderProjects();
            });
        });

        // Modal interactions
        closeModalBtn.addEventListener('click', closeDemoModal);
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeDemoModal();
            }
        });
    }

    function openDemoModal(project) {
        if (!project.demo_url) return;

        modalTitle.textContent = project.name;
        demoFrame.src = project.demo_url;
        modalExternalLink.href = project.demo_url;

        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeDemoModal() {
        modal.classList.add('hidden');
        demoFrame.src = '';
        document.body.style.overflow = '';
    }

    function renderStats() {
        // Safety check
        const data = window.projects || [];
        totalEl.textContent = data.length;

        const counts = data.reduce((acc, p) => {
            acc[p.category_short] = (acc[p.category_short] || 0) + 1;
            return acc;
        }, {});

        if (webEl) webEl.textContent = counts['Web'] || 0;
        if (pythonEl) pythonEl.textContent = counts['Python'] || 0;
        if (cppEl) cppEl.textContent = counts['C++'] || 0;
        if (aimlEl) aimlEl.textContent = counts['AI/ML'] || 0;
        if (gamesEl) gamesEl.textContent = counts['Games'] || 0;
        // Apps includes both 'Apps' and 'Mobile' categories
        if (appsEl) appsEl.textContent = (counts['Apps'] || 0) + (counts['Mobile'] || 0);
    }

    function getCategoryClass(categoryShort) {
        switch (categoryShort) {
            case 'Web': return 'cat-web';
            case 'Python': return 'cat-python';
            case 'C++': return 'cat-cpp';
            case 'AI/ML': return 'cat-aiml';
            case 'Games': return 'cat-games';
            case 'Mobile': return 'cat-mobile';
            case 'Apps': return 'cat-apps';
            case 'GitHub': return 'cat-github';
            default: return 'cat-other';
        }
    }

    function renderProjects() {
        projectsGrid.innerHTML = '';

        const data = window.projects || [];
        const filtered = data.filter(project => {
            const matchesCategory = currentCategory === 'all' || project.category === currentCategory;
            const matchesSearch = project.name.toLowerCase().includes(searchQuery) ||
                project.description.toLowerCase().includes(searchQuery);
            return matchesCategory && matchesSearch;
        });

        if (filtered.length === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');

            filtered.forEach((project, index) => {
                const card = document.createElement('div');
                card.className = 'project-card';
                card.style.animationDelay = `${Math.min(index * 0.05, 1)}s`;

                const categoryClass = getCategoryClass(project.category_short);

                // Features list
                let featuresHtml = '';
                if (project.features && project.features.length > 0) {
                    featuresHtml = `<ul class="project-features">
                        ${project.features.slice(0, 3).map(f => `<li>${f}</li>`).join('')}
                    </ul>`;
                }

                // Demo Button
                let demoBtnHtml = '';
                if (project.demo_url) {
                    demoBtnHtml = `<button class="demo-btn" data-id="${index}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        Live Demo
                    </button>`;
                }

                // GUI Demo badge for Python apps
                let guiBadgeHtml = '';
                if (project.has_gui && project.run_command) {
                    guiBadgeHtml = `<span class="gui-badge">🖥️ GUI App</span>`;
                }

                // Run command for Python GUI demos
                let runCommandHtml = '';
                if (project.run_command) {
                    runCommandHtml = `<div class="run-command">
                        <span class="run-label">Run:</span>
                        <code>${project.run_command}</code>
                    </div>`;
                }

                card.innerHTML = `
                    <span class="project-category ${categoryClass}">${project.category_short}</span>
                    ${guiBadgeHtml}
                    <h3 class="project-title">${project.name}</h3>
                    <p class="project-desc">${project.description}</p>
                    ${featuresHtml}
                    ${runCommandHtml}
                    <div class="card-actions">
                        ${demoBtnHtml}
                        <a href="${project.path}" class="project-link" target="_blank">
                            View Code
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                    </div>
                `;

                projectsGrid.appendChild(card);
            });

            // Attach event listeners to new dynamic buttons
            document.querySelectorAll('.demo-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const index = parseInt(e.currentTarget.dataset.id);
                    openDemoModal(filtered[index]);
                });
            });
        }
    }
});

// ============================================
// PARTICLES (Global function for theme changes)
// ============================================

function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;

    const particleCount = 25;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (15 + Math.random() * 20) + 's';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.width = (2 + Math.random() * 4) + 'px';
        particle.style.height = particle.style.width;
        particlesContainer.appendChild(particle);
    }
}

// ============================================
// ANIMATED COUNTERS
// ============================================

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (isNaN(target) || target === 0) return;

        let current = 0;
        const increment = target / 40;
        const stepTime = 30;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.ceil(current);
                setTimeout(updateCounter, stepTime);
            } else {
                counter.textContent = target;
            }
        };

        // Simply run animation immediately without IntersectionObserver
        // to avoid mobile specific issues where observer might reset to 0 and fail
        counter.textContent = '0';
        updateCounter();
    });
}
