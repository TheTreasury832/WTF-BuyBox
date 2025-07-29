// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.getElementById('header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Modal functionality
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Plan selection
function selectPlan(planType) {
    // Add loading state
    event.target.classList.add('loading');
    const originalText = event.target.textContent;
    event.target.textContent = '';
    
    // Send request to backend
    fetch('/api/select-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ planType: planType })
    })
    .then(response => response.json())
    .then(data => {
        event.target.classList.remove('loading');
        event.target.textContent = originalText;
        
        if (data.success) {
            alert(data.message);
            // In a real app, you would redirect to checkout
            // window.location.href = data.redirect_url;
        } else {
            alert('Error selecting plan. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        event.target.classList.remove('loading');
        event.target.textContent = originalText;
        alert('Error selecting plan. Please try again.');
    });
}

// Form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            submitBtn.classList.add('loading');
            submitBtn.textContent = '';
            
            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Sign In';
                
                if (data.success) {
                    alert(data.message);
                    closeModal('loginModal');
                    // Optionally redirect to dashboard
                    // window.location.href = '/dashboard';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Sign In';
                alert('Login failed. Please try again.');
            });
        });
    }

    // Signup form
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            submitBtn.classList.add('loading');
            submitBtn.textContent = '';
            
            fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Start Free Trial';
                
                if (data.success) {
                    alert(data.message);
                    closeModal('signupModal');
                    // Optionally redirect to dashboard
                    // window.location.href = '/dashboard';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Start Free Trial';
                alert('Signup failed. Please try again.');
            });
        });
    }

    // Buyer qualification form
    const qualificationForm = document.getElementById('buyerQualificationForm');
    if (qualificationForm) {
        qualificationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const formData = new FormData(e.target);
            
            // Collect checkbox values
            const strategies = [];
            document.querySelectorAll('input[name="strategy"]:checked').forEach(checkbox => {
                strategies.push(checkbox.value);
            });
            
            const data = Object.fromEntries(formData);
            data.strategy = strategies;
            data.newsletter = document.getElementById('newsletter').checked;
            data.discord = document.getElementById('discord').checked;
            data.mentorship = document.getElementById('mentorship').checked;
            
            submitBtn.classList.add('loading');
            submitBtn.textContent = '';
            
            fetch('/api/buyer-qualification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Join Verified Buyer Network';
                
                if (data.success) {
                    alert(data.message);
                    // Reset form
                    e.target.reset();
                    // Remove selected states from checkboxes
                    document.querySelectorAll('.checkbox-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.classList.remove('loading');
                submitBtn.textContent = 'Join Verified Buyer Network';
                alert('Submission failed. Please try again.');
            });
        });
    }
});

// Checkbox interactions
document.querySelectorAll('.checkbox-item').forEach(item => {
    item.addEventListener('click', function() {
        const checkbox = this.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
        
        if (checkbox.checked) {
            this.classList.add('selected');
        } else {
            this.classList.remove('selected');
        }
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe all cards and sections
document.querySelectorAll('.feature-card, .pricing-card, .stat-item').forEach(el => {
    observer.observe(el);
});

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    }
    updateCounter();
}

// Trigger counter animations when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const numbers = entry.target.querySelectorAll('.stat-number');
            numbers.forEach((num, index) => {
                const targets = [15000, 2.8, 47, 72];
                const suffixes = ['K+', 'B', '%', 'hrs'];
                setTimeout(() => {
                    animateCounter(num, targets[index], 1500);
                    setTimeout(() => {
                        num.textContent = targets[index] + suffixes[index];
                    }, 1600);
                }, index * 200);
            });
            statsObserver.unobserve(entry.target);
        }
    });
});

const statsSection = document.querySelector('.stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Mobile menu toggle
function toggleMobileMenu() {
    const nav = document.querySelector('.nav');
    nav.classList.toggle('mobile-open');
}

// Add mobile menu button for small screens
if (window.innerWidth <= 768) {
    const headerContent = document.querySelector('.header-content');
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.innerHTML = '☰';
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.onclick = toggleMobileMenu;
    mobileMenuBtn.style.cssText = `
        display: block;
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--dark-color);
        cursor: pointer;
        padding: 0.5rem;
    `;
    headerContent.appendChild(mobileMenuBtn);
}

// Enhanced form validation
function validateForm(form) {
    const required = form.querySelectorAll('[required]');
    let isValid = true;
    
    required.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--accent-color)';
        }
    });
    
    return isValid;
}

// Real-time form validation
document.querySelectorAll('input, select, textarea').forEach(field => {
    field.addEventListener('blur', function() {
        if (this.hasAttribute('required')) {
            if (!this.value.trim()) {
                this.style.borderColor = 'var(--danger-color)';
            } else {
                this.style.borderColor = 'var(--accent-color)';
            }
        }
    });
});

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Add initial animations
    setTimeout(() => {
        const heroContent = document.querySelector('.hero-content');
        if (heroContent) {
            heroContent.classList.add('fade-in-up');
        }
    }, 500);
    
    // Preload critical resources
    const criticalImages = [
        // Add any critical images here
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
});