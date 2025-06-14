#!/usr/bin/env python3
"""
Test Configuration for Smart Shopping Platform
"""

import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv('.env.test')

class TestConfig:
    """Test environment configuration"""
    
    # Test Database
    TEST_DATABASE_URL = (
        f"postgresql://{os.getenv('TEST_AWS_DB_USER')}:"
        f"{os.getenv('TEST_AWS_DB_PASSWORD')}@"
        f"{os.getenv('TEST_AWS_DB_HOST')}:"
        f"{os.getenv('TEST_AWS_DB_PORT', '5432')}/"
        f"{os.getenv('TEST_AWS_DB_NAME')}"
    )
    
    # Test Security
    JWT_SECRET_KEY = os.getenv('TEST_JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('TEST_JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS = int(os.getenv('TEST_JWT_EXPIRATION_HOURS', '1'))
    
    # Test Server
    HOST = os.getenv('TEST_HOST', '127.0.0.1')
    PORT = int(os.getenv('TEST_PORT', '8889'))
    ENVIRONMENT = 'test'
    
    # Test Features
    ENABLE_TEST_ENDPOINTS = os.getenv('ENABLE_TEST_ENDPOINTS', 'true').lower() == 'true'
    MOCK_EXTERNAL_APIS = os.getenv('MOCK_EXTERNAL_APIS', 'true').lower() == 'true'
    BYPASS_EMAIL_VERIFICATION = os.getenv('BYPASS_EMAIL_VERIFICATION', 'true').lower() == 'true'
    
    # Test Data
    TEST_DATA_RESET = os.getenv('TEST_DATA_RESET', 'true').lower() == 'true'
    TEST_SAMPLE_DATA = os.getenv('TEST_SAMPLE_DATA', 'true').lower() == 'true'
    CREATE_TEST_USERS = os.getenv('CREATE_TEST_USERS', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('TEST_LOG_LEVEL', 'DEBUG')
    LOG_FILE = os.getenv('TEST_LOG_FILE', 'test_smart_shopping.log')

# Test user data
TEST_USERS = [
    {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "testpass123",
        "full_name": "Test User One"
    },
    {
        "username": "testuser2", 
        "email": "test2@example.com",
        "password": "testpass456",
        "full_name": "Test User Two"
    }
]

# Test shopping lists
TEST_SHOPPING_LISTS = [
    {
        "name": "Weekly Groceries",
        "items": ["Milk", "Bread", "Eggs", "Apples", "Chicken"]
    },
    {
        "name": "Party Supplies",
        "items": ["Chips", "Soda", "Ice Cream", "Balloons"]
    }
]

# Test product data
TEST_PRODUCTS = [
    {
        "name": "Test Milk",
        "category": "Dairy",
        "brand": "Test Brand",
        "price": 2.99,
        "store": "Test Store A"
    },
    {
        "name": "Test Bread",
        "category": "Bakery", 
        "brand": "Test Bakery",
        "price": 1.99,
        "store": "Test Store B"
    }
]
