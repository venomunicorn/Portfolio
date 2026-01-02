
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('clones-grid');
    const searchInput = document.getElementById('search-input');

    const data = await fetchData('app_clones.json');

    if (!data) {
        container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--color-red);">Failed to load clones data.</div>';
        return;
    }

    let searchTerm = '';
    let expandedCategory = null;

    function render() {
        const filtered = data.filter(cat =>
            cat.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
            cat.apps.some(app => app.toLowerCase().includes(searchTerm.toLowerCase()))
        );

        // Icons
        const Layers = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>';
        const ArrowRight = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>';
        const Smartphone = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg>';

        if (filtered.length === 0) {
            container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 2rem;">No categories found.</div>';
            return;
        }

        container.innerHTML = filtered.map(category => {
            const isExpanded = expandedCategory === category.category;

            return `
                <div class="clone-card">
                    <div class="card-header">
                        <div class="category-icon">
                            ${Layers}
                        </div>
                        <h2 class="category-title" title="${category.category}">${category.category}</h2>
                    </div>

                    <div class="tags-container">
                        ${category.apps.slice(0, 6).map(app => `
                            <span class="app-tag">${app}</span>
                        `).join('')}
                        ${category.apps.length > 6 ? `
                            <span class="app-tag more">+${category.apps.length - 6} more</span>
                        ` : ''}
                    </div>

                    <button class="view-btn" data-category="${category.category}">
                        ${isExpanded ? 'Hide List' : 'View All Apps'}
                        <span style="transform: ${isExpanded ? 'rotate(-90deg)' : 'rotate(0)'}; transition: transform 0.2s;">${ArrowRight}</span>
                    </button>

                    <div class="expanded-list ${isExpanded ? 'show' : ''}">
                        <ul style="list-style: none;">
                            ${category.apps.map(app => `
                                <li class="list-item">
                                    ${Smartphone}
                                    ${app}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }).join('');

        // Event Listeners
        container.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const cat = btn.dataset.category;
                expandedCategory = expandedCategory === cat ? null : cat;
                render();
            });
        });
    }

    searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value;
        render();
    });

    render();
});
