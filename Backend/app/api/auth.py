"""
Authentication API with PostgreSQL
User registration, login, and authentication
"""

from flask import Blueprint, request, jsonify
from app.models import db, User
from app.utils.security import create_token, hash_password, verify_password
from app.utils.decorators import require_auth, log_request
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
@log_request
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['email', 'username', 'password', 'full_name']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create user
        user = User(
            email=data['email'],
            username=data['username'],
            hashed_password=hash_password(data['password']),
            full_name=data['full_name'],
            profile_image=data.get('profile_image'),
            is_active=True,
            is_verified=False
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = create_token(user.id, user.email)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@bp.route('/login', methods=['POST'])
@log_request
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(data['password'], user.hashed_password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 401
        
        # Generate token
        token = create_token(user.id, user.email)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user profile"""
    try:
        user = User.query.get(request.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/me', methods=['PUT'])
@require_auth
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        user = User.query.get(request.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'profile_image' in data:
            user.profile_image = data['profile_image']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
