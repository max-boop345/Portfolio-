// ===== Mobile Navigation Toggle =====
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// ===== Navbar Scroll Effect =====
const navbar = document.querySelector('.navbar');

if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ===== Close Mobile Menu on Link Click =====
const navLinksAll = document.querySelectorAll('.nav-links a');

navLinksAll.forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
});

// ===== Smooth Scroll for Anchor Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// ===== Form Submission (Placeholder) =====
const contactForm = document.getElementById('contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('This is a placeholder form. To enable it, connect to a backend service like Formspree or Netlify Forms.');
    });
}

// ===== Initialize Dijkstra and Ants on Projects Page =====
if (window.location.pathname.includes('projects.html') || 
    window.location.pathname.endsWith('projects.html') ||
    window.location.pathname === '/') {
    
    // Initialize Dijkstra's visualizer
    if (typeof initDijkstra === 'function') {
        initDijkstra();
    }
    
    // Initialize Ant Colony simulation
    if (typeof setupAnts === 'function') {
        // We'll call this from the ants.js script
    }
}

// ===== Lazy Loading for Images =====
if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Add Loading Animation for Interactive Demos =====
const demoContainers = document.querySelectorAll('.interactive-demo');

demoContainers.forEach(container => {
    const canvas = container.querySelector('canvas');
    if (canvas) {
        canvas.style.opacity = '0';
        canvas.style.transition = 'opacity 0.5s ease';
        
        // Show canvas when the demo is ready
        setTimeout(() => {
            canvas.style.opacity = '1';
        }, 100);
    }
});

// ===== Console Easter Egg =====
console.log('%c🚀 Maxime Novo Frelicot Portfolio', 'color: #2563EB; font-size: 20px; font-weight: bold;');
console.log('%cPassionate about MMC, Numerical Simulation, and AI in Engineering!', 'color: #10B981; font-size: 14px;');
