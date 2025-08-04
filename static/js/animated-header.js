// Animated Header JavaScript

class AnimatedHeader {
    constructor() {
        this.particleContainer = document.querySelector('.particle-container');
        this.waveContainer = document.querySelector('.wave-container');
        this.initParticles();
        this.initWave();
    }

    // Initialize particles
    initParticles() {
        const numParticles = 30;
        for (let i = 0; i < numParticles; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            this.setupParticle(particle);
            this.particleContainer.appendChild(particle);
        }
    }

    // Setup individual particle
    setupParticle(particle) {
        const size = Math.random() * 5 + 2;
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        
        // Add color variation
        const hue = Math.random() * 360;
        particle.style.background = `hsla(${hue}, 100%, 50%, 0.8)`;
    }

    // Initialize wave effect
    initWave() {
        const wave = document.createElement('div');
        wave.className = 'wave';
        this.waveContainer.appendChild(wave);
        
        // Create multiple wave layers
        for (let i = 0; i < 3; i++) {
            const waveLayer = document.createElement('div');
            waveLayer.className = 'wave';
            waveLayer.style.animationDelay = `${i * 0.2}s`;
            waveLayer.style.background = `rgba(${i * 50}, ${255 - i * 50}, 255, 0.2)`;
            this.waveContainer.appendChild(waveLayer);
        }
    }

    // Update particle positions
    updateParticles() {
        const particles = document.querySelectorAll('.particle');
        particles.forEach(particle => {
            const rect = particle.getBoundingClientRect();
            const x = rect.left;
            const y = rect.top;
            
            // Add random movement
            const newX = x + (Math.random() - 0.5) * 10;
            const newY = y + (Math.random() - 0.5) * 10;
            
            particle.style.left = `${newX}px`;
            particle.style.top = `${newY}px`;
        });
    }

    // Handle window resize
    handleResize() {
        this.particleContainer.style.width = `${window.innerWidth}px`;
        this.particleContainer.style.height = `${window.innerHeight}px`;
    }

    // Start animation
    startAnimation() {
        this.updateParticles();
        requestAnimationFrame(() => this.startAnimation());
    }
}

// Initialize animated header
window.addEventListener('DOMContentLoaded', () => {
    const animatedHeader = new AnimatedHeader();
    animatedHeader.startAnimation();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        animatedHeader.handleResize();
    });
});
