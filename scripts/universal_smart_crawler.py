#!/usr/bin/env python3
"""
Universal Smart Crawler for National Price System
=================================================
This crawler works for ANY store and implements the smart cross-reference logic:

1. Updates national_brands with latest prices (recalculates national averages)
2. Only stores store-specific prices when they DIFFER from national average
3. Automatically cleans up store tables when prices match national average
4. Prepares foundation for daily price comparison system

Architecture:
- national_brands = Master catalog with national average prices
- {store}_national_prices = Only prices that differ from national average
- Website/App shows national average unless store has different price
"""

import os
import json
import asyncio
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ProductPrice:
    """Product price data structure"""
    product_id: str
    name: str
    current_price: Decimal
    was_price: Optional[Decimal]
    price_per_unit: Optional[str]
    category: str
    subcategory: Optional[str]
    store_name: str
    
class UniversalSmartCrawler:
    """Smart crawler that works for any store with national average price logic"""
    
    def __init__(self, store_name: str):
        self.store_name = store_name.lower()
        self.store_table = f"{self.store_name}_national_prices"
        self.connection = None
        self.session = None
        
        # Database connection
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'), 
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', 5432)
        }
    
    async def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print(f"✅ Connected to database for {self.store_name}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def close_db(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print(f"📤 Database connection closed for {self.store_name}")
    
    async def get_current_national_averages(self) -> Dict[str, Decimal]:
        """Get current national average prices for all products"""
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT product_id, national_average_price 
            FROM national_brands 
            WHERE national_average_price IS NOT NULL
        """)
        
        national_prices = {}
        for row in cursor.fetchall():
            national_prices[row['product_id']] = row['national_average_price']
        
        cursor.close()
        print(f"📊 Loaded {len(national_prices)} national average prices")
        return national_prices
    
    async def crawl_store_products(self) -> List[ProductPrice]:
        """Crawl products from the specific store - Override this method for each store"""
        if self.store_name == "morrisons":
            return await self.crawl_morrisons()
        elif self.store_name == "tesco":
            return await self.crawl_tesco()
        elif self.store_name == "asda":
            return await self.crawl_asda()
        else:
            raise NotImplementedError(f"Crawler not implemented for {self.store_name}")
    
    async def crawl_morrisons(self) -> List[ProductPrice]:
        """Crawl Morrisons products - Uses existing Morrisons crawler logic"""
        print("🛒 Crawling Morrisons products...")
        
        # For now, load from existing JSON files
        # In production, this would be actual web crawling
        products = []
          # Load from existing JSON files in data directory
        data_dir = "crawlers/morrisons/crawler/data/branded"
        
        if os.path.exists(data_dir):
            for category_file in os.listdir(data_dir):
                if category_file.endswith('.json'):
                    file_path = os.path.join(data_dir, category_file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            category_data = json.load(f)
                              category_name = category_file.replace('.json', '').replace('_', ' ').title()
                        
                        for product in category_data:
                            if 'name' in product and 'price' in product:
                                try:
                                    # Extract price from string format like "£2.75"
                                    price_str = product['price'].replace('£', '').replace(',', '')
                                    current_price = Decimal(price_str)
                                    
                                    # Generate product ID from name (simplified for demo)
                                    product_id = f"morrisons_{hash(product['name']) % 1000000}"
                                    
                                    # Extract was_price from offer if it contains "was" (optional)
                                    was_price = None
                                    offer = product.get('offer', '')
                                    if 'was' in offer.lower():
                                        # Try to extract was price from offer text
                                        import re
                                        was_match = re.search(r'was\s*£?(\d+\.?\d*)', offer.lower())
                                        if was_match:
                                            was_price = Decimal(was_match.group(1))
                                    
                                    products.append(ProductPrice(
                                        product_id=product_id,
                                        name=product['name'],
                                        current_price=current_price,
                                        was_price=was_price,
                                        price_per_unit=None,  # Not available in this format
                                        category=category_name,
                                        subcategory=None,
                                        store_name='morrisons'
                                    ))
                                except (ValueError, TypeError) as e:
                                    print(f"⚠️ Price parsing error for {product.get('name', 'unknown')}: {e}")
                                    continue
                    except Exception as e:
                        print(f"⚠️ Error reading {category_file}: {e}")
                        continue
        
        print(f"🛒 Crawled {len(products)} Morrisons products")
        return products
    
    async def crawl_tesco(self) -> List[ProductPrice]:
        """Crawl Tesco products - Placeholder for future implementation"""
        print("🛒 Tesco crawler not yet implemented")
        return []
    
    async def crawl_asda(self) -> List[ProductPrice]:
        """Crawl ASDA products - Placeholder for future implementation"""
        print("🛒 ASDA crawler not yet implemented")
        return []
    
    def calculate_new_national_averages(self, all_store_data: Dict[str, List[ProductPrice]]) -> Dict[str, Dict]:
        """Calculate new national averages from all store data"""
        print("📊 Calculating new national averages...")
        
        product_aggregates = {}
        
        # Aggregate prices from all stores
        for store_name, products in all_store_data.items():
            for product in products:
                if product.product_id not in product_aggregates:
                    product_aggregates[product.product_id] = {
                        'name': product.name,
                        'category': product.category,
                        'subcategory': product.subcategory,
                        'prices': [],
                        'stores': []
                    }
                
                product_aggregates[product.product_id]['prices'].append(product.current_price)
                product_aggregates[product.product_id]['stores'].append(store_name)
        
        # Calculate averages, min, max
        national_averages = {}
        for product_id, data in product_aggregates.items():
            prices = data['prices']
            
            avg_price = Decimal(sum(prices)) / len(prices)
            avg_price = avg_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            national_averages[product_id] = {
                'name': data['name'],
                'category': data['category'],
                'subcategory': data['subcategory'],
                'national_average_price': avg_price,
                'lowest_price': min(prices),
                'highest_price': max(prices),
                'store_count': len(set(data['stores'])),
                'last_updated': datetime.now()
            }
        
        print(f"📊 Calculated averages for {len(national_averages)} products")
        return national_averages
    
    async def update_national_brands(self, national_averages: Dict[str, Dict]):
        """Update the national_brands table with new averages"""
        print("📝 Updating national_brands table...")
        
        cursor = self.connection.cursor()
        
        update_count = 0
        insert_count = 0
        
        for product_id, data in national_averages.items():
            # Check if product exists
            cursor.execute("SELECT product_id FROM national_brands WHERE product_id = %s", (product_id,))
            
            if cursor.fetchone():
                # Update existing
                cursor.execute("""
                    UPDATE national_brands 
                    SET national_average_price = %s,
                        lowest_price = %s,
                        highest_price = %s,
                        store_count = %s,
                        last_updated = %s
                    WHERE product_id = %s
                """, (
                    data['national_average_price'],
                    data['lowest_price'], 
                    data['highest_price'],
                    data['store_count'],
                    data['last_updated'],
                    product_id
                ))
                update_count += 1
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO national_brands 
                    (product_id, name, category, subcategory, national_average_price, 
                     lowest_price, highest_price, store_count, last_updated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    product_id,
                    data['name'],
                    data['category'],
                    data['subcategory'],
                    data['national_average_price'],
                    data['lowest_price'],
                    data['highest_price'],
                    data['store_count'],
                    data['last_updated']
                ))
                insert_count += 1
        
        self.connection.commit()
        cursor.close()
        
        print(f"✅ National brands updated: {update_count} updated, {insert_count} inserted")
    
    async def update_store_specific_prices(self, products: List[ProductPrice], national_averages: Dict[str, Dict]):
        """Update store-specific prices table (only differences from national average)"""
        print(f"📝 Updating {self.store_table} with price differences...")
        
        cursor = self.connection.cursor()
        
        # Clear existing data for this store
        cursor.execute(f"DELETE FROM {self.store_table}")
        
        different_prices = 0
        
        for product in products:
            if product.product_id in national_averages:
                national_price = national_averages[product.product_id]['national_average_price']
                
                # Only store if price is different from national average
                if product.current_price != national_price:
                    cursor.execute(f"""
                        INSERT INTO {self.store_table}
                        (product_id, name, current_price, was_price, price_per_unit, 
                         category, subcategory, last_updated)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        product.product_id,
                        product.name,
                        product.current_price,
                        product.was_price,
                        product.price_per_unit,
                        product.category,
                        product.subcategory,
                        datetime.now()
                    ))
                    different_prices += 1
        
        self.connection.commit()
        cursor.close()
        
        total_products = len(products)
        matching_national = total_products - different_prices
        
        print(f"✅ Store-specific prices updated:")
        print(f"   📊 Total products: {total_products}")
        print(f"   🎯 Matching national average: {matching_national}")
        print(f"   💰 Different prices stored: {different_prices}")
    
    async def create_daily_price_snapshot(self):
        """Create daily price snapshot for shopping list optimization"""
        print("📸 Creating daily price snapshot...")
        
        cursor = self.connection.cursor()
        
        # Create daily snapshot table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_price_snapshots (
                snapshot_date DATE,
                product_id VARCHAR(255),
                store_name VARCHAR(100),
                store_price DECIMAL(10,2),
                national_average_price DECIMAL(10,2),
                price_difference DECIMAL(10,2),
                is_cheapest BOOLEAN,
                PRIMARY KEY (snapshot_date, product_id, store_name)
            )
        """)
        
        # Insert today's snapshot
        today = date.today()
        
        cursor.execute(f"""
            INSERT INTO daily_price_snapshots 
            (snapshot_date, product_id, store_name, store_price, national_average_price, price_difference, is_cheapest)
            SELECT 
                %s as snapshot_date,
                nb.product_id,
                %s as store_name,
                COALESCE(sp.current_price, nb.national_average_price) as store_price,
                nb.national_average_price,
                COALESCE(sp.current_price, nb.national_average_price) - nb.national_average_price as price_difference,
                false as is_cheapest
            FROM national_brands nb
            LEFT JOIN {self.store_table} sp ON nb.product_id = sp.product_id
            WHERE nb.national_average_price IS NOT NULL
            ON CONFLICT (snapshot_date, product_id, store_name) 
            DO UPDATE SET 
                store_price = EXCLUDED.store_price,
                national_average_price = EXCLUDED.national_average_price,
                price_difference = EXCLUDED.price_difference
        """, (today, self.store_name))
        
        self.connection.commit()
        cursor.close()
        
        print(f"✅ Daily price snapshot created for {today}")
    
    async def run_smart_crawl(self):
        """Run the complete smart crawling process"""
        print(f"🚀 Starting smart crawl for {self.store_name.title()}")
        print("=" * 50)
        
        if not await self.connect_db():
            return False
        
        try:
            # 1. Crawl current store products
            products = await self.crawl_store_products()
            if not products:
                print(f"⚠️ No products found for {self.store_name}")
                return False
            
            # 2. For single store setup, use current store as national baseline
            # In multi-store setup, this would aggregate all stores
            all_store_data = {self.store_name: products}
            
            # 3. Calculate new national averages
            national_averages = self.calculate_new_national_averages(all_store_data)
            
            # 4. Update national_brands table
            await self.update_national_brands(national_averages)
            
            # 5. Update store-specific prices (only differences)
            await self.update_store_specific_prices(products, national_averages)
            
            # 6. Create daily price snapshot
            await self.create_daily_price_snapshot()
            
            print("=" * 50)
            print(f"🎉 Smart crawl completed successfully for {self.store_name.title()}!")
            print(f"📊 System ready for website/app with optimized price delivery")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during smart crawl: {e}")
            return False
        finally:
            self.close_db()

async def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python universal_smart_crawler.py <store_name>")
        print("Available stores: morrisons, tesco, asda")
        return
    
    store_name = sys.argv[1].lower()
    
    crawler = UniversalSmartCrawler(store_name)
    success = await crawler.run_smart_crawl()
    
    if success:
        print(f"\n✅ {store_name.title()} smart crawl completed!")
        print("🌐 Website/app will now show:")
        print("   • National average prices as default")
        print("   • Store-specific prices only when different")
        print("   • Optimal storage and performance")
    else:
        print(f"\n❌ {store_name.title()} smart crawl failed!")

if __name__ == "__main__":
    asyncio.run(main())
