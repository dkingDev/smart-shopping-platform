#!/usr/bin/env python3
"""Create secure deployment packages - hide proprietary crawler code"""

import os
import zipfile
import shutil
import json
from datetime import datetime

def create_secure_backend_package():
    """Create backend package with only public-facing code"""
    print("🔒 CREATING SECURE BACKEND PACKAGE")
    print("=" * 40)
    
    # Create clean backend directory
    secure_dir = "secure-backend-deploy"
    if os.path.exists(secure_dir):
        shutil.rmtree(secure_dir)
    os.makedirs(secure_dir)
    
    # Only include essential backend files (NO CRAWLER CODE)
    essential_files = {
        "secure_aws_shopping.py": "Main FastAPI application",
        "requirements.txt": "Python dependencies", 
        "Procfile": "Heroku deployment config",
        "runtime.txt": "Python version",
        ".env.production": "Environment template"
    }
    
    # Copy only essential files
    for file, description in essential_files.items():
        if os.path.exists(file):
            shutil.copy2(file, f"{secure_dir}/{file}")
            print(f"✅ Included: {file} - {description}")
        else:
            print(f"⚠️  Missing: {file}")
    
    # Create minimal database directory (NO CRAWLER SCHEMAS)
    secure_db_dir = f"{secure_dir}/database"
    os.makedirs(secure_db_dir)
    
    # Only include user authentication database files
    db_files = {
        "aws_postgresql_manager.py": "Database connection manager",
        "minimal_schema.sql": "User authentication schema only"
    }
    
    for file, description in db_files.items():
        src_path = f"database/{file}"
        if os.path.exists(src_path):
            shutil.copy2(src_path, f"{secure_db_dir}/{file}")
            print(f"✅ Included: database/{file} - {description}")
    
    # Create a clean requirements.txt with only essential dependencies
    clean_requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic[email]==2.5.0
jinja2==3.1.2
aiofiles==23.2.1
"""
    
    with open(f"{secure_dir}/requirements.txt", "w") as f:
        f.write(clean_requirements)
    print("✅ Created: Clean requirements.txt (essential dependencies only)")
    
    # Create secure deployment instructions
    instructions = f"""# Smart Shopping Platform - Secure Backend Deployment

## IMPORTANT: CRAWLER CODE PROTECTED
This deployment package contains ONLY the public-facing website code.
Proprietary crawler and data collection systems are NOT included.

## Files Included:
- secure_aws_shopping.py (Public FastAPI application)
- requirements.txt (Essential dependencies only)
- database/minimal_schema.sql (User authentication only)
- Environment configuration

## Files EXCLUDED (Protected IP):
- Crawler systems and algorithms
- Data collection scripts
- Store-specific scraping logic
- Price analysis algorithms
- Proprietary database schemas

## Environment Variables:
```
AWS_DB_HOST=supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=postgres
AWS_DB_USER=AdminTakeo
AWS_DB_PASSWORD=Alex8nd3r12
JWT_SECRET_KEY=3f2a8b9c4d1e7f6a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
```

**Deployment:** Standard Heroku web application
**Features:** User authentication, shopping lists, basic UI
**Protected:** All crawler and data collection IP

---
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(f"{secure_dir}/SECURE_DEPLOY_README.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Created: Secure deployment instructions")
    
    return secure_dir

