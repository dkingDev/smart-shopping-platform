# Smart Shopping Platform - Project Structure

## 📁 Project Organization

This document outlines the clean, organized structure of the Smart Shopping Platform project.

## 🏗️ Directory Structure

```
smart-shopping-platform/
├── 📁 config/                 # Configuration files
│   ├── cloudflare-*.js        # Cloudflare configurations
│   ├── domain-config.js       # Domain settings
│   ├── ssl-certificates.conf  # SSL configuration
│   └── security-*.md          # Security documentation
├── 📁 database/               # Database schema and data
│   ├── aws_postgresql_*.sql   # Database schemas
│   ├── aws_postgresql_manager.py
│   └── imports/               # Sample data and references
├── 📁 frontend/               # Client-side application
│   ├── index.html
│   ├── index.production.html
│   └── js/                    # JavaScript files
├── 📁 scripts/                # Utility and setup scripts
│   ├── production_setup.py
│   ├── github_setup.py
│   └── *.py                   # Various automation scripts
├── 📁 docs/                   # Documentation
│   ├── PROJECT-STRUCTURE.md   # This file
│   ├── SECURITY-BREACH-RESOLVED.md
│   └── deployment guides
├── 📁 company-website/        # Corporate website
└── 🔧 Root files              # Core application files
    ├── secure_aws_shopping.py # Main application
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Environment variables (local only)
    ├── .gitignore            # Git exclusions
    └── README.md             # Project overview
```

## 🔒 Security & Privacy

### Files Never Committed to Git:
- `.env*` - Environment variables and secrets
- `*.pem` - SSH keys and certificates
- `ec2-key.pem` - AWS EC2 access key
- `*.key` - Any private keys
- `config.ini` - Local configuration files
- `logs/` - Application logs
- `build/` - Build artifacts

### Protected Information:
- AWS credentials
- Database passwords
- JWT secret keys
- SSL certificates
- SSH keys
- API tokens

## 🚀 Deployment

The project uses:
- **AWS EC2** for hosting
- **AWS RDS PostgreSQL** for database
- **Cloudflare** for DNS, SSL, and security
- **Environment variables** for secrets management

## 📋 Usage

1. **Development**: Use local `.env` file for configuration
2. **Production**: Set environment variables on the server
3. **Deployment**: Use the deployment scripts in `/scripts/`
4. **Security**: Follow the security guidelines in `/docs/`

## 🔄 Maintenance

- Keep `.gitignore` updated for new sensitive file types
- Regularly audit files being committed to Git
- Update documentation when project structure changes
- Review security settings periodically

---
**Note**: This project structure ensures security, maintainability, and clean separation of concerns.
