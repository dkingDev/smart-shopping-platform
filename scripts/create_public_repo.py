#!/usr/bin/env python3
"""
Repository Cleanup - Separate Public Code from Personal Reference Files
Creates a clean public repository with only essential code
"""

import os
import shutil
from pathlib import Path

def create_public_repository():
    """Create a clean public repository with only essential files"""
    print("🧹 Creating clean public repository...")
    
    # Create clean repo folder
    public_repo = Path("../smart-shopping-platform-public")
    if public_repo.exists():
        shutil.rmtree(public_repo)
    public_repo.mkdir()
    
    # Files that should be PUBLIC (essential code only)
    public_files = [
        # Core application
        "secure_aws_shopping.py",
        "requirements.txt", 
        "runtime.txt",
        "Procfile",
        "LICENSE",
        
        # Frontend (essential)
        "frontend/index.html",
        "frontend/index.production.html", 
        "frontend/js/app.js",
        "frontend/js/app.production.js",
        
        # Company website
        "company-website/index.html",
        
        # Database (schema only)
        "database/aws_postgresql_schema.sql",
        "database/minimal_schema.sql",
        "database/README.md",
        "database/imports/database_schema.sql",
        "database/imports/brands_catalog.json",
        "database/imports/categories_reference.json",
        
        # Essential documentation
        "README.md",
        ".gitignore"
    ]
    
    # Files that should stay PRIVATE (your reference files)
    private_files = [
        # Personal deployment scripts
        "*.ps1",  # All PowerShell scripts
        "*.sh",   # All shell scripts
        
        # Personal configuration
        "config/",  # All config files
        
        # Personal automation scripts  
        "scripts/", # All scripts folder
        
        # Personal documentation
        "docs/",    # All docs folder
        "PROJECT-CLEANUP-COMPLETE.md",
        
        # Your environment files (already in .gitignore)
        ".env*",
        "*.pem",
        "*.key"
    ]
    
    base_path = Path(".")
    
    # Copy public files
    print("\n📁 Copying public files:")
    for file_path in public_files:
        source = base_path / file_path
        dest = public_repo / file_path
        
        if source.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, dest)
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  {file_path} (not found)")
    
    # Create public README
    create_public_readme(public_repo)
    
    # Create public .gitignore
    create_public_gitignore(public_repo)
    
    print(f"\n✅ Clean public repository created at: {public_repo}")
    return public_repo

def create_public_readme(repo_path):
    """Create a clean public README"""
    readme_content = """# Smart Shopping Platform

A modern, secure e-commerce platform built with Python FastAPI and PostgreSQL.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication
- **Product Management**: Complete product catalog system
- **Shopping Cart**: Advanced cart functionality
- **Order Processing**: Full order management
- **Admin Dashboard**: Administrative controls
- **Responsive Design**: Mobile-friendly interface
- **Cloud Ready**: Optimized for AWS deployment

## 🛠️ Technology Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Authentication**: JWT tokens
- **Hosting**: AWS EC2, RDS
- **Security**: CORS, input validation, SQL injection protection

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/smart-shopping-platform.git
   cd smart-shopping-platform
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file with your configuration
   AWS_DB_HOST=your_database_host
   AWS_DB_PORT=5432
   AWS_DB_NAME=your_database_name
   AWS_DB_USER=your_database_user
   AWS_DB_PASSWORD=your_database_password
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

4. **Initialize database**:
   ```bash
   # Run the SQL schema files in database/
   psql -h your_host -U your_user -d your_db -f database/aws_postgresql_schema.sql
   ```

5. **Run the application**:
   ```bash
   python secure_aws_shopping.py
   ```

## 🌐 Usage

- **Main Application**: `http://localhost:8888`
- **API Documentation**: `http://localhost:8888/docs`
- **Company Website**: `http://localhost:8888/company`

## 📚 API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login  
- `GET /products` - List products
- `POST /cart/add` - Add to cart
- `GET /orders` - User orders
- `GET /admin/*` - Admin endpoints

## 🔒 Security Features

- JWT authentication
- Password hashing
- SQL injection protection
- CORS configuration
- Input validation
- Rate limiting ready

## 🚀 Deployment

This application is designed for cloud deployment with:
- AWS EC2 for hosting
- AWS RDS for PostgreSQL database
- Environment-based configuration
- Production-ready security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

See LICENSE file for details.

## 🏢 Company

**Spirit of the Immortals Ltd**  
Professional E-commerce Solutions

---
*Built with ❤️ for modern e-commerce*
"""
    
    with open(repo_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✅ Created public README.md")

def create_public_gitignore(repo_path):
    """Create a clean public .gitignore"""
    gitignore_content = """# Smart Shopping Platform - Git Ignore

# Environment files
.env*
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Secrets and Keys
*.key
*.pem
*.crt

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Runtime data
pids
*.pid
*.seed
*.pid.lock
"""
    
    with open(repo_path / ".gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("  ✅ Created public .gitignore")

def show_file_categorization():
    """Show what files will be public vs private"""
    print("📋 File Categorization:")
    print("=" * 50)
    
    print("\n🌐 PUBLIC (Essential Code - Will be in GitHub):")
    public_categories = {
        "Core Application": ["secure_aws_shopping.py", "requirements.txt", "runtime.txt", "Procfile"],
        "Frontend": ["frontend/", "company-website/"],
        "Database Schema": ["database/*.sql", "database/README.md", "database/imports/*.json"],
        "Documentation": ["README.md", ".gitignore", "LICENSE"]
    }
    
    for category, files in public_categories.items():
        print(f"  📁 {category}:")
        for file in files:
            print(f"    ✅ {file}")
    
    print(f"\n🔒 PRIVATE (Your Reference Files - Stay Local):")
    private_categories = {
        "Personal Scripts": ["*.ps1", "*.sh", "scripts/"],
        "Configuration": ["config/", "docs/"],
        "Deployment Docs": ["docs/", "PROJECT-CLEANUP-COMPLETE.md"],
        "Sensitive Files": [".env*", "*.pem", "*.key"]
    }
    
    for category, files in private_categories.items():
        print(f"  📁 {category}:")
        for file in files:
            print(f"    🔒 {file}")

def main():
    print("🎯 Repository Cleanup - Public vs Private Files")
    print("=" * 55)
    
    show_file_categorization()
    
    print("\n🤔 What would you like to do?")
    print("1. 🌐 CREATE CLEAN PUBLIC REPO - Only essential code")
    print("2. 📊 SHOW ANALYSIS ONLY - See what would be public/private")
    print("3. 🔒 CURRENT REPO TO PRIVATE - Keep current as personal reference")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🌐 Creating clean public repository...")
        public_repo = create_public_repository()
        print(f"\n✅ DONE! Clean public repo created at: {public_repo}")
        print("\n💡 Next steps:")
        print(f"   cd {public_repo}")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial public release'")
        print("   # Create GitHub repo and push")
        print("\n🔒 Your original folder remains as your private reference!")
        
    elif choice == "2":
        print("\n📊 Analysis complete!")
        print("💡 Run option 1 when ready to create the clean public version.")
        
    elif choice == "3":
        print("\n🔒 Recommended approach:")
        print("   1. Keep current folder as your private workspace")
        print("   2. Create clean public version with option 1")
        print("   3. Push only the clean version to GitHub")
        print("   4. Use your private folder for continued development")
        
    else:
        print("❌ Invalid choice. Please run again and choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
