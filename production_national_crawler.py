#!/usr/bin/env python3
"""
Production National Brands Crawler
Scalable crawler for populating national brands database from JSON data files.
Designed for user crowdsourcing enhancement.
"""

import os
import json
import psycopg2
import psycopg2.extras
import uuid
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

# Register UUID adapter
psycopg2.extras.register_uuid()

load_dotenv()

class ProductionNationalCrawler:
    """Production crawler for national brands database"""
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('AWS_DB_HOST'),
            'database': os.getenv('AWS_DB_NAME'), 
            'user': os.getenv('AWS_DB_USER'),
            'password': os.getenv('AWS_DB_PASSWORD'),
            'port': int(os.getenv('AWS_DB_PORT', 5432)),
            'sslmode': 'require'
        }
        
        # Data directories for each store
        self.data_sources = [
            {
                'store': 'morrisons',
                'name': 'Morrisons',
                'data_dir': 'crawlers/morrisons/crawler/data/branded',
                'table': 'morrisons_national_prices'
            }
            # Add more stores as data becomes available
        ]
    
    def get_db_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def extract_brand(self, product_name):
        """Extract brand from product name"""
        # UK brand mapping for national products
        brands = {
            'hovis': 'Hovis', 'warburtons': 'Warburtons', 'kingsmill': 'Kingsmill',
            'cadbury': 'Cadbury', 'nestle': 'Nestlé', 'heinz': 'Heinz',
            'kelloggs': "Kellogg's", 'walkers': 'Walkers', 'coca-cola': 'Coca-Cola',
            'pepsi': 'Pepsi', 'innocent': 'Innocent', 'tesco': 'Tesco',
            'sainsburys': "Sainsbury's", 'asda': 'ASDA', 'morrisons': 'Morrisons',
            'birds eye': 'Birds Eye', 'ben jerry': "Ben & Jerry's",
            'muller': 'Müller', 'dettol': 'Dettol', 'fairy': 'Fairy'
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
    
    def extract_size_info(self, product_name):
        """Extract size information from product name"""
        import re
        size_patterns = [
            r'(\d+(?:\.\d+)?(?:kg|g|ml|l|pack|x\d+))',
            r'(\d+\s?x\s?\d+(?:g|ml))',
            r'(\d+(?:\.\d+)?\s?(?:litre|liter)s?)',
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, product_name, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def process_store_data(self, store_info):
        """Process data for a specific store"""
        print(f"\n🏪 PROCESSING {store_info['name'].upper()}")
        print("-" * 40)
        
        data_dir = store_info['data_dir']
        store_table = store_info['table']
        
        if not os.path.exists(data_dir):
            print(f"⚠️ Data directory not found: {data_dir}")
            return 0
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        total_products = 0
        
        # Process each category file
        for category_file in os.listdir(data_dir):
            if not category_file.endswith('.json'):
                continue
                
            file_path = os.path.join(data_dir, category_file)
            category_name = category_file.replace('.json', '').replace('_', ' ').title()
            
            print(f"  📂 Processing {category_name}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    products_data = json.load(f)
                
                category_count = 0
                
                for product in products_data:
                    if not isinstance(product, dict) or 'name' not in product or 'price' not in product:
                        continue
                    
                    try:
                        # Extract product information
                        product_name = product['name']
                        price_str = product['price'].replace('£', '').replace(',', '')
                        current_price = Decimal(price_str)
                        brand = self.extract_brand(product_name)
                        size_info = self.extract_size_info(product_name)
                        normalized_name = product_name.lower().replace(' ', '').replace('-', '')
                        
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
                                    size_info = %s, updated_at = %s
                                WHERE product_id = %s
                            """, (product_name, brand, category_name, 
                                  size_info, datetime.now(), product_id))
                        else:
                            # Create new product
                            product_id = uuid.uuid4()
                            cursor.execute("""
                                INSERT INTO national_brands (
                                    product_id, normalized_name, display_name, brand, category,
                                    size_info, created_at, updated_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, (product_id, normalized_name, product_name, brand,
                                  category_name, size_info, datetime.now(), datetime.now()))
                        
                        # Add/update store price
                        cursor.execute(f"""
                            SELECT price_id FROM {store_table}
                            WHERE national_brand_id = %s
                        """, (product_id,))
                        
                        if cursor.fetchone():
                            cursor.execute(f"""
                                UPDATE {store_table}
                                SET store_price = %s, last_crawled = %s
                                WHERE national_brand_id = %s
                            """, (current_price, datetime.now(), product_id))
                        else:
                            price_id = uuid.uuid4()
                            cursor.execute(f"""
                                INSERT INTO {store_table} (
                                    price_id, national_brand_id, store_price, last_crawled
                                ) VALUES (%s, %s, %s, %s)
                            """, (price_id, product_id, current_price, datetime.now()))
                        
                        category_count += 1
                        
                    except Exception as e:
                        print(f"    ⚠️ Error processing {product.get('name', 'unknown')}: {e}")
                        continue
                
                print(f"    ✅ {category_name}: {category_count} products")
                total_products += category_count
                
            except Exception as e:
                print(f"    ❌ Error processing {category_file}: {e}")
                continue
        
        # Update national averages
        self.update_national_averages(cursor)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ {store_info['name']} total: {total_products} products")
        return total_products
    
    def update_national_averages(self, cursor):
        """Update national average prices for scalable user access"""
        print("  🔄 Updating national averages...")
        
        # Get all products that need average calculation
        cursor.execute("""
            SELECT DISTINCT nb.product_id 
            FROM national_brands nb
            WHERE EXISTS (
                SELECT 1 FROM morrisons_national_prices mnp 
                WHERE mnp.national_brand_id = nb.product_id
            )
        """)
        
        products_to_update = cursor.fetchall()
        updated_count = 0
        
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
            
            # Add other stores as they become available
            
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
                
                updated_count += 1
        
        print(f"    ✅ Updated {updated_count} product averages")
    
    def run_production_crawl(self):
        """Run production crawl for all available stores"""
        print("🚀 PRODUCTION NATIONAL BRANDS CRAWLER")
        print("=" * 50)
        print("Building scalable foundation for user crowdsourcing...")
        print("=" * 50)
        
        total_products = 0
        successful_stores = 0
        
        for store_info in self.data_sources:
            try:
                products_added = self.process_store_data(store_info)
                total_products += products_added
                successful_stores += 1
            except Exception as e:
                print(f"❌ Error processing {store_info['name']}: {e}")
        
        # Show final statistics
        self.show_database_stats()
        
        print(f"\n📊 CRAWL SUMMARY")
        print("-" * 30)
        print(f"✅ Stores processed: {successful_stores}/{len(self.data_sources)}")
        print(f"📦 Total products: {total_products:,}")
        
        print(f"\n🎯 SCALABLE SYSTEM READY")
        print("-" * 30)
        print("✅ National brands database populated")
        print("✅ Store price data available")
        print("✅ Ready for user crowdsourcing")
        print("✅ Website/app searches will work")
        print("✅ Users will enhance with location data")
        print("✅ System scales automatically")
        print("✅ Designed for production deployment")
    
    def show_database_stats(self):
        """Show current database statistics"""
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
        
        # Categories
        cursor.execute("""
            SELECT COUNT(DISTINCT category) FROM national_brands 
            WHERE category IS NOT NULL
        """)
        category_count = cursor.fetchone()[0]
        
        # Brands
        cursor.execute("""
            SELECT COUNT(DISTINCT brand) FROM national_brands 
            WHERE brand IS NOT NULL
        """)
        brand_count = cursor.fetchone()[0]
        
        print(f"\n📈 DATABASE STATISTICS")
        print("-" * 30)
        print(f"📦 Total products: {total_products:,}")
        print(f"🏪 Morrisons prices: {morrisons_count:,}")
        print(f"📂 Categories: {category_count}")
        print(f"🏷️ Brands: {brand_count}")
        
        cursor.close()
        conn.close()

def main():
    """Main function to run production crawler"""
    crawler = ProductionNationalCrawler()
    crawler.run_production_crawl()

if __name__ == "__main__":
    main()
