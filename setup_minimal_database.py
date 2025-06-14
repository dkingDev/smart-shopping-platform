#!/usr/bin/env python3
"""Setup minimal AWS PostgreSQL database schema for user authentication"""

import os
from dotenv import load_dotenv
from database.aws_postgresql_manager import AWSPostgreSQLManager

# Load environment variables
load_dotenv()

def setup_minimal_database():
    """Setup minimal AWS PostgreSQL database schema"""
    print("🔧 Setting up minimal AWS PostgreSQL database schema...")
    
    try:
        # Initialize database manager
        db_manager = AWSPostgreSQLManager()
        print("✅ Connected to AWS PostgreSQL")
        
        # Read minimal schema file
        schema_file = "database/minimal_schema.sql"
        if not os.path.exists(schema_file):
            print(f"❌ Schema file not found: {schema_file}")
            return False
            
        print(f"📖 Reading schema from {schema_file}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Execute schema
        print("🏗️ Creating database schema...")
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Execute the entire schema
                cur.execute(schema_sql)
                conn.commit()
                print("✅ Database schema created successfully!")
                
                # Verify tables were created
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('users', 'shopping_lists', 'shopping_list_items', 'user_activity_logs')
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                
                print(f"\n📊 Created {len(tables)} tables:")
                for table in tables:
                    print(f"  ✅ {table[0]}")
                    
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 AWS PostgreSQL Minimal Database Setup")
    print("=" * 50)
    
    success = setup_minimal_database()
    
    if success:
        print("\n🎉 Database setup complete!")
        print("🚀 Ready for user registration and data storage!")
    else:
        print("\n❌ Database setup failed!")
        
    print("=" * 50)
