#!/usr/bin/env python3
"""
Load Testing Script for Smart Shopping Website
Tests concurrent user capacity up to 100 users
"""

import asyncio
import aiohttp
import time
import random
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def simulate_user_session(session_id: int, session: aiohttp.ClientSession):
    """Simulate a complete user session"""
    user_actions = []
    
    try:
        # 1. Login
        start_time = time.time()
        login_data = {
            "username": f"test_user_{session_id}",
            "password": "password123"
        }
        
        async with session.post(f"{BASE_URL}/api/auth/login", json=login_data) as resp:
            login_result = await resp.json()
            user_session_id = login_result.get("session_id", "")
        
        user_actions.append(f"Login: {time.time() - start_time:.2f}s")
        
        # 2. View home page
        start_time = time.time()
        async with session.get(f"{BASE_URL}/?session_id={user_session_id}") as resp:
            await resp.text()
        user_actions.append(f"Home page: {time.time() - start_time:.2f}s")
        
        # 3. Get promotions
        start_time = time.time()
        async with session.get(f"{BASE_URL}/api/promotions") as resp:
            await resp.json()
        user_actions.append(f"Promotions: {time.time() - start_time:.2f}s")
        
        # 4. Search products
        search_terms = ["beans", "bread", "milk", "chicken", "pasta"]
        search_term = random.choice(search_terms)
        
        start_time = time.time()
        async with session.get(f"{BASE_URL}/api/products/search?q={search_term}&session_id={user_session_id}") as resp:
            await resp.json()
        user_actions.append(f"Product search: {time.time() - start_time:.2f}s")
        
        # 5. Analyze savings
        items = random.sample(search_terms, 3)
        savings_data = {"items": items, "preferred_store": None}
        
        start_time = time.time()
        async with session.post(f"{BASE_URL}/api/analyze-savings?session_id={user_session_id}", json=savings_data) as resp:
            await resp.json()
        user_actions.append(f"Savings analysis: {time.time() - start_time:.2f}s")
        
        # 6. Create shopping list
        list_data = {
            "name": f"Shopping List {session_id}",
            "items": items,
            "store_preference": "Tesco"
        }
        
        start_time = time.time()
        async with session.post(f"{BASE_URL}/api/shopping-lists?session_id={user_session_id}", json=list_data) as resp:
            await resp.json()
        user_actions.append(f"Create list: {time.time() - start_time:.2f}s")
        
        # 7. Get user stats
        start_time = time.time()
        async with session.get(f"{BASE_URL}/api/user-stats?session_id={user_session_id}") as resp:
            await resp.json()
        user_actions.append(f"User stats: {time.time() - start_time:.2f}s")
        
        return f"User {session_id}: SUCCESS - {', '.join(user_actions)}"
        
    except Exception as e:
        return f"User {session_id}: ERROR - {str(e)}"

async def load_test(num_users: int = 50):
    """Run load test with specified number of concurrent users"""
    print(f"🚀 Starting load test with {num_users} concurrent users")
    print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    # Create connector with limits for high concurrency
    connector = aiohttp.TCPConnector(
        limit=200,  # Total connection limit
        limit_per_host=100,  # Per-host connection limit
        ttl_dns_cache=300,
        use_dns_cache=True,
    )
    
    timeout = aiohttp.ClientTimeout(total=30)  # 30-second timeout
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:        # Test server health first
        try:
            async with session.get(f"{BASE_URL}/api/system-stats") as resp:
                if resp.status == 200:
                    print("✅ Server is healthy and responding")
                else:
                    print(f"❌ Server health check failed: {resp.status}")
                    return
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return
        
        # Create tasks for concurrent users
        start_time = time.time()
        tasks = []
        
        for i in range(num_users):
            task = simulate_user_session(i + 1, session)
            tasks.append(task)
        
        # Run all user sessions concurrently
        print(f"🧪 Running {num_users} concurrent user sessions...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        successful_users = 0
        failed_users = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Exception: {result}")
                failed_users += 1
            elif "SUCCESS" in str(result):
                successful_users += 1
            else:
                print(f"❌ {result}")
                failed_users += 1
        
        # Print summary
        print(f"\n📊 LOAD TEST RESULTS")
        print(f"={'='*50}")
        print(f"Total Users: {num_users}")
        print(f"Successful: {successful_users} ({successful_users/num_users*100:.1f}%)")
        print(f"Failed: {failed_users} ({failed_users/num_users*100:.1f}%)")
        print(f"Total Time: {total_time:.2f} seconds")
        print(f"Avg Time per User: {total_time/num_users:.2f} seconds")
        print(f"Users per Second: {num_users/total_time:.2f}")
        
        # Performance rating
        if successful_users == num_users and total_time < num_users * 0.5:
            print(f"🎉 EXCELLENT: All users completed successfully in {total_time:.1f}s")
        elif successful_users >= num_users * 0.9:
            print(f"✅ GOOD: {successful_users}/{num_users} users successful")
        elif successful_users >= num_users * 0.7:
            print(f"⚠️  FAIR: {successful_users}/{num_users} users successful")
        else:
            print(f"❌ POOR: Only {successful_users}/{num_users} users successful")

async def stress_test():
    """Progressive stress test"""
    test_levels = [10, 25, 50, 75, 100]
    
    print("🔥 PROGRESSIVE STRESS TEST")
    print("Testing server capacity with increasing user loads...\n")
    
    for num_users in test_levels:
        print(f"\n{'='*60}")
        print(f"TESTING {num_users} CONCURRENT USERS")
        print(f"{'='*60}")
        
        await load_test(num_users)
        
        # Wait between tests
        if num_users < test_levels[-1]:
            print(f"\n⏳ Waiting 10 seconds before next test...")
            await asyncio.sleep(10)

async def quick_test():
    """Quick test with a few users"""
    await load_test(5)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "stress":
            asyncio.run(stress_test())
        elif sys.argv[1] == "quick":
            asyncio.run(quick_test())
        elif sys.argv[1].isdigit():
            asyncio.run(load_test(int(sys.argv[1])))
        else:
            print("Usage:")
            print("  python load_test.py         - Test with 50 users")
            print("  python load_test.py quick   - Quick test with 5 users")
            print("  python load_test.py stress  - Progressive test (10→100 users)")
            print("  python load_test.py 100     - Test with specific number of users")
    else:
        asyncio.run(load_test(50))
