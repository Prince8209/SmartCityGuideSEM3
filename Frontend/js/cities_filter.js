/**
 * Cities Filter and Sort Module
 * Handles filtering and sorting of city cards on the cities page
 */

const CitiesFilterSort = {
    cities: [],

    /**
     * Initialize the filter and sort functionality
     */
    init() {
        this.loadCities();
        this.setupEventListeners();
    },

    /**
     * Load all city cards from the DOM
     */
    loadCities() {
        const container = document.getElementById('citiesContainer');
        if (!container) return;

        const cityCards = container.querySelectorAll('.city-card');
        this.cities = Array.from(cityCards).map(card => {
            const name = card.querySelector('.city-name')?.textContent || '';
            const budgetText = card.querySelector('.city-stat .fa-rupee-sign')?.parentElement?.textContent || '';
            const budget = parseInt(budgetText.replace(/[^0-9]/g, '')) || 0;
            const region = this.detectRegion(name);

            return {
                element: card,
                name: name.trim(),
                budget: budget,
                region: region,
                description: card.querySelector('.city-desc')?.textContent.toLowerCase() || ''
            };
        });
    },

    /**
     * Detect region based on city name (simple mapping)
     */
    detectRegion(cityName) {
        const regionMap = {
            'North': ['Delhi', 'Agra', 'Shimla', 'Manali', 'Jaipur', 'Udaipur'],
            'South': ['Bangalore', 'Kerala', 'Chennai', 'Hyderabad'],
            'West': ['Mumbai', 'Goa', 'Pune'],
            'East': ['Kolkata', 'Varanasi', 'Darjeeling']
        };

        for (const [region, cities] of Object.entries(regionMap)) {
            if (cities.some(city => cityName.includes(city))) {
                return region;
            }
        }
        return 'Other';
    },

    /**
     * Setup event listeners for filters and sort
     */
    setupEventListeners() {
        const searchInput = document.getElementById('citySearch');
        const regionFilter = document.getElementById('regionFilter');
        const budgetFilter = document.getElementById('budgetFilter');
        const sortBy = document.getElementById('sortBy');
        const clearBtn = document.getElementById('clearFilters');

        if (searchInput) {
            searchInput.addEventListener('input', () => this.applyFiltersAndSort());
        }

        if (regionFilter) {
            regionFilter.addEventListener('change', () => this.applyFiltersAndSort());
        }

        if (budgetFilter) {
            budgetFilter.addEventListener('change', () => this.applyFiltersAndSort());
        }

        if (sortBy) {
            sortBy.addEventListener('change', () => this.applyFiltersAndSort());
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearFilters());
        }
    },

    /**
     * Apply all filters and sorting
     */
    applyFiltersAndSort() {
        const searchTerm = document.getElementById('citySearch')?.value.toLowerCase() || '';
        const selectedRegion = document.getElementById('regionFilter')?.value || '';
        const maxBudget = parseInt(document.getElementById('budgetFilter')?.value) || Infinity;
        const sortOption = document.getElementById('sortBy')?.value || 'name-asc';

        // Filter cities
        let filteredCities = this.cities.filter(city => {
            // Search filter
            if (searchTerm && !city.name.toLowerCase().includes(searchTerm) &&
                !city.description.includes(searchTerm)) {
                return false;
            }

            // Region filter
            if (selectedRegion && city.region !== selectedRegion) {
                return false;
            }

            // Budget filter
            if (city.budget > maxBudget) {
                return false;
            }

            return true;
        });

        // Sort cities
        filteredCities.sort((a, b) => {
            switch (sortOption) {
                case 'name-asc':
                    return a.name.localeCompare(b.name);
                case 'name-desc':
                    return b.name.localeCompare(a.name);
                case 'budget-asc':
                    return a.budget - b.budget;
                case 'budget-desc':
                    return b.budget - a.budget;
                default:
                    return 0;
            }
        });

        this.renderCities(filteredCities);
    },

    /**
     * Render filtered and sorted cities
     */
    renderCities(filteredCities) {
        const container = document.getElementById('citiesContainer');
        if (!container) return;

        // Clear container
        container.innerHTML = '';

        if (filteredCities.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #718096;">
                    <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <p style="font-size: 1.2rem;">No cities found matching your criteria</p>
                    <button onclick="CitiesFilterSort.clearFilters()" class="btn-city" style="margin-top: 1rem;">
                        Clear Filters
                    </button>
                </div>
            `;
            return;
        }

        // Append filtered cities in sorted order
        filteredCities.forEach(city => {
            container.appendChild(city.element);
        });
    },

    /**
     * Clear all filters
     */
    clearFilters() {
        const searchInput = document.getElementById('citySearch');
        const regionFilter = document.getElementById('regionFilter');
        const budgetFilter = document.getElementById('budgetFilter');
        const sortBy = document.getElementById('sortBy');

        if (searchInput) searchInput.value = '';
        if (regionFilter) regionFilter.value = '';
        if (budgetFilter) budgetFilter.value = '';
        if (sortBy) sortBy.value = 'name-asc';

        this.applyFiltersAndSort();
    }
};

// Initialize when DOM is ready
if (window.location.pathname.includes('cities.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        CitiesFilterSort.init();
    });
}

// Expose to window for onclick handlers
window.CitiesFilterSort = CitiesFilterSort;
