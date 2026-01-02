
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('app-container');
    const data = await fetchData('skills.json');

    if (!data) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load skills data.</div>';
        return;
    }

    let activeTab = 'guitar';
    let completedDays = new Set();

    // Load progress
    const savedProgress = localStorage.getItem('guitarProgress');
    if (savedProgress) {
        try {
            completedDays = new Set(JSON.parse(savedProgress));
        } catch (e) {
            console.error("Failed to parse progress", e);
        }
    }

    function toggleDay(day) {
        if (completedDays.has(day)) {
            completedDays.delete(day);
        } else {
            completedDays.add(day);
        }
        localStorage.setItem('guitarProgress', JSON.stringify(Array.from(completedDays)));
        render();
    }

    function render() {
        // Icons
        const Guitar = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>'; // Placeholder
        const Crosshair = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" x2="18" y1="12" y2="12"/><line x1="6" x2="2" y1="12" y2="12"/><line x1="12" x2="12" y1="6" y2="2"/><line x1="12" x2="12" y1="22" y2="18"/></svg>';
        const Check = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        const Play = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>';
        const Terminal = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>';
        const Code = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>';

        // Update tabs UI
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active-guitar', 'active-valorant');
            if (btn.dataset.tab === activeTab) {
                btn.classList.add(`active-${activeTab}`);
            }
        });

        if (activeTab === 'guitar') {
            container.innerHTML = `
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h2 style="font-size: 1.875rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">${data.guitar.title}</h2>
                    <p style="color: var(--text-muted);">${data.guitar.description}</p>
                </div>

                <div style="display: grid; gap: 2rem;">
                    ${data.guitar.phases.map(phase => `
                        <div>
                            <h3 class="phase-title">${phase.title}</h3>
                            <div class="days-grid">
                                ${phase.days.map(day => {
                const isCompleted = completedDays.has(day.day);
                return `
                                        <div class="day-card ${isCompleted ? 'completed' : ''}" data-day="${day.day}">
                                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                                                <span class="day-badge">Day ${day.day}</span>
                                                ${isCompleted ? `<div style="color: #fbbf24;">${Check}</div>` : ''}
                                            </div>
                                            <h4 style="font-size: 1.125rem; font-weight: 700; color: white; margin-bottom: 0.25rem;">${day.title}</h4>
                                            <p style="font-size: 0.875rem; color: #fde68a; opacity: 0.8; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                                                ${Play} ${day.piece}
                                            </p>
                                            <div style="font-size: 0.875rem;">
                                                <strong style="color: #cbd5e1; display: block; margin-bottom: 0.25rem;">Goals:</strong>
                                                <ul style="list-style-type: disc; padding-left: 1.25rem; color: var(--text-muted);">
                                                    ${day.goals.map(g => `<li>${g}</li>`).join('')}
                                                </ul>
                                            </div>
                                        </div>
                                    `;
            }).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            // Add click listeners for days
            container.querySelectorAll('.day-card').forEach(card => {
                card.addEventListener('click', () => {
                    toggleDay(parseInt(card.dataset.day));
                });
            });

        } else {
            container.innerHTML = `
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h2 style="font-size: 1.875rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">${data.valorant.title}</h2>
                    <p style="color: var(--text-muted);">${data.valorant.description}</p>
                </div>

                <div class="valorant-grid">
                    <div>
                        ${data.valorant.specs.map(spec => `
                            <div class="spec-card">
                                <h3 style="font-size: 1.125rem; font-weight: 600; color: #f87171; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                                    ${Terminal} ${spec.category}
                                </h3>
                                ${spec.items ? `
                                    <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem;">
                                        ${spec.items.map(item => `
                                            <li style="color: #cbd5e1; display: flex; align-items: flex-start; gap: 0.5rem;">
                                                <span style="margin-top: 0.375rem; width: 0.375rem; height: 0.375rem; border-radius: 50%; background-color: rgba(239, 68, 68, 0.5);"></span>
                                                ${item}
                                            </li>
                                        `).join('')}
                                    </ul>
                                ` : ''}
                                ${spec.steps ? `
                                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                                        ${spec.steps.map((step, i) => `
                                            <div style="display: flex; align-items: center; gap: 0.75rem; color: #cbd5e1; background-color: rgba(0,0,0,0.2); padding: 0.5rem; border-radius: 0.25rem;">
                                                <span style="font-family: monospace; color: rgba(239, 68, 68, 0.5);">${i + 1}</span>
                                                ${step}
                                            </div>
                                        `).join('')}
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>

                    <div class="code-block">
                        <div class="code-header">
                            ${Code}
                            <span>trainer.py</span>
                        </div>
                        <div class="code-content">
                            <pre>${data.valorant.code_snippet}</pre>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            activeTab = btn.dataset.tab;
            render();
        });
    });

    render();
});
