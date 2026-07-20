// ===== Main JavaScript =====

// ===== Loading Screen =====
window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
            document.body.style.overflow = 'auto';
            
            // Initialize animations
            initScrollAnimations();
            
            // Initialize typed text
            initTypedText();
        }, 1500);
    }
});

// Prevent scrolling while loading
document.body.style.overflow = 'hidden';

// ===== Mobile Navigation Toggle =====
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
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

// ===== Smooth Scroll for Anchor Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const navHeight = navbar ? navbar.offsetHeight : 0;
            const targetPosition = targetElement.offsetTop - navHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Typed.js Animation =====
function initTypedText() {
    const typedElement = document.querySelector('.typed-text');
    if (!typedElement) return;
    
    const typed = new Typed(typedElement, {
        strings: [
            'Civil Engineering Student',
            'MMC & Numerical Simulation Enthusiast',
            'Future Structural Analysis Engineer'
        ],
        typeSpeed: 50,
        backSpeed: 30,
        loop: true,
        loopCount: Infinity,
        showCursor: true,
        cursorChar: '|',
        autoInsertCss: true
    });
}

// ===== Scroll Animations =====
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-aos]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// ===== Form Submission =====
const contactForm = document.getElementById('contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('This is a placeholder form. To enable it, connect to a backend service like Formspree or Netlify Forms.');
    });
}

// ===== Console Easter Egg =====
console.log('%c🚀 Maxime Novo Frelicot Portfolio', 'color: #2563EB; font-size: 20px; font-weight: bold;');
console.log('%cPassionate about MMC, Numerical Simulation, and Structural Analysis!', 'color: #10B981; font-size: 14px;');
