// ===== Three.js Background Animation for Hero Section =====

// Check if the container exists
const container = document.getElementById('threejs-container');
if (!container) {
    console.warn('Three.js container not found. Skipping 3D animation.');
    return;
}

// Scene setup
const scene = new THREE.Scene();
scene.background = null; // Transparent background

// Camera setup
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.z = 5;

// Renderer setup
const renderer = new THREE.WebGLRenderer({ 
    antialias: true, 
    alpha: true 
});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setClearColor(0x000000, 0); // Transparent
container.appendChild(renderer.domElement);

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});

// ===== Create a Simple Bridge Model =====
function createBridge() {
    const group = new THREE.Group();
    
    // Bridge deck (main horizontal part)
    const deckGeometry = new THREE.BoxGeometry(4, 0.2, 0.5);
    const deckMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x6B7280, // Gray
        transparent: true,
        opacity: 0.8
    });
    const deck = new THREE.Mesh(deckGeometry, deckMaterial);
    group.add(deck);
    
    // Bridge supports (vertical pillars)
    const supportGeometry = new THREE.BoxGeometry(0.2, 1, 0.2);
    const supportMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x4B5563, // Darker gray
        transparent: true,
        opacity: 0.8
    });
    
    // Left support
    const support1 = new THREE.Mesh(supportGeometry, supportMaterial);
    support1.position.x = -1.5;
    support1.position.y = -0.5;
    group.add(support1);
    
    // Right support
    const support2 = new THREE.Mesh(supportGeometry, supportMaterial);
    support2.position.x = 1.5;
    support2.position.y = -0.5;
    group.add(support2);
    
    // Cables (diagonal supports)
    const cableGeometry = new THREE.CylinderGeometry(0.05, 0.05, 1.2, 8);
    const cableMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x374151, // Dark gray
        transparent: true,
        opacity: 0.8
    });
    
    // Left cable
    const cable1 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable1.position.x = -1.2;
    cable1.position.y = 0.2;
    cable1.rotation.z = Math.PI / 4;
    group.add(cable1);
    
    // Right cable
    const cable2 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable2.position.x = 1.2;
    cable2.position.y = 0.2;
    cable2.rotation.z = -Math.PI / 4;
    group.add(cable2);
    
    return group;
}

// Create bridge and add to scene
const bridge = createBridge();
scene.add(bridge);

// ===== Lighting =====
const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 0.8);
directionalLight.position.set(1, 1, 1);
scene.add(directionalLight);

// ===== Animation Loop =====
let rotationSpeed = 0.002;

function animate() {
    requestAnimationFrame(animate);
    
    // Rotate the bridge slowly
    bridge.rotation.y += rotationSpeed;
    
    // Render the scene
    renderer.render(scene, camera);
}

// Start animation
animate();

// ===== Cleanup on Page Navigation =====
window.addEventListener('beforeunload', () => {
    container.removeChild(renderer.domElement);
    renderer.dispose();
});
