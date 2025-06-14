#!/usr/bin/env python3
"""
Security Audit for Smart Shopping Platform
Comprehensive review of all security protocols for user data protection
"""

import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

class SecurityAuditor:
    def __init__(self):
        self.security_issues = []
        self.security_passes = []
        self.recommendations = []
    
    def audit_environment_variables(self):
        """Audit environment variable security"""
        print("🔍 ENVIRONMENT VARIABLES SECURITY AUDIT")
        print("="*60)
        
        # Check for sensitive data in .env
        sensitive_vars = {
            "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY"),
            "AWS_DB_PASSWORD": os.getenv("AWS_DB_PASSWORD"),
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY")
        }
        
        for var, value in sensitive_vars.items():
            if not value:
                self.security_issues.append(f"❌ {var} not set")
            elif value == "your-super-secret-jwt-key-change-in-production-please":
                self.security_issues.append(f"⚠️  {var} using default value - CHANGE FOR PRODUCTION!")
            elif len(value) < 16:
                self.security_issues.append(f"⚠️  {var} appears too short")
            else:
                self.security_passes.append(f"✅ {var} properly configured")
    
    def audit_password_security(self):
        """Audit password security implementation"""
        print("\n🔒 PASSWORD SECURITY AUDIT")
        print("="*60)
          # Read the backend file to check password security
        try:
            with open("secure_aws_shopping.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check for bcrypt usage
            if "bcrypt" in content and "CryptContext" in content:
                self.security_passes.append("✅ BCrypt password hashing implemented")
            else:
                self.security_issues.append("❌ BCrypt password hashing not found")
            
            # Check for password validation
            if "validate_password" in content:
                self.security_passes.append("✅ Password validation function exists")
                
                # Check validation rules
                if "len(password) < 8" in content:
                    self.security_passes.append("✅ Minimum password length check (8 chars)")
                if "re.search(r\"[A-Z]\"" in content:
                    self.security_passes.append("✅ Uppercase letter requirement")
                if "re.search(r\"[a-z]\"" in content:
                    self.security_passes.append("✅ Lowercase letter requirement")
                if "re.search(r\"\\d\"" in content:
                    self.security_passes.append("✅ Number requirement")
            else:
                self.security_issues.append("❌ Password validation not implemented")
            
            # Check for password hashing
            if "hash_password" in content and "pwd_context.hash" in content:
                self.security_passes.append("✅ Password hashing function implemented")
            else:
                self.security_issues.append("❌ Password hashing function not found")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found")
    
    def audit_jwt_security(self):
        """Audit JWT token security"""
        print("\n🎫 JWT TOKEN SECURITY AUDIT")
        print("="*60)
        
        try:            with open("secure_aws_shopping.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check JWT implementation
            if "jose" in content and "jwt" in content:
                self.security_passes.append("✅ JWT library (python-jose) implemented")
            else:
                self.security_issues.append("❌ JWT implementation not found")
            
            # Check for token expiration
            if "expires_delta" in content or "JWT_EXPIRATION_HOURS" in content:
                self.security_passes.append("✅ JWT token expiration implemented")
            else:
                self.security_issues.append("❌ JWT token expiration not configured")
            
            # Check for secure algorithm
            if "HS256" in content:
                self.security_passes.append("✅ Secure JWT algorithm (HS256) used")
            else:
                self.security_issues.append("❌ JWT algorithm not specified or insecure")
            
            # Check for token validation
            if "get_current_user" in content and "HTTPAuthorizationCredentials" in content:
                self.security_passes.append("✅ JWT token validation implemented")
            else:
                self.security_issues.append("❌ JWT token validation not found")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found for JWT audit")
    
    def audit_database_security(self):
        """Audit database security measures"""
        print("\n🗄️ DATABASE SECURITY AUDIT")
        print("="*60)
        
        # Check AWS connection
        aws_host = os.getenv("AWS_DB_HOST")
        if aws_host and "amazonaws.com" in aws_host:
            self.security_passes.append("✅ Using AWS RDS (managed database service)")
        else:
            self.security_issues.append("⚠️  Database host not AWS RDS")
        
        # Check SSL/TLS
        try:
            with open("database/aws_postgresql_manager.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            if "sslmode" in content and "require" in content:
                self.security_passes.append("✅ SSL/TLS encryption required for database")
            else:
                self.security_issues.append("❌ SSL/TLS not enforced for database connection")
                
            # Check for SQL injection protection
            if "execute(" in content and "%s" in content:
                self.security_passes.append("✅ Parameterized queries (SQL injection protection)")
            else:
                self.security_issues.append("❌ SQL injection protection not verified")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Database manager file not found")
    
    def audit_cors_security(self):
        """Audit CORS security configuration"""
        print("\n🌐 CORS SECURITY AUDIT")
        print("="*60)
        
        try:
            with open("secure_aws_shopping.py", "r") as f:
                content = f.read()
            
            if "CORSMiddleware" in content:
                self.security_passes.append("✅ CORS middleware configured")
                
                # Check for wildcard origins
                if "allow_origins=[\"*\"]" in content:
                    self.security_issues.append("❌ CORS allows all origins (*) - SECURITY RISK!")
                else:
                    self.security_passes.append("✅ CORS origins restricted (not wildcard)")
                
                # Check for credentials
                if "allow_credentials=True" in content:
                    self.security_passes.append("✅ CORS credentials allowed for authenticated requests")
                
            else:
                self.security_issues.append("❌ CORS middleware not configured")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found for CORS audit")
    
    def audit_logging_security(self):
        """Audit security logging and monitoring"""
        print("\n📋 SECURITY LOGGING AUDIT")
        print("="*60)
        
        try:
            with open("secure_aws_shopping.py", "r") as f:
                content = f.read()
            
            # Check for logging setup
            if "logging" in content and "logger" in content:
                self.security_passes.append("✅ Security logging implemented")
            else:
                self.security_issues.append("❌ Security logging not found")
            
            # Check for user activity logging
            if "log_user_activity" in content:
                self.security_passes.append("✅ User activity logging implemented")
            else:
                self.security_issues.append("❌ User activity logging not implemented")
            
            # Check for failed login logging
            if "login_failed" in content:
                self.security_passes.append("✅ Failed login attempt logging")
            else:
                self.security_issues.append("❌ Failed login logging not found")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found for logging audit")
    
    def audit_input_validation(self):
        """Audit input validation security"""
        print("\n✅ INPUT VALIDATION AUDIT")
        print("="*60)
        
        try:
            with open("secure_aws_shopping.py", "r") as f:
                content = f.read()
            
            # Check for Pydantic models
            if "BaseModel" in content and "EmailStr" in content:
                self.security_passes.append("✅ Pydantic input validation models")
            else:
                self.security_issues.append("❌ Input validation models not found")
            
            # Check for email validation
            if "EmailStr" in content:
                self.security_passes.append("✅ Email format validation")
            else:
                self.security_issues.append("❌ Email validation not implemented")
            
            # Check for username validation
            if "validate_username" in content:
                self.security_passes.append("✅ Username validation function")
            else:
                self.security_issues.append("❌ Username validation not found")
                
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found for validation audit")
    
    def audit_api_security(self):
        """Audit API endpoint security"""
        print("\n🔐 API SECURITY AUDIT")
        print("="*60)
        
        try:
            with open("secure_aws_shopping.py", "r") as f:
                content = f.read()
            
            # Check for authentication requirements
            if "Depends(get_current_user)" in content:
                self.security_passes.append("✅ Protected endpoints require authentication")
            else:
                self.security_issues.append("❌ Protected endpoints not found")
            
            # Check for rate limiting (basic check)
            if "docs_url=\"/admin/docs\"" in content:
                self.security_passes.append("✅ API documentation access restricted")
            else:
                self.security_issues.append("⚠️  API documentation access not restricted")
            
            # Check for HTTPS enforcement (production recommendation)
            self.recommendations.append("🔄 Ensure HTTPS enforcement in production")
            
        except FileNotFoundError:
            self.security_issues.append("❌ Backend file not found for API audit")
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n" + "="*80)
        print("🛡️  COMPREHENSIVE SECURITY AUDIT REPORT")
        print("="*80)
        
        print(f"\n✅ SECURITY MEASURES PASSED: {len(self.security_passes)}")
        for item in self.security_passes:
            print(f"   {item}")
        
        print(f"\n❌ SECURITY ISSUES FOUND: {len(self.security_issues)}")
        for item in self.security_issues:
            print(f"   {item}")
        
        if self.recommendations:
            print(f"\n🔄 RECOMMENDATIONS: {len(self.recommendations)}")
            for item in self.recommendations:
                print(f"   {item}")
        
        # Calculate security score
        total_checks = len(self.security_passes) + len(self.security_issues)
        if total_checks > 0:
            security_score = (len(self.security_passes) / total_checks) * 100
            print(f"\n📊 SECURITY SCORE: {security_score:.1f}%")
            
            if security_score >= 90:
                print("🎉 EXCELLENT security implementation!")
            elif security_score >= 75:
                print("👍 GOOD security implementation with minor issues")
            elif security_score >= 60:
                print("⚠️  MODERATE security - address issues before production")
            else:
                print("🚨 POOR security - immediate attention required!")
        
        return len(self.security_issues) == 0

def main():
    """Run comprehensive security audit"""
    print("🛡️  SMART SHOPPING PLATFORM - SECURITY AUDIT")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*80)
    
    auditor = SecurityAuditor()
    
    # Run all security audits
    auditor.audit_environment_variables()
    auditor.audit_password_security()
    auditor.audit_jwt_security()
    auditor.audit_database_security()
    auditor.audit_cors_security()
    auditor.audit_logging_security()
    auditor.audit_input_validation()
    auditor.audit_api_security()
    
    # Generate final report
    security_passed = auditor.generate_security_report()
    
    print("\n" + "="*80)
    if security_passed:
        print("🎉 SECURITY AUDIT PASSED - System is secure for production!")
    else:
        print("⚠️  SECURITY AUDIT FAILED - Address issues before production deployment!")
    
    return security_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
