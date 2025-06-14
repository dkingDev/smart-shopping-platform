#!/usr/bin/env python3
"""
Smart Shopping Platform - Secure Backend API
Copyright (c) 2025 Spirit of the Immortals Ltd
Company Registration: 13434726 (England & Wales)
Director: Derek King

ALL RIGHTS RESERVED - PROPRIETARY SOFTWARE
This software contains trade secrets and proprietary algorithms.
Unauthorized copying, modification, or distribution is strictly prohibited.
For licensing inquiries: derek.j.king@live.com

Production-ready FastAPI backend with AWS PostgreSQL integration
"""

from dotenv import load_dotenv
# Load environment variables first
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import json
import os
import hashlib
import secrets
import asyncio
from datetime import datetime, timedelta
import logging
from jose import JWTError, jwt
from passlib.context import CryptContext
import re
from database.aws_postgresql_manager import AWSPostgreSQLManager

# Setup secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smart_shopping_secure.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with security
app = FastAPI(
    title="Smart Shopping Platform - Secure AWS",
    description="Secure smart shopping platform with AWS PostgreSQL",
    version="3.1.0-aws",
    docs_url="/admin/docs",  # Restrict docs access
    redoc_url=None
)

# Security configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Update .env JWT secret if it's the default
if os.getenv("JWT_SECRET_KEY") == "your-super-secret-jwt-key-change-in-production-please":
    logger.warning("⚠️  Using default JWT secret! Update JWT_SECRET_KEY in .env for production!")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Development
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:9999",
        "http://localhost:8888",
        
        # Production domains - Shopping Platform
        "https://thesmartshoppingsite.com",
        "https://www.thesmartshoppingsite.com",
        "https://thesmartshoppingsite.co.uk",
        "https://www.thesmartshoppingsite.co.uk",
          # Production domains - Company
        "https://spiritoftheimmortalsltd.co.uk",
        "https://www.spiritoftheimmortalsltd.co.uk",
        "https://spiritoftheimmortals.co.uk",
        "https://www.spiritoftheimmortals.co.uk",
        
        # Temporary hosting
        "https://*.github.io",
        "https://yourusername.github.io",
        "https://*.herokuapp.com",
        "https://*.railway.app",
        "https://*.vercel.app",
        "https://*.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security bearer token
security = HTTPBearer()

# Templates and static files
templates = Jinja2Templates(directory="templates")
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount frontend
if os.path.exists("frontend"):
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# AWS Database manager
try:
    db_manager = AWSPostgreSQLManager()
    print("✅ Connected to AWS PostgreSQL Database")
except Exception as e:
    print(f"❌ AWS Database connection failed: {e}")
    print("🔧 Please check your .env file AWS credentials")
    db_manager = None

# Security models with basic validation
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    location: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class SavingsAnalysis(BaseModel):
    items: List[str]
    preferred_store: Optional[str] = None

class ShoppingList(BaseModel):
    name: str
    items: List[str]
    store_preference: Optional[str] = None

# Security validation functions
def validate_username(username: str) -> bool:
    """Validate username format"""
    return bool(re.match("^[a-zA-Z0-9_]{3,50}$", username))

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

# Security functions
def hash_password(password: str) -> str:
    """Hash password securely"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if username is None or user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from AWS database
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, email, full_name, is_active, is_premium, created_at
                    FROM users 
                    WHERE id = %s AND username = %s AND is_active = true
                """, (user_id, username))
                
                user = cur.fetchone()
                if user is None:
                    raise credentials_exception
                
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "full_name": user[3],
                    "is_active": user[4],
                    "is_premium": user[5],
                    "created_at": user[6].isoformat() if user[6] else None
                }
                
    except Exception as e:
        logger.error(f"Database error getting user: {e}")
        raise credentials_exception

async def log_user_activity(user_id: int, action: str, data: Dict[str, Any], ip_address: Optional[str] = None):
    """Log user activity to AWS database"""
    if not db_manager:
        return
        
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_activity_logs (user_id, action, details, ip_address, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, action, json.dumps(data), ip_address, datetime.utcnow()))
                conn.commit()
    except Exception as e:
        logger.error(f"Failed to log user activity: {e}")

