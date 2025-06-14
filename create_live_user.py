#!/usr/bin/env python3
"""Create a live user account for the website"""

import sys
import requests
import getpass
from email.utils import parseaddr

def is_valid_email(email):
    """Validate email format"""
    parsed = parseaddr(email)
    return '@' in parsed[1] and '.' in parsed[1].split('@')[1]

def create_live_user():
    print("🚀 SMART SHOPPING PLATFORM - CREATE LIVE USER")
    print("=" * 50)
    
    base_url = "http://localhost:9999"  # Change to your production URL
    
    print("Please enter details for the new user:")
    
    # Get user details
    full_name = input("Full Name: ").strip()
    while not full_name:
        full_name = input("Full Name (required): ").strip()
    
    email = input("Email: ").strip().lower()
    while not is_valid_email(email):
        email = input("Valid Email (required): ").strip().lower()
    
    password = getpass.getpass("Password (8+ chars): ")
    while len(password) < 8:
        print("Password must be at least 8 characters")
        password = getpass.getpass("Password (8+ chars): ")
    
    location = input("Location (optional): ").strip()
    
    # Create user
    user_data = {
        "full_name": full_name,
        "email": email,
        "password": password
    }
    
    if location:
        user_data["location"] = location
    
    try:
        print(f"\n📡 Creating user account...")
        response = requests.post(f"{base_url}/auth/register", json=user_data)
        
        if response.status_code in [200, 201]:
            print("✅ User created successfully!")
            data = response.json()
            user_info = data.get('data', {}).get('user', {})
            
            print(f"📧 Email: {user_info.get('email')}")
            print(f"👤 Name: {user_info.get('full_name')}")
            print(f"🆔 User ID: {user_info.get('id')}")
            print(f"🔗 Login at: {base_url}")
            
            return True
            
        elif response.status_code == 400:
            print("❌ User already exists with this email")
            return False
            
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        print("💡 Make sure the backend server is running")
        return False

if __name__ == "__main__":
    success = create_live_user()
    
    if success:
        print("\n🎉 User account ready!")
        print("🌐 They can now login at your website")
    else:
        print("\n🔧 Please try again or check system status")
