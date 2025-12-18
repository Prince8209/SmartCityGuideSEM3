/**
 * Budget Tracker Module
 * Tracks travel expenses and compares against budget
 */

const BudgetTracker = {
    expenses: [],
    budget: 0,
    duration: 1,

    /**
     * Initialize budget tracker
     */
    init(budget, duration) {
        this.budget = budget || 10000;
        this.duration = duration || 3;
        this.expenses = [];
        this.loadFromStorage();
    },

    /**
     * Add expense
     */
    addExpense(category, amount, description) {
        const expense = {
            id: Date.now(),
            category: category,
            amount: parseFloat(amount),
            description: description,
            date: new Date().toISOString()
        };

        this.expenses.push(expense);
        this.saveToStorage();
        return expense;
    },

    /**
     * Remove expense
     */
    removeExpense(id) {
        this.expenses = this.expenses.filter(e => e.id !== id);
        this.saveToStorage();
    },

    /**
     * Get total spent
     */
    getTotalSpent() {
        return this.expenses.reduce((sum, expense) => sum + expense.amount, 0);
    },

    /**
     * Get spending by category
     */
    getSpendingByCategory() {
        const categories = {
            'Accommodation': 0,
            'Food': 0,
            'Transport': 0,
            'Activities': 0,
            'Shopping': 0,
            'Other': 0
        };

        this.expenses.forEach(expense => {
            if (categories.hasOwnProperty(expense.category)) {
                categories[expense.category] += expense.amount;
            }
        });

        return categories;
    },

    /**
     * Get remaining budget
     */
    getRemainingBudget() {
        return this.budget - this.getTotalSpent();
    },

    /**
     * Get budget percentage used
     */
    getBudgetPercentage() {
        return (this.getTotalSpent() / this.budget) * 100;
    },

    /**
     * Get daily average
     */
    getDailyAverage() {
        return this.getTotalSpent() / this.duration;
    },

    /**
     * Get projected total
     */
    getProjectedTotal() {
        return this.getDailyAverage() * this.duration;
    },

    /**
     * Save to localStorage
     */
    saveToStorage() {
        localStorage.setItem('budgetTracker', JSON.stringify({
            expenses: this.expenses,
            budget: this.budget,
            duration: this.duration
        }));
    },

    /**
     * Load from localStorage
     */
    loadFromStorage() {
        const data = localStorage.getItem('budgetTracker');
        if (data) {
            const parsed = JSON.parse(data);
            this.expenses = parsed.expenses || [];
            this.budget = parsed.budget || this.budget;
            this.duration = parsed.duration || this.duration;
        }
    },

    /**
     * Clear all data
     */
    clearAll() {
        this.expenses = [];
        this.saveToStorage();
    },

    /**
     * Get recommendations based on budget and spending
     */
    getRecommendations() {
        const remaining = this.getRemainingBudget();
        const dailyBudget = this.budget / this.duration;
        const categorySpending = this.getSpendingByCategory();

        const recommendations = {
            hotels: [],
            restaurants: [],
            activities: []
        };

        // Hotel recommendations based on accommodation budget
        const accommodationBudget = dailyBudget * 0.4; // 40% of daily budget
        if (accommodationBudget < 1000) {
            recommendations.hotels = [
                { name: 'Budget Hostels', price: '₹500-800/night', rating: '3.5★' },
                { name: 'Zostel', price: '₹600-900/night', rating: '4.0★' },
                { name: 'Backpacker Panda', price: '₹400-700/night', rating: '3.8★' }
            ];
        } else if (accommodationBudget < 2500) {
            recommendations.hotels = [
                { name: 'OYO Rooms', price: '₹1200-2000/night', rating: '3.8★' },
                { name: 'Treebo Hotels', price: '₹1500-2200/night', rating: '4.0★' },
                { name: 'FabHotels', price: '₹1300-2100/night', rating: '3.9★' }
            ];
        } else {
            recommendations.hotels = [
                { name: 'Taj Hotels', price: '₹5000-8000/night', rating: '4.8★' },
                { name: 'ITC Hotels', price: '₹4500-7500/night', rating: '4.7★' },
                { name: 'Oberoi Hotels', price: '₹6000-10000/night', rating: '4.9★' }
            ];
        }

        // Restaurant recommendations based on food budget
        const foodBudget = dailyBudget * 0.3; // 30% of daily budget
        if (foodBudget < 500) {
            recommendations.restaurants = [
                { name: 'Local Dhabas', price: '₹100-200/meal', cuisine: 'Indian' },
                { name: 'Street Food Stalls', price: '₹50-150/meal', cuisine: 'Local' },
                { name: 'Budget Cafes', price: '₹150-250/meal', cuisine: 'Multi-cuisine' }
            ];
        } else if (foodBudget < 1000) {
            recommendations.restaurants = [
                { name: 'Mid-range Restaurants', price: '₹300-500/meal', cuisine: 'Multi-cuisine' },
                { name: 'Popular Chains', price: '₹350-600/meal', cuisine: 'Various' },
                { name: 'Cafe Coffee Day', price: '₹200-400/meal', cuisine: 'Cafe' }
            ];
        } else {
            recommendations.restaurants = [
                { name: 'Fine Dining', price: '₹1000-2000/meal', cuisine: 'Gourmet' },
                { name: 'Luxury Restaurants', price: '₹1500-2500/meal', cuisine: 'International' },
                { name: 'Hotel Restaurants', price: '₹1200-2200/meal', cuisine: 'Multi-cuisine' }
            ];
        }

        // Activity recommendations based on remaining budget
        const activityBudget = dailyBudget * 0.2; // 20% of daily budget
        if (activityBudget < 500) {
            recommendations.activities = [
                { name: 'Free Walking Tours', price: 'Free-₹200', type: 'Sightseeing' },
                { name: 'Public Parks & Gardens', price: '₹20-100', type: 'Nature' },
                { name: 'Local Markets', price: 'Free-₹50', type: 'Shopping' }
            ];
        } else if (activityBudget < 1500) {
            recommendations.activities = [
                { name: 'Museum Visits', price: '₹200-500', type: 'Culture' },
                { name: 'City Tours', price: '₹500-1000', type: 'Sightseeing' },
                { name: 'Adventure Sports', price: '₹800-1200', type: 'Adventure' }
            ];
        } else {
            recommendations.activities = [
                { name: 'Premium Tours', price: '₹2000-3500', type: 'Luxury' },
                { name: 'Hot Air Balloon', price: '₹8000-12000', type: 'Adventure' },
                { name: 'Spa & Wellness', price: '₹2500-5000', type: 'Relaxation' }
            ];
        }

        return recommendations;
    },

    /**
     * Render budget tracker UI
     */
    renderTracker(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const totalSpent = this.getTotalSpent();
        const remaining = this.getRemainingBudget();
        const percentage = this.getBudgetPercentage();
        const dailyAvg = this.getDailyAverage();
        const categorySpending = this.getSpendingByCategory();
        const recommendations = this.getRecommendations();

        // Determine status color
        const statusColor = percentage < 70 ? '#48bb78' : percentage < 90 ? '#ed8936' : '#f56565';

        container.innerHTML = `
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                    <h3 style="color: #2d3748; margin: 0;">
                        <i class="fas fa-wallet"></i> Budget Tracker
                    </h3>
                    <button onclick="BudgetTracker.clearAll(); BudgetTracker.renderTracker('${containerId}')" 
                        style="padding: 0.5rem 1rem; background: #edf2f7; border: none; border-radius: 8px; cursor: pointer; color: #4a5568;">
                        <i class="fas fa-trash"></i> Clear All
                    </button>
                </div>

                <!-- Budget Overview -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 12px;">
                        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.5rem;">Total Budget</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2d3748;">₹${this.budget.toLocaleString()}</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 12px;">
                        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.5rem;">Spent</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: ${statusColor};">₹${totalSpent.toLocaleString()}</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 12px;">
                        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.5rem;">Remaining</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: ${remaining >= 0 ? '#48bb78' : '#f56565'};">₹${remaining.toLocaleString()}</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 12px;">
                        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.5rem;">Daily Avg</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2d3748;">₹${dailyAvg.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div style="margin-bottom: 2rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.9rem; color: #4a5568;">Budget Usage</span>
                        <span style="font-size: 0.9rem; font-weight: 600; color: ${statusColor};">${percentage.toFixed(1)}%</span>
                    </div>
                    <div style="width: 100%; height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden;">
                        <div style="width: ${Math.min(percentage, 100)}%; height: 100%; background: ${statusColor}; transition: width 0.3s ease;"></div>
                    </div>
                    ${percentage > 90 ? '<p style="color: #f56565; font-size: 0.85rem; margin-top: 0.5rem;"><i class="fas fa-exclamation-triangle"></i> Warning: Approaching budget limit!</p>' : ''}
                </div>

                <!-- Recommendations Section -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
                    <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                        <i class="fas fa-lightbulb"></i> Recommendations Within Your Budget
                    </h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <!-- Hotels -->
                        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i class="fas fa-bed"></i> Hotels
                            </div>
                            ${recommendations.hotels.map(hotel => `
                                <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                                    <div style="font-weight: 500;">${hotel.name}</div>
                                    <div style="opacity: 0.9; font-size: 0.85rem;">${hotel.price} • ${hotel.rating}</div>
                                </div>
                            `).join('')}
                        </div>
                        <!-- Restaurants -->
                        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i class="fas fa-utensils"></i> Restaurants
                            </div>
                            ${recommendations.restaurants.map(rest => `
                                <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                                    <div style="font-weight: 500;">${rest.name}</div>
                                    <div style="opacity: 0.9; font-size: 0.85rem;">${rest.price} • ${rest.cuisine}</div>
                                </div>
                            `).join('')}
                        </div>
                        <!-- Activities -->
                        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i class="fas fa-ticket-alt"></i> Activities
                            </div>
                            ${recommendations.activities.map(activity => `
                                <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                                    <div style="font-weight: 500;">${activity.name}</div>
                                    <div style="opacity: 0.9; font-size: 0.85rem;">${activity.price} • ${activity.type}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Category Breakdown -->
                <div style="margin-bottom: 2rem;">
                    <h4 style="color: #2d3748; margin-bottom: 1rem; font-size: 1rem;">Spending by Category</h4>
                    <div style="display: grid; gap: 0.75rem;">
                        ${Object.entries(categorySpending).map(([category, amount]) => {
            const catPercentage = this.budget > 0 ? (amount / this.budget) * 100 : 0;
            const icons = {
                'Accommodation': 'bed',
                'Food': 'utensils',
                'Transport': 'car',
                'Activities': 'ticket-alt',
                'Shopping': 'shopping-bag',
                'Other': 'ellipsis-h'
            };
            return `
                                <div>
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                        <span style="font-size: 0.9rem; color: #4a5568;">
                                            <i class="fas fa-${icons[category]}"></i> ${category}
                                        </span>
                                        <span style="font-size: 0.9rem; font-weight: 600; color: #2d3748;">₹${amount.toLocaleString()}</span>
                                    </div>
                                    <div style="width: 100%; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden;">
                                        <div style="width: ${catPercentage}%; height: 100%; background: #667eea;"></div>
                                    </div>
                                </div>
                            `;
        }).join('')}
                    </div>
                </div>

                <!-- Add Expense Form -->
                <div style="border-top: 2px solid #e2e8f0; padding-top: 1.5rem;">
                    <h4 style="color: #2d3748; margin-bottom: 1rem; font-size: 1rem;">Add Expense</h4>
                    <div style="display: grid; gap: 1rem;">
                        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1rem;">
                            <select id="expenseCategory" style="padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1rem;">
                                <option value="Accommodation">Accommodation</option>
                                <option value="Food">Food</option>
                                <option value="Transport">Transport</option>
                                <option value="Activities">Activities</option>
                                <option value="Shopping">Shopping</option>
                                <option value="Other">Other</option>
                            </select>
                            <input type="number" id="expenseAmount" placeholder="Amount (₹)" 
                                style="padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1rem;">
                        </div>
                        <input type="text" id="expenseDescription" placeholder="Description (optional)" 
                            style="padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1rem;">
                        <button onclick="BudgetTracker.handleAddExpense('${containerId}')" class="btn-city" style="width: 100%;">
                            <i class="fas fa-plus"></i> Add Expense
                        </button>
                    </div>
                </div>

                <!-- Recent Expenses -->
                ${this.expenses.length > 0 ? `
                    <div style="border-top: 2px solid #e2e8f0; padding-top: 1.5rem; margin-top: 1.5rem;">
                        <h4 style="color: #2d3748; margin-bottom: 1rem; font-size: 1rem;">Recent Expenses</h4>
                        <div style="max-height: 300px; overflow-y: auto;">
                            ${this.expenses.slice().reverse().slice(0, 10).map(expense => `
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: #f7fafc; border-radius: 8px; margin-bottom: 0.5rem;">
                                    <div>
                                        <div style="font-weight: 600; color: #2d3748;">${expense.category}</div>
                                        ${expense.description ? `<div style="font-size: 0.85rem; color: #718096;">${expense.description}</div>` : ''}
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 1rem;">
                                        <span style="font-weight: 700; color: #2d3748;">₹${expense.amount.toLocaleString()}</span>
                                        <button onclick="BudgetTracker.removeExpense(${expense.id}); BudgetTracker.renderTracker('${containerId}')" 
                                            style="padding: 0.25rem 0.5rem; background: #fed7d7; color: #c53030; border: none; border-radius: 4px; cursor: pointer;">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    },

    /**
     * Handle add expense button click
     */
    handleAddExpense(containerId) {
        const category = document.getElementById('expenseCategory').value;
        const amount = parseFloat(document.getElementById('expenseAmount').value);
        const description = document.getElementById('expenseDescription').value;

        if (!amount || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }

        this.addExpense(category, amount, description);
        this.renderTracker(containerId);

        // Clear form
        document.getElementById('expenseAmount').value = '';
        document.getElementById('expenseDescription').value = '';
    }
};

// Expose to window
window.BudgetTracker = BudgetTracker;
