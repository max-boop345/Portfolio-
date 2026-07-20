// ===== Dijkstra's Algorithm Visualizer =====

// Canvas and context
let dijkstraCanvas, dijkstraCtx;

// Graph data
let nodes = [];
let edges = [];
let selectedNode = null;
let isAddingEdge = false;
let startNode = null;
let endNode = null;

// Node and edge styles
const NODE_RADIUS = 20;
const NODE_COLOR = '#2563EB';
const NODE_HOVER_COLOR = '#3B82F6';
const NODE_START_COLOR = '#10B981';
const NODE_END_COLOR = '#EF4444';
const NODE_VISITED_COLOR = '#8B5CF6';
const EDGE_COLOR = '#4A5568';
const EDGE_WEIGHT_COLOR = '#A0AEC0';
const PATH_COLOR = '#F59E0B';
const PATH_WIDTH = 4;
const BG_COLOR = '#1E1E1E';

// Animation state
let isAnimating = false;
let animationQueue = [];
let animationIndex = 0;

// ===== Node Class =====
class Node {
    constructor(x, y, id) {
        this.x = x;
        this.y = y;
        this.id = id;
        this.connections = []; // Array of { node: Node, weight: number }
    }
    
    draw(isHovered = false, isStart = false, isEnd = false, isVisited = false) {
        dijkstraCtx.beginPath();
        dijkstraCtx.arc(this.x, this.y, NODE_RADIUS, 0, Math.PI * 2);
        
        // Determine node color
        let color = NODE_COLOR;
        if (isStart) color = NODE_START_COLOR;
        else if (isEnd) color = NODE_END_COLOR;
        else if (isVisited) color = NODE_VISITED_COLOR;
        else if (isHovered) color = NODE_HOVER_COLOR;
        
        dijkstraCtx.fillStyle = color;
        dijkstraCtx.fill();
        
        // Draw node ID
        dijkstraCtx.fillStyle = '#FFFFFF';
        dijkstraCtx.font = '12px Montserrat';
        dijkstraCtx.textAlign = 'center';
        dijkstraCtx.textBaseline = 'middle';
        dijkstraCtx.fillText(this.id, this.x, this.y);
        
        // Draw stroke
        dijkstraCtx.strokeStyle = '#FFFFFF';
        dijkstraCtx.lineWidth = 2;
        dijkstraCtx.stroke();
    }
    
    containsPoint(px, py) {
        const dx = px - this.x;
        const dy = py - this.y;
        return Math.sqrt(dx * dx + dy * dy) <= NODE_RADIUS;
    }
}

// ===== Edge Class =====
class Edge {
    constructor(node1, node2, weight) {
        this.node1 = node1;
        this.node2 = node2;
        this.weight = weight;
    }
    
    draw(isPath = false) {
        dijkstraCtx.beginPath();
        dijkstraCtx.moveTo(this.node1.x, this.node1.y);
        dijkstraCtx.lineTo(this.node2.x, this.node2.y);
        
        dijkstraCtx.strokeStyle = isPath ? PATH_COLOR : EDGE_COLOR;
        dijkstraCtx.lineWidth = isPath ? PATH_WIDTH : 2;
        dijkstraCtx.stroke();
        
        // Draw weight
        const midX = (this.node1.x + this.node2.x) / 2;
        const midY = (this.node1.y + this.node2.y) / 2;
        dijkstraCtx.fillStyle = EDGE_WEIGHT_COLOR;
        dijkstraCtx.font = '12px Montserrat';
        dijkstraCtx.textAlign = 'center';
        dijkstraCtx.textBaseline = 'middle';
        dijkstraCtx.fillText(this.weight.toString(), midX, midY);
    }
}

