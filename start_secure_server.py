#!/usr/bin/env python3
"""
Start the Secure Smart Shopping Server with AWS PostgreSQL
"""

import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def check_requirements():
    """Check if all required files and dependencies exist"""
    required_files = [
        ".env",
        "secure_aws_shopping.py",
        "database/aws_postgresql_manager.py",
        "frontend/index.html",
        "frontend/js/app.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_environment():
    """Check environment variables"""
    required_env_vars = [
        "AWS_DB_HOST",
        "AWS_DB_PORT", 
        "AWS_DB_NAME",
        "AWS_DB_USER",
        "AWS_DB_PASSWORD"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please check your .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def install_dependencies():
    """Install required Python packages"""
    requirements = [
        "fastapi[all]",
        "uvicorn[standard]",
        "psycopg2-binary",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "jinja2",
        "python-dotenv",
        "pandas"
    ]
    
    print("📦 Installing dependencies...")
    try:
        for req in requirements:
            print(f"   Installing {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Smart Shopping Server...")
    print("📡 API URL: http://localhost:8000")
    print("🌐 Frontend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/admin/docs")
    print("\n🔐 Features:")
    print("   ✓ AWS PostgreSQL Database Integration")
    print("   ✓ JWT Authentication Required")
    print("   ✓ Secure Registration & Login")
    print("   ✓ Shopping Lists Management")
    print("   ✓ Store Price Comparison")
    print("   ✓ Savings Analysis")
    print("   ✓ Active Promotions")
    print("\n📝 Note: All features require user registration/login with AWS DB")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        uvicorn.run(
            "secure_aws_shopping:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["."],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🎯 Smart Shopping Platform - Secure AWS Edition")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check requirements
    if not check_requirements():
        print("\n💡 Please ensure all required files are present")
        return
    
    if not check_environment():
        print("\n💡 Please configure your AWS database credentials in .env")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n💡 Please install dependencies manually:")
        print("   pip install fastapi[all] uvicorn[standard] psycopg2-binary python-jose[cryptography] passlib[bcrypt]")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
