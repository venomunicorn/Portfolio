// ============================================
// PROFESSIONAL THEME EFFECTS SYSTEM
// Premium-grade visual effects for portfolio
// ============================================

class ThemeEffectsManager {
    constructor() {
        this.currentEffect = null;
        this.effectsContainer = null;
        this.canvas = null;
        this.ctx = null;
        this.animationId = null;
        this.mouseX = window.innerWidth / 2;
        this.mouseY = window.innerHeight / 2;
        this.targetMouseX = this.mouseX;
        this.targetMouseY = this.mouseY;
        this.scrollY = 0;

        // Mobile detection for performance optimization
        this.isMobile = window.innerWidth <= 768 ||
            ('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0);
        this.particleMultiplier = this.isMobile ? 0.3 : 1; // Reduce particles on mobile
        this.frameSkip = this.isMobile ? 2 : 0; // Skip frames on mobile
        this.frameCount = 0;

        this.init();
    }

    init() {
        this.effectsContainer = document.querySelector('.background-effects');
        if (!this.effectsContainer) return;

        // Create high-DPI canvas
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'effectsCanvas';
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        `;
        this.effectsContainer.insertBefore(this.canvas, this.effectsContainer.firstChild);
        this.ctx = this.canvas.getContext('2d');

        this.resize();
        window.addEventListener('resize', () => this.resize());

        // Smooth mouse tracking
        document.addEventListener('mousemove', (e) => {
            this.targetMouseX = e.clientX;
            this.targetMouseY = e.clientY;
        });

        // Track scroll
        window.addEventListener('scroll', () => {
            this.scrollY = window.scrollY;
        });
    }

    resize() {
        if (!this.canvas) return;
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = window.innerWidth * dpr;
        this.canvas.height = window.innerHeight * dpr;
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = window.innerWidth + 'px';
        this.canvas.style.height = window.innerHeight + 'px';
    }

    switchTheme(themeName) {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }

        if (this.currentEffect && this.currentEffect.cleanup) {
            this.currentEffect.cleanup();
        }

        switch (themeName) {
            case 'brutalist':
                this.currentEffect = new CyberpunkGridEffect(this);
                break;
            case 'luxury':
                this.currentEffect = new LuxuryAuroraEffect(this);
                break;
            case 'scientific':
                this.currentEffect = new NeuralNetworkEffect(this);
                break;
            case 'chaos':
                this.currentEffect = new PlasmaVortexEffect(this);
                break;
            default:
                this.currentEffect = null;
        }

        if (this.currentEffect) {
            this.currentEffect.start();
        }
    }

    animate() {
        // Frame skipping for mobile performance
        this.frameCount++;
        if (this.frameSkip > 0 && this.frameCount % (this.frameSkip + 1) !== 0) {
            this.animationId = requestAnimationFrame(() => this.animate());
            return;
        }

        // Smooth mouse interpolation
        this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
        this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;

        if (this.currentEffect && this.currentEffect.update) {
            this.currentEffect.update();
        }
        this.animationId = requestAnimationFrame(() => this.animate());
    }
}

// ============================================
// THEME 1: CYBERPUNK GRID (Brutalist)
// Professional terminal/hacker aesthetic
// ============================================

class CyberpunkGridEffect {
    constructor(manager) {
        this.manager = manager;
        this.ctx = manager.ctx;
        this.canvas = manager.canvas;
        this.time = 0;
        this.gridLines = [];
        this.dataStreams = [];
        this.glitchTimer = 0;
        this.scanLineY = 0;
        // New effects
        this.codeBlocks = [];
        this.circuitNodes = [];
        this.hexagons = [];
        this.pulseWaves = [];
    }

    start() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create perspective grid lines
        this.gridLines = [];
        const lineCount = 40;
        for (let i = 0; i < lineCount; i++) {
            this.gridLines.push({
                x: (i / lineCount) * width,
                speed: 0.5 + Math.random() * 0.5,
                opacity: 0.1 + Math.random() * 0.2,
                pulseOffset: Math.random() * Math.PI * 2
            });
        }

        // Create data streams (falling code effect but more subtle)
        this.dataStreams = [];
        for (let i = 0; i < 15; i++) {
            this.dataStreams.push({
                x: Math.random() * width,
                y: Math.random() * height,
                speed: 1 + Math.random() * 2,
                length: 50 + Math.random() * 150,
                opacity: 0.3 + Math.random() * 0.4
            });
        }

        // Create floating code blocks
        this.codeBlocks = [];
        for (let i = 0; i < 8; i++) {
            this.codeBlocks.push({
                x: Math.random() * width,
                y: Math.random() * height,
                width: 60 + Math.random() * 80,
                height: 30 + Math.random() * 40,
                speed: 0.3 + Math.random() * 0.5,
                opacity: 0.15 + Math.random() * 0.15,
                cursorPhase: Math.random() * Math.PI * 2,
                lines: Math.floor(2 + Math.random() * 3)
            });
        }

        // Create circuit nodes
        this.circuitNodes = [];
        for (let i = 0; i < 12; i++) {
            this.circuitNodes.push({
                x: Math.random() * width,
                y: Math.random() * height,
                size: 4 + Math.random() * 6,
                pulse: Math.random() * Math.PI * 2,
                connections: []
            });
        }
        // Connect nearby nodes
        this.circuitNodes.forEach((node, i) => {
            this.circuitNodes.forEach((other, j) => {
                if (i !== j) {
                    const dist = Math.hypot(node.x - other.x, node.y - other.y);
                    if (dist < 200 && node.connections.length < 3) {
                        node.connections.push(j);
                    }
                }
            });
        });

        // Create hexagonal overlay
        this.hexagons = [];
        const hexSize = 80;
        const hexRows = Math.ceil(height / (hexSize * 0.866)) + 1;
        const hexCols = Math.ceil(width / (hexSize * 1.5)) + 1;
        for (let row = 0; row < hexRows; row++) {
            for (let col = 0; col < hexCols; col++) {
                const x = col * hexSize * 1.5;
                const y = row * hexSize * 0.866 * 2 + (col % 2) * hexSize * 0.866;
                if (Math.random() < 0.2) {
                    this.hexagons.push({ x, y, size: hexSize * 0.3, pulse: Math.random() * Math.PI * 2 });
                }
            }
        }

        // Create pulse waves from center
        this.pulseWaves = [];

        this.manager.animate();
    }

    update() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        this.time += 0.016;

        // Clear with slight fade for motion blur
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
        this.ctx.fillRect(0, 0, width, height);

        // Draw hexagonal overlay (subtle background)
        this.drawHexOverlay(width, height);

        // Draw perspective grid floor
        this.drawPerspectiveGrid(width, height);

        // Draw circuit node network
        this.drawCircuitNodes(width, height);

        // Draw subtle data streams
        this.drawDataStreams(width, height);

        // Draw floating code blocks
        this.drawCodeBlocks(width, height);

        // Draw pulse waves
        this.drawPulseWaves(width, height);

        // Draw scan line
        this.drawScanLine(width, height);

        // Occasional glitch effect
        this.drawGlitch(width, height);

        // Draw vignette
        this.drawVignette(width, height);
    }

    drawPerspectiveGrid(width, height) {
        const horizon = height * 0.3;
        const vanishX = width / 2 + Math.sin(this.time * 0.5) * 50;

        // Horizontal lines with perspective
        this.ctx.strokeStyle = 'rgba(0, 255, 65, 0.15)';
        this.ctx.lineWidth = 1;

        for (let i = 0; i < 20; i++) {
            const y = horizon + (i / 20) * (height - horizon);
            const perspective = (y - horizon) / (height - horizon);
            const squeeze = 1 - perspective * 0.5;

            this.ctx.globalAlpha = 0.1 + perspective * 0.2;
            this.ctx.beginPath();
            this.ctx.moveTo(vanishX - (vanishX * squeeze), y);
            this.ctx.lineTo(vanishX + ((width - vanishX) * squeeze), y);
            this.ctx.stroke();
        }

        // Vertical lines converging to horizon
        for (let i = 0; i < 30; i++) {
            const x = (i / 29) * width;
            const pulse = Math.sin(this.time * 2 + i * 0.5) * 0.5 + 0.5;

            this.ctx.globalAlpha = 0.05 + pulse * 0.1;
            this.ctx.beginPath();
            this.ctx.moveTo(x, height);
            this.ctx.lineTo(vanishX, horizon);
            this.ctx.stroke();
        }

        this.ctx.globalAlpha = 1;
    }

    drawDataStreams(width, height) {
        this.dataStreams.forEach(stream => {
            const gradient = this.ctx.createLinearGradient(
                stream.x, stream.y - stream.length,
                stream.x, stream.y
            );
            gradient.addColorStop(0, 'rgba(0, 255, 65, 0)');
            gradient.addColorStop(0.5, `rgba(0, 255, 65, ${stream.opacity * 0.5})`);
            gradient.addColorStop(1, `rgba(0, 255, 65, ${stream.opacity})`);

            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(stream.x, stream.y - stream.length);
            this.ctx.lineTo(stream.x, stream.y);
            this.ctx.stroke();

            // Glowing head
            this.ctx.beginPath();
            this.ctx.arc(stream.x, stream.y, 3, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(180, 255, 180, ${stream.opacity})`;
            this.ctx.fill();

            stream.y += stream.speed;
            if (stream.y > height + stream.length) {
                stream.y = -stream.length;
                stream.x = Math.random() * width;
            }
        });
    }

    drawScanLine(width, height) {
        this.scanLineY += 2;
        if (this.scanLineY > height) this.scanLineY = 0;

        const gradient = this.ctx.createLinearGradient(0, this.scanLineY - 20, 0, this.scanLineY + 20);
        gradient.addColorStop(0, 'rgba(0, 255, 65, 0)');
        gradient.addColorStop(0.5, 'rgba(0, 255, 65, 0.1)');
        gradient.addColorStop(1, 'rgba(0, 255, 65, 0)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, this.scanLineY - 20, width, 40);
    }

    drawGlitch(width, height) {
        this.glitchTimer += 0.016;
        if (this.glitchTimer > 3 + Math.random() * 5) {
            this.glitchTimer = 0;

            // Random glitch strips
            for (let i = 0; i < 3; i++) {
                const y = Math.random() * height;
                const h = 2 + Math.random() * 8;
                const offset = (Math.random() - 0.5) * 20;

                this.ctx.fillStyle = `rgba(255, 0, 0, ${0.1 + Math.random() * 0.2})`;
                this.ctx.fillRect(offset, y, width, h);

                this.ctx.fillStyle = `rgba(0, 255, 255, ${0.1 + Math.random() * 0.2})`;
                this.ctx.fillRect(-offset, y + 2, width, h);
            }
        }
    }

    drawCodeBlocks(width, height) {
        this.codeBlocks.forEach(block => {
            // Floating motion
            block.y -= block.speed;
            block.cursorPhase += 0.1;

            if (block.y < -block.height) {
                block.y = height + block.height;
                block.x = Math.random() * width;
            }

            // Block background
            this.ctx.fillStyle = `rgba(0, 20, 0, ${block.opacity})`;
            this.ctx.fillRect(block.x, block.y, block.width, block.height);

            // Border
            this.ctx.strokeStyle = `rgba(0, 255, 65, ${block.opacity * 0.8})`;
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(block.x, block.y, block.width, block.height);

            // Fake code lines
            this.ctx.fillStyle = `rgba(0, 255, 65, ${block.opacity * 0.6})`;
            for (let i = 0; i < block.lines; i++) {
                const lineWidth = 20 + Math.random() * (block.width - 30);
                this.ctx.fillRect(block.x + 5, block.y + 8 + i * 10, lineWidth, 2);
            }

            // Blinking cursor
            const cursorVisible = Math.sin(block.cursorPhase) > 0;
            if (cursorVisible) {
                this.ctx.fillStyle = `rgba(0, 255, 65, ${block.opacity})`;
                this.ctx.fillRect(block.x + block.width - 15, block.y + 8, 8, 12);
            }
        });
    }

    drawCircuitNodes(width, height) {
        // Draw connections first
        this.circuitNodes.forEach((node, i) => {
            node.connections.forEach(j => {
                const other = this.circuitNodes[j];
                const pulse = Math.sin(this.time * 3 + i * 0.5) * 0.5 + 0.5;

                // Draw connection line
                this.ctx.beginPath();
                this.ctx.moveTo(node.x, node.y);
                this.ctx.lineTo(other.x, other.y);
                this.ctx.strokeStyle = `rgba(0, 255, 65, ${0.1 + pulse * 0.15})`;
                this.ctx.lineWidth = 1;
                this.ctx.stroke();

                // Draw traveling pulse on line
                const pulsePos = (this.time * 0.5 + i * 0.3) % 1;
                const px = node.x + (other.x - node.x) * pulsePos;
                const py = node.y + (other.y - node.y) * pulsePos;

                this.ctx.beginPath();
                this.ctx.arc(px, py, 2, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(0, 255, 65, ${0.4 + pulse * 0.4})`;
                this.ctx.fill();
            });
        });

        // Draw nodes
        this.circuitNodes.forEach((node, i) => {
            node.pulse += 0.02;
            const pulse = Math.sin(node.pulse) * 0.5 + 0.5;

            // Outer glow
            const gradient = this.ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, node.size * 3);
            gradient.addColorStop(0, `rgba(0, 255, 65, ${0.3 + pulse * 0.3})`);
            gradient.addColorStop(0.5, `rgba(0, 255, 65, ${0.1 + pulse * 0.1})`);
            gradient.addColorStop(1, 'rgba(0, 255, 65, 0)');

            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.size * 3, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Core
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.size * 0.5, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(150, 255, 150, ${0.6 + pulse * 0.4})`;
            this.ctx.fill();
        });
    }

    drawHexOverlay(width, height) {
        this.hexagons.forEach(hex => {
            hex.pulse += 0.015;
            const pulse = Math.sin(hex.pulse) * 0.3 + 0.7;

            this.ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i - Math.PI / 6;
                const x = hex.x + hex.size * Math.cos(angle);
                const y = hex.y + hex.size * Math.sin(angle);
                if (i === 0) this.ctx.moveTo(x, y);
                else this.ctx.lineTo(x, y);
            }
            this.ctx.closePath();
            this.ctx.strokeStyle = `rgba(0, 255, 65, ${0.05 * pulse})`;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
        });
    }

    drawPulseWaves(width, height) {
        // Create new pulse waves periodically
        if (Math.random() < 0.01) {
            this.pulseWaves.push({
                x: width / 2 + (Math.random() - 0.5) * 300,
                y: height / 2 + (Math.random() - 0.5) * 200,
                radius: 0,
                maxRadius: 150 + Math.random() * 100,
                opacity: 0.3
            });
        }

        // Update and draw pulse waves
        this.pulseWaves = this.pulseWaves.filter(wave => {
            wave.radius += 2;
            wave.opacity *= 0.98;

            if (wave.radius > wave.maxRadius || wave.opacity < 0.01) {
                return false;
            }

            this.ctx.beginPath();
            this.ctx.arc(wave.x, wave.y, wave.radius, 0, Math.PI * 2);
            this.ctx.strokeStyle = `rgba(0, 255, 65, ${wave.opacity})`;
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            return true;
        });
    }

    drawVignette(width, height) {
        const gradient = this.ctx.createRadialGradient(
            width / 2, height / 2, height * 0.3,
            width / 2, height / 2, height
        );
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.7)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
    }

    cleanup() {
        this.gridLines = [];
        this.dataStreams = [];
        this.codeBlocks = [];
        this.circuitNodes = [];
        this.hexagons = [];
        this.pulseWaves = [];
    }
}

// ============================================
// THEME 2: LUXURY AURORA (Cinematic)
// Elegant, premium flowing gradients
// ============================================

class LuxuryAuroraEffect {
    constructor(manager) {
        this.manager = manager;
        this.ctx = manager.ctx;
        this.canvas = manager.canvas;
        this.time = 0;
        this.layers = [];
        this.particles = [];
        // New effects
        this.lensFlares = [];
        this.silkThreads = [];
        this.diamonds = [];
        this.ripples = [];
    }

    start() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create flowing aurora layers
        this.layers = [];
        for (let i = 0; i < 5; i++) {
            this.layers.push({
                offset: i * 0.5,
                amplitude: 30 + i * 20,
                frequency: 0.002 - i * 0.0003,
                speed: 0.3 + i * 0.1,
                opacity: 0.15 - i * 0.02
            });
        }

        // Create floating dust particles
        this.particles = [];
        for (let i = 0; i < 60; i++) {
            this.particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                size: 0.5 + Math.random() * 2,
                speedX: (Math.random() - 0.5) * 0.3,
                speedY: -0.1 - Math.random() * 0.3,
                opacity: Math.random() * 0.6,
                twinkle: Math.random() * Math.PI * 2
            });
        }

        // Create lens flares
        this.lensFlares = [];
        for (let i = 0; i < 3; i++) {
            this.lensFlares.push({
                x: width * (0.3 + i * 0.2),
                y: height * (0.2 + Math.random() * 0.3),
                size: 30 + Math.random() * 40,
                phase: Math.random() * Math.PI * 2,
                speed: 0.02 + Math.random() * 0.02
            });
        }

        // Create silk threads (curves connecting particles)
        this.silkThreads = [];
        for (let i = 0; i < 6; i++) {
            this.silkThreads.push({
                startX: Math.random() * width,
                startY: height + 50,
                controlX: Math.random() * width,
                controlY: height * 0.3 + Math.random() * height * 0.4,
                endX: Math.random() * width,
                endY: -50,
                phase: Math.random() * Math.PI * 2,
                opacity: 0.1 + Math.random() * 0.15
            });
        }

        // Create floating diamonds
        this.diamonds = [];
        for (let i = 0; i < 12; i++) {
            this.diamonds.push({
                x: Math.random() * width,
                y: Math.random() * height,
                size: 3 + Math.random() * 5,
                rotation: Math.random() * Math.PI * 2,
                rotSpeed: 0.01 + Math.random() * 0.02,
                speedY: -0.2 - Math.random() * 0.3,
                opacity: 0.3 + Math.random() * 0.3
            });
        }

        // Create ripple effects
        this.ripples = [];

        this.manager.animate();
    }

    update() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        this.time += 0.008;

        // Deep black background
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, width, height);

        // Draw silk threads (background layer)
        this.drawSilkThreads(width, height);

        // Draw aurora layers
        this.drawAurora(width, height);

        // Draw floating diamonds
        this.drawDiamonds(width, height);

        // Draw floating particles
        this.drawParticles(width, height);

        // Draw lens flares
        this.drawLensFlares(width, height);

        // Draw ripples
        this.drawRipples(width, height);

        // Subtle light beam from top
        this.drawLightBeam(width, height);

        // Golden vignette
        this.drawVignette(width, height);
    }

    drawAurora(width, height) {
        this.layers.forEach((layer, index) => {
            this.ctx.beginPath();
            this.ctx.moveTo(0, height);

            // Create flowing wave
            for (let x = 0; x <= width; x += 5) {
                const wave1 = Math.sin(x * layer.frequency + this.time * layer.speed + layer.offset) * layer.amplitude;
                const wave2 = Math.sin(x * layer.frequency * 0.5 + this.time * layer.speed * 0.7) * layer.amplitude * 0.5;
                const y = height * 0.4 + wave1 + wave2 + index * 40;

                if (x === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
            }

            this.ctx.lineTo(width, height);
            this.ctx.lineTo(0, height);
            this.ctx.closePath();

            // Golden gradient
            const gradient = this.ctx.createLinearGradient(0, height * 0.3, 0, height);
            gradient.addColorStop(0, `rgba(212, 175, 55, ${layer.opacity})`);
            gradient.addColorStop(0.3, `rgba(180, 140, 40, ${layer.opacity * 0.7})`);
            gradient.addColorStop(0.7, `rgba(139, 90, 43, ${layer.opacity * 0.3})`);
            gradient.addColorStop(1, 'rgba(10, 10, 10, 0)');

            this.ctx.fillStyle = gradient;
            this.ctx.fill();
        });
    }

    drawParticles(width, height) {
        this.particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            p.twinkle += 0.02;

            // Wrap around
            if (p.y < -10) {
                p.y = height + 10;
                p.x = Math.random() * width;
            }
            if (p.x < -10) p.x = width + 10;
            if (p.x > width + 10) p.x = -10;

            const twinkleFactor = 0.5 + Math.sin(p.twinkle) * 0.5;
            const alpha = p.opacity * twinkleFactor;

            // Soft glow
            const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 4);
            gradient.addColorStop(0, `rgba(255, 223, 150, ${alpha})`);
            gradient.addColorStop(0.5, `rgba(212, 175, 55, ${alpha * 0.3})`);
            gradient.addColorStop(1, 'rgba(212, 175, 55, 0)');

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size * 4, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();
        });
    }

    drawLightBeam(width, height) {
        const beamX = width * 0.7 + Math.sin(this.time * 0.5) * 100;

        const gradient = this.ctx.createLinearGradient(beamX - 200, 0, beamX + 200, 0);
        gradient.addColorStop(0, 'rgba(212, 175, 55, 0)');
        gradient.addColorStop(0.3, 'rgba(212, 175, 55, 0.03)');
        gradient.addColorStop(0.5, 'rgba(255, 223, 186, 0.05)');
        gradient.addColorStop(0.7, 'rgba(212, 175, 55, 0.03)');
        gradient.addColorStop(1, 'rgba(212, 175, 55, 0)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(beamX - 200, 0, 400, height);
    }

    drawLensFlares(width, height) {
        this.lensFlares.forEach(flare => {
            flare.phase += flare.speed;
            const pulse = 0.5 + Math.sin(flare.phase) * 0.3;
            const size = flare.size * pulse;

            // Main flare glow
            const gradient = this.ctx.createRadialGradient(flare.x, flare.y, 0, flare.x, flare.y, size);
            gradient.addColorStop(0, `rgba(255, 235, 180, ${0.15 * pulse})`);
            gradient.addColorStop(0.3, `rgba(212, 175, 55, ${0.08 * pulse})`);
            gradient.addColorStop(0.6, `rgba(180, 140, 40, ${0.03 * pulse})`);
            gradient.addColorStop(1, 'rgba(180, 140, 40, 0)');

            this.ctx.beginPath();
            this.ctx.arc(flare.x, flare.y, size, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Starburst rays
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i + this.time * 0.2;
                const rayLength = size * 0.8;

                this.ctx.beginPath();
                this.ctx.moveTo(flare.x, flare.y);
                this.ctx.lineTo(
                    flare.x + Math.cos(angle) * rayLength,
                    flare.y + Math.sin(angle) * rayLength
                );
                this.ctx.strokeStyle = `rgba(255, 223, 150, ${0.1 * pulse})`;
                this.ctx.lineWidth = 1;
                this.ctx.stroke();
            }
        });
    }

    drawSilkThreads(width, height) {
        this.silkThreads.forEach(thread => {
            thread.phase += 0.01;
            const sway = Math.sin(thread.phase) * 30;

            this.ctx.beginPath();
            this.ctx.moveTo(thread.startX + sway, thread.startY);
            this.ctx.quadraticCurveTo(
                thread.controlX + sway * 2,
                thread.controlY,
                thread.endX - sway,
                thread.endY
            );

            const gradient = this.ctx.createLinearGradient(
                thread.startX, thread.startY,
                thread.endX, thread.endY
            );
            gradient.addColorStop(0, 'rgba(212, 175, 55, 0)');
            gradient.addColorStop(0.3, `rgba(212, 175, 55, ${thread.opacity})`);
            gradient.addColorStop(0.7, `rgba(255, 223, 150, ${thread.opacity * 1.2})`);
            gradient.addColorStop(1, 'rgba(212, 175, 55, 0)');

            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
        });
    }

    drawDiamonds(width, height) {
        this.diamonds.forEach(d => {
            d.y += d.speedY;
            d.rotation += d.rotSpeed;

            // Wrap around
            if (d.y < -20) {
                d.y = height + 20;
                d.x = Math.random() * width;
            }

            this.ctx.save();
            this.ctx.translate(d.x, d.y);
            this.ctx.rotate(d.rotation);

            // Diamond shape
            this.ctx.beginPath();
            this.ctx.moveTo(0, -d.size);
            this.ctx.lineTo(d.size * 0.6, 0);
            this.ctx.lineTo(0, d.size);
            this.ctx.lineTo(-d.size * 0.6, 0);
            this.ctx.closePath();

            // Fill with gradient
            const gradient = this.ctx.createRadialGradient(0, 0, 0, 0, 0, d.size);
            gradient.addColorStop(0, `rgba(255, 235, 180, ${d.opacity})`);
            gradient.addColorStop(1, `rgba(212, 175, 55, ${d.opacity * 0.3})`);

            this.ctx.fillStyle = gradient;
            this.ctx.fill();
            this.ctx.strokeStyle = `rgba(255, 223, 150, ${d.opacity * 0.5})`;
            this.ctx.lineWidth = 0.5;
            this.ctx.stroke();

            this.ctx.restore();
        });
    }

    drawRipples(width, height) {
        // Create ripples on mouse movement
        if (Math.random() < 0.02) {
            this.ripples.push({
                x: this.manager.mouseX + (Math.random() - 0.5) * 100,
                y: this.manager.mouseY + (Math.random() - 0.5) * 100,
                radius: 0,
                maxRadius: 80 + Math.random() * 60,
                opacity: 0.2
            });
        }

        // Update and draw ripples
        this.ripples = this.ripples.filter(ripple => {
            ripple.radius += 1;
            ripple.opacity *= 0.97;

            if (ripple.radius > ripple.maxRadius || ripple.opacity < 0.01) {
                return false;
            }

            this.ctx.beginPath();
            this.ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
            this.ctx.strokeStyle = `rgba(212, 175, 55, ${ripple.opacity})`;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();

            return true;
        });
    }

    drawVignette(width, height) {
        // Dark edges vignette
        const gradient = this.ctx.createRadialGradient(
            width / 2, height / 2, height * 0.4,
            width / 2, height / 2, height
        );
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(0.7, 'rgba(0, 0, 0, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.8)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
    }

    cleanup() {
        this.layers = [];
        this.particles = [];
        this.lensFlares = [];
        this.silkThreads = [];
        this.diamonds = [];
        this.ripples = [];
    }
}

// ============================================
// THEME 3: AEROSPACE COMMAND (Scientific)
// Multi-layered data visualization with radar, circuits, hexagons
// ============================================

class NeuralNetworkEffect {
    constructor(manager) {
        this.manager = manager;
        this.ctx = manager.ctx;
        this.canvas = manager.canvas;
        this.time = 0;
        this.radarAngle = 0;
        this.hexagons = [];
        this.circuits = [];
        this.floatingData = [];
        this.orbitRings = [];
        this.scanLines = [];
    }

    start() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create hexagonal grid points
        this.hexagons = [];
        const hexSize = 60;
        const hexHeight = hexSize * Math.sqrt(3);
        for (let row = -1; row < height / hexHeight + 1; row++) {
            for (let col = -1; col < width / (hexSize * 1.5) + 1; col++) {
                const x = col * hexSize * 1.5;
                const y = row * hexHeight + (col % 2) * hexHeight / 2;
                this.hexagons.push({
                    x, y,
                    size: hexSize * 0.4,
                    pulse: Math.random() * Math.PI * 2,
                    active: Math.random() < 0.15
                });
            }
        }

        // Create circuit traces
        this.circuits = [];
        for (let i = 0; i < 12; i++) {
            const isHorizontal = Math.random() < 0.5;
            this.circuits.push({
                x: Math.random() * width,
                y: Math.random() * height,
                length: 100 + Math.random() * 200,
                speed: 1 + Math.random() * 2,
                progress: Math.random(),
                horizontal: isHorizontal
            });
        }

        // Create floating data particles
        this.floatingData = [];
        for (let i = 0; i < 40; i++) {
            this.floatingData.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: -0.3 - Math.random() * 0.5,
                size: 2 + Math.random() * 3,
                type: Math.floor(Math.random() * 3), // 0: circle, 1: square, 2: diamond
                alpha: 0.4 + Math.random() * 0.4
            });
        }

        // Create orbital rings
        this.orbitRings = [];
        for (let i = 0; i < 3; i++) {
            this.orbitRings.push({
                centerX: width * (0.2 + i * 0.3),
                centerY: height * (0.3 + Math.random() * 0.4),
                radius: 80 + i * 40,
                rotation: Math.random() * Math.PI * 2,
                rotationSpeed: 0.005 + Math.random() * 0.01,
                satellites: Math.floor(3 + Math.random() * 4)
            });
        }

        // Create horizontal scan lines
        this.scanLines = [];
        for (let i = 0; i < 3; i++) {
            this.scanLines.push({
                y: Math.random() * height,
                speed: 0.5 + Math.random() * 1,
                width: 2 + Math.random() * 3
            });
        }

        this.manager.animate();
    }

    update() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        this.time += 0.016;
        this.radarAngle += 0.015;

        // Light gradient background
        const bgGradient = this.ctx.createLinearGradient(0, 0, 0, height);
        bgGradient.addColorStop(0, '#e8ecf1');
        bgGradient.addColorStop(1, '#d5dce5');
        this.ctx.fillStyle = bgGradient;
        this.ctx.fillRect(0, 0, width, height);

        // Draw layers
        this.drawHexGrid(width, height);
        this.drawCircuitTraces(width, height);
        this.drawOrbitRings(width, height);
        this.drawRadarSweep(width, height);
        this.drawFloatingData(width, height);
        this.drawScanLines(width, height);
        this.drawDataOverlay(width, height);
        this.drawVignette(width, height);
    }

    drawHexGrid(width, height) {
        this.hexagons.forEach(hex => {
            hex.pulse += 0.02;
            const pulse = hex.active ? (0.5 + Math.sin(hex.pulse) * 0.3) : 0.15;

            this.ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i - Math.PI / 6;
                const x = hex.x + hex.size * Math.cos(angle);
                const y = hex.y + hex.size * Math.sin(angle);
                if (i === 0) this.ctx.moveTo(x, y);
                else this.ctx.lineTo(x, y);
            }
            this.ctx.closePath();
            this.ctx.strokeStyle = `rgba(30, 58, 95, ${pulse * 0.3})`;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();

            if (hex.active) {
                this.ctx.fillStyle = `rgba(52, 152, 219, ${pulse * 0.1})`;
                this.ctx.fill();
            }

            // Random activation
            if (Math.random() < 0.001) hex.active = !hex.active;
        });
    }

    drawCircuitTraces(width, height) {
        this.circuits.forEach(circuit => {
            circuit.progress += circuit.speed * 0.01;
            if (circuit.progress > 1) {
                circuit.progress = 0;
                circuit.x = Math.random() * width;
                circuit.y = Math.random() * height;
            }

            const startX = circuit.horizontal ? circuit.x : circuit.x;
            const startY = circuit.horizontal ? circuit.y : circuit.y;
            const endX = circuit.horizontal ? circuit.x + circuit.length : circuit.x;
            const endY = circuit.horizontal ? circuit.y : circuit.y + circuit.length;

            // Draw trace line
            this.ctx.beginPath();
            this.ctx.moveTo(startX, startY);
            this.ctx.lineTo(endX, endY);
            this.ctx.strokeStyle = 'rgba(30, 58, 95, 0.1)';
            this.ctx.lineWidth = 1;
            this.ctx.stroke();

            // Draw moving pulse
            const pulseX = startX + (endX - startX) * circuit.progress;
            const pulseY = startY + (endY - startY) * circuit.progress;

            const gradient = this.ctx.createRadialGradient(pulseX, pulseY, 0, pulseX, pulseY, 15);
            gradient.addColorStop(0, 'rgba(52, 152, 219, 0.8)');
            gradient.addColorStop(0.5, 'rgba(52, 152, 219, 0.3)');
            gradient.addColorStop(1, 'rgba(52, 152, 219, 0)');

            this.ctx.beginPath();
            this.ctx.arc(pulseX, pulseY, 15, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Core
            this.ctx.beginPath();
            this.ctx.arc(pulseX, pulseY, 3, 0, Math.PI * 2);
            this.ctx.fillStyle = 'rgba(52, 152, 219, 1)';
            this.ctx.fill();
        });
    }

    drawOrbitRings(width, height) {
        this.orbitRings.forEach(ring => {
            ring.rotation += ring.rotationSpeed;

            // Draw orbit path
            this.ctx.beginPath();
            this.ctx.arc(ring.centerX, ring.centerY, ring.radius, 0, Math.PI * 2);
            this.ctx.strokeStyle = 'rgba(30, 58, 95, 0.15)';
            this.ctx.lineWidth = 1;
            this.ctx.setLineDash([5, 5]);
            this.ctx.stroke();
            this.ctx.setLineDash([]);

            // Draw satellites
            for (let i = 0; i < ring.satellites; i++) {
                const angle = ring.rotation + (Math.PI * 2 / ring.satellites) * i;
                const x = ring.centerX + ring.radius * Math.cos(angle);
                const y = ring.centerY + ring.radius * Math.sin(angle);

                // Satellite glow
                const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, 10);
                gradient.addColorStop(0, 'rgba(52, 152, 219, 0.6)');
                gradient.addColorStop(1, 'rgba(52, 152, 219, 0)');

                this.ctx.beginPath();
                this.ctx.arc(x, y, 10, 0, Math.PI * 2);
                this.ctx.fillStyle = gradient;
                this.ctx.fill();

                // Satellite core
                this.ctx.beginPath();
                this.ctx.arc(x, y, 4, 0, Math.PI * 2);
                this.ctx.fillStyle = 'rgba(30, 58, 95, 0.8)';
                this.ctx.fill();
            }

            // Draw center
            this.ctx.beginPath();
            this.ctx.arc(ring.centerX, ring.centerY, 6, 0, Math.PI * 2);
            this.ctx.fillStyle = 'rgba(30, 58, 95, 0.3)';
            this.ctx.fill();
        });
    }

    drawRadarSweep(width, height) {
        const centerX = width * 0.85;
        const centerY = height * 0.2;
        const radius = 100;

        // Radar circle
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        this.ctx.strokeStyle = 'rgba(30, 58, 95, 0.2)';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();

        // Radar rings
        for (let i = 1; i <= 3; i++) {
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, radius * (i / 3), 0, Math.PI * 2);
            this.ctx.strokeStyle = 'rgba(30, 58, 95, 0.1)';
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
        }

        // Cross lines
        this.ctx.beginPath();
        this.ctx.moveTo(centerX - radius, centerY);
        this.ctx.lineTo(centerX + radius, centerY);
        this.ctx.moveTo(centerX, centerY - radius);
        this.ctx.lineTo(centerX, centerY + radius);
        this.ctx.strokeStyle = 'rgba(30, 58, 95, 0.1)';
        this.ctx.stroke();

        // Radar sweep
        const sweepGradient = this.ctx.createConicalGradient ?
            null :
            this.ctx.createLinearGradient(centerX, centerY, centerX + radius, centerY);

        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY);
        this.ctx.arc(centerX, centerY, radius, this.radarAngle - 0.5, this.radarAngle, false);
        this.ctx.closePath();

        const gradient = this.ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
        gradient.addColorStop(0, 'rgba(52, 152, 219, 0.3)');
        gradient.addColorStop(1, 'rgba(52, 152, 219, 0.05)');
        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // Sweep line
        const endX = centerX + Math.cos(this.radarAngle) * radius;
        const endY = centerY + Math.sin(this.radarAngle) * radius;

        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY);
        this.ctx.lineTo(endX, endY);
        this.ctx.strokeStyle = 'rgba(52, 152, 219, 0.8)';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();

        // Center dot
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 4, 0, Math.PI * 2);
        this.ctx.fillStyle = 'rgba(52, 152, 219, 1)';
        this.ctx.fill();
    }

    drawFloatingData(width, height) {
        this.floatingData.forEach(data => {
            data.x += data.vx;
            data.y += data.vy;

            // Wrap around
            if (data.y < -20) {
                data.y = height + 20;
                data.x = Math.random() * width;
            }
            if (data.x < -20) data.x = width + 20;
            if (data.x > width + 20) data.x = -20;

            this.ctx.fillStyle = `rgba(30, 58, 95, ${data.alpha})`;

            if (data.type === 0) {
                // Circle
                this.ctx.beginPath();
                this.ctx.arc(data.x, data.y, data.size, 0, Math.PI * 2);
                this.ctx.fill();
            } else if (data.type === 1) {
                // Square
                this.ctx.fillRect(data.x - data.size, data.y - data.size, data.size * 2, data.size * 2);
            } else {
                // Diamond
                this.ctx.beginPath();
                this.ctx.moveTo(data.x, data.y - data.size);
                this.ctx.lineTo(data.x + data.size, data.y);
                this.ctx.lineTo(data.x, data.y + data.size);
                this.ctx.lineTo(data.x - data.size, data.y);
                this.ctx.closePath();
                this.ctx.fill();
            }
        });
    }

    drawScanLines(width, height) {
        this.scanLines.forEach(line => {
            line.y += line.speed;
            if (line.y > height) line.y = -10;

            const gradient = this.ctx.createLinearGradient(0, line.y - 20, 0, line.y + 20);
            gradient.addColorStop(0, 'rgba(52, 152, 219, 0)');
            gradient.addColorStop(0.5, 'rgba(52, 152, 219, 0.15)');
            gradient.addColorStop(1, 'rgba(52, 152, 219, 0)');

            this.ctx.fillStyle = gradient;
            this.ctx.fillRect(0, line.y - 20, width, 40);
        });
    }

    drawDataOverlay(width, height) {
        // Top-left corner data display
        this.ctx.fillStyle = 'rgba(30, 58, 95, 0.6)';
        this.ctx.font = '10px "IBM Plex Mono", monospace';

        const data = [
            `SYS.TIME: ${new Date().toLocaleTimeString()}`,
            `NODES: ${this.hexagons.filter(h => h.active).length}/${this.hexagons.length}`,
            `SCAN: ${Math.floor(this.radarAngle * 180 / Math.PI) % 360}°`
        ];

        data.forEach((text, i) => {
            this.ctx.fillText(text, 20, 30 + i * 15);
        });
    }

    drawVignette(width, height) {
        const gradient = this.ctx.createRadialGradient(
            width / 2, height / 2, height * 0.4,
            width / 2, height / 2, height
        );
        gradient.addColorStop(0, 'rgba(245, 245, 245, 0)');
        gradient.addColorStop(1, 'rgba(200, 210, 220, 0.4)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
    }

    cleanup() {
        this.hexagons = [];
        this.circuits = [];
        this.floatingData = [];
        this.orbitRings = [];
        this.scanLines = [];
    }
}

