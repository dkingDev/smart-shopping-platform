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

print('All tables in database:')
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

for table in cursor.fetchall():
    print(f'  • {table[0]}')

cursor.close()
conn.close()
