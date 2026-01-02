// ============================================
// CONNECT 2025 - Social Media Landing Page
// ============================================

// --- DOM ELEMENTS ---
const elements = {
    mobileMenu: document.getElementById('mobileMenu'),
    navLinks: document.getElementById('navLinks'),
    waitlistForm: document.getElementById('waitlistForm'),
    ctaForm: document.getElementById('ctaForm'),
    emailInput: document.getElementById('emailInput'),
    formNote: document.getElementById('formNote'),
    earlyAccess: document.getElementById('earlyAccess'),
    faqItems: document.querySelectorAll('.faq-item')
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupCountUp();
    setupScrollAnimations();
});

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // Mobile menu
    elements.mobileMenu?.addEventListener('click', toggleMobileMenu);

    // Waitlist forms
    elements.waitlistForm?.addEventListener('submit', handleWaitlistSubmit);
    elements.ctaForm?.addEventListener('submit', handleWaitlistSubmit);

    // Early access button
    elements.earlyAccess?.addEventListener('click', () => {
        elements.emailInput?.focus();
        document.getElementById('hero')?.scrollIntoView({ behavior: 'smooth' });
    });

    // FAQ accordion
    elements.faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question?.addEventListener('click', () => toggleFAQ(item));
    });

    // Smooth scroll for nav links
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

// --- FORM HANDLING ---
function handleWaitlistSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const emailInput = form.querySelector('input[type="email"]');
    const button = form.querySelector('button');
    const email = emailInput.value;

    // Validate
    if (!email || !email.includes('@')) {
        showFormError(form, 'Please enter a valid email');
        return;
    }

    // Animate button
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    // Simulate submission
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> You\'re In!';
        button.style.background = '#10b981';
        emailInput.value = '';

        // Update form note
        if (elements.formNote) {
            elements.formNote.textContent = '🎉 Welcome! Check your email for next steps.';
            elements.formNote.style.color = '#10b981';
        }

        // Reset after delay
        setTimeout(() => {
            button.innerHTML = originalContent;
            button.style.background = '';
            button.disabled = false;
        }, 3000);
    }, 1500);
}

function showFormError(form, message) {
    const input = form.querySelector('input');
    input.style.borderColor = '#ef4444';
    input.placeholder = message;

    setTimeout(() => {
        input.style.borderColor = '';
        input.placeholder = 'Enter your email';
    }, 2000);
}

// --- FAQ ACCORDION ---
function toggleFAQ(item) {
    const isOpen = item.classList.contains('open');

    // Close all
    elements.faqItems.forEach(faq => {
        faq.classList.remove('open');
        const answer = faq.querySelector('.faq-answer');
        if (answer) answer.style.maxHeight = null;
    });

    // Open clicked if it wasn't open
    if (!isOpen) {
        item.classList.add('open');
        const answer = item.querySelector('.faq-answer');
        if (answer) answer.style.maxHeight = answer.scrollHeight + 'px';
    }
}

// --- COUNT UP ANIMATION ---
function setupCountUp() {
    const countElements = document.querySelectorAll('.count');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCount(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    countElements.forEach(el => observer.observe(el));
}

function animateCount(el) {
    const target = parseInt(el.dataset.target);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            el.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            el.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// --- SCROLL ANIMATIONS ---
function setupScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.feature-card, .step, .testimonial-card, .pricing-card, .faq-item'
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

// --- NAV SCROLL EFFECT ---
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});
