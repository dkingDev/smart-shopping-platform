#!/usr/bin/env python3
"""
Clean up workspace - Remove unnecessary files and folders
Keep only: 
1. Essential production files
2. Universal crawler infrastructure  
3. Clean deployment packages
4. Core documentation
"""

import os
import shutil
from pathlib import Path

def cleanup_workspace():
    """Remove unnecessary files and folders"""
    
    print("🧹 Cleaning up workspace...")
    print("🎯 Keeping only essential files for production and crawler infrastructure")
    print()
    
    # Files and folders to KEEP (everything else will be removed)
    keep_items = {
        # Essential production files
        'secure_aws_shopping.py',           # Main backend
        'run_local.py',                     # Local development 
        'run_production.py',                # Production runner
        '.env',                             # Environment variables
        '.env.production',                  # Production environment
        'requirements.txt',                 # Dependencies
        'Procfile',                         # Heroku config
        'runtime.txt',                      # Python version
        
        # Clean deployment packages (ready to deploy)
        'github-pages-public-only.zip',     # Clean frontend package
        'heroku-backend-public-only.zip',   # Clean backend package
        
        # Core infrastructure folders
        'database',                         # Database management
        'frontend',                         # Frontend source
        'scripts',                          # Your crawler infrastructure
        
        # Essential documentation
        'README.md',                        # Main documentation
        'CLEAN_DEPLOYMENT_READY.md',       # Deployment status
        
        # Git and development
        '.git',                             # Git repository
        '.gitignore',                       # Git ignore
        '__pycache__',                      # Python cache (auto-generated)
    }
    
    # Get all items in current directory
    all_items = set(os.listdir('.'))
    items_to_remove = all_items - keep_items
    
    print("📁 Items to KEEP:")
    for item in sorted(keep_items):
        if item in all_items:
            print(f"  ✅ {item}")
    
    print(f"\n🗑️  Items to REMOVE ({len(items_to_remove)}):")
    for item in sorted(items_to_remove):
        print(f"  ❌ {item}")
    
    print(f"\n⚠️  About to remove {len(items_to_remove)} items...")
    confirm = input("Continue? (y/N): ").lower().strip()
    
    if confirm != 'y':
        print("❌ Cleanup cancelled")
        return
    
    # Remove items
    removed_count = 0
    for item in items_to_remove:
        try:
            item_path = Path(item)
            if item_path.exists():
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"  🗂️  Removed folder: {item}")
                else:
                    item_path.unlink()
                    print(f"  📄 Removed file: {item}")
                removed_count += 1
        except Exception as e:
            print(f"  ❌ Error removing {item}: {e}")
    
    print(f"\n🎉 Cleanup complete!")
    print(f"✅ Removed {removed_count} items")
    print(f"📦 Kept {len(keep_items)} essential items")
    
    # Show final workspace structure
    print(f"\n📁 Final workspace structure:")
    remaining_items = sorted(os.listdir('.'))
    for item in remaining_items:
        item_path = Path(item)
        if item_path.is_dir():
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")
    
    print(f"\n🎯 Workspace optimized!")
    print("✅ Production files ready")
    print("✅ Crawler infrastructure preserved") 
    print("✅ Clean deployment packages ready")
    print("✅ Unnecessary files removed")

if __name__ == "__main__":
    cleanup_workspace()
