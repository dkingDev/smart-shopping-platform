#!/usr/bin/env python3
"""
Check AWS database schema and fix crawler compatibility
"""

import psycopg2
from dotenv import load_dotenv
import os

def check_database_schema():
    """Check the actual database schema"""
    
    load_dotenv()
    
    print("🔍 CHECKING AWS DATABASE SCHEMA")
    print("=" * 40)
    
    try:
        db_config = {
            'host': os.getenv('AWS_DB_HOST'),
            'database': os.getenv('AWS_DB_NAME'), 
            'user': os.getenv('AWS_DB_USER'),
            'password': os.getenv('AWS_DB_PASSWORD'),
            'port': int(os.getenv('AWS_DB_PORT', 5432)),
            'sslmode': 'require'
        }
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check national_brands table structure
        print("\n📋 national_brands table structure:")
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'national_brands'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            length_info = f", max_length: {col[2]}" if col[2] else ""
            print(f"  • {col[0]} ({col[1]}{length_info}) - Nullable: {col[3]}")
        
        # Check if we have any existing store tables
        print(f"\n📋 Store tables:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%_national_prices';
        """)
        
        store_tables = cursor.fetchall()
        if store_tables:
            for table in store_tables:
                print(f"  • {table[0]}")
                
                # Check structure of first store table
                if table[0] == store_tables[0][0]:
                    print(f"    Structure of {table[0]}:")
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns 
                        WHERE table_name = '{table[0]}'
                        ORDER BY ordinal_position;
                    """)
                    
                    store_cols = cursor.fetchall()
                    for col in store_cols:
                        print(f"      - {col[0]} ({col[1]}) - Nullable: {col[2]}")
        else:
            print("  • No store tables found")
        
        # Check sample data
        print(f"\n📊 Sample data from national_brands:")
        cursor.execute("SELECT * FROM national_brands LIMIT 3;")
        sample_data = cursor.fetchall()
        
        if sample_data:
            # Get column names
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns 
                WHERE table_name = 'national_brands'
                ORDER BY ordinal_position;
            """)
            col_names = [row[0] for row in cursor.fetchall()]
            
            for i, row in enumerate(sample_data):
                print(f"  Row {i+1}:")
                for j, value in enumerate(row):
                    if j < len(col_names):
                        print(f"    {col_names[j]}: {value}")
                print()
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False

if __name__ == "__main__":
    check_database_schema()
