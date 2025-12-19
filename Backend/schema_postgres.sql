-- ============================================
-- Smart City Guide - Database Schema
-- PostgreSQL Database Schema
-- ============================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS itineraries CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS attractions CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    profile_image VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- ============================================
-- CITIES TABLE
-- ============================================
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    badge VARCHAR(100),
    best_season VARCHAR(100),
    avg_budget_per_day INT,
    recommended_days VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    category VARCHAR(100),
    region VARCHAR(50),
    trip_types JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cities_name ON cities(name);
CREATE INDEX idx_cities_category ON cities(category);
CREATE INDEX idx_cities_region ON cities(region);

-- ============================================
-- ATTRACTIONS TABLE
-- ============================================
CREATE TABLE attractions (
    id SERIAL PRIMARY KEY,
    city_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    category VARCHAR(100),
    entry_fee INT,
    opening_hours VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    rating FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);

CREATE INDEX idx_attractions_city_id ON attractions(city_id);
CREATE INDEX idx_attractions_category ON attractions(category);

-- ============================================
-- REVIEWS TABLE
-- ============================================
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    city_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);

CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_city_id ON reviews(city_id);

-- ============================================
-- BOOKINGS TABLE
-- ============================================
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    city_name VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    num_travelers INT NOT NULL,
    daily_budget INT NOT NULL,
    total_cost INT NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bookings_reference ON bookings(booking_reference);
CREATE INDEX idx_bookings_email ON bookings(customer_email);

-- ============================================
-- ITINERARIES TABLE
-- ============================================
CREATE TABLE itineraries (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    total_budget INT,
    cities JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_itineraries_user_id ON itineraries(user_id);

-- ============================================
-- FAVORITES TABLE
-- ============================================
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    city_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    UNIQUE(user_id, city_id)
);

CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_city_id ON favorites(city_id);

-- ============================================
-- AUTOMATED UPDATED_AT TRIGGER
-- ============================================
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_modtime BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_cities_modtime BEFORE UPDATE ON cities FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_attractions_modtime BEFORE UPDATE ON attractions FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_reviews_modtime BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_bookings_modtime BEFORE UPDATE ON bookings FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_itineraries_modtime BEFORE UPDATE ON itineraries FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
