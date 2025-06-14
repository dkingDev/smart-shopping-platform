#!/usr/bin/env python3
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

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

print('Current store coverage:')
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND (table_name LIKE '%_prices' OR table_name LIKE '%_national_prices')
    ORDER BY table_name;
""")

store_tables = cursor.fetchall()
for table in store_tables:
    print(f'  • {table[0]}')
    cursor.execute(f'SELECT COUNT(*) FROM {table[0]};')
    count = cursor.fetchone()[0]
    print(f'    Products: {count:,}')

cursor.close()
conn.close()
