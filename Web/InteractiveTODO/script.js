// ============================================
// TASK MASTER - Enhanced Todo Application
// ============================================

// --- STATE ---
let todos = [];
let filter = 'all';
let priorityFilter = 'all';
let searchQuery = '';
let isDarkMode = false;

// --- DOM ELEMENTS ---
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const prioritySelect = document.getElementById('priority-select');
const dueDateInput = document.getElementById('due-date');
const todoList = document.getElementById('todo-list');
const searchInput = document.getElementById('search-input');
const priorityFilterSelect = document.getElementById('priority-filter');
const emptyState = document.getElementById('emptyState');
const themeToggle = document.getElementById('themeToggle');
const clearCompletedBtn = document.getElementById('clearCompleted');

// Stats elements
const totalTasksEl = document.getElementById('totalTasks');
const completedTasksEl = document.getElementById('completedTasks');
const pendingTasksEl = document.getElementById('pendingTasks');
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    loadTheme();
    setupEventListeners();
    render();
});

function setupEventListeners() {
    // Form submission
    todoForm.addEventListener('submit', addTodo);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            filter = e.target.dataset.filter;
            render();
        });
    });

    // Priority filter
    priorityFilterSelect.addEventListener('change', (e) => {
        priorityFilter = e.target.value;
        render();
    });

    // Search
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        render();
    });

    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);

    // Clear completed
    clearCompletedBtn.addEventListener('click', clearCompleted);

    // Todo list clicks (delegation)
    todoList.addEventListener('click', handleTodoClick);
}

// --- ADD TODO ---
function addTodo(e) {
    e.preventDefault();

    const text = todoInput.value.trim();
    if (!text) return;

    const newTodo = {
        id: Date.now(),
        text: text,
        completed: false,
        priority: prioritySelect.value,
        dueDate: dueDateInput.value || null,
        createdAt: new Date().toISOString()
    };

    todos.unshift(newTodo);
    saveTodos();
    render();

    // Reset form
    todoInput.value = '';
    dueDateInput.value = '';
    prioritySelect.value = 'medium';
    todoInput.focus();
}

// --- HANDLE TODO CLICKS ---
function handleTodoClick(e) {
    const todoEl = e.target.closest('.todo');
    if (!todoEl) return;

    const id = parseInt(todoEl.dataset.id);

    // Complete button
    if (e.target.closest('.complete-btn')) {
        toggleComplete(id);
    }

    // Delete button
    if (e.target.closest('.trash-btn')) {
        deleteTodo(id);
    }

    // Edit button
    if (e.target.closest('.edit-btn')) {
        startEdit(id, todoEl);
    }
}

// --- TOGGLE COMPLETE ---
function toggleComplete(id) {
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        saveTodos();
        render();
    }
}

// --- DELETE TODO ---
function deleteTodo(id) {
    const todoEl = document.querySelector(`.todo[data-id="${id}"]`);
    if (todoEl) {
        todoEl.classList.add('fall');
        setTimeout(() => {
            todos = todos.filter(t => t.id !== id);
            saveTodos();
            render();
        }, 300);
    }
}

// --- START EDIT ---
function startEdit(id, todoEl) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const textEl = todoEl.querySelector('.todo-text');
    const currentText = todo.text;

    textEl.innerHTML = `<input type="text" class="edit-input" value="${currentText}">`;
    const input = textEl.querySelector('.edit-input');
    input.focus();
    input.select();

    input.addEventListener('blur', () => finishEdit(id, input.value));
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            finishEdit(id, input.value);
        }
    });
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            render();
        }
    });
}

function finishEdit(id, newText) {
    const todo = todos.find(t => t.id === id);
    if (todo && newText.trim()) {
        todo.text = newText.trim();
        saveTodos();
    }
    render();
}

// --- CLEAR COMPLETED ---
function clearCompleted() {
    todos = todos.filter(t => !t.completed);
    saveTodos();
    render();
}

// --- RENDER ---
function render() {
    // Filter todos
    let filtered = todos.filter(todo => {
        // Status filter
        if (filter === 'completed' && !todo.completed) return false;
        if (filter === 'pending' && todo.completed) return false;

        // Priority filter
        if (priorityFilter !== 'all' && todo.priority !== priorityFilter) return false;

        // Search filter
        if (searchQuery && !todo.text.toLowerCase().includes(searchQuery)) return false;

        return true;
    });

    // Clear list
    todoList.innerHTML = '';

    // Show/hide empty state
    emptyState.style.display = filtered.length === 0 ? 'flex' : 'none';

    // Render todos
    filtered.forEach(todo => {
        const todoEl = createTodoElement(todo);
        todoList.appendChild(todoEl);
    });

    // Update stats
    updateStats();
}

function createTodoElement(todo) {
    const div = document.createElement('div');
    div.className = `todo ${todo.completed ? 'completed' : ''} priority-${todo.priority}`;
    div.dataset.id = todo.id;

    // Check if overdue
    const isOverdue = todo.dueDate && !todo.completed && new Date(todo.dueDate) < new Date();
    if (isOverdue) div.classList.add('overdue');

    // Priority badge
    const priorityBadge = `<span class="priority-badge ${todo.priority}">${todo.priority}</span>`;

    // Due date display
    let dueDateHtml = '';
    if (todo.dueDate) {
        const date = new Date(todo.dueDate);
        const formatted = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        dueDateHtml = `<span class="due-date ${isOverdue ? 'overdue' : ''}"><i class="fas fa-calendar"></i> ${formatted}</span>`;
    }

    div.innerHTML = `
        <button class="complete-btn" title="${todo.completed ? 'Undo' : 'Complete'}">
            <i class="fas ${todo.completed ? 'fa-check-circle' : 'fa-circle'}"></i>
        </button>
        <div class="todo-content">
            <span class="todo-text">${todo.text}</span>
            <div class="todo-meta">
                ${priorityBadge}
                ${dueDateHtml}
            </div>
        </div>
        <div class="todo-actions">
            <button class="edit-btn" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="trash-btn" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
    `;

    return div;
}

// --- UPDATE STATS ---
function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;
    const pending = total - completed;
    const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

    totalTasksEl.textContent = total;
    completedTasksEl.textContent = completed;
    pendingTasksEl.textContent = pending;
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}%`;
}

// --- THEME ---
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);
    themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('taskmaster_theme', isDarkMode ? 'dark' : 'light');
}

function loadTheme() {
    const saved = localStorage.getItem('taskmaster_theme');
    if (saved === 'dark') {
        isDarkMode = true;
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

// --- LOCAL STORAGE ---
function saveTodos() {
    localStorage.setItem('taskmaster_todos', JSON.stringify(todos));
}

function loadTodos() {
    const saved = localStorage.getItem('taskmaster_todos');
    todos = saved ? JSON.parse(saved) : [];
}
