#!/usr/bin/env python3
"""
Quick GitHub Pages Deployment
Uses existing secure frontend package to deploy live for test users.
"""

import os
import subprocess
import shutil

def deploy_frontend_to_github_pages():
    """Deploy the secure frontend package to GitHub Pages"""
    print("🚀 DEPLOYING SMART SHOPPING PLATFORM TO GITHUB PAGES")
    print("=" * 60)
    
    # Check if we have the secure package
    if not os.path.exists('github-pages-public-only.zip'):
        print("❌ Secure frontend package not found!")
        return False
    
    print("✅ Secure frontend package found")
    
    # Extract to temporary directory
    print("📦 Extracting secure frontend...")
    if os.path.exists('temp-frontend-deploy'):
        shutil.rmtree('temp-frontend-deploy')
    
    subprocess.run([
        'pwsh', '-Command', 
        'Expand-Archive -Path github-pages-public-only.zip -DestinationPath temp-frontend-deploy -Force'
    ])
    
    # Check git status
    print("🔍 Checking git repository...")
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    
    if result.stdout.strip():
        print("⚠️ Repository has uncommitted changes")
        print("To deploy safely, let's create a new branch:")
        
        # Create deployment branch
        print("🌿 Creating deployment branch...")
        subprocess.run(['git', 'checkout', '-b', 'github-pages-deploy'], capture_output=True)
        
        # Copy secure frontend files to root
        print("📁 Copying secure frontend files...")
        
        # Copy main files
        shutil.copy('temp-frontend-deploy/index.html', 'index.html')
        shutil.copy('temp-frontend-deploy/.nojekyll', '.nojekyll')
        
        # Copy js directory
        if os.path.exists('js'):
            shutil.rmtree('js')
        shutil.copytree('temp-frontend-deploy/js', 'js')
        
        # Add deployment files
        subprocess.run(['git', 'add', 'index.html', '.nojekyll', 'js/'])
        
        # Commit deployment
        subprocess.run([
            'git', 'commit', '-m', 
            'Deploy secure frontend for test users - Production ready'
        ])
        
        print("✅ Deployment branch ready")
        print("\n🔗 TO COMPLETE DEPLOYMENT:")
        print("1. Push this branch to GitHub:")
        print("   git push origin github-pages-deploy")
        print("2. Go to your GitHub repository")
        print("3. Settings → Pages → Source → Deploy from branch")
        print("4. Select 'github-pages-deploy' branch")
        print("5. Your site will be live at:")
        print("   https://YOURUSERNAME.github.io/REPOSITORY-NAME")
        
        return True
    
    else:
        print("✅ Repository is clean - ready for direct deployment")
        
        # We can deploy directly
        print("📁 Copying secure frontend to root...")
        
        # Backup current files if they exist
        files_to_backup = ['index.html', 'js']
        for file in files_to_backup:
            if os.path.exists(file):
                backup_name = f"{file}.backup"
                if os.path.isdir(file):
                    if os.path.exists(backup_name):
                        shutil.rmtree(backup_name)
                    shutil.copytree(file, backup_name)
                else:
                    shutil.copy(file, backup_name)
        
        # Copy secure frontend files
        shutil.copy('temp-frontend-deploy/index.html', 'index.html')
        shutil.copy('temp-frontend-deploy/.nojekyll', '.nojekyll')
        
        if os.path.exists('js'):
            shutil.rmtree('js')
        shutil.copytree('temp-frontend-deploy/js', 'js')
        
        # Add and commit
        subprocess.run(['git', 'add', 'index.html', '.nojekyll', 'js/'])
        subprocess.run(['git', 'commit', '-m', 'Deploy secure frontend - Ready for test users'])
        
        print("✅ Frontend deployed to main branch")
        print("\n🔗 TO GO LIVE:")
        print("1. Push to GitHub: git push origin main")
        print("2. Enable GitHub Pages in repository settings")
        print("3. Your site will be live at:")
        print("   https://YOURUSERNAME.github.io/REPOSITORY-NAME")
        
        return True

def main():
    """Main deployment function"""
    if deploy_frontend_to_github_pages():
        print("\n🎉 DEPLOYMENT READY!")
        print("Your test users will be able to access the Smart Shopping Platform")
        print("once you complete the GitHub Pages setup steps above.")
        
        # Cleanup
        if os.path.exists('temp-frontend-deploy'):
            shutil.rmtree('temp-frontend-deploy')
    else:
        print("\n❌ Deployment failed")

if __name__ == "__main__":
    main()
