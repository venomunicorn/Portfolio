
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('roadmap-container');
    const rawData = await fetchData('youtube_roadmap.json');

    if (!rawData) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load roadmap data.</div>';
        return;
    }

    // Load progress
    let completedTasks = new Set();
    const savedProgress = localStorage.getItem('creatorProgress');
    if (savedProgress) {
        try {
            completedTasks = new Set(JSON.parse(savedProgress));
        } catch (e) {
            console.error("Failed to parse progress", e);
        }
    }

    // Transform Data
    const phases = rawData.map((phase, pIndex) => ({
        id: `phase-${pIndex}`,
        title: phase.phase,
        days: phase.days,
        goals: phase.goals,
        weeks: phase.weeks.map((week, wIndex) => ({
            id: `week-${pIndex}-${wIndex}`,
            title: week.title,
            weekLabel: week.week,
            tasks: week.tasks.map((task, tIndex) => ({
                id: `task-${pIndex}-${wIndex}-${tIndex}`,
                text: task
            }))
        }))
    }));

    function toggleTask(taskId) {
        if (completedTasks.has(taskId)) {
            completedTasks.delete(taskId);
        } else {
            completedTasks.add(taskId);
        }
        localStorage.setItem('creatorProgress', JSON.stringify(Array.from(completedTasks)));
        render();
    }

    function render() {
        // Icons
        const Trophy = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>';
        const Calendar = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: rgba(255,255,255,0.2);"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>';
        const Square = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/></svg>';
        const CheckSquare = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 12 2 2 4-4"/></svg>';

        const html = phases.map(phase => `
            <div class="phase-card">
                <div class="phase-header">
                    <div>
                        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                            <span class="phase-badge">${phase.days} Days</span>
                            <h2 class="phase-title" style="margin: 0; font-size: 1.5rem;">${phase.title}</h2>
                        </div>
                        <p class="phase-goals">
                            ${Trophy}
                            Goals: ${phase.goals}
                        </p>
                    </div>
                    ${Calendar}
                </div>

                <div class="phase-content">
                    ${phase.weeks.map(week => `
                        <div class="week-container">
                            <h3 class="week-header">
                                <span class="week-label">${week.weekLabel}:</span> ${week.title}
                            </h3>
                            <div class="tasks-list">
                                ${week.tasks.map(task => {
            const isCompleted = completedTasks.has(task.id);
            return `
                                        <div class="task-item ${isCompleted ? 'completed' : ''}" data-task="${task.id}">
                                            <div class="task-checkbox">
                                                ${isCompleted ? CheckSquare : Square}
                                            </div>
                                            <span class="task-text">${task.text}</span>
                                        </div>
                                    `;
        }).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');

        container.innerHTML = html;

        // Event Listeners
        container.querySelectorAll('.task-item').forEach(item => {
            item.addEventListener('click', () => {
                toggleTask(item.dataset.task);
            });
        });
    }

    render();
});
