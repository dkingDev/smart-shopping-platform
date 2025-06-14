#!/usr/bin/env python3
"""
Test Runner for Smart Shopping Platform

This script runs all tests in the test environment with proper isolation.
"""

import sys
import os
import pytest
import uvicorn
import threading
import time
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.test.test_config import TestConfig

class TestRunner:
    """Test runner with environment management"""
    
    def __init__(self):
        self.config = TestConfig()
        self.server_thread = None
        self.server_running = False
        
    def setup_test_environment(self):
        """Setup test environment"""
        print("🔧 Setting up test environment...")
        
        # Load test environment
        from dotenv import load_dotenv
        load_dotenv('.env.test')
        
        # Verify test configuration
        if not all([
            os.getenv('TEST_AWS_DB_HOST'),
            os.getenv('TEST_AWS_DB_USER'),
            os.getenv('TEST_AWS_DB_PASSWORD')
        ]):
            print("❌ Test environment variables not configured")
            print("💡 Please configure .env.test file")
            return False
            
        print("✅ Test environment configured")
        return True
    
    def start_test_server(self):
        """Start test server in background"""
        print(f"🚀 Starting test server on http://{self.config.HOST}:{self.config.PORT}")
        
        def run_server():
            # Import the app with test configuration
            from secure_aws_shopping import app
            uvicorn.run(
                app,
                host=self.config.HOST,
                port=self.config.PORT,
                log_level="warning"  # Reduce noise during tests
            )
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait for server to start
        for _ in range(30):  # 30 second timeout
            try:
                response = requests.get(f"http://{self.config.HOST}:{self.config.PORT}/admin/docs")
                if response.status_code == 200:
                    self.server_running = True
                    print("✅ Test server started successfully")
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        
        print("❌ Test server failed to start")
        return False
    
    def run_unit_tests(self):
        """Run unit tests"""
        print("\n🧪 Running unit tests...")
        result = pytest.main([
            "tests/unit",
            "-v",
            "--tb=short",
            f"--junitxml=test_results_unit.xml"
        ])
        return result == 0
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n🔗 Running integration tests...")
        result = pytest.main([
            "tests/integration",
            "-v", 
            "--tb=short",
            f"--junitxml=test_results_integration.xml"
        ])
        return result == 0
    
    def run_api_tests(self):
        """Run API tests against test server"""
        print("\n🌐 Running API tests...")
        
        base_url = f"http://{self.config.HOST}:{self.config.PORT}"
        
        tests = [
            ("Health Check", f"{base_url}/admin/docs"),
            ("Frontend", f"{base_url}/frontend/"),
            ("API Root", f"{base_url}/")
        ]
        
        all_passed = True
        for test_name, url in tests:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {test_name}: PASS")
                else:
                    print(f"❌ {test_name}: FAIL (Status: {response.status_code})")
                    all_passed = False
            except Exception as e:
                print(f"❌ {test_name}: FAIL ({str(e)})")
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🎯 Smart Shopping Platform - Test Suite")
        print("=" * 50)
        
        # Setup
        if not self.setup_test_environment():
            return False
        
        # Start test server
        if not self.start_test_server():
            return False
        
        try:
            # Run all test suites
            results = []
            results.append(("Unit Tests", self.run_unit_tests()))
            results.append(("Integration Tests", self.run_integration_tests()))
            results.append(("API Tests", self.run_api_tests()))
            
            # Summary
            print("\n" + "=" * 50)
            print("📊 Test Results Summary:")
            
            all_passed = True
            for test_type, passed in results:
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"{test_type}: {status}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("\n🎉 All tests passed! Ready for deployment.")
            else:
                print("\n⚠️ Some tests failed. Please review and fix issues.")
            
            return all_passed
            
        except KeyboardInterrupt:
            print("\n🛑 Tests interrupted by user")
            return False

def main():
    """Main entry point"""
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
