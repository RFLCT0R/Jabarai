/**
 * ALLAITOOLS - Search & Filter UI Enhancements
 * Adds loading states, no results messaging, and improved search UX
 * 
 * Usage: Include this file after your main search/filter logic
 * Initialize: ALLAITOOLS.SearchEnhancements.init()
 */

(function() {
    'use strict';

    const SearchEnhancements = {
        // Configuration
        config: {
            searchInputSelector: '#search-input',
            resultsContainerSelector: '.cards-section',
            loadingSpinnerSelector: '#search-loading',
            debounceDelay: 300,
            minSearchLength: 2
        },

        // State
        state: {
            isSearching: false,
            lastQuery: '',
            debounceTimer: null
        },

        // DOM Elements
        elements: {},

        /**
         * Initialize the enhancements
         * @param {Object} options - Override default configuration
         */
        init(options = {}) {
            this.config = { ...this.config, ...options };
            this.cacheElements();
            this.createNoResultsElement();
            this.bindEvents();
        },

        /**
         * Cache DOM elements for performance
         */
        cacheElements() {
            this.elements.searchInput = document.querySelector(this.config.searchInputSelector);
            this.elements.resultsContainer = document.querySelector(this.config.resultsContainerSelector);
            this.elements.loadingSpinner = document.querySelector(this.config.loadingSpinnerSelector);
            
            // If no loading spinner exists in HTML, create one
            if (!this.elements.loadingSpinner && this.elements.searchInput) {
                this.createLoadingSpinner();
            }
        },

        /**
         * Create loading spinner if not present in HTML
         */
        createLoadingSpinner() {
            const spinner = document.createElement('div');
            spinner.id = 'search-loading';
            spinner.className = 'search-spinner';
            spinner.style.cssText = `
                position: absolute;
                right: 14px;
                top: 50%;
                transform: translateY(-50%);
                width: 16px;
                height: 16px;
                border: 2px solid #e0e0e0;
                border-top-color: #4f46e5;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                display: none;
            `;
            
            // Add keyframes if not already present
            if (!document.getElementById('search-spinner-styles')) {
                const style = document.createElement('style');
                style.id = 'search-spinner-styles';
                style.textContent = `
                    @keyframes spin {
                        to { transform: translateY(-50%) rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
            }

            const searchContainer = this.elements.searchInput.closest('.search-container, .search-container-compact');
            if (searchContainer) {
                searchContainer.style.position = 'relative';
                searchContainer.appendChild(spinner);
                this.elements.loadingSpinner = spinner;
            }
        },

        /**
         * Create no results message element
         */
        createNoResultsElement() {
            if (!this.elements.resultsContainer) return;

            // Check if already exists
            let noResults = document.getElementById('no-results-message');
            
            if (!noResults) {
                noResults = document.createElement('div');
                noResults.id = 'no-results-message';
                noResults.className = 'no-results';
                noResults.innerHTML = `
                    <div class="no-results-icon">🔍</div>
                    <h3>No tools found</h3>
                    <p>Try adjusting your filters or search term.</p>
                    <button class="btn-clear" id="clear-filters-btn">
                        <i class="fas fa-undo"></i> Clear all filters
                    </button>
                `;
                
                // Add styles if not present
                if (!document.getElementById('no-results-styles')) {
                    const style = document.createElement('style');
                    style.id = 'no-results-styles';
                    style.textContent = `
                        .no-results {
                            text-align: center;
                            padding: 60px 24px;
                            display: none;
                        }
                        .no-results.show {
                            display: block;
                        }
                        .no-results-icon {
                            font-size: 48px;
                            margin-bottom: 16px;
                            opacity: 0.5;
                        }
                        .no-results h3 {
                            font-size: 18px;
                            font-weight: 600;
                            color: #374151;
                            margin-bottom: 8px;
                        }
                        .no-results p {
                            font-size: 14px;
                            color: #6b7280;
                            margin-bottom: 20px;
                        }
                        .btn-clear {
                            background: #ffffff;
                            border: 1px solid #d1d5db;
                            color: #374151;
                            padding: 10px 20px;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 500;
                            cursor: pointer;
                            transition: all 0.2s;
                            font-family: 'Inter', Arial, sans-serif;
                        }
                        .btn-clear:hover {
                            background: #f9fafb;
                            border-color: #9ca3af;
                        }
                        .btn-clear i {
                            margin-right: 6px;
                        }
                    `;
                    document.head.appendChild(style);
                }

                // Insert after the results container
                this.elements.resultsContainer.parentNode.insertBefore(
                    noResults, 
                    this.elements.resultsContainer.nextSibling
                );
                this.elements.noResults = noResults;
            }
        },

        /**
         * Bind event listeners
         */
        bindEvents() {
            if (this.elements.searchInput) {
                // Input event with debouncing
                this.elements.searchInput.addEventListener('input', (e) => {
                    this.handleSearchInput(e.target.value);
                });

                // Clear on Escape key
                this.elements.searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        this.clearSearch();
                    }
                });
            }

            // Clear filters button
            const clearBtn = document.getElementById('clear-filters-btn');
            if (clearBtn) {
                clearBtn.addEventListener('click', () => {
                    this.clearAllFilters();
                });
            }
        },

        /**
         * Handle search input with debouncing
         * @param {string} query - The search query
         */
        handleSearchInput(query) {
            // Clear existing timer
            clearTimeout(this.state.debounceTimer);

            // Show loading immediately
            this.showLoading();
            this.state.lastQuery = query;

            // Debounce the actual search
            this.state.debounceTimer = setTimeout(() => {
                this.performSearch(query);
            }, this.config.debounceDelay);
        },

        /**
         * Show loading spinner
         */
        showLoading() {
            if (this.elements.loadingSpinner) {
                this.elements.loadingSpinner.style.display = 'block';
            }
            this.state.isSearching = true;
        },

        /**
         * Hide loading spinner
         */
        hideLoading() {
            if (this.elements.loadingSpinner) {
                this.elements.loadingSpinner.style.display = 'none';
            }
            this.state.isSearching = false;
        },

        /**
         * Perform the actual search
         * Override this method or use callbacks for custom search logic
         * @param {string} query - The search query
         */
        performSearch(query) {
            // This is a placeholder - integrate with your existing search logic
            // Call your existing search function here
            
            // Example integration:
            // if (window.performToolSearch) {
            //     window.performToolSearch(query);
            // }

            // After search completes, check results and update UI
            setTimeout(() => {
                this.hideLoading();
                this.checkResults();
            }, 100);

            // Dispatch custom event for integration with existing code
            window.dispatchEvent(new CustomEvent('searchQueryChanged', { 
                detail: { query } 
            }));
        },

        /**
         * Check if there are any results and show/hide no results message
         */
        checkResults() {
            if (!this.elements.resultsContainer || !this.elements.noResults) return;

            const visibleCards = this.elements.resultsContainer.querySelectorAll(
                '.info-card:not([style*="display: none"]):not(.hidden)'
            );

            if (visibleCards.length === 0) {
                this.showNoResults();
            } else {
                this.hideNoResults();
            }
        },

        /**
         * Show no results message
         */
        showNoResults() {
            if (this.elements.noResults) {
                this.elements.noResults.classList.add('show');
            }
            if (this.elements.resultsContainer) {
                this.elements.resultsContainer.style.display = 'none';
            }
        },

        /**
         * Hide no results message
         */
        hideNoResults() {
            if (this.elements.noResults) {
                this.elements.noResults.classList.remove('show');
            }
            if (this.elements.resultsContainer) {
                this.elements.resultsContainer.style.display = '';
            }
        },

        /**
         * Clear search input and reset
         */
        clearSearch() {
            if (this.elements.searchInput) {
                this.elements.searchInput.value = '';
                this.elements.searchInput.focus();
            }
            this.handleSearchInput('');
        },

        /**
         * Clear all filters and search
         */
        clearAllFilters() {
            // Clear search input
            this.clearSearch();

            // Clear category filters
            document.querySelectorAll('input[name="category"]:checked').forEach(cb => {
                cb.checked = false;
            });

            // Clear pricing filters
            document.querySelectorAll('input[name="pricing"]:checked').forEach(cb => {
                cb.checked = false;
            });

            // Dispatch event for filter change
            window.dispatchEvent(new CustomEvent('filtersCleared'));

            // Trigger update
            this.performSearch('');
        },

        /**
         * Manually trigger a results check (call this after your filter logic updates)
         */
        refreshResults() {
            this.checkResults();
        },

        /**
         * Set a callback for when search is performed
         * @param {Function} callback 
         */
        onSearch(callback) {
            window.addEventListener('searchQueryChanged', (e) => {
                callback(e.detail.query);
            });
        },

        /**
         * Set a callback for when filters are cleared
         * @param {Function} callback 
         */
        onClearFilters(callback) {
            window.addEventListener('filtersCleared', callback);
        }
    };

    // Expose to global scope
    window.ALLAITOOLS = window.ALLAITOOLS || {};
    window.ALLAITOOLS.SearchEnhancements = SearchEnhancements;

    // Auto-initialize if data-auto-init attribute is present
    document.addEventListener('DOMContentLoaded', () => {
        if (document.querySelector('[data-search-enhancements]')) {
            SearchEnhancements.init();
        }
    });

})();
