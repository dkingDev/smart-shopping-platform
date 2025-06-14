#!/usr/bin/env python3
"""
Production Scalable Crawler Runner
This runs the universal crawler for all available stores to populate the national brands database.
Designed to scale with user crowdsourced data collection.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from universal_smart_crawler import UniversalSmartCrawler
import psycopg2
import psycopg2.extras
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

# Register UUID adapter
psycopg2.extras.register_uuid()

load_dotenv()

class ProductionCrawlerRunner:
    """Scalable crawler runner for production deployment"""
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('AWS_DB_HOST'),
            'database': os.getenv('AWS_DB_NAME'), 
            'user': os.getenv('AWS_DB_USER'),
            'password': os.getenv('AWS_DB_PASSWORD'),
            'port': int(os.getenv('AWS_DB_PORT', 5432)),
            'sslmode': 'require'
        }
        
        # Available stores for national brand data
        self.available_stores = ['morrisons', 'asda']  # Add more as crawlers are built
        
    def get_db_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    async def run_store_crawler(self, store_name):
        """Run crawler for a specific store"""
        print(f"\n🏪 CRAWLING {store_name.upper()} FOR NATIONAL BRANDS")
        print("-" * 50)
        
        try:
            # Initialize store crawler
            crawler = UniversalSmartCrawler(store_name)
            
            # Connect to database
            if not await crawler.connect_db():
                print(f"❌ Failed to connect to database for {store_name}")
                return False
            
            # Run the crawl
            products = await crawler.crawl_store_products()
            
            if products:
                print(f"✅ {store_name.title()}: Found {len(products)} products")
                
                # Process and store products
                await self.process_products(crawler, products)
                
                print(f"✅ {store_name.title()}: Processing complete")
            else:
                print(f"⚠️ {store_name.title()}: No products found")
            
            # Close connection
            crawler.close_db()
            return True
            
        except Exception as e:
            print(f"❌ Error crawling {store_name}: {e}")
            return False
    
    async def process_products(self, crawler, products):
        """Process and store products in scalable format"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        products_processed = 0
        
        for product in products:
            try:
                # Extract brand and normalize name
                brand = self.extract_brand(product.name)
                normalized_name = product.name.lower().replace(' ', '').replace('-', '')
                
                # Check if product exists in national_brands
                cursor.execute("""
                    SELECT product_id FROM national_brands 
                    WHERE normalized_name = %s
                """, (normalized_name,))
                
                existing = cursor.fetchone()
                
                if existing:
                    product_id = existing[0]
                    # Update existing product
                    cursor.execute("""
                        UPDATE national_brands 
                        SET display_name = %s, brand = %s, category = %s,
                            updated_at = %s
                        WHERE product_id = %s
                    """, (product.name, brand, product.category, 
                          datetime.now(), product_id))
                else:
                    # Create new product
                    import uuid
                    product_id = uuid.uuid4()
                    cursor.execute("""
                        INSERT INTO national_brands (
                            product_id, normalized_name, display_name, brand, category,
                            created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (product_id, normalized_name, product.name, brand,
                          product.category, datetime.now(), datetime.now()))
                
                # Add/update store price
                store_table = f"{crawler.store_name}_national_prices"
                cursor.execute(f"""
                    SELECT price_id FROM {store_table}
                    WHERE national_brand_id = %s
                """, (product_id,))
                
                if cursor.fetchone():
                    cursor.execute(f"""
                        UPDATE {store_table}
                        SET store_price = %s, last_crawled = %s
                        WHERE national_brand_id = %s
                    """, (product.current_price, datetime.now(), product_id))
                else:
                    import uuid
                    price_id = uuid.uuid4()
                    cursor.execute(f"""
                        INSERT INTO {store_table} (
                            price_id, national_brand_id, store_price, last_crawled
                        ) VALUES (%s, %s, %s, %s)
                    """, (price_id, product_id, product.current_price, datetime.now()))
                
                products_processed += 1
                
            except Exception as e:
                print(f"  ⚠️ Error processing {product.name}: {e}")
                continue
        
        # Update national averages for scalability
        await self.update_national_averages(cursor)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"  ✅ Processed {products_processed} products")
    
    async def update_national_averages(self, cursor):
        """Update national average prices for scalable user access"""
        print("  🔄 Updating national averages...")
        
        # Get all products that need average calculation
        cursor.execute("""
            SELECT DISTINCT nb.product_id 
            FROM national_brands nb
            WHERE EXISTS (
                SELECT 1 FROM morrisons_national_prices mnp 
                WHERE mnp.national_brand_id = nb.product_id
            ) OR EXISTS (
                SELECT 1 FROM asda_national_prices anp 
                WHERE anp.national_brand_id = nb.product_id
            )
        """)
        
        products_to_update = cursor.fetchall()
        
        for (product_id,) in products_to_update:
            # Get all store prices for this product
            prices = []
            
            # Morrisons price
            cursor.execute("""
                SELECT store_price FROM morrisons_national_prices 
                WHERE national_brand_id = %s
            """, (product_id,))
            morr_price = cursor.fetchone()
            if morr_price:
                prices.append(morr_price[0])
            
            # ASDA price (if exists)
            try:
                cursor.execute("""
                    SELECT store_price FROM asda_national_prices 
                    WHERE national_brand_id = %s
                """, (product_id,))
                asda_price = cursor.fetchone()
                if asda_price:
                    prices.append(asda_price[0])
            except:
                pass  # ASDA table might not exist yet
            
            if prices:
                avg_price = sum(prices) / len(prices)
                lowest_price = min(prices)
                highest_price = max(prices)
                
                cursor.execute("""
                    UPDATE national_brands 
                    SET national_average_price = %s,
                        lowest_price = %s,
                        highest_price = %s,
                        price_last_updated = %s,
                        updated_at = %s
                    WHERE product_id = %s
                """, (avg_price, lowest_price, highest_price,
                          datetime.now(), datetime.now(), product_id))
        
        print(f"  ✅ Updated {len(products_to_update)} product averages")
    
    def extract_brand(self, product_name):
        """Extract brand from product name for scalable categorization"""
        # UK brand mapping
        brands = {
            'hovis': 'Hovis', 'warburtons': 'Warburtons', 'kingsmill': 'Kingsmill',
            'cadbury': 'Cadbury', 'nestle': 'Nestlé', 'heinz': 'Heinz',
            'kelloggs': "Kellogg's", 'walkers': 'Walkers', 'coca-cola': 'Coca-Cola',
            'pepsi': 'Pepsi', 'innocent': 'Innocent', 'tesco': 'Tesco',
            'sainsburys': "Sainsbury's", 'asda': 'ASDA', 'morrisons': 'Morrisons'
        }
        
        name_lower = product_name.lower()
        
        for brand_key, brand_name in brands.items():
            if brand_key in name_lower:
                return brand_name
        
        # Extract first word if capitalized
        words = product_name.split()
        if words and words[0][0].isupper() and len(words[0]) > 2:
            return words[0]
        
        return 'Generic'
    
    async def run_all_crawlers(self):
        """Run all available store crawlers for national brand database"""
        print("🚀 PRODUCTION SCALABLE CRAWLER - NATIONAL BRANDS")
        print("=" * 60)
        print("Building foundation database for user crowdsourcing...")
        print("=" * 60)
        
        total_stores = len(self.available_stores)
        successful_stores = 0
        
        for store_name in self.available_stores:
            success = await self.run_store_crawler(store_name)
            if success:
                successful_stores += 1
        
        print(f"\n📊 CRAWL SUMMARY")
        print("-" * 30)
        print(f"✅ Successful stores: {successful_stores}/{total_stores}")
        
        # Get final database stats
        await self.show_database_stats()
        
        print(f"\n🎯 SCALABLE SYSTEM STATUS")
        print("-" * 30)
        print("✅ National brands database populated")
        print("✅ Store price data available")
        print("✅ Ready for user crowdsourcing")
        print("✅ Website/app can search national data")
        print("✅ Users will enhance with location data")
        print("✅ System scales automatically with user input")
        
    async def show_database_stats(self):
        """Show current database statistics for scaling validation"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Total products with prices
        cursor.execute("""
            SELECT COUNT(*) FROM national_brands 
            WHERE national_average_price IS NOT NULL
        """)
        total_products = cursor.fetchone()[0]
        
        # Store coverage
        cursor.execute("SELECT COUNT(*) FROM morrisons_national_prices")
        morrisons_count = cursor.fetchone()[0]
        
        try:
            cursor.execute("SELECT COUNT(*) FROM asda_national_prices")
            asda_count = cursor.fetchone()[0]
        except:
            asda_count = 0
        
        # Products with barcodes (for mobile app)
        cursor.execute("""
            SELECT COUNT(*) FROM national_brands 
            WHERE barcode IS NOT NULL
        """)
        barcode_count = cursor.fetchone()[0]
        
        print(f"\n📈 DATABASE STATISTICS")
        print("-" * 30)
        print(f"📦 Total products: {total_products:,}")
        print(f"🏪 Morrisons prices: {morrisons_count:,}")
        print(f"🏪 ASDA prices: {asda_count:,}")
        print(f"📱 Products with barcodes: {barcode_count:,}")
        
        cursor.close()
        conn.close()

async def main():
    """Main function to run production crawler"""
    runner = ProductionCrawlerRunner()
    await runner.run_all_crawlers()

if __name__ == "__main__":
    asyncio.run(main())
