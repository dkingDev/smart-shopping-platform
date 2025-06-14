# 🚀 GitHub Setup Guide for DkingDev/Smart-Shopping-Platform

## 📋 Complete Data Flow Configuration

This guide ensures your Smart Shopping Platform connects properly:
**Website (GitHub Pages) → API Backend → AWS PostgreSQL Database**

## 🔧 Step 1: GitHub Repository Setup

### Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `smart-shopping-platform`
3. Owner: `DkingDev`
4. Description: `Secure smart shopping platform with AWS PostgreSQL integration`
5. Public repository
6. **Don't** initialize with README, .gitignore, or license

### Push Code to GitHub
```bash
# Add GitHub remote (replace with your actual repository URL)
git remote add origin https://github.com/DkingDev/smart-shopping-platform.git

# Push main branch
git push -u origin master

# Push develop branch
git push origin develop
```

## 🔒 Step 2: Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions

Add these **Repository Secrets**:

### Production Database Secrets
```
AWS_DB_HOST = your-production-rds-endpoint.amazonaws.com
AWS_DB_PORT = 5432
AWS_DB_NAME = smart_shopping_production
AWS_DB_USER = your_production_db_user
AWS_DB_PASSWORD = your_production_db_password
```

### Security Secrets
```
JWT_SECRET_KEY = your-super-secure-jwt-secret-key-minimum-32-characters
```

### Production API URL
```
PRODUCTION_API_URL = https://your-production-api-domain.com
```

## 🌐 Step 3: GitHub Pages Setup

### Enable GitHub Pages
1. Go to repository → Settings → Pages
2. Source: Deploy from a branch
3. Branch: `master` (or `main`)
4. Folder: `/ (root)`
5. Save

Your website will be available at: `https://dkingdev.github.io/smart-shopping-platform/`

### Update Frontend API Configuration
In `frontend/js/app.js`, update the `getApiBaseUrl()` method:

```javascript
getApiBaseUrl() {
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:8888';
    } else if (hostname === 'dkingdev.github.io') {
        // Your production API URL
        return 'https://your-production-api-domain.com';
    } else {
        return 'https://your-production-api-domain.com';
    }
}
```

## ☁️ Step 4: AWS Database Configuration

### AWS RDS PostgreSQL Setup
1. **Create AWS RDS PostgreSQL Instance**:
   - Engine: PostgreSQL 15+
   - Instance class: db.t3.micro (for testing) or larger
   - Storage: 20GB (minimum)
   - Multi-AZ: No (for cost savings in development)
   - Public access: Yes (for testing, secure with proper security groups)

2. **Security Group Configuration**:
   - Inbound rules: PostgreSQL (5432) from your IP addresses
   - For production: Use VPC endpoints or private subnets

3. **Database Setup**:
   ```sql
   -- Connect to your RDS instance and run:
   CREATE DATABASE smart_shopping_production;
   CREATE USER your_production_db_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE smart_shopping_production TO your_production_db_user;
   ```

4. **Run Database Schema**:
   ```bash
   # Use the schema file to create tables
   psql -h your-rds-endpoint.amazonaws.com -U your_production_db_user -d smart_shopping_production -f database/aws_postgresql_schema.sql
   ```

## 🚀 Step 5: Production API Deployment

### Option A: AWS EC2 Deployment
```bash
# On your EC2 instance
git clone https://github.com/DkingDev/smart-shopping-platform.git
cd smart-shopping-platform

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your production settings

# Run production setup
python scripts/production_setup.py

# Start with Gunicorn (production WSGI server)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker secure_aws_shopping:app --bind 0.0.0.0:8888
```

### Option B: Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set AWS_DB_HOST=your-rds-endpoint.amazonaws.com
heroku config:set AWS_DB_PORT=5432
heroku config:set AWS_DB_NAME=smart_shopping_production
heroku config:set AWS_DB_USER=your_production_db_user
heroku config:set AWS_DB_PASSWORD=your_production_db_password
heroku config:set JWT_SECRET_KEY=your-secure-jwt-key

# Deploy
git push heroku master
```

### Option C: Railway/Render/DigitalOcean
Similar process - set environment variables and deploy the FastAPI application.

## 🔄 Step 6: Update CORS Configuration

In `secure_aws_shopping.py`, update the CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://dkingdev.github.io",  # Your GitHub Pages URL
        "https://your-production-api-domain.com"  # Your API domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## ✅ Step 7: Test Complete Data Flow

Run the comprehensive test:

```bash
# Start your local server first
python scripts/quick_start.py

# In another terminal, run the data flow test
python scripts/test_data_flow.py
```

This will verify:
- ✅ User registration → AWS database
- ✅ User login → JWT token
- ✅ Shopping list creation → AWS database
- ✅ Data persistence and retrieval

## 📊 Step 8: Verify Production Deployment

### Test Production Website
1. Visit: `https://dkingdev.github.io/smart-shopping-platform/frontend/`
2. Register a new user
3. Create a shopping list
4. Verify data appears in AWS database

### Check AWS Database
```sql
-- Connect to your production database
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM shopping_lists;
SELECT COUNT(*) FROM user_activity;
```

## 🔐 Security Checklist

- [ ] AWS RDS security groups properly configured
- [ ] JWT secret key is secure (32+ characters)
- [ ] Database passwords are strong
- [ ] GitHub secrets are properly set
- [ ] HTTPS enabled for production API
- [ ] Environment variables not hardcoded

## 📈 Monitoring & Maintenance

### GitHub Actions
- Automatic testing on every push
- Production deployment on main branch
- Test environment for development

### AWS Monitoring
- RDS Performance Insights
- CloudWatch for API monitoring
- Database backup strategy

---

## 🎉 Final Verification

Once everything is set up:

1. **Website**: `https://dkingdev.github.io/smart-shopping-platform/frontend/`
2. **API**: `https://your-production-api-domain.com/admin/docs`
3. **Database**: AWS RDS PostgreSQL instance
4. **Repository**: `https://github.com/DkingDev/smart-shopping-platform`

**Data Flow**: User action on website → API call to your backend → Data stored in AWS PostgreSQL → Real-time updates

Your Smart Shopping Platform is now fully connected and production-ready! 🚀
