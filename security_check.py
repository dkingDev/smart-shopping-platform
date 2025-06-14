#!/usr/bin/env python3
"""
Final Security Check - Verify no sensitive data will be leaked to GitHub
"""

import os
import re
from pathlib import Path

def check_sensitive_patterns():
    """Check for sensitive patterns in files that might be committed"""
    
    sensitive_patterns = [
        (r'password\s*[=:]\s*["\']?([^"\'\s]+)', 'Password found'),
        (r'secret\s*[=:]\s*["\']?([^"\'\s]+)', 'Secret found'),
        (r'key\s*[=:]\s*["\']?([^"\'\s]+)', 'API key found'),
        (r'AWS_DB_PASSWORD', 'AWS DB password reference'),
        (r'AdminTakeo', 'Database username'),
        (r'supermarket-db\.cbu8qc0uk2re\.eu-north-1\.rds\.amazonaws\.com', 'Database host'),
    ]
    
    # Files to check (excluding .env files which are gitignored)
    files_to_check = [
        'secure_aws_shopping.py',
        'run_local.py', 
        'run_production.py',
        'frontend/js/app.js',
        'frontend/index.html',
        'README.md',
        'requirements.txt'
    ]
    
    issues = []
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern, description in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"{file_path}: {description}")
        except Exception as e:
            print(f"Warning: Could not check {file_path}: {e}")
    
    return issues

def check_gitignore_coverage():
    """Verify .gitignore covers all sensitive files"""
    
    # Check if .env files are ignored
    env_files = ['.env', '.env.production']
    ignored_properly = True
    
    for env_file in env_files:
        if os.path.exists(env_file):
            # Check if it would be committed
            result = os.system(f'git check-ignore {env_file} > nul 2>&1')
            if result != 0:  # 0 means ignored, non-zero means not ignored
                print(f"WARNING: {env_file} is NOT ignored by git!")
                ignored_properly = False
    
    return ignored_properly

def main():
    """Run final security check"""
    
    print("🔒 Final Security Check for GitHub Deployment")
    print("=" * 50)
    
    # Check for sensitive patterns in code
    issues = check_sensitive_patterns()
    
    if issues:
        print("❌ SECURITY ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n⚠️  DO NOT COMMIT until these are fixed!")
        return False
    else:
        print("✅ No sensitive patterns found in public files")
    
    # Check gitignore coverage
    if check_gitignore_coverage():
        print("✅ Environment files properly ignored")
    else:
        print("❌ Environment files not properly ignored!")
        return False
    
    print("\n🎯 Files that will be public:")
    public_files = [
        'secure_aws_shopping.py',
        'run_local.py',
        'run_production.py', 
        'frontend/',
        'README.md',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    for file_path in public_files:
        if os.path.exists(file_path):
            print(f"  📄 {file_path}")
    
    print("\n🔒 Files that will be private (gitignored):")
    private_files = ['.env', '.env.production', 'scripts/']
    for file_path in private_files:
        if os.path.exists(file_path):
            print(f"  🔐 {file_path}")
    
    print("\n✅ SECURITY CHECK PASSED")
    print("🚀 Safe to deploy to GitHub!")
    
    return True

if __name__ == "__main__":
    main()
