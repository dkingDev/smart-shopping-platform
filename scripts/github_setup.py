#!/usr/bin/env python3
"""
GitHub Setup Script for Smart Shopping Platform

This script initializes the repository for GitHub with proper configuration.
"""

import os
import subprocess
import sys
from pathlib import Path

class GitHubSetup:
    """GitHub repository setup and configuration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        os.chdir(self.project_root)
    
    def check_git_installed(self):
        """Check if Git is installed"""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Git installed: {result.stdout.strip()}")
                return True
            else:
                print("❌ Git is not installed")
                return False
        except FileNotFoundError:
            print("❌ Git is not installed or not in PATH")
            return False
    
    def initialize_git_repo(self):
        """Initialize Git repository if not already initialized"""
        if (self.project_root / '.git').exists():
            print("✅ Git repository already initialized")
            return True
        
        try:
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            print("✅ Git repository initialized")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Git repository: {e}")
            return False
    
    def setup_gitignore(self):
        """Setup comprehensive .gitignore"""
        gitignore_content = """# Smart Shopping Platform - Git Ignore

# Environment files
.env
.env.local
.env.production
.env.test
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/
smart_shopping*.log
production_setup.log
test_*.log

# Database
*.db
*.sqlite3

# Test results
test-results*.xml
.coverage
htmlcov/
.pytest_cache/

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Deployment
deploy/
.deployment/

# Secrets
secrets/
*.key
*.pem
*.crt

# Generated documentation
docs/_build/
site/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# Backup files
*.backup
*.bak
"""
        
        gitignore_path = self.project_root / '.gitignore'
        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print("✅ .gitignore file created")
            return True
        except Exception as e:
            print(f"❌ Failed to create .gitignore: {e}")
            return False
      def create_readme_for_github(self):
        """Create GitHub-ready README"""
        readme_github = self.project_root / 'README_GITHUB.md'
        readme_main = self.project_root / 'README.md'
        
        if readme_github.exists():
            try:
                # Replace main README with GitHub version
                with open(readme_github, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(readme_main, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Remove the separate GitHub readme
                readme_github.unlink()
                print("✅ README.md updated for GitHub")
                return True
            except Exception as e:
                print(f"❌ Failed to update README: {e}")
                return False
        
        print("✅ README.md already configured")
        return True
    
    def add_initial_commit(self):
        """Add initial commit"""
        try:
            # Add all files
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
            if result.returncode == 0:
                print("✅ No changes to commit")
                return True
            
            # Create initial commit
            subprocess.run([
                'git', 'commit', '-m', 
                'Initial commit: Smart Shopping Platform with test environment'
            ], check=True, capture_output=True)
            
            print("✅ Initial commit created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create initial commit: {e}")
            return False
    
    def setup_branches(self):
        """Setup development and production branches"""
        try:
            # Create develop branch
            subprocess.run(['git', 'checkout', '-b', 'develop'], check=True, capture_output=True)
            print("✅ Develop branch created")
            
            # Switch back to main
            subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)
            print("✅ Main branch active")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup branches: {e}")
            return False
    
    def display_github_instructions(self):
        """Display instructions for GitHub setup"""
        print("\n" + "="*60)
        print("🚀 GitHub Repository Setup Instructions")
        print("="*60)
        print("\n1. Create a new repository on GitHub:")
        print("   - Go to https://github.com/new")
        print("   - Repository name: smart-shopping-platform")
        print("   - Description: Secure smart shopping platform with AWS integration")
        print("   - Make it Public or Private as needed")
        print("   - Don't initialize with README, .gitignore, or license")
        
        print("\n2. Add GitHub remote and push:")
        print("   git remote add origin https://github.com/yourusername/smart-shopping-platform.git")
        print("   git push -u origin main")
        print("   git push origin develop")
        
        print("\n3. Configure GitHub Secrets (for CI/CD):")
        print("   Go to repository Settings > Secrets and variables > Actions")
        print("   Add the following secrets:")
        print("   - AWS_DB_HOST: your-rds-endpoint.amazonaws.com")
        print("   - AWS_DB_PORT: 5432")
        print("   - AWS_DB_NAME: smart_shopping")
        print("   - AWS_DB_USER: your_username")
        print("   - AWS_DB_PASSWORD: your_password")
        print("   - JWT_SECRET_KEY: your-super-secret-key")
        
        print("\n4. Enable GitHub Actions:")
        print("   - GitHub Actions will run automatically on push/PR")
        print("   - Tests will run on multiple Python versions")
        print("   - Production deployment on main branch pushes")
        
        print("\n5. Setup branch protection (recommended):")
        print("   - Go to Settings > Branches")
        print("   - Add rule for 'main' branch")
        print("   - Require status checks (tests) before merging")
        print("   - Require pull request reviews")
        
        print("\n6. Configure environments:")
        print("   - Go to Settings > Environments")
        print("   - Create 'production' environment")
        print("   - Add protection rules and secrets")
        
        print(f"\n✅ Repository ready for GitHub!")
        print(f"📁 Project root: {self.project_root}")
        print("🔗 Next: Push to GitHub and configure secrets")
    
    def run_setup(self):
        """Run complete GitHub setup"""
        print("🚀 Setting up Smart Shopping Platform for GitHub...")
        print("="*60)
        
        steps = [
            ("Git Installation Check", self.check_git_installed),
            ("Initialize Git Repository", self.initialize_git_repo),
            ("Setup .gitignore", self.setup_gitignore),
            ("Update README for GitHub", self.create_readme_for_github),
            ("Add Initial Commit", self.add_initial_commit),
            ("Setup Branches", self.setup_branches),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 Step: {step_name}")
            if not step_func():
                print(f"❌ Setup failed at step: {step_name}")
                return False
        
        self.display_github_instructions()
        return True

def main():
    """Main entry point"""
    setup = GitHubSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
