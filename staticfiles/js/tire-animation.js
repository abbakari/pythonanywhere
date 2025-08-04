// Tire Animation Script
const tireContainer = document.querySelector('.tire-container');
const tire = document.querySelector('.tire');

// Constants for animation
const ANIMATION_SPEED = 100; // pixels per second
const WINDOW_WIDTH = window.innerWidth;
const TIRE_WIDTH = tireContainer.offsetWidth;

// Current position and direction
let currentPosition = 0;
let direction = 1; // 1 for right, -1 for left

// Function to update tire position
function updateTirePosition() {
    // Update position
    currentPosition += direction * (ANIMATION_SPEED / 60); // 60fps
    
    // Check boundaries
    if (currentPosition + TIRE_WIDTH >= WINDOW_WIDTH) {
        currentPosition = WINDOW_WIDTH - TIRE_WIDTH;
        direction = -1;
    } else if (currentPosition <= 0) {
        currentPosition = 0;
        direction = 1;
    }
    
    // Update transform
    tireContainer.style.transform = `translateX(${currentPosition}px)`;
}

// Function to rotate tire
function rotateTire() {
    const rotation = Date.now() / 10; // Rotate 360 degrees every 10 seconds
    tire.style.transform = `rotate(${rotation}deg)`;
}

// Animation loop
function animate() {
    updateTirePosition();
    rotateTire();
    requestAnimationFrame(animate);
}

// Start animation when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tire position
    currentPosition = WINDOW_WIDTH / 2 - TIRE_WIDTH / 2;
    tireContainer.style.transform = `translateX(${currentPosition}px)`;
    
    // Start animation
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        WINDOW_WIDTH = window.innerWidth;
        TIRE_WIDTH = tireContainer.offsetWidth;
        currentPosition = WINDOW_WIDTH / 2 - TIRE_WIDTH / 2;
        tireContainer.style.transform = `translateX(${currentPosition}px)`;
    });
});
