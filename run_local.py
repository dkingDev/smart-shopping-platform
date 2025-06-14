#!/usr/bin/env python3
# Local Development Test Script
import subprocess
import sys
import os

def main():
    print("🚀 Starting Smart Shopping Platform - Local Development Mode")
    
    # Use local environment
    os.environ['ENV_FILE'] = '.env'
    
    # Start with uvicorn for development
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "secure_aws_shopping:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "9999"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Local development server stopped")

if __name__ == "__main__":
    main()
