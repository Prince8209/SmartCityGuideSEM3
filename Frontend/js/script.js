// ========================================
// SMART CITY GUIDE - RESPONSIVE JAVASCRIPT
// ========================================

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if device is mobile/tablet
function isMobileDevice() {
    return window.innerWidth <= 768 || ('ontouchstart' in window);
}

// Get correct path based on current location
function getCorrectPath(filename) {
    const currentPath = window.location.pathname;
    const isInPages = currentPath.includes('/pages/');

    if (filename === 'cities.html' || filename === 'features.html' ||
        filename === 'itinerary.html' || filename === 'contact.html' ||
        filename === 'login.html' || filename === 'signup.html') {
        return isInPages ? filename : `pages/${filename}`;
    }

    if (filename === 'index.html') {
        return isInPages ? '../index.html' : 'index.html';
    }

    return filename;
}

// ========================================
// MOBILE MENU TOGGLE - ENHANCED
// ========================================

const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');
const body = document.body;

if (menuToggle && navLinks) {
    // Toggle menu
    menuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        navLinks.classList.toggle('active');
        const icon = menuToggle.querySelector('i');

        if (navLinks.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
            body.style.overflow = 'hidden'; // Prevent scroll when menu open
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.style.overflow = '';
        }
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            const icon = menuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.style.overflow = '';
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active') &&
            !navLinks.contains(e.target) &&
            !menuToggle.contains(e.target)) {
            navLinks.classList.remove('active');
            const icon = menuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.style.overflow = '';
        }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            const icon = menuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.style.overflow = '';
        }
    });
}

// ========================================
// NAVBAR SCROLL EFFECT - OPTIMIZED
// ========================================

const navbar = document.getElementById('navbar');
let lastScrollY = window.scrollY;
let ticking = false;

function updateNavbar() {
    const scrollY = window.scrollY;

    if (scrollY > 50) {
        navbar?.classList.add('scrolled');
    } else {
        navbar?.classList.remove('scrolled');
    }

    // Hide navbar on scroll down, show on scroll up (mobile)
    if (isMobileDevice()) {
        if (scrollY > lastScrollY && scrollY > 100) {
            navbar?.style.setProperty('transform', 'translateY(-100%)');
        } else {
            navbar?.style.setProperty('transform', 'translateY(0)');
        }
    }

    lastScrollY = scrollY;
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(updateNavbar);
        ticking = true;
    }
});

// ========================================
// ANIMATED COUNTER - OPTIMIZED
// ========================================

function animateCounter(element, target, duration = 2000) {
    const start = parseFloat(element.textContent) || 0;
    const isDecimal = target % 1 !== 0;
    const increment = (target - start) / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = isDecimal ? current.toFixed(1) : Math.floor(current);
    }, 16);
}

// Trigger counters when visible
const stats = document.querySelectorAll('.stat-number');
if (stats.length > 0) {
    const observerOptions = {
        threshold: isMobileDevice() ? 0.3 : 0.5,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                const target = parseFloat(entry.target.dataset.target);
                animateCounter(entry.target, target);
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);

    stats.forEach(stat => observer.observe(stat));
}

// ========================================
// SEARCH FUNCTIONALITY - ENHANCED
// ========================================

function searchCities() {
    const searchInputElement = document.getElementById('searchInput');
    const citiesPath = getCorrectPath('cities.html');

    if (searchInputElement && searchInputElement.value.trim()) {
        sessionStorage.setItem('searchQuery', searchInputElement.value);
        window.location.href = citiesPath;
    } else {
        window.location.href = citiesPath;
    }
}

// Search on Enter key
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchCities();
        }
    });

    // Enhanced search with debouncing
    const debouncedSearch = debounce((value) => {
        if (value.length > 2) {
            console.log('Searching for:', value);
            // Future: Add live search suggestions here
        }
    }, 300);

    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });

    // Save search history
    searchInput.addEventListener('change', (e) => {
        if (e.target.value.trim()) {
            let history = UserPreferences.load('searchHistory') || [];
            history.unshift(e.target.value);
            history = [...new Set(history)].slice(0, 5);
            UserPreferences.save('searchHistory', history);
        }
    });
}

// Filter cities on cities page
if (window.location.pathname.includes('cities.html')) {
    const searchQuery = sessionStorage.getItem('searchQuery');
    if (searchQuery) {
        setTimeout(() => {
            filterCities(searchQuery);
            sessionStorage.removeItem('searchQuery');
        }, 100);
    }
}

function filterCities(query) {
    const cards = document.querySelectorAll('.city-card');
    const searchLower = query.toLowerCase();

    cards.forEach(card => {
        const name = card.querySelector('.city-name')?.textContent.toLowerCase();
        const desc = card.querySelector('.city-desc')?.textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll('.attraction-tag'))
            .map(tag => tag.textContent.toLowerCase())
            .join(' ');

        const matches = name?.includes(searchLower) ||
            desc?.includes(searchLower) ||
            tags.includes(searchLower);

        const parentCol = card.closest('[class*="col-"]');
        if (parentCol) {
            parentCol.style.display = matches ? 'block' : 'none';
        } else {
            card.style.display = matches ? 'block' : 'none';
        }
    });
}

// ========================================
// SMOOTH SCROLL - ENHANCED
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            const offset = isMobileDevice() ? 80 : 100;
            const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ========================================
