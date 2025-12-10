"""
Attractions API with PostgreSQL
"""

from flask import Blueprint, request, jsonify
from app.models import db, Attraction
from app.utils.decorators import log_request

bp = Blueprint('attractions', __name__)


@bp.route('', methods=['GET'])
@log_request
def get_attractions():
    """Get all attractions"""
    try:
        city_id = request.args.get('city_id', type=int)
        category = request.args.get('category')
        
        query = Attraction.query
        
        if city_id:
            query = query.filter_by(city_id=city_id)
        if category:
            query = query.filter_by(category=category)
        
        attractions = query.all()
        return jsonify([a.to_dict() for a in attractions])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:attraction_id>', methods=['GET'])
@log_request
def get_attraction(attraction_id):
    """Get single attraction"""
    try:
        attraction = Attraction.query.get_or_404(attraction_id)
        return jsonify(attraction.to_dict())
    except Exception as e:
        return jsonify({'error': 'Attraction not found'}), 404
