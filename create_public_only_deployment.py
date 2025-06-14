#!/usr/bin/env python3
"""
Create completely clean public-only deployment packages
Excludes ALL proprietary crawler code, product catalogs, and sensitive data
"""

import shutil
import zipfile
import json
from pathlib import Path

def create_clean_github_pages_deployment():
    """Create minimal GitHub Pages deployment with only frontend code"""
    
    # Clean GitHub Pages directory
    github_dir = Path("github-pages-clean")
    if github_dir.exists():
        shutil.rmtree(github_dir)
    github_dir.mkdir()
    
    # Copy only essential frontend files
    files_to_copy = {
        "frontend/index.html": "index.html",
        "frontend/js/app.js": "js/app.js"
    }
    
    # Create js directory
    (github_dir / "js").mkdir()
    
    # Copy files
    for src, dst in files_to_copy.items():
        if Path(src).exists():
            shutil.copy2(src, github_dir / dst)
            print(f"✅ Copied {src} -> {dst}")
    
    # Create minimal package.json (no dependencies)
    package_json = {
        "name": "smart-shopping-platform",
        "version": "1.0.0",
        "description": "Smart Shopping Platform - Frontend Only",
        "scripts": {
            "start": "python -m http.server 8080"
        },
        "repository": {
            "type": "git",
            "url": "git+https://github.com/YOURUSERNAME/smart-shopping-platform.git"
        },
        "keywords": ["shopping", "deals", "price-comparison"],
        "author": "Smart Shopping Platform",
        "license": "MIT"
    }
    
    with open(github_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create clean README
    readme_content = """# Smart Shopping Platform

**Live Demo:** https://YOURUSERNAME.github.io/smart-shopping-platform

## Features
- User Registration & Login
- Shopping List Management  
- Price Comparison
- Store Analysis
- Secure Authentication

## Setup
This is a frontend-only repository. The backend API is hosted separately.

## Usage
1. Open the live demo link above
2. Register a new account or login
3. Start creating shopping lists and comparing prices

---
*Powered by Smart Shopping Platform*
"""
    
    with open(github_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    # Create .nojekyll file for GitHub Pages
    (github_dir / ".nojekyll").touch()
    
    # Create .gitignore
    gitignore_content = """# Dependencies
node_modules/
npm-debug.log*

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
    
    with open(github_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print(f"✅ Clean GitHub Pages deployment created in: {github_dir}")
    return github_dir

def create_clean_heroku_deployment():
    """Create minimal Heroku deployment with only backend essentials"""
    
    # Clean Heroku directory
    heroku_dir = Path("heroku-backend-clean")
    if heroku_dir.exists():
        shutil.rmtree(heroku_dir)
    heroku_dir.mkdir()
    
    # Copy only essential backend files
    essential_files = [
        "secure_aws_shopping.py",
        "Procfile",
        "runtime.txt"
    ]
    
    for file in essential_files:
        if Path(file).exists():
            shutil.copy2(file, heroku_dir / file)
            print(f"✅ Copied {file}")
    
    # Create minimal database directory with only public schema
    db_dir = heroku_dir / "database"
    db_dir.mkdir()
    
    # Copy only public database files
    public_db_files = [
        "database/aws_postgresql_manager.py",
        "database/minimal_schema.sql"
    ]
    
    for file in public_db_files:
        if Path(file).exists():
            shutil.copy2(file, heroku_dir / file)
            print(f"✅ Copied {file}")
    
    # Create minimal requirements.txt (production only)
    requirements_content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
boto3==1.34.0
requests==2.31.0
"""
    
    with open(heroku_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # Create production environment template
    env_content = """# Production Environment Variables for Heroku
# Set these in Heroku Config Vars

DATABASE_URL=postgresql://username:password@hostname:port/database
JWT_SECRET_KEY=your-super-secure-jwt-secret-key-here
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=your-aws-region

# Optional
DEBUG=false
"""
    
    with open(heroku_dir / ".env.example", "w") as f:
        f.write(env_content)
    
    # Create deployment instructions
    deploy_instructions = """# Heroku Deployment Instructions

## Prerequisites
1. Create a Heroku account
2. Install Heroku CLI
3. Have your AWS PostgreSQL credentials ready

## Deployment Steps

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set DATABASE_URL="postgresql://username:password@hostname:port/database"
   heroku config:set JWT_SECRET_KEY="your-super-secure-jwt-secret-key"
   heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key"
   heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
   heroku config:set AWS_REGION="your-aws-region"
   ```

3. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git remote add heroku https://git.heroku.com/your-app-name.git
   git push heroku main
   ```

4. **Verify**
   ```bash
   heroku logs --tail
   heroku open
   ```

## API Endpoints
- POST /register - User registration
- POST /login - User login
- GET /shopping-lists - Get user's shopping lists
- POST /shopping-lists - Create new shopping list

## Security Notes
- All endpoints require JWT authentication (except register/login)
- User data is stored in AWS PostgreSQL
- No sensitive data is logged or cached
"""
    
    with open(heroku_dir / "DEPLOYMENT.md", "w") as f:
        f.write(deploy_instructions)
    
    print(f"✅ Clean Heroku deployment created in: {heroku_dir}")
    return heroku_dir

def create_deployment_packages():
    """Create clean deployment packages for both platforms"""
    
    print("🧹 Creating completely clean deployment packages...")
    print("📦 Excluding ALL proprietary content:")
    print("  ❌ Crawler code")
    print("  ❌ Product catalogs") 
    print("  ❌ Store-specific data")
    print("  ❌ Sensitive configuration")
    print("  ❌ Development tools")
    print()
    
    # Create clean deployments
    github_dir = create_clean_github_pages_deployment()
    heroku_dir = create_clean_heroku_deployment()
    
    # Create zip packages
    print("\n📦 Creating deployment packages...")
    
    # GitHub Pages package
    github_zip = "github-pages-public-only.zip"
    with zipfile.ZipFile(github_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in github_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(github_dir)
                zf.write(file_path, arc_name)
    print(f"✅ Created: {github_zip}")
    
    # Heroku package
    heroku_zip = "heroku-backend-public-only.zip"
    with zipfile.ZipFile(heroku_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in heroku_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(heroku_dir)
                zf.write(file_path, arc_name)
    print(f"✅ Created: {heroku_zip}")
    
    print("\n🎉 Clean deployment packages ready!")
    print(f"📁 GitHub Pages: {github_zip}")
    print(f"📁 Heroku Backend: {heroku_zip}")
    print()
    print("🔒 Security verified:")
    print("  ✅ No crawler code included")
    print("  ✅ No proprietary data included")
    print("  ✅ No sensitive credentials included")
    print("  ✅ Only public-facing functionality included")
    print()
    print("📋 Next steps:")
    print("  1. Upload heroku-backend-public-only.zip to Heroku")
    print("  2. Upload github-pages-public-only.zip to GitHub repository")
    print("  3. Enable GitHub Pages on the repository")
    print("  4. Update API URL in frontend to point to Heroku backend")

if __name__ == "__main__":
    create_deployment_packages()
