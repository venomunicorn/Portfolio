// ============================================
// VANILLA SPA - Single Page Application
// ============================================

// --- ROUTES ---
const routes = {
    'home': {
        title: 'Home',
        render: () => `
            <div class="page-header">
                <h1>Welcome to Our SPA</h1>
                <p>A modern single-page application built with vanilla JavaScript</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon"><i class="fas fa-bolt"></i></div>
                    <h3>Lightning Fast</h3>
                    <p>No page reloads, instant navigation between views</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"><i class="fas fa-code"></i></div>
                    <h3>Pure JavaScript</h3>
                    <p>No frameworks needed, just vanilla JS and modern CSS</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"><i class="fas fa-mobile-alt"></i></div>
                    <h3>Responsive</h3>
                    <p>Works beautifully on all devices and screen sizes</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"><i class="fas fa-palette"></i></div>
                    <h3>Themeable</h3>
                    <p>Toggle between light and dark mode instantly</p>
                </div>
            </div>
            
            <div class="cta-section">
                <h2>Ready to explore?</h2>
                <a href="#projects" class="btn-primary">View Projects</a>
            </div>
        `
    },

    'about': {
        title: 'About',
        render: () => `
            <div class="page-header">
                <h1>About Us</h1>
                <p>Building the future of web applications</p>
            </div>
            
            <div class="about-content">
                <div class="about-text">
                    <h2>Our Story</h2>
                    <p>We started with a simple mission: prove that you don't need heavy frameworks to build amazing web experiences. This SPA demonstrates what's possible with just HTML, CSS, and JavaScript.</p>
                    
                    <h2>Our Tech Stack</h2>
                    <ul class="tech-list">
                        <li><i class="fab fa-html5"></i> HTML5 Semantic Markup</li>
                        <li><i class="fab fa-css3-alt"></i> CSS3 with Custom Properties</li>
                        <li><i class="fab fa-js"></i> Vanilla ES6+ JavaScript</li>
                        <li><i class="fas fa-route"></i> Hash-based Routing</li>
                    </ul>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>0</h3>
                        <p>Dependencies</p>
                    </div>
                    <div class="stat-card">
                        <h3>< 10KB</h3>
                        <p>Total Size</p>
                    </div>
                    <div class="stat-card">
                        <h3>100%</h3>
                        <p>Modern JS</p>
                    </div>
                </div>
            </div>
        `
    },

    'projects': {
        title: 'Projects',
        render: () => `
            <div class="page-header">
                <h1>Our Projects</h1>
                <p>Explore our portfolio of innovative solutions</p>
            </div>
            
            <div class="projects-grid">
                ${projectsData.map(project => `
                    <div class="project-card" onclick="showProjectModal(${project.id})">
                        <div class="project-image">
                            <img src="${project.image}" alt="${project.name}" loading="lazy">
                            <div class="project-overlay" style="background: ${project.gradient}">
                                <i class="${project.icon}"></i>
                            </div>
                        </div>
                        <div class="project-info">
                            <h3>${project.name}</h3>
                            <p>${project.short}</p>
                            <div class="project-tags">
                                ${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `
    },

    'team': {
        title: 'Team',
        render: () => `
            <div class="page-header">
                <h1>Meet Our Team</h1>
                <p>The talented people behind our success</p>
            </div>
            
            <div class="team-grid">
                ${teamData.map(member => `
                    <div class="team-card">
                        <div class="team-avatar" style="background: ${member.color}">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>${member.name}</h3>
                        <p class="team-role">${member.role}</p>
                        <p class="team-bio">${member.bio}</p>
                        <div class="team-social">
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin"></i></a>
                            <a href="#"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                `).join('')}
            </div>
        `
    },

    'blog': {
        title: 'Blog',
        render: () => `
            <div class="page-header">
                <h1>Latest Articles</h1>
                <p>Insights and updates from our team</p>
            </div>
            
            <div class="blog-grid">
                ${blogData.map(post => `
                    <article class="blog-card">
                        <div class="blog-image" style="background: ${post.gradient}">
                            <span class="blog-category">${post.category}</span>
                        </div>
                        <div class="blog-content">
                            <div class="blog-meta">
                                <span><i class="fas fa-calendar"></i> ${post.date}</span>
                                <span><i class="fas fa-clock"></i> ${post.readTime}</span>
                            </div>
                            <h3>${post.title}</h3>
                            <p>${post.excerpt}</p>
                            <button class="btn-read-more" onclick="alert('Full article coming soon!')">
                                Read More <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                    </article>
                `).join('')}
            </div>
        `
    },

    'contact': {
        title: 'Contact',
        render: () => `
            <div class="page-header">
                <h1>Get In Touch</h1>
                <p>We'd love to hear from you</p>
            </div>
            
            <div class="contact-container">
                <div class="contact-info">
                    <div class="info-card">
                        <i class="fas fa-envelope"></i>
                        <h3>Email</h3>
                        <p>hello@spademo.com</p>
                    </div>
                    <div class="info-card">
                        <i class="fas fa-phone"></i>
                        <h3>Phone</h3>
                        <p>+1 (555) 123-4567</p>
                    </div>
                    <div class="info-card">
                        <i class="fas fa-map-marker-alt"></i>
                        <h3>Location</h3>
                        <p>San Francisco, CA</p>
                    </div>
                </div>
                
                <form class="contact-form" id="contactForm" onsubmit="handleContactSubmit(event)">
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" id="name" required placeholder="Your name">
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" required placeholder="Your email">
                    </div>
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <input type="text" id="subject" required placeholder="Subject">
                    </div>
                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea id="message" rows="5" required placeholder="Your message"></textarea>
                    </div>
                    <button type="submit" class="btn-primary btn-submit">
                        <i class="fas fa-paper-plane"></i> Send Message
                    </button>
                </form>
            </div>
        `
    },

    '404': {
        title: 'Not Found',
        render: () => `
            <div class="error-page">
                <h1>404</h1>
                <p>Oops! The page you're looking for doesn't exist.</p>
                <a href="#home" class="btn-primary">Go Home</a>
            </div>
        `
    }
};

// --- DATA ---
const projectsData = [
    // C++ Projects - All with interactive web demos
    { id: 1, name: '2D Arcade Game', short: 'Space Invaders-style game', icon: 'fas fa-gamepad', gradient: 'linear-gradient(135deg, #f87171, #dc2626)', tags: ['C++', 'Game', 'Canvas'], description: 'Space Invaders with player, enemies, bullets, and explosions. Full arcade experience!', image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=250&fit=crop', demo: '../../C++/2DArcadeGame/demo.html', category: 'C++' },
    { id: 2, name: '3D Graphics Engine', short: 'Interactive 3D renderer', icon: 'fas fa-cube', gradient: 'linear-gradient(135deg, #a855f7, #7c3aed)', tags: ['C++', '3D', 'Graphics'], description: 'Rotating 3D shapes with mouse controls and painter\'s algorithm rendering.', image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=250&fit=crop', demo: '../../C++/3dGraphicEngine/demo.html', category: 'C++' },
    { id: 3, name: 'Chess Engine', short: 'Playable chess game', icon: 'fas fa-chess', gradient: 'linear-gradient(135deg, #8b5cf6, #6366f1)', tags: ['C++', 'AI', 'Game'], description: 'Full chess with piece movement, highlighting, and turn-based gameplay.', image: 'https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=400&h=250&fit=crop', demo: '../../C++/ChessEngine/demo.html', category: 'C++' },
    { id: 4, name: 'Ray Tracer', short: 'Real-time ray tracing', icon: 'fas fa-sun', gradient: 'linear-gradient(135deg, #f59e0b, #d97706)', tags: ['C++', 'Graphics', 'Math'], description: 'Ray traced spheres with reflections, shadows, and animation controls.', image: 'https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=400&h=250&fit=crop', demo: '../../C++/RayTracer/demo.html', category: 'C++' },
    { id: 5, name: 'Neural Network', short: 'Visual ML training', icon: 'fas fa-brain', gradient: 'linear-gradient(135deg, #10b981, #059669)', tags: ['C++', 'ML', 'AI'], description: 'Watch a neural network learn to solve the XOR problem with live visualization.', image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop', demo: '../../C++/MachineLearningModel/demo.html', category: 'C++' },
    { id: 6, name: 'Sudoku Solver', short: 'Backtracking algorithm', icon: 'fas fa-th', gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)', tags: ['C++', 'Algorithm', 'Puzzle'], description: 'Solve any Sudoku puzzle with visual backtracking animation.', image: 'https://images.unsplash.com/photo-1580541832626-2a7131ee809f?w=400&h=250&fit=crop', demo: '../../C++/SudokuSolver/demo.html', category: 'C++' },
    { id: 7, name: 'File Encryption', short: 'Caesar, XOR, Base64', icon: 'fas fa-lock', gradient: 'linear-gradient(135deg, #ef4444, #dc2626)', tags: ['C++', 'Crypto', 'Security'], description: 'Encrypt and decrypt text using multiple algorithms.', image: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=250&fit=crop', demo: '../../C++/FileEncryption/demo.html', category: 'C++' },
    { id: 8, name: 'Game Server', short: 'Multiplayer networking', icon: 'fas fa-server', gradient: 'linear-gradient(135deg, #06b6d4, #0891b2)', tags: ['C++', 'Network', 'Server'], description: 'Server panel with client connections and packet statistics.', image: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=250&fit=crop', demo: '../../C++/GameServerClient/demo.html', category: 'C++' },
    { id: 9, name: 'Music Player', short: 'Playlist & controls', icon: 'fas fa-music', gradient: 'linear-gradient(135deg, #ec4899, #db2777)', tags: ['C++', 'Audio', 'UI'], description: 'Beautiful music player with animated album art and playlist.', image: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=250&fit=crop', demo: '../../C++/SimpleMusicPlayer/demo.html', category: 'C++' },
    { id: 10, name: 'Dragon\'s Lair', short: 'Text adventure game', icon: 'fas fa-dragon', gradient: 'linear-gradient(135deg, #f97316, #ea580c)', tags: ['C++', 'Adventure', 'Story'], description: 'Branching story with inventory, health, gold, and multiple endings!', image: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&h=250&fit=crop', demo: '../../C++/TextBasedAdventureGame/demo.html', category: 'C++' },

    // Python Projects - GUI apps with run commands
    { id: 11, name: 'Scientific Calculator', short: 'Advanced math functions', icon: 'fas fa-calculator', gradient: 'linear-gradient(135deg, #fbbf24, #f59e0b)', tags: ['Python', 'Math', 'GUI'], description: 'Full scientific calculator with history, dark theme, and advanced functions.', image: 'https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },
    { id: 12, name: 'Tic-Tac-Toe AI', short: 'Unbeatable Minimax', icon: 'fas fa-times', gradient: 'linear-gradient(135deg, #f87171, #ef4444)', tags: ['Python', 'AI', 'Game'], description: 'Play against an unbeatable AI using the Minimax algorithm.', image: 'https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },
    { id: 13, name: 'AI Chatbot', short: 'Chat with support mode', icon: 'fas fa-robot', gradient: 'linear-gradient(135deg, #6366f1, #4f46e5)', tags: ['Python', 'AI', 'NLP'], description: 'Conversational chatbot with message bubbles and tech support mode.', image: 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },
    { id: 14, name: 'Blockchain Demo', short: 'Mining & validation', icon: 'fas fa-link', gradient: 'linear-gradient(135deg, #14b8a6, #0d9488)', tags: ['Python', 'Crypto', 'Blockchain'], description: 'Interactive blockchain with mining, proof-of-work, and block explorer.', image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },
    { id: 15, name: 'Data Visualization', short: 'Charts from CSV', icon: 'fas fa-chart-pie', gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', tags: ['Python', 'Data', 'Charts'], description: 'Create bar, line, and pie charts from CSV data with color themes.', image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },
    { id: 16, name: 'QR Code Generator', short: 'Custom colors & save', icon: 'fas fa-qrcode', gradient: 'linear-gradient(135deg, #64748b, #475569)', tags: ['Python', 'Utility', 'QR'], description: 'Generate QR codes with custom colors and save as PNG.', image: 'https://images.unsplash.com/photo-1595079676339-1534801ad6cf?w=400&h=250&fit=crop', runCmd: 'python gui_main.py', category: 'Python' },

    // Web Projects - Live demos
    { id: 17, name: 'E-Commerce Platform', short: 'Modern shopping experience', icon: 'fas fa-shopping-cart', gradient: 'linear-gradient(135deg, #667eea, #764ba2)', tags: ['Web', 'React', 'Node.js'], description: 'Full-featured e-commerce platform with cart and checkout.', image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=250&fit=crop', demo: '../../Web/E-commercePlatform/index.html', category: 'Web' },
    { id: 18, name: 'Real-Time Dashboard', short: 'Live data visualization', icon: 'fas fa-chart-line', gradient: 'linear-gradient(135deg, #f093fb, #f5576c)', tags: ['Web', 'Charts', 'Real-time'], description: 'Interactive dashboard for monitoring business metrics.', image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop', demo: '../../Web/RealTimeDataDashboard/index.html', category: 'Web' },
    { id: 19, name: 'Quiz Application', short: 'Interactive quiz', icon: 'fas fa-question-circle', gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)', tags: ['Web', 'Interactive', 'Game'], description: 'Quiz app with timer, scoring, and multiple question types.', image: 'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=400&h=250&fit=crop', demo: '../../Web/QuizApplication/index.html', category: 'Web' },
    { id: 20, name: 'Weather App', short: 'Live weather data', icon: 'fas fa-cloud-sun', gradient: 'linear-gradient(135deg, #43e97b, #38f9d7)', tags: ['Web', 'API', 'Weather'], description: 'Beautiful weather app with forecasts and location detection.', image: 'https://images.unsplash.com/photo-1592210454359-9043f067919b?w=400&h=250&fit=crop', demo: '../../Web/WeatherAPp/index.html', category: 'Web' }
];

const teamData = [
    { name: 'Alex Johnson', role: 'CEO & Founder', bio: 'Visionary leader with 15+ years in tech', color: 'linear-gradient(135deg, #667eea, #764ba2)' },
    { name: 'Sarah Chen', role: 'Lead Developer', bio: 'Full-stack expert passionate about clean code', color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
    { name: 'Michael Brown', role: 'UI/UX Designer', bio: 'Creating beautiful and intuitive experiences', color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
    { name: 'Emily Davis', role: 'Product Manager', bio: 'Turning ideas into successful products', color: 'linear-gradient(135deg, #43e97b, #38f9d7)' }
];

const blogData = [
    { title: 'Building Modern SPAs', excerpt: 'Learn how to create fast, modern single-page applications without heavy frameworks...', date: 'Dec 20, 2024', readTime: '5 min', category: 'Tutorial', gradient: 'linear-gradient(135deg, #667eea, #764ba2)' },
    { title: 'The Power of Vanilla JS', excerpt: 'Discover what you can achieve with pure JavaScript and modern browser APIs...', date: 'Dec 18, 2024', readTime: '4 min', category: 'Opinion', gradient: 'linear-gradient(135deg, #f093fb, #f5576c)' },
    { title: 'CSS Custom Properties', excerpt: 'Master CSS variables for themeable and maintainable stylesheets...', date: 'Dec 15, 2024', readTime: '6 min', category: 'CSS', gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)' }
];

// --- STATE ---
let isDarkMode = false;

// --- DOM ELEMENTS ---
const elements = {
    viewContainer: document.getElementById('view-container'),
    sidebar: document.getElementById('sidebar'),
    sidebarOverlay: document.getElementById('sidebarOverlay'),
    mobileMenuBtn: document.getElementById('mobileMenuBtn'),
    themeToggle: document.getElementById('themeToggle'),
    loading: document.getElementById('loading'),
    modal: document.getElementById('productModal'),
    modalBody: document.getElementById('modalBody'),
    modalClose: document.getElementById('modalClose')
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    setupEventListeners();
    router();
});

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // Hash change
    window.addEventListener('hashchange', router);

    // Mobile menu
    elements.mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    elements.sidebarOverlay.addEventListener('click', closeMobileMenu);

    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);

    // Modal close
    elements.modalClose.addEventListener('click', closeModal);
    elements.modal.addEventListener('click', (e) => {
        if (e.target === elements.modal) closeModal();
    });

    // Close mobile menu on nav click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
}

// --- ROUTER ---
function router() {
    let hash = window.location.hash.slice(1) || 'home';

    // 404 handling
    if (!routes[hash]) hash = '404';

    const route = routes[hash];

    // Show loading
    elements.loading.classList.add('visible');

    // Simulate slight delay for effect
    setTimeout(() => {
        // Update content with animation
        elements.viewContainer.innerHTML = `<div class="page-transition">${route.render()}</div>`;

        // Update active nav
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + hash) {
                link.classList.add('active');
            }
        });

        // Update title
        document.title = `${route.title} | Vanilla SPA`;

        // Hide loading
        elements.loading.classList.remove('visible');

        // Scroll to top
        elements.viewContainer.scrollTop = 0;
    }, 200);
}

// --- MOBILE MENU ---
function toggleMobileMenu() {
    elements.sidebar.classList.toggle('open');
    elements.sidebarOverlay.classList.toggle('visible');
}

function closeMobileMenu() {
    elements.sidebar.classList.remove('open');
    elements.sidebarOverlay.classList.remove('visible');
}

// --- THEME ---
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);
    elements.themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('spa_theme', isDarkMode ? 'dark' : 'light');
}

function loadTheme() {
    const saved = localStorage.getItem('spa_theme');
    if (saved === 'dark') {
        isDarkMode = true;
        document.body.classList.add('dark-mode');
        elements.themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

// --- MODAL ---
function showProjectModal(id) {
    const project = projectsData.find(p => p.id === id);
    if (!project) return;

    // Determine action button based on project type
    let actionButton = '';
    if (project.demo) {
        actionButton = `<a href="${project.demo}" target="_blank" class="btn-primary"><i class="fas fa-play"></i> Launch Demo</a>`;
    } else if (project.runCmd) {
        actionButton = `
            <div class="run-command-box">
                <span class="run-label">Run in terminal:</span>
                <code>${project.runCmd}</code>
            </div>
        `;
    } else {
        actionButton = `<a href="#" class="btn-primary" onclick="closeModal(); return false;">View Details</a>`;
    }

    // Category badge
    const categoryBadge = project.category ?
        `<span class="category-badge" style="background: ${project.gradient}">${project.category}</span>` : '';

    elements.modalBody.innerHTML = `
        <div class="modal-project">
            <div class="modal-image">
                <img src="${project.image}" alt="${project.name}">
                <div class="modal-icon-overlay" style="background: ${project.gradient}">
                    <i class="${project.icon}"></i>
                </div>
                ${categoryBadge}
            </div>
            <h2>${project.name}</h2>
            <p>${project.description}</p>
            <div class="modal-tags">
                ${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            ${actionButton}
        </div>
    `;

    elements.modal.classList.add('visible');
}

function closeModal() {
    elements.modal.classList.remove('visible');
}

// --- CONTACT FORM ---
function handleContactSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const name = form.querySelector('#name').value;
    const email = form.querySelector('#email').value;

    // Simulate submission
    const btn = form.querySelector('.btn-submit');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    btn.disabled = true;

    setTimeout(() => {
        btn.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
        btn.style.background = '#10b981';

        form.reset();

        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
            btn.style.background = '';
            btn.disabled = false;
        }, 2000);
    }, 1500);
}
