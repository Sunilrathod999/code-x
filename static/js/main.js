// Main JavaScript for MTS Furnitech

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Service modal functionality
    const serviceModal = document.getElementById('serviceModal');
    if (serviceModal) {
        serviceModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const title = button.getAttribute('data-title');
            const description = button.getAttribute('data-description');
            const image = button.getAttribute('data-image');

            const modalTitle = serviceModal.querySelector('#serviceModalTitle');
            const modalDescription = serviceModal.querySelector('#serviceModalDescription');
            const modalImage = serviceModal.querySelector('#serviceModalImage');

            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalImage.src = image;
            modalImage.alt = title;
        });
    }

    // Services tab functionality
    const serviceTabs = document.querySelectorAll('#servicesTabs button[data-bs-toggle="tab"]');
    serviceTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            // Add fade animation to tab content
            const activePane = document.querySelector(tab.getAttribute('data-bs-target'));
            if (activePane) {
                activePane.style.opacity = '0';
                setTimeout(() => {
                    activePane.style.transition = 'opacity 0.3s ease';
                    activePane.style.opacity = '1';
                }, 50);
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .feature-box');
    animateElements.forEach(el => {
        observer.observe(el);
    });

    // WhatsApp button click tracking
    const whatsappButtons = document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp"]');
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('WhatsApp button clicked');
            // Add analytics tracking here if needed
        });
    });

    // Contact form enhancement
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        const phoneInput = contactForm.querySelector('input[type="tel"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                // Simple phone number formatting
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 10) {
                    value = value.substring(0, 10);
                }
                e.target.value = value;
            });
        }
    }

    // Admin panel enhancements
    if (document.body.classList.contains('admin-page')) {
        // File upload preview
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        // Create preview image
                        let preview = input.parentNode.querySelector('.image-preview');
                        if (!preview) {
                            preview = document.createElement('img');
                            preview.className = 'image-preview img-thumbnail mt-2';
                            preview.style.maxWidth = '200px';
                            preview.style.maxHeight = '150px';
                            input.parentNode.appendChild(preview);
                        }
                        preview.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            });
        });

        // Confirm delete actions
        const deleteButtons = document.querySelectorAll('button[onclick*="confirm"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item?')) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Service card click enhancement
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add click animation
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = '';
            }, 150);
        });
    });

    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTopButton.className = 'btn btn-success position-fixed';
    backToTopButton.style.cssText = `
        bottom: 80px;
        right: 20px;
        z-index: 999;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    `;
    backToTopButton.setAttribute('title', 'Back to top');
    document.body.appendChild(backToTopButton);

    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    // Back to top functionality
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Initialize tooltips for back to top button
    new bootstrap.Tooltip(backToTopButton);

    // Enhanced lazy loading for images with loading indicators
    const images = document.querySelectorAll('img[data-src], .card-img-top');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const container = img.closest('.card-img-container');
                
                // Add loading state
                if (container) {
                    container.classList.add('loading');
                }
                
                // Create new image for preloading
                const newImg = new Image();
                newImg.onload = function() {
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    img.classList.add('loaded');
                    if (container) {
                        container.classList.remove('loading');
                        container.classList.add('loaded');
                    }
                };
                newImg.onerror = function() {
                    img.classList.add('error');
                    if (container) {
                        container.classList.remove('loading');
                        container.classList.add('error');
                    }
                };
                
                // Start loading
                if (img.dataset.src) {
                    newImg.src = img.dataset.src;
                } else {
                    newImg.src = img.src;
                }
                
                imageObserver.unobserve(img);
            }
        });
    }, { threshold: 0.1, rootMargin: '50px' });

    images.forEach(img => {
        imageObserver.observe(img);
    });

    // Service interest auto-selection based on URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const serviceParam = urlParams.get('service');
    if (serviceParam) {
        const serviceSelect = document.getElementById('service_interest');
        if (serviceSelect) {
            const option = Array.from(serviceSelect.options).find(opt => 
                opt.value.toLowerCase().includes(serviceParam.toLowerCase())
            );
            if (option) {
                option.selected = true;
            }
        }
    }
});

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

function formatPhoneNumber(phoneNumber) {
    // Remove all non-digit characters
    const cleaned = phoneNumber.replace(/\D/g, '');
    
    // Check if it's a valid length
    if (cleaned.length === 10) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    } else if (cleaned.length === 11) {
        return cleaned.replace(/(\d{1})(\d{3})(\d{3})(\d{4})/, '+$1 ($2) $3-$4');
    }
    
    return phoneNumber;
}

// Analytics tracking (placeholder)
function trackEvent(category, action, label = '') {
    console.log('Event tracked:', { category, action, label });
    // Add your analytics tracking code here (Google Analytics, etc.)
}

// Form submission tracking
document.addEventListener('submit', function(e) {
    if (e.target.classList.contains('contact-form')) {
        trackEvent('Form', 'Submit', 'Contact Form');
    }
});

// WhatsApp link tracking
document.addEventListener('click', function(e) {
    if (e.target.closest('a[href*="wa.me"]')) {
        trackEvent('External Link', 'Click', 'WhatsApp');
    }
});