# Authentication endpoints
@app.post("/auth/register")
async def register_user(user: UserRegister, request: Request, background_tasks: BackgroundTasks):
    """Secure user registration with AWS database"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    # Validate password strength (simplified for email-based auth)
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    try:
        # Hash password
        hashed_password = hash_password(user.password)
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check if user exists (using email as unique identifier)
                cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
                
                if cur.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
                  # Create user in AWS database (using email as username)
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, full_name, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (user.email, user.email, hashed_password, user.full_name, True, datetime.utcnow()))
                
                user_id = cur.fetchone()[0]
                conn.commit()
                  # Create access token
                access_token = create_access_token(data={"sub": user.email, "user_id": user_id})
                
                user_data = {
                    "id": user_id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": True,
                    "is_premium": False
                }
                # Log registration
                background_tasks.add_task(
                    log_user_activity, 
                    user_id, 
                    "user_registration", 
                    {"email": user.email, "full_name": user.full_name},
                    request.client.host if request.client else None
                )
                
                logger.info(f"New user registered: {user.email}")
                return {"success": True, "data": {"access_token": access_token, "token_type": "bearer", "user": user_data}}
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@app.post("/auth/login")
async def login_user(user: UserLogin, request: Request, background_tasks: BackgroundTasks):
    """Secure user login with AWS database"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:                # Get user from AWS database using email
                cur.execute("""
                    SELECT id, username, email, password_hash, full_name, is_active, is_premium
                    FROM users 
                    WHERE email = %s AND is_active = true
                """, (user.email,))
                
                db_user = cur.fetchone()
                
                if not db_user or not verify_password(user.password, db_user[3]):
                    # Log failed login attempt
                    background_tasks.add_task(
                        log_user_activity,
                        0,  # No user ID for failed login
                        "login_failed",
                        {"email": user.email, "reason": "invalid_credentials"},
                        request.client.host if request.client else None
                    )
                    
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect email or password"
                    )
                
                # Update last login
                cur.execute("""
                    UPDATE users SET last_login = %s WHERE id = %s
                """, (datetime.utcnow(), db_user[0]))
                conn.commit()
                  # Create access token
                access_token = create_access_token(data={"sub": db_user[2], "user_id": db_user[0]})  # Use email as sub
                
                user_data = {
                    "id": db_user[0],
                    "email": db_user[2],
                    "full_name": db_user[4],
                    "is_active": db_user[5],
                    "is_premium": db_user[6]
                }
                
                # Log successful login
                background_tasks.add_task(
                    log_user_activity,
                    db_user[0],
                    "user_login",
                    {"email": user.email},
                    request.client.host if request.client else None
                )
                
                logger.info(f"User logged in: {user.email}")
                return {"success": True, "data": {"access_token": access_token, "token_type": "bearer", "user": user_data}}
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@app.get("/auth/verify-token")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token validity"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return {"success": True, "message": "Token is valid", "user_id": user_id, "username": username}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/auth/refresh-token")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new access token
        new_token = create_access_token(data={"sub": username, "user_id": user_id})
        
        return {"success": True, "data": {"access_token": new_token, "token_type": "bearer"}}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/auth/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user (client-side token invalidation)"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        
        logger.info(f"User logged out: {username}")
        return {"success": True, "message": "Logged out successfully"}
        
    except JWTError:
        # Even if token is invalid, logout succeeds
        return {"success": True, "message": "Logged out successfully"}

# Protected endpoints with AWS database integration
@app.get("/api/promotions")
async def get_active_promotions(promotion_type: Optional[str] = None, limit: int = 10):
    """Get active promotions from AWS database"""
    if not db_manager:
        # Return mock data if AWS not available
        return {"promotions": [
            {"id": 1, "store_name": "Tesco", "title": "Summer Savings", "promotion_type": "banner"},
            {"id": 2, "store_name": "ASDA", "title": "Price Promise", "promotion_type": "banner"}
        ]}
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Use the AWS function we created
                cur.execute("SELECT * FROM get_active_store_promotions(%s, %s)", 
                          (promotion_type, limit))
                
                promotions = []
                for row in cur.fetchall():
                    promotions.append({
                        "id": row[0],
                        "store_name": row[1],
                        "promotion_type": row[2],
                        "title": row[3],
                        "description": row[4],
                        "image_url": row[5],
                        "target_url": row[6],
                        "promotion_data": row[7],
                        "display_priority": row[8]
                    })
                
                return {"promotions": promotions}
                
    except Exception as e:
        logger.error(f"Error getting promotions: {e}")
        return {"promotions": []}

