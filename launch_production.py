#!/usr/bin/env python3
"""
Production Launch Script for Smart Shopping Platform
Prepares and launches the platform for production deployment
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def create_production_env():
    """Create production environment file"""
    print_section("PRODUCTION ENVIRONMENT SETUP")
    
    production_env = f"""# Smart Shopping Platform - Production Environment
# Generated on {datetime.now().isoformat()}

# ========================================
# AWS RDS PostgreSQL Connection (PRODUCTION)
# ========================================
AWS_DB_HOST={os.getenv('AWS_DB_HOST')}
AWS_DB_PORT={os.getenv('AWS_DB_PORT')}
AWS_DB_NAME={os.getenv('AWS_DB_NAME')}
AWS_DB_USER={os.getenv('AWS_DB_USER')}
AWS_DB_PASSWORD={os.getenv('AWS_DB_PASSWORD')}

# ========================================
# Security Configuration (PRODUCTION)
# ========================================
JWT_SECRET_KEY={os.getenv('JWT_SECRET_KEY')}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS Configuration for production (UPDATE WITH YOUR DOMAIN)
ALLOWED_ORIGINS=["https://yourusername.github.io", "https://your-custom-domain.com"]

# ========================================
# AWS Services Configuration
# ========================================
AWS_REGION=eu-north-1
AWS_ACCESS_KEY_ID={os.getenv('AWS_ACCESS_KEY_ID', 'your_access_key_id')}
AWS_SECRET_ACCESS_KEY={os.getenv('AWS_SECRET_ACCESS_KEY', 'your_secret_access_key')}

# ========================================
# Application Configuration (PRODUCTION)
# ========================================
ENVIRONMENT=production
DEBUG=false

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# ========================================
# Crawler Configuration
# ========================================
CRAWLER_USER_AGENT=SmartShopping-Bot/1.0
CRAWLER_DELAY_SECONDS=2
CRAWLER_MAX_CONCURRENT=3
CRAWLER_TIMEOUT_SECONDS=30
"""
    
    with open('.env.production', 'w') as f:
        f.write(production_env)
    
    print("✅ Production environment file created: .env.production")
    print("⚠️  IMPORTANT: Update ALLOWED_ORIGINS with your actual domain!")
    return True

def create_production_requirements():
    """Create production requirements.txt"""
    print_section("PRODUCTION REQUIREMENTS")
    
    requirements = """# Smart Shopping Platform - Production Requirements
# Core framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
psycopg2-binary==2.9.7
pandas==2.1.3

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Environment
python-dotenv==1.0.0

# Web scraping (for crawler)
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2

# Data processing
lxml==4.9.3
openpyxl==3.1.2

# Email validation
email-validator==2.1.0

# CORS
starlette==0.27.0

# Production server
gunicorn==21.2.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Production requirements.txt created")
    return True

def create_procfile():
    """Create Procfile for deployment platforms like Heroku"""
    print_section("DEPLOYMENT CONFIGURATION")
    
    procfile = "web: gunicorn secure_aws_shopping:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
    
    with open('Procfile', 'w') as f:
        f.write(procfile)
    
    print("✅ Procfile created for deployment")
    
    # Create runtime.txt for Python version
    with open('runtime.txt', 'w') as f:
        f.write("python-3.11.6")
    
    print("✅ Runtime configuration created")
    return True

def update_frontend_for_production():
    """Update frontend for production deployment"""
    print_section("FRONTEND PRODUCTION SETUP")
    
    try:
        # Read current frontend JS
        with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Create production version
        production_js = js_content.replace(
            'const API_BASE_URL = "http://localhost:8000";',
            '// Production API URL - UPDATE THIS WITH YOUR DEPLOYED BACKEND URL\n' +
            'const API_BASE_URL = window.location.hostname.includes("github.io") \n' +
            '    ? "https://your-backend-url.herokuapp.com"  // Replace with actual backend URL\n' +
            '    : "http://localhost:8001";  // Local development'
        )
        
        # Save production version
        with open('frontend/js/app.production.js', 'w', encoding='utf-8') as f:
            f.write(production_js)
        
        # Create production HTML
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        production_html = html_content.replace(
            '<script src="js/app.js"></script>',
            '<script src="js/app.production.js"></script>'
        )
        
        with open('frontend/index.production.html', 'w', encoding='utf-8') as f:
            f.write(production_html)
        
        print("✅ Frontend production files created")
        print("⚠️  IMPORTANT: Update API_BASE_URL in app.production.js with your deployed backend URL!")
        return True
        
    except Exception as e:
        print(f"❌ Frontend setup error: {e}")
        return False

