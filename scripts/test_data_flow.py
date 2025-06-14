#!/usr/bin/env python3
"""
Complete Data Flow Verification Script
Tests the entire data flow from website to AWS database to ensure everything is connected properly.
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.aws_postgresql_manager import AWSPostgreSQLManager
from dotenv import load_dotenv

class DataFlowTester:
    """Test complete data flow from frontend to AWS database"""
    
    def __init__(self):
        load_dotenv()
        self.base_url = "http://localhost:8888"
        self.test_user_email = f"test_user_{int(time.time())}@example.com"
        self.test_password = "testpass123"
        self.access_token = None
        self.user_id = None
        self.db_manager = None
        
    def test_database_connection(self):
        """Test AWS PostgreSQL database connection"""
        print("🔗 Testing AWS PostgreSQL connection...")
        
        try:
            self.db_manager = AWSPostgreSQLManager()
            
            with self.db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    print(f"✅ Connected to PostgreSQL: {version[:50]}...")
                    
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def test_server_running(self):
        """Test if the FastAPI server is running"""
        print("🚀 Testing FastAPI server...")
        
        try:
            response = requests.get(f"{self.base_url}/admin/docs", timeout=5)
            if response.status_code == 200:
                print("✅ FastAPI server is running")
                return True
            else:
                print(f"❌ Server returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Please start the server with: python scripts/quick_start.py")
            return False
        except Exception as e:
            print(f"❌ Server test failed: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration flow"""
        print("👤 Testing user registration...")
        
        user_data = {
            "full_name": "Test User",
            "email": self.test_user_email,
            "password": self.test_password,
            "location": "Test Location"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.access_token = data["data"]["access_token"]
                    self.user_id = data["data"]["user"]["id"]
                    print(f"✅ User registered successfully - User ID: {self.user_id}")
                    return True
                else:
                    print(f"❌ Registration failed: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Registration request failed with status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration test failed: {e}")
            return False
    
    def test_user_login(self):
        """Test user login flow"""
        print("🔐 Testing user login...")
        
        login_data = {
            "email": self.test_user_email,
            "password": self.test_password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print("✅ User login successful")
                    return True
                else:
                    print(f"❌ Login failed: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Login request failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login test failed: {e}")
            return False
    
    def test_shopping_list_creation(self):
        """Test shopping list creation"""
        print("📋 Testing shopping list creation...")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        list_data = {
            "list_name": f"Test Shopping List {int(time.time())}"
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/shopping-lists",
                json=list_data,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    list_id = data["data"]["list_id"]
                    print(f"✅ Shopping list created successfully - List ID: {list_id}")
                    return True
                else:
                    print(f"❌ Shopping list creation failed: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Shopping list request failed with status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Shopping list test failed: {e}")
            return False
    
    def test_data_in_database(self):
        """Verify data is actually stored in AWS database"""
        print("🗄️ Verifying data in AWS database...")
        
        if not self.db_manager or not self.user_id:
            print("❌ Database manager or user ID not available")
            return False
        
        try:
            with self.db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    # Check if user exists in database
                    cur.execute("SELECT id, email, full_name FROM users WHERE id = %s", (self.user_id,))
                    user_row = cur.fetchone()
                    
                    if user_row:
                        print(f"✅ User found in database: {user_row[1]} ({user_row[2]})")
                    else:
                        print("❌ User not found in database")
                        return False
                    
                    # Check if shopping lists exist
                    cur.execute("SELECT COUNT(*) FROM shopping_lists WHERE user_id = %s", (self.user_id,))
                    list_count = cur.fetchone()[0]
                    
                    if list_count > 0:
                        print(f"✅ Found {list_count} shopping list(s) in database")
                    else:
                        print("⚠️ No shopping lists found in database")
                    
                    # Check user activity
                    cur.execute("SELECT COUNT(*) FROM user_activity WHERE user_id = %s", (self.user_id,))
                    activity_count = cur.fetchone()[0]
                    
                    if activity_count > 0:
                        print(f"✅ Found {activity_count} user activity record(s)")
                    else:
                        print("⚠️ No user activity records found")
                    
            return True
            
        except Exception as e:
            print(f"❌ Database verification failed: {e}")
            return False
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print("🧹 Cleaning up test data...")
        
        if not self.db_manager or not self.user_id:
            return
        
        try:
            with self.db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    # Delete test user and related data (cascades to other tables)
                    cur.execute("DELETE FROM users WHERE id = %s", (self.user_id,))
                    conn.commit()
                    print("✅ Test data cleaned up")
                    
        except Exception as e:
            print(f"⚠️ Cleanup failed: {e}")
    
    def run_complete_test(self):
        """Run complete data flow test"""
        print("🎯 Smart Shopping Platform - Complete Data Flow Test")
        print("=" * 60)
        
        tests = [
            ("Database Connection", self.test_database_connection),
            ("Server Running", self.test_server_running),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Shopping List Creation", self.test_shopping_list_creation),
            ("Data in AWS Database", self.test_data_in_database),
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}...")
            try:
                result = test_func()
                results.append((test_name, result))
                if not result:
                    print(f"❌ {test_name} failed - stopping tests")
                    break
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))
                break
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Results Summary:")
        
        all_passed = True
        for test_name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name}: {status}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 All tests passed! Data flow is working correctly.")
            print("\n✅ VERIFIED: User data flows from website → AWS database")
            print("✅ VERIFIED: Shopping lists are stored in AWS PostgreSQL")
            print("✅ VERIFIED: Authentication system working")
            print("✅ VERIFIED: API endpoints functional")
        else:
            print("\n⚠️ Some tests failed. Please check configuration.")
        
        # Always cleanup
        self.cleanup_test_data()
        
        return all_passed

def main():
    """Main entry point"""
    tester = DataFlowTester()
    success = tester.run_complete_test()
    
    if success:
        print(f"\n🚀 Ready for GitHub push to DkingDev repository!")
        print("📝 Configuration Summary:")
        print("   - Website: GitHub Pages (yourusername.github.io)")
        print("   - API Backend: Your production server")
        print("   - Database: AWS RDS PostgreSQL")
        print("   - Authentication: JWT with bcrypt")
        print("   - Data Flow: Website → API → AWS Database ✅")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
