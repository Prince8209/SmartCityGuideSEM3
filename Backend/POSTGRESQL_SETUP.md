# PostgreSQL Setup Guide for Windows

## Step 1: Download PostgreSQL

1. Go to https://www.postgresql.org/download/windows/
2. Click on "Download the installer"
3. Download the latest version (PostgreSQL 16.x recommended)
4. Choose the Windows x86-64 installer

## Step 2: Install PostgreSQL

1. **Run the installer** (postgresql-16.x-windows-x64.exe)

2. **Installation Directory**: Use default
   - `C:\Program Files\PostgreSQL\16`

3. **Select Components**: Keep all selected
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4 (GUI tool)
   - ✅ Stack Builder
   - ✅ Command Line Tools

4. **Data Directory**: Use default
   - `C:\Program Files\PostgreSQL\16\data`

5. **Password**: Set a password for the `postgres` superuser
   - **IMPORTANT**: Remember this password!
   - Example: `postgres123` (use a stronger password in production)

6. **Port**: Use default `5432`

7. **Locale**: Use default (your system locale)

8. Click **Next** and **Install**

9. **Uncheck** "Launch Stack Builder" at the end
   - Click **Finish**

## Step 3: Verify Installation

Open **Command Prompt** and test:

```bash
# Check PostgreSQL version
psql --version

# If command not found, add to PATH:
# Add this to System Environment Variables:
C:\Program Files\PostgreSQL\16\bin
```

## Step 4: Create Database

### Option A: Using pgAdmin (GUI)

1. Open **pgAdmin 4** from Start Menu
2. Enter your master password (if prompted)
3. Expand **Servers** → **PostgreSQL 16**
4. Enter the password you set during installation
5. Right-click **Databases** → **Create** → **Database**
6. Database name: `smart_city_guide`
7. Click **Save**

### Option B: Using Command Line

```bash
# Open Command Prompt as Administrator

# Login to PostgreSQL
psql -U postgres

# Enter your password when prompted

# Create database
CREATE DATABASE smart_city_guide;

# Verify database was created
\l

# Exit
\q
```

## Step 5: Configure Backend

1. **Copy environment file**:
```bash
cd e:\SAM3\Backend
copy .env.example .env
```

2. **Edit `.env` file** with your credentials:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smart_city_guide
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
```

Replace `YOUR_PASSWORD` with the password you set during PostgreSQL installation.

## Step 6: Install Python Dependencies

```bash
# Make sure you're in the Backend directory
cd e:\SAM3\Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 7: Initialize Database

```bash
# Still in Backend directory with venv activated
python seed_database.py
```

You should see:
```
==================================================
Smart City Guide - Database Seeding
==================================================
✓ Database tables created
Seeding cities...
  ✓ Created city: Delhi
  ✓ Created city: Goa
  ✓ Created city: Jaipur
  ✓ Created city: Mumbai
  ✓ Created city: Kerala
Seeded 5 cities
Seeding attractions...
  ✓ Created attraction: Red Fort
  ✓ Created attraction: Qutub Minar
  ✓ Created attraction: India Gate
Seeded attractions

✓ Database seeding completed!
==================================================
```

## Step 8: Start the Server

```bash
python -m app.main
```

You should see:
```
 * Serving Flask app 'app.main'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://0.0.0.0:5000
```

## Step 9: Test the API

Open a new Command Prompt and test:

```bash
# Health check
curl http://localhost:5000/api/health

# Get cities
curl http://localhost:5000/api/cities
```

Or open in browser: http://localhost:5000/api/health

## Troubleshooting

### Issue: "psql: command not found"

**Solution**: Add PostgreSQL to PATH
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", select "Path"
4. Click "Edit" → "New"
5. Add: `C:\Program Files\PostgreSQL\16\bin`
6. Click OK and restart Command Prompt

### Issue: "password authentication failed"

**Solution**: Check your password in `.env` file matches PostgreSQL password

### Issue: "database does not exist"

**Solution**: Create the database first using pgAdmin or psql

### Issue: "pip install fails for psycopg2-binary"

**Solution**: 
```bash
# Try installing Visual C++ Build Tools
# Or use pre-built wheel:
pip install psycopg2-binary --only-binary :all:
```

### Issue: "Port 5432 already in use"

**Solution**: Another PostgreSQL instance is running
- Stop other PostgreSQL services
- Or change port in PostgreSQL config and `.env`

## Useful PostgreSQL Commands

```bash
# Connect to database
psql -U postgres -d smart_city_guide

# List all databases
\l

# List all tables
\dt

# View table structure
\d users

# View data
SELECT * FROM cities;

# Exit
\q
```

## pgAdmin 4 Tips

- **View Tables**: Expand Databases → smart_city_guide → Schemas → public → Tables
- **Run Queries**: Right-click database → Query Tool
- **View Data**: Right-click table → View/Edit Data → All Rows

## Next Steps

✅ PostgreSQL installed and running
✅ Database created
✅ Backend configured
✅ Dependencies installed
✅ Database seeded
✅ Server running

You're all set! Your backend is now running with PostgreSQL.

Test the API endpoints from the main README.md file.
