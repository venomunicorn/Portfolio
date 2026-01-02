// data.js is loaded before this file, providing specific variables
// Variable 'projects' is available globally

document.addEventListener('DOMContentLoaded', () => {
    const projectsGrid = document.getElementById('projectsGrid');
    const searchInput = document.getElementById('searchInput');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const emptyState = document.getElementById('emptyState');

    // Stats elements
    const totalEl = document.getElementById('totalProjects');
    const webEl = document.getElementById('webProjects');
    const pythonEl = document.getElementById('pythonProjects');
    const cppEl = document.getElementById('cppProjects');

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
    init();

    function init() {
        renderStats();
        renderProjects();
        setupEventListeners();
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
                // Update UI
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Update State
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
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    function closeDemoModal() {
        modal.classList.add('hidden');
        demoFrame.src = ''; // Stop video/iframe content
        document.body.style.overflow = '';
    }

    function renderStats() {
        totalEl.textContent = projects.length;

        const counts = projects.reduce((acc, p) => {
            acc[p.category_short] = (acc[p.category_short] || 0) + 1;
            return acc;
        }, {});

        webEl.textContent = counts['Web'] || 0;
        pythonEl.textContent = counts['Python'] || 0;
        cppEl.textContent = counts['C++'] || 0;
    }

    function getCategoryClass(categoryShort) {
        switch (categoryShort) {
            case 'Web': return 'cat-web';
            case 'Python': return 'cat-python';
            case 'C++': return 'cat-cpp';
            default: return '';
        }
    }

    function renderProjects() {
        projectsGrid.innerHTML = '';

        const filtered = projects.filter(project => {
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
                    // Find correct project (using index might be risky if filtered, 
                    // but we re-render on filter so indices match 'filtered' array)
                    // Wait, we need the original index or pass project object.
                    // Actually, since we clear grid and re-render filtered list, 
                    // the index in the loop matches the index in the "filtered" array.
                    const index = parseInt(e.currentTarget.dataset.id);
                    openDemoModal(filtered[index]);
                });
            });
        }
    }
});
