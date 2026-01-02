
document.addEventListener('DOMContentLoaded', async () => {
    const listContainer = document.getElementById('ideas-list');
    const detailContainer = document.getElementById('idea-detail-container');

    const data = await fetchData('startup_ideas.json');

    if (!data) {
        listContainer.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load ideas data.</div>';
        return;
    }

    let selectedIdeaId = null;

    function renderList() {
        listContainer.innerHTML = data.map(idea => `
            <div class="idea-item ${selectedIdeaId === idea.id ? 'active' : ''}" data-id="${idea.id}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 9999px; background-color: rgba(255,255,255,0.1); color: var(--text-muted);">#${idea.id}</span>
                    ${idea.score > 0 ? `
                        <span style="font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 9999px; background-color: ${idea.score >= 80 ? 'rgba(16, 185, 129, 0.2); color: var(--color-emerald);' : 'rgba(251, 191, 36, 0.2); color: var(--color-amber);'}">
                            Score: ${idea.score}
                        </span>
                    ` : ''}
                </div>
                <h3 style="font-weight: 700; font-size: 1.125rem; color: white; margin-bottom: 0.25rem;">${idea.name}</h3>
                <p style="font-size: 0.875rem; color: var(--text-muted); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${idea.description}</p>
            </div>
        `).join('');

        // Add click listeners
        listContainer.querySelectorAll('.idea-item').forEach(item => {
            item.addEventListener('click', () => {
                selectedIdeaId = item.dataset.id;
                renderList(); // Re-render list to update active state
                renderDetail();
            });
        });
    }

    function renderDetail() {
        if (!selectedIdeaId) return;

        const idea = data.find(i => i.id === selectedIdeaId);
        if (!idea) return;

        // Icons
        const Lightbulb = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-1 1.5-2 1.5-3.5 0-2.2-1.8-4-4-4s-4 1.8-4 4c0 1.5.5 2.5 1.5 3.5.8.8 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>';
        const Target = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>';
        const TrendingUp = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>';
        const DollarSign = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
        const CheckCircle = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
        const ArrowRight = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>';

        detailContainer.innerHTML = `
            <div class="idea-detail">
                <div class="detail-header">
                    <div class="detail-icon">
                        ${Lightbulb}
                    </div>
                    <div>
                        <h2 style="font-size: 1.875rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">${idea.name}</h2>
                        <p style="font-size: 1.125rem; color: var(--text-muted);">${idea.description}</p>
                    </div>
                </div>

                <div class="info-grid">
                    ${idea.problem ? `
                        <div class="info-card card-problem">
                            <h3>${Target} Problem</h3>
                            <p>${idea.problem}</p>
                        </div>
                    ` : ''}
                    ${idea.market ? `
                        <div class="info-card card-market">
                            <h3>${TrendingUp} Market Opportunity</h3>
                            <p>${idea.market}</p>
                        </div>
                    ` : ''}
                    ${idea.revenue ? `
                        <div class="info-card card-revenue">
                            <h3>${DollarSign} Revenue Model</h3>
                            <p>${idea.revenue}</p>
                        </div>
                    ` : ''}
                    ${idea.cost ? `
                        <div class="info-card card-cost">
                            <h3>${CheckCircle} Est. Cost & Time</h3>
                            <p>${idea.cost}</p>
                        </div>
                    ` : ''}
                </div>

                ${idea.tasks && idea.tasks.length > 0 ? `
                    <div>
                        <h3 style="font-size: 1.25rem; font-weight: 700; color: white; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span style="color: var(--color-emerald);">${ArrowRight}</span>
                            Execution Roadmap
                        </h3>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            ${idea.tasks.map(task => `
                                <div class="roadmap-item">
                                    <div class="roadmap-dot"></div>
                                    <span style="color: #cbd5e1; font-size: 0.875rem;">${task}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    renderList();
});
