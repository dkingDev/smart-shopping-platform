#!/usr/bin/env python3
"""
Populate AWS PostgreSQL with demo data for new smart shopping features
Uses existing AWS database data to create realistic promotional content
"""

import os
import json
import random
from datetime import datetime, timedelta
from database.aws_postgresql_manager import AWSPostgreSQLManager

def populate_store_promotions(db_manager):
    """Create store promotions using existing store data from AWS PostgreSQL"""
    print("🎯 Creating store promotions...")
    
    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            # Get existing stores from store_prices table
            cur.execute("SELECT DISTINCT store_name FROM store_prices LIMIT 10")
            stores = [row[0] for row in cur.fetchall()]
            
            promotions = []
            
            # Create sponsored banner promotions
            for i, store in enumerate(stores[:5]):
                promotion = {
                    'store_name': store,
                    'promotion_type': 'sponsored_banner',
                    'title': f'{store} - Best Prices Guaranteed!',
                    'description': f'Save up to 30% on thousands of products at {store}. Free delivery on orders over £40.',
                    'image_url': f'/static/images/banners/{store.lower().replace(" ", "_")}_banner.jpg',
                    'target_url': f'/store/{store.lower().replace(" ", "-")}',
                    'promotion_data': json.dumps({
                        'discount_percentage': random.randint(10, 30),
                        'min_order_value': 40,
                        'categories': ['groceries', 'household', 'fresh_food']
                    }),
                    'display_priority': 10 - i,
                    'max_impressions': 10000,
                    'cost_per_impression': round(random.uniform(0.05, 0.15), 4),
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=30)
                }
                promotions.append(promotion)
            
            # Create product highlight promotions
            for store in stores[:8]:
                promotion = {
                    'store_name': store,
                    'promotion_type': 'product_highlight',
                    'title': f'Featured Deals at {store}',
                    'description': f'Hand-picked deals and offers from {store}',
                    'image_url': f'/static/images/offers/{store.lower().replace(" ", "_")}_offers.jpg',
                    'target_url': f'/store/{store.lower().replace(" ", "-")}/offers',
                    'promotion_data': json.dumps({
                        'featured_products': ['bread', 'milk', 'chicken', 'pasta'],
                        'offer_type': 'percentage',
                        'discount_range': [15, 25]
                    }),
                    'display_priority': random.randint(5, 8),
                    'max_impressions': 5000,
                    'cost_per_impression': round(random.uniform(0.03, 0.10), 4),
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=14)
                }
                promotions.append(promotion)
            
            # Insert promotions
            for promo in promotions:
                cur.execute("""
                    INSERT INTO store_promotions 
                    (store_name, promotion_type, title, description, image_url, target_url, 
                     promotion_data, display_priority, max_impressions, cost_per_impression, 
                     start_date, end_date, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    promo['store_name'], promo['promotion_type'], promo['title'], 
                    promo['description'], promo['image_url'], promo['target_url'],
                    promo['promotion_data'], promo['display_priority'], 
                    promo['max_impressions'], promo['cost_per_impression'],
                    promo['start_date'], promo['end_date'], True
                ))
            
            conn.commit()
            print(f"✅ Created {len(promotions)} store promotions")

def populate_product_availability(db_manager):
    """Create product availability data using existing products and stores"""
    print("📦 Creating product availability data...")
    
    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            # Get existing products and stores
            cur.execute("""
                SELECT DISTINCT bp.product_id, sp.store_name 
                FROM branded_products bp 
                JOIN store_prices sp ON bp.product_id = sp.product_id 
                LIMIT 100
            """)
            
            product_store_combinations = cur.fetchall()
            
            # Sample UK postcodes for location testing
            postcodes = ['SW1A 1AA', 'M1 1AA', 'B1 1AA', 'LS1 1AB', 'NE1 1EE', 'G1 1AA']
            
            availability_records = []
            
            for product_id, store_name in product_store_combinations:
                for postcode in random.sample(postcodes, random.randint(2, 4)):
                    availability_records.append({
                        'product_id': product_id,
                        'store_name': store_name,
                        'location_identifier': postcode,
                        'is_available': random.choice([True, True, True, False]),  # 75% availability
                        'stock_level': random.choice(['in_stock', 'in_stock', 'low_stock', 'out_of_stock']),
                        'delivery_available': random.choice([True, True, False]),
                        'click_collect_available': random.choice([True, False])
                    })
            
            # Insert availability data
            for record in availability_records:
                cur.execute("""
                    INSERT INTO product_availability 
                    (product_id, store_name, location_identifier, is_available, 
                     stock_level, delivery_available, click_collect_available)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (product_id, store_name, location_identifier) DO NOTHING
                """, (
                    record['product_id'], record['store_name'], record['location_identifier'],
                    record['is_available'], record['stock_level'], 
                    record['delivery_available'], record['click_collect_available']
                ))
            
            conn.commit()
            print(f"✅ Created availability data for {len(availability_records)} product-store-location combinations")

def create_demo_users_and_lists(db_manager):
    """Create demo users with shopping lists and templates"""
    print("👥 Creating demo users and shopping data...")
    
    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            # Create demo users
            demo_users = [
                {
                    'username': 'demo_user1',
                    'email': 'demo1@smartshopping.com',
                    'password_hash': '$2b$12$LQv3c1yqBwlaDlOzCAx8a.2WjCExAzTL0b1LqIcf3qKjlVtfGKY16',  # 'password123'
                    'full_name': 'Sarah Johnson',
                    'is_premium': True
                },
                {
                    'username': 'demo_user2',
                    'email': 'demo2@smartshopping.com', 
                    'password_hash': '$2b$12$LQv3c1yqBwlaDlOzCAx8a.2WjCExAzTL0b1LqIcf3qKjlVtfGKY16',
                    'full_name': 'Michael Brown',
                    'is_premium': False
                }
            ]
            
            user_ids = []
            for user in demo_users:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, full_name, is_premium)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE SET
                    email = EXCLUDED.email,
                    full_name = EXCLUDED.full_name,
                    is_premium = EXCLUDED.is_premium
                    RETURNING id
                """, (user['username'], user['email'], user['password_hash'], 
                      user['full_name'], user['is_premium']))
                
                user_id = cur.fetchone()[0]
                user_ids.append(user_id)
            
            # Create user locations
            locations = [
                {
                    'user_id': user_ids[0],
                    'location_name': 'Home',
                    'postcode': 'SW1A 1AA',
                    'is_primary': True,
                    'available_stores': ['Tesco', 'Sainsburys', 'ASDA', 'Morrisons']
                },
                {
                    'user_id': user_ids[0],
                    'location_name': 'Work',
                    'postcode': 'M1 1AA',
                    'is_primary': False,
                    'available_stores': ['Tesco', 'ASDA', 'Iceland']
                },
                {
                    'user_id': user_ids[1],
                    'location_name': 'Home',
                    'postcode': 'B1 1AA',
                    'is_primary': True,
                    'available_stores': ['ASDA', 'Morrisons', 'Iceland', 'Lidl']
                }
            ]
            
            for location in locations:
                cur.execute("""
                    INSERT INTO user_locations 
                    (user_id, location_name, postcode, is_primary, available_stores)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (location['user_id'], location['location_name'], 
                      location['postcode'], location['is_primary'], location['available_stores']))
            
            # Get some real product names for shopping lists
            cur.execute("SELECT name FROM branded_products LIMIT 20")
            available_products = [row[0] for row in cur.fetchall()]
            
            # Create shopping lists
            for user_id in user_ids:
                # Weekly shopping list
                cur.execute("""
                    INSERT INTO shopping_lists (user_id, name, description)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (user_id, 'Weekly Shopping', 'Regular weekly groceries'))
                
                list_id = cur.fetchone()[0]
                
                # Add items to the list
                for product in random.sample(available_products, min(8, len(available_products))):
                    cur.execute("""
                        INSERT INTO shopping_list_items 
                        (list_id, product_name, quantity, preferred_stores)
                        VALUES (%s, %s, %s, %s)
                    """, (list_id, product, random.randint(1, 3), 
                          random.sample(['Tesco', 'ASDA', 'Sainsburys', 'Morrisons'], 2)))
            
            # Create shopping list templates
            template_items = [
                {'name': 'Bread', 'quantity': 1, 'preferred_stores': ['Tesco', 'ASDA']},
                {'name': 'Milk', 'quantity': 2, 'preferred_stores': ['Sainsburys', 'Morrisons']},
                {'name': 'Eggs', 'quantity': 1, 'preferred_stores': ['Tesco', 'ASDA']},
                {'name': 'Chicken', 'quantity': 1, 'preferred_stores': ['Sainsburys', 'Morrisons']}
            ]
            
            for user_id in user_ids:
                cur.execute("""
                    INSERT INTO shopping_list_templates 
                    (user_id, template_name, base_items, frequency, auto_create)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, 'Weekly Essentials', json.dumps(template_items), 'weekly', False))
            
            conn.commit()
            print(f"✅ Created {len(demo_users)} demo users with locations, lists, and templates")

def create_savings_analysis_data(db_manager):
    """Create sample savings analysis data"""
    print("💰 Creating savings analysis data...")
    
    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            # Get user IDs
            cur.execute("SELECT id FROM users WHERE username LIKE 'demo_user%'")
            user_ids = [row[0] for row in cur.fetchall()]
            
            # Create savings analysis records
            for user_id in user_ids:
                analysis_data = {
                    'tesco': {'total': 45.67, 'savings': 0},
                    'asda': {'total': 42.30, 'savings': 3.37},
                    'sainsburys': {'total': 48.99, 'savings': -3.32},
                    'morrisons': {'total': 44.15, 'savings': 1.52}
                }
                
                cur.execute("""
                    INSERT INTO savings_analysis 
                    (user_id, analysis_type, comparison_data, potential_savings, recommended_action)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    user_id, 'list_comparison', json.dumps(analysis_data), 
                    3.37, 'Switch to ASDA to save £3.37 on your weekly shop'
                ))
            
            conn.commit()
            print(f"✅ Created savings analysis for {len(user_ids)} users")

def main():
    """Main function to populate all demo data"""
    print("🚀 Starting AWS PostgreSQL demo data population...")
    
    # Initialize database manager
    db_manager = AWSPostgreSQLManager()
    
    try:
        # Test connection
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print(f"✅ Connected to PostgreSQL: {version}")
        
        # Populate data
        populate_store_promotions(db_manager)
        populate_product_availability(db_manager)
        create_demo_users_and_lists(db_manager)
        create_savings_analysis_data(db_manager)
        
        print("\n🎉 Demo data population completed successfully!")
        print("\nDemo users created:")
        print("- Username: demo_user1, Password: password123 (Premium)")
        print("- Username: demo_user2, Password: password123 (Free)")
        print("\nYou can now test all the smart shopping features!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
