"""
Analytics Service with PostgreSQL
NumPy-based analytics and statistics
"""

import numpy as np
from app.models import City, Review, Itinerary
from sqlalchemy import func


class AnalyticsService:
    """
    Travel analytics using NumPy and PostgreSQL
    """
    
    @staticmethod
    def calculate_budget_insights():
        """Calculate budget statistics using NumPy"""
        from app.database.config import db
        
        # Get all budgets
        budgets = db.session.query(Itinerary.total_budget).filter(
            Itinerary.total_budget > 0
        ).all()
        
        if not budgets:
            return {
                'mean_budget': 0,
                'median_budget': 0,
                'std_budget': 0,
                'min_budget': 0,
                'max_budget': 0
            }
        
        budget_array = np.array([b[0] for b in budgets])
        
        return {
            'mean_budget': float(np.mean(budget_array)),
            'median_budget': float(np.median(budget_array)),
            'std_budget': float(np.std(budget_array)),
            'min_budget': float(np.min(budget_array)),
            'max_budget': float(np.max(budget_array)),
            'percentile_25': float(np.percentile(budget_array, 25)),
            'percentile_75': float(np.percentile(budget_array, 75))
        }
    
    @staticmethod
    def get_popular_cities(top_n=10):
        """Get most popular cities based on reviews"""
        from app.database.config import db
        
        # Get average ratings and review counts per city
        city_stats = db.session.query(
            Review.city_id,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).filter(
            Review.city_id.isnot(None)
        ).group_by(Review.city_id).all()
        
        if not city_stats:
            return []
        
        popularity_scores = []
        
        for city_id, avg_rating, review_count in city_stats:
            # Popularity = (avg_rating * 0.7) + (normalized_review_count * 0.3)
            popularity = (float(avg_rating) * 0.7) + (min(review_count / 100, 1) * 0.3)
            
            city = City.query.get(city_id)
            if city:
                popularity_scores.append({
                    'city': city.to_dict(),
                    'popularity_score': float(popularity),
                    'avg_rating': float(avg_rating),
                    'review_count': review_count
                })
        
        # Sort by popularity
        sorted_cities = sorted(
            popularity_scores,
            key=lambda x: x['popularity_score'],
            reverse=True
        )
        
        return sorted_cities[:top_n]
    
    @staticmethod
    def get_rating_distribution(city_id):
        """Get rating distribution for a city"""
        from app.database.config import db
        
        ratings = db.session.query(Review.rating).filter_by(city_id=city_id).all()
        
        if not ratings:
            return {
                'distribution': [0, 0, 0, 0, 0],
                'total_reviews': 0,
                'average_rating': 0
            }
        
        ratings_array = np.array([r[0] for r in ratings])
        
        # Count ratings (1-5)
        distribution = np.bincount(ratings_array.astype(int), minlength=6)[1:]
        
        return {
            'distribution': distribution.tolist(),
            'total_reviews': len(ratings),
            'average_rating': float(np.mean(ratings_array))
        }
