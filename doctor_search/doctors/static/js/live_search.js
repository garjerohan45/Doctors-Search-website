/**
 * Live Doctor Search - AJAX Implementation
 * Fetches search results in real-time without page reload
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const nameInput = document.getElementById('name');
    const locationInput = document.getElementById('location');
    const minExperienceInput = document.getElementById('min_experience');
    const resultsContainer = document.querySelector('.results-container');
    const submitButton = searchForm.querySelector('button[type="submit"]');
    
    let searchTimeout;

    /**
     * Perform live search with debouncing
     */
    function performLiveSearch() {
        clearTimeout(searchTimeout);
        
        // Debounce search to avoid too many requests
        searchTimeout = setTimeout(() => {
            const name = nameInput.value.trim();
            const location = locationInput.value.trim();
            const minExperience = minExperienceInput.value.trim();

            // Show loading indicator
            showLoading();

            // Build query string
            const params = new URLSearchParams();
            if (name) params.append('name', name);
            if (location) params.append('location', location);
            if (minExperience) params.append('min_experience', minExperience);

            // Construct API URL
            const apiUrl = '/api/doctors/search/?' + params.toString();

            // Fetch results from API
            fetch(apiUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    displayResults(data.results);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    showError('Failed to fetch results. Please try again.');
                });
        }, 500); // Wait 500ms after user stops typing
    }

    /**
     * Display search results dynamically
     */
    function displayResults(doctors) {
        resultsContainer.innerHTML = '';

        if (doctors.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h2>No Doctors Found</h2>
                    <p>Try adjusting your search criteria to find available doctors.</p>
                </div>
            `;
            return;
        }

        // Create results header
        const resultsHeader = document.createElement('div');
        resultsHeader.className = 'results-header';
        resultsHeader.innerHTML = `
            Search Results
            <span class="result-count">${doctors.length} found</span>
        `;
        resultsContainer.appendChild(resultsHeader);

        // Create results grid
        const grid = document.createElement('div');
        grid.className = 'results-grid';

        // Create doctor cards
        doctors.forEach(doctor => {
            const card = createDoctorCard(doctor);
            grid.appendChild(card);
        });

        resultsContainer.appendChild(grid);
    }

    /**
     * Create a single doctor card element
     */
    function createDoctorCard(doctor) {
        const card = document.createElement('div');
        card.className = 'doctor-card';
        card.innerHTML = `
            <div class="doctor-card-header">
                <h3>${escapeHtml(doctor.name)}</h3>
                <div class="doctor-card-specialization">${escapeHtml(doctor.specialization)}</div>
            </div>
            <div class="doctor-card-body">
                <div class="doctor-info">
                    <div class="info-icon">📍</div>
                    <div class="info-content">
                        <div class="info-label">Location</div>
                        <div class="info-value">${escapeHtml(doctor.location)}</div>
                    </div>
                </div>
                <div class="doctor-info">
                    <div class="info-icon">⭐</div>
                    <div class="info-content">
                        <div class="info-label">Experience</div>
                        <div class="info-value">${doctor.experience} years</div>
                    </div>
                </div>
                <div class="doctor-info">
                    <div class="info-icon">📞</div>
                    <div class="info-content">
                        <div class="info-label">Contact</div>
                        <div class="info-value">${escapeHtml(doctor.contact)}</div>
                    </div>
                </div>
                <a href="/book/${doctor.id}/" class="contact-btn">📅 Book Appointment</a>
            </div>
        `;
        return card;
    }

    /**
     * Show loading indicator
     */
    function showLoading() {
        resultsContainer.innerHTML = `
            <div class="loading-container">
                <div class="spinner"></div>
                <p class="loading-text">Searching doctors...</p>
            </div>
        `;
    }

    /**
     * Show error message
     */
    function showError(message) {
        resultsContainer.innerHTML = `
            <div class="error-container">
                <div class="error-icon">⚠️</div>
                <p class="error-text">${escapeHtml(message)}</p>
            </div>
        `;
    }

    /**
     * Escape HTML to prevent XSS attacks
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Handle form submission
     */
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performLiveSearch();
    });

    /**
     * Add event listeners for live search
     */
    nameInput.addEventListener('input', performLiveSearch);
    locationInput.addEventListener('input', performLiveSearch);
    minExperienceInput.addEventListener('input', performLiveSearch);

    /**
     * Perform initial search on page load if parameters exist
     */
    if (nameInput.value || locationInput.value || minExperienceInput.value) {
        performLiveSearch();
    }
});
