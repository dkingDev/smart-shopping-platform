#!/usr/bin/env python3
"""
Full Cleanup Script for Secure Smart Shopping Platform
Removes obsolete files and organizes the workspace for production
"""

import os
import shutil
import json
from pathlib import Path

def cleanup_workspace():
    """Perform comprehensive cleanup of the workspace"""
    
    print("🧹 Starting Full Workspace Cleanup...")
    
    # Files to keep (essential for secure AWS platform)
    essential_files = {
        # Core application files
        'secure_aws_shopping.py',
        'quick_start.py',
        '.env',
        '.env.example',
        '.gitignore',
        'requirements.txt',
        'README_SECURE_PLATFORM.md',
        
        # Database files
        'database/aws_postgresql_manager.py',
        'database/aws_postgresql_schema.sql',
        'setup_aws_database.py',
        
        # Frontend files
        'frontend/index.html',
        'frontend/js/app.js',
        
        # Configuration
        'config/database_config.json',
        
        # Documentation
        'docs/api_documentation.md',
        'AWS_RDS_SETUP_GUIDE.md',
        'PRODUCTION_DEPLOYMENT_GUIDE.md',
        
        # Data files
        'processed_price_history.csv',
        
        # Crawler integration
        'universal_smart_crawler.py',
        'populate_aws_demo_data.py'
    }
    
    # Directories to keep
    essential_dirs = {
        'database',
        'frontend',
        'config',
        'docs',
        '.vscode'
    }
    
    # Files and directories to remove
    obsolete_items = [
        # Old demos and prototypes
        'demo_auth_shopping.py',
        'demo_shopping_website.py',
        'complete_system_demo.py',
        'smart_shopping_demo.py',
        'enhanced_shopping_website.py',
        'production_smart_shopping.py',
        'secure_smart_shopping.py',
        'secure_auth.py',
        'shopping_website_app.py',
        'shopping_website_auth.py',
        'shopping_website_fastapi.py',
        'start_secure_server.py',
        
        # Old database files
        'products.db',
        'website_data.db',
        'test_app_collection.db',
        'check_db.py',
        'check_databases.py',
        
        # Test and development files
        'test_*.py',
        'example_usage.py',
        'final_cleanup.py',
        
        # Analysis and reports
        'analysis/',
        'deduplication_report.md',
        'detailed_duplicates_report.csv',
        'duplicate_files_analysis.md',
        'morrisons_own_brand_analysis.md',
        
        # Build and deployment scripts
        'docker-compose.yml',
        'Dockerfile',
        '*.ps1',
        
        # Log files
        '*.log',
        
        # Cache and temporary
        '__pycache__/',
        'processed/',
        'static/',
        'templates/',
        
        # Obsolete documentation
        'ALTERNATIVES_TO_FLASK.md',
        'COMPLETE_SHOPPING_WEBSITE.md',
        'CUSTOMER_APP_STRATEGY.md',
        'FASTAPI_WEBSITE_SUCCESS.md',
        'GITHUB_DEPLOYMENT.md',
        'MISSION_ACCOMPLISHED.md',
        'MONETIZATION_NOW.md',
        'README_Deduplication.md',
        'SHOPPING_WEBSITE_STRATEGY.md',
        'SPACE_OPTIMIZATION_STRATEGY.md',
        'STRATEGY_GUIDE.md',
        
        # Old data directories
        'brand-items-img/',
        'branded-products/',
        'data/',
        'database-ready/',
        'images/',
        
        # Old load testing
        'load_test.py',
        'test_api_features.py'
    ]
    
    cleanup_count = 0
    
    # Remove obsolete files and directories
    for item in obsolete_items:
        item_path = Path(item)
        if item_path.exists():
            try:
                if item_path.is_file():
                    item_path.unlink()
                    print(f"✅ Removed file: {item}")
                elif item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"✅ Removed directory: {item}")
                cleanup_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {item}: {e}")
    
    print(f"\n📊 Cleanup Summary: Removed {cleanup_count} obsolete items")
    return cleanup_count

def organize_remaining_files():
    """Organize the remaining essential files"""
    
    print("\n📁 Organizing remaining files...")
    
    # Ensure essential directories exist
    essential_dirs = ['docs', 'config', 'scripts']
    for dir_name in essential_dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    # Move utility scripts to scripts directory
    utility_scripts = [
        'quick_start.py',
        'setup_aws_database.py',
        'populate_aws_demo_data.py',
        'universal_smart_crawler.py'
    ]
    
    scripts_dir = Path('scripts')
    scripts_dir.mkdir(exist_ok=True)
    
    for script in utility_scripts:
        script_path = Path(script)
        if script_path.exists():
            try:
                new_path = scripts_dir / script
                if not new_path.exists():
                    shutil.move(str(script_path), str(new_path))
                    print(f"📦 Moved {script} to scripts/")
            except Exception as e:
                print(f"❌ Failed to move {script}: {e}")
    
    print("✅ File organization complete")

