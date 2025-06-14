#!/usr/bin/env python3
"""Quick live testing with ngrok"""

import subprocess
import sys
import time
import requests
import webbrowser

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is installed")
            return True
        else:
            print("❌ ngrok not found")
            return False
    except FileNotFoundError:
        print("❌ ngrok not found")
        return False

def start_ngrok_tunnel():
    """Start ngrok tunnel for local server"""
    
    print("🌐 STARTING LIVE DEMO WITH NGROK")
    print("=" * 40)
    
    if not check_ngrok():
        print("\n📥 INSTALL NGROK FIRST:")
        print("1. Go to https://ngrok.com/download")
        print("2. Download and install ngrok")
        print("3. Run: ngrok authtoken YOUR_TOKEN")
        print("4. Then run this script again")
        return False
    
    print("🚀 Starting ngrok tunnel on port 9999...")
    
    try:
        # Start ngrok in background
        process = subprocess.Popen(['ngrok', 'http', '9999'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for ngrok to start
        time.sleep(3)
        
        # Get ngrok public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()
            
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ Live demo URL: {public_url}")
                print(f"🌐 Share this URL with test users!")
                
                # Test the connection
                print("\n🧪 Testing live URL...")
                health_response = requests.get(f"{public_url}/api/system-health")
                
                if health_response.status_code == 200:
                    print("✅ Live website is working!")
                    
                    print(f"\n👥 SHARE WITH USERS:")
                    print(f"📱 URL: {public_url}")
                    print(f"👤 Test Login: derek.j.king@live.com")
                    print(f"🔑 Password: Alex8nd3r!")
                    
                    # Open browser
                    print(f"\n🌐 Opening {public_url} in browser...")
                    webbrowser.open(public_url)
                    
                    print("\n⚠️  KEEP THIS TERMINAL OPEN")
                    print("Press Ctrl+C to stop the live demo")
                    
                    # Keep running
                    try:
                        process.wait()
                    except KeyboardInterrupt:
                        print("\n🛑 Stopping live demo...")
                        process.terminate()
                        print("✅ Live demo stopped")
                        
                    return True
                else:
                    print("❌ Live URL not responding")
                    return False
            else:
                print("❌ No tunnels found")
                return False
                
        except Exception as e:
            print(f"❌ Error getting ngrok URL: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INSTANT LIVE DEMO SETUP")
    print("This will make your localhost:9999 accessible to anyone worldwide")
    print("")
    
    choice = input("Continue? (y/n): ").lower().strip()
    
    if choice == 'y':
        start_ngrok_tunnel()
    else:
        print("📖 See GET_LIVE_WEBSITE.md for permanent deployment options")