// ============================================
// THEME 4: NEON FLUX (Chaos)
// Sophisticated neon aesthetic with cohesive palette
// ============================================

class PlasmaVortexEffect {
    constructor(manager) {
        this.manager = manager;
        this.ctx = manager.ctx;
        this.canvas = manager.canvas;
        this.time = 0;
        this.particles = [];
        this.flowLines = [];
        // New effects
        this.energyRings = [];
        this.lightningArcs = [];
        this.geometricShapes = [];
        this.neonScanlines = [];
        // Cohesive neon palette: magenta, cyan, purple, pink
        this.colors = [
            { r: 255, g: 0, b: 128 },   // Hot pink/magenta
            { r: 0, g: 255, b: 255 },   // Cyan
            { r: 138, g: 43, b: 226 },  // Purple
            { r: 255, g: 20, b: 147 },  // Deep pink
            { r: 75, g: 0, b: 130 }     // Indigo
        ];
    }

    start() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create elegant flowing particles
        this.particles = [];
        for (let i = 0; i < 100; i++) {
            this.particles.push(this.createParticle(width, height));
        }

        // Create background flow lines
        this.flowLines = [];
        for (let i = 0; i < 8; i++) {
            this.flowLines.push({
                points: [],
                colorIndex: i % this.colors.length,
                speed: 0.5 + Math.random() * 0.5,
                amplitude: 50 + Math.random() * 100,
                frequency: 0.002 + Math.random() * 0.003,
                yOffset: (height / 8) * i + Math.random() * 50
            });
        }

