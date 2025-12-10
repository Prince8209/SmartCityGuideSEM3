"""
Security Utilities
JWT and password hashing with PyJWT
"""

import hashlib
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'


def create_token(user_id, email, expires_in_hours=24):
    """
    Create JWT token using PyJWT
    Args:
        user_id: User ID
        email: User email
        expires_in_hours: Token expiration time
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token):
    """
    Decode and verify JWT token
    Args:
        token: JWT token string
    Returns:
        Decoded payload dictionary
    Raises:
        jwt.ExpiredSignatureError: If token is expired
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def hash_password(password):
    """
    Hash password using SHA-256
    Args:
        password: Plain text password
    Returns:
        Hashed password string
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    """
    Verify password against hash
    Args:
        password: Plain text password
        hashed: Hashed password
    Returns:
        True if password matches
    """
    return hash_password(password) == hashed
