#!/usr/bin/env python3
"""Prepare GitHub repository upload package"""

import os
import zipfile
import shutil
from datetime import datetime

def create_github_upload_package():
    """Create a zip file ready for GitHub upload"""
    print("📦 CREATING GITHUB UPLOAD PACKAGE")
    print("=" * 40)
    
    # Create a zip file with all frontend files
    zip_filename = "github-pages-upload.zip"
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from github-pages-deploy
        for root, dirs, files in os.walk("github-pages-deploy"):
            for file in files:
                file_path = os.path.join(root, file)
                # Get relative path from github-pages-deploy
                arcname = os.path.relpath(file_path, "github-pages-deploy")
                zipf.write(file_path, arcname)
                print(f"✅ Added: {arcname}")
    
    print(f"📦 Created: {zip_filename}")
    print(f"📂 Size: {os.path.getsize(zip_filename)} bytes")
    
    return zip_filename

def create_heroku_upload_package():
    """Create a zip file ready for Heroku upload"""
    print("\n📦 CREATING HEROKU UPLOAD PACKAGE")
    print("=" * 40)
    
    # Create a zip file with all backend files
    zip_filename = "heroku-backend-upload.zip"
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from backend-deploy
        for root, dirs, files in os.walk("backend-deploy"):
            for file in files:
                file_path = os.path.join(root, file)
                # Get relative path from backend-deploy
                arcname = os.path.relpath(file_path, "backend-deploy")
                zipf.write(file_path, arcname)
                print(f"✅ Added: {arcname}")
    
    print(f"📦 Created: {zip_filename}")
    print(f"📂 Size: {os.path.getsize(zip_filename)} bytes")
    
    return zip_filename

def create_deployment_summary():
    """Create a deployment summary with all URLs and steps"""
    
    summary = f"""# 🚀 DEPLOYMENT READY - ALL FILES PREPARED

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📦 UPLOAD PACKAGES CREATED

### 1. Heroku Backend: `heroku-backend-upload.zip`
- **Upload to:** https://dashboard.heroku.com/new-app
- **Contains:** Backend API files + database
- **Environment Variables:** See HEROKU_DEPLOYMENT_COMPLETE.md

### 2. GitHub Frontend: `github-pages-upload.zip`  
- **Upload to:** https://github.com/new (then upload files)
- **Contains:** Website files (HTML, CSS, JS)
- **Result:** Live website at github.io

## 🎯 DEPLOYMENT STEPS

### Step 1: Deploy Backend (Heroku)
1. Go to https://dashboard.heroku.com/new-app
2. Create app (name: smart-shopping-derek)
3. Upload heroku-backend-upload.zip files
4. Add environment variables (see guide)
5. Deploy
6. Copy your Heroku URL

### Step 2: Deploy Frontend (GitHub)
1. Go to https://github.com/new
2. Create repository (name: smart-shopping-platform)
3. Upload github-pages-upload.zip files
4. Enable GitHub Pages in Settings
5. Update js/app.js with Heroku URL
6. Get your live website URL

## 🌐 YOUR LIVE URLS

**Backend API:** https://YOUR-APP-NAME.herokuapp.com  
**Frontend Website:** https://YOUR-USERNAME.github.io/smart-shopping-platform

## 👥 TEST ACCOUNT

**Email:** derek.j.king@live.com  
**Password:** Alex8nd3r!

## 📋 QUICK CHECKLIST

- [ ] Deploy backend to Heroku
- [ ] Deploy frontend to GitHub Pages  
- [ ] Update API URL in frontend
- [ ] Test live website
- [ ] Share with users

**🎉 Your Smart Shopping Platform will be live worldwide!**

---
*Follow HEROKU_DEPLOYMENT_COMPLETE.md for detailed step-by-step instructions*
"""
    
    with open("DEPLOYMENT_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📋 Created: DEPLOYMENT_SUMMARY.md")

def main():
    print("🚀 PREPARING COMPLETE DEPLOYMENT PACKAGES")
    print("=" * 50)
    
    # Create upload packages
    heroku_zip = create_heroku_upload_package()
    github_zip = create_github_upload_package()
    
    # Create summary
    create_deployment_summary()
    
    print("\n" + "=" * 50)
    print("🎉 DEPLOYMENT PACKAGES READY!")
    print("=" * 50)
    print(f"🔹 Heroku Backend: {heroku_zip}")
    print(f"🔹 GitHub Frontend: {github_zip}")
    print(f"📋 Instructions: DEPLOYMENT_SUMMARY.md")
    print(f"📖 Detailed Guide: HEROKU_DEPLOYMENT_COMPLETE.md")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Upload heroku package to Heroku")
    print("2. Upload github package to GitHub")
    print("3. Follow the detailed guide")
    print("4. Your website will be LIVE!")
    
    print("\n🌐 TOTAL DEPLOYMENT TIME: ~6 minutes")
    print("🚀 RESULT: Live website for user testing!")

if __name__ == "__main__":
    main()
