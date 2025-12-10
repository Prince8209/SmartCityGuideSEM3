"""
Reviews API with PostgreSQL
"""

from flask import Blueprint, request, jsonify
from app.models import db, Review
from app.utils.decorators import require_auth, log_request

bp = Blueprint('reviews', __name__)


@bp.route('', methods=['POST'])
@require_auth
@log_request
def create_review():
    """Create new review"""
    try:
        data = request.get_json()
        
        review = Review(
            user_id=request.user_id,
            city_id=data.get('city_id'),
            attraction_id=data.get('attraction_id'),
            rating=data.get('rating'),
            title=data.get('title'),
            comment=data.get('comment')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/user', methods=['GET'])
@require_auth
@log_request
def get_user_reviews():
    """Get user's reviews"""
    try:
        reviews = Review.query.filter_by(user_id=request.user_id).all()
        return jsonify([r.to_dict() for r in reviews])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
