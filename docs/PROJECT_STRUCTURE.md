# Smart Shopping Platform - Project Structure

## Core Application
- `secure_aws_shopping.py` - Main FastAPI application with AWS PostgreSQL integration
- `requirements.txt` - Essential Python dependencies
- `.env` - Environment configuration (AWS credentials, JWT secrets)
- `.env.example` - Template for environment variables

## Database
- `database/aws_postgresql_manager.py` - AWS PostgreSQL connection and operations
- `database/aws_postgresql_schema.sql` - Complete database schema with triggers/functions

## Frontend
- `frontend/index.html` - Single Page Application (SPA) with authentication
- `frontend/js/app.js` - JavaScript application logic with JWT handling

## Scripts
- `scripts/quick_start.py` - Development server launcher with health checks
- `scripts/setup_aws_database.py` - Database initialization and schema setup
- `scripts/populate_aws_demo_data.py` - Demo data population for testing
- `scripts/universal_smart_crawler.py` - Store data crawler for AWS database

## Documentation
- `README_SECURE_PLATFORM.md` - Complete platform documentation
- `AWS_RDS_SETUP_GUIDE.md` - AWS RDS PostgreSQL setup instructions
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Production deployment guide
- `docs/` - Additional documentation files

## Data
- `processed_price_history.csv` - Historical price data for analysis

## Configuration
- `config/` - Configuration files and templates
- `.vscode/` - VS Code workspace settings
- `.gitignore` - Git ignore patterns

## Quick Start
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python scripts/setup_aws_database.py

# 4. Start server
python scripts/quick_start.py
```

## Security Features
- JWT authentication with bcrypt password hashing
- AWS PostgreSQL database for all data storage
- CORS protection for secure API access
- User activity logging and session management

## Frontend Features
- User registration and login with AWS database
- Protected dashboard requiring authentication
- Shopping list management with persistence
- Price comparison across multiple stores
- Savings analysis and promotional offers
- Real-time data from AWS PostgreSQL

## Deployment Options
- **Local Development**: Use `scripts/quick_start.py`
- **GitHub Pages**: Deploy frontend with API backend on cloud
- **Production**: Deploy complete system with HTTPS/SSL