// FADE IN ANIMATION ON SCROLL - OPTIMIZED
// ========================================

const fadeElements = document.querySelectorAll('.city-card, .section');
if (fadeElements.length > 0) {
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: isMobileDevice() ? 0.05 : 0.1,
        rootMargin: '0px 0px -30px 0px'
    });

    fadeElements.forEach(el => fadeObserver.observe(el));
}

// ========================================
// CONTACT FORM VALIDATION
// ========================================

const contactForm = document.querySelector('#contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = document.getElementById('name')?.value.trim();
        const email = document.getElementById('email')?.value.trim();
        const message = document.getElementById('message')?.value.trim();

        if (!name || !email || !message) {
            alert('Please fill in all fields');
            return;
        }

        if (!isValidEmail(email)) {
            alert('Please enter a valid email address');
            return;
        }

        alert(`Thank you ${name}! Your message has been sent successfully. We'll get back to you soon at ${email}`);
        contactForm.reset();
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ========================================
// SCROLL TO TOP BUTTON - ENHANCED
// ========================================

const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.className = 'scroll-to-top';
scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollToTopBtn.setAttribute('aria-label', 'Scroll to top');
document.body.appendChild(scrollToTopBtn);

let scrollTicking = false;
window.addEventListener('scroll', () => {
    if (!scrollTicking) {
        window.requestAnimationFrame(() => {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
            scrollTicking = false;
        });
        scrollTicking = true;
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ========================================
// LOCAL STORAGE FOR USER PREFERENCES
// ========================================

const UserPreferences = {
    save: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },

    load: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error loading from localStorage:', e);
            return null;
        }
    },

    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// ========================================
// FORM DATA PERSISTENCE
// ========================================

document.querySelectorAll('form input, form textarea, form select').forEach(field => {
    if (!field.id) return;

    const savedValue = UserPreferences.load(`form_${field.id}`);
    if (savedValue && field.type !== 'password') {
        field.value = savedValue;
    }

    field.addEventListener('change', (e) => {
        if (e.target.type !== 'password' && e.target.id) {
            UserPreferences.save(`form_${e.target.id}`, e.target.value);
        }
    });
});

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        setTimeout(() => {
            form.querySelectorAll('input, textarea, select').forEach(field => {
                if (field.id) {
                    UserPreferences.remove(`form_${field.id}`);
                }
            });
        }, 1000);
    });
});

// ========================================
// SMOOTH PAGE TRANSITIONS
// ========================================

document.body.style.opacity = '0';
window.addEventListener('load', () => {
    document.body.style.transition = 'opacity 0.3s ease';
    document.body.style.opacity = '1';
});

// ========================================
// RESPONSIVE GRID HANDLING
// ========================================

if (window.location.pathname.includes('itinerary.html')) {
    function handleResponsiveGrid() {
        const gridContainers = document.querySelectorAll('[style*="grid-template-columns: 1fr 2fr"]');
        gridContainers.forEach(container => {
            if (window.innerWidth <= 1024) {
                container.style.gridTemplateColumns = '1fr';
                container.style.gap = '2rem';
            } else {
                container.style.gridTemplateColumns = '1fr 2fr';
            }
        });
    }

    handleResponsiveGrid();
    window.addEventListener('resize', debounce(handleResponsiveGrid, 250));
}

// ========================================
// TOUCH GESTURES FOR MOBILE
// ========================================

if (isMobileDevice()) {
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 100;
        const diff = touchStartX - touchEndX;

        // Swipe left to close menu
        if (diff > swipeThreshold && navLinks?.classList.contains('active')) {
            navLinks.classList.remove('active');
            const icon = menuToggle?.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
            body.style.overflow = '';
        }
    }
}

// ========================================
// ACCESSIBILITY ENHANCEMENTS
// ========================================

document.querySelectorAll('.city-card, .feature-card').forEach(card => {
    card.setAttribute('tabindex', '0');
    card.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            const button = card.querySelector('button');
            if (button) button.click();
        }
    });
});

// Announce page changes to screen readers
const announcePageChange = () => {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = `Navigated to ${document.title}`;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
};

// ========================================
// INITIALIZE - RUN ON PAGE LOAD
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Smart City Guide loaded successfully!');

    // Add active class to current page nav link
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        const linkPage = href ? href.split('/').pop() : '';

        if (linkPage === currentPage ||
            (currentPage === 'index.html' && href === '../index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Announce page load
    announcePageChange();
});

// ========================================
// PERFORMANCE MONITORING
// ========================================

window.addEventListener('load', () => {
    if (window.performance) {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        if (pageLoadTime > 0) {
            console.log(`Page load time: ${pageLoadTime}ms`);
        }
    }

    console.log('Enhanced responsive features loaded successfully!');
});

// ========================================
// RESPONSIVE IMAGE LOADING
// ========================================

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ========================================
// WINDOW RESIZE HANDLER - OPTIMIZED
// ========================================

let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Close mobile menu if window is resized to desktop
        if (window.innerWidth > 768 && navLinks?.classList.contains('active')) {
            navLinks.classList.remove('active');
            const icon = menuToggle?.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
            body.style.overflow = '';
        }

        // Reset navbar transform on desktop
        if (window.innerWidth > 768 && navbar) {
            navbar.style.removeProperty('transform');
        }
    }, 250);
});