        // Create energy rings
        this.energyRings = [];
        for (let i = 0; i < 3; i++) {
            this.energyRings.push({
                x: width * (0.2 + i * 0.3),
                y: height * (0.3 + Math.random() * 0.4),
                radius: 60 + Math.random() * 80,
                phase: Math.random() * Math.PI * 2,
                colorIndex: i % this.colors.length,
                rotationSpeed: 0.01 + Math.random() * 0.02
            });
        }

        // Create lightning arcs
        this.lightningArcs = [];

        // Create geometric shapes (triangles, hexagons)
        this.geometricShapes = [];
        for (let i = 0; i < 8; i++) {
            this.geometricShapes.push({
                x: Math.random() * width,
                y: Math.random() * height,
                size: 20 + Math.random() * 30,
                sides: Math.random() < 0.5 ? 3 : 6,
                rotation: Math.random() * Math.PI * 2,
                rotSpeed: 0.005 + Math.random() * 0.01,
                colorIndex: Math.floor(Math.random() * this.colors.length),
                opacity: 0.2 + Math.random() * 0.2,
                driftX: (Math.random() - 0.5) * 0.3,
                driftY: (Math.random() - 0.5) * 0.3
            });
        }

        // Create neon scanlines
        this.neonScanlines = [];
        for (let i = 0; i < 3; i++) {
            this.neonScanlines.push({
                y: Math.random() * height,
                speed: 1 + Math.random() * 2,
                colorIndex: Math.floor(Math.random() * this.colors.length),
                width: 2 + Math.random() * 3
            });
        }

