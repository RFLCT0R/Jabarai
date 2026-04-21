/**
 * ALLAITOOLS - Shared Components JavaScript
 * Handles footer, loading states, and utility functions
 */

(function() {
    'use strict';

    // ============================================
    // Copy to Clipboard Utility
    // ============================================
    function initCopyToClipboard() {
        document.querySelectorAll('.btn-copy').forEach(btn => {
            btn.addEventListener('click', function() {
                const textToCopy = this.dataset.copy || 
                    this.closest('.contact-card').querySelector('.email-display')?.textContent;
                
                if (textToCopy) {
                    navigator.clipboard.writeText(textToCopy).then(() => {
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        this.classList.add('copied');
                        
                        setTimeout(() => {
                            this.innerHTML = originalText;
                            this.classList.remove('copied');
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy:', err);
                        // Fallback for older browsers
                        const textArea = document.createElement('textarea');
                        textArea.value = textToCopy;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        this.classList.add('copied');
                        
                        setTimeout(() => {
                            this.innerHTML = originalText;
                            this.classList.remove('copied');
                        }, 2000);
                    });
                }
            });
        });
    }

    // ============================================
    // Contact Form Handler
    // ============================================
    function initContactForm() {
        const form = document.getElementById('contact-form');
        const successMessage = document.getElementById('form-success');

        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Show success message and hide form
                if (successMessage) {
                    form.style.display = 'none';
                    successMessage.classList.add('show');
                    form.reset();
                    
                    // Hide after 5 seconds and show form again
                    setTimeout(() => {
                        successMessage.classList.remove('show');
                        form.style.display = 'flex';
                    }, 5000);
                }
            });
        }
    }

    // ============================================
    // Loading Spinner Utilities
    // ============================================
    const LoadingSpinner = {
        overlay: null,

        init() {
            this.overlay = document.querySelector('.loading-overlay');
            if (!this.overlay) {
                this.overlay = document.createElement('div');
                this.overlay.className = 'loading-overlay';
                this.overlay.innerHTML = '<div class="spinner-large"></div>';
                document.body.appendChild(this.overlay);
            }
        },

        show() {
            if (this.overlay) {
                this.overlay.classList.add('show');
            }
        },

        hide() {
            if (this.overlay) {
                this.overlay.classList.remove('show');
            }
        }
    };

    // ============================================
    // No Results Handler
    // ============================================
    const NoResults = {
        container: null,

        init(containerSelector, onClearCallback) {
            this.container = document.querySelector(containerSelector);
            
            if (this.container) {
                const clearBtn = this.container.querySelector('.btn-clear');
                if (clearBtn && onClearCallback) {
                    clearBtn.addEventListener('click', onClearCallback);
                }
            }
        },

        show() {
            if (this.container) {
                this.container.classList.add('show');
            }
        },

        hide() {
            if (this.container) {
                this.container.classList.remove('show');
            }
        }
    };

    // ============================================
    // Search with Debounce & Loading State
    // ============================================
    function initSearchEnhancement(options) {
        const {
            searchInputSelector = '#search-input',
            resultsContainerSelector = '.cards-section',
            loadingDelay = 300,
            onSearch,
            onClear
        } = options;

        const searchInput = document.querySelector(searchInputSelector);
        const resultsContainer = document.querySelector(resultsContainerSelector);
        let debounceTimer;
        let loadingSpinner;

        // Get or create loading spinner
        function getSpinner() {
            if (!loadingSpinner) {
                loadingSpinner = document.getElementById('search-loading');
            }
            return loadingSpinner;
        }

        if (searchInput && onSearch) {
            searchInput.addEventListener('input', function() {
                const query = this.value.trim();

                // Clear existing timer
                clearTimeout(debounceTimer);

                // Show loading state
                const spinner = getSpinner();
                if (spinner) {
                    spinner.style.display = 'block';
                }

                // Debounce search
                debounceTimer = setTimeout(() => {
                    onSearch(query);
                    
                    // Hide loading state
                    if (spinner) {
                        spinner.style.display = 'none';
                    }
                }, loadingDelay);
            });
        }
    }

    // ============================================
    // Mobile Navigation Toggle
    // ============================================
    function initMobileNav() {
        const navToggle = document.querySelector('.nav-toggle');
        const navLinks = document.querySelector('.nav-links');

        if (navToggle && navLinks) {
            navToggle.addEventListener('click', function() {
                this.classList.toggle('active');
                navLinks.classList.toggle('active');
            });
        }
    }

    // ============================================
    // Intersection Observer for Animations
    // ============================================
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('[data-animate]');
        
        if (animatedElements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(el => observer.observe(el));
    }

    // ============================================
    // Utility: Smooth Scroll to Element
    // ============================================
    function smoothScrollTo(target, offset = 80) {
        const element = typeof target === 'string' 
            ? document.querySelector(target) 
            : target;

        if (element) {
            const top = element.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    }

    // ============================================
    // Utility: Format Number
    // ============================================
    function formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    // ============================================
    // Initialize Everything on DOM Ready
    // ============================================
    function init() {
        initCopyToClipboard();
        initContactForm();
        initMobileNav();
        initScrollAnimations();
        LoadingSpinner.init();
    }

    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose utilities globally
    window.ALLAITOOLS = {
        LoadingSpinner,
        NoResults,
        initSearchEnhancement,
        smoothScrollTo,
        formatNumber
    };

})();