def update_requirements():
    """Update requirements.txt with only essential dependencies"""
    
    print("\n📋 Updating requirements.txt...")
    
    essential_requirements = [
        "fastapi[all]==0.104.1",
        "uvicorn[standard]==0.24.0",
        "psycopg2-binary==2.9.9",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "jinja2==3.1.2",
        "python-dotenv==1.0.0",
        "pandas==2.1.4",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "lxml==4.9.3"
    ]
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write("# Smart Shopping Platform - Secure AWS Edition\n")
            f.write("# Essential dependencies for production deployment\n\n")
            for req in essential_requirements:
                f.write(f"{req}\n")
        
        print("✅ Updated requirements.txt with essential dependencies")
    except Exception as e:
        print(f"❌ Failed to update requirements.txt: {e}")

def create_project_structure_doc():
    """Create documentation of the cleaned project structure"""
    
    print("\n📄 Creating project structure documentation...")
    
    structure_doc = """# Smart Shopping Platform - Project Structure

## 🏗️ Core Application
- `secure_aws_shopping.py` - Main FastAPI application with AWS PostgreSQL integration
- `requirements.txt` - Essential Python dependencies
- `.env` - Environment configuration (AWS credentials, JWT secrets)
- `.env.example` - Template for environment variables

## 🗄️ Database
- `database/aws_postgresql_manager.py` - AWS PostgreSQL connection and operations
- `database/aws_postgresql_schema.sql` - Complete database schema with triggers/functions

## 🌐 Frontend
- `frontend/index.html` - Single Page Application (SPA) with authentication
- `frontend/js/app.js` - JavaScript application logic with JWT handling

## 🛠️ Scripts
- `scripts/quick_start.py` - Development server launcher with health checks
- `scripts/setup_aws_database.py` - Database initialization and schema setup
- `scripts/populate_aws_demo_data.py` - Demo data population for testing
- `scripts/universal_smart_crawler.py` - Store data crawler for AWS database

## 📚 Documentation
- `README_SECURE_PLATFORM.md` - Complete platform documentation
- `AWS_RDS_SETUP_GUIDE.md` - AWS RDS PostgreSQL setup instructions
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Production deployment guide
- `docs/` - Additional documentation files

## 📊 Data
- `processed_price_history.csv` - Historical price data for analysis

## ⚙️ Configuration
- `config/` - Configuration files and templates
- `.vscode/` - VS Code workspace settings
- `.gitignore` - Git ignore patterns

## 🚀 Quick Start
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

## 🔐 Security Features
- JWT authentication with bcrypt password hashing
- AWS PostgreSQL database for all data storage
- CORS protection for secure API access
- User activity logging and session management

## 📱 Frontend Features
- User registration and login with AWS database
- Protected dashboard requiring authentication
- Shopping list management with persistence
- Price comparison across multiple stores
- Savings analysis and promotional offers
- Real-time data from AWS PostgreSQL

## 🌍 Deployment Options
- **Local Development**: Use `scripts/quick_start.py`
- **GitHub Pages**: Deploy frontend with API backend on cloud
- **Production**: Deploy complete system with HTTPS/SSL
"""
    
    try:
        with open('docs/PROJECT_STRUCTURE.md', 'w') as f:
            f.write(structure_doc)
        print("✅ Created project structure documentation")
    except Exception as e:
        print(f"❌ Failed to create structure doc: {e}")

def main():
    """Main cleanup function"""
    print("🎯 Smart Shopping Platform - Full Cleanup")
    print("=" * 60)
    
    # Perform cleanup
    cleanup_count = cleanup_workspace()
    
    # Organize files
    organize_remaining_files()
    
    # Update requirements
    update_requirements()
    
    # Create documentation
    create_project_structure_doc()
    
    print(f"\n✅ Full cleanup complete!")
    print(f"📊 Removed {cleanup_count} obsolete files/directories")
    print("🎯 Workspace is now optimized for production deployment")
    print("\n📋 Essential files remaining:")
    print("   ✓ secure_aws_shopping.py (main application)")
    print("   ✓ frontend/ (SPA with authentication)")
    print("   ✓ database/ (AWS PostgreSQL integration)")
    print("   ✓ scripts/ (utilities and setup)")
    print("   ✓ docs/ (documentation)")
    print("   ✓ requirements.txt (dependencies)")
    print("   ✓ .env (configuration)")

if __name__ == "__main__":
    main()
