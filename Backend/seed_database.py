"""
Seed Database Script for PostgreSQL
Populate database with initial data
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import create_app
from app.models import db, City, Attraction


def seed_cities():
    """Seed cities from JSON file"""
    print("Seeding cities...")
    
    seed_file = Path(__file__).parent / "seed_data" / "cities_seed.json"
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    for city_data in cities_data:
        # Check if city already exists
        existing = City.query.filter_by(name=city_data['name']).first()
        if existing:
            print(f"  - City already exists: {city_data['name']}")
            continue
        
        city = City(**city_data)
        db.session.add(city)
        print(f"  ✓ Created city: {city.name}")
    
    db.session.commit()
    print(f"Seeded {len(cities_data)} cities")


def seed_attractions():
    """Seed sample attractions"""
    print("Seeding attractions...")
    
    # Get Delhi
    delhi = City.query.filter_by(name='Delhi').first()
    if delhi:
        attractions_data = [
            {
                'city_id': delhi.id,
                'name': 'Red Fort',
                'description': 'Historic fort and UNESCO World Heritage Site',
                'category': 'heritage',
                'entry_fee': 50,
                'opening_hours': '9:00 AM - 5:00 PM',
                'latitude': 28.6562,
                'longitude': 77.2410
            },
            {
                'city_id': delhi.id,
                'name': 'Qutub Minar',
                'description': 'Tallest brick minaret in the world',
                'category': 'heritage',
                'entry_fee': 30,
                'opening_hours': '7:00 AM - 5:00 PM',
                'latitude': 28.5244,
                'longitude': 77.1855
            },
            {
                'city_id': delhi.id,
                'name': 'India Gate',
                'description': 'War memorial and iconic landmark',
                'category': 'monument',
                'entry_fee': 0,
                'opening_hours': 'Open 24 hours',
                'latitude': 28.6129,
                'longitude': 77.2295
            }
        ]
        
        for attr_data in attractions_data:
            # Check if attraction already exists
            existing = Attraction.query.filter_by(
                city_id=attr_data['city_id'],
                name=attr_data['name']
            ).first()
            if existing:
                print(f"  - Attraction already exists: {attr_data['name']}")
                continue
            
            attraction = Attraction(**attr_data)
            db.session.add(attraction)
            print(f"  ✓ Created attraction: {attraction.name}")
        
        db.session.commit()
    
    print("Seeded attractions")


if __name__ == '__main__':
    print("=" * 50)
    print("Smart City Guide - Database Seeding")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Seed data
        seed_cities()
        seed_attractions()
    
    print("\n✓ Database seeding completed!")
    print("=" * 50)
