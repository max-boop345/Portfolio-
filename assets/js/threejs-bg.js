// ===== Three.js Bridge Animation for Hero Section =====

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
camera.position.set(0, 2, 5);
camera.lookAt(0, 0, 0);

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

// ===== Create a Bridge Structure =====
function createBridge() {
    const group = new THREE.Group();
    
    // Materials
    const deckMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x4a5568, // Dark slate gray
        transparent: true,
        opacity: 0.9
    });
    
    const supportMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x2d3748, // Darker gray
        transparent: true,
        opacity: 0.9
    });
    
    const cableMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x718096, // Light gray
        transparent: true,
        opacity: 0.8
    });
    
    // Bridge deck (main horizontal part)
    const deckGeometry = new THREE.BoxGeometry(6, 0.2, 0.5);
    const deck = new THREE.Mesh(deckGeometry, deckMaterial);
    deck.position.y = 2;
    group.add(deck);
    
    // Bridge supports (vertical pillars)
    const supportGeometry = new THREE.BoxGeometry(0.3, 2.5, 0.3);
    
    // Left support
    const support1 = new THREE.Mesh(supportGeometry, supportMaterial);
    support1.position.set(-2.5, 0.25, 0);
    group.add(support1);
    
    // Right support
    const support2 = new THREE.Mesh(supportGeometry, supportMaterial);
    support2.position.set(2.5, 0.25, 0);
    group.add(support2);
    
    // Central support
    const support3 = new THREE.Mesh(supportGeometry, supportMaterial);
    support3.position.set(0, 0.25, 0);
    group.add(support3);
    
    // Cables (diagonal supports)
    const cableGeometry = new THREE.CylinderGeometry(0.03, 0.03, 2.8, 16);
    
    // Left cables
    const cable1 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable1.position.set(-2.2, 1.4, 0);
    cable1.rotation.z = Math.PI / 4;
    cable1.rotation.x = Math.PI / 2;
    group.add(cable1);
    
    const cable2 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable2.position.set(-2.2, 1.4, 0);
    cable2.rotation.z = -Math.PI / 4;
    cable2.rotation.x = Math.PI / 2;
    group.add(cable2);
    
    // Right cables
    const cable3 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable3.position.set(2.2, 1.4, 0);
    cable3.rotation.z = Math.PI / 4;
    cable3.rotation.x = Math.PI / 2;
    group.add(cable3);
    
    const cable4 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable4.position.set(2.2, 1.4, 0);
    cable4.rotation.z = -Math.PI / 4;
    cable4.rotation.x = Math.PI / 2;
    group.add(cable4);
    
    // Central cables
    const cable5 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable5.position.set(-1.1, 1.4, 0);
    cable5.rotation.z = Math.PI / 4;
    cable5.rotation.x = Math.PI / 2;
    group.add(cable5);
    
    const cable6 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable6.position.set(1.1, 1.4, 0);
    cable6.rotation.z = -Math.PI / 4;
    cable6.rotation.x = Math.PI / 2;
    group.add(cable6);
    
    return group;
}

// Create bridge and add to scene
const bridge = createBridge();
scene.add(bridge);

// ===== Lighting =====
const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(1, 1, 1);
scene.add(directionalLight);

const directionalLight2 = new THREE.DirectionalLight(0x2563eb, 0.3);
directionalLight2.position.set(-1, -1, -1);
scene.add(directionalLight2);

// ===== Animation Loop =====
let rotationSpeed = 0.001;
let time = 0;

function animate() {
    requestAnimationFrame(animate);
    
    // Rotate the bridge slowly
    time += 0.01;
    bridge.rotation.y = Math.sin(time * 0.5) * 0.1;
    
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
