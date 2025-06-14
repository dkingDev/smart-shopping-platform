#!/usr/bin/env python3
"""
Enhanced Smart Shopping Website - SQLite Version for Testing
Works with your existing SQLite database while AWS is being configured
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import os
import sqlite3
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Shopping Platform - Demo",
    description="Enhanced shopping platform with smart features (SQLite Demo)",
    version="2.0.0-demo"
)

# Security
security = HTTPBearer()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates and static files
templates = Jinja2Templates(directory="templates")
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple SQLite connection
def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models
class SavingsAnalysis(BaseModel):
    items: List[str]
    preferred_store: Optional[str] = None

# Mock auth for demo (replace with real auth)
def get_current_user_demo():
    return {
        "id": 1,
        "username": "demo_user",
        "email": "demo@smartshopping.com",
        "full_name": "Demo User"
    }

@app.get("/", response_class=HTMLResponse)
async def home_with_promotions(request: Request):
    """Enhanced home page with demo promotions"""
    try:
        # Mock promotions data
        promotions = [
            {
                "id": 1,
                "store_name": "Tesco",
                "title": "Tesco - Summer Savings!",
                "description": "Save up to 25% on fresh produce and household essentials",
                "image_url": "/static/images/tesco-banner.jpg",
                "promotion_type": "sponsored_banner"
            },
            {
                "id": 2,
                "store_name": "ASDA",
                "title": "ASDA - Price Promise",
                "description": "Lowest prices guaranteed or we'll refund the difference",
                "image_url": "/static/images/asda-banner.jpg",
                "promotion_type": "sponsored_banner"
            }
        ]
        
        # Mock featured offers
        featured_offers = [
            {
                "store_name": "Aldi",
                "title": "Special Buys This Week",
                "description": "Limited time offers on quality products"
            },
            {
                "store_name": "Iceland",
                "title": "Frozen Food Deals", 
                "description": "Buy 2 get 1 free on selected frozen items"
            }
        ]
        
        return templates.TemplateResponse("enhanced_home.html", {
            "request": request,
            "promotions": promotions,
            "featured_offers": featured_offers,
            "user": None,
            "page_title": "Smart Shopping Demo - Best Prices Across All Stores"
        })
        
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        return HTMLResponse("<h1>Demo Home Page</h1><p>Testing smart shopping features...</p>")

@app.get("/api/promotions")
async def get_active_promotions(promotion_type: str = None, limit: int = 10):
    """Get demo promotions"""
    promotions = [
        {
            "id": 1,
            "store_name": "Tesco",
            "promotion_type": "sponsored_banner",
            "title": "Tesco - Best Prices Guaranteed!",
            "description": "Save up to 30% on thousands of products at Tesco. Free delivery on orders over £40.",
            "display_priority": 10
        },
        {
            "id": 2,
            "store_name": "ASDA",
            "promotion_type": "product_highlight",
            "title": "ASDA Weekly Specials",
            "description": "Featured deals handpicked for maximum savings",
            "display_priority": 8
        },
        {
            "id": 3,
            "store_name": "Aldi",
            "promotion_type": "sponsored_banner",
            "title": "Aldi - Quality at Low Prices",
            "description": "Discover award-winning products at unbeatable prices",
            "display_priority": 9
        }
    ]
    
    if promotion_type:
        promotions = [p for p in promotions if p["promotion_type"] == promotion_type]
    
    return {"promotions": promotions[:limit]}

@app.post("/api/analyze-savings")
async def analyze_shopping_savings(analysis: SavingsAnalysis):
    """Analyze potential savings using your SQLite data"""
    try:
        conn = get_db_connection()
        
        # Get actual price data from your database
        savings_data = []
        
        # Get all stores
        stores_query = "SELECT DISTINCT store_name FROM store_prices"
        stores = [row[0] for row in conn.execute(stores_query).fetchall()]
        
        for store in stores:
            total_cost = 0
            available_items = 0
            
            # Calculate costs for each item in this store
            for item_search in analysis.items:
                # Search for products matching the item
                product_query = """
                    SELECT sp.current_price 
                    FROM store_prices sp 
                    JOIN products p ON sp.product_id = p.id 
                    WHERE sp.store_name = ? AND p.name LIKE ?
                    ORDER BY sp.current_price ASC 
                    LIMIT 1
                """
                
                result = conn.execute(product_query, (store, f"%{item_search}%")).fetchone()
                
                if result:
                    total_cost += result[0]
                    available_items += 1
            
            if available_items > 0:
                savings_data.append({
                    "store_name": store,
                    "total_cost": round(total_cost, 2),
                    "potential_savings": 0,  # Will calculate below
                    "unavailable_items": len(analysis.items) - available_items,
                    "best_offers": [f"Save on {available_items} items"]
                })
        
        # Calculate potential savings
        if savings_data:
            min_cost = min(store["total_cost"] for store in savings_data)
            for store in savings_data:
                store["potential_savings"] = round(store["total_cost"] - min_cost, 2)
        
        conn.close()
        
        best_store = min(savings_data, key=lambda x: x["total_cost"])["store_name"] if savings_data else "Unknown"
        max_savings = max(store["potential_savings"] for store in savings_data) if savings_data else 0
        
        return {
            "savings_analysis": savings_data,
            "recommendation": {
                "best_store": best_store,
                "max_savings": max_savings
            }
        }
        
    except Exception as e:
        logger.error(f"Error analyzing savings: {e}")
        return {
            "savings_analysis": [],
            "recommendation": {"best_store": "Tesco", "max_savings": 0}
        }

@app.get("/api/products/search")
async def search_products(q: str = "", limit: int = 20):
    """Search products in your SQLite database"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT p.*, sp.store_name, sp.current_price, sp.offer_text
            FROM products p
            LEFT JOIN store_prices sp ON p.id = sp.product_id
            WHERE p.name LIKE ?
            ORDER BY p.name
            LIMIT ?
        """
        
        results = conn.execute(query, (f"%{q}%", limit)).fetchall()
        
        products = []
        for row in results:
            products.append({
                "id": row[0],
                "name": row[1],
                "brand": row[2],
                "category": row[3],
                "barcode": row[4],
                "description": row[5],
                "image_url": row[6],
                "store_name": row[9] if len(row) > 9 else None,
                "current_price": row[10] if len(row) > 10 else None,
                "offer_text": row[11] if len(row) > 11 else None
            })
        
        conn.close()
        
        return {"products": products}
        
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        return {"products": []}

@app.get("/api/stores")
async def get_stores():
    """Get all available stores from your database"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT store_name, COUNT(*) as product_count, 
                   ROUND(AVG(current_price), 2) as avg_price,
                   MIN(current_price) as min_price,
                   MAX(current_price) as max_price
            FROM store_prices 
            GROUP BY store_name
            ORDER BY product_count DESC
        """
        
        results = conn.execute(query).fetchall()
        
        stores = []
        for row in results:
            stores.append({
                "name": row[0],
                "product_count": row[1],
                "avg_price": row[2],
                "min_price": row[3],
                "max_price": row[4]
            })
        
        conn.close()
        
        return {"stores": stores}
        
    except Exception as e:
        logger.error(f"Error getting stores: {e}")
        return {"stores": []}

@app.get("/api/smart-switch-demo")
async def demo_smart_switch():
    """Demo smart switching feature"""
    return {
        "switch_options": [
            {
                "target_store": "Tesco",
                "switchable_items": 8,
                "unavailable_items": 2,
                "estimated_savings": 3.45,
                "availability_score": 0.8,
                "recommendation_score": 0.85
            },
            {
                "target_store": "ASDA", 
                "switchable_items": 9,
                "unavailable_items": 1,
                "estimated_savings": 5.20,
                "availability_score": 0.9,
                "recommendation_score": 0.92
            },
            {
                "target_store": "Aldi",
                "switchable_items": 6,
                "unavailable_items": 4,
                "estimated_savings": 7.80,
                "availability_score": 0.6,
                "recommendation_score": 0.65
            }
        ],
        "demo_mode": True
    }

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Demo dashboard with smart features"""
    try:
        return templates.TemplateResponse("enhanced_dashboard.html", {
            "request": request,
            "user": get_current_user_demo(),
            "page_title": "Smart Shopping Dashboard - Demo"
        })
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return HTMLResponse("<h1>Demo Dashboard</h1><p>Smart shopping features dashboard...</p>")

@app.get("/health")
async def health_check():
    """Health check with database stats"""
    try:
        conn = get_db_connection()
        
        # Get database stats
        product_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        price_count = conn.execute("SELECT COUNT(*) FROM store_prices").fetchone()[0]
        store_count = conn.execute("SELECT COUNT(DISTINCT store_name) FROM store_prices").fetchone()[0]
        
        conn.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0-demo",
            "database": "SQLite",
            "features": {
                "promotions": True,
                "smart_switching": True,
                "savings_analysis": True,
                "product_search": True
            },
            "stats": {
                "products": product_count,
                "price_records": price_count,
                "stores": store_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Smart Shopping Demo Website...")
    print("📊 Using SQLite database with your existing data")
    print("🌐 Visit: http://localhost:8000")
    print("\n✨ Features available:")
    print("- Store promotions and sponsored content")
    print("- Smart cost savings analysis")
    print("- Product search across all stores")
    print("- Store comparison and switching demo")
    print("\n🔧 Configure AWS PostgreSQL in .env to use full features")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
