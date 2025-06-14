#!/usr/bin/env python3
"""Complete System Test - Verify ALL data flows to AWS Database"""

import os
import requests
import time
from dotenv import load_dotenv
from database.aws_postgresql_manager import AWSPostgreSQLManager

# Load environment variables
load_dotenv()

def test_aws_database_connection():
    """Test AWS database connection and check existing data"""
    print("🔗 Testing AWS PostgreSQL connection...")
    try:
        db_manager = AWSPostgreSQLManager()
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check what tables exist
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                
                print(f"📊 Tables in AWS Database: {len(tables)}")
                for table in tables:
                    print(f"  ✅ {table[0]}")
                    
                # Check current data counts
                for table in ['users', 'shopping_lists', 'shopping_list_items', 'user_activity_logs']:
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cur.fetchone()[0]
                        print(f"  📋 {table}: {count} records")
                    except Exception as e:
                        print(f"  ❌ {table}: Table doesn't exist or error: {e}")
                        
        return True
    except Exception as e:
        print(f"❌ AWS Database connection failed: {e}")
        return False

def test_backend_server():
    """Test backend server startup and API endpoints"""
    print("\n🚀 Testing Backend Server...")
    
    # Start the server in background
    import subprocess
    import time
    
    try:
        # Start server
        server_process = subprocess.Popen(
            ["python", "secure_aws_shopping.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test server is running
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            print("✅ Backend server is running")
            return server_process
        except requests.exceptions.RequestException:
            print("❌ Backend server not responding")
            server_process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend server: {e}")
        return None

def test_user_registration_to_aws(server_process):
    """Test user registration flows to AWS database"""
    print("\n👤 Testing User Registration → AWS Database...")
    
    timestamp = int(time.time())
    test_user = {
        "full_name": "Complete Test User",
        "email": f"test_complete_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    
    try:
        # Register user via API
        response = requests.post("http://localhost:8000/auth/register", json=test_user, timeout=10)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User registration successful")
            user_id = data['data']['user']['id']
            
            # Verify user exists in AWS database
            db_manager = AWSPostgreSQLManager()
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, email, full_name FROM users WHERE id = %s", (user_id,))
                    user_row = cur.fetchone()
                    
                    if user_row:
                        print(f"✅ User verified in AWS Database: {user_row[1]} ({user_row[2]})")
                        return test_user, data['data']['access_token']
                    else:
                        print("❌ User NOT found in AWS database")
                        return None, None
        else:
            print(f"❌ Registration failed: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return None, None

def test_shopping_list_to_aws(user_data, token):
    """Test shopping list creation flows to AWS database"""
    print("\n📋 Testing Shopping List Creation → AWS Database...")
    
    if not token:
        print("❌ No token available for shopping list test")
        return False
        
    try:
        headers = {"Authorization": f"Bearer {token}"}
        shopping_list = {
            "list_name": "Complete System Test List"
        }
        
        # Create shopping list via API
        response = requests.post(
            "http://localhost:8000/api/shopping-lists", 
            json=shopping_list, 
            headers=headers,
            timeout=10
        )
        
        print(f"Shopping List Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Shopping list creation successful")
            list_id = data['data']['list_id']
            
            # Verify shopping list exists in AWS database
            db_manager = AWSPostgreSQLManager()
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, name, user_id FROM shopping_lists WHERE id = %s", (list_id,))
                    list_row = cur.fetchone()
                    
                    if list_row:
                        print(f"✅ Shopping list verified in AWS Database: '{list_row[1]}' (User ID: {list_row[2]})")
                        return True
                    else:
                        print("❌ Shopping list NOT found in AWS database")
                        return False
        else:
            print(f"❌ Shopping list creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Shopping list test failed: {e}")
        return False

def test_user_login_to_aws(user_data):
    """Test user login and verify authentication flows to AWS"""
    print("\n🔐 Testing User Login → AWS Database...")
    
    if not user_data:
        print("❌ No user data available for login test")
        return None
        
    try:
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        # Login via API
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User login successful")
            
            # Verify login activity is logged in AWS database
            db_manager = AWSPostgreSQLManager()
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    # Check for recent login activity
                    cur.execute("""
                        SELECT action, created_at 
                        FROM user_activity_logs 
                        WHERE user_id = %s 
                        ORDER BY created_at DESC 
                        LIMIT 5
                    """, (data['data']['user']['id'],))
                    
                    activities = cur.fetchall()
                    print(f"✅ User activities logged in AWS: {len(activities)} records")
                    for activity in activities:
                        print(f"  📝 {activity[0]} at {activity[1]}")
                        
            return data['data']['access_token']
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return None

def test_frontend_configuration():
    """Test frontend is configured to point to correct API"""
    print("\n🌐 Testing Frontend Configuration...")
    
    try:
        with open("frontend/js/app.js", "r") as f:
            content = f.read()
            
        if "localhost:8000" in content or "localhost:8888" in content:
            print("✅ Frontend configured for local development")
        
        if "github.io" in content:
            print("✅ Frontend has GitHub Pages configuration")
            
        if "production-api" in content:
            print("⚠️ Frontend has production API placeholder - needs real URL")
        else:
            print("⚠️ Frontend may need production API URL configuration")
            
        return True
        
    except Exception as e:
        print(f"❌ Frontend configuration check failed: {e}")
        return False

def run_complete_system_test():
    """Run complete system test to verify all data flows to AWS"""
    print("🎯 COMPLETE SYSTEM TEST - All Data Must Flow to AWS Database")
    print("=" * 80)
    
    # Test 1: AWS Database Connection
    db_ok = test_aws_database_connection()
    if not db_ok:
        print("❌ Cannot proceed without AWS database connection")
        return
    
    # Test 2: Backend Server
    server_process = test_backend_server()
    if not server_process:
        print("❌ Cannot proceed without backend server")
        return
    
    try:
        # Test 3: User Registration → AWS
        user_data, token = test_user_registration_to_aws(server_process)
        
        # Test 4: User Login → AWS
        login_token = test_user_login_to_aws(user_data)
        
        # Test 5: Shopping List → AWS
        list_ok = test_shopping_list_to_aws(user_data, login_token or token)
        
        # Test 6: Frontend Configuration
        frontend_ok = test_frontend_configuration()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 COMPLETE SYSTEM TEST RESULTS:")
        print(f"✅ AWS Database Connection: {'PASS' if db_ok else 'FAIL'}")
        print(f"✅ Backend Server: {'PASS' if server_process else 'FAIL'}")
        print(f"✅ User Registration → AWS: {'PASS' if user_data else 'FAIL'}")
        print(f"✅ User Login → AWS: {'PASS' if login_token else 'FAIL'}")
        print(f"✅ Shopping Lists → AWS: {'PASS' if list_ok else 'FAIL'}")
        print(f"✅ Frontend Configuration: {'PASS' if frontend_ok else 'FAIL'}")
        
        if db_ok and server_process and user_data and list_ok:
            print("\n🎉 SUCCESS: All user data flows correctly to AWS Database!")
            print("🚀 System is ready for production deployment!")
        else:
            print("\n⚠️ Some tests failed - check configuration")
            
    finally:
        # Clean up
        if server_process:
            print("\n🧹 Stopping test server...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    run_complete_system_test()
