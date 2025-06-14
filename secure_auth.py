#!/usr/bin/env python3
"""
Secure Authentication System for Smart Shopping Website
Implements proper password hashing, JWT tokens, and data protection
"""

import os
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
import hashlib
import logging

# Security configuration
security = HTTPBearer()
logger = logging.getLogger(__name__)

class SecurityConfig:
    """Security configuration with proper defaults"""
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_SPECIAL_CHARS = True
    REQUIRE_NUMBERS = True
    REQUIRE_UPPERCASE = True
    
    # Rate limiting (requests per minute)
    LOGIN_RATE_LIMIT = 5
    REGISTRATION_RATE_LIMIT = 3
    
    # Session security
    SESSION_TIMEOUT_MINUTES = 30
    MAX_SESSIONS_PER_USER = 3
    
    # Data encryption
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", secrets.token_urlsafe(32))

class PasswordValidator:
    """Validate password strength"""
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validate password meets security requirements"""
        if len(password) < SecurityConfig.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {SecurityConfig.MIN_PASSWORD_LENGTH} characters"
        
        if SecurityConfig.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if SecurityConfig.REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        if SecurityConfig.REQUIRE_SPECIAL_CHARS and not any(c in "!@#$%^&*()_+-=" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is valid"

class SecureAuth:
    """Secure authentication handler"""
    
    def __init__(self):
        self.failed_attempts = {}  # Track failed login attempts
        self.active_sessions = {}  # Track active user sessions
    
    def hash_password(self, password: str) -> str:
        """Securely hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Create secure JWT token"""
        payload = {
            "user_id": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(hours=SecurityConfig.JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16)  # Unique token ID
        }
        
        return jwt.encode(payload, SecurityConfig.JWT_SECRET_KEY, algorithm=SecurityConfig.JWT_ALGORITHM)
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SecurityConfig.JWT_SECRET_KEY, algorithms=[SecurityConfig.JWT_ALGORITHM])
            
            # Check if token is blacklisted (implement token blacklist in production)
            
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    def check_rate_limit(self, identifier: str, limit: int) -> bool:
        """Check if request is within rate limit"""
        now = datetime.now()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        # Remove old attempts (older than 1 minute)
        self.failed_attempts[identifier] = [
            attempt for attempt in self.failed_attempts[identifier]
            if now - attempt < timedelta(minutes=1)
        ]
        
        return len(self.failed_attempts[identifier]) < limit
    
    def record_failed_attempt(self, identifier: str):
        """Record failed login attempt"""
        now = datetime.now()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        self.failed_attempts[identifier].append(now)
        logger.warning(f"Failed login attempt for: {identifier}")
    
    def register_user(self, username: str, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """Securely register new user"""
        
        # Validate input
        if not username or len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters"
            )
        
        if not email or "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid email address required"
            )
        
        # Validate password
        is_valid, message = PasswordValidator.validate_password(password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Check rate limiting
        client_ip = "127.0.0.1"  # Get from request in production
        if not self.check_rate_limit(f"register_{client_ip}", SecurityConfig.REGISTRATION_RATE_LIMIT):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many registration attempts. Please try again later."
            )
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Store in database (sanitized)
        conn = sqlite3.connect('products.db')
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                failed_login_attempts INTEGER DEFAULT 0,
                account_locked_until TIMESTAMP
            )
        """)
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # Log registration (without sensitive data)
            logger.info(f"New user registered: {username} (ID: {user_id})")
            
            return {
                "id": user_id,
                "username": username,
                "email": email,
                "full_name": full_name,
                "created_at": datetime.now().isoformat()
            }
            
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Registration failed"
                )
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str, client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """Securely authenticate user"""
        
        # Check rate limiting
        if not self.check_rate_limit(f"login_{client_ip}", SecurityConfig.LOGIN_RATE_LIMIT):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later."
            )
        
        if not self.check_rate_limit(f"login_{username}", 3):  # Per username limit
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Account temporarily locked due to failed attempts"
            )
        
        # Get user from database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, full_name, is_active, 
                   failed_login_attempts, account_locked_until
            FROM users 
            WHERE username = ? OR email = ?
        """, (username, username))
        
        user_row = cursor.fetchone()
        conn.close()
        
        if not user_row:
            self.record_failed_attempt(f"login_{client_ip}")
            self.record_failed_attempt(f"login_{username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        user_id, username, email, password_hash, full_name, is_active, failed_attempts, locked_until = user_row
        
        # Check if account is active
        if not is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Check if account is locked
        if locked_until and datetime.now() < datetime.fromisoformat(locked_until):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is temporarily locked"
            )
        
        # Verify password
        if not self.verify_password(password, password_hash):
            self.record_failed_attempt(f"login_{client_ip}")
            self.record_failed_attempt(f"login_{username}")
            
            # Update failed attempts in database
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET failed_login_attempts = failed_login_attempts + 1,
                    account_locked_until = CASE 
                        WHEN failed_login_attempts >= 5 THEN datetime('now', '+30 minutes')
                        ELSE account_locked_until
                    END
                WHERE id = ?
            """, (user_id,))
            conn.commit()
            conn.close()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Successful login - reset failed attempts
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET failed_login_attempts = 0, 
                account_locked_until = NULL,
                last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))
        conn.commit()
        conn.close()
        
        # Log successful login
        logger.info(f"Successful login: {username} from {client_ip}")
        
        return {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name
        }

# Initialize secure auth
secure_auth = SecureAuth()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    
    token = credentials.credentials
    payload = secure_auth.verify_jwt_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for logging/storage"""
    return hashlib.sha256(data.encode()).hexdigest()[:16]

def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent injection"""
    if not data:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
    for char in dangerous_chars:
        data = data.replace(char, '')
    
    return data.strip()

# Data protection utilities
class DataProtection:
    """Utilities for protecting sensitive data"""
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email for display"""
        if '@' not in email:
            return email
        
        local, domain = email.split('@')
        if len(local) <= 2:
            return f"{local[0]}***@{domain}"
        
        return f"{local[:2]}***@{domain}"
    
    @staticmethod
    def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive fields in data"""
        masked = data.copy()
        
        sensitive_fields = ['password', 'password_hash', 'credit_card', 'ssn']
        
        for field in sensitive_fields:
            if field in masked:
                masked[field] = "***MASKED***"
        
        if 'email' in masked:
            masked['email'] = DataProtection.mask_email(masked['email'])
        
        return masked

# Export the secure authentication functions
def create_access_token(user_data: Dict[str, Any]) -> str:
    """Create JWT access token"""
    return secure_auth.create_jwt_token(user_data)

def get_password_hash(password: str) -> str:
    """Hash password securely"""
    return secure_auth.hash_password(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return secure_auth.verify_password(password, hashed)
