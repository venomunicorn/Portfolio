
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('app-container');
    const data = await fetchData('health_protocols.json');

    if (!data) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load health protocols.</div>';
        return;
    }

    const categories = Object.keys(data);
    let activeCategory = categories[0];
    let completedItems = new Set();

    // Load progress
    const savedProgress = localStorage.getItem('healthProgress');
    if (savedProgress) {
        try {
            completedItems = new Set(JSON.parse(savedProgress));
        } catch (e) {
            console.error("Failed to parse progress", e);
        }
    }

    function toggleItem(category, sectionIdx, itemIdx) {
        const id = `${category}-${sectionIdx}-${itemIdx}`;
        if (completedItems.has(id)) {
            completedItems.delete(id);
        } else {
            completedItems.add(id);
        }
        localStorage.setItem('healthProgress', JSON.stringify(Array.from(completedItems)));
        render();
    }

    function render() {
        const currentData = data[activeCategory];

        // Calculate progress
        let totalCheckboxes = 0;
        let checkedCount = 0;

        currentData.sections.forEach((section, sIdx) => {
            section.items.forEach((item, iIdx) => {
                if (item.type === 'checkbox') {
                    totalCheckboxes++;
                    if (completedItems.has(`${activeCategory}-${sIdx}-${iIdx}`)) {
                        checkedCount++;
                    }
                }
            });
        });

        const progress = totalCheckboxes > 0 ? Math.round((checkedCount / totalCheckboxes) * 100) : 0;

        // Icons
        const Activity = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>';
        const Sun = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>';
        const User = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
        const Utensils = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>';
        const Check = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        const ChevronRight = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>';
        const Info = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>';

        function getIcon(cat) {
            switch (cat) {
                case 'height': return Activity;
                case 'skin': return Sun;
                case 'aesthetics': return User;
                case 'nutrition': return Utensils;
                default: return Activity;
            }
        }

        let html = `
            <div class="category-nav">
                ${categories.map(cat => `
                    <button class="nav-btn ${activeCategory === cat ? 'active' : ''}" data-cat="${cat}">
                        ${getIcon(cat)}
                        <span style="text-transform: capitalize;">${cat}</span>
                    </button>
                `).join('')}
            </div>

            <div class="health-grid">
                <div class="left-col">
                    <div class="info-card">
                        <h2 style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">${currentData.title}</h2>
                        <p style="color: var(--text-muted); line-height: 1.6; margin-bottom: 1.5rem;">${currentData.description}</p>

                        <div class="progress-container">
                            <div style="display: flex; justify-content: space-between; font-size: 0.875rem;">
                                <span style="color: var(--text-muted);">Daily Completion</span>
                                <span style="color: var(--color-green); font-weight: 500;">${progress}%</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: ${progress}%"></div>
                            </div>
                        </div>
                    </div>

                    <div class="info-card" style="background-color: rgba(59, 130, 246, 0.1); border-color: rgba(59, 130, 246, 0.2);">
                        <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                            <div style="color: #60a5fa; margin-top: 0.25rem;">${Info}</div>
                            <div>
                                <h3 style="color: #bfdbfe; font-weight: 500; margin-bottom: 0.25rem;">Pro Tip</h3>
                                <p style="font-size: 0.875rem; color: #dbeafe; opacity: 0.8; line-height: 1.6;">
                                    Consistency is key. Try to complete your daily checklist at the same time each day to build a habit.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="right-col">
                    ${currentData.sections.map((section, sIdx) => `
                        <div class="protocol-section">
                            <div class="section-header">
                                <h3 class="section-title">${section.title}</h3>
                            </div>
                            <div class="section-content">
                                ${section.items.map((item, iIdx) => {
            const id = `${activeCategory}-${sIdx}-${iIdx}`;
            const isChecked = completedItems.has(id);

            if (item.type === 'info') {
                return `
                                            <div class="protocol-item info-item">
                                                <div style="color: var(--text-muted);">${ChevronRight}</div>
                                                <span class="item-text">${item.text}</span>
                                            </div>
                                        `;
            }

            return `
                                        <div class="protocol-item checkbox ${isChecked ? 'checked' : ''}" data-sidx="${sIdx}" data-iidx="${iIdx}">
                                            <div class="checkbox-box">
                                                ${isChecked ? Check : ''}
                                            </div>
                                            <span class="item-text">${item.text}</span>
                                        </div>
                                    `;
        }).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;

        // Event Listeners
        container.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                activeCategory = btn.dataset.cat;
                render();
            });
        });

        container.querySelectorAll('.protocol-item.checkbox').forEach(item => {
            item.addEventListener('click', () => {
                toggleItem(activeCategory, parseInt(item.dataset.sidx), parseInt(item.dataset.iidx));
            });
        });
    }

    render();
});
