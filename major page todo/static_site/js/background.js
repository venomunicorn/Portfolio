/**
 * 3D-like Particle Network Background
 * Creates a premium, dynamic background with floating particles and connections.
 * Theme-aware: Adapts to Light/Dark mode.
 */

const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
document.body.appendChild(canvas);

canvas.style.position = 'fixed';
canvas.style.top = '0';
canvas.style.left = '0';
canvas.style.width = '100%';
canvas.style.height = '100%';
canvas.style.zIndex = '-1';
canvas.style.transition = 'background 0.5s ease'; // Smooth transition

let width, height;
let particles = [];

// Configuration
const connectionDistance = 150;

// Theme Configuration
const themes = {
    light: {
        background: 'linear-gradient(to bottom right, #fdfbf7, #f1f5f9)', // Cream to Slate-100
        particleColor: 'rgba(71, 85, 105, 0.3)', // Slate-600
        lineColor: 'rgba(100, 116, 139, ' // Slate-500
    },
    dark: {
        background: 'linear-gradient(to bottom right, #0f172a, #1e293b)', // Slate-900 to Slate-800
        particleColor: 'rgba(148, 163, 184, 0.3)', // Slate-400
        lineColor: 'rgba(148, 163, 184, ' // Slate-400
    }
};

let currentTheme = 'light';

class Particle {
    constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 2 + 1;
        this.color = themes[currentTheme].particleColor;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function updateTheme() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    currentTheme = isDark ? 'dark' : 'light';
    // canvas.style.background = themes[currentTheme].background; // Removed to rely on CSS

    // Update existing particles color
    const color = themes[currentTheme].particleColor;
    particles.forEach(p => p.color = color);
}

// Watch for theme changes
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
            updateTheme();
        }
    });
});

observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
});

function init() {
    resize();
    updateTheme(); // Set initial theme
    createParticles();
    animate();
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

function createParticles() {
    particles = [];
    const count = Math.floor((width * height) / 15000); // Responsive count
    for (let i = 0; i < count; i++) {
        particles.push(new Particle());
    }
}

function animate() {
    ctx.clearRect(0, 0, width, height);

    // Draw particles and connections
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();

        // Connect particles
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < connectionDistance) {
                ctx.beginPath();
                const opacity = 1 - distance / connectionDistance;
                ctx.strokeStyle = themes[currentTheme].lineColor + opacity + ')';
                ctx.lineWidth = 0.5;
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }

    requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
    resize();
    createParticles();
});

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
