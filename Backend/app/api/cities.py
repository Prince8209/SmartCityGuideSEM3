"""
Cities API with PostgreSQL
CRUD operations for cities
"""

from flask import Blueprint, request, jsonify
from app.models import db, City
from app.utils.decorators import log_request
from sqlalchemy import or_

bp = Blueprint('cities', __name__)


@bp.route('', methods=['GET'])
@log_request
def get_cities():
    """Get all cities with optional filters"""
    try:
        # Get query parameters
        category = request.args.get('category')
        max_budget = request.args.get('max_budget', type=int)
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = City.query
        
        if category:
            query = query.filter_by(category=category)
        
        if max_budget:
            query = query.filter(City.avg_budget_per_day <= max_budget)
        
        if search:
            query = query.filter(
                or_(
                    City.name.ilike(f'%{search}%'),
                    City.description.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'data': [city.to_dict() for city in pagination.items],
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:city_id>', methods=['GET'])
@log_request
def get_city(city_id):
    """Get single city by ID"""
    try:
        city = City.query.get_or_404(city_id)
        return jsonify(city.to_dict())
    except Exception as e:
        return jsonify({'error': 'City not found'}), 404


@bp.route('/<int:city_id>/attractions', methods=['GET'])
@log_request
def get_city_attractions(city_id):
    """Get all attractions for a city"""
    try:
        city = City.query.get_or_404(city_id)
        return jsonify([a.to_dict() for a in city.attractions])
    except Exception as e:
        return jsonify({'error': 'City not found'}), 404


@bp.route('/<int:city_id>/reviews', methods=['GET'])
@log_request
def get_city_reviews(city_id):
    """Get all reviews for a city"""
    try:
        city = City.query.get_or_404(city_id)
        return jsonify([r.to_dict() for r in city.reviews])
    except Exception as e:
        return jsonify({'error': 'City not found'}), 404


@bp.route('/search', methods=['GET'])
@log_request
def search_cities():
    """Search cities"""
    try:
        q = request.args.get('q', '')
        
        if not q:
            return jsonify([])
        
        cities = City.query.filter(
            or_(
                City.name.ilike(f'%{q}%'),
                City.description.ilike(f'%{q}%'),
                City.state.ilike(f'%{q}%')
            )
        ).all()
        
        return jsonify([city.to_dict() for city in cities])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
