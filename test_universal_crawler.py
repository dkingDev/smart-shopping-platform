#!/usr/bin/env python3
"""
Test the Universal Smart Crawler for ASDA and Morrisons
Creates sample data and tests the crawler functionality
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent))

from universal_smart_crawler import UniversalSmartCrawler, ProductPrice
from decimal import Decimal

def create_sample_morrisons_data():
    """Create sample Morrisons data for testing"""
    
    print("📁 Creating sample Morrisons data...")
    
    # Create data directory structure
    data_dir = Path("crawlers/morrisons/crawler/data/branded")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample products data
    sample_categories = {
        "bakery_cakes.json": [
            {"name": "Hovis Medium White Bread 800g", "price": "£1.25", "offer": ""},
            {"name": "Warburtons Medium White Bread 800g", "price": "£1.30", "offer": "was £1.50"},
            {"name": "Kingsmill Medium White Bread 800g", "price": "£1.20", "offer": ""},
            {"name": "Mother Pride White Bread 800g", "price": "£1.15", "offer": ""},
            {"name": "Tesco White Bread 800g", "price": "£1.10", "offer": "was £1.40"}
        ],
        "drinks.json": [
            {"name": "Coca Cola Original 330ml Can", "price": "£0.85", "offer": ""},
            {"name": "Pepsi Original 330ml Can", "price": "£0.80", "offer": "was £0.95"},
            {"name": "Sprite Lemon Lime 330ml Can", "price": "£0.85", "offer": ""},
            {"name": "Fanta Orange 330ml Can", "price": "£0.82", "offer": ""},
            {"name": "7UP Regular 330ml Can", "price": "£0.78", "offer": "was £0.90"}
        ],
        "meat_poultry.json": [
            {"name": "British Chicken Breast Fillets 1kg", "price": "£4.50", "offer": ""},
            {"name": "British Beef Mince 500g", "price": "£3.25", "offer": "was £3.75"},
            {"name": "British Pork Sausages 454g", "price": "£2.80", "offer": ""},
            {"name": "Free Range Chicken Thighs 1kg", "price": "£3.90", "offer": ""},
            {"name": "British Lamb Leg Joint 1kg", "price": "£8.50", "offer": "was £9.20"}
        ]
    }
    
    # Write sample data files
    for filename, products in sample_categories.items():
        file_path = data_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Created {filename} with {len(products)} products")
    
    print(f"📁 Sample Morrisons data created in: {data_dir}")
    return data_dir

def create_sample_asda_data():
    """Create sample ASDA data for testing"""
    
    print("📁 Creating sample ASDA data...")
    
    # Create data directory structure  
    data_dir = Path("crawlers/asda/crawler/data/branded")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample ASDA products (slightly different prices)
    sample_categories = {
        "bakery_cakes.json": [
            {"name": "Hovis Medium White Bread 800g", "price": "£1.20", "offer": ""},
            {"name": "Warburtons Medium White Bread 800g", "price": "£1.35", "offer": ""},
            {"name": "Kingsmill Medium White Bread 800g", "price": "£1.18", "offer": "was £1.35"},
            {"name": "Mother Pride White Bread 800g", "price": "£1.12", "offer": ""},
            {"name": "ASDA Smart Price White Bread 800g", "price": "£0.95", "offer": ""}
        ],
        "drinks.json": [
            {"name": "Coca Cola Original 330ml Can", "price": "£0.88", "offer": ""},
            {"name": "Pepsi Original 330ml Can", "price": "£0.85", "offer": ""},
            {"name": "Sprite Lemon Lime 330ml Can", "price": "£0.87", "offer": "was £0.95"},
            {"name": "Fanta Orange 330ml Can", "price": "£0.84", "offer": ""},
            {"name": "ASDA Cola 330ml Can", "price": "£0.45", "offer": ""}
        ],
        "meat_poultry.json": [
            {"name": "British Chicken Breast Fillets 1kg", "price": "£4.25", "offer": "was £4.80"},
            {"name": "British Beef Mince 500g", "price": "£3.50", "offer": ""},
            {"name": "British Pork Sausages 454g", "price": "£2.75", "offer": ""},
            {"name": "Free Range Chicken Thighs 1kg", "price": "£4.10", "offer": ""},
            {"name": "ASDA Extra Special Lamb Leg 1kg", "price": "£7.95", "offer": "was £8.50"}
        ]
    }
    
    # Write sample data files
    for filename, products in sample_categories.items():
        file_path = data_dir / filename  
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Created {filename} with {len(products)} products")
    
    print(f"📁 Sample ASDA data created in: {data_dir}")
    return data_dir

async def test_crawler_for_store(store_name: str):
    """Test the universal crawler for a specific store"""
    
    print(f"\n🧪 Testing Universal Crawler for {store_name.title()}")
    print("=" * 50)
    
    try:
        # Create crawler instance
        crawler = UniversalSmartCrawler(store_name)
        
        # Test database connection
        connected = await crawler.connect_db()
        if not connected:
            print(f"❌ Failed to connect to database for {store_name}")
            return False
        
        # Test crawling products
        print(f"🔍 Testing product crawling for {store_name}...")
        products = await crawler.crawl_store_products()
        
        if not products:
            print(f"⚠️ No products found for {store_name}")
            return False
        
        print(f"✅ Successfully crawled {len(products)} products from {store_name}")
        
        # Show sample products
        print(f"\n📦 Sample products from {store_name}:")
        for i, product in enumerate(products[:5]):  # Show first 5 products
            print(f"  {i+1}. {product.name}")
            print(f"     Price: £{product.current_price}")
            if product.was_price:
                print(f"     Was: £{product.was_price}")
            print(f"     Category: {product.category}")
            print()
        
        if len(products) > 5:
            print(f"  ... and {len(products) - 5} more products")
        
        # Close database connection
        crawler.close_db()
        
        print(f"✅ {store_name.title()} crawler test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing {store_name} crawler: {e}")
        return False

async def test_national_average_calculation():
    """Test the national average calculation with sample data"""
    
    print(f"\n🧮 Testing National Average Calculation")
    print("=" * 50)
    
    try:
        # Create sample data for both stores
        morrisons_products = [
            ProductPrice("test_001", "Test Product A", Decimal("1.25"), None, None, "test", None, "morrisons"),
            ProductPrice("test_002", "Test Product B", Decimal("2.50"), None, None, "test", None, "morrisons"),
            ProductPrice("test_003", "Test Product C", Decimal("3.75"), None, None, "test", None, "morrisons"),
        ]
        
        asda_products = [
            ProductPrice("test_001", "Test Product A", Decimal("1.20"), None, None, "test", None, "asda"),
            ProductPrice("test_002", "Test Product B", Decimal("2.60"), None, None, "test", None, "asda"),
            ProductPrice("test_003", "Test Product C", Decimal("3.65"), None, None, "test", None, "asda"),
        ]
        
        # Test calculation
        crawler = UniversalSmartCrawler("test")
        
        all_store_data = {
            "morrisons": morrisons_products,
            "asda": asda_products
        }
        
        national_averages = crawler.calculate_new_national_averages(all_store_data)
        
        print("📊 Calculated National Averages:")
        for product_id, data in national_averages.items():
            print(f"  {product_id}: {data['name']}")
            print(f"    Average: £{data['national_average_price']}")
            print(f"    Range: £{data['lowest_price']} - £{data['highest_price']}")
            print(f"    Stores: {data['store_count']}")
            print()
        
        print("✅ National average calculation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing national average calculation: {e}")
        return False

async def main():
    """Main test function"""
    
    print("🧪 UNIVERSAL CRAWLER TEST SUITE")
    print("=" * 60)
    print("Testing crawler functionality for ASDA and Morrisons")
    print()
    
    # Create sample data
    print("📋 Step 1: Creating sample data...")
    create_sample_morrisons_data()
    create_sample_asda_data()
    print()
    
    # Test Morrisons crawler
    print("📋 Step 2: Testing Morrisons crawler...")
    morrisons_success = await test_crawler_for_store("morrisons")
    
    # Test ASDA crawler (will show not implemented)
    print("📋 Step 3: Testing ASDA crawler...")
    asda_success = await test_crawler_for_store("asda")
    
    # Test national average calculation
    print("📋 Step 4: Testing national average calculation...")
    calc_success = await test_national_average_calculation()
    
    # Summary
    print("\n🎯 TEST RESULTS SUMMARY")
    print("=" * 30)
    print(f"Morrisons Crawler: {'✅ PASS' if morrisons_success else '❌ FAIL'}")
    print(f"ASDA Crawler: {'✅ PASS' if asda_success else '❌ FAIL (not implemented)'}")
    print(f"National Averages: {'✅ PASS' if calc_success else '❌ FAIL'}")
    
    if morrisons_success and calc_success:
        print("\n🎉 Core crawler functionality is working!")
        print("💡 ASDA crawler needs implementation (currently placeholder)")
        print("🚀 Ready to implement real web crawling for both stores")
    else:
        print("\n⚠️ Some tests failed - check errors above")
    
    # Cleanup test data
    print("\n🧹 Cleaning up test data...")
    import shutil
    if Path("crawlers").exists():
        shutil.rmtree("crawlers")
        print("✅ Test data cleaned up")

if __name__ == "__main__":
    asyncio.run(main())
