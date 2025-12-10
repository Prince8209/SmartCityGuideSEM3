# Smart City Guide - Python Backend with PostgreSQL

## Production-Ready Backend with PostgreSQL

This backend uses **PostgreSQL** database with **SQLAlchemy ORM** for production-ready data persistence, while maintaining custom data structures and NumPy analytics for educational purposes.

## Features

- ✅ **PostgreSQL Database**: Production-grade relational database
- ✅ **SQLAlchemy ORM**: Modern Python ORM with relationships
- ✅ **Custom Data Structures**: LinkedList, Stack, Queue, BST, HashTable, Graph (for algorithms)
- ✅ **NumPy Analytics**: Recommendations, route optimization, statistics
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **RESTful API**: Flask-based API with CORS support

## Project Structure

```
Backend/
├── app/
│   ├── data_structures/    # Custom data structures (for algorithms)
│   ├── database/            # PostgreSQL configuration
│   ├── models/              # SQLAlchemy models
│   ├── api/                 # Flask API endpoints
│   ├── services/            # Business logic with NumPy
│   ├── utils/               # Utilities (security, logging)
│   └── main.py              # Flask application
├── seed_data/               # Initial data
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

1. **PostgreSQL** installed and running
2. **Python 3.8+**

## Installation

### 1. Install PostgreSQL

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Install and remember your password

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

**Mac:**
```bash
brew install postgresql
```

### 2. Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE smart_city_guide;

# Exit
\q
```

### 3. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file from example:
```bash
cp .env.example .env
```

Edit `.env` and update database credentials:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/smart_city_guide
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
```

### 5. Initialize Database

```bash
# Create tables and seed data
python seed_database.py
```

## Running the Server

```bash
python -m app.main
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (requires auth)
- `PUT /api/auth/me` - Update profile (requires auth)

### Cities
- `GET /api/cities` - Get all cities (with filters & pagination)
- `GET /api/cities/{id}` - Get city details
- `GET /api/cities/{id}/attractions` - Get city attractions
- `GET /api/cities/{id}/reviews` - Get city reviews
- `GET /api/cities/search?q=query` - Search cities

### Attractions
- `GET /api/attractions` - Get all attractions
- `GET /api/attractions/{id}` - Get attraction details

### Itineraries (Auth Required)
- `GET /api/itineraries` - Get user itineraries
- `POST /api/itineraries` - Create itinerary
- `GET /api/itineraries/{id}` - Get itinerary details
- `GET /api/itineraries/{id}/optimize` - Optimize route (NumPy)

### Reviews (Auth Required)
- `POST /api/reviews` - Create review
- `GET /api/reviews/user` - Get user reviews

### Analytics
- `GET /api/analytics/popular-cities` - Most popular cities (NumPy)
- `GET /api/analytics/budget-insights` - Budget statistics (NumPy)
- `POST /api/analytics/recommendations` - Get recommendations (NumPy)
- `GET /api/analytics/city/{id}/ratings` - Rating distribution

## Database Schema

### Tables
- **users** - User accounts with authentication
- **cities** - City destinations
- **attractions** - Tourist attractions
- **itineraries** - User travel plans
- **reviews** - User reviews and ratings
- **favorites** - User favorites

### Relationships
- User → Itineraries (one-to-many)
- User → Reviews (one-to-many)
- User → Favorites (one-to-many)
- City → Attractions (one-to-many)
- City → Reviews (one-to-many)

## Testing the API

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Get Cities
```bash
curl http://localhost:5000/api/cities
```

### Get Recommendations
```bash
curl -X POST http://localhost:5000/api/analytics/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "max_budget": 2000,
    "season": "October-March",
    "categories": ["heritage", "beach"]
  }'
```

## Technologies Used

- **Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **NumPy** - Analytics and calculations
- **PyJWT** - JWT authentication
- **Flask-CORS** - CORS support

## Python Concepts Demonstrated

1. **OOP**: SQLAlchemy models with inheritance and relationships
2. **Data Structures**: Custom implementations for algorithms
3. **NumPy**: Statistical analysis, matrix operations, recommendations
4. **Database**: PostgreSQL with SQLAlchemy ORM
5. **API Design**: RESTful endpoints with Flask
6. **Authentication**: JWT token-based auth
7. **Error Handling**: Try-except blocks, custom exceptions

## Production Deployment

For production deployment:

1. Use environment variables for all secrets
2. Enable SSL/HTTPS
3. Use a production WSGI server (Gunicorn)
4. Set up database connection pooling
5. Enable database backups
6. Use a reverse proxy (Nginx)

## License

MIT
