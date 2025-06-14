#!/usr/bin/env python3
"""
Final security check for deployment packages
Only flags actual proprietary content, not placeholder text
"""

import zipfile
from pathlib import Path

def check_package_security(zip_path):
    """Check deployment package for proprietary content"""
    
    print(f"🔍 Security check: {zip_path}")
    
    # Files that should NOT be in public deployment
    forbidden_files = [
        'universal_smart_crawler.py',
        'processed_price_history.csv',
        'categories_baby_toddler.json',
        'remove_morrisons_products.py',
        'scripts/',
        'test_'
    ]
    
    # Content that should NOT be in public deployment  
    forbidden_content = [
        'derek.j.king@live.com',
        'Alex8nd3r!',
        'universal_smart_crawler',
        'processed_price_history',
        'categories_baby_toddler'
    ]
    
    violations = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Check filenames
            for file_info in zf.filelist:
                filename = file_info.filename
                for forbidden in forbidden_files:
                    if forbidden in filename:
                        violations.append(f"Forbidden file: {filename}")
                
                # Check file content if it's a text file
                if filename.endswith(('.py', '.js', '.html', '.md', '.txt', '.sql', '.json')):
                    try:
                        content = zf.read(file_info.filename).decode('utf-8', errors='ignore')
                        for forbidden in forbidden_content:
                            if forbidden in content:
                                violations.append(f"Forbidden content '{forbidden}' in {filename}")
                    except:
                        pass  # Skip binary or unreadable files
        
        if violations:
            print(f"  ❌ {len(violations)} violations found:")
            for violation in violations:
                print(f"    - {violation}")
            return False
        else:
            print(f"  ✅ Clean - no proprietary content found")
            return True
            
    except Exception as e:
        print(f"  ❌ Error checking {zip_path}: {e}")
        return False

def main():
    """Check all deployment packages"""
    
    print("🔒 Final Security Check for Public Deployment")
    print("=" * 50)
    
    packages = [
        "github-pages-public-only.zip",
        "heroku-backend-public-only.zip"
    ]
    
    all_clean = True
    
    for package in packages:
        if Path(package).exists():
            is_clean = check_package_security(package)
            all_clean = all_clean and is_clean
        else:
            print(f"⚠️  Package not found: {package}")
            all_clean = False
    
    print("\n" + "=" * 50)
    if all_clean:
        print("🎉 ALL PACKAGES ARE SECURE FOR PUBLIC DEPLOYMENT!")
        print("✅ No proprietary content detected")
        print("✅ Ready for GitHub and Heroku deployment")
        print("\n📋 Deployment ready:")
        print("  1. Upload heroku-backend-public-only.zip to Heroku")
        print("  2. Upload github-pages-public-only.zip to GitHub")
        print("  3. Set environment variables in Heroku")
        print("  4. Enable GitHub Pages")
    else:
        print("❌ VIOLATIONS FOUND - DO NOT DEPLOY")

if __name__ == "__main__":
    main()
