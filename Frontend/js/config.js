/**
 * API Configuration
 * Backend endpoint URLs
 */
const API_CONFIG = {
    // Check if running on localhost, otherwise use production URL (to be updated after deployment)
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000/api'
        : 'https://smart-city-guide-backend.onrender.com/api', // Placeholder - Update this after deploying backend
    ENDPOINTS: {
        // Cities
        CITIES: '/cities',
        CITY_BY_ID: (id) => `/cities/${id}`,
        REGIONS: '/cities/regions',
        TRIP_TYPES: '/cities/trip-types',
        ATTRACTION_CATEGORIES: '/cities/attraction-categories',

        // Auth
        LOGIN: '/auth/login',
        SIGNUP: '/auth/signup',

        // Bookings
        BOOKINGS: '/bookings',

        // Reviews
        REVIEWS: '/reviews',

        // Upload
        UPLOAD: '/upload/local'
    }
};
