"""
Models Package
SQLAlchemy models
"""

from app.database.config import db
from .user import User
from .city import City
from .attraction import Attraction
from .itinerary import Itinerary
from .review import Review
from .favorite import Favorite

__all__ = [
    'db',
    'User',
    'City',
    'Attraction',
    'Itinerary',
    'Review',
    'Favorite'
]
