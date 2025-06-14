#!/usr/bin/env python3
"""Test login with derek.j.king@live.com"""

import requests

def test_derek_login():
    print("🧪 TESTING LOGIN FOR DEREK J KING")
    print("=" * 40)
    
    # Login data
    login_data = {
        "email": "derek.j.king@live.com",
        "password": "Alex8nd3r!"
    }
    
    try:
        print("📡 Attempting login...")
        response = requests.post("http://localhost:9999/auth/login", json=login_data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user_info = data.get('data', {}).get('user', {})
            token = data.get('data', {}).get('access_token', '')
            
            print("✅ LOGIN SUCCESSFUL!")
            print(f"📧 Email: {user_info.get('email')}")
            print(f"👤 Name: {user_info.get('full_name')}")
            print(f"🆔 User ID: {user_info.get('id')}")
            print(f"🎫 Token: {token[:30]}...")
            print(f"🌐 Frontend: http://localhost:9999")
            
            # Test token verification
            print("\n🔐 Testing token verification...")
            headers = {"Authorization": f"Bearer {token}"}
            verify_response = requests.get("http://localhost:9999/auth/verify-token", headers=headers)
            
            if verify_response.status_code == 200:
                print("✅ Token verification successful!")
                return True
            else:
                print(f"❌ Token verification failed: {verify_response.text}")
                return False
                
        else:
            print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_derek_login()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Derek can now login to the website")
        print("🚀 System ready for live use!")
    else:
        print("❌ Login test failed")
        print("🔧 Please check the credentials")
