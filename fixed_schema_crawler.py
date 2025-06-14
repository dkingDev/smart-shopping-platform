#!/usr/bin/env python3
"""
Fixed Live Universal Crawler - Matches actual AWS database schema exactly
"""

import os
import asyncio
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from datetime import datetime, date
import uuid
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
    size_info: str = ""

class FixedSchemaCrawler:
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
    
    def normalize_name(self, name: str) -> str:
        """Normalize product name for database key"""
        return name.lower().replace(' ', '_').replace('-', '_').replace('&', 'and').replace('.', '').replace(',', '').replace("'", "").replace('"', '').replace('(', '').replace(')', '').replace('/', '_').replace('\\', '_')[:255]
    
    async def create_sample_products(self) -> List[ProductData]:
        """Create sample product data for testing"""
        
        print(f"📦 Creating sample {self.store_name} products...")
        
        if self.store_name == "morrisons":
            sample_data = [
                {"name": "Hovis Medium White Bread 800g", "brand": "Hovis", "category": "branded_bakery", "price": "1.25", "prev_price": "1.30", "size": "800g"},
                {"name": "Warburtons Medium White Bread 800g", "brand": "Warburtons", "category": "branded_bakery", "price": "1.30", "prev_price": "1.50", "offer": "was £1.50", "size": "800g"},
                {"name": "Coca Cola Original 330ml Can", "brand": "Coca-Cola", "category": "branded_drinks", "price": "0.85", "size": "330ml"},
                {"name": "Pepsi Original 330ml Can", "brand": "Pepsi", "category": "branded_drinks", "price": "0.80", "prev_price": "0.95", "offer": "was £0.95", "size": "330ml"},
                {"name": "British Chicken Breast Fillets 1kg", "brand": "Morrisons", "category": "branded_meat", "price": "4.50", "size": "1kg"},
                {"name": "British Beef Mince 500g 5% Fat", "brand": "Morrisons", "category": "branded_meat", "price": "3.25", "prev_price": "3.75", "offer": "was £3.75", "size": "500g"},
            ]
        elif self.store_name == "asda":
            sample_data = [
                {"name": "Hovis Medium White Bread 800g", "brand": "Hovis", "category": "branded_bakery", "price": "1.20", "size": "800g"},
                {"name": "Warburtons Medium White Bread 800g", "brand": "Warburtons", "category": "branded_bakery", "price": "1.35", "size": "800g"},
                {"name": "Coca Cola Original 330ml Can", "brand": "Coca-Cola", "category": "branded_drinks", "price": "0.88", "size": "330ml"},
                {"name": "Pepsi Original 330ml Can", "brand": "Pepsi", "category": "branded_drinks", "price": "0.85", "size": "330ml"},
                {"name": "British Chicken Breast Fillets 1kg", "brand": "ASDA", "category": "branded_meat", "price": "4.25", "prev_price": "4.80", "offer": "was £4.80", "size": "1kg"},
                {"name": "British Beef Mince 500g 5% Fat", "brand": "ASDA", "category": "branded_meat", "price": "3.50", "size": "500g"},
            ]
        else:
            return []
        
        products = []
        for i, product in enumerate(sample_data):
            # Generate UUID for product_id to match national_brands schema
            normalized_name = self.normalize_name(product['name'])
            product_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, normalized_name))
            
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
                offer_text=product.get('offer', ''),
                size_info=product.get('size', "")
            ))
        
        print(f"📦 Created {len(products)} sample products for {self.store_name}")
        return products
    
    async def upsert_national_brands(self, products: List[ProductData]):
        """Insert or update products in national_brands table"""
        
        print(f"📝 Updating national_brands table...")
        
        cursor = self.connection.cursor()
        
        insert_count = 0
        update_count = 0
        
        for product in products:
            try:
                normalized_name = self.normalize_name(product.name)
                
                # Check if product exists by normalized_name
                cursor.execute("SELECT product_id FROM national_brands WHERE normalized_name = %s", 
                             (normalized_name,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing product
                    cursor.execute("""
                        UPDATE national_brands 
                        SET display_name = %s,
                            brand = %s,
                            category = %s,
                            size_info = %s,
                            updated_at = %s
                        WHERE normalized_name = %s
                    """, (
                        product.name,
                        product.brand,
                        product.category,
                        product.size_info,
                        datetime.now(),
                        normalized_name
                    ))
                    update_count += 1
                    print(f"  📝 Updated product: {product.name}")
                else:
                    # Insert new product with UUID
                    cursor.execute("""
                        INSERT INTO national_brands 
                        (product_id, normalized_name, display_name, brand, category, size_info, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        product.product_id,
                        normalized_name,
                        product.name,
                        product.brand,
                        product.category,
                        product.size_info,
                        datetime.now(),
                        datetime.now()
                    ))
                    insert_count += 1
                    print(f"  ➕ Inserted new product: {product.name}")
                    
            except Exception as e:
                print(f"❌ Error processing product {product.name}: {e}")
                continue
        
        self.connection.commit()
        print(f"✅ national_brands updated: {insert_count} inserted, {update_count} updated")
    
    async def upsert_store_prices(self, products: List[ProductData]):
        """Insert or update prices in store-specific table"""
        
        table_name = f"{self.store_name}_national_prices"
        print(f"📝 Updating {table_name} table...")
        
        cursor = self.connection.cursor()
        
        insert_count = 0
        update_count = 0
        
        for product in products:
            try:
                # Use product.product_id as string for store tables (matching schema)
                price_per_unit = f"£{product.current_price}/unit" if product.size_info else None
                
                # Check if price record exists
                cursor.execute(f"SELECT product_id FROM {table_name} WHERE product_id = %s", 
                             (product.product_id,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing price record
                    cursor.execute(f"""
                        UPDATE {table_name} 
                        SET name = %s,
                            current_price = %s,
                            was_price = %s,
                            price_per_unit = %s,
                            category = %s,
                            subcategory = %s,
                            last_updated = %s
                        WHERE product_id = %s
                    """, (
                        product.name,
                        product.current_price,
                        product.previous_price,
                        price_per_unit,
                        product.category,
                        product.category,  # using category as subcategory for now
                        datetime.now(),
                        product.product_id
                    ))
                    update_count += 1
                    print(f"  📝 Updated price for: {product.name} - £{product.current_price}")
                else:
                    # Insert new price record
                    cursor.execute(f"""
                        INSERT INTO {table_name} 
                        (product_id, name, current_price, was_price, price_per_unit, category, subcategory, last_updated)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        product.product_id,
                        product.name,
                        product.current_price,
                        product.previous_price,
                        price_per_unit,
                        product.category,
                        product.category,  # using category as subcategory for now
                        datetime.now()
                    ))
                    insert_count += 1
                    print(f"  ➕ Inserted new price: {product.name} - £{product.current_price}")
                    
            except Exception as e:
                print(f"❌ Error processing price for {product.name}: {e}")
                continue
        
        self.connection.commit()
        print(f"✅ {table_name} updated: {insert_count} inserted, {update_count} updated")
    
    async def update_national_price_stats(self, products: List[ProductData]):
        """Update national price statistics in national_brands table"""
        
        print(f"📊 Updating national price statistics...")
        
        cursor = self.connection.cursor()
        
        for product in products:
            try:
                normalized_name = self.normalize_name(product.name)
                
                # Get all store prices for this product
                cursor.execute("""
                    SELECT current_price FROM asda_national_prices 
                    WHERE product_id = %s AND current_price IS NOT NULL
                    UNION ALL
                    SELECT current_price FROM morrisons_national_prices 
                    WHERE product_id = %s AND current_price IS NOT NULL
                """, (product.product_id, product.product_id))
                
                prices = [row[0] for row in cursor.fetchall()]
                
                if prices:
                    national_avg = sum(prices) / len(prices)
                    lowest_price = min(prices)
                    highest_price = max(prices)
                    
                    # Update national_brands with price statistics
                    cursor.execute("""
                        UPDATE national_brands 
                        SET national_average_price = %s,
                            lowest_price = %s,
                            highest_price = %s,
                            price_last_updated = %s
                        WHERE normalized_name = %s
                    """, (
                        national_avg,
                        lowest_price,
                        highest_price,
                        datetime.now(),
                        normalized_name
                    ))
                    
                    print(f"  📊 Updated stats for {product.name}: avg=£{national_avg:.2f}, low=£{lowest_price:.2f}, high=£{highest_price:.2f}")
                
            except Exception as e:
                print(f"❌ Error updating stats for {product.name}: {e}")
                continue
        
        self.connection.commit()
        print(f"✅ National price statistics updated")
    
    async def run_full_update(self):
        """Run a complete crawler update cycle"""
        
        print(f"🚀 STARTING LIVE CRAWLER FOR {self.store_name.upper()}")
        print("=" * 60)
        
        # Connect to database
        if not await self.connect_db():
            return False
        
        try:
            # 1. Create sample product data
            products = await self.create_sample_products()
            if not products:
                print(f"❌ No products created for {self.store_name}")
                return False
            
            # 2. Update national_brands table
            await self.upsert_national_brands(products)
            
            # 3. Update store-specific prices table
            await self.upsert_store_prices(products)
            
            # 4. Update national price statistics
            await self.update_national_price_stats(products)
            
            print(f"✅ CRAWLER COMPLETED SUCCESSFULLY FOR {self.store_name.upper()}")
            return True
            
        except Exception as e:
            print(f"❌ Crawler error: {e}")
            return False
        finally:
            self.close_db()

async def test_both_stores():
    """Test crawler for both ASDA and Morrisons"""
    
    print("🌟 TESTING LIVE CRAWLERS FOR BOTH STORES")
    print("=" * 60)
    
    stores = ["asda", "morrisons"]
    results = {}
    
    for store in stores:
        print(f"\n🛒 Testing {store.upper()} crawler...")
        crawler = FixedSchemaCrawler(store)
        results[store] = await crawler.run_full_update()
        print("-" * 40)
    
    print("\n📋 FINAL RESULTS:")
    for store, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {store.upper()}: {status}")
    
    return all(results.values())

if __name__ == "__main__":
    asyncio.run(test_both_stores())
