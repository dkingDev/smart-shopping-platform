#!/usr/bin/env python3
"""
Quick Test and Start for Secure Smart Shopping Platform
"""

import os
import sys
from dotenv import load_dotenv

def test_setup():
    """Test the setup quickly"""
    print("🔧 Testing Smart Shopping Platform Setup...")
    
    # Load environment
    load_dotenv()
    
    # Test environment variables
    aws_vars = ['AWS_DB_HOST', 'AWS_DB_PORT', 'AWS_DB_NAME', 'AWS_DB_USER', 'AWS_DB_PASSWORD']
    missing = [var for var in aws_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    
    print("✅ Environment variables configured")
      # Test database connection
    try:
        # Add parent directory to path for imports
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from database.aws_postgresql_manager import AWSPostgreSQLManager
        db_manager = AWSPostgreSQLManager()
        print("✅ AWS PostgreSQL connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

    # Test backend import
    try:
        import secure_aws_shopping
        print("✅ Backend imports successfully")
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False
    
    return True

def start_server():
    """Start the server"""
    print("\n🚀 Starting Secure Smart Shopping Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Frontend Application: http://localhost:8000/frontend/")
    print("📚 API Documentation: http://localhost:8000/admin/docs")
    print("\n🔐 Security Features Enabled:")
    print("   ✓ JWT Authentication Required")
    print("   ✓ AWS PostgreSQL Database")
    print("   ✓ Password Hashing (bcrypt)")
    print("   ✓ CORS Protection")
    print("   ✓ User Activity Logging")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    try:
        os.system("uvicorn secure_aws_shopping:app --host 0.0.0.0 --port 8000 --reload")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    if test_setup():
        print("✅ All tests passed!")
        start_server()
    else:
        print("❌ Setup tests failed. Please check your configuration.")
        sys.exit(1)
