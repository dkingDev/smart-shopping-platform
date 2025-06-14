#!/usr/bin/env python3
# Production Server Script
import subprocess
import sys
import os

def main():
    print("🚀 Starting Smart Shopping Platform - Production Mode")
    
    # Use production environment
    os.environ['ENV_FILE'] = '.env.production'
    
    # Start with gunicorn for production
    try:
        subprocess.run([
            "gunicorn", 
            "secure_aws_shopping:app",
            "-w", "4",
            "-k", "uvicorn.workers.UvicornWorker",
            "--bind", "0.0.0.0:8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Production server stopped")

if __name__ == "__main__":
    main()