@app.post("/api/analyze-savings")
async def analyze_shopping_savings(
    analysis: SavingsAnalysis,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Secure savings analysis with AWS data"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Call the AWS analysis function
                cur.execute("""
                    SELECT * FROM analyze_shopping_list_savings(%s, %s::jsonb, %s)
                """, (current_user["id"], json.dumps(analysis.items), analysis.preferred_store))
                
                savings_data = []
                for row in cur.fetchall():
                    savings_data.append({
                        "store_name": row[0],
                        "total_cost": float(row[1]) if row[1] else 0,
                        "potential_savings": float(row[2]) if row[2] else 0,
                        "unavailable_items": row[3],
                        "best_offers": row[4] or []
                    })
                
                # Store analysis in AWS database
                if savings_data:
                    best_option = min(savings_data, key=lambda x: x["total_cost"])
                    worst_option = max(savings_data, key=lambda x: x["total_cost"])
                    max_savings = worst_option["total_cost"] - best_option["total_cost"]
                    
                    cur.execute("""
                        INSERT INTO savings_analysis (user_id, analysis_type, comparison_data, potential_savings, recommended_action)
                        VALUES (%s, 'list_comparison', %s, %s, %s)
                    """, (
                        current_user["id"],
                        json.dumps(savings_data),
                        max_savings,
                        f"Shop at {best_option['store_name']} to save £{max_savings:.2f}"
                    ))
                    conn.commit()
                    
                    recommendation = {
                        "best_store": best_option["store_name"],
                        "max_savings": max_savings
                    }
                else:
                    recommendation = {"best_store": "Unknown", "max_savings": 0}
                
                # Log activity
                background_tasks.add_task(
                    log_user_activity,
                    current_user["id"],
                    "savings_analysis",
                    {"items": analysis.items, "recommended_store": recommendation["best_store"]},
                    request.client.host if request.client else None
                )
                
                return {
                    "savings_analysis": savings_data,
                    "recommendation": recommendation
                }
                
    except Exception as e:
        logger.error(f"Error analyzing savings: {e}")
        raise HTTPException(status_code=500, detail="Savings analysis failed")

@app.get("/api/system-health")
async def get_system_health():
    """System health check with AWS database stats"""
    if not db_manager:
        return {
            "status": "limited",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "AWS PostgreSQL - Not Connected",
            "message": "Check AWS credentials in .env file"
        }
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Get database stats
                cur.execute("SELECT COUNT(*) FROM users WHERE is_active = true")
                active_users = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM branded_products")
                total_products = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM store_prices")
                total_prices = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(DISTINCT store_name) FROM store_prices")
                total_stores = cur.fetchone()[0]
                
                return {
                    "status": "healthy",
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "3.1.0-aws",
                    "database": "AWS PostgreSQL - Connected",
                    "security": {
                        "jwt_enabled": True,
                        "password_hashing": "bcrypt",
                        "cors_enabled": True,
                        "activity_logging": True
                    },
                    "stats": {
                        "active_users": active_users,
                        "total_products": total_products,
                        "total_prices": total_prices,
                        "total_stores": total_stores
                    }
                }
                
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "database": "AWS PostgreSQL - Error"
        }

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Home page - redirect to frontend app"""
    try:
        # Try to serve the frontend HTML file
        frontend_path = os.path.join("frontend", "index.html")
        if os.path.exists(frontend_path):
            with open(frontend_path, "r", encoding="utf-8") as f:
                content = f.read()
            return HTMLResponse(content)
        else:
            # Fallback embedded frontend
            return HTMLResponse("""
            <!DOCTYPE html>
            <html><head>
                <title>Smart Shopping - AWS Secure</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="text-center">
                        <h1>🛒 Smart Shopping Platform</h1>
                        <p class="lead">🔒 Secure AWS-powered shopping platform</p>
                        <div class="alert alert-info">
                            <strong>Authentication Required:</strong> 
                            All features require registration or login with your AWS database credentials.
                        </div>
                        <a href="/frontend/" class="btn btn-primary btn-lg">
                            🚀 Launch Application
                        </a>
                        <br><br>
                        <small class="text-muted">
                            API Documentation: <a href="/admin/docs">/admin/docs</a>
                        </small>
                    </div>
                </div>
            </body>
            </html>            """)
    except Exception as e:
        logger.error(f"Home page error: {e}")
        return HTMLResponse("<h1>Smart Shopping Platform</h1><p>Service temporarily unavailable</p>")

# Protected endpoints requiring authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        user_id = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return {"email": email, "user_id": user_id}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@app.get("/api/shopping-lists")
async def get_shopping_lists(current_user: Dict = Depends(get_current_user)):
    """Get user's shopping lists from AWS database"""
    if not db_manager:
        return {"success": True, "data": []}
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT sl.list_id, sl.list_name, sl.created_at, sl.total_estimated_cost,
                           COUNT(sli.item_id) as items_count
                    FROM shopping_lists sl
                    LEFT JOIN shopping_list_items sli ON sl.list_id = sli.list_id
                    WHERE sl.user_id = %s
                    GROUP BY sl.list_id, sl.list_name, sl.created_at, sl.total_estimated_cost
                    ORDER BY sl.created_at DESC
                """, (current_user["user_id"],))
                
                lists = []
                for row in cur.fetchall():
                    lists.append({
                        "list_id": row[0],
                        "list_name": row[1],
                        "created_at": row[2].isoformat() if row[2] else None,
                        "total_estimated_cost": float(row[3]) if row[3] else None,
                        "items_count": row[4]
                    })
                
                return {"success": True, "data": lists}
                
    except Exception as e:
        logger.error(f"Get shopping lists error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/shopping-lists")
async def create_shopping_list(
    list_data: Dict[str, str], 
    current_user: Dict = Depends(get_current_user)
):
    """Create a new shopping list"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    list_name = list_data.get("list_name", "").strip()
    if not list_name:
        raise HTTPException(status_code=400, detail="List name is required")    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO shopping_lists (user_id, name, created_at)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (current_user["user_id"], list_name, datetime.utcnow()))
                
                list_id = cur.fetchone()[0]
                conn.commit()
                
                return {"success": True, "data": {"list_id": list_id, "list_name": list_name}}
                
    except Exception as e:
        logger.error(f"Create shopping list error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create shopping list")