        this.manager.animate();
    }

    createParticle(width, height) {
        const colorIndex = Math.floor(Math.random() * this.colors.length);
        return {
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5,
            size: 1.5 + Math.random() * 2.5,
            colorIndex: colorIndex,
            alpha: 0.6 + Math.random() * 0.4,
            trail: []
        };
    }

    update() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        this.time += 0.012;

        // Dark background with subtle trail
        this.ctx.fillStyle = 'rgba(8, 8, 15, 0.12)';
        this.ctx.fillRect(0, 0, width, height);

        // Draw geometric shapes (background)
        this.drawGeometricShapes(width, height);

        // Draw flowing background waves
        this.drawFlowingWaves(width, height);

        // Draw energy rings
        this.drawEnergyRings(width, height);

        // Update and draw particles
        this.updateParticles(width, height);

        // Draw lightning arcs
        this.drawLightningArcs(width, height);

        // Draw neon scanlines
        this.drawNeonScanlines(width, height);

        // Draw ambient glow
        this.drawAmbientGlow(width, height);

        // Vignette
        this.drawVignette(width, height);
    }

    drawFlowingWaves(width, height) {
        this.flowLines.forEach((line, lineIndex) => {
            const color = this.colors[line.colorIndex];

            this.ctx.beginPath();

            for (let x = 0; x <= width; x += 3) {
                const wave1 = Math.sin(x * line.frequency + this.time * line.speed) * line.amplitude;
                const wave2 = Math.sin(x * line.frequency * 1.5 + this.time * line.speed * 0.7) * line.amplitude * 0.3;
                const y = line.yOffset + wave1 + wave2;

                if (x === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
            }

            // Create gradient stroke
            const gradient = this.ctx.createLinearGradient(0, 0, width, 0);
            gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, 0)`);
            gradient.addColorStop(0.3, `rgba(${color.r}, ${color.g}, ${color.b}, 0.15)`);
            gradient.addColorStop(0.5, `rgba(${color.r}, ${color.g}, ${color.b}, 0.25)`);
            gradient.addColorStop(0.7, `rgba(${color.r}, ${color.g}, ${color.b}, 0.15)`);
            gradient.addColorStop(1, `rgba(${color.r}, ${color.g}, ${color.b}, 0)`);

            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 2;
            this.ctx.stroke();
        });
    }

    updateParticles(width, height) {
        this.particles.forEach(p => {
            // Store trail
            p.trail.push({ x: p.x, y: p.y });
            if (p.trail.length > 12) p.trail.shift();

            // Mouse interaction - gentle attraction
            const dx = this.manager.mouseX - p.x;
            const dy = this.manager.mouseY - p.y;
            const dist = Math.hypot(dx, dy);

            if (dist < 200 && dist > 20) {
                const force = (200 - dist) / 200 * 0.3;
                p.vx += (dx / dist) * force * 0.1;
                p.vy += (dy / dist) * force * 0.1;
            }

            // Apply velocity with flow field influence
            const flowAngle = Math.sin(p.x * 0.005 + this.time) * Math.PI * 0.5;
            p.vx += Math.cos(flowAngle) * 0.02;
            p.vy += Math.sin(flowAngle) * 0.02;

            p.x += p.vx;
            p.y += p.vy;

            // Damping
            p.vx *= 0.97;
            p.vy *= 0.97;

            // Bounds with wrap
            if (p.x < -20) p.x = width + 20;
            if (p.x > width + 20) p.x = -20;
            if (p.y < -20) p.y = height + 20;
            if (p.y > height + 20) p.y = -20;

            const color = this.colors[p.colorIndex];

            // Draw trail
            if (p.trail.length > 2) {
                this.ctx.beginPath();
                this.ctx.moveTo(p.trail[0].x, p.trail[0].y);

                for (let i = 1; i < p.trail.length; i++) {
                    this.ctx.lineTo(p.trail[i].x, p.trail[i].y);
                }

                const trailAlpha = p.alpha * 0.4;
                this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${trailAlpha})`;
                this.ctx.lineWidth = p.size * 0.6;
                this.ctx.lineCap = 'round';
                this.ctx.stroke();
            }

            // Draw particle with glow
            const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 4);
            gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, ${p.alpha})`);
            gradient.addColorStop(0.4, `rgba(${color.r}, ${color.g}, ${color.b}, ${p.alpha * 0.4})`);
            gradient.addColorStop(1, `rgba(${color.r}, ${color.g}, ${color.b}, 0)`);

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size * 4, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Bright core
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size * 0.8, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha * 0.8})`;
            this.ctx.fill();
        });
    }

    drawAmbientGlow(width, height) {
        // Corner glows
        const glows = [
            { x: 0, y: 0, colorIndex: 0 },
            { x: width, y: 0, colorIndex: 1 },
            { x: 0, y: height, colorIndex: 2 },
            { x: width, y: height, colorIndex: 3 }
        ];

        glows.forEach(glow => {
            const color = this.colors[glow.colorIndex];
            const pulse = 0.5 + Math.sin(this.time * 2 + glow.colorIndex) * 0.3;

            const gradient = this.ctx.createRadialGradient(
                glow.x, glow.y, 0,
                glow.x, glow.y, height * 0.6
            );
            gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, ${0.08 * pulse})`);
            gradient.addColorStop(0.5, `rgba(${color.r}, ${color.g}, ${color.b}, ${0.03 * pulse})`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

            this.ctx.fillStyle = gradient;
            this.ctx.fillRect(0, 0, width, height);
        });
    }

    drawEnergyRings(width, height) {
        this.energyRings.forEach(ring => {
            ring.phase += ring.rotationSpeed;
            const color = this.colors[ring.colorIndex];
            const pulse = 0.6 + Math.sin(ring.phase * 3) * 0.3;

            // Multiple concentric rings
            for (let i = 0; i < 3; i++) {
                const r = ring.radius * (0.6 + i * 0.25);
                const alpha = (0.15 - i * 0.04) * pulse;

                this.ctx.beginPath();
                this.ctx.arc(ring.x, ring.y, r, 0, Math.PI * 2);
                this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${alpha})`;
                this.ctx.lineWidth = 2;
                this.ctx.stroke();
            }

            // Rotating segments
            for (let i = 0; i < 4; i++) {
                const startAngle = ring.phase + (Math.PI / 2) * i;
                const endAngle = startAngle + Math.PI / 4;

                this.ctx.beginPath();
                this.ctx.arc(ring.x, ring.y, ring.radius, startAngle, endAngle);
                this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${0.4 * pulse})`;
                this.ctx.lineWidth = 3;
                this.ctx.stroke();
            }

            // Center glow
            const gradient = this.ctx.createRadialGradient(ring.x, ring.y, 0, ring.x, ring.y, ring.radius * 0.3);
            gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, ${0.2 * pulse})`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            this.ctx.beginPath();
            this.ctx.arc(ring.x, ring.y, ring.radius * 0.3, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();
        });
    }

    drawLightningArcs(width, height) {
        // Randomly create new lightning
        if (Math.random() < 0.02) {
            const colorIndex = Math.floor(Math.random() * this.colors.length);
            this.lightningArcs.push({
                startX: Math.random() * width,
                startY: Math.random() * height * 0.3,
                endX: Math.random() * width,
                endY: height * 0.5 + Math.random() * height * 0.5,
                colorIndex: colorIndex,
                life: 1.0,
                segments: Math.floor(5 + Math.random() * 5)
            });
        }

        // Draw and update lightning
        this.lightningArcs = this.lightningArcs.filter(arc => {
            arc.life -= 0.08;
            if (arc.life <= 0) return false;

            const color = this.colors[arc.colorIndex];
            this.ctx.beginPath();
            this.ctx.moveTo(arc.startX, arc.startY);

            // Create jagged lightning path
            let currentX = arc.startX;
            let currentY = arc.startY;
            const dx = (arc.endX - arc.startX) / arc.segments;
            const dy = (arc.endY - arc.startY) / arc.segments;

            for (let i = 1; i < arc.segments; i++) {
                const offsetX = (Math.random() - 0.5) * 60;
                const offsetY = (Math.random() - 0.5) * 20;
                currentX += dx + offsetX;
                currentY += dy + offsetY;
                this.ctx.lineTo(currentX, currentY);
            }
            this.ctx.lineTo(arc.endX, arc.endY);

            // Glow effect
            this.ctx.shadowColor = `rgb(${color.r}, ${color.g}, ${color.b})`;
            this.ctx.shadowBlur = 15;
            this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${arc.life * 0.6})`;
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            // Brighter core
            this.ctx.strokeStyle = `rgba(255, 255, 255, ${arc.life * 0.4})`;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();

            this.ctx.shadowBlur = 0;

            return true;
        });
    }

    drawGeometricShapes(width, height) {
        this.geometricShapes.forEach(shape => {
            shape.rotation += shape.rotSpeed;
            shape.x += shape.driftX;
            shape.y += shape.driftY;

            // Wrap around
            if (shape.x < -50) shape.x = width + 50;
            if (shape.x > width + 50) shape.x = -50;
            if (shape.y < -50) shape.y = height + 50;
            if (shape.y > height + 50) shape.y = -50;

            const color = this.colors[shape.colorIndex];

            this.ctx.save();
            this.ctx.translate(shape.x, shape.y);
            this.ctx.rotate(shape.rotation);

            this.ctx.beginPath();
            for (let i = 0; i < shape.sides; i++) {
                const angle = (Math.PI * 2 / shape.sides) * i - Math.PI / 2;
                const x = shape.size * Math.cos(angle);
                const y = shape.size * Math.sin(angle);
                if (i === 0) this.ctx.moveTo(x, y);
                else this.ctx.lineTo(x, y);
            }
            this.ctx.closePath();

            this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${shape.opacity})`;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();

            this.ctx.restore();
        });
    }

    drawNeonScanlines(width, height) {
        this.neonScanlines.forEach(line => {
            line.y += line.speed;
            if (line.y > height + 50) {
                line.y = -50;
                line.colorIndex = Math.floor(Math.random() * this.colors.length);
            }

            const color = this.colors[line.colorIndex];

            const gradient = this.ctx.createLinearGradient(0, line.y - 30, 0, line.y + 30);
            gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
            gradient.addColorStop(0.5, `rgba(${color.r}, ${color.g}, ${color.b}, 0.15)`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

            this.ctx.fillStyle = gradient;
            this.ctx.fillRect(0, line.y - 30, width, 60);

            // Bright center line
            this.ctx.beginPath();
            this.ctx.moveTo(0, line.y);
            this.ctx.lineTo(width, line.y);
            this.ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.3)`;
            this.ctx.lineWidth = line.width;
            this.ctx.stroke();
        });
    }

    drawVignette(width, height) {
        const gradient = this.ctx.createRadialGradient(
            width / 2, height / 2, height * 0.35,
            width / 2, height / 2, height
        );
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(0.7, 'rgba(8, 8, 15, 0.3)');
        gradient.addColorStop(1, 'rgba(8, 8, 15, 0.7)');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
    }

    cleanup() {
        this.particles = [];
        this.flowLines = [];
        this.energyRings = [];
        this.lightningArcs = [];
        this.geometricShapes = [];
        this.neonScanlines = [];
    }
}

// ============================================
// GLOBAL INITIALIZATION
// ============================================

let themeEffectsManager = null;

function initThemeEffects() {
    themeEffectsManager = new ThemeEffectsManager();
    const currentTheme = document.body.getAttribute('data-theme') || 'brutalist';
    themeEffectsManager.switchTheme(currentTheme);
}

window.ThemeEffectsManager = ThemeEffectsManager;
window.initThemeEffects = initThemeEffects;
window.switchThemeEffect = (themeName) => {
    if (themeEffectsManager) {
        themeEffectsManager.switchTheme(themeName);
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeEffects);
} else {
    initThemeEffects();
}
