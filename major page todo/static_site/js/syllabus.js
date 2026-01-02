
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('app-container');
    const data = await fetchData('exams.json');

    if (!data) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load syllabus data.</div>';
        return;
    }

    // State
    const state = {
        data: data,
        examNames: Object.keys(data),
        selectedExam: Object.keys(data)[0],
        selectedStream: null,
        searchQuery: '',
        expandedSubject: null,
        completedTopics: new Set()
    };

    // Initialize Stream
    updateAvailableStreams();

    // Load Progress
    const savedProgress = localStorage.getItem('syllabusProgress');
    if (savedProgress) {
        try {
            const parsed = JSON.parse(savedProgress);
            state.completedTopics = new Set(parsed);
        } catch (e) {
            console.error("Failed to parse progress", e);
        }
    }

    function updateAvailableStreams() {
        const streams = Object.keys(state.data[state.selectedExam] || {});
        state.selectedStream = streams.length > 0 ? streams[0] : null;
    }

    function saveProgress() {
        localStorage.setItem('syllabusProgress', JSON.stringify(Array.from(state.completedTopics)));
    }

    function toggleTopic(topicTitle) {
        if (state.completedTopics.has(topicTitle)) {
            state.completedTopics.delete(topicTitle);
        } else {
            state.completedTopics.add(topicTitle);
        }
        saveProgress();
        render();
    }

    function resetProgress() {
        if (confirm('Are you sure you want to reset all progress?')) {
            state.completedTopics = new Set();
            saveProgress();
            render();
        }
    }

    function render() {
        const currentSubjects = state.data[state.selectedExam]?.[state.selectedStream] || [];

        // Filter logic
        const filteredSubjects = currentSubjects.map(subject => ({
            ...subject,
            topics: subject.topics.filter(topic =>
                topic.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
                topic.details.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
                subject.name.toLowerCase().includes(state.searchQuery.toLowerCase())
            )
        })).filter(subject => subject.topics.length > 0 || subject.name.toLowerCase().includes(state.searchQuery.toLowerCase()));

        // Progress logic
        const totalTopics = currentSubjects.reduce((acc, subject) => acc + subject.topics.length, 0);
        const completedCount = currentSubjects.reduce((acc, subject) => {
            return acc + subject.topics.filter(t => state.completedTopics.has(t.title)).length;
        }, 0);
        const progressPercentage = totalTopics > 0 ? Math.round((completedCount / totalTopics) * 100) : 0;

        // Icons
        const GraduationCap = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>';
        const SearchIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>';
        const BookOpen = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 1-4 4v14a3 3 0 0 1 3-3h7z"/></svg>';
        const ChevronDown = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
        const Check = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

        // HTML Construction
        let html = `
            <div class="controls-container">
                <div class="exam-selector">
                    ${state.examNames.map(exam => `
                        <button class="btn-exam ${state.selectedExam === exam ? 'active' : ''}" data-exam="${exam}">
                            ${GraduationCap}
                            ${exam}
                        </button>
                    `).join('')}
                </div>

                <div class="stream-search-row">
                    <div class="stream-selector">
                        ${Object.keys(state.data[state.selectedExam] || {}).map(stream => `
                            <button class="btn-stream ${state.selectedStream === stream ? 'active' : ''}" data-stream="${stream}">
                                ${stream}
                            </button>
                        `).join('')}
                    </div>

                    <div class="search-container">
                        <div class="search-icon">${SearchIcon}</div>
                        <input type="text" class="search-input" placeholder="Search topics..." value="${state.searchQuery}">
                    </div>
                </div>

                <div class="progress-section">
                    <div class="progress-header">
                        <span style="color: var(--text-muted)">Progress</span>
                        <div style="display: flex; gap: 1rem;">
                            <span style="color: var(--color-blue); font-weight: 500;">${progressPercentage}% Completed</span>
                            ${completedCount > 0 ? `<button id="reset-btn" style="color: var(--color-red); background: none; border: none; cursor: pointer; text-decoration: underline; font-size: 0.75rem;">Reset</button>` : ''}
                        </div>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: ${progressPercentage}%"></div>
                    </div>
                </div>
            </div>

            <div class="subjects-grid">
                ${filteredSubjects.length === 0 ?
                '<div style="text-align: center; padding: 3rem; color: var(--text-muted);">No topics found matching your search.</div>' :
                filteredSubjects.map(subject => `
                        <div class="subject-card ${state.expandedSubject === subject.name ? 'expanded' : ''}">
                            <button class="subject-header" data-subject="${subject.name}">
                                <div class="subject-info">
                                    <div class="subject-icon">
                                        ${BookOpen}
                                    </div>
                                    <div>
                                        <h3 style="font-size: 1.125rem; font-weight: 600; color: white; margin-bottom: 0.25rem;">${subject.name}</h3>
                                        <p style="font-size: 0.875rem; color: var(--text-muted);">${subject.topics.length} Topics</p>
                                    </div>
                                </div>
                                <div class="chevron">${ChevronDown}</div>
                            </button>
                            <div class="topics-list">
                                ${subject.topics.map(topic => {
                    const isCompleted = state.completedTopics.has(topic.title);
                    return `
                                        <div class="topic-item ${isCompleted ? 'completed' : ''}" data-topic="${topic.title}">
                                            <div class="checkbox">
                                                ${isCompleted ? Check : ''}
                                            </div>
                                            <div>
                                                <div class="topic-title">${topic.title}</div>
                                                <div class="topic-desc">${topic.details}</div>
                                            </div>
                                        </div>
                                    `;
                }).join('')}
                            </div>
                        </div>
                    `).join('')
            }
            </div>
        `;

        container.innerHTML = html;

        // Event Listeners
        // Exam Selection
        container.querySelectorAll('.btn-exam').forEach(btn => {
            btn.addEventListener('click', () => {
                state.selectedExam = btn.dataset.exam;
                updateAvailableStreams();
                render();
            });
        });

        // Stream Selection
        container.querySelectorAll('.btn-stream').forEach(btn => {
            btn.addEventListener('click', () => {
                state.selectedStream = btn.dataset.stream;
                render();
            });
        });

        // Search
        const searchInput = container.querySelector('.search-input');
        searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value;
            render();
            // Refocus input after render
            const newInput = container.querySelector('.search-input');
            newInput.focus();
            newInput.setSelectionRange(newInput.value.length, newInput.value.length);
        });

        // Reset Progress
        const resetBtn = container.querySelector('#reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', resetProgress);
        }

        // Expand Subject
        container.querySelectorAll('.subject-header').forEach(btn => {
            btn.addEventListener('click', () => {
                const subjectName = btn.dataset.subject;
                state.expandedSubject = state.expandedSubject === subjectName ? null : subjectName;
                render();
            });
        });

        // Toggle Topic
        container.querySelectorAll('.topic-item').forEach(item => {
            item.addEventListener('click', () => {
                toggleTopic(item.dataset.topic);
            });
        });
    }

    render();
});
