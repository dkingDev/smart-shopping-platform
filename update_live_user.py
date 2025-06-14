#!/usr/bin/env python3
"""Update live user to derek.j.king@live.com"""

import sys
import os
sys.path.append('.')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env')

from database.aws_postgresql_manager import AWSPostgreSQLManager
from passlib.context import CryptContext

def main():
    print("🔄 UPDATING LIVE USER ACCOUNT")
    print("=" * 40)
    
    # New user details
    new_email = "derek.j.king@live.com"
    new_password = "Alex8nd3r!"
    new_name = "Derek J King"
    
    # Password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(new_password)
    
    try:
        db_manager = AWSPostgreSQLManager()
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check current users
                print("📋 Current users in database:")
                cur.execute("SELECT id, username, email, full_name, created_at FROM users ORDER BY created_at DESC")
                users = cur.fetchall()
                
                if users:
                    for user in users:
                        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}")
                    
                    # Update the existing user
                    user_id = users[0][0]  # Get the first user's ID
                    print(f"\n🔄 Updating user ID {user_id}...")
                    
                    cur.execute("""
                        UPDATE users 
                        SET username = %s, email = %s, password_hash = %s, full_name = %s
                        WHERE id = %s
                    """, (new_email, new_email, hashed_password, new_name, user_id))
                    
                    conn.commit()
                    print("✅ User updated successfully!")
                    
                else:
                    # Create new user if none exist
                    print("\n👤 Creating new user...")
                    cur.execute("""
                        INSERT INTO users (username, email, password_hash, full_name, is_active, created_at)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (new_email, new_email, hashed_password, new_name, True))
                    
                    conn.commit()
                    print("✅ User created successfully!")
                
                # Verify the update
                print("\n📋 Updated user details:")
                cur.execute("SELECT id, username, email, full_name, is_active, created_at FROM users WHERE email = %s", (new_email,))
                user = cur.fetchone()
                
                if user:
                    print(f"  ✅ ID: {user[0]}")
                    print(f"  ✅ Email: {user[1]}")
                    print(f"  ✅ Name: {user[3]}")
                    print(f"  ✅ Active: {user[4]}")
                    print(f"  ✅ Created: {user[5]}")
                    
                    print(f"\n🎯 LOGIN CREDENTIALS:")
                    print(f"  📧 Email: {new_email}")
                    print(f"  🔑 Password: {new_password}")
                    print(f"  🌐 URL: http://localhost:9999")
                else:
                    print("❌ Failed to verify user update")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
