# Smart Shopping Platform - Secure AWS Integration

## 🎯 Overview

This is a **production-ready, secure smart shopping platform** that enforces AWS PostgreSQL authentication for all features. The system is designed to:

- ✅ **Require user registration/login** for ALL website access
- ✅ **Store all data in AWS PostgreSQL** (no local-only data)
- ✅ **Integrate crawler and user input** with AWS database
- ✅ **Provide secure JWT authentication** with bcrypt password hashing
- ✅ **Support GitHub Pages frontend** deployment with API backend

## 🏗️ Architecture

### Backend (Python FastAPI)
- **File**: `secure_aws_shopping.py`
- **Database**: AWS PostgreSQL (managed by `database/aws_postgresql_manager.py`)
- **Security**: JWT tokens, bcrypt passwords, CORS, activity logging
- **Features**: User auth, shopping lists, price comparison, savings analysis, promotions

### Frontend (HTML/JavaScript SPA)
- **File**: `frontend/index.html` + `frontend/js/app.js`
- **Framework**: Bootstrap 5 + Vanilla JavaScript
- **Security**: JWT-enforced API calls, secure token management
- **Features**: Registration, login, protected dashboard with all shopping features

### Database Schema
- **File**: `database/aws_postgresql_schema.sql`
- **Tables**: Users, products, stores, shopping lists, promotions, price history, analytics
- **Features**: Triggers, functions, indexes for performance

## 🔐 Security Features

### Authentication & Authorization
- **Registration**: Email-based with password strength requirements
- **Login**: Secure email/password with JWT token response
- **Token Management**: 24-hour expiry with auto-refresh
- **Protected Routes**: All API endpoints require valid JWT

### Data Protection
- **Password Hashing**: bcrypt with salt
- **CORS**: Configured for secure cross-origin requests
- **Activity Logging**: All user actions logged to database
- **Input Validation**: Comprehensive validation on all inputs

## 🚀 Deployment Options

### Local Development
```bash
python quick_start.py
# Access: http://localhost:8000
```

### GitHub Pages Frontend + API Backend
1. **Frontend**: Deploy `frontend/` folder to GitHub Pages
2. **Backend**: Deploy `secure_aws_shopping.py` to cloud server (Heroku, AWS, etc.)
3. **Update**: Change `apiBaseUrl` in `frontend/js/app.js` to your API server

### Production Server
- Deploy both frontend and backend together
- Use HTTPS/SSL certificates
- Add rate limiting and additional security

## 📊 Features Integration with AWS DB

### User Management
- **Registration**: Creates user in AWS `users` table
- **Login**: Validates against AWS database
- **Profile**: Stores location and preferences in AWS

### Shopping Lists
- **Create/Read/Update/Delete**: All operations in AWS `shopping_lists` table
- **Items**: Stored in AWS `shopping_list_items` table
- **Persistence**: Lists survive browser sessions

### Price Comparison & Savings
- **Data Source**: AWS `products` and `price_history` tables
- **Analysis**: Real-time comparison across stores
- **Savings**: Calculated from AWS promotional data

### Store Promotions
- **Source**: AWS `promotions` table
- **Updates**: Crawler data flows directly to AWS
- **Display**: Real-time promotional pricing

## 🛠️ Configuration

### Environment Variables (.env)
```env
# AWS Database
AWS_DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=postgres
AWS_DB_USER=your_username
AWS_DB_PASSWORD=your_password

# Security
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Required Dependencies
```bash
pip install fastapi[all] uvicorn[standard] psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart jinja2 python-dotenv pandas
```

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - User login with email/password
- `GET /auth/verify-token` - Validate JWT token
- `POST /auth/refresh-token` - Refresh expired token
- `POST /auth/logout` - User logout

### Protected Features (Require JWT)
- `GET /api/shopping-lists` - Get user's shopping lists
- `POST /api/shopping-lists` - Create new shopping list
- `DELETE /api/shopping-lists/{id}` - Delete shopping list
- `POST /api/analyze-savings` - Savings analysis
- `POST /api/compare-stores` - Price comparison
- `GET /api/promotions` - Current promotions

### System
- `GET /api/system-health` - System status and stats
- `GET /admin/docs` - API documentation (Swagger)

## 🔄 Data Flow

### User Input → AWS Database
1. User registers/logs in → `users` table
2. User creates shopping list → `shopping_lists` table
3. User adds items → `shopping_list_items` table
4. User queries products → Real-time AWS data retrieval

### Crawler Data → AWS Database
1. Crawler scrapes store data → AWS `products` table
2. Price updates → AWS `price_history` table
3. Promotions → AWS `promotions` table
4. Store info → AWS `stores` table

### Frontend ↔ Backend ↔ AWS
```
Frontend (JWT Auth) → API Endpoints → AWS PostgreSQL → Response → Frontend
```

## 🎨 Frontend Features

### Authentication Flow
1. **Landing**: Shows login/register forms
2. **Validation**: Client-side and server-side validation
3. **Success**: JWT token stored, redirected to dashboard
4. **Protection**: All features require valid token

### Dashboard Features
- **Savings Analysis**: Search products, compare prices
- **Shopping Lists**: Create, view, manage lists
- **Promotions**: Browse current deals
- **Store Comparison**: Side-by-side price comparison

## 🔧 Development Workflow

### Setup
1. Clone repository
2. Configure `.env` with AWS credentials
3. Run `python quick_start.py`
4. Access `http://localhost:8000`

### Testing
- **Backend**: API tests with authenticated requests
- **Frontend**: Manual testing of all features
- **Database**: Verify data persistence in AWS

### Deployment
1. **Prepare**: Update API URLs for production
2. **Backend**: Deploy to cloud server with HTTPS
3. **Frontend**: Deploy to GitHub Pages or static hosting
4. **Test**: End-to-end authentication and features

## 📈 Scalability & Performance

### AWS Database Optimizations
- Indexed columns for fast queries
- Connection pooling for concurrent users
- Triggers for automated data maintenance

### Security Hardening
- Rate limiting (add middleware)
- Email verification (extend registration)
- Password reset functionality
- Session management improvements

## 🎯 Success Criteria

✅ **Frontend Access Control**: Only registered/logged-in users can access features
✅ **AWS Database Integration**: All data stored and retrieved from AWS PostgreSQL
✅ **Secure Authentication**: JWT-based with proper validation
✅ **Data Persistence**: User data survives browser sessions
✅ **Real-time Features**: Price comparison, promotions, savings analysis
✅ **Production Ready**: Secure, scalable, deployable

## 🚀 Next Steps

1. **Deploy to Production**: Set up HTTPS API server
2. **GitHub Pages**: Deploy frontend with production API URL
3. **Monitor Performance**: AWS CloudWatch, error tracking
4. **Enhance Security**: Rate limiting, email verification
5. **Add Features**: More advanced analytics, notifications

---

**🔒 Security Note**: This platform enforces AWS database authentication for ALL features. Users must register or have existing credentials in your AWS PostgreSQL database to access any functionality.
