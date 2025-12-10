"""
Itineraries API with PostgreSQL
"""

from flask import Blueprint, request, jsonify
from app.models import db, Itinerary, City
from app.utils.decorators import require_auth, log_request
from app.services.route_optimizer import RouteOptimizer

bp = Blueprint('itineraries', __name__)


@bp.route('', methods=['GET'])
@require_auth
@log_request
def get_itineraries():
    """Get user's itineraries"""
    try:
        itineraries = Itinerary.query.filter_by(user_id=request.user_id).all()
        return jsonify([i.to_dict() for i in itineraries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
@require_auth
@log_request
def create_itinerary():
    """Create new itinerary"""
    try:
        data = request.get_json()
        
        itinerary = Itinerary(
            user_id=request.user_id,
            title=data.get('title'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            total_budget=data.get('total_budget', 0),
            status='draft',
            cities=data.get('cities', [])
        )
        
        db.session.add(itinerary)
        db.session.commit()
        
        return jsonify({
            'message': 'Itinerary created successfully',
            'itinerary': itinerary.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:itinerary_id>', methods=['GET'])
@require_auth
@log_request
def get_itinerary(itinerary_id):
    """Get itinerary details"""
    try:
        itinerary = Itinerary.query.get_or_404(itinerary_id)
        
        # Check ownership
        if itinerary.user_id != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(itinerary.to_dict())
    except Exception as e:
        return jsonify({'error': 'Itinerary not found'}), 404


@bp.route('/<int:itinerary_id>/optimize', methods=['GET'])
@require_auth
@log_request
def optimize_route(itinerary_id):
    """Optimize itinerary route using NumPy"""
    try:
        itinerary = Itinerary.query.get_or_404(itinerary_id)
        
        if itinerary.user_id != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get city details
        cities_data = []
        for city_id in itinerary.cities:
            city = City.query.get(city_id)
            if city:
                cities_data.append({
                    'id': city.id,
                    'name': city.name,
                    'latitude': city.latitude,
                    'longitude': city.longitude
                })
        
        # Optimize route
        optimized = RouteOptimizer.optimize_route(cities_data)
        
        return jsonify(optimized)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
