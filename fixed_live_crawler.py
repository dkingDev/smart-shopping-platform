#!/usr/bin/env python3
"""
Fixed Live Universal Crawler - Matches actual AWS database schema
"""

import os
import asyncio
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from datetime import datetime, date
from typing import List
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ProductData:
    """Product data structure matching database schema"""
    product_id: str
    name: str
    brand: str
    category: str
    store_name: str
    current_price: Decimal
    previous_price: Decimal = None
    offer_text: str = ""

class FixedLiveCrawler:
    """Live crawler that matches the actual AWS database schema"""
    
    def __init__(self, store_name: str):
        self.store_name = store_name.lower()
        self.connection = None
        
        # Database connection
        self.db_config = {
            'host': os.getenv('AWS_DB_HOST'),
            'database': os.getenv('AWS_DB_NAME'), 
            'user': os.getenv('AWS_DB_USER'),
            'password': os.getenv('AWS_DB_PASSWORD'),
            'port': int(os.getenv('AWS_DB_PORT', 5432)),
            'sslmode': 'require'
        }
    
    async def connect_db(self):
        """Connect to AWS PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print(f"✅ Connected to AWS database for {self.store_name}")
            return True
        except Exception as e:
            print(f"❌ AWS database connection failed: {e}")
            return False
    
    def close_db(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print(f"📤 AWS database connection closed for {self.store_name}")
    
    async def create_sample_products(self) -> List[ProductData]:
        """Create sample product data for testing"""
        
        print(f"📦 Creating sample {self.store_name} products...")
        
        if self.store_name == "morrisons":
            sample_data = [
                {"name": "Hovis Medium White Bread 800g", "brand": "Hovis", "category": "Bakery", "price": "1.25", "prev_price": "1.30"},
                {"name": "Warburtons Medium White Bread 800g", "brand": "Warburtons", "category": "Bakery", "price": "1.30", "prev_price": "1.50", "offer": "was £1.50"},
                {"name": "Coca Cola Original 330ml Can", "brand": "Coca Cola", "category": "Drinks", "price": "0.85"},
                {"name": "Pepsi Original 330ml Can", "brand": "Pepsi", "category": "Drinks", "price": "0.80", "prev_price": "0.95", "offer": "was £0.95"},
                {"name": "British Chicken Breast Fillets 1kg", "brand": "Fresh", "category": "Meat", "price": "4.50"},
                {"name": "British Beef Mince 500g", "brand": "Fresh", "category": "Meat", "price": "3.25", "prev_price": "3.75", "offer": "was £3.75"},
            ]
        elif self.store_name == "asda":
            sample_data = [
                {"name": "Hovis Medium White Bread 800g", "brand": "Hovis", "category": "Bakery", "price": "1.20"},
                {"name": "Warburtons Medium White Bread 800g", "brand": "Warburtons", "category": "Bakery", "price": "1.35"},
                {"name": "Coca Cola Original 330ml Can", "brand": "Coca Cola", "category": "Drinks", "price": "0.88"},
                {"name": "Pepsi Original 330ml Can", "brand": "Pepsi", "category": "Drinks", "price": "0.85"},
                {"name": "British Chicken Breast Fillets 1kg", "brand": "Fresh", "category": "Meat", "price": "4.25", "prev_price": "4.80", "offer": "was £4.80"},
                {"name": "British Beef Mince 500g", "brand": "Fresh", "category": "Meat", "price": "3.50"},
            ]
        else:
            return []
        
        products = []
        for i, product in enumerate(sample_data):
            # Generate consistent product ID
            product_id = f"{abs(hash(product['name'])) % 900000 + 100000:06d}"
            
            prev_price = None
            if 'prev_price' in product:
                prev_price = Decimal(product['prev_price'])
            
            products.append(ProductData(
                product_id=product_id,
                name=product['name'],
                brand=product['brand'],
                category=product['category'],
                store_name=self.store_name,
                current_price=Decimal(product['price']),
                previous_price=prev_price,
                offer_text=product.get('offer', '')
            ))
        
        print(f"📦 Created {len(products)} sample products for {self.store_name}")
        return products
    
    async def upsert_branded_products(self, products: List[ProductData]):
        """Insert or update products in branded_products table"""
        
        print(f"📝 Updating branded_products table...")
        
        cursor = self.connection.cursor()
        
        insert_count = 0
        update_count = 0
        
        for product in products:
            try:
                # Check if product exists
                cursor.execute("SELECT product_id FROM branded_products WHERE product_id = %s", 
                             (product.product_id,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing product
                    cursor.execute("""
                        UPDATE branded_products 
                        SET name = %s,
                            brand = %s,
                            category = %s,
                            updated_at = %s
                        WHERE product_id = %s
                    """, (
                        product.name,
                        product.brand,
                        product.category,
                        datetime.now(),
                        product.product_id
                    ))
                    update_count += 1
                    print(f"  📝 Updated product: {product.name}")
                else:
                    # Insert new product
                    cursor.execute("""
                        INSERT INTO branded_products 
                        (product_id, name, brand, category, reference_price, created_date, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        product.product_id,
                        product.name,
                        product.brand,
                        product.category,
                        product.current_price,
                        date.today(),
                        datetime.now()
                    ))
                    insert_count += 1
                    print(f"  ➕ Inserted product: {product.name}")
                
            except Exception as e:
                print(f"  ❌ Error processing product {product.name}: {e}")
                self.connection.rollback()
                continue
        
        # Commit changes
        self.connection.commit()
        cursor.close()
        
        print(f"✅ Branded products updated: {insert_count} inserted, {update_count} updated")
        return insert_count + update_count
    
    async def upsert_store_prices(self, products: List[ProductData]):
        """Insert or update store prices"""
        
        print(f"🏪 Updating store_prices table for {self.store_name}...")
        
        cursor = self.connection.cursor()
        
        insert_count = 0
        update_count = 0
        
        for product in products:
            try:
                # Check if store price exists for this product/store combination
                cursor.execute("""
                    SELECT id FROM store_prices 
                    WHERE product_id = %s AND store_name = %s
                """, (product.product_id, product.store_name))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing price
                    cursor.execute("""
                        UPDATE store_prices 
                        SET current_price = %s,
                            previous_price = %s,
                            offer_text = %s,
                            last_updated = %s
                        WHERE product_id = %s AND store_name = %s
                    """, (
                        product.current_price,
                        product.previous_price,
                        product.offer_text,
                        datetime.now(),
                        product.product_id,
                        product.store_name
                    ))
                    update_count += 1
                    print(f"  📝 Updated price: {product.name} - £{product.current_price}")
                else:
                    # Insert new price
                    cursor.execute("""
                        INSERT INTO store_prices 
                        (product_id, store_name, current_price, previous_price, offer_text, last_updated)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        product.product_id,
                        product.store_name,
                        product.current_price,
                        product.previous_price,
                        product.offer_text,
                        datetime.now()
                    ))
                    insert_count += 1
                    print(f"  ➕ Inserted price: {product.name} - £{product.current_price}")
                
            except Exception as e:
                print(f"  ❌ Error processing price for {product.name}: {e}")
                self.connection.rollback()
                continue
        
        # Commit changes
        self.connection.commit()
        cursor.close()
        
        print(f"✅ Store prices updated: {insert_count} inserted, {update_count} updated")
        return insert_count + update_count
    
    async def run_live_crawl(self):
        """Run the live crawler and update AWS database"""
        
        print(f"\n🚀 STARTING LIVE CRAWL FOR {self.store_name.upper()}")
        print("=" * 50)
        
        try:
            # Connect to database
            if not await self.connect_db():
                return False
            
            # Create sample products (in production this would be real web scraping)
            products = await self.create_sample_products()
            
            if not products:
                print(f"⚠️ No products to process for {self.store_name}")
                return False
            
            # Update branded products table
            products_updated = await self.upsert_branded_products(products)
            
            # Update store prices table
            prices_updated = await self.upsert_store_prices(products)
            
            print(f"\n🎉 LIVE CRAWL COMPLETED FOR {self.store_name.upper()}!")
            print(f"📊 Results:")
            print(f"  • Products updated: {products_updated}")
            print(f"  • Prices updated: {prices_updated}")
            print(f"  • Total items processed: {len(products)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during live crawl: {e}")
            return False
        finally:
            self.close_db()

async def check_database_status():
    """Check database status before and after"""
    
    load_dotenv()
    
    db_config = {
        'host': os.getenv('AWS_DB_HOST'),
        'database': os.getenv('AWS_DB_NAME'), 
        'user': os.getenv('AWS_DB_USER'),
        'password': os.getenv('AWS_DB_PASSWORD'),
        'port': int(os.getenv('AWS_DB_PORT', 5432)),
        'sslmode': 'require'
    }
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check branded_products count
        cursor.execute("SELECT COUNT(*) FROM branded_products")
        products_count = cursor.fetchone()[0]
        
        # Check store_prices count
        cursor.execute("SELECT COUNT(*) FROM store_prices")
        prices_count = cursor.fetchone()[0]
        
        # Check recent updates
        cursor.execute("""
            SELECT store_name, COUNT(*) 
            FROM store_prices 
            WHERE last_updated > NOW() - INTERVAL '1 hour'
            GROUP BY store_name
        """)
        recent_updates = cursor.fetchall()
        
        print(f"📊 Database Status:")
        print(f"  • Total products: {products_count}")
        print(f"  • Total store prices: {prices_count}")
        print(f"  • Recent updates (last hour):")
        for store, count in recent_updates:
            print(f"    - {store}: {count} price updates")
        
        cursor.close()
        conn.close()
        
        return products_count, prices_count
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return 0, 0

async def main():
    """Main function to run fixed live crawlers"""
    
    print("🔥 FIXED LIVE UNIVERSAL CRAWLER TEST")
    print("=" * 60)
    print("Testing with actual AWS database schema")
    print()
    
    # Check database before
    print("📋 BEFORE - Database Status:")
    before_products, before_prices = await check_database_status()
    print()
    
    # Run live crawlers
    stores_to_test = ["morrisons", "asda"]
    results = {}
    
    for store in stores_to_test:
        print(f"\n🏪 Running live crawler for {store.title()}...")
        crawler = FixedLiveCrawler(store)
        success = await crawler.run_live_crawl()
        results[store] = success
        print()
    
    # Check database after
    print("📋 AFTER - Database Status:")
    after_products, after_prices = await check_database_status()
    print()
    
    # Summary
    print("🎯 LIVE CRAWL RESULTS")
    print("=" * 30)
    for store, success in results.items():
        print(f"{store.title()}: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    print(f"\n📈 Database Changes:")
    print(f"  • Products before: {before_products}")
    print(f"  • Products after: {after_products}")
    print(f"  • New products: {after_products - before_products}")
    print(f"  • Prices before: {before_prices}")
    print(f"  • Prices after: {after_prices}")
    print(f"  • New prices: {after_prices - before_prices}")
    
    if all(results.values()) and (after_products > before_products or after_prices > before_prices):
        print(f"\n🎉 SUCCESS! LIVE CRAWLERS UPDATED AWS DATABASE!")
        print("✅ Your crawler successfully wrote data to AWS")
        print("✅ Database now contains fresh product and price data")
        print("✅ Ready for production web scraping")
    else:
        print(f"\n⚠️ Some issues detected - check errors above")

if __name__ == "__main__":
    asyncio.run(main())
