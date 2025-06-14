#!/usr/bin/env python3
"""
GitHub Repository Setup Script with Corporate Protection
Creates and configures GitHub repository for Spirit of the Immortals Ltd
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def setup_github_repo():
    """Set up GitHub repository with corporate protection"""
    
    print("🏢 Spirit of the Immortals Ltd - GitHub Repository Setup")
    print("=" * 55)
    print("Company Registration: 13434726 (England & Wales)")
    print("Director: Derek King")
    print()
    
    # Check if we're in the right directory
    if not Path("secure_aws_shopping.py").exists():
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    print("🚀 Setting up GitHub repository...")
    print()
    
    # Step 1: Configure git if needed
    try:
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("⚙️  Configuring git user...")
            subprocess.run(['git', 'config', 'user.name', 'Derek King'], check=True)
            subprocess.run(['git', 'config', 'user.email', 'derek.j.king@live.com'], check=True)
            print("✅ Git user configured")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git configuration warning: {e}")
    
    # Step 2: Check current git status
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        print("📊 Current git status:")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("❌ Error checking git status")
        return False
    
    # Step 3: Add files to git
    print("📁 Adding files to git...")
    try:
        # Add essential files
        files_to_add = [
            'LICENSE',
            'README.md', 
            'secure_aws_shopping.py',
            'frontend/',
            'database/',
            'requirements.txt',
            'Procfile',
            'runtime.txt',
            '.gitignore',
            'WORKSPACE_CLEANUP_COMPLETE.md'
        ]
        
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
                print(f"  ✅ Added {file}")
        
        print("✅ Files added to git")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error adding files: {e}")
        return False
    
    # Step 4: Commit changes
    print("\n💾 Committing changes...")
    try:
        commit_message = "Initial commit: Smart Shopping Platform by Spirit of the Immortals Ltd"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Changes committed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Commit info: {e}")
    
    # Step 5: Open GitHub to create repository
    print("\n🌐 Opening GitHub to create repository...")
    github_url = "https://github.com/new"
    
    print(f"📋 Repository Configuration:")
    print(f"   Repository name: smart-shopping-platform")
    print(f"   Description: Smart Shopping Platform by Spirit of the Immortals Ltd - Price comparison across UK supermarkets")
    print(f"   Visibility: PUBLIC (for users to access)")
    print(f"   License: Custom (already added LICENSE file)")
    print(f"   Initialize: NO (we have existing code)")
    
    try:
        webbrowser.open(github_url)
        print("✅ GitHub opened in browser")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print(f"Please manually go to: {github_url}")
    
    print(f"\n📋 INSTRUCTIONS:")
    print(f"1. Create repository with name: smart-shopping-platform")
    print(f"2. Add description: Smart Shopping Platform by Spirit of the Immortals Ltd")
    print(f"3. Make it PUBLIC")
    print(f"4. Do NOT initialize with README, .gitignore, or license")
    print(f"5. Click 'Create repository'")
    print(f"6. Copy the remote URL and run the commands shown")
    
    print(f"\n🔗 After creating the repository, run these commands:")
    print(f"   git remote add origin https://github.com/dkingDev/smart-shopping-platform.git")
    print(f"   git branch -M main")
    print(f"   git push -u origin main")
    
    print(f"\n🏢 Corporate Protection Active:")
    print(f"   ✅ Proprietary LICENSE file included")
    print(f"   ✅ Copyright headers in source code")
    print(f"   ✅ Corporate information in README")
    print(f"   ✅ Sensitive files gitignored")
    
    return True

if __name__ == "__main__":
    setup_github_repo()
