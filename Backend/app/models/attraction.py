"""
Attraction Model with SQLAlchemy
"""

from datetime import datetime
from app.database.config import db
from sqlalchemy import String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Attraction(db.Model):
    __tablename__ = 'attractions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    entry_fee: Mapped[int] = mapped_column(Integer, default=0)
    opening_hours: Mapped[str] = mapped_column(String(255), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    city = db.relationship('City', back_populates='attractions')
    reviews = db.relationship('Review', back_populates='attraction', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='attraction', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'city_id': self.city_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'image_url': self.image_url,
            'entry_fee': self.entry_fee,
            'opening_hours': self.opening_hours,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Attraction {self.name}>'
