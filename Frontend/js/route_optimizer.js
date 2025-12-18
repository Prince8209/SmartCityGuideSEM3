/**
 * Route Optimizer Module
 * Optimizes travel route using Nearest Neighbor algorithm
 */
const RouteOptimizer = {
    /**
     * Calculate distance between two points using Haversine formula
     * @param {number} lat1 
     * @param {number} lon1 
     * @param {number} lat2 
     * @param {number} lon2 
     * @returns {number} Distance in km
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Radius of the earth in km
        const dLat = this.deg2rad(lat2 - lat1);
        const dLon = this.deg2rad(lon2 - lon1);
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const d = R * c; // Distance in km
        return d;
    },

    deg2rad(deg) {
        return deg * (Math.PI / 180);
    },

    /**
     * Optimize route using Nearest Neighbor algorithm
     * @param {Array} cities - List of city objects with lat/lon
     * @returns {Object} Optimized route and total distance
     */
    optimizeRoute(cities) {
        if (!cities || cities.length <= 1) {
            return {
                route: cities,
                totalDistance: 0
            };
        }

        // Clone cities to avoid modifying original array
        let unvisited = [...cities];
        const route = [];
        let totalDistance = 0;

        // Start with the first city in the list (or user could select start)
        // For now, we assume the first selected city is the starting point
        let currentCity = unvisited.shift();
        route.push(currentCity);

        while (unvisited.length > 0) {
            let nearestCity = null;
            let minDistance = Infinity;
            let nearestIndex = -1;

            unvisited.forEach((city, index) => {
                // If lat/lon missing, assume 0 distance (or handle error)
                if (!currentCity.latitude || !city.latitude) return;

                const dist = this.calculateDistance(
                    currentCity.latitude, currentCity.longitude,
                    city.latitude, city.longitude
                );

                if (dist < minDistance) {
                    minDistance = dist;
                    nearestCity = city;
                    nearestIndex = index;
                }
            });

            if (nearestCity) {
                totalDistance += minDistance;
                currentCity = nearestCity;
                route.push(currentCity);
                unvisited.splice(nearestIndex, 1);
            } else {
                // If we can't calculate distance (missing coords), just add the rest
                route.push(...unvisited);
                break;
            }
        }

        return {
            route: route,
            totalDistance: Math.round(totalDistance)
        };
    }
};

// Expose to window
window.RouteOptimizer = RouteOptimizer;
