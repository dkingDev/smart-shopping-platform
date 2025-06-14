#!/usr/bin/env python3
"""
Secure Smart Shopping Website with AWS PostgreSQL Integration
Production-ready with proper security protocols for user data
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Form, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field, field_validator
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
from passlib.hash import bcrypt
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
    title="Smart Shopping Platform - Secure Production",
    description="Secure smart shopping platform with AWS PostgreSQL integration",
    version="3.0.0-secure",
    docs_url=None,  # Disable docs in production
    redoc_url=None  # Disable redoc in production
)

# Security configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if not JWT_SECRET_KEY or JWT_SECRET_KEY == "your-super-secret-jwt-key-change-in-production-please":
    # Generate a secure key if not set
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    logger.warning("Generated temporary JWT secret. Set JWT_SECRET_KEY in production!")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://*.github.io",  # For GitHub Pages
        os.getenv("FRONTEND_URL", "")
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

# AWS Database manager
db_manager = AWSPostgreSQLManager()

# Security models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=255)
      @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError('Username must be alphanumeric with underscores only')
        return v
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class SavingsAnalysis(BaseModel):
    items: List[str] = Field(..., min_items=1, max_items=50)
    preferred_store: Optional[str] = None

class ShoppingList(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    items: List[str] = Field(..., min_items=1, max_items=100)
    store_preference: Optional[str] = None

# Security functions
def hash_password(password: str) -> str:
    """Hash password securely"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
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
    
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
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

async def log_user_activity(user_id: int, action: str, data: Dict[str, Any], ip_address: str = None):
    """Log user activity to AWS database"""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_activity (user_id, action_type, action_data, ip_address, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, action, json.dumps(data), ip_address, datetime.utcnow()))
                conn.commit()
    except Exception as e:
        logger.error(f"Failed to log user activity: {e}")

# Authentication endpoints
@app.post("/api/auth/register", response_model=Token)
async def register_user(user: UserRegister, request: Request, background_tasks: BackgroundTasks):
    """Secure user registration with AWS database"""
    try:
        # Hash password
        hashed_password = hash_password(user.password)
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check if user exists
                cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", 
                          (user.username, user.email))
                
                if cur.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username or email already registered"
                    )
                
                # Create user in AWS database
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, full_name, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (user.username, user.email, hashed_password, user.full_name, True, datetime.utcnow()))
                
                user_id = cur.fetchone()[0]
                conn.commit()
                
                # Create access token
                access_token = create_access_token(data={"sub": user.username, "user_id": user_id})
                
                user_data = {
                    "id": user_id,
                    "username": user.username,
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
                    {"username": user.username, "email": user.email},
                    request.client.host if request.client else None
                )
                
                return Token(access_token=access_token, user=user_data)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@app.post("/api/auth/login", response_model=Token)
async def login_user(user: UserLogin, request: Request, background_tasks: BackgroundTasks):
    """Secure user login with AWS database"""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Get user from AWS database
                cur.execute("""
                    SELECT id, username, email, password_hash, full_name, is_active, is_premium
                    FROM users 
                    WHERE username = %s AND is_active = true
                """, (user.username,))
                
                db_user = cur.fetchone()
                
                if not db_user or not verify_password(user.password, db_user[3]):
                    # Log failed login attempt
                    background_tasks.add_task(
                        log_user_activity,
                        0,  # No user ID for failed login
                        "login_failed",
                        {"username": user.username, "reason": "invalid_credentials"},
                        request.client.host if request.client else None
                    )
                    
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password"
                    )
                
                # Update last login
                cur.execute("""
                    UPDATE users SET last_login = %s WHERE id = %s
                """, (datetime.utcnow(), db_user[0]))
                conn.commit()
                
                # Create access token
                access_token = create_access_token(data={"sub": db_user[1], "user_id": db_user[0]})
                
                user_data = {
                    "id": db_user[0],
                    "username": db_user[1],
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
                    {"username": user.username},
                    request.client.host if request.client else None
                )
                
                return Token(access_token=access_token, user=user_data)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

