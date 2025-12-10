"""
Analytics API
NumPy-based analytics endpoints
"""

from flask import Blueprint, request, jsonify
from app.services.analytics_service import AnalyticsService
from app.services.recommendation_service import RecommendationEngine
from app.utils.decorators import log_request

bp = Blueprint('analytics', __name__)


@bp.route('/popular-cities', methods=['GET'])
@log_request
def get_popular_cities():
    """
    Get most popular cities
    Demonstrates: NumPy analytics
    """
    try:
        top_n = request.args.get('limit', 10, type=int)
        popular = AnalyticsService.get_popular_cities(top_n)
        return jsonify(popular)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/budget-insights', methods=['GET'])
@log_request
def get_budget_insights():
    """
    Get budget statistics
    Demonstrates: NumPy statistical operations
    """
    try:
        insights = AnalyticsService.calculate_budget_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/recommendations', methods=['POST'])
@log_request
def get_recommendations():
    """
    Get personalized recommendations
    Demonstrates: NumPy-based recommendation engine
    """
    try:
        preferences = request.get_json() or {}
        top_n = request.args.get('limit', 5, type=int)
        
        engine = RecommendationEngine(preferences)
        recommendations = engine.get_recommendations(top_n)
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/city/<int:city_id>/ratings', methods=['GET'])
@log_request
def get_city_ratings(city_id):
    """Get rating distribution for a city"""
    try:
        distribution = AnalyticsService.get_rating_distribution(city_id)
        return jsonify(distribution)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
