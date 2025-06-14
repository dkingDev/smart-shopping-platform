#!/usr/bin/env python3
"""Quick script to add missing branded_products table."""

import sys
sys.path.append('.')

from database.aws_postgresql_manager import AWSPostgreSQLManager

def main():
    print("Adding missing branded_products table...")
    
    try:
        # Initialize database manager
        db_manager = AWSPostgreSQLManager()
          # SQL to create the missing table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS store_prices (
            id SERIAL PRIMARY KEY,
            store_name VARCHAR(255) NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
                conn.commit()
                print("Table created successfully!")
                  # Insert a test record
                cur.execute("""
                    INSERT INTO store_prices (store_name, product_name, price)
                    VALUES ('Test Store', 'Test Product', 1.99)
                    ON CONFLICT DO NOTHING;
                """)
                conn.commit()
                print("Test data added!")
        
        print("Database update complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