// ===== Dijkstra's Algorithm =====
function dijkstra(start, end) {
    if (!start || !end) return [];
    
    // Reset distances and previous nodes
    const distances = {};
    const previous = {};
    const visited = new Set();
    const queue = [];
    
    // Initialize distances
    nodes.forEach(node => {
        distances[node.id] = node === start ? 0 : Infinity;
        previous[node.id] = null;
        queue.push(node);
    });
    
    // Animation steps
    animationQueue = [];
    
    // Main loop
    while (queue.length > 0) {
        // Find node with smallest distance
        let current = queue.reduce((minNode, node) => 
            distances[node.id] < distances[minNode.id] ? node : minNode, queue[0]);
        
        // If we've reached the end, stop
        if (current === end) break;
        
        // Remove current from queue
        queue.splice(queue.indexOf(current), 1);
        visited.add(current.id);
        
        // Add visit step to animation
        animationQueue.push({ 
            type: 'visit', 
            node: current.id 
        });
        
        // Update distances for neighbors
        current.connections.forEach(connection => {
            const neighbor = connection.node;
            const alt = distances[current.id] + connection.weight;
            
            if (alt < distances[neighbor.id]) {
                distances[neighbor.id] = alt;
                previous[neighbor.id] = current;
                
                // Add update step to animation
                animationQueue.push({ 
                    type: 'update', 
                    node: neighbor.id,
                    distance: alt
                });
            }
        });
    }
    
    // Reconstruct path
    const path = [];
    let current = end;
    while (current) {
        path.unshift(current);
        current = previous[current.id];
    }
    
    // Add path to animation
    if (path.length > 1) {
        animationQueue.push({ 
            type: 'path', 
            edges: []
        });
        
        for (let i = 0; i < path.length - 1; i++) {
            const edge = edges.find(e => 
                (e.node1 === path[i] && e.node2 === path[i + 1]) ||
                (e.node1 === path[i + 1] && e.node2 === path[i]));
            if (edge) {
                animationQueue[animationQueue.length - 1].edges.push(edge);
            }
        }
    }
    
    return path;
}

// ===== Drawing Functions =====
function drawGraph() {
    // Clear canvas
    dijkstraCtx.fillStyle = BG_COLOR;
    dijkstraCtx.fillRect(0, 0, dijkstraCanvas.width, dijkstraCanvas.height);
    
    // Draw edges
    edges.forEach(edge => {
        const isPathEdge = animationQueue.some(step => 
            step.type === 'path' && step.edges.includes(edge));
        edge.draw(isPathEdge);
    });
    
    // Draw nodes
    nodes.forEach(node => {
        const isStart = node === startNode;
        const isEnd = node === endNode;
        const isVisited = animationQueue.some(step => 
            step.type === 'visit' && step.node === node.id);
        const isHovered = selectedNode === node;
        
        node.draw(isHovered, isStart, isEnd, isVisited);
    });
}

function drawAnimationStep() {
    if (animationIndex >= animationQueue.length) {
        isAnimating = false;
        return;
    }
    
    const step = animationQueue[animationIndex];
    
    // Clear canvas
    dijkstraCtx.fillStyle = BG_COLOR;
    dijkstraCtx.fillRect(0, 0, dijkstraCanvas.width, dijkstraCanvas.height);
    
    // Draw all edges
    edges.forEach(edge => {
        const isPathEdge = step.type === 'path' && step.edges.includes(edge);
        edge.draw(isPathEdge);
    });
    
    // Draw nodes with animation state
    nodes.forEach(node => {
        const isStart = node === startNode;
        const isEnd = node === endNode;
        const isVisited = animationQueue.slice(0, animationIndex + 1).some(s => 
            s.type === 'visit' && s.node === node.id);
        const isHovered = selectedNode === node;
        
        node.draw(isHovered, isStart, isEnd, isVisited);
    });
    
    // Draw current step info
    dijkstraCtx.fillStyle = '#A0AEC0';
    dijkstraCtx.font = '14px Montserrat';
    dijkstraCtx.textAlign = 'center';
    
    if (step.type === 'visit') {
        dijkstraCtx.fillText('Visiting node ' + step.node, dijkstraCanvas.width / 2, 20);
    } else if (step.type === 'update') {
        dijkstraCtx.fillText('Updated distance to ' + step.node + ': ' + step.distance, dijkstraCanvas.width / 2, 20);
    } else if (step.type === 'path') {
        dijkstraCtx.fillText('Shortest path found!', dijkstraCanvas.width / 2, 20);
    }
    
    animationIndex++;
    
    if (isAnimating) {
        setTimeout(drawAnimationStep, 1000);
    }
}

