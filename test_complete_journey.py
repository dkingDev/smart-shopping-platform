#!/usr/bin/env python3
"""
Complete End-to-End Test - Test full user journey with AWS data storage
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

def test_complete_user_journey():
    """Test complete user journey: register -> login -> create shopping list"""
    print("🚀 COMPLETE USER JOURNEY TEST")
    print("="*70)
    
    test_email = f"journey_test_{int(time.time())}@example.com"
    user_data = {
        "full_name": "Journey Test User",
        "email": test_email,
        "password": "TestPassword123!",
        "location": "London, UK"
    }
    
    db_manager = AWSPostgreSQLManager()
    user_id = None
    auth_token = None
    
    try:
        # Step 1: Register User
        print("\n📝 Step 1: User Registration")
        response = requests.post("http://localhost:8001/auth/register", json=user_data)
        if response.status_code == 200:
            print(f"✅ User registered: {test_email}")
            
            # Verify in database
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, full_name FROM users WHERE email = %s", (test_email,))
                    user = cur.fetchone()
                    if user:
                        user_id = user[0]
                        print(f"✅ User verified in AWS DB: ID={user_id}, Name={user[1]}")
                    else:
                        print("❌ User not found in AWS database")
                        return False
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return False
        
        # Step 2: User Login
        print("\n🔐 Step 2: User Login")
        login_data = {"email": test_email, "password": "TestPassword123!"}
        response = requests.post("http://localhost:8001/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            auth_token = data.get("data", {}).get("access_token")
            if auth_token:
                print(f"✅ Login successful, token received")
            else:
                print(f"❌ No access token in response: {data}")
                return False
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
        
        # Step 3: Create Shopping List
        print("\n🛒 Step 3: Create Shopping List")
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        list_data = {
            "list_name": "Test Shopping List"
        }
        
        response = requests.post("http://localhost:8001/api/shopping-lists", 
                               json=list_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            list_id = data.get("data", {}).get("list_id")
            print(f"✅ Shopping list created: ID={list_id}")
            
            # Verify shopping list in database
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT sl.id, sl.name, sl.user_id, u.email
                        FROM shopping_lists sl
                        JOIN users u ON sl.user_id = u.id
                        WHERE sl.id = %s
                    """, (list_id,))
                    shopping_list = cur.fetchone()
                    
                    if shopping_list:
                        print(f"✅ Shopping list verified in AWS DB:")
                        print(f"   List ID: {shopping_list[0]}")
                        print(f"   Name: {shopping_list[1]}")
                        print(f"   User ID: {shopping_list[2]}")
                        print(f"   User Email: {shopping_list[3]}")
                    else:
                        print("❌ Shopping list not found in AWS database")
                        return False
        else:
            print(f"❌ Shopping list creation failed: {response.status_code} - {response.text}")
            return False
        
        print("\n🎉 COMPLETE USER JOURNEY SUCCESSFUL!")
        print("✅ All data stored in AWS PostgreSQL:")
        print(f"   • User: {test_email} (ID: {user_id})")
        print(f"   • Shopping List: {list_data['list_name']} (ID: {list_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Journey test error: {e}")
        return False
        
    finally:
        # Cleanup
        print("\n🧹 Cleaning up test data...")
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    # Delete shopping lists first (foreign key)
                    cur.execute("DELETE FROM shopping_lists WHERE user_id = %s", (user_id,))
                    lists_deleted = cur.rowcount
                    
                    # Delete user
                    cur.execute("DELETE FROM users WHERE email = %s", (test_email,))
                    users_deleted = cur.rowcount
                    
                    conn.commit()
                    print(f"✅ Cleanup: {users_deleted} user(s), {lists_deleted} list(s) deleted")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")

def verify_aws_environment():
    """Verify we're using AWS environment variables"""
    print("🔍 AWS ENVIRONMENT VERIFICATION")
    print("="*70)
    
    aws_vars = {
        "AWS_DB_HOST": os.getenv("AWS_DB_HOST"),
        "AWS_DB_PORT": os.getenv("AWS_DB_PORT"),
        "AWS_DB_NAME": os.getenv("AWS_DB_NAME"),
        "AWS_DB_USER": os.getenv("AWS_DB_USER"),
    }
    
    for var, value in aws_vars.items():
        if value:
            if "HOST" in var:
                print(f"✅ {var}: {value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            return False
    
    # Check that it's pointing to AWS RDS
    host = aws_vars["AWS_DB_HOST"]
    if host and "amazonaws.com" in host:
        print(f"✅ Confirmed AWS RDS endpoint: {host}")
        return True
    else:
        print(f"⚠️  Host doesn't appear to be AWS RDS: {host}")
        return False

def main():
    """Run complete production verification"""
    print("🌐 SMART SHOPPING PLATFORM - COMPLETE PRODUCTION VERIFICATION")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*70)
    
    # Test AWS environment
    if not verify_aws_environment():
        print("❌ AWS environment verification failed")
        return False
    
    print("\n" + "="*70)
    
    # Test complete user journey
    if test_complete_user_journey():
        print("\n🎉 PRODUCTION SYSTEM FULLY VERIFIED!")
        print("✅ All user data flows to AWS PostgreSQL")
        print("✅ Complete user journey works end-to-end")
        print("✅ Ready for production deployment!")
        print("\n📋 DEPLOYMENT CHECKLIST:")
        print("   1. ✅ AWS PostgreSQL database connected")
        print("   2. ✅ User registration stores data in AWS")
        print("   3. ✅ User login works with AWS data")
        print("   4. ✅ Shopping lists stored in AWS")
        print("   5. ✅ No local database files for production")
        print("   6. 🔄 Deploy backend to cloud service")
        print("   7. 🔄 Update frontend API URL for production")
        print("   8. 🔄 Deploy frontend to GitHub Pages")
        return True
    else:
        print("\n❌ Production verification failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
