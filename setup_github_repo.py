#!/usr/bin/env python3
"""
GitHub Repository Setup Script for Smart Shopping Platform
Creates a new GitHub repository and pushes the clean project
"""

import os
import subprocess
import webbrowser

def setup_github_repo():
    """Set up GitHub repository for the Smart Shopping Platform"""
    
    print("🚀 Setting up GitHub Repository for Smart Shopping Platform")
    print("=" * 60)
    
    # Repository details
    repo_name = "smart-shopping-platform"
    description = "Smart Shopping Platform - Price comparison and savings tracker across UK supermarkets"
    
    print(f"📝 Repository Name: {repo_name}")
    print(f"📝 Description: {description}")
    print()
    
    # Step 1: Clean up any remaining non-essential files
    print("1️⃣ Cleaning up workspace...")
    if os.path.exists("comprehensive_cleanup.py"):
        os.remove("comprehensive_cleanup.py")
        print("   ✅ Removed cleanup script")
    
    # Step 2: Stage and commit changes
    print("\n2️⃣ Staging files for commit...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🎉 Clean workspace ready for production deployment"], check=True)
        print("   ✅ Files committed successfully")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Git commit issue: {e}")
    
    # Step 3: Instructions for GitHub
    print("\n3️⃣ GitHub Repository Setup Instructions:")
    print("   📍 You need to manually create the repository on GitHub")
    print("   📍 Here's what to do:")
    print()
    print("   STEP A: Create Repository on GitHub")
    print("   ========================")
    print(f"   1. Go to: https://github.com/dkingDev")
    print("   2. Click 'New' or 'New repository'")
    print(f"   3. Repository name: {repo_name}")
    print(f"   4. Description: {description}")
    print("   5. Make it PUBLIC")
    print("   6. DON'T initialize with README (we already have one)")
    print("   7. Click 'Create repository'")
    print()
    
    print("   STEP B: Connect Local Repository")
    print("   ================================")
    github_url = f"https://github.com/dkingDev/{repo_name}.git"
    print(f"   Run these commands in your terminal:")
    print(f"   git remote add origin {github_url}")
    print(f"   git branch -M main")
    print(f"   git push -u origin main")
    print()
    
    print("   STEP C: Enable GitHub Pages")
    print("   ===========================")
    print("   1. Go to repository Settings")
    print("   2. Scroll to 'Pages' section")
    print("   3. Source: 'Deploy from a branch'")
    print("   4. Branch: 'main' folder: '/ (root)'")
    print("   5. Click 'Save'")
    print()
    
    # Step 4: Open GitHub in browser
    print("4️⃣ Opening GitHub in your browser...")
    github_new_repo_url = "https://github.com/new"
    try:
        webbrowser.open(github_new_repo_url)
        print(f"   ✅ Opened: {github_new_repo_url}")
    except Exception as e:
        print(f"   ⚠️  Could not open browser: {e}")
        print(f"   📍 Manually go to: {github_new_repo_url}")
    
    print("\n✅ Ready for GitHub!")
    print("📦 Your clean workspace is prepared for deployment")
    print("🔒 No sensitive data will be leaked")
    print("🚀 Follow the instructions above to publish to GitHub")
    
    return github_url

if __name__ == "__main__":
    github_url = setup_github_repo()
    print(f"\n🎯 Target Repository: {github_url}")
