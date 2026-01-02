
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('app-container');
    const data = await fetchData('film.json');

    if (!data) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load film data.</div>';
        return;
    }

    // State
    const state = {
        data: data,
        activeSection: 0,
        expandedSequences: new Set(),
        searchQuery: '',
        completedItems: {}
    };

    // Load progress
    const savedProgress = localStorage.getItem('film_production_progress');
    if (savedProgress) {
        try {
            state.completedItems = JSON.parse(savedProgress);
        } catch (e) {
            console.error("Failed to parse progress", e);
        }
    }

    function toggleItem(id) {
        state.completedItems[id] = !state.completedItems[id];
        localStorage.setItem('film_production_progress', JSON.stringify(state.completedItems));
        render();
    }

    function toggleSequence(id) {
        if (state.expandedSequences.has(id)) {
            state.expandedSequences.delete(id);
        } else {
            state.expandedSequences.add(id);
        }
        render();
    }

    function calculateProgress() {
        const currentSection = state.data.sections[state.activeSection];
        let total = 0;
        let completed = 0;

        currentSection.phases.forEach(phase => {
            phase.episodes.forEach(ep => {
                total++;
                if (state.completedItems[`ep-${ep.title}`]) completed++;
            });
        });

        currentSection.sequences.forEach(seq => {
            seq.shots.forEach(shot => {
                total++;
                if (state.completedItems[`shot-${shot.id}`]) completed++;
            });
        });

        return total === 0 ? 0 : (completed / total) * 100;
    }

    function renderSpecialBlock(block) {
        let type = 'default';
        let icon = ''; // We can add SVG icons here if needed
        const titleLower = block.title.toLowerCase();

        if (titleLower.includes("grading")) type = 'grading';
        else if (titleLower.includes("edit")) type = 'edit';
        else if (titleLower.includes("camera") || titleLower.includes("technical")) type = 'camera';
        else if (titleLower.includes("audio") || titleLower.includes("sound")) type = 'audio';
        else if (titleLower.includes("sequence notes")) type = 'notes';

        return `
            <div class="special-block block-${type}">
                <div class="special-block-title">
                    ${block.title}
                </div>
                <div style="font-size: 0.875rem; opacity: 0.9;">
                    ${block.items.map(item => {
            const parts = item.split(':');
            if (parts.length > 1 && parts[0].length < 30) {
                return `<div style="display: flex; gap: 0.5rem; margin-bottom: 0.25rem;">
                                <span style="font-weight: 500; opacity: 0.8; min-width: 100px;">${parts[0]}:</span>
                                <span>${parts.slice(1).join(':').trim()}</span>
                            </div>`;
            }
            return `<div style="margin-bottom: 0.25rem;">${item}</div>`;
        }).join('')}
                </div>
            </div>
        `;
    }

    function render() {
        const currentSection = state.data.sections[state.activeSection];
        const progress = calculateProgress();

        // Icons
        const CheckCircle = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
        const Circle = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>';
        const ChevronDown = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
        const SearchIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>';
        const FilmIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/></svg>';

        let html = `
            <div class="film-header">
                <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem;">
                    <div>
                        <h1 class="film-title">${state.data.title}</h1>
                        <p style="color: var(--text-muted);">Production Bible & Shot Lists</p>
                    </div>
                    <div class="section-selector">
                        ${state.data.sections.map((section, idx) => `
                            <button class="btn-section ${state.activeSection === idx ? 'active' : ''}" data-idx="${idx}">
                                ${section.title.split(' ')[0]}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <div style="background-color: rgba(255,255,255,0.05); border-radius: 9999px; height: 0.5rem; overflow: hidden;">
                    <div style="height: 100%; background: linear-gradient(to right, #6366f1, #a855f7); width: ${progress}%; transition: width 0.5s;"></div>
                </div>
            </div>

            <div style="position: relative; margin-bottom: 2rem;">
                <div style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-muted);">${SearchIcon}</div>
                <input type="text" id="search-input" placeholder="Search shots, episodes, or details..." value="${state.searchQuery}" 
                    style="width: 100%; background-color: rgba(0,0,0,0.4); border: 1px solid var(--border-color); border-radius: 0.75rem; padding: 0.75rem 1rem 0.75rem 3rem; color: white; outline: none;">
            </div>

            <div class="content-area">
                ${currentSection.phases.length > 0 ? `
                    <div class="phases-grid">
                        ${currentSection.phases.map(phase => `
                            <div class="phase-card">
                                <h3 class="phase-title">
                                    <span style="color: var(--color-indigo);">${FilmIcon}</span>
                                    ${phase.title}
                                </h3>
                                <div>
                                    ${phase.episodes.map(ep => `
                                        <div class="episode-item" data-id="ep-${ep.title}">
                                            <div style="color: ${state.completedItems[`ep-${ep.title}`] ? 'var(--color-green)' : 'var(--text-muted)'}">
                                                ${state.completedItems[`ep-${ep.title}`] ? CheckCircle : Circle}
                                            </div>
                                            <span style="${state.completedItems[`ep-${ep.title}`] ? 'text-decoration: line-through; color: var(--text-muted);' : 'color: #cbd5e1;'}">
                                                ${ep.title}
                                            </span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}

                <div class="sequences-list">
                    ${currentSection.sequences.map(seq => {
            const isExpanded = state.expandedSequences.has(seq.id) || state.searchQuery.length > 0;
            const hasMatches = state.searchQuery === '' ||
                seq.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
                seq.shots.some(s => s.title.toLowerCase().includes(state.searchQuery.toLowerCase()));

            if (!hasMatches) return '';

            return `
                            <div class="sequence-card ${isExpanded ? 'expanded' : ''}">
                                <div class="sequence-header" data-seq="${seq.id}">
                                    <div style="display: flex; align-items: center; gap: 1rem;">
                                        <div class="sequence-id">${seq.id}</div>
                                        <div>
                                            <h3 style="font-weight: 500; color: white;">${seq.title}</h3>
                                            <p style="font-size: 0.75rem; color: var(--text-muted);">${seq.shots.length} shots</p>
                                        </div>
                                    </div>
                                    <div style="transform: ${isExpanded ? 'rotate(180deg)' : 'rotate(0)'}; transition: transform 0.2s; color: var(--text-muted);">
                                        ${ChevronDown}
                                    </div>
                                </div>
                                <div class="sequence-content">
                                    ${seq.notes && seq.notes.length > 0 ? `
                                        <div class="special-block block-notes" style="margin-top: 1rem;">
                                            <h4 class="special-block-title">Sequence Notes</h4>
                                            <ul style="list-style-type: disc; padding-left: 1.5rem; font-size: 0.875rem; opacity: 0.9;">
                                                ${seq.notes.map(note => `<li>${note}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}

                                    ${seq.special_blocks ? seq.special_blocks.map(block => renderSpecialBlock(block)).join('') : ''}

                                    <div style="margin-top: 1rem;">
                                        ${seq.shots.map(shot => `
                                            <div class="shot-item">
                                                <div style="display: flex; align-items: start; gap: 0.75rem;">
                                                    <div class="shot-toggle" data-id="shot-${shot.id}" style="cursor: pointer; color: ${state.completedItems[`shot-${shot.id}`] ? 'var(--color-green)' : 'var(--text-muted)'}">
                                                        ${state.completedItems[`shot-${shot.id}`] ? CheckCircle : Circle}
                                                    </div>
                                                    <div style="flex: 1;">
                                                        <h4 style="font-weight: 500; color: ${state.completedItems[`shot-${shot.id}`] ? 'var(--text-muted); text-decoration: line-through;' : 'white;'}">
                                                            ${shot.id}: ${shot.title}
                                                        </h4>
                                                        ${shot.details ? `
                                                            <div class="shot-details">
                                                                ${Object.entries(shot.details).map(([key, value]) => `
                                                                    <div style="display: flex; gap: 0.5rem;">
                                                                        <span style="font-weight: 500; color: var(--text-muted); min-width: 80px;">${key}:</span>
                                                                        <span style="color: #cbd5e1;">${value}</span>
                                                                    </div>
                                                                `).join('')}
                                                            </div>
                                                        ` : ''}
                                                    </div>
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            </div>
                        `;
        }).join('')}
                </div>
                
                <div style="margin-top: 2rem;">
                    ${currentSection.content.map(item => {
            if (item.type === 'header') return `<h2 style="font-size: 1.25rem; font-weight: 700; color: white; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">${item.text}</h2>`;
            if (item.type === 'checklist') return `<div style="display: flex; align-items: center; gap: 0.75rem; color: #cbd5e1; margin-left: 1rem; margin-bottom: 0.5rem;"><div style="width: 0.375rem; height: 0.375rem; background-color: var(--color-indigo); border-radius: 50%;"></div>${item.text}</div>`;
            if (item.type === 'special_block' && item.data) return renderSpecialBlock(item.data);
            return `<p style="color: var(--text-muted); margin-bottom: 0.5rem;">${item.text}</p>`;
        }).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;

        // Event Listeners
        container.querySelectorAll('.btn-section').forEach(btn => {
            btn.addEventListener('click', () => {
                state.activeSection = parseInt(btn.dataset.idx);
                render();
            });
        });

        container.querySelectorAll('.episode-item').forEach(item => {
            item.addEventListener('click', () => {
                toggleItem(item.dataset.id);
            });
        });

        container.querySelectorAll('.sequence-header').forEach(header => {
            header.addEventListener('click', () => {
                toggleSequence(header.dataset.seq);
            });
        });

        container.querySelectorAll('.shot-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleItem(toggle.dataset.id);
            });
        });

        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value;
            render();
            const newInput = document.getElementById('search-input');
            newInput.focus();
            newInput.setSelectionRange(newInput.value.length, newInput.value.length);
        });
    }

    render();
});
