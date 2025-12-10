"""
City Model with SQLAlchemy
"""

from datetime import datetime
from app.database.config import db
from sqlalchemy import String, Integer, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class City(db.Model):
    __tablename__ = 'cities'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    badge: Mapped[str] = mapped_column(String(100), nullable=True)
    best_season: Mapped[str] = mapped_column(String(100), nullable=True)
    avg_budget_per_day: Mapped[int] = mapped_column(Integer, nullable=True)
    recommended_days: Mapped[str] = mapped_column(String(50), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attractions = db.relationship('Attraction', back_populates='city', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='city', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='city', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'description': self.description,
            'image_url': self.image_url,
            'badge': self.badge,
            'best_season': self.best_season,
            'avg_budget_per_day': self.avg_budget_per_day,
            'recommended_days': self.recommended_days,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def is_budget_friendly(self):
        return self.avg_budget_per_day and self.avg_budget_per_day < 2000
    
    def __repr__(self):
        return f'<City {self.name}>'