def create_deployment_scripts():
    """Create deployment helper scripts"""
    print_section("DEPLOYMENT SCRIPTS")
    
    # Local test script
    local_test_script = """#!/usr/bin/env python3
# Local Development Test Script
import subprocess
import sys
import os

def main():
    print("🚀 Starting Smart Shopping Platform - Local Development Mode")
    
    # Use local environment
    os.environ['ENV_FILE'] = '.env'
    
    # Start with uvicorn for development
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "secure_aws_shopping:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8001"
        ])
    except KeyboardInterrupt:
        print("\\n🛑 Local development server stopped")

if __name__ == "__main__":
    main()
"""    
    with open('run_local.py', 'w', encoding='utf-8') as f:
        f.write(local_test_script)
    
    # Production server script
    production_script = """#!/usr/bin/env python3
# Production Server Script
import subprocess
import sys
import os

def main():
    print("🚀 Starting Smart Shopping Platform - Production Mode")
    
    # Use production environment
    os.environ['ENV_FILE'] = '.env.production'
    
    # Start with gunicorn for production
    try:
        subprocess.run([
            "gunicorn", 
            "secure_aws_shopping:app",
            "-w", "4",
            "-k", "uvicorn.workers.UvicornWorker",
            "--bind", "0.0.0.0:8000"
        ])
    except KeyboardInterrupt:
        print("\\n🛑 Production server stopped")

if __name__ == "__main__":
    main()
"""    
    with open('run_production.py', 'w', encoding='utf-8') as f:
        f.write(production_script)
    
    print("✅ Deployment scripts created:")
    print("   - run_local.py (for local testing)")
    print("   - run_production.py (for production)")
    return True

def create_docker_setup():
    """Create Docker configuration for production deployment"""
    print_section("DOCKER CONFIGURATION")
    
    dockerfile = """# Smart Shopping Platform - Production Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/ || exit 1

# Start command
CMD ["gunicorn", "secure_aws_shopping:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    # Docker compose for local testing
    docker_compose = """version: '3.8'

services:
  smart-shopping:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV_FILE=.env.production
    volumes:
      - ./.env.production:/app/.env.production:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    print("✅ Docker configuration created:")
    print("   - Dockerfile (production image)")
    print("   - docker-compose.yml (local testing)")
    return True

def create_deployment_guide():
    """Create comprehensive deployment guide"""
    print_section("DEPLOYMENT DOCUMENTATION")
    
    deployment_guide = f"""# Smart Shopping Platform - Production Deployment Guide

Generated on: {datetime.now().isoformat()}

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Heroku Deployment (Recommended for beginners)

1. **Prepare for Heroku:**
   ```bash
   # Install Heroku CLI
   # Create Heroku app
   heroku create your-smart-shopping-app
   
   # Set environment variables
   heroku config:set AWS_DB_HOST={os.getenv('AWS_DB_HOST')}
   heroku config:set AWS_DB_PORT={os.getenv('AWS_DB_PORT')}
   heroku config:set AWS_DB_NAME={os.getenv('AWS_DB_NAME')}
   heroku config:set AWS_DB_USER={os.getenv('AWS_DB_USER')}
   heroku config:set AWS_DB_PASSWORD={os.getenv('AWS_DB_PASSWORD')}
   heroku config:set JWT_SECRET_KEY={os.getenv('JWT_SECRET_KEY')}
   
   # Deploy
   git add .
   git commit -m "Production deployment"
   git push heroku main
   ```

2. **Update Frontend:**
   - Copy `frontend/` folder to a new repository
   - Update `js/app.production.js` with your Heroku app URL
   - Deploy to GitHub Pages

### Option 2: AWS EC2 Deployment

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - t3.micro or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Setup on EC2:**
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip nginx git
   
   # Clone your repository
   git clone https://github.com/yourusername/smart-shopping-platform
   cd smart-shopping-platform
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   
   # Copy production environment
   cp .env.production .env
   
   # Start with systemd (create service file)
   sudo systemctl enable smart-shopping
   sudo systemctl start smart-shopping
   ```

### Option 3: Docker Deployment

1. **Build and Run:**
   ```bash
   # Build image
   docker build -t smart-shopping .
   
   # Run container
   docker run -d -p 8000:8000 --env-file .env.production smart-shopping
   ```

2. **Using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## 🌐 FRONTEND DEPLOYMENT (GitHub Pages)

1. **Create new repository for frontend:**
   ```bash
   # Create new repo: smart-shopping-frontend
   # Copy frontend/ contents to new repo
   ```

2. **Update configuration:**
   - Edit `js/app.production.js`
   - Replace `your-backend-url.herokuapp.com` with actual backend URL
   - Rename `index.production.html` to `index.html`
   - Rename `app.production.js` to `app.js`

3. **Deploy to GitHub Pages:**
   - Repository Settings → Pages
   - Source: Deploy from branch (main)
   - Your site will be at: `https://yourusername.github.io/smart-shopping-frontend`

## 🔧 CONFIGURATION CHECKLIST

### Backend Configuration:
- [ ] Environment variables set in production
- [ ] CORS origins updated with frontend URL
- [ ] Database connection tested
- [ ] JWT secret key changed from default
- [ ] SSL/HTTPS enabled

### Frontend Configuration:
- [ ] API_BASE_URL updated to backend URL
- [ ] CORS properly configured on backend
- [ ] GitHub Pages deployed and accessible
- [ ] All features tested with production URLs

## 🧪 TESTING SETUP

### Local Development (with production data):
```bash
# Start local server (connects to AWS DB)
python run_local.py

# Access at: http://localhost:8001
```

### Production Testing:
```bash
# Test production environment locally
python run_production.py

# Access at: http://localhost:8000
```

## 📊 MONITORING & MAINTENANCE

### Health Checks:
- Backend health: `https://your-backend-url.com/`
- Database connectivity: Monitor AWS RDS metrics
- Frontend accessibility: Check GitHub Pages status

### Security Monitoring:
- Monitor user activity logs in AWS database
- Review failed login attempts
- Keep dependencies updated

### Regular Maintenance:
- Update Python dependencies monthly
- Monitor AWS RDS storage and performance
- Review and rotate JWT secrets quarterly
- Backup database regularly (AWS RDS handles this automatically)

## 🚨 TROUBLESHOOTING

### Common Issues:
1. **CORS errors**: Check ALLOWED_ORIGINS in backend
2. **Database connection**: Verify AWS RDS security groups
3. **Authentication issues**: Check JWT_SECRET_KEY configuration
4. **Deployment failures**: Review logs in deployment platform

### Support Resources:
- AWS RDS Documentation
- FastAPI Documentation
- GitHub Pages Documentation
- Your deployment platform documentation

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. **Test complete user journey on production**
2. **Set up monitoring and alerts**
3. **Configure domain name (optional)**
4. **Set up SSL certificate**
5. **Implement rate limiting**
6. **Add analytics (optional)**
7. **Plan for scaling as user base grows**

---

**✅ Your Smart Shopping Platform is ready for production deployment!**
"""    
    with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(deployment_guide)
    
    print("✅ Comprehensive deployment guide created: DEPLOYMENT_GUIDE.md")
    return True

