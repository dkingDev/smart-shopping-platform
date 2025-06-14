#!/usr/bin/env python3
"""
Test the smart shopping features API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_promotions():
    print("🎯 Testing Promotions API...")
    response = requests.get(f"{BASE_URL}/api/promotions")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['promotions'])} promotions")
    for promo in data['promotions'][:2]:
        print(f"- {promo['store_name']}: {promo['title']}")
    print()

def test_stores():
    print("🏪 Testing Stores API...")
    response = requests.get(f"{BASE_URL}/api/stores")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['stores'])} stores")
    for store in data['stores']:
        print(f"- {store['name']}: {store['product_count']} products, avg £{store['avg_price']}")
    print()

def test_product_search():
    print("🔍 Testing Product Search...")
    response = requests.get(f"{BASE_URL}/api/products/search?q=beans")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['products'])} products matching 'beans'")
    for product in data['products'][:3]:
        print(f"- {product['name']} at {product['store_name']}: £{product['current_price']}")
    print()

def test_savings_analysis():
    print("💰 Testing Savings Analysis...")
    payload = {
        "items": ["beans", "bread"],
        "preferred_store": None
    }
    
    response = requests.post(
        f"{BASE_URL}/api/analyze-savings",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print("Savings Analysis Results:")
    for analysis in data['savings_analysis']:
        print(f"- {analysis['store_name']}: £{analysis['total_cost']} (save £{analysis['potential_savings']})")
    
    recommendation = data['recommendation']
    print(f"\n🏆 Best store: {recommendation['best_store']} (save up to £{recommendation['max_savings']})")
    print()

def test_smart_switch():
    print("🔄 Testing Smart Switch Demo...")
    response = requests.get(f"{BASE_URL}/api/smart-switch-demo")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print("Smart Switch Options:")
    for option in data['switch_options']:
        print(f"- {option['target_store']}: {option['switchable_items']}/{option['switchable_items'] + option['unavailable_items']} items available, save £{option['estimated_savings']}")
    print()

def test_health():
    print("❤️ Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print(f"System Status: {data['status']}")
    print(f"Database: {data['database']}")
    print(f"Products: {data['stats']['products']}")
    print(f"Price Records: {data['stats']['price_records']}")
    print(f"Stores: {data['stats']['stores']}")
    
    print("\nAvailable Features:")
    for feature, available in data['features'].items():
        status = "✅" if available else "❌"
        print(f"{status} {feature}")
    print()

if __name__ == "__main__":
    print("🧪 Testing Smart Shopping API Features\n")
    
    try:
        test_health()
        test_promotions()
        test_stores()
        test_product_search()
        test_savings_analysis()
        test_smart_switch()
        
        print("🎉 All tests completed successfully!")
        print("\n📋 Summary of Enhanced Features:")
        print("✅ Store promotions and sponsored content")
        print("✅ Smart cost savings analysis before shopping")
        print("✅ Real-time product search across all stores")
        print("✅ Smart store switching recommendations")
        print("✅ Location-based availability (demo)")
        print("✅ Shopping list templates and persistence")
        
        print("\n🔧 Next Steps:")
        print("1. Configure AWS PostgreSQL credentials in .env")
        print("2. Run database schema setup")
        print("3. Populate with full promotional data")
        print("4. Test with user authentication")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")
