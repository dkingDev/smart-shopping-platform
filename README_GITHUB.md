# Smart Shopping Platform

[![Tests](https://github.com/yourusername/smart-shopping-platform/workflows/Tests/badge.svg)](https://github.com/yourusername/smart-shopping-platform/actions)
[![Production](https://github.com/yourusername/smart-shopping-platform/workflows/Production/badge.svg)](https://github.com/yourusername/smart-shopping-platform/actions)

## 🎯 Overview

A **production-ready, secure smart shopping platform** with AWS PostgreSQL integration, JWT authentication, and comprehensive testing.

## 🚀 Quick Start

### Development
```bash
git clone https://github.com/yourusername/smart-shopping-platform.git
cd smart-shopping-platform
cp .env.example .env
# Configure your .env file
pip install -r requirements-dev.txt
python scripts/quick_start.py
```

### Testing
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
```

### Production
```bash
cp .env.example .env
# Configure production environment variables
python scripts/production_setup.py
```

## 🏗️ Architecture

- **Backend**: FastAPI with AWS PostgreSQL
- **Frontend**: Modern SPA with Bootstrap 5
- **Authentication**: JWT with bcrypt hashing
- **Testing**: Comprehensive unit and integration tests
- **Deployment**: Automated CI/CD with GitHub Actions

## 📁 Project Structure

```
├── secure_aws_shopping.py      # Main FastAPI application
├── frontend/                   # SPA frontend
├── database/                   # AWS PostgreSQL integration
├── scripts/                    # Automation scripts
├── tests/                      # Test suites
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── config/                     # Configuration
│   └── test/                   # Test configuration
├── docs/                       # Documentation
└── .github/                    # GitHub workflows
```

## 🔧 Environment Configuration

### Production (.env)
```env
AWS_DB_HOST=your-rds-endpoint.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=smart_shopping
AWS_DB_USER=your_username
AWS_DB_PASSWORD=your_password
JWT_SECRET_KEY=your-super-secret-key
```

### Testing (.env.test)
```env
TEST_AWS_DB_HOST=your-test-rds-endpoint.amazonaws.com
TEST_AWS_DB_NAME=smart_shopping_test
TEST_JWT_SECRET_KEY=test-secret-key
```

## 🧪 Testing Strategy

### Test Environments
- **Unit Tests**: Isolated component testing
- **Integration Tests**: API and database integration
- **End-to-End Tests**: Complete user workflows

### Test Configuration
- Separate test database and configuration
- Mock external services
- Automated test data setup and teardown

## 🚀 Deployment

### GitHub Actions CI/CD
- Automated testing on push/PR
- Separate test and production environments
- Database migration and deployment

### Manual Deployment
```bash
python scripts/production_setup.py
```

## 📚 Documentation

- [API Documentation](http://localhost:8888/admin/docs)
- [Production Guide](docs/PRODUCTION_DEPLOYMENT_GUIDE.md)
- [AWS Setup](docs/AWS_SETUP.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)

## 🛡️ Security Features

- JWT authentication with secure sessions
- bcrypt password hashing
- AWS RDS PostgreSQL with encryption
- CORS protection
- Protected API routes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for intelligent shopping experiences**
