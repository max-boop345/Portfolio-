// ===== Ant Colony Optimization Simulation =====

// Canvas setup
let antsCanvas, antsCtx;

// Simulation parameters
const NUM_ANTS = 25;
const PHEROMONE_EVAPORATION = 0.95;
const PHEROMONE_DEPOSIT = 0.15;
const ANT_SPEED = 2;
const GRID_SIZE = 15;

// World dimensions
let worldWidth = 800;
let worldHeight = 500;

// Nest and food positions
let nest = { x: 100, y: 250 };
let food = { x: 700, y: 250 };

// Pheromone grid
let pheromones = [];

// Ants array
let ants = [];

// Obstacles
let obstacles = [];

// Animation state
let isRunning = true;
let lastTime = 0;

// ===== Ant Class =====
class Ant {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.x = nest.x + (Math.random() - 0.5) * 20;
        this.y = nest.y + (Math.random() - 0.5) * 20;
        this.target = food;
        this.path = [];
        this.carriesFood = false;
        this.direction = Math.random() * Math.PI * 2;
    }
    
    update() {
        // Simple movement: move towards target with some randomness
        const dx = this.target.x - this.x;
        const dy = this.target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 10) {
            // Reached target
            if (this.target === food) {
                this.carriesFood = true;
                this.target = nest;
            } else {
                this.carriesFood = false;
                this.target = food;
            }
            this.path = [];
        } else {
            // Move towards target with some randomness
            const angle = Math.atan2(dy, dx);
            const randomAngle = angle + (Math.random() - 0.5) * 0.5; // Add some randomness
            
            this.x += Math.cos(randomAngle) * ANT_SPEED;
            this.y += Math.sin(randomAngle) * ANT_SPEED;
            
            // Add current position to path
            this.path.push({ x: this.x, y: this.y });
            
            // Limit path length
            if (this.path.length > 30) {
                this.path.shift();
            }
            
            // Deposit pheromones along the path
            if (this.path.length > 0 && Math.random() < 0.15) {
                const pathIndex = Math.floor(Math.random() * this.path.length);
                const pos = this.path[pathIndex];
                const gridX = Math.floor(pos.x / GRID_SIZE);
                const gridY = Math.floor(pos.y / GRID_SIZE);
                
                if (gridX >= 0 && gridX < pheromones.length && gridY >= 0 && gridY < pheromones[0].length) {
                    pheromones[gridX][gridY] += PHEROMONE_DEPOSIT;
                }
            }
        }
        
        // Avoid obstacles
        for (const obs of obstacles) {
            const obsDx = this.x - obs.x;
            const obsDy = this.y - obs.y;
            const obsDistance = Math.sqrt(obsDx * obsDx + obsDy * obsDy);
            
            if (obsDistance < obs.radius + 10) {
                // Push ant away from obstacle
                this.x += (obsDx / obsDistance) * 3;
                this.y += (obsDy / obsDistance) * 3;
            }
        }
        
        // Keep ant within bounds
        this.x = Math.max(0, Math.min(worldWidth, this.x));
        this.y = Math.max(0, Math.min(worldHeight, this.y));
    }
    
    draw() {
        // Draw ant
        antsCtx.fillStyle = this.carriesFood ? '#EF4444' : '#2563EB';
        antsCtx.beginPath();
        antsCtx.arc(this.x, this.y, 5, 0, Math.PI * 2);
        antsCtx.fill();
        
        // Draw path
        if (this.path.length > 1) {
            antsCtx.beginPath();
            antsCtx.moveTo(this.path[0].x, this.path[0].y);
            for (let i = 1; i < this.path.length; i++) {
                antsCtx.lineTo(this.path[i].x, this.path[i].y);
            }
            antsCtx.strokeStyle = this.carriesFood ? '#EF4444' : '#2563EB';
            antsCtx.lineWidth = 1;
            antsCtx.stroke();
        }
    }
}

// ===== Initialize Pheromones =====
function initPheromones() {
    const cols = Math.ceil(worldWidth / GRID_SIZE);
    const rows = Math.ceil(worldHeight / GRID_SIZE);
    
    pheromones = [];
    for (let i = 0; i < cols; i++) {
        pheromones[i] = [];
        for (let j = 0; j < rows; j++) {
            pheromones[i][j] = 0;
        }
    }
}

// ===== Initialize Ants =====
function initAnts() {
    ants = [];
    for (let i = 0; i < NUM_ANTS; i++) {
        ants.push(new Ant());
    }
}

// ===== Initialize Obstacles =====
function initObstacles() {
    obstacles = [
        { x: 400, y: 150, radius: 40 },
        { x: 400, y: 350, radius: 40 }
    ];
}

// ===== Draw Pheromones =====
function drawPheromones() {
    const cols = pheromones.length;
    const rows = pheromones[0] ? pheromones[0].length : 0;
    
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            const value = pheromones[i][j];
            if (value > 0) {
                const alpha = Math.min(value * 0.3, 0.8);
                antsCtx.fillStyle = `rgba(16, 185, 129, ${alpha})`;
                antsCtx.beginPath();
                antsCtx.arc(
                    i * GRID_SIZE + GRID_SIZE / 2,
                    j * GRID_SIZE + GRID_SIZE / 2,
                    GRID_SIZE / 2,
                    0,
                    Math.PI * 2
                );
                antsCtx.fill();
            }
        }
    }
}

