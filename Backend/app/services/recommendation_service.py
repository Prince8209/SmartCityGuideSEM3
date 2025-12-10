"""
Recommendation Service with PostgreSQL
NumPy-based recommendation engine
"""

import numpy as np
from app.models import City, Review
from sqlalchemy import func


class RecommendationEngine:
    """
    Recommendation system using NumPy and PostgreSQL
    """
    
    def __init__(self, user_preferences=None):
        self.preferences = user_preferences or {}
        # Weights: [budget, rating, season_match, category_match]
        self.weights = np.array([0.3, 0.3, 0.2, 0.2])
    
    def get_recommendations(self, top_n=5):
        """Get top N city recommendations"""
        cities = City.query.all()
        
        if not cities:
            return []
        
        # Calculate scores for all cities
        scores = np.array([self._calculate_score(city) for city in cities])
        
        # Get top N indices
        top_indices = np.argsort(scores)[-top_n:][::-1]
        
        # Return top cities with scores
        recommendations = []
        for idx in top_indices:
            recommendations.append({
                'city': cities[idx].to_dict(),
                'score': float(scores[idx]),
                'match_percentage': float(scores[idx] * 100)
            })
        
        return recommendations
    
    def _calculate_score(self, city):
        """Calculate recommendation score using NumPy"""
        features = np.array([
            self._budget_score(city.avg_budget_per_day),
            self._rating_score(city),
            self._season_score(city.best_season),
            self._category_score(city.category)
        ])
        
        # Weighted dot product
        score = np.dot(features, self.weights)
        return score
    
    def _budget_score(self, budget):
        """Normalize budget score"""
        if not budget:
            return 0.5
        
        max_budget = self.preferences.get('max_budget', 3000)
        if budget > max_budget:
            return 0.0
        return 1.0 - (budget / max_budget)
    
    def _rating_score(self, city):
        """Get rating score from reviews"""
        from app.database.config import db
        
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(
            city_id=city.id
        ).scalar()
        
        if not avg_rating:
            return 0.5
        
        return float(avg_rating) / 5.0
    
    def _season_score(self, season):
        """Season matching score"""
        preferred = self.preferences.get('season')
        if not preferred:
            return 0.5
        return 1.0 if season == preferred else 0.3
    
    def _category_score(self, category):
        """Category matching score"""
        preferred = self.preferences.get('categories', [])
        if not preferred:
            return 0.5
        return 1.0 if category in preferred else 0.3
