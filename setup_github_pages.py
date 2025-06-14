#!/usr/bin/env python3
"""Setup GitHub Pages deployment for live website testing"""

import os
import shutil
import json
from datetime import datetime

def create_github_pages_setup():
    print("🌐 SETTING UP GITHUB PAGES FOR LIVE WEBSITE")
    print("=" * 50)
    
    # Create a separate directory for GitHub Pages deployment
    pages_dir = "github-pages-deploy"
    
    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
    
    os.makedirs(pages_dir)
    
    print(f"📁 Created deployment directory: {pages_dir}")
      # Copy frontend files
    frontend_files = [
        ("frontend/index.production.html", "index.html"),
        ("frontend/js/app.production.js", "js/app.js"),
    ]
    
    # Copy additional directories if they exist
    if os.path.exists("frontend/css"):
        frontend_files.append(("frontend/css", "css"))
    if os.path.exists("frontend/images"):
        frontend_files.append(("frontend/images", "images"))
      # Create js directory
    os.makedirs(f"{pages_dir}/js", exist_ok=True)
    
    for src, dst in frontend_files:
        if os.path.exists(src):
            if os.path.isfile(src):
                dst_path = f"{pages_dir}/{dst}"
                # Create directory if needed
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src, dst_path)
                print(f"📄 Copied: {src} -> {dst}")
            elif os.path.isdir(src):
                dst_path = f"{pages_dir}/{dst}"
                shutil.copytree(src, dst_path)
                print(f"📁 Copied directory: {src} -> {dst}")
    
    # Create a custom domain file (optional)
    with open(f"{pages_dir}/CNAME", "w") as f:
        f.write("# Replace with your custom domain if you have one\n")
        f.write("# smart-shopping.yourdomain.com\n")
      # Create README for GitHub Pages
    readme_content = f"""# Smart Shopping Platform - Live Website

**Live Demo:** https://YOURUSERNAME.github.io/REPOSITORY-NAME

## Features
- User Registration & Login
- Shopping List Management  
- Price Comparison
- Store Analysis
- Secure Authentication

## Backend API
This frontend connects to a live backend API for full functionality.

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Test Account
- **Email:** derek.j.king@live.com
- **Password:** Ask the developer

---
*Powered by Smart Shopping Platform*
"""
    
    with open(f"{pages_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create GitHub Pages configuration
    pages_config = {
        "name": "Smart Shopping Platform",
        "description": "Intelligent shopping companion with price comparison and deal discovery",
        "homepage": "https://YOURUSERNAME.github.io/REPOSITORY-NAME",
        "topics": ["shopping", "price-comparison", "deals", "savings", "javascript", "fastapi"]
    }
    
    with open(f"{pages_dir}/package.json", "w") as f:
        json.dump(pages_config, f, indent=2)
    
    # Create .nojekyll file to prevent Jekyll processing
    with open(f"{pages_dir}/.nojekyll", "w") as f:
        f.write("")
    
    print("\n✅ GitHub Pages setup complete!")
    print(f"📁 Deployment files in: {pages_dir}/")
    
    return pages_dir

def create_deployment_instructions():
    """Create step-by-step deployment instructions"""
    
    instructions = """# DEPLOY TO GITHUB PAGES - STEP BY STEP

## Prerequisites
1. GitHub account
2. Backend deployed (Heroku/Railway/Render)

## Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `smart-shopping-platform` (or your choice)
3. Description: "Intelligent Shopping Platform with Price Comparison"
4. Public repository
5. Add README file
6. Click "Create repository"

## Step 2: Upload Website Files
1. Click "uploading an existing file" on the new repo page
2. Drag and drop ALL files from `github-pages-deploy/` folder
3. Commit message: "Initial website deployment"
4. Click "Commit changes"

## Step 3: Enable GitHub Pages
1. Go to repository Settings > Pages (left sidebar)
2. Source: "Deploy from a branch"
3. Branch: "main" or "master"
4. Folder: "/ (root)"
5. Click "Save"

## Step 4: Update API URL
1. Deploy your backend first (see DEPLOYMENT_GUIDE.md)
2. Edit `js/app.js` in GitHub repository
3. Update the API_BASE_URL with your live backend URL
4. Commit the change

## Step 5: Get Your Live URL
After 2-3 minutes, your site will be live at:
**https://YOURUSERNAME.github.io/REPOSITORY-NAME**

## Step 6: Test with Users
Share your live URL with users to test:
- User registration
- Login functionality  
- Shopping lists
- Price comparisons

## Updates
To update the website:
1. Make changes locally
2. Copy files to `github-pages-deploy/`
3. Upload to GitHub repository
4. Changes go live automatically

---
**Your website will be live and ready for user testing!**
"""
    
    with open("GITHUB_PAGES_DEPLOYMENT.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📖 Created: GITHUB_PAGES_DEPLOYMENT.md")

def update_frontend_for_production():
    """Update frontend files for production deployment"""
    
    print("\n🔧 UPDATING FRONTEND FOR PRODUCTION...")
    
    # Read the production app.js
    if os.path.exists("frontend/js/app.production.js"):
        with open("frontend/js/app.production.js", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update API base URL placeholder
        content = content.replace(
            "https://your-heroku-app.herokuapp.com",
            "https://your-backend-app.herokuapp.com"  # This will need to be updated with actual backend URL
        )
        
        # Save to deployment directory
        with open("github-pages-deploy/js/app.js", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Updated app.js with production settings")
    
    # Update index.html with proper title and meta
    if os.path.exists("github-pages-deploy/index.html"):
        with open("github-pages-deploy/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add meta tags for better SEO
        meta_tags = '''<meta name="description" content="Smart Shopping Platform - Compare prices, find deals, save money">
    <meta name="keywords" content="shopping, deals, price comparison, savings, grocery">
    <meta name="author" content="Smart Shopping Platform">
    <meta property="og:title" content="Smart Shopping Platform">
    <meta property="og:description" content="Intelligent shopping companion with price comparison">
    <meta property="og:type" content="website">'''
        
        content = content.replace('<meta name="viewport"', meta_tags + '\n    <meta name="viewport"')
        
        with open("github-pages-deploy/index.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Updated index.html with meta tags")

def main():
    try:
        # Create GitHub Pages setup
        pages_dir = create_github_pages_setup()
        
        # Update frontend for production
        update_frontend_for_production()
        
        # Create deployment instructions
        create_deployment_instructions()
        
        print("\n" + "=" * 50)
        print("🎉 GITHUB PAGES SETUP COMPLETE!")
        print("=" * 50)
        print(f"📁 Files ready for deployment in: {pages_dir}/")
        print("📖 Read: GITHUB_PAGES_DEPLOYMENT.md for step-by-step guide")
        print("\n🌐 NEXT STEPS:")
        print("1. Create GitHub repository")
        print("2. Upload files from github-pages-deploy/ folder")
        print("3. Enable GitHub Pages in repository settings")
        print("4. Deploy backend and update API URL")
        print("5. Share live URL with test users!")
        print("\n🎯 Your website will be live for user testing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