// ===== Draw Obstacles =====
function drawObstacles() {
    antsCtx.fillStyle = '#2D3748';
    for (const obs of obstacles) {
        antsCtx.beginPath();
        antsCtx.arc(obs.x, obs.y, obs.radius, 0, Math.PI * 2);
        antsCtx.fill();
        
        // Draw border
        antsCtx.strokeStyle = '#4A5568';
        antsCtx.lineWidth = 2;
        antsCtx.stroke();
    }
}

// ===== Draw Nest and Food =====
function drawNestAndFood() {
    // Nest
    antsCtx.fillStyle = '#4A5568';
    antsCtx.beginPath();
    antsCtx.arc(nest.x, nest.y, 20, 0, Math.PI * 2);
    antsCtx.fill();
    antsCtx.fillStyle = '#FFFFFF';
    antsCtx.font = '14px Montserrat';
    antsCtx.textAlign = 'center';
    antsCtx.textBaseline = 'middle';
    antsCtx.fillText('Nest', nest.x, nest.y);
    
    // Food
    antsCtx.fillStyle = '#F59E0B';
    antsCtx.beginPath();
    antsCtx.arc(food.x, food.y, 20, 0, Math.PI * 2);
    antsCtx.fill();
    antsCtx.fillStyle = '#FFFFFF';
    antsCtx.font = '14px Montserrat';
    antsCtx.textAlign = 'center';
    antsCtx.textBaseline = 'middle';
    antsCtx.fillText('Food', food.x, food.y);
}

// ===== Main Animation Loop =====
function animateAnts(timestamp) {
    if (!isRunning) return;
    
    const deltaTime = timestamp - lastTime;
    if (deltaTime < 16) { // ~60fps
        requestAnimationFrame(animateAnts);
        return;
    }
    lastTime = timestamp;
    
    // Clear canvas
    antsCtx.fillStyle = '#1E1E1E';
    antsCtx.fillRect(0, 0, worldWidth, worldHeight);
    
    // Update and draw
    drawPheromones();
    drawObstacles();
    drawNestAndFood();
    
    // Update ants
    for (const ant of ants) {
        ant.update();
    }
    
    // Draw ants
    for (const ant of ants) {
        ant.draw();
    }
    
    // Evaporate pheromones
    const cols = pheromones.length;
    const rows = pheromones[0] ? pheromones[0].length : 0;
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            pheromones[i][j] *= PHEROMONE_EVAPORATION;
            if (pheromones[i][j] < 0.01) {
                pheromones[i][j] = 0;
            }
        }
    }
    
    // Continue animation
    requestAnimationFrame(animateAnts);
}

// ===== Setup Function =====
function setupAnts() {
    // Get canvas container
    const container = document.getElementById('ants-canvas');
    if (!container) {
        console.warn('Ants canvas container not found.');
        return;
    }
    
    // Create canvas
    antsCanvas = document.createElement('canvas');
    antsCanvas.width = container.clientWidth;
    antsCanvas.height = 500;
    container.appendChild(antsCanvas);
    antsCtx = antsCanvas.getContext('2d');
    
    // Set world dimensions
    worldWidth = antsCanvas.width;
    worldHeight = antsCanvas.height;
    
    // Initialize simulation
    initPheromones();
    initAnts();
    initObstacles();
    
    // Start animation
    isRunning = true;
    lastTime = 0;
    requestAnimationFrame(animateAnts);
}

// ===== Reset Function =====
function resetAnts() {
    if (!antsCanvas) return;
    
    isRunning = false;
    
    // Clear canvas
    antsCtx.fillStyle = '#1E1E1E';
    antsCtx.fillRect(0, 0, worldWidth, worldHeight);
    
    // Reinitialize
    initPheromones();
    initAnts();
    
    // Restart animation
    isRunning = true;
    lastTime = 0;
    requestAnimationFrame(animateAnts);
}

// ===== Handle Window Resize =====
function handleAntsResize() {
    if (!antsCanvas) return;
    
    const container = document.getElementById('ants-canvas');
    if (container) {
        antsCanvas.width = container.clientWidth;
        antsCanvas.height = 500;
        worldWidth = antsCanvas.width;
        worldHeight = antsCanvas.height;
        
        // Redraw
        if (!isRunning) {
            antsCtx.fillStyle = '#1E1E1E';
            antsCtx.fillRect(0, 0, worldWidth, worldHeight);
            drawPheromones();
            drawObstacles();
            drawNestAndFood();
            for (const ant of ants) {
                ant.draw();
            }
        }
    }
}

// ===== Initialize =====
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setupAnts();
        window.addEventListener('resize', handleAntsResize);
    });
} else {
    setupAnts();
    window.addEventListener('resize', handleAntsResize);
}

// Make resetAnts available globally
window.resetAnts = resetAnts;