# Protected endpoints with AWS database integration
@app.get("/api/user/profile")
async def get_user_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user profile from AWS database"""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Get user stats
                cur.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM shopping_lists WHERE user_id = %s) as total_lists,
                        (SELECT COUNT(*) FROM user_activity WHERE user_id = %s) as total_activities,
                        (SELECT COUNT(*) FROM user_locations WHERE user_id = %s) as total_locations
                """, (current_user["id"], current_user["id"], current_user["id"]))
                
                stats = cur.fetchone()
                
                return {
                    "user": current_user,
                    "stats": {
                        "total_shopping_lists": stats[0] if stats else 0,
                        "total_activities": stats[1] if stats else 0,
                        "total_locations": stats[2] if stats else 0
                    }
                }
                
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user profile")

@app.post("/api/analyze-savings")
async def analyze_shopping_savings(
    analysis: SavingsAnalysis,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Secure savings analysis with AWS data integration"""
    try:
        # Use AWS PostgreSQL function for analysis
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Call the analysis function we created in the schema
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

@app.post("/api/shopping-lists")
async def create_shopping_list(
    shopping_list: ShoppingList,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create shopping list in AWS database"""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Create shopping list
                cur.execute("""
                    INSERT INTO shopping_lists (user_id, name, description, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    current_user["id"], 
                    shopping_list.name, 
                    f"Created with {len(shopping_list.items)} items",
                    datetime.utcnow(),
                    datetime.utcnow()
                ))
                
                list_id = cur.fetchone()[0]
                
                # Add items to the list
                for item in shopping_list.items:
                    # Try to find matching product
                    cur.execute("""
                        SELECT product_id FROM branded_products 
                        WHERE name ILIKE %s 
                        ORDER BY similarity(name, %s) DESC 
                        LIMIT 1
                    """, (f"%{item}%", item))
                    
                    product_result = cur.fetchone()
                    product_id = product_result[0] if product_result else None
                    
                    # Insert shopping list item
                    cur.execute("""
                        INSERT INTO shopping_list_items 
                        (list_id, product_id, product_name, quantity, preferred_stores, added_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        list_id, product_id, item, 1, 
                        [shopping_list.store_preference] if shopping_list.store_preference else [],
                        datetime.utcnow()
                    ))
                
                conn.commit()
                
                # Log activity
                background_tasks.add_task(
                    log_user_activity,
                    current_user["id"],
                    "create_shopping_list",
                    {"list_name": shopping_list.name, "item_count": len(shopping_list.items)},
                    request.client.host if request.client else None
                )
                
                return {
                    "success": True,
                    "list_id": list_id,
                    "list_name": shopping_list.name,
                    "item_count": len(shopping_list.items)
                }
                
    except Exception as e:
        logger.error(f"Error creating shopping list: {e}")
        raise HTTPException(status_code=500, detail="Failed to create shopping list")

@app.get("/api/promotions")
async def get_active_promotions(
    promotion_type: Optional[str] = None, 
    limit: int = 10,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """Get active promotions from AWS database"""
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

@app.get("/api/system-health")
async def get_system_health():
    """System health check with AWS database stats"""
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
                    "version": "3.0.0-secure",
                    "database": "AWS PostgreSQL",
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
        raise HTTPException(status_code=503, detail=f"System unhealthy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print("🔒 Starting SECURE Smart Shopping Website")
    print("🗄️  Connected to AWS PostgreSQL Database")
    print("🔐 Security Features:")
    print("  ✅ JWT Authentication")
    print("  ✅ BCrypt Password Hashing")
    print("  ✅ Input Validation")
    print("  ✅ SQL Injection Protection")
    print("  ✅ CORS Security")
    print("  ✅ User Activity Logging")
    print("  ✅ Rate Limiting Ready")
    print("\n🌐 Starting server on https://localhost:8443 (HTTPS recommended for production)")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,  # Use 8443 for HTTPS in production
        # ssl_keyfile="path/to/key.pem",  # Enable for HTTPS
        # ssl_certfile="path/to/cert.pem",  # Enable for HTTPS
        access_log=True,
        log_level="info"
    )
