#!/usr/bin/env python3
"""
Check actual database schema to fix crawler
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    print("🔍 Checking AWS database schema...")
    
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
    
    # Check national_brands structure
    print("\n📦 NATIONAL_BRANDS TABLE:")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'national_brands'
        ORDER BY ordinal_position;
    """)
    
    nb_columns = cursor.fetchall()
    for col in nb_columns:
        print(f"  • {col[0]} ({col[1]})")
    
    # Check morrisons table structure  
    print("\n🏪 MORRISONS_NATIONAL_PRICES TABLE:")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'morrisons_national_prices'
        ORDER BY ordinal_position;
    """)
    
    morr_columns = cursor.fetchall()
    for col in morr_columns:
        print(f"  • {col[0]} ({col[1]})")
    
    # Sample data from national_brands
    print(f"\n📊 SAMPLE DATA FROM NATIONAL_BRANDS:")
    cursor.execute("SELECT product_id, product_name FROM national_brands LIMIT 3;")
    samples = cursor.fetchall()
    for sample in samples:
        print(f"  • ID: {sample[0]}")
        print(f"    Name: {sample[1]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Schema check complete")
    
except Exception as e:
    print(f"❌ Error: {e}")
