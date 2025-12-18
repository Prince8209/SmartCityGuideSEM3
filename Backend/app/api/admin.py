"""
Admin API Endpoints
Admin-only routes for managing cities, users, and site data
"""

from flask import Blueprint, request, jsonify
from app.models import db, City, User, Review
from app.utils.decorators import require_auth, require_admin, log_request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

bp = Blueprint('admin', __name__)


@bp.route('/cities', methods=['POST'])
@require_auth
@require_admin
@log_request
def create_city():
    """Create a new city (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['name', 'state', 'description']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create city
        city = City(
            name=data['name'],
            state=data['state'],
            description=data['description'],
            image_url=data.get('image_url'),
            badge=data.get('badge'),
            best_season=data.get('best_season'),
            avg_budget_per_day=data.get('avg_budget_per_day'),
            recommended_days=data.get('recommended_days'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            category=data.get('category'),
            region=data.get('region'),
            trip_types=data.get('trip_types')
        )
        
        db.session.add(city)
        db.session.commit()
        
        return jsonify({
            'message': 'City created successfully',
            'city': city.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'City already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create city: {str(e)}'}), 500


@bp.route('/cities/<int:city_id>', methods=['PUT'])
@require_auth
@require_admin
@log_request
def update_city(city_id):
    """Update an existing city (admin only)"""
    try:
        city = City.query.get(city_id)
        if not city:
            return jsonify({'error': 'City not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'name', 'state', 'description', 'image_url', 'badge',
            'best_season', 'avg_budget_per_day', 'recommended_days',
            'latitude', 'longitude', 'category', 'region', 'trip_types'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(city, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'City updated successfully',
            'city': city.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update city: {str(e)}'}), 500


@bp.route('/cities/<int:city_id>', methods=['DELETE'])
@require_auth
@require_admin
@log_request
def delete_city(city_id):
    """Delete a city (admin only)"""
    try:
        city = City.query.get(city_id)
        if not city:
            return jsonify({'error': 'City not found'}), 404
        
        city_name = city.name
        db.session.delete(city)
        db.session.commit()
        
        return jsonify({
            'message': f'City {city_name} deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete city: {str(e)}'}), 500


@bp.route('/users', methods=['GET'])
@require_auth
@require_admin
@log_request
def list_users():
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/users/<int:user_id>/toggle-admin', methods=['PUT'])
@require_auth
@require_admin
@log_request
def toggle_admin(user_id):
    """Promote or demote admin status (admin only)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Toggle admin status
        user.is_admin = not user.is_admin
        db.session.commit()
        
        return jsonify({
            'message': f'User admin status updated',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/stats', methods=['GET'])
@require_auth
@require_admin
@log_request
def get_stats():
    """Get admin dashboard statistics"""
    try:
        total_users = User.query.count()
        total_cities = City.query.count()
        total_reviews = Review.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        # Get cities by region
        cities_by_region = db.session.query(
            City.region,
            func.count(City.id)
        ).group_by(City.region).all()
        
        return jsonify({
            'total_users': total_users,
            'total_cities': total_cities,
            'total_reviews': total_reviews,
            'active_users': active_users,
            'admin_users': admin_users,
            'cities_by_region': {region: count for region, count in cities_by_region if region}
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
