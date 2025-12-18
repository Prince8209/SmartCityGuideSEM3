"""
Custom Decorators
Auth and logging decorators
"""

from functools import wraps
from flask import request, jsonify
from app.utils.security import decode_token


def require_auth(f):
    """
    Decorator to require authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token (format: "Bearer <token>")
            parts = auth_header.split()
            if len(parts) != 2 or parts[0] != 'Bearer':
                return jsonify({'error': 'Invalid authorization header'}), 401
            
            token = parts[1]
            
            # Verify token
            payload = decode_token(token)
            
            # Add user info to request
            request.user_id = payload.get('user_id')
            request.user_email = payload.get('email')
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def log_request(f):
    """
    Decorator to log API requests
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"{request.method} {request.path} - {request.remote_addr}")
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """
    Decorator to require admin authentication
    Must be used after @require_auth
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app.models import User
        
        # require_auth should have already set user_id
        if not hasattr(request, 'user_id'):
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check if user is admin
        user = User.query.get(request.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_administrator():
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

