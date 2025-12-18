/**
 * Budget Tracker Module
 * Handles trip expense calculations and budget management
 */
const BudgetTracker = {
    // Standard costs (can be updated from API/backend later)
    defaults: {
        foodPerDay: 500,
        transportPerDay: 300,
        miscPerDay: 200
    },

    /**
     * Calculate total estimated budget
     * @param {Array} cities - List of selected city objects
     * @param {number} travelers - Number of travelers
     * @returns {Object} Breakdown of costs
     */
    calculateBudget(cities, travelers = 1) {
        let totalAccommodation = 0;
        let totalFood = 0;
        let totalTransport = 0;
        let totalActivities = 0;
        let totalDays = 0;

        cities.forEach(city => {
            // Parse days (e.g., "3-5 days" -> take average 4, or min 3)
            // For safety, let's take the lower bound or default to 2
            let days = 2;
            if (city.recommended_days) {
                const match = city.recommended_days.match(/(\d+)/);
                if (match) days = parseInt(match[0]);
            }
            totalDays += days;

            // Accommodation (Avg budget usually includes stay + basic food, but let's assume it's mostly stay)
            // If avg_budget_per_day is provided, use it. Else default to 1500.
            const dailyCost = city.avg_budget_per_day || 1500;

            // We'll assume avg_budget_per_day covers accommodation + food for one person
            // But to be more granular:
            // Let's assume 60% is stay, 40% is food/others if we only have one number.
            // Or just use the number as "Base Daily Cost"

            totalAccommodation += (dailyCost * 0.6) * days;
            totalFood += (dailyCost * 0.4) * days;

            // Add extra for activities (rough estimate)
            totalActivities += 500 * days;
        });

        // Transport between cities (Rough estimate: ₹1000 per city transfer)
        // If N cities, N-1 transfers + arrival/departure = N transfers approx
        const interCityTransport = cities.length * 1000;

        // Local transport within cities
        const localTransport = this.defaults.transportPerDay * totalDays;

        totalTransport = interCityTransport + localTransport;

        // Multiply by travelers
        const grandTotal = (totalAccommodation + totalFood + totalTransport + totalActivities) * travelers;

        return {
            accommodation: Math.round(totalAccommodation * travelers),
            food: Math.round(totalFood * travelers),
            transport: Math.round(totalTransport * travelers),
            activities: Math.round(totalActivities * travelers),
            total: Math.round(grandTotal),
            days: totalDays,
            perPerson: Math.round(grandTotal / travelers)
        };
    },

    /**
     * Format currency
     */
    formatMoney(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    }
};

// Expose to window
window.BudgetTracker = BudgetTracker;