// ===== Event Handlers =====
function handleCanvasClick(e) {
    if (isAnimating) return;
    
    const rect = dijkstraCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    if (isAddingEdge && selectedNode) {
        // Find node to connect to
        const targetNode = nodes.find(node => node.containsPoint(x, y));
        if (targetNode && targetNode !== selectedNode) {
            // Create edge
            const weight = Math.floor(Math.random() * 10) + 1; // Random weight between 1-10
            const edge = new Edge(selectedNode, targetNode, weight);
            edges.push(edge);
            
            // Add connection to both nodes
            selectedNode.connections.push({ node: targetNode, weight });
            targetNode.connections.push({ node: selectedNode, weight });
            
            isAddingEdge = false;
            selectedNode = null;
            drawGraph();
        }
    } else {
        // Check if clicked on a node
        const node = nodes.find(node => node.containsPoint(x, y));
        if (node) {
            selectedNode = node;
            
            // Set as start or end node
            if (!startNode) {
                startNode = node;
            } else if (!endNode) {
                endNode = node;
            }
            
            drawGraph();
        } else {
            // Add new node
            const id = 'N' + (nodes.length + 1);
            const newNode = new Node(x, y, id);
            nodes.push(newNode);
            selectedNode = newNode;
            drawGraph();
        }
    }
}

function handleCanvasMove(e) {
    if (isAnimating) return;
    
    const rect = dijkstraCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Check if hovering over a node
    const hoveredNode = nodes.find(node => node.containsPoint(x, y));
    if (hoveredNode !== selectedNode) {
        selectedNode = hoveredNode;
        drawGraph();
    }
}

// ===== Public Functions =====
function initDijkstra() {
    dijkstraCanvas = document.getElementById('dijkstra-canvas');
    if (!dijkstraCanvas) return;
    
    dijkstraCtx = dijkstraCanvas.getContext('2d');
    
    // Set canvas size
    dijkstraCanvas.width = dijkstraCanvas.parentElement.clientWidth;
    dijkstraCanvas.height = 500;
    
    // Add event listeners
    dijkstraCanvas.addEventListener('click', handleCanvasClick);
    dijkstraCanvas.addEventListener('mousemove', handleCanvasMove);
    
    // Initialize with some nodes
    nodes = [];
    edges = [];
    selectedNode = null;
    isAddingEdge = false;
    startNode = null;
    endNode = null;
    isAnimating = false;
    animationQueue = [];
    animationIndex = 0;
    
    // Add some default nodes
    const node1 = new Node(100, 100, 'A');
    const node2 = new Node(300, 100, 'B');
    const node3 = new Node(200, 300, 'C');
    const node4 = new Node(400, 300, 'D');
    nodes.push(node1, node2, node3, node4);
    
    // Add some default edges
    const edge1 = new Edge(node1, node2, 4);
    const edge2 = new Edge(node1, node3, 2);
    const edge3 = new Edge(node2, node3, 1);
    const edge4 = new Edge(node2, node4, 5);
    const edge5 = new Edge(node3, node4, 3);
    edges.push(edge1, edge2, edge3, edge4, edge5);
    
    // Add connections
    node1.connections.push({ node: node2, weight: 4 });
    node1.connections.push({ node: node3, weight: 2 });
    node2.connections.push({ node: node1, weight: 4 });
    node2.connections.push({ node: node3, weight: 1 });
    node2.connections.push({ node: node4, weight: 5 });
    node3.connections.push({ node: node1, weight: 2 });
    node3.connections.push({ node: node2, weight: 1 });
    node3.connections.push({ node: node4, weight: 3 });
    node4.connections.push({ node: node2, weight: 5 });
    node4.connections.push({ node: node3, weight: 3 });
    
    // Set start and end nodes
    startNode = node1;
    endNode = node4;
    
    // Draw initial graph
    drawGraph();
}

function addNodeDijkstra() {
    if (isAnimating) return;
    isAddingEdge = false;
    selectedNode = null;
}

function addEdgeDijkstra() {
    if (isAnimating) return;
    if (selectedNode) {
        isAddingEdge = true;
    } else {
        alert('Please select a node first by clicking on it.');
    }
}

function runDijkstra() {
    if (isAnimating) return;
    if (!startNode || !endNode) {
        alert('Please set start and end nodes by clicking on them.');
        return;
    }
    
    isAnimating = true;
    animationIndex = 0;
    dijkstra(startNode, endNode);
    drawAnimationStep();
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDijkstra);
} else {
    initDijkstra();
}

// Handle window resize
window.addEventListener('resize', () => {
    if (dijkstraCanvas) {
        dijkstraCanvas.width = dijkstraCanvas.parentElement.clientWidth;
        dijkstraCanvas.height = 500;
        if (!isAnimating) {
            drawGraph();
        }
    }
});
