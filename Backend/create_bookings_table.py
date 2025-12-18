"""
Database Migration Script
Creates the bookings table in PostgreSQL
"""

from app.main import create_app
from app.models import db, Booking

def create_bookings_table():
    """Create bookings table"""
    app = create_app()
    
    with app.app_context():
        # Create bookings table
        db.create_all()
        print("✅ Bookings table created successfully!")
        print(f"📊 Table: {Booking.__tablename__}")
        print(f"📝 Columns: {[c.name for c in Booking.__table__.columns]}")

if __name__ == '__main__':
    create_bookings_table()
