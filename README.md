# Smart Shopping Platform

[![Tests](https://github.com/yourusername/smart-shopping-platform/workflows/Tests/badge.svg)](https://github.com/yourusername/smart-shopping-platform/actions)
[![Production](https://github.com/yourusername/smart-shopping-platform/workflows/Production/badge.svg)](https://github.com/yourusername/smart-shopping-platform/actions)

## 🎯 Overview

A **production-ready, secure smart shopping platform** with AWS PostgreSQL integration, JWT authentication, and comprehensive testing.

## 🚀 Quick Start

### Development
```bash
git clone https://github.com/yourusername/smart-shopping-platform.git
cd smart-shopping-platform
cp .env.example .env
# Configure your .env file
pip install -r requirements-minimal.txt
python scripts/quick_start.py
```

### Testing
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
```

### Production
```bash
cp .env.example .env
# Configure production environment variables
python scripts/production_setup.py
```

## 🏗️ Architecture

- **Backend**: FastAPI with AWS PostgreSQL
- **Frontend**: Modern SPA with Bootstrap 5
- **Authentication**: JWT with bcrypt hashing
- **Testing**: Comprehensive unit and integration tests
- **Deployment**: Automated CI/CD with GitHub Actions
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   python scripts/setup_aws_database.py
   ```

5. **Production Setup (Automated)**
   ```bash
   python scripts/production_setup.py
   ```

6. **Start Development Server**
   ```bash
   python scripts/quick_start.py
   ```

7. **Access Application**
   - **Web App**: http://localhost:8888/frontend/
   - **API Docs**: http://localhost:8888/admin/docs

## 📁 Project Structure

```
├── secure_aws_shopping.py      # Main FastAPI application
├── frontend/                   # SPA frontend application
│   ├── index.html             # Main HTML file
│   └── js/app.js              # JavaScript application logic
├── database/                   # Database management
│   ├── aws_postgresql_manager.py
│   └── aws_postgresql_schema.sql
├── scripts/                    # Utility scripts
│   ├── quick_start.py         # Development server
│   ├── setup_aws_database.py # Database setup
│   └── populate_aws_demo_data.py
├── docs/                      # Documentation
├── config/                    # Configuration files
└── requirements.txt           # Python dependencies
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# AWS PostgreSQL Database
AWS_DB_HOST=your-rds-endpoint.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=postgres
AWS_DB_USER=your_username
AWS_DB_PASSWORD=your_password

# Security Configuration
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## 📚 Documentation

For comprehensive documentation, see the `docs/` folder:
- **AWS Setup Guide**: `docs/AWS_SETUP.md`
- **Database Guide**: `docs/AWS_DATABASE_COMPLETE.md`
- **RDS Setup**: `docs/AWS_RDS_SETUP_GUIDE.md`
- **Production Deployment**: `docs/PRODUCTION_DEPLOYMENT_GUIDE.md`
- **Platform Features**: `docs/README_SECURE_PLATFORM.md`
- **Project Structure**: `docs/PROJECT_STRUCTURE.md`

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/verify-token` - Token verification
- `POST /auth/refresh-token` - Token refresh

### Protected Features (JWT Required)
- `GET /api/shopping-lists` - User shopping lists
- `POST /api/shopping-lists` - Create shopping list
- `POST /api/analyze-savings` - Savings analysis
- `POST /api/compare-stores` - Store price comparison
- `GET /api/promotions` - Current promotions

## 🚢 Deployment

### Local Development
```bash
python scripts/quick_start.py
```

### Production Deployment
1. **Deploy Backend**: Any cloud server (AWS EC2, Heroku, etc.)
2. **Deploy Frontend**: GitHub Pages, Netlify, or static hosting
3. **Configure HTTPS**: SSL certificates for production
4. **Update URLs**: Change API base URL in frontend

## 🛡️ Security Features

- **Authentication Required**: All features require user registration/login
- **Password Security**: bcrypt hashing with salt
- **JWT Tokens**: Secure session management with auto-refresh
- **Database Security**: AWS RDS with encrypted connections
- **CORS Protection**: Secure cross-origin request handling

## 🎯 Success Criteria

✅ **Frontend Access Control**: Only registered users can access features  
✅ **AWS Database Integration**: All data stored in AWS PostgreSQL  
✅ **Secure Authentication**: JWT-based with proper validation  
✅ **Real-time Features**: Price comparison, promotions, savings analysis  
✅ **Production Ready**: Secure, scalable, deployable platform  

---

**Built with ❤️ for smart shopping and intelligent savings**

## Integration Guide

### Adding Your Crawler
1. Copy your crawler to `crawlers/[store]/`
2. Adapt using `crawlers/national_crawler_template.py`
3. Configure in `config/[store]_config.json`
4. Test with branded products validation

### Database Integration
```sql
-- Load master products (one-time)
LOAD DATA INFILE 'database/imports/master_branded_products.csv' 
INTO TABLE branded_products;

-- Daily price updates
LOAD DATA INFILE 'processed/branded_products/[store]_prices.csv'
INTO TABLE store_prices;
```

## Key Benefits

🎯 **National Coverage**: Track prices across all major UK retailers  
📊 **Branded Focus**: Only genuine branded products, no store own-brands  
⚡ **Efficient Updates**: Only update changed prices, not entire catalog  
🔍 **Price Comparison**: Easy cross-store price analysis  
📈 **Trend Analysis**: Historical price tracking and insights  

## Next Steps

1. **Integrate your existing crawlers** using the template
2. **Set up database** using provided schema
3. **Configure crawl schedules** in master_config.json
4. **Start daily crawling** for national price tracking
5. **Generate reports** for price comparison insights

**Ready for national branded products price tracking! 🚀**