def main():
    """Main production launch process"""
    print("🚀 SMART SHOPPING PLATFORM - PRODUCTION LAUNCH")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*80)
    
    steps = [
        ("Production Environment", create_production_env),
        ("Production Requirements", create_production_requirements),
        ("Deployment Configuration", create_procfile),
        ("Frontend Production Setup", update_frontend_for_production),
        ("Deployment Scripts", create_deployment_scripts),
        ("Docker Configuration", create_docker_setup),
        ("Deployment Documentation", create_deployment_guide),
    ]
    
    completed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n📋 Step {completed + 1}/{total}: {step_name}")
        if step_func():
            completed += 1
        else:
            print(f"❌ Step failed: {step_name}")
            break
    
    print_section("PRODUCTION LAUNCH SUMMARY")
    
    if completed == total:
        print("🎉 PRODUCTION LAUNCH SUCCESSFUL!")
        print(f"✅ All {total} steps completed successfully")
        
        print("\n📁 FILES CREATED:")
        files = [
            ".env.production (production environment)",
            "requirements.txt (production dependencies)",
            "Procfile (deployment configuration)",
            "runtime.txt (Python version)",
            "frontend/js/app.production.js (production frontend)",
            "frontend/index.production.html (production HTML)",
            "run_local.py (local testing script)",
            "run_production.py (production server script)",
            "Dockerfile (container configuration)",
            "docker-compose.yml (local container testing)",
            "DEPLOYMENT_GUIDE.md (comprehensive guide)"
        ]
        
        for file in files:
            print(f"   ✅ {file}")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. 📖 Read DEPLOYMENT_GUIDE.md for detailed deployment instructions")
        print("   2. 🧪 Test locally: python run_local.py")
        print("   3. 🌐 Deploy backend to your chosen platform (Heroku, AWS, etc.)")
        print("   4. 📱 Deploy frontend to GitHub Pages")
        print("   5. 🔄 Update frontend API URL with deployed backend URL")
        print("   6. ✅ Test complete production system")
        
        print("\n🛡️  SECURITY REMINDER:")
        print("   ⚠️  Update ALLOWED_ORIGINS in .env.production with your actual domain")
        print("   ⚠️  Update API_BASE_URL in frontend/js/app.production.js")
        
    else:
        print(f"❌ Production launch incomplete: {completed}/{total} steps completed")
    
    return completed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
