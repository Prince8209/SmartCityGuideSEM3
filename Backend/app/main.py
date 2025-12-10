"""
Flask Application with PostgreSQL
Main entry point for the backend
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.database.config import db, init_db

# Load environment variables
load_dotenv()


def create_app():
    """
    Create and configure Flask application
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/smart_city_guide'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.api import auth, cities, attractions, itineraries, reviews, analytics
    
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(cities.bp, url_prefix='/api/cities')
    app.register_blueprint(attractions.bp, url_prefix='/api/attractions')
    app.register_blueprint(itineraries.bp, url_prefix='/api/itineraries')
    app.register_blueprint(reviews.bp, url_prefix='/api/reviews')
    app.register_blueprint(analytics.bp, url_prefix='/api/analytics')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Smart City Guide API is running',
            'database': 'PostgreSQL'
        }
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'name': 'Smart City Guide API',
            'version': '2.0.0',
            'database': 'PostgreSQL + SQLAlchemy',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'cities': '/api/cities',
                'attractions': '/api/attractions',
                'itineraries': '/api/itineraries',
                'reviews': '/api/reviews',
                'analytics': '/api/analytics'
            }
        }
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
