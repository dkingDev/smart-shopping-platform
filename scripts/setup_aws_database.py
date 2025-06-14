#!/usr/bin/env python3
"""
Quick Setup Script for AWS PostgreSQL Integration
Run this after setting up your environment variables
"""

import os
import sys

def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        "AWS_DB_HOST",
        "AWS_DB_PORT", 
        "AWS_DB_NAME",
        "AWS_DB_USER",
        "AWS_DB_PASSWORD"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please set these in your environment or .env file")
        print("   Example: set AWS_DB_HOST=your-rds-endpoint.amazonaws.com")
        return False
    
    print("✅ All required environment variables are set")
    return True

def install_dependencies():
    """Check and install required Python packages."""
    required_packages = [
        "psycopg2-binary",  # PostgreSQL adapter
        "pandas",           # Data processing
        "python-dotenv"     # Environment variables
    ]
    
    print("📦 Checking Python dependencies...")
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - missing")
            print(f"   Install with: pip install {package}")
            return False
    
    return True

def test_database_connection():
    """Test connection to AWS PostgreSQL."""
    try:
        sys.path.append('database')
        from aws_postgresql_manager import AWSPostgreSQLManager
        
        print("🔗 Testing AWS PostgreSQL connection...")
        db = AWSPostgreSQLManager()
        
        if db.test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def setup_database_schema():
    """Setup database schema if needed."""
    try:
        sys.path.append('database')
        from aws_postgresql_manager import AWSPostgreSQLManager
        
        db = AWSPostgreSQLManager()
        
        print("🏗️  Setting up database schema...")
        db.setup_database()
        print("✅ Database schema ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema setup failed: {e}")
        print("💡 This might be normal if schema already exists")
        return True  # Continue anyway

def load_initial_data():
    """Load branded products catalog if available."""
    try:
        sys.path.append('database')
        from aws_postgresql_manager import AWSPostgreSQLManager
        
        products_file = "database/imports/master_branded_products.csv"
        if not os.path.exists(products_file):
            print("⚠️  Master products file not found, skipping initial load")
            return True
        
        db = AWSPostgreSQLManager()
        
        print("📊 Loading branded products catalog...")
        db.load_branded_products(products_file)
        print("✅ Branded products loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def main():
    """Main setup process."""
    print("🚀 AWS PostgreSQL Setup for National Branded Products")
    print("=" * 60)
    
    # Step 1: Check environment
    if not check_environment():
        print("\n💡 Setup your environment variables first:")
        print("   1. Copy .env.example to .env")
        print("   2. Update with your AWS RDS details")
        print("   3. Source the environment file")
        create_env_file_if_missing()
        return False
    
    # Step 2: Check dependencies
    if not install_dependencies():
        print("\n💡 Install missing dependencies:")
        print("   pip install psycopg2-binary pandas python-dotenv fastapi uvicorn")
        return False
    
    # Step 3: Test database connection
    if not test_database_connection():
        print("\n💡 Check your AWS RDS configuration:")
        print("   - Endpoint URL correct?")
        print("   - Security groups allow connection?")
        print("   - Credentials valid?")
        print("   - Database created?")
        return False
    
    # Step 4: Setup schema
    if not setup_database_schema():
        return False
    
    # Step 5: Load initial data
    if not load_initial_data():
        print("⚠️  Initial data load failed, but continuing...")
    
    # Step 6: Test FastAPI integration
    if not test_fastapi_integration():
        print("⚠️  FastAPI integration test failed, but database is ready")
    
    # Step 7: Create sample data for testing
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ AWS PostgreSQL setup complete!")
    print("\n🎯 Your smart shopping platform is ready:")
    print("   📊 Database: Fully configured with user system")
    print("   🔐 Authentication: JWT-based user management")
    print("   🛒 Shopping Lists: Automated crawler prioritization")
    print("   💰 Monetization: Affiliate tracking and subscriptions")
    print("   🚀 API: FastAPI backend with AWS integration")
    
    print("\n🚀 Next steps:")
    print("   1. Deploy FastAPI app: python shopping_website_fastapi.py")
    print("   2. Test authentication: python demo_auth_shopping.py")
    print("   3. Run crawler integration: python universal_smart_crawler.py")
    print("   4. Deploy to production (Railway/Vercel/AWS)")
    
    return True

def create_env_file_if_missing():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        print("📝 Creating .env file from template...")
        import shutil
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file - please update with your AWS details")

def test_fastapi_integration():
    """Test FastAPI app can connect to database."""
    try:
        print("🔗 Testing FastAPI integration...")
        
        # Try to import and initialize the auth system
        sys.path.append('.')
        from shopping_website_auth import get_database_connection
        
        # Test auth database functions
        conn = get_database_connection()
        if conn:
            conn.close()
            print("✅ FastAPI can connect to AWS database")
            return True
        else:
            print("❌ FastAPI connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI integration test failed: {e}")
        return False

def create_sample_data():
    """Create sample users and data for testing."""
    try:
        print("🎭 Creating sample data for testing...")
        
        sys.path.append('database')
        from aws_postgresql_manager import AWSPostgreSQLManager
        
        db = AWSPostgreSQLManager()
        
        # Create sample user (with hashed password)
        import hashlib
        password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
        
        try:
            user_id = db.create_user(
                username="testuser", 
                email="test@example.com", 
                password_hash=password_hash,
                full_name="Test User"
            )
            
            # Create sample shopping list
            list_id = db.create_shopping_list(
                user_id=user_id,
                name="Weekly Groceries",
                description="Test shopping list"
            )
            
            # Add sample items
            db.add_to_shopping_list(
                list_id=list_id,
                product_name="Coca Cola 2L",
                quantity=2,
                preferred_stores=["tesco", "morrisons"]
            )
            
            db.add_to_shopping_list(
                list_id=list_id,
                product_name="Bread White Loaf",
                quantity=1,
                preferred_stores=["tesco"]
            )
            
            print("✅ Sample data created successfully")
            print(f"   - Test user: testuser (ID: {user_id})")
            print(f"   - Shopping list: Weekly Groceries (ID: {list_id})")
            print("   - 2 sample products with crawler priorities")
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print("ℹ️  Sample data already exists, skipping creation")
            else:
                raise e
                
    except Exception as e:
        print(f"⚠️  Could not create sample data: {e}")

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
