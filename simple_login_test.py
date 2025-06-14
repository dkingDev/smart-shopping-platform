#!/usr/bin/env python3
"""Simple live login test"""

import requests
import json

def test_login():
    print("🧪 Testing Live Login System")
    
    # Login data
    login_data = {
        "email": "live.user@realsite.com",
        "password": "SecureLivePass123!"
    }
    
    try:
        response = requests.post("http://localhost:9999/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token received: {data.get('data', {}).get('access_token', 'N/A')[:30]}...")
            return True
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_login()
