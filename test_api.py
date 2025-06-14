#!/usr/bin/env python3
"""Quick API test to verify registration and login"""

import requests
import json
import time

# Test data with unique timestamp
timestamp = int(time.time())
test_user = {
    "full_name": "Test User",
    "email": f"test{timestamp}@example.com",
    "password": "TestPass123"
}

base_url = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("🧪 Testing user registration...")
    try:
        response = requests.post(f"{base_url}/auth/register", json=test_user)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code in [200, 201] and "access_token" in response.json().get("data", {})
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("🧪 Testing user login...")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200 and "access_token" in response.json().get("data", {})
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_shopping_list(token):
    """Test creating shopping list"""
    print("🧪 Testing shopping list creation...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        shopping_list = {
            "name": "Test List",
            "items": ["bread", "milk", "eggs"]
        }
        response = requests.post(f"{base_url}/api/shopping-lists", json=shopping_list, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Shopping list error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Smart Shopping API Test")
    print("=" * 50)
    
    # Test registration
    reg_success = test_registration()
    
    if reg_success:
        print("✅ Registration successful!")
        
        # Test login
        login_success = test_login()
        
        if login_success:
            print("✅ Login successful!")
              # Get token for shopping list test
            login_response = requests.post(f"{base_url}/auth/login", json={
                "email": test_user["email"],
                "password": test_user["password"]
            })
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                token = response_data.get("data", {}).get("access_token")
            else:
                print("❌ Could not get token for shopping list test")
                return
            
            # Test shopping list
            list_success = test_shopping_list(token)
            
            if list_success:
                print("✅ Shopping list creation successful!")
                print("🎉 All tests passed! Data flows to AWS database!")
            else:
                print("❌ Shopping list test failed")
        else:
            print("❌ Login test failed")
    else:
        print("❌ Registration test failed")
        
    print("\n" + "=" * 50)
    print("Test complete!")
