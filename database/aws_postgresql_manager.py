#!/usr/bin/env python3
"""
AWS PostgreSQL Database Manager for National Branded Products System
Handles connection, data import, and maintenance tasks for AWS RDS PostgreSQL
"""

import os
import json
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor, execute_batch
from contextlib import contextmanager
import logging
from datetime import datetime
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSPostgreSQLManager:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize AWS PostgreSQL connection manager."""
        self.config = self.load_config(config_path)
        self.connection_params = self.get_connection_params()
        
    def load_config(self, config_path: Optional[str]) -> Dict:
        """Load database configuration."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration using environment variables
        return {
            "database": {
                "type": "aws_postgresql",
                "connection": {
                    "use_environment_variables": True,
                    "required_env_vars": [
                        "AWS_DB_HOST", "AWS_DB_PORT", "AWS_DB_NAME",
                        "AWS_DB_USER", "AWS_DB_PASSWORD"
                    ]
                },
                "performance": {
                    "batch_insert_size": 1000,
                    "connection_timeout": 30,
                    "query_timeout": 60
                }
            }
        }
    
    def get_connection_params(self) -> Dict:
        """Get database connection parameters from environment variables."""
        required_vars = self.config["database"]["connection"]["required_env_vars"]
        
        params = {}
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"Required environment variable {var} not set")
            
            # Map environment variable names to psycopg2 parameter names
            param_map = {
                "AWS_DB_HOST": "host",
                "AWS_DB_PORT": "port", 
                "AWS_DB_NAME": "database",
                "AWS_DB_USER": "user",
                "AWS_DB_PASSWORD": "password"
            }
            
            if var in param_map:
                params[param_map[var]] = value
        
        # Add SSL requirement for AWS RDS
        params["sslmode"] = "require"
        params["connect_timeout"] = self.config["database"]["performance"]["connection_timeout"]
        
        return params
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    logger.info(f"Successfully connected to PostgreSQL: {version}")
                    return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def setup_database(self, schema_file: str = "database/aws_postgresql_schema.sql"):
        """Create tables and indexes from schema file."""
        try:
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
                    conn.commit()
                    logger.info("Database schema setup completed")
                    
        except Exception as e:
            logger.error(f"Schema setup failed: {e}")
            raise
    
    def load_branded_products(self, csv_file: str = "database/imports/master_branded_products.csv"):
        """Load master branded products catalog."""
        try:
            df = pd.read_csv(csv_file)
            logger.info(f"Loading {len(df)} branded products...")
            
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Clear existing data
                    cur.execute("TRUNCATE TABLE branded_products CASCADE")
                    
                    # Prepare insert query
                    insert_query = """
                        INSERT INTO branded_products 
                        (product_id, name, original_name, brand, category, category_id, 
                         image_filename, reference_price, has_offer, created_date, data_source)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    # Convert DataFrame to list of tuples
                    records = df.to_records(index=False)
                    data = [tuple(record) for record in records]
                    
                    # Batch insert
                    batch_size = self.config["database"]["performance"]["batch_insert_size"]
                    execute_batch(cur, insert_query, data, page_size=batch_size)
                    
                    conn.commit()
                    logger.info(f"Successfully loaded {len(data)} branded products")
                    
        except Exception as e:
            logger.error(f"Failed to load branded products: {e}")
            raise
    
    def upsert_store_prices(self, store_name: str, prices_data: List[Dict]):
        """Insert or update store prices with conflict resolution."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    upsert_query = """
                        INSERT INTO store_prices 
                        (product_id, store_name, current_price, offer_text, availability)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (product_id, store_name) 
                        DO UPDATE SET
                            current_price = EXCLUDED.current_price,
                            offer_text = EXCLUDED.offer_text,
                            availability = EXCLUDED.availability,
                            last_updated = CURRENT_TIMESTAMP
                        WHERE store_prices.current_price != EXCLUDED.current_price
                    """
                    
                    # Prepare data for batch insert
                    data = [
                        (
                            item['product_id'],
                            store_name,
                            item['price'],
                            item.get('offer_text'),
                            item.get('availability', True)
                        )
                        for item in prices_data
                    ]
                    
                    execute_batch(cur, upsert_query, data, page_size=1000)
                    conn.commit()
                    
                    logger.info(f"Updated {len(data)} prices for {store_name}")
                    
        except Exception as e:
            logger.error(f"Failed to update store prices: {e}")
            raise
    
    def get_price_comparison(self, brand: Optional[str] = None, category: Optional[str] = None) -> List[Dict]:
        """Get price comparison data across stores."""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    query = """
                        SELECT * FROM store_price_comparison
                        WHERE 1=1
                    """
                    params = []
                    
                    if brand:
                        query += " AND brand ILIKE %s"
                        params.append(f"%{brand}%")
                    
                    if category:
                        query += " AND category ILIKE %s"
                        params.append(f"%{category}%")
                    
                    query += " ORDER BY min_price ASC"
                    
                    cur.execute(query, params)
                    return [dict(row) for row in cur.fetchall()]
                    
        except Exception as e:
            logger.error(f"Failed to get price comparison: {e}")
            raise
    
    def refresh_analytics(self):
        """Refresh materialized views and update statistics."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Refresh materialized view
                    cur.execute("SELECT refresh_price_comparison()")
                    
                    # Update category statistics
                    cur.execute("SELECT update_category_stats()")
                    
                    # Update brand statistics  
                    cur.execute("SELECT update_brand_stats()")
                    
                    conn.commit()
                    logger.info("Analytics refreshed successfully")
                    
        except Exception as e:
            logger.error(f"Failed to refresh analytics: {e}")
            raise
    
    def get_database_stats(self) -> Dict:
        """Get database usage statistics."""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Get table sizes
                    cur.execute("""
                        SELECT 
                            tablename,
                            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                            pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                        FROM pg_tables 
                        WHERE schemaname = 'public'
                        ORDER BY size_bytes DESC
                    """)
                    tables = [dict(row) for row in cur.fetchall()]
                    
                    # Get record counts
                    cur.execute("SELECT COUNT(*) as branded_products FROM branded_products")
                    branded_count = cur.fetchone()['branded_products']
                    
                    cur.execute("SELECT COUNT(*) as store_prices FROM store_prices")
                    prices_count = cur.fetchone()['store_prices']
                    
                    cur.execute("SELECT COUNT(DISTINCT store_name) as stores FROM store_prices")
                    stores_count = cur.fetchone()['stores']
                    
                    # Get user and shopping list stats
                    cur.execute("SELECT COUNT(*) as users FROM users WHERE is_active = true")
                    users_count = cur.fetchone()['users']
                    
                    cur.execute("SELECT COUNT(*) as shopping_lists FROM shopping_lists")
                    lists_count = cur.fetchone()['shopping_lists']
                    
                    cur.execute("SELECT COUNT(*) as shopping_list_items FROM shopping_list_items")
                    items_count = cur.fetchone()['shopping_list_items']
                    
                    cur.execute("SELECT COUNT(*) as crawler_priorities FROM user_crawler_priorities WHERE last_crawled IS NULL")
                    pending_priorities = cur.fetchone()['crawler_priorities']
                    
                    return {
                        "tables": tables,
                        "counts": {
                            "branded_products": branded_count,
                            "store_prices": prices_count,
                            "stores": stores_count,
                            "active_users": users_count,
                            "shopping_lists": lists_count,
                            "shopping_list_items": items_count,
                            "pending_crawler_priorities": pending_priorities
                        },
                        "last_updated": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            raise

    def create_user(self, username: str, email: str, password_hash: str, full_name: str = None) -> int:
        """Create a new user account."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (username, email, password_hash, full_name)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, (username, email, password_hash, full_name))
                    
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    
                    logger.info(f"Created user {username} with ID {user_id}")
                    return user_id
                    
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, username, email, password_hash, full_name, 
                               is_active, is_premium, subscription_type, created_at
                        FROM users 
                        WHERE username = %s AND is_active = true
                    """, (username,))
                    
                    result = cur.fetchone()
                    return dict(result) if result else None
                    
        except Exception as e:
            logger.error(f"Failed to get user by username: {e}")
            raise

    def create_shopping_list(self, user_id: int, name: str, description: str = None) -> int:
        """Create a new shopping list."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO shopping_lists (user_id, name, description)
                        VALUES (%s, %s, %s)
                        RETURNING id
                    """, (user_id, name, description))
                    
                    list_id = cur.fetchone()[0]
                    conn.commit()
                    
                    logger.info(f"Created shopping list '{name}' for user {user_id}")
                    return list_id
                    
        except Exception as e:
            logger.error(f"Failed to create shopping list: {e}")
            raise

    def add_to_shopping_list(self, list_id: int, product_name: str, product_id: str = None, 
                           quantity: int = 1, preferred_stores: List[str] = None) -> int:
        """Add item to shopping list."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO shopping_list_items 
                        (list_id, product_id, product_name, quantity, preferred_stores)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (list_id, product_id, product_name, quantity, preferred_stores))
                    
                    item_id = cur.fetchone()[0]
                    conn.commit()
                    
                    logger.info(f"Added '{product_name}' to shopping list {list_id}")
                    return item_id
                    
        except Exception as e:
            logger.error(f"Failed to add item to shopping list: {e}")
            raise

    def get_crawler_priorities(self, limit: int = 100) -> List[Dict]:
        """Get top crawler priorities for scheduling."""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT * FROM get_top_crawler_priorities(%s)", (limit,))
                    return [dict(row) for row in cur.fetchall()]
                    
        except Exception as e:
            logger.error(f"Failed to get crawler priorities: {e}")
            raise

    def mark_priority_crawled(self, product_search: str, store_name: str):
        """Mark a crawler priority as completed."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT mark_crawler_priority_completed(%s, %s)", 
                              (product_search, store_name))
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Failed to mark priority crawled: {e}")
            raise

