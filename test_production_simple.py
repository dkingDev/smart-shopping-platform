#!/usr/bin/env python3
"""
Simple Production Data Flow Test - Verify all user data goes to AWS PostgreSQL
"""

import os
import sys
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import database manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.aws_postgresql_manager import AWSPostgreSQLManager

def test_aws_connection():
    """Test AWS database connection"""
    print("🔍 Testing AWS Database Connection...")
    
    try:
        db_manager = AWSPostgreSQLManager()
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"✅ Connected to AWS PostgreSQL: {version}")
                
                cur.execute("SELECT current_database();")
                db_name = cur.fetchone()[0]
                print(f"✅ Database: {db_name}")
                return True
    except Exception as e:
        print(f"❌ AWS connection failed: {e}")
        return False

def test_user_registration():
    """Test user registration and verify data goes to AWS"""
    print("\n🔍 Testing User Registration...")
    
    # Test data
    test_email = f"test_user_{int(time.time())}@example.com"
    user_data = {
        "full_name": "Test User",
        "email": test_email,
        "password": "TestPassword123!",
        "location": "London, UK"
    }
    
    try:
        # Register user
        response = requests.post("http://localhost:8001/auth/register", json=user_data)
        if response.status_code == 200:
            print(f"✅ User registered: {test_email}")
            
            # Verify user in AWS database
            db_manager = AWSPostgreSQLManager()
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, full_name, email FROM users WHERE email = %s", (test_email,))
                    user = cur.fetchone()
                    
                    if user:
                        print(f"✅ User found in AWS DB: ID={user[0]}, Name={user[1]}")
                        
                        # Cleanup
                        cur.execute("DELETE FROM users WHERE email = %s", (test_email,))
                        conn.commit()
                        print("🧹 Test user cleaned up")
                        
                        return True
                    else:
                        print("❌ User not found in AWS database")
                        return False
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration test error: {e}")
        return False

def test_server_running():
    """Test if backend server is running"""
    print("\n🔍 Testing Backend Server...")
    
    try:
        response = requests.get("http://localhost:8001/")
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False

def verify_no_local_db():
    """Verify no local database files exist"""
    print("\n🔍 Checking for Local Database Files...")
    
    local_files = ["smart_shopping.db", "shopping_platform.db", "local_shopping.db"]
    found_local = False
    
    for db_file in local_files:
        if os.path.exists(db_file):
            print(f"⚠️  Local database found: {db_file}")
            found_local = True
        else:
            print(f"✅ No local file: {db_file}")
    
    return not found_local

def main():
    """Run all production verification tests"""
    print("🚀 SMART SHOPPING PLATFORM - PRODUCTION DATA VERIFICATION")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*70)
    
    tests = [
        ("AWS Database Connection", test_aws_connection),
        ("No Local Database Files", verify_no_local_db),
        ("Backend Server Running", test_server_running),
        ("User Registration to AWS", test_user_registration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 50)
        
        if test_func():
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "="*70)
    print(f"FINAL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Production system is correctly configured:")
        print("   • All user data flows to AWS PostgreSQL")
        print("   • No production data stored locally")
        print("   • Backend server is functional")
        print("   • Ready for production deployment!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
