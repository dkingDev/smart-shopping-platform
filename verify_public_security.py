#!/usr/bin/env python3
"""
Security verification for public deployment packages
Ensures no proprietary or sensitive content is included
"""

import zipfile
import re
from pathlib import Path

def scan_file_content(file_path, content):
    """Scan file content for sensitive patterns"""
      # Patterns that indicate proprietary or sensitive content
    sensitive_patterns = [
        r'universal.*smart.*crawler',
        r'scripts/.*crawler',
        r'processed_price_history',
        r'categories_.*\.json',
        r'populate_aws_demo_data',
        r'production_setup\.py',
        r'derek\.j\.king@live\.com.*Alex8nd3r!',
        r'master_branded_products\.csv',
        r'brands_catalog\.json'
    ]
    
    violations = []
    content_lower = content.lower()
    
    for pattern in sensitive_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        if matches:
            violations.append(f"  ⚠️  Pattern '{pattern}' found: {matches}")
    
    return violations

def verify_deployment_package(zip_path):
    """Verify a deployment package contains only public code"""
    
    print(f"🔍 Scanning: {zip_path}")
    print("="*50)
    
    violations = []
    file_count = 0
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for file_info in zf.filelist:
                if not file_info.is_dir():
                    file_count += 1
                    print(f"📄 {file_info.filename}")
                    
                    # Check filename for sensitive patterns
                    if any(pattern in file_info.filename.lower() for pattern in 
                          ['crawler', 'scraper', 'secret', 'password', 'key', 'catalog', 'brand']):
                        violations.append(f"  ⚠️  Sensitive filename: {file_info.filename}")
                    
                    # Read and scan file content
                    try:
                        content = zf.read(file_info.filename).decode('utf-8', errors='ignore')
                        file_violations = scan_file_content(file_info.filename, content)
                        violations.extend(file_violations)
                    except Exception as e:
                        print(f"    (Binary file or read error: {e})")
        
        print(f"\\n📊 Summary for {zip_path}:")
        print(f"  Files scanned: {file_count}")
        
        if violations:
            print(f"  ❌ Security violations found: {len(violations)}")
            for violation in violations:
                print(violation)
            return False
        else:
            print(f"  ✅ Security scan passed - no violations found")
            return True
            
    except Exception as e:
        print(f"❌ Error scanning {zip_path}: {e}")
        return False

def verify_all_packages():
    """Verify all deployment packages"""
    
    print("🔒 Security Verification for Public Deployment Packages")
    print("="*60)
    print()
    
    packages = [
        "github-pages-public-only.zip",
        "heroku-backend-public-only.zip"
    ]
    
    all_secure = True
    
    for package in packages:
        if Path(package).exists():
            is_secure = verify_deployment_package(package)
            all_secure = all_secure and is_secure
            print()
        else:
            print(f"⚠️  Package not found: {package}")
            all_secure = False
    
    print("🎯 Final Security Assessment:")
    print("="*40)
    
    if all_secure:
        print("🎉 ALL PACKAGES SECURE FOR PUBLIC DEPLOYMENT!")
        print("✅ No proprietary content detected")
        print("✅ No sensitive credentials detected") 
        print("✅ No crawler code detected")
        print("✅ Ready for public release")
        print()
        print("📋 Deployment checklist:")
        print("  1. ✅ Upload heroku-backend-public-only.zip to Heroku")
        print("  2. ✅ Set environment variables in Heroku (DATABASE_URL, JWT_SECRET_KEY)")
        print("  3. ✅ Upload github-pages-public-only.zip to GitHub repository")
        print("  4. ✅ Enable GitHub Pages")
        print("  5. ✅ Update API URL in frontend to point to Heroku backend")
    else:
        print("❌ SECURITY VIOLATIONS DETECTED!")
        print("⚠️  DO NOT DEPLOY UNTIL ISSUES ARE RESOLVED")
        print("🔧 Review and fix violations above")

if __name__ == "__main__":
    verify_all_packages()