def main():
    """Test AWS PostgreSQL connection and setup."""
    print("🔧 AWS PostgreSQL Setup for National Branded Products")
    print("=" * 60)
    
    # Initialize database manager
    db = AWSPostgreSQLManager()
    
    # Test connection
    print("🔗 Testing database connection...")
    if db.test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
        return
    
    # Setup database schema
    print("🏗️  Setting up database schema...")
    try:
        db.setup_database()
        print("✅ Database schema created")
    except Exception as e:
        print(f"❌ Schema setup failed: {e}")
        return
    
    # Load branded products if file exists
    products_file = "database/imports/master_branded_products.csv"
    if os.path.exists(products_file):
        print("📊 Loading branded products catalog...")
        try:
            db.load_branded_products(products_file)
            print("✅ Branded products loaded")
        except Exception as e:
            print(f"❌ Failed to load products: {e}")
    
    # Get database statistics
    print("📈 Database statistics:")
    try:
        stats = db.get_database_stats()
        print(f"   - Branded products: {stats['counts']['branded_products']:,}")
        print(f"   - Store prices: {stats['counts']['store_prices']:,}")
        print(f"   - Active stores: {stats['counts']['stores']}")
    except Exception as e:
        print(f"❌ Failed to get stats: {e}")
    
    print("\n🎯 AWS PostgreSQL setup complete!")
    print("💡 Ready for crawler integration")

if __name__ == "__main__":
    main()
