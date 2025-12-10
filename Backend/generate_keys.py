"""
Generate Secret Keys for Flask Application
Run this script to generate secure random keys
"""

import secrets

print("=" * 60)
print("Flask Secret Keys Generator")
print("=" * 60)

# Generate SECRET_KEY
secret_key = secrets.token_hex(32)
print(f"\nSECRET_KEY={secret_key}")

# Generate JWT_SECRET_KEY
jwt_secret = secrets.token_hex(32)
print(f"JWT_SECRET_KEY={jwt_secret}")

print("\n" + "=" * 60)
print("Copy these values to your .env file")
print("=" * 60)

# Also create a sample .env file
env_content = f"""# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smart_city_guide

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# JWT Configuration
JWT_SECRET_KEY={jwt_secret}
JWT_EXPIRATION_HOURS=24
"""

with open('.env', 'w') as f:
    f.write(env_content)

print("\n✓ .env file created with generated keys!")
print("⚠ Remember to update YOUR_PASSWORD with your PostgreSQL password")
