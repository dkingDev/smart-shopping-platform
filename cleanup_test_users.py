#!/usr/bin/env python3
"""Clean up test users from AWS database"""

import sys
import os
sys.path.append('.')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env')

from database.aws_postgresql_manager import AWSPostgreSQLManager

def main():
    print("🧹 CLEANING UP TEST USERS FROM AWS DATABASE")
    print("=" * 50)
    
    try:
        db_manager = AWSPostgreSQLManager()
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # First, show current users
                print("📋 Current users in database:")
                cur.execute("SELECT id, username, email, full_name, created_at FROM users ORDER BY created_at DESC")
                users = cur.fetchall()
                
                if not users:
                    print("  No users found in database")
                    return
                
                for user in users:
                    print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}, Created: {user[4]}")
                
                print("\n🗑️ Identifying test users...")
                
                # Delete test users (emails containing 'test' or 'example.com')
                cur.execute("""
                    DELETE FROM users 
                    WHERE email LIKE '%test%' 
                    OR email LIKE '%example.com%'
                    OR username LIKE '%test%'
                    OR full_name LIKE '%Test%'
                """)
                deleted_users = cur.rowcount
                
                # Also clean up any test shopping lists and activity logs
                cur.execute("DELETE FROM shopping_list_items WHERE list_id IN (SELECT id FROM shopping_lists WHERE user_id NOT IN (SELECT id FROM users))")
                deleted_items = cur.rowcount
                
                cur.execute("DELETE FROM shopping_lists WHERE user_id NOT IN (SELECT id FROM users)")
                deleted_lists = cur.rowcount
                
                cur.execute("DELETE FROM user_activity_logs WHERE user_id NOT IN (SELECT id FROM users)")
                deleted_logs = cur.rowcount
                
                conn.commit()
                
                print(f"✅ Cleanup complete:")
                print(f"  🗑️ Deleted {deleted_users} test users")
                print(f"  🗑️ Deleted {deleted_lists} orphaned shopping lists")
                print(f"  🗑️ Deleted {deleted_items} orphaned list items")
                print(f"  🗑️ Deleted {deleted_logs} orphaned activity logs")
                
                # Show remaining users
                print("\n📋 Remaining users in database:")
                cur.execute("SELECT id, username, email, full_name, created_at FROM users ORDER BY created_at DESC")
                remaining_users = cur.fetchall()
                
                if remaining_users:
                    for user in remaining_users:
                        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}, Created: {user[4]}")
                else:
                    print("  ✅ Database is clean - no users remaining")
                
                print("\n🎯 Database is ready for live users!")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