def create_public_frontend_package():
    """Create frontend package with no proprietary information"""
    print("\n🌐 CREATING PUBLIC FRONTEND PACKAGE")
    print("=" * 40)
    
    # Create clean frontend directory
    public_dir = "public-frontend-deploy"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)
    os.makedirs(f"{public_dir}/js")
    
    # Copy and clean frontend files
    if os.path.exists("github-pages-deploy/index.html"):
        shutil.copy2("github-pages-deploy/index.html", f"{public_dir}/index.html")
        print("✅ Included: index.html")
    
    if os.path.exists("github-pages-deploy/js/app.js"):
        # Read and clean the frontend JavaScript
        with open("github-pages-deploy/js/app.js", "r", encoding="utf-8") as f:
            js_content = f.read()
        
        # Remove any crawler-related comments or references
        cleaned_js = js_content.replace("crawler", "data collection")
        cleaned_js = cleaned_js.replace("scraping", "data gathering")
        
        with open(f"{public_dir}/js/app.js", "w", encoding="utf-8") as f:
            f.write(cleaned_js)
        print("✅ Included: js/app.js (cleaned)")
    
    # Create public README
    public_readme = """# Smart Shopping Platform

A modern web application for smart shopping and price comparison.

## Features
- User registration and authentication
- Shopping list management
- Price comparison tools
- Responsive design

## Technology Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Hosting: GitHub Pages + Heroku

## Live Demo
Visit the live application to test features including user registration, shopping lists, and price comparison tools.

## Usage
1. Create an account or login
2. Build shopping lists
3. Compare prices across stores
4. Save money with smart shopping

---
*Modern shopping made simple*
"""
    
    with open(f"{public_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(public_readme)
    
    # Copy other safe files
    safe_files = [".nojekyll", "package.json"]
    for file in safe_files:
        src_path = f"github-pages-deploy/{file}"
        if os.path.exists(src_path):
            shutil.copy2(src_path, f"{public_dir}/{file}")
            print(f"✅ Included: {file}")
    
    print(f"📁 Public frontend ready in: {public_dir}/")
    return public_dir

def create_secure_deployment_packages():
    """Create secure zip packages for deployment"""
    print("\n📦 CREATING SECURE DEPLOYMENT PACKAGES")
    print("=" * 40)
    
    # Create secure backend zip
    backend_zip = "secure-heroku-deploy.zip"
    if os.path.exists(backend_zip):
        os.remove(backend_zip)
    
    with zipfile.ZipFile(backend_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("secure-backend-deploy"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "secure-backend-deploy")
                zipf.write(file_path, arcname)
                print(f"📦 Added to backend: {arcname}")
    
    # Create public frontend zip
    frontend_zip = "public-github-deploy.zip"
    if os.path.exists(frontend_zip):
        os.remove(frontend_zip)
    
    with zipfile.ZipFile(frontend_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("public-frontend-deploy"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "public-frontend-deploy")
                zipf.write(file_path, arcname)
                print(f"📦 Added to frontend: {arcname}")
    
    print(f"✅ Created: {backend_zip} ({os.path.getsize(backend_zip)} bytes)")
    print(f"✅ Created: {frontend_zip} ({os.path.getsize(frontend_zip)} bytes)")
    
    return backend_zip, frontend_zip

def list_excluded_files():
    """Show what proprietary files are being protected"""
    print("\n🔒 PROPRIETARY FILES PROTECTED (NOT INCLUDED)")
    print("=" * 50)
    
    excluded_items = [
        "scripts/universal_smart_crawler.py - Proprietary crawler engine",
        "scripts/test_*.py - Internal testing scripts", 
        "database/imports/ - Proprietary data schemas",
        "All price collection algorithms",
        "Store-specific scraping logic",
        "Data analysis and ML models",
        "Internal configuration files",
        "Development and testing data",
        "Crawler strategy documentation",
        "Price history processing code"
    ]
    
    for item in excluded_items:
        print(f"🔒 PROTECTED: {item}")
    
    print("\n✅ Your intellectual property is secure!")

def main():
    print("🔒 SECURE DEPLOYMENT PACKAGE CREATION")
    print("Protecting your proprietary crawler code!")
    print("=" * 60)
    
    # Create secure packages
    backend_dir = create_secure_backend_package()
    frontend_dir = create_public_frontend_package()
    
    # Create deployment zips
    backend_zip, frontend_zip = create_secure_deployment_packages()
    
    # Show what's protected
    list_excluded_files()
    
    print("\n" + "=" * 60)
    print("🎉 SECURE DEPLOYMENT PACKAGES READY!")
    print("=" * 60)
    print(f"🔒 Secure Backend: {backend_zip}")
    print(f"🌐 Public Frontend: {frontend_zip}")
    print(f"📁 Source folders: {backend_dir}/ & {frontend_dir}/")
    
    print("\n✅ WHAT'S INCLUDED:")
    print("  - User authentication system")
    print("  - Shopping list management")
    print("  - Basic price comparison UI")
    print("  - Modern responsive design")
    
    print("\n🔒 WHAT'S PROTECTED:")
    print("  - All crawler algorithms")
    print("  - Data collection systems")
    print("  - Store scraping logic")
    print("  - Price analysis code")
    print("  - Internal development tools")
    
    print("\n🎯 DEPLOYMENT:")
    print("  - Upload backend to Heroku (private business logic safe)")
    print("  - Upload frontend to GitHub (clean public interface)")
    print("  - Your proprietary IP remains protected")
    
    print("\n🚀 Ready for public deployment with IP protection!")

if __name__ == "__main__":
    main()
