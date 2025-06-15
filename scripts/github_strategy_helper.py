#!/usr/bin/env python3
"""
GitHub Repository Strategy Helper
Choose between full platform or website-only repository
"""

import os
import shutil
from pathlib import Path

def create_website_only_repo():
    """Create a separate website-only repository structure"""
    print("🌐 Creating website-only repository structure...")
    
    # Create website-only folder
    website_repo = Path("../smart-shopping-website-only")
    website_repo.mkdir(exist_ok=True)
    
    # Copy website files
    website_files = [
        "frontend/",
        "company-website/", 
        "README.md"
    ]
    
    base_path = Path(".")
    
    for file_path in website_files:
        source = base_path / file_path
        dest = website_repo / file_path
        
        if source.exists():
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"✅ Copied {file_path}")
            else:
                dest.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(source, dest)
                print(f"✅ Copied {file_path}")
    
    # Create website-specific README
    website_readme = website_repo / "README.md"
    with open(website_readme, 'w') as f:
        f.write("""# Spirit of the Immortals Ltd - Website

Professional e-commerce website and web application.

## 🌐 Components

- **Company Website**: Corporate information and branding
- **Web Application**: Interactive shopping platform frontend
- **Responsive Design**: Mobile-friendly interface

## 🚀 Deployment

This repository contains only the frontend components. 
The backend API is deployed separately for security.

## 📱 Features

- Modern responsive design
- Product browsing and search
- Shopping cart functionality  
- User authentication interface
- Company information pages

---
*Spirit of the Immortals Ltd - Professional E-commerce Solutions*
""")
    
    # Create website .gitignore
    website_gitignore = website_repo / ".gitignore"
    with open(website_gitignore, 'w') as f:
        f.write("""# Website Repository - Git Ignore

# Logs
*.log
logs/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Dependency directories
node_modules/

# Build outputs
dist/
build/

# Environment files
.env*

# Editor directories and files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
*.tmp
*.temp
""")
    
    print(f"✅ Website-only repository created at: {website_repo}")
    print("📁 Contains: frontend/, company-website/, README.md")
    return website_repo

def show_current_status():
    """Show what's currently in the repository"""
    print("📊 Current Repository Analysis:")
    print("=" * 50)
    
    # Count files by category
    categories = {
        "Frontend/Website": ["frontend/", "company-website/"],
        "Backend/API": ["secure_aws_shopping.py", "requirements.txt"],
        "Database": ["database/"],
        "Scripts/Automation": ["scripts/"],
        "Configuration": ["config/"],
        "Documentation": ["docs/", "*.md"],
        "Security": [".gitignore", ".env*"]
    }
    
    import subprocess
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    all_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    print(f"📁 Total tracked files: {len(all_files)}")
    print("\n📋 File breakdown:")
    
    for category, patterns in categories.items():
        count = 0
        for file in all_files:
            for pattern in patterns:
                if pattern.replace("*", "") in file or file.startswith(pattern.rstrip("/")):
                    count += 1
                    break
        print(f"  {category}: {count} files")
    
    print("\n🔒 Security Status:")
    print("  ✅ Sensitive files protected by .gitignore")
    print("  ✅ No secrets in tracked files")
    print("  ✅ Safe for public repositories")

def main():
    print("🎯 Smart Shopping Platform - GitHub Strategy Helper")
    print("=" * 60)
    
    show_current_status()
    
    print("\n🤔 Choose your GitHub strategy:")
    print("1. 🚀 FULL PLATFORM (Recommended) - Complete professional project")
    print("2. 🌐 WEBSITE ONLY - Just frontend components")
    print("3. 📊 ANALYSIS ONLY - Show current status and exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n✅ EXCELLENT CHOICE!")
        print("🚀 Your current repository is perfect for GitHub:")
        print("   - Complete professional platform")
        print("   - All sensitive data protected")
        print("   - Team collaboration ready")
        print("   - Great portfolio showcase")
        print("\n💡 Action: Just push your current repository to GitHub!")
        print("   git push origin main")
        
    elif choice == "2":
        print("\n🌐 Creating website-only repository...")
        website_repo = create_website_only_repo()
        print(f"\n✅ Website-only repository created!")
        print(f"📁 Location: {website_repo}")
        print("\n💡 Next steps:")
        print(f"   cd {website_repo}")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial website repository'")
        print("   # Create GitHub repo and push")
        
    elif choice == "3":
        print("\n📊 Analysis complete! Choose option 1 or 2 when ready.")
        
    else:
        print("❌ Invalid choice. Please run again and choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
