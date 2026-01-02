// ============================================
// NEXUS CREATIVE - Static Website
// ============================================

// --- DOM ELEMENTS ---
const elements = {
    themeToggle: document.getElementById('theme-toggle'),
    mobileMenu: document.getElementById('mobileMenu'),
    navLinks: document.getElementById('navLinks'),
    contactForm: document.getElementById('contactForm'),
    navbar: document.querySelector('.navbar')
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    setupEventListeners();
    setupScrollAnimations();
});

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // Theme toggle
    elements.themeToggle?.addEventListener('click', toggleTheme);

    // Mobile menu
    elements.mobileMenu?.addEventListener('click', toggleMobileMenu);

    // Contact form
    elements.contactForm?.addEventListener('submit', handleContactSubmit);

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                closeMobileMenu();
            }
        });
    });

    // Close mobile menu on link click
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Navbar scroll effect
    window.addEventListener('scroll', handleScroll);
}

// --- THEME TOGGLE ---
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    const icon = elements.themeToggle.querySelector('i');
    icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const icon = elements.themeToggle?.querySelector('i');
    if (icon) {
        icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// --- MOBILE MENU ---
function toggleMobileMenu() {
    elements.navLinks?.classList.toggle('open');
    const icon = elements.mobileMenu?.querySelector('i');
    if (icon) {
        icon.className = elements.navLinks?.classList.contains('open')
            ? 'fas fa-times'
            : 'fas fa-bars';
    }
}

function closeMobileMenu() {
    elements.navLinks?.classList.remove('open');
    const icon = elements.mobileMenu?.querySelector('i');
    if (icon) icon.className = 'fas fa-bars';
}

// --- SCROLL EFFECTS ---
function handleScroll() {
    const scrollY = window.scrollY;

    // Navbar background
    if (scrollY > 50) {
        elements.navbar?.classList.add('scrolled');
    } else {
        elements.navbar?.classList.remove('scrolled');
    }
}

// --- SCROLL ANIMATIONS ---
function setupScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.service-card, .portfolio-item, .testimonial-card, .team-card, .info-card, .about-feature'
    );

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('animate-in');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animatedElements.forEach(el => {
        el.classList.add('animate-hidden');
        observer.observe(el);
    });
}

// --- CONTACT FORM ---
function handleContactSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const button = form.querySelector('button[type="submit"]');
    const originalContent = button.innerHTML;

    // Validate
    const name = form.querySelector('#name').value.trim();
    const email = form.querySelector('#email').value.trim();
    const message = form.querySelector('#message').value.trim();

    if (!name || !email || !message) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Animate button
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    button.disabled = true;

    // Simulate submission
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
        button.style.background = '#10b981';

        form.reset();

        setTimeout(() => {
            button.innerHTML = originalContent;
            button.style.background = '';
            button.disabled = false;
        }, 3000);
    }, 1500);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle'}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);

    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// --- COUNTER ANIMATION ---
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const suffix = counter.textContent.replace(/[0-9]/g, '');
        let current = 0;
        const increment = target / 50;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target + suffix;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current) + suffix;
            }
        }, 30);
    });
}

// Start counter animation when hero is visible
const heroObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        animateCounters();
        heroObserver.disconnect();
    }
}, { threshold: 0.5 });

const heroSection = document.querySelector('.hero');
if (heroSection) heroObserver.observe(heroSection);
