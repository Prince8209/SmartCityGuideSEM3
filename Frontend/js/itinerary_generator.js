/**
 * Itinerary Generator Module with Smart Route Optimization
 * Generates optimized day-by-day itineraries with minimal travel distance
 */

const ItineraryGenerator = {
    // City data with attractions and geographical coordinates
    cityData: {
        'Delhi': {
            attractions: [
                { name: 'Red Fort', time: '2-3 hours', type: 'heritage', icon: 'landmark', lat: 28.6562, lng: 77.2410 },
                { name: 'Chandni Chowk', time: '2-3 hours', type: 'market', icon: 'shopping-bag', lat: 28.6506, lng: 77.2303 },
                { name: 'India Gate', time: '1 hour', type: 'monument', icon: 'map-marker-alt', lat: 28.6129, lng: 77.2295 },
                { name: 'Connaught Place', time: '2 hours', type: 'shopping', icon: 'shopping-bag', lat: 28.6315, lng: 77.2167 },
                { name: 'Humayun\'s Tomb', time: '1-2 hours', type: 'heritage', icon: 'landmark', lat: 28.5933, lng: 77.2507 },
                { name: 'Qutub Minar', time: '1-2 hours', type: 'heritage', icon: 'landmark', lat: 28.5244, lng: 77.1855 },
                { name: 'Lotus Temple', time: '1-2 hours', type: 'spiritual', icon: 'praying-hands', lat: 28.5535, lng: 77.2588 },
                { name: 'Akshardham Temple', time: '2-3 hours', type: 'spiritual', icon: 'praying-hands', lat: 28.6127, lng: 77.2773 }
            ],
            meals: ['Paranthe Wali Gali', 'Karim\'s', 'Indian Accent', 'Saravana Bhavan']
        },
        'Mumbai': {
            attractions: [
                { name: 'Gateway of India', time: '1 hour', type: 'monument', icon: 'landmark', lat: 18.9220, lng: 72.8347 },
                { name: 'Colaba Causeway', time: '2 hours', type: 'shopping', icon: 'shopping-bag', lat: 18.9067, lng: 72.8147 },
                { name: 'Marine Drive', time: '1-2 hours', type: 'scenic', icon: 'water', lat: 18.9432, lng: 72.8236 },
                { name: 'Haji Ali Dargah', time: '1 hour', type: 'spiritual', icon: 'praying-hands', lat: 18.9826, lng: 72.8089 },
                { name: 'Siddhivinayak Temple', time: '1 hour', type: 'spiritual', icon: 'praying-hands', lat: 19.0176, lng: 72.8301 },
                { name: 'Bandra-Worli Sea Link', time: '30 min', type: 'scenic', icon: 'car', lat: 19.0330, lng: 72.8181 },
                { name: 'Juhu Beach', time: '1-2 hours', type: 'beach', icon: 'umbrella-beach', lat: 19.0990, lng: 72.8265 },
                { name: 'Elephanta Caves', time: '3-4 hours', type: 'heritage', icon: 'landmark', lat: 18.9633, lng: 72.9315 }
            ],
            meals: ['Leopold Cafe', 'Trishna', 'Britannia & Co', 'Bademiya']
        },
        'Goa': {
            attractions: [
                { name: 'Fort Aguada', time: '1-2 hours', type: 'heritage', icon: 'fort-awesome', lat: 15.4909, lng: 73.7732 },
                { name: 'Calangute Beach', time: '2-3 hours', type: 'beach', icon: 'umbrella-beach', lat: 15.5440, lng: 73.7551 },
                { name: 'Baga Beach', time: '2-3 hours', type: 'beach', icon: 'umbrella-beach', lat: 15.5559, lng: 73.7516 },
                { name: 'Anjuna Flea Market', time: '2-3 hours', type: 'shopping', icon: 'shopping-bag', lat: 15.5736, lng: 73.7401 },
                { name: 'Chapora Fort', time: '1 hour', type: 'heritage', icon: 'fort-awesome', lat: 15.6005, lng: 73.7364 },
                { name: 'Old Goa Churches', time: '2-3 hours', type: 'heritage', icon: 'church', lat: 15.5007, lng: 73.9114 },
                { name: 'Palolem Beach', time: '2-3 hours', type: 'beach', icon: 'umbrella-beach', lat: 15.0100, lng: 74.0233 },
                { name: 'Dudhsagar Falls', time: '4-5 hours', type: 'nature', icon: 'water', lat: 15.3144, lng: 74.3144 }
            ],
            meals: ['Fisherman\'s Wharf', 'Thalassa', 'Britto\'s', 'Vinayak Family Restaurant']
        },
        'Jaipur': {
            attractions: [
                { name: 'Hawa Mahal', time: '1 hour', type: 'heritage', icon: 'landmark', lat: 26.9239, lng: 75.8267 },
                { name: 'City Palace', time: '2 hours', type: 'heritage', icon: 'landmark', lat: 26.9255, lng: 75.8237 },
                { name: 'Jantar Mantar', time: '1-2 hours', type: 'heritage', icon: 'landmark', lat: 26.9246, lng: 75.8247 },
                { name: 'Johari Bazaar', time: '2 hours', type: 'shopping', icon: 'shopping-bag', lat: 26.9196, lng: 75.8242 },
                { name: 'Jal Mahal', time: '30 min', type: 'scenic', icon: 'water', lat: 26.9530, lng: 75.8462 },
                { name: 'Amber Fort', time: '2-3 hours', type: 'heritage', icon: 'fort-awesome', lat: 26.9855, lng: 75.8513 },
                { name: 'Nahargarh Fort', time: '1-2 hours', type: 'heritage', icon: 'fort-awesome', lat: 26.9401, lng: 75.8153 },
                { name: 'Albert Hall Museum', time: '1-2 hours', type: 'museum', icon: 'university', lat: 26.9017, lng: 75.8171 }
            ],
            meals: ['Laxmi Mishthan Bhandar', 'Chokhi Dhani', 'Rawat Mishthan', 'Peacock Rooftop']
        },
        'Bangalore': {
            attractions: [
                { name: 'Vidhana Soudha', time: '30 min', type: 'monument', icon: 'landmark', lat: 12.9796, lng: 77.5909 },
                { name: 'Cubbon Park', time: '1-2 hours', type: 'nature', icon: 'tree', lat: 12.9762, lng: 77.5929 },
                { name: 'Lalbagh Botanical Garden', time: '2 hours', type: 'nature', icon: 'tree', lat: 12.9507, lng: 77.5848 },
                { name: 'Tipu Sultan\'s Palace', time: '1 hour', type: 'heritage', icon: 'landmark', lat: 12.9591, lng: 77.5744 },
                { name: 'MG Road', time: '2 hours', type: 'shopping', icon: 'shopping-bag', lat: 12.9750, lng: 77.6061 },
                { name: 'Bangalore Palace', time: '1-2 hours', type: 'heritage', icon: 'landmark', lat: 12.9980, lng: 77.5920 },
                { name: 'ISKCON Temple', time: '1 hour', type: 'spiritual', icon: 'praying-hands', lat: 13.0093, lng: 77.5509 },
                { name: 'Nandi Hills', time: '3-4 hours', type: 'nature', icon: 'mountain', lat: 13.3703, lng: 77.6838 }
            ],
            meals: ['MTR', 'Vidyarthi Bhavan', 'Koshy\'s', 'Toit Brewpub']
        },
        'Kerala': {
            attractions: [
                { name: 'Fort Kochi', time: '2-3 hours', type: 'heritage', icon: 'fort-awesome', lat: 9.9654, lng: 76.2430 },
                { name: 'Kovalam Beach', time: '2-3 hours', type: 'beach', icon: 'umbrella-beach', lat: 8.4004, lng: 76.9790 },
                { name: 'Padmanabhaswamy Temple', time: '1 hour', type: 'spiritual', icon: 'praying-hands', lat: 8.4829, lng: 76.9494 },
                { name: 'Varkala Beach', time: '2-3 hours', type: 'beach', icon: 'umbrella-beach', lat: 8.7379, lng: 76.7163 },
                { name: 'Alleppey Backwaters', time: '4-6 hours', type: 'nature', icon: 'water', lat: 9.4981, lng: 76.3388 },
                { name: 'Athirapally Falls', time: '2-3 hours', type: 'nature', icon: 'water', lat: 10.2854, lng: 76.5692 },
                { name: 'Munnar Tea Gardens', time: '3-4 hours', type: 'nature', icon: 'leaf', lat: 10.0889, lng: 77.0595 },
                { name: 'Periyar Wildlife Sanctuary', time: '4-5 hours', type: 'nature', icon: 'paw', lat: 9.4647, lng: 77.2355 }
            ],
            meals: ['Paragon Restaurant', 'Dhe Puttu', 'Kayees Rahmathulla', 'Kashi Art Cafe']
        }
    },

    /**
     * Generate itinerary based on user inputs
     */
    generateItinerary() {
        // Get user inputs from the settings panel
        const settingsPanel = document.querySelector('.section .container > div');
        const selects = settingsPanel.querySelectorAll('select');
        const inputs = settingsPanel.querySelectorAll('input[type="number"]');

        const destination = selects[0]?.value || 'Delhi';
        const duration = parseInt(inputs[0]?.value) || 3;
        const budget = parseInt(inputs[1]?.value) || 2000;
        const travelStyle = selects[1]?.value || 'Balanced';

        // Get city data
        const cityInfo = this.cityData[destination] || this.cityData['Delhi'];

        // Generate days with route optimization
        const itinerary = this.createDailyPlan(destination, duration, cityInfo, travelStyle, budget);

        // Render itinerary
        this.renderItinerary(itinerary);
    },

    /**
     * Calculate distance between two points using Haversine formula
     * Returns distance in kilometers
     */
    calculateDistance(lat1, lng1, lat2, lng2) {
        const R = 6371; // Earth's radius in kilometers
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLng = (lng2 - lng1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    },

    /**
     * Optimize route using nearest-neighbor algorithm
     * Returns attractions ordered for minimal travel distance
     */
    optimizeRoute(attractions) {
        if (attractions.length <= 1) return attractions;

        const optimized = [];
        const remaining = [...attractions];

        // Start with the first attraction
        let current = remaining.shift();
        optimized.push(current);

        // Find nearest neighbor for each step
        while (remaining.length > 0) {
            let nearestIndex = 0;
            let minDistance = Infinity;

            // Find the nearest unvisited attraction
            for (let i = 0; i < remaining.length; i++) {
                const distance = this.calculateDistance(
                    current.lat, current.lng,
                    remaining[i].lat, remaining[i].lng
                );
                if (distance < minDistance) {
                    minDistance = distance;
                    nearestIndex = i;
                }
            }

            // Move to nearest attraction
            current = remaining.splice(nearestIndex, 1)[0];
            optimized.push(current);
        }

        return optimized;
    },

    /**
     * Calculate total route distance
     */
    calculateTotalDistance(attractions) {
        let total = 0;
        for (let i = 0; i < attractions.length - 1; i++) {
            total += this.calculateDistance(
                attractions[i].lat, attractions[i].lng,
                attractions[i + 1].lat, attractions[i + 1].lng
            );
        }
        return total.toFixed(1);
    },

    /**
     * Create daily plan with route optimization
     */
    createDailyPlan(destination, duration, cityInfo, style, budget) {
        const days = [];
        const attractionsPerDay = style === 'Relaxed' ? 2 : style === 'Balanced' ? 3 : 4;
        const allAttractions = [...cityInfo.attractions];

        for (let day = 1; day <= duration; day++) {
            const dayPlan = {
                day: day,
                title: this.getDayTitle(day, duration, destination),
                timeOfDay: day === 1 ? 'Morning to Evening' : day === duration ? 'Morning to Afternoon' : 'Full Day',
                activities: [],
                totalDistance: 0
            };

            // Get attractions for this day
            const startIdx = (day - 1) * attractionsPerDay;
            const dayAttractions = allAttractions.slice(startIdx, startIdx + attractionsPerDay);

            // Optimize route for the day using nearest-neighbor algorithm
            const optimizedAttractions = this.optimizeRoute(dayAttractions);

            // Calculate total distance for the day
            if (optimizedAttractions.length > 1) {
                dayPlan.totalDistance = this.calculateTotalDistance(optimizedAttractions);
            }

            // Morning activity
            if (day === 1) {
                dayPlan.activities.push({
                    time: '9:00 AM',
                    title: `Arrive at ${destination}`,
                    description: 'Check into hotel and freshen up',
                    icon: 'clock'
                });
            }

            // Add optimized attractions with distance info
            let currentTime = day === 1 ? 11 : 9;
            optimizedAttractions.forEach((attraction, idx) => {
                const hour = currentTime % 12 || 12;
                const period = currentTime < 12 ? 'AM' : 'PM';

                // Calculate distance from previous location
                let travelInfo = '';
                if (idx > 0) {
                    const distance = this.calculateDistance(
                        optimizedAttractions[idx - 1].lat, optimizedAttractions[idx - 1].lng,
                        attraction.lat, attraction.lng
                    );
                    travelInfo = ` • ${distance.toFixed(1)}km from previous stop`;
                }

                dayPlan.activities.push({
                    time: `${hour}:00 ${period}`,
                    title: attraction.name,
                    description: `Visit this ${attraction.type} attraction (${attraction.time})${travelInfo}`,
                    icon: attraction.icon
                });

                currentTime += 3;

                // Add lunch
                if (idx === 0 && currentTime > 12) {
                    const lunchHour = 1;
                    dayPlan.activities.push({
                        time: `${lunchHour}:00 PM`,
                        title: `Lunch at ${cityInfo.meals[day % cityInfo.meals.length]}`,
                        description: 'Try local cuisine and specialties',
                        icon: 'utensils'
                    });
                    currentTime = 14;
                }
            });

            // Evening activity
            if (day < duration) {
                dayPlan.activities.push({
                    time: '7:00 PM',
                    title: 'Dinner & Leisure',
                    description: 'Explore local markets and enjoy dinner',
                    icon: 'moon'
                });
            }

            days.push(dayPlan);
        }

        return days;
    },

    /**
     * Get appropriate title for each day
     */
    getDayTitle(day, totalDays, destination) {
        if (day === 1) return `Arrival & ${destination} Tour`;
        if (day === totalDays) return 'Final Exploration & Departure';
        if (day === 2) return 'Heritage Sites';
        if (day === 3) return 'Cultural Experience';
        return `Day ${day} Exploration`;
    },

    /**
     * Render the generated itinerary to the DOM
     */
    renderItinerary(days) {
        const container = document.querySelector('.section .container > div > div:last-child');
        if (!container) return;

        // Clear existing content
        container.innerHTML = '<h3 style="margin-bottom: 1.5rem; color: #2d3748;"><i class="fas fa-calendar-alt"></i> Your Optimized Itinerary</h3>';

        // Color gradients for each day
        const gradients = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
        ];

        // Render each day
        days.forEach((dayPlan, index) => {
            const gradient = gradients[index % gradients.length];
            const iconColor = index === 0 ? '#667eea' : index === 1 ? '#4facfe' : '#f093fb';

            const dayCard = document.createElement('div');
            dayCard.style.cssText = 'background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 1.5rem;';

            // Add route optimization badge if distance > 0
            const routeBadge = dayPlan.totalDistance > 0
                ? `<span style="background: #48bb78; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; margin-left: 1rem;">
                     <i class="fas fa-route"></i> Optimized: ${dayPlan.totalDistance}km total
                   </span>`
                : '';

            dayCard.innerHTML = `
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="width: 50px; height: 50px; background: ${gradient}; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; margin-right: 1rem;">
                        DAY ${dayPlan.day}
                    </div>
                    <div style="flex: 1;">
                        <h4 style="margin-bottom: 0.25rem; color: #2d3748;">${dayPlan.title}</h4>
                        <p style="color: #718096; font-size: 0.9rem;">${dayPlan.timeOfDay}</p>
                    </div>
                    ${routeBadge}
                </div>
                <div style="border-left: 3px solid #e2e8f0; padding-left: 1.5rem; margin-left: 1.5rem;">
                    ${dayPlan.activities.map(activity => `
                        <div style="margin-bottom: 1.5rem;">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <i class="fas fa-${activity.icon}" style="color: ${iconColor}; margin-right: 0.5rem;"></i>
                                <strong style="color: #2d3748;">${activity.time} - ${activity.title}</strong>
                            </div>
                            <p style="color: #718096; font-size: 0.95rem; margin-left: 1.8rem;">${activity.description}</p>
                        </div>
                    `).join('')}
                </div>
            `;

            container.appendChild(dayCard);
        });

        // Show success message with route optimization info
        this.showNotification('✨ Smart itinerary with optimized routes generated!', 'success');
    },

    /**
     * Show notification message
     */
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'success' ? '#48bb78' : '#667eea'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Initialize when DOM is ready
if (window.location.pathname.includes('itinerary.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        // Replace the button's onclick
        const generateBtn = document.querySelector('.btn-city');
        if (generateBtn) {
            generateBtn.onclick = () => ItineraryGenerator.generateItinerary();
        }
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Expose to window
window.ItineraryGenerator = ItineraryGenerator;
