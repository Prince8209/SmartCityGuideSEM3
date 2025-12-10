"""
Favorite Model with SQLAlchemy
"""

from datetime import datetime
from app.database.config import db
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=True, index=True)
    attraction_id: Mapped[int] = mapped_column(ForeignKey('attractions.id'), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='favorites')
    city = db.relationship('City', back_populates='favorites')
    attraction = db.relationship('Attraction', back_populates='favorites')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'city_id': self.city_id,
            'attraction_id': self.attraction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Favorite {self.id}>'
