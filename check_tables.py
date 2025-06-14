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

print('ASDA table structure:')
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'asda_national_prices'
    ORDER BY ordinal_position;
""")

for col in cursor.fetchall():
    print(f'  • {col[0]} ({col[1]})')

print('\nMorrisons table structure:')
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'morrisons_national_prices'
    ORDER BY ordinal_position;
""")

for col in cursor.fetchall():
    print(f'  • {col[0]} ({col[1]})')

cursor.close()
conn.close()
