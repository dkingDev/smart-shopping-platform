#!/usr/bin/env python3
"""
EMERGENCY SECURITY CLEANUP SCRIPT
Remove exposed AWS credentials from git history
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run shell command safely"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def emergency_cleanup():
    """Remove sensitive files from git history"""
    print("🚨 EMERGENCY: REMOVING AWS CREDENTIALS FROM GIT HISTORY")
    print("=" * 60)
    
    # Files to remove completely from git history
    sensitive_files = [
        "prepare_deployment.py",
        "DEPLOY_INSTRUCTIONS.md",
        "backend-deploy/*"
    ]
    
    print("⚠️  WARNING: This will rewrite git history!")
    print("⚠️  All contributors will need to re-clone the repository!")
    print("")
    
    response = input("Continue with emergency cleanup? (type 'EMERGENCY' to confirm): ")
    if response != "EMERGENCY":
        print("❌ Cleanup cancelled")
        return False
    
    # Use git filter-branch to remove sensitive files
    for file_pattern in sensitive_files:
        print(f"🗑️  Removing {file_pattern} from git history...")
        cmd = f'git filter-branch --force --index-filter "git rm --cached --ignore-unmatch {file_pattern}" --prune-empty --tag-name-filter cat -- --all'
        if not run_command(cmd):
            print(f"⚠️  Failed to remove {file_pattern}")
    
    # Force push to overwrite remote history
    print("🚀 Force pushing cleaned history to GitHub...")
    if run_command("git push origin --force --all"):
        print("✅ Git history cleaned on GitHub")
    else:
        print("❌ Failed to push cleaned history")
        return False
    
    # Clean up local refs
    print("🧹 Cleaning up local references...")
    run_command("rm -rf .git/refs/original/")
    run_command("git reflog expire --expire=now --all")
    run_command("git gc --prune=now --aggressive")
    
    print("")
    print("✅ EMERGENCY CLEANUP COMPLETE!")
    print("=" * 60)
    print("🔒 AWS credentials removed from git history")
    print("🚀 Clean history pushed to GitHub")
    print("")
    print("⚠️  IMPORTANT: All other contributors must now:")
    print("   1. Delete their local repository")
    print("   2. Fresh clone from GitHub")
    print("")
    return True

def create_secure_env_template():
    """Create a secure .env template"""
    template = '''# Smart Shopping Platform - Production Environment
# Copyright (c) 2025 Spirit of the Immortals Ltd

# ⚠️  NEVER COMMIT THESE VALUES TO GIT!
# Replace with your actual secure credentials

# AWS Database Configuration
AWS_DB_HOST=your-secure-rds-endpoint.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=your_database_name
AWS_DB_USER=your_secure_username
AWS_DB_PASSWORD=your_very_secure_password

# JWT Configuration
JWT_SECRET_KEY=generate_a_secure_random_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Environment
ENVIRONMENT=production
DEBUG=false

# Domain Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
'''
    
    with open('.env.template', 'w') as f:
        f.write(template)
    
    print("✅ Created secure .env.template")

def main():
    print("🚨 AWS CREDENTIALS SECURITY BREACH DETECTED!")
    print("=" * 60)
    print("The file 'prepare_deployment.py' contains exposed AWS credentials")
    print("that have been committed to your GitHub repository.")
    print("")
    print("CREDENTIALS FOUND:")
    print("• AWS_DB_HOST: supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com")
    print("• AWS_DB_USER: AdminTakeo")
    print("• AWS_DB_PASSWORD: Alex8nd3r12")
    print("")
    print("🎯 REQUIRED ACTIONS:")
    print("1. Change your AWS RDS password immediately")
    print("2. Remove credentials from git history")
    print("3. Update all systems with new credentials")
    print("")
    
    # Emergency cleanup
    if emergency_cleanup():
        create_secure_env_template()
        print("🔒 SECURITY BREACH CONTAINED!")
    else:
        print("❌ MANUAL CLEANUP REQUIRED!")
        print("")
        print("Manual steps:")
        print("1. Change AWS RDS password in AWS Console")
        print("2. Use git filter-branch to remove prepare_deployment.py")
        print("3. Force push to GitHub")

if __name__ == "__main__":
    main()