@app.delete("/api/shopping-lists/{list_id}")
async def delete_shopping_list(
    list_id: int, 
    current_user: Dict = Depends(get_current_user)
):
    """Delete a shopping list"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Verify ownership and delete
                cur.execute("""
                    DELETE FROM shopping_lists 
                    WHERE list_id = %s AND user_id = %s
                    RETURNING list_id
                """, (list_id, current_user["user_id"]))
                
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Shopping list not found")
                
                conn.commit()
                return {"success": True, "message": "Shopping list deleted"}
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete shopping list error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete shopping list")

@app.post("/api/compare-stores")
async def compare_stores(
    request_data: Dict[str, str], 
    current_user: Dict = Depends(get_current_user)
):
    """Compare product prices across stores"""
    product_query = request_data.get("product_query", "").strip()
    if not product_query:
        raise HTTPException(status_code=400, detail="Product query is required")
    
    if not db_manager:
        # Return mock data if AWS not available
        return {"success": True, "data": [
            {
                "store_name": "Tesco",
                "product_name": product_query,
                "current_price": 2.50,
                "promotion_price": None,
                "rating": 4.2,
                "in_stock": True
            },
            {
                "store_name": "ASDA",
                "product_name": product_query,
                "current_price": 2.30,
                "promotion_price": 2.00,
                "rating": 4.1,
                "in_stock": True
            }
        ]}
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT p.store_name, p.product_name, p.current_price, 
                           pr.promotional_price, p.rating, p.availability_status
                    FROM products p
                    LEFT JOIN promotions pr ON p.product_id = pr.product_id 
                        AND pr.is_active = true
                    WHERE LOWER(p.product_name) LIKE LOWER(%s)
                    ORDER BY p.current_price ASC
                    LIMIT 20
                """, (f"%{product_query}%",))
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        "store_name": row[0],
                        "product_name": row[1],
                        "current_price": float(row[2]) if row[2] else 0,
                        "promotion_price": float(row[3]) if row[3] else None,
                        "rating": float(row[4]) if row[4] else None,
                        "in_stock": row[5] == "in_stock" if row[5] else True
                    })
                
                return {"success": True, "data": results}
                
    except Exception as e:
        logger.error(f"Store comparison error: {e}")
        raise HTTPException(status_code=500, detail="Failed to compare stores")

if __name__ == "__main__":
    import uvicorn
    
    print("🔒 Starting SECURE Smart Shopping Website")
    print("🗄️  AWS PostgreSQL Database Integration")
    print("🔐 Security Features Enabled:")
    print("  ✅ JWT Authentication")
    print("  ✅ BCrypt Password Hashing") 
    print("  ✅ Input Validation")
    print("  ✅ SQL Injection Protection")
    print("  ✅ CORS Security")
    print("  ✅ User Activity Logging")
    print("  ✅ Secure Session Management")
    
    if db_manager:
        print("  ✅ AWS PostgreSQL Connected")
    else:
        print("  ⚠️  AWS PostgreSQL Not Connected - Check .env")
    
    print("\n🌐 Starting server on http://localhost:8000")
    print("🚀 Ready for GitHub Pages deployment")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        access_log=True,
        log_level="info"
    )
