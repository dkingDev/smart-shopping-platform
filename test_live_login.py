#!/usr/bin/env python3
"""Test live user registration and login functionality"""

import sys
import os
import requests
import json
from datetime import datetime

sys.path.append('.')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env')

def test_live_login_system():
    print("🧪 TESTING LIVE LOGIN SYSTEM")
    print("=" * 40)
    
    # Test user data
    test_email = "live.user@realsite.com"
    test_password = "SecureLivePass123!"
    test_name = "Live Test User"
    
    base_url = "http://localhost:9999"
    
    print(f"📡 Testing against: {base_url}")
    
    try:
        # 1. Test Registration
        print("\n1️⃣ Testing User Registration...")
        registration_data = {
            "full_name": test_name,
            "email": test_email,
            "password": test_password,
            "location": "London"        }
        
        response = requests.post(f"{base_url}/auth/register", json=registration_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("   ✅ Registration successful!")
            reg_data = response.json()
            print(f"   📧 Email: {reg_data.get('data', {}).get('user', {}).get('email')}")
            print(f"   👤 Name: {reg_data.get('data', {}).get('user', {}).get('full_name')}")
        elif response.status_code == 400:
            print("   ⚠️ User already exists, proceeding to login test...")
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return False
        
        # 2. Test Login
        print("\n2️⃣ Testing User Login...")
        login_data = {
            "email": test_email,
            "password": test_password
        }
        
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            login_data = response.json()
            token = login_data.get('access_token')
            user_info = login_data.get('user', {})
            
            print(f"   🎫 Token received: {token[:20]}...")
            print(f"   👤 User ID: {user_info.get('id')}")
            print(f"   📧 Email: {user_info.get('email')}")
            print(f"   👤 Name: {user_info.get('full_name')}")
            
            # 3. Test Token Verification
            print("\n3️⃣ Testing Token Verification...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/auth/verify-token", headers=headers)
            
            if response.status_code == 200:
                print("   ✅ Token verification successful!")
                return True
            else:
                print(f"   ❌ Token verification failed: {response.text}")
                return False
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def verify_database_state():
    """Verify the database is clean and ready"""
    print("\n🗄️ VERIFYING DATABASE STATE")
    print("=" * 30)
    
    try:
        from database.aws_postgresql_manager import AWSPostgreSQLManager
        
        db_manager = AWSPostgreSQLManager()
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check users table
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()[0]
                print(f"📊 Total users in database: {user_count}")
                
                # Show recent users (non-test)
                cur.execute("""
                    SELECT id, email, full_name, created_at 
                    FROM users 
                    WHERE email NOT LIKE '%test%' 
                    AND email NOT LIKE '%example.com%'
                    ORDER BY created_at DESC
                    LIMIT 5
                """)
                users = cur.fetchall()
                
                if users:
                    print("📋 Recent live users:")
                    for user in users:
                        print(f"   ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Created: {user[3]}")
                else:
                    print("✅ No live users yet - database is clean")
                
                return True
                
    except Exception as e:
        print(f"❌ Database verification error: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 LIVE LOGIN SYSTEM TEST - {datetime.now()}")
    print("=" * 60)
    
    # Verify database state
    db_ok = verify_database_state()
    
    if db_ok:
        # Test live login system
        success = test_live_login_system()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ALL TESTS PASSED!")
            print("✅ Live login system is working correctly")
            print("🚀 Ready for real users!")
        else:
            print("❌ Some tests failed")
            print("🔧 Please check the system configuration")
    else:
        print("❌ Database verification failed")
        print("🔧 Please check your AWS database connection")
